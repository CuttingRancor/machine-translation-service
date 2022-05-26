# Machine Translation Service
Translation flask API for the Helsinki NLP models available in the [Huggingface Transformers library](https://huggingface.co/Helsinki-NLP). 

## Usage
### Language Detect Models  
Clone models from Hugging Face to machine-translation-service/lang_detect_models (Requires git-lfs)  

### Translation models  
Download language translation models using the command line utility.  
These get saved to machine-translation-service/data  
For example...

```
cd machine-translation-service
python download_models.py --source es --target en
```
For multiple languages:  
(CAUTION - this model detects languages and does not use the the apps language detection)
```
cd machine-translation-service
python download_models.py --source mul --target en
```
### Certificates
Certificates are required to run the app. Test certificates can be created with:
```
./gen_certs.sh
```
### Running the service
To run with Python>=3.6:

```
pip install -r requirements.txt
cd app
flask run [--reload]
```

To run with docker:

```
docker build -t machine-translation-service .
docker-compose up [-d]
```

The front end should then become available at https://localhost:5000.

Call the service with curl:
```
curl --location --request POST 'https://localhost:5000/translate' \
--header 'Content-Type: application/json' \
--cacert './certs/localhost.crt' \
-d '{
 "text":"Hola, soy Chris"
}'
```