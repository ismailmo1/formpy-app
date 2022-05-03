
# run container with same settings as ../docker-compose.yml
# .env file for secrets
docker run -d --network linode-config_default --name formpy-flask --env FLASK_DEBUG=False --env FLASK_PORT=5000 --env FLASK_ENV=production --env FLASK_CONFIG_FILE=config/prod_config.py --env IMG_STORAGE_PATH=/var/www/app/static/image_storage/template_images --env DOCS_FOLDER_PATH=/static/docs --env MONGODB_HOSTNAME=mongodb --env MONGODB_DATABASE=formpydb --env VIRTUAL_HOST=formpy.ismailmo.com --env LETSENCRYPT_HOST=formpy.ismailmo.com -v appdata:/var/www -v userimages:/var/www/app/static/image_storage/template_images --env-file /home/ismail/formpy-app/app/.env ismailmo1/formpy-flask
# attach to network
docker network connect formpy-flask formpy-app_backend