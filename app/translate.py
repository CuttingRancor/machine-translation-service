"""Translation Scripts"""
import os
from typing import List
from transformers import MarianTokenizer, MarianMTModel


class Translator():
    """Translation Class"""

    def __init__(self, models_dir):
        """Initialise the class"""
        self.models: dict = {}
        self.models_dir: str = models_dir
        self.model_name: str = ""

    def get_supported_langs(self):
        """Return a list of languages found in the models dir"""
        routes = [x.split('-')[-2:] for x in os.listdir(self.models_dir)]
        return routes

    def load_model(self, route):
        """Load a downloaded model"""
        self.model_name = f'opus-mt-{route[0]}-{route[1]}'
        path = os.path.join(self.models_dir, self.model_name)

        if not os.path.exists(path):
            return 0, f"Make sure you have downloaded model {self.model_name} for translation"

        try:
            model = MarianMTModel.from_pretrained(path)
            tok = MarianTokenizer.from_pretrained(path)
        except Exception:
            return 0, f"Error loading model {self.model_name}"  # NOQA
        self.models[route] = (model, tok)
        return 1, f"Successfully loaded model {self.model_name} for transation"

    def translate(self, source, target, text):
        """Transaltion function

        :return: success code, model name, message/translation
        """
        route = (source, target)
        if not self.models.get(route):
            success_code, message = self.load_model(route)
            if not success_code:
                return 0, self.model_name, message

        batch = self.models[route][1].prepare_seq2seq_batch(
            src_texts=list([text]), return_tensors="pt")
        gen = self.models[route][0].generate(**batch)
        words: List[str] = self.models[route][1].batch_decode(
            gen, skip_special_tokens=True)
        return 1, self.model_name, words[0]
