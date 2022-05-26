"""Download models for the translation service"""
import os
import argparse
import urllib
from urllib.request import urlretrieve
from config import HUGGINGFACE_S3_BASE_URL, FILENAMES

TRANSLATION_MODELS_PATH = os.environ['TRANSLATION_MODELS_PATH']

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, help="source language code")
parser.add_argument(
    "--target", type=str, help="sum the integers (default: find the max)"
)


def download_language_model(source, target):
    """Download function"""
    model = f"opus-mt-{source}-{target}"
    print(f">>>Downloading data for {source} to {target} model...")

    model_path = os.path.join(TRANSLATION_MODELS_PATH, model)
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    for file in FILENAMES:
        file_list = os.listdir(model_path)
        if file not in file_list:
            try:
                print(os.path.join(HUGGINGFACE_S3_BASE_URL, model, file))
                urlretrieve(
                    "/".join([HUGGINGFACE_S3_BASE_URL, model, file]),
                    os.path.join(model_path, file),
                )
                print("Download complete!")
            except urllib.error.HTTPError:
                print("Error retrieving model from url. Please confirm model exists.")  # NOQA
                os.rmdir(os.path.join("data", model))
                break


if __name__ == "__main__":
    args = parser.parse_args()
    download_language_model(args.source, args.target)
