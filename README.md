# formpy-app

Checkout the live website [here](https://formpy.ismailmo.com)!

The [formpy library]( https://github.com/ismailmo1/formpy) is open if you'd like to create your own applications.

---

### To use locally:

clone this repo

```git clone```

add secrets folders and files

``` 
mkdir secrets
touch mongo_root_pwd.txt mongo_pwd.txt mongo_root_user.txt mongo_user.txt 
```

add .env file and and environment variables

```touch app/.env```

add FLASK_SECRET environment variable

```
FLASK_SECRET=secret
MONGODB_USERNAME=user
MONGODB_PASSWORD=pass
```
