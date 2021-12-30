mongosh -- "$MONGO_INITDB_DATABASE" <<EOF
    var rootUser = '$(cat "$MONGO_INITDB_ROOT_USERNAME_FILE")';
    var rootPassword = '$(cat "$MONGO_INITDB_ROOT_PASSWORD_FILE")';
    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);

    var user = '$(cat "$MONGO_INITDB_USERNAME_FILE")';
    var passwd = '$(cat "$MONGO_INITDB_PASSWORD_FILE")';
    var dbName = "$MONGO_INITDB_DATABASE"
    db.createUser({user: user, pwd: passwd, roles: [{role: "readWrite", db:dbName}]});
EOF