"""Check if a language model is available for translation"""
import os


class LanguageAvailable:
    """Language Model check Class"""

    def __init__(self, model_path, language) -> None:
        """Initialise the class"""
        self.model_path: str = model_path
        self.language: str = language
        self.dwnld_lang: list = []
        self.available: bool = False
        self._get_downloaded_langs()
        self._language_available()

    def _get_downloaded_langs(self):
        """Get a list of downloaded languages"""
        download_list = os.listdir(self.model_path)
        self.dwnld_lang = [
            x.replace("opus-mt-", "").replace("-en", "") for x in download_list]

    def _language_available(self):
        """Check if the language is available for translation"""
        self.available = bool(self.language in self.dwnld_lang)
