export LANGUAGE_DETECT_MODELS_PATH=../language_detect_models
export TRANSLATION_MODELS_PATH=../translation_models
export CERTS_PATH=../certs
gunicorn -w 4 -b 0.0.0.0:5000 --keyfile "${CERTS_PATH}/localhost.key" --certfile "${CERTS_PATH}/localhost.crt" --chdir app app:app