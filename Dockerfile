FROM python:3.10

ENV TRANSFORMERS_OFFLINE=1
ENV HF_DATASETS_OFFLINE=1
ENV LANGUAGE_DETECT_MODELS_PATH=/opt/language_detect_models
ENV TRANSLATION_MODELS_PATH=/opt/translation_models
ENV CERTS_PATH=/opt/certs

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app /app

CMD gunicorn \
    -w 4 \
    -b 0.0.0.0:5000 \
    --keyfile "${CERTS_PATH}/localhost.key" \
    --certfile "${CERTS_PATH}/localhost.crt" \
    app:app