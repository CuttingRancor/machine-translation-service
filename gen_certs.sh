# Delete certs if they exist
rm -rf ./certs
# Create and go to the certs directory
mkdir certs && cd certs
# Make the key and self-signed certificate. A signed certificate should be used in Production environments
openssl req -newkey rsa:2048 -nodes -keyout localhost.key -x509 -sha256 -days 3650 -subj /CN=localhost -out localhost.crt