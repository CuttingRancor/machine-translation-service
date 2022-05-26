"""Language Detection & Translation App"""
import os
from flask import Flask, request, jsonify
from language_available import LanguageAvailable
from language_detect import DetectLanguage
from translate import Translator

app = Flask(__name__)
TRANSLATION_MODELS_PATH = os.environ['TRANSLATION_MODELS_PATH']
translator = Translator(TRANSLATION_MODELS_PATH)

app.config["DEBUG"] = False  # turn off in prod


@app.route('/', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return "Machine translation service is up and running."


@app.route('/lang_routes', methods=["GET"])
def get_lang_route():
    """Return a list of languages the specified lang can transalte"""
    lang = request.args['lang']
    all_langs = translator.get_supported_langs()
    lang_routes = [lng for lng in all_langs if lng[0] == lang]
    return jsonify({"output": lang_routes})


@app.route('/supported_languages', methods=["GET"])
def get_supported_languages():
    """Return a list of supported languages"""
    langs = translator.get_supported_langs()
    return jsonify({"output": langs})


@app.route('/translate', methods=["POST"])
def get_prediction():
    """Main Translation route"""
    # detect source language
    text = request.json['text']
    source, source_full = DetectLanguage().detect(text)
    # check if the language is availble for translation
    lang_available = LanguageAvailable(TRANSLATION_MODELS_PATH, source).available
    if not lang_available:
        # Try the multi-language model
        source = "mul"

    target = 'en'
    # translate
    success, model_name, translation = translator.translate(source, target, text)
    return jsonify({"detected_language": source_full,
                    "translation_successful": bool(success),
                    "translation_model": model_name,
                    "output": translation})
