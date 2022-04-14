# formpy-app

Checkout the live website [here](https://formpy.ismailmo.com)!

---

Formpy started out as a bunch of scripts sitting on local machine to help speed up the processing of hand-filled paper forms in a manufacturing plant to track productivity. Using openCV to process the scanned documents (aligning the pages and detecting filled in answers) - the data was easily digitised at scale which opened up a whole range of possibilities for data analysis and insights to improve operational efficiency.

It has now evolved into this website: a platform to open up a wide range of use cases, where users can build their own forms and use them to scale up their own data gathering processes.

---
### You can also deploy this website to use locally:

clone this repo

```
git clone https://github.com/ismailmo1/formpy-app.git
```

add secrets folders and files

``` 
cd formpy-app
mkdir secrets && cd secrets
touch mongo_root_pwd.txt mongo_pwd.txt mongo_root_user.txt mongo_user.txt 
```

add .env file and and environment variables

```
cd ../app
touch .env
```

edit the .env file to add the environment variables for the flask application (mongo user/password must match the mongo_user and mongo_pwd secrets defined in the secrets folder above)

```
FLASK_SECRET=secret
MONGODB_USERNAME=user
MONGODB_PASSWORD=pass
```

Build, create and run the containers

```
docker-compose up -d
```

your app should now be available at http://localhost:5000

Feel free to open an issue on this repo or [contact me](mailto:ismailmo4@gmail.com) if you have any issues.
