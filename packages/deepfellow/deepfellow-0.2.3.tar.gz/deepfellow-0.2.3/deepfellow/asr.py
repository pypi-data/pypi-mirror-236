
from abc import ABC
import json
import logging
import os

import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from ts.torch_handler.base_handler import BaseHandler
from ts.protocol.otf_message_handler import send_intermediate_predict_response

logger = logging.getLogger(__name__)


class ASRDeepFellow(BaseHandler, ABC):
    """
    BaseDeepFellow Automatic Speech Recognition handler.
    """
    def __init__(self):
        super(ASRDeepFellow, self).__init__()
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
            raise "Set model directory by overriding method set_model_dir() and setting self.model_dir to a directory that contains model files."
    
        ### 
        my_device = self.get_device(str(properties.get("gpu_id")))
        self.device = torch.device(my_device)
        logger.info(f"Device: {self.device}")
        
        
        # Read model serialize/pt file
        self.model, self.processor = self.load_model()

        self.model.eval()

        logger.debug('Model from path {0} loaded successfully'.format(self.model_dir))

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

        model = Wav2Vec2ForCTC.from_pretrained(
            model_dir,
            #device_map=int(properties.get("gpu_id")),
        )
        processor = Wav2Vec2Processor.from_pretrained(model_dir)

        ### More args?
        return model, processor


    def parse_request(self, req):
        import json
        data = req[0].get("data")
        if data is None:
            data = req[0].get("body")
        data = json.loads(data.decode('utf-8'))
        self.cmd = "inference" 
        prompt = data.get("prompt")

        return prompt

    def process_audio(self, prompt):
        import librosa
        import random
        import base64

        decoded = base64.b64decode(prompt)
        file_name = f"/home/patryk/speech2text/input/file{random.randint(0,3)}"
        with open(file_name, "wb") as fh:
            fh.write(decoded)
        
        audio, sr = librosa.load(file_name, sr=16_000)
        inputs = self.processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True)
        return inputs

    ###
    def preprocess(self, req):
        
        prompt = self.parse_request(req)
        logger.info(f"Received prompt.")
        processed_audio = self.process_audio(prompt)
        logger.info(f"Finished processing audio.")

        return processed_audio
    
    def audio_to_text(self, in_vals):
        with torch.no_grad():
            logits = self.model(in_vals.input_values, attention_mask=in_vals.attention_mask).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentences = self.processor.batch_decode(predicted_ids)
        #my_output[0] = predicted_sentences
        return predicted_sentences

    def inference(self, prcsd_audio):
        # from threading import Thread
        # try:
        #     my_output = [None]
        #     thread = Thread(target=self.audio_to_text, args=(prcsd_audio, my_output))
        #     thread.start()
        #     yield {"delta":output[0]}
        #     logger.log(output[0])
        #     thread.join()
        # except:
        #     yield {"delta":f"Inference error, please contact AI Specialist. \nMODEL: {self.model.__class__.__name__}", "tokens": 0}
        return self.audio_to_text(prcsd_audio)


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
            "max_seq_len": 0
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
                return [{"delta": "Not supported for ASR."}]

            if self.cmd == "inference":
                predictions = self.inference(data)
                logger.info(f"Output: {predictions}")
                return predictions
            return [""]
        
        except Exception as e:
            raise e

_service = ASRDeepFellow()
