
from abc import ABC
import json
import logging
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig, TextIteratorStreamer, BitsAndBytesConfig, GenerationConfig

from ts.torch_handler.base_handler import BaseHandler
from ts.protocol.otf_message_handler import send_intermediate_predict_response

logger = logging.getLogger(__name__)


class BaseDeepFellow(BaseHandler, ABC):
    """
    BaseDeepFellow base handler.
    """
    def __init__(self):
        super(BaseDeepFellow, self).__init__()
        self.initialized = False

    def set_model_dir(self):
        return None

    def get_device(self, gpu_id = None):
        if torch.cuda.is_available():
            return "cuda:" + gpu_id
        elif torch.backends.mps.is_available(): 
            return "mps"
        else:
            return "cpu"

    def initialize(self, ctx):
        self.context = ctx
        self.metrics = self.context.metrics
        self.manifest = ctx.manifest
        properties = ctx.system_properties

        self.set_model_dir()

        if self.model_dir == None:
            raise "Set model directory by overriding method set_model_dir() and setting self.model_dir to a directory containing model files."
    
        ### 
        
        self.my_device = self.get_device(str(properties.get("gpu_id")))
        self.device = torch.device(self.my_device)        
        logger.info(f"Device: {self.device}")
        
        
        # Read model serialize/pt file
        self.model, self.tokenizer = self.load_model()

        self.streamer = TextIteratorStreamer(self.tokenizer, 
                                    skip_prompt=True, 
                                    timeout=3,
                                    clean_up_tokenization_spaces=True,
                                    skip_special_tokens=True)

        self.generation_config = GenerationConfig(eos_token_id=self.tokenizer.eos_token_id,
                                                  pad_token_id=self.tokenizer.eos_token_id,)

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

        my_map = int(properties.get("gpu_id")) if properties.get("gpu_id") is not None else "mps"

        model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            config=config,
            device_map=my_map,
            #quantization_config=bnb_config,
            load_in_8bit=True if self.my_device != "mps" else False,
            trust_remote_code=True
        )
        ### More args?
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        return model, tokenizer

    def set_generation_parameter(self, data, param, default):
        """Sets generation_config parameter to a value.

        Tries to set param to value, if there's an error it sets param to default.

        Args:
            data (dict): dictionary from which value of "param" is taken,
            param (str): A valid GenerationConfig parameter name,
            default(int, float, str): Valid value to default to if setting param to "value" fails.

        Example:
            set_generation_parameter(data, "max_new_tokens", 128)
            Will take value from data and set to self.generation_config.max_new_tokens to that value.
            If "max_new_token" is of wrong type or is empty then it will default to setting that value to 128.
        """
        try:
            value = data.get(param)
            if value is None:
                raise ValueError("None isn't a valid value!")
            setattr(self.generation_config, param, value)
        except:
            setattr(self.generation_config, param, default)

    def parse_request(self, req):

        data = req[0].get("data")
        if data is None:
            data = req[0].get("body")

        self.cmd = "inference" if data.get("cmd") != "tokencounter" else "tokencounter"

        self.set_generation_parameter(data, "max_new_tokens", 128)
        self.set_generation_parameter(data, "temperature", 1.0)
        self.set_generation_parameter(data, "repetition_penalty", 1.0)
        
        self.generation_config.do_sample = True if self.generation_config.temperature > 0.0 else False
        
        prompt = data.get("prompt")

        return prompt

    def tokenize(self, prompt):
        tokens = self.tokenizer.encode_plus(
            prompt,
            add_special_tokens=True,
            return_tensors="pt"
        )
        return tokens
    ###
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
            generation_config=self.generation_config,
            streamer=self.streamer
        )
        self._gen_kwargs = generation_kwargs
        try:
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            for new_text in self.streamer:
                if new_text != "":
                    yield {"delta":new_text}
            thread.join()
        except:
            yield {"delta":f"Inference error, please contact AI Specialist. \nMODEL: {self.model.__class__.__name__}", "tokens": 0}

    def postprocess(self, inference_output):
        # Add any needed post-processing of the model predictions here
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
                return [{"delta": len(data['input_ids'][0])}]

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

_service = BaseDeepFellow()
