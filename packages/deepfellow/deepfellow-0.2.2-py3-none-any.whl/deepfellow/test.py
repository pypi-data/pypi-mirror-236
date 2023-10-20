
from abc import ABC
import json
import logging
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig, TextIteratorStreamer

from ts.torch_handler.base_handler import BaseHandler
from ts.protocol.otf_message_handler import send_intermediate_predict_response

logger = logging.getLogger(__name__)


class TestDeepFellow(BaseHandler, ABC):
    """
    BaseDeepFellow base handler.
    """
    def __init__(self):
        super(TestDeepFellow, self).__init__()
        self.initialized = False

    def set_model_dir(self):
        return None

    def initialize(self, ctx):
        self.context = ctx
        self.metrics = self.context.metrics
        self.manifest = ctx.manifest
        properties = ctx.system_properties

        self.set_model_dir()

        if self.model_dir == None:
            raise "Set model directory by overriding method set_model_dir() and setting self.model_dir to a directory containing model files."
    
        ### 
        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")
        logger.info(f"Device: {self.device}")
        
        
        # Read model serialize/pt file
        self.model, self.tokenizer = self.load_model()

        self.streamer = TextIteratorStreamer(self.tokenizer, 
                                    skip_prompt=True, 
                                    timeout=3,
                                    decoder_kwargs=dict(clean_up_tokenization_spaces=True))

        self.model.eval()

        logger.debug('Transformer model from path {0} loaded successfully'.format(self.model_dir))

        # Read the mapping file, index to object name
        mapping_file_path = os.path.join(self.model_dir, "index_to_name.json")

        if os.path.isfile(mapping_file_path):
            with open(mapping_file_path) as f:
                self.mapping = json.load(f)
        else:
            logger.warning('Missing the index_to_name.json file. Inference output will not include class name.')

        self.initialized = True

    def load_model(self):
        model_dir = self.model_dir
        properties = self.context.system_properties
        config = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)
        config.init_device = 'meta' # For fast initialization directly on GPU

        model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            config=config,
            device_map=int(properties.get("gpu_id")),
            load_in_8bit=True,
            trust_remote_code=True
        )
        ### More args?
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        return model, tokenizer

    def parse_request(self, req):
        data = req[0].get("data")
        if data is None:
            data = req[0].get("body")
        
        prompt = data.get("prompt")
        try:
            self.max_new_tokens = int(data.get("max_new_tokens"))
            if self.max_new_tokens is None:
                self.max_new_tokens = 128
        except:
            self.max_new_tokens = 128

        self.cmd = "inference" if data.get("cmd") != "tokencounter" else "tokencounter"

        return prompt

    def tokenize(self, prompt):
        tokens = self.tokenizer.encode_plus(
            prompt,
            add_special_tokens=True,
            return_tensors="pt"
        )
        return tokens
    
    def preprocess(self, req):
        
        prompt = self.parse_request(req)
        logger.info(f"Received prompt: {prompt}")
        tokens = self.tokenize(prompt)
        logger.info(f"Finished tokenization.")

        return tokens
    
    def inference(self, inputs):
        from threading import Thread

        generation_kwargs = dict(
            inputs=inputs['input_ids'].to(self.device), 
            max_new_tokens=self.max_new_tokens, 
            do_sample=True, 
            top_p=0.95, 
            top_k=60,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
            streamer=self.streamer
        )
        
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        for new_text in self.streamer:
            if new_text != "":
                new_text = new_text.replace(self.tokenizer.eos_token, '')
                yield {"delta":new_text, "tokens": len(self.tokenizer.encode(new_text))}
        thread.join()

    def postprocess(self, inference_output):
        # TODO: Add any needed post-processing of the model predictions here
        return inference_output

    def _is_describe(self):
        if self.context and self.context.get_request_header(0, "describe"):
            if self.context.get_request_header(0, "describe") == "True":
                return True
        return False

    def describe_handle(self):
        """Customized describe handler
        Returns:
            dict : A dictionary response.
        """
        output_describe = {"DeepFellow": {
            "max_seq_len": self.model.config.max_seq_len
        }}

        logger.info("Collect customized metadata")

        return output_describe

    


    def handle(self, data, context):
        try:
            if not self.initialized:
                self.initialize(context)

            if data is None:
                return None

            if self._is_describe():
                return [self.describe_handle()]

            data = self.preprocess(data)

            if self.cmd == "tokencounter":
                return [{"tokencount": len(data['input_ids'][0])}]

            if self.cmd == "inference":
                for text in self.inference(data):
                    send_intermediate_predict_response(
                        [text], 
                        context.request_ids, 
                        "Intermediate Prediction success", 
                        200, 
                        context)
            return [""]
        
        except Exception as e:
            raise e

_service = TestDeepFellow()
