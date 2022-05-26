"""Detect language of text

source: https://huggingface.co/spaces/team-language-detector/LanguageDetector/blob/main/app.py
"""
import os
import pandas as pd
from transformers import pipeline, AutoModelForSequenceClassification


LANGUAGE_DETECT_MODELS_PATH = os.environ['LANGUAGE_DETECT_MODELS_PATH']


class DetectLanguage:
    """Class to detect languages"""

    def __init__(self) -> None:
        self.text: str = ""
        self.lang_df: pd.DataFrame
        self.dwnld_lang: list = [str]
        self.detect_df: pd.DataFrame = pd.DataFrame(
            [], columns=['model', 'label', 'score'])
        self._read_langs()

    def _read_langs(self):
        """Read Hugging Face languages from a file"""
        lang_file_path = "HuggingFaceLanguages.csv"
        if not os.path.exists(lang_file_path):
            raise FileNotFoundError(f"Missing File: {lang_file_path}")

        self.lang_df = pd.read_csv(lang_file_path)

    def detect(self, text):
        """Detect language based on text"""
        self.text = text

        # Get transformer model and set up a pipeline
        lang_detect_models = os.listdir(LANGUAGE_DETECT_MODELS_PATH)
        model_ckpt: list = [os.path.join(LANGUAGE_DETECT_MODELS_PATH, x) for x in lang_detect_models]
        # loop through the models to get the best match
        for model in model_ckpt:
            pipe = pipeline("text-classification", model=model)
            preds = pipe(self.text)

            label: str = preds[0]['label']
            score: int = preds[0]['score']

            # get the language code if the language name is returned
            if len(label) > 2:
                if label in self.lang_df['LanguageCaps'].values:
                    label = self.lang_df.loc[
                        self.lang_df['LanguageCaps'] == label,
                        "Code"].values[0]

            # add the new row to the dataframe
            new_row: pd.DataFrame = pd.DataFrame([[model[:5], label, score]],
                                                 columns=['model',
                                                          'label',
                                                          'score'])
            self.detect_df = pd.concat([self.detect_df, new_row])

        # sort the dataframe and return the top match
        sorted_df = self.detect_df.sort_values(by='score', ascending=False)
        detected_language = sorted_df['label'].values[0]
        # get full language name
        if len(detected_language) > 2:
            detected_language_full = detected_language
        else:
            detected_language_full = self.lang_df.loc[
                self.lang_df['Code'] == detected_language,
                "LanguageCaps"].values[0]

        return detected_language, detected_language_full
