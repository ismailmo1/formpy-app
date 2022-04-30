def test_register_get(client):
    res = client.get("/register")

    assert res.status_code == 200
    assert b"<h1>Register</h1>" in res.data
    assert b'<form action="/register" method="post">' in res.data


def test_register_post(client):
    form_data = {
        "username": "ismailmo",
        "first_name": "ismail",
        "last_name": "test",
        "email": "ismail@ismail.com",
        "password": "test",
        "password2": "test",
    }
    res = client.post("/register", data=form_data, follow_redirects=True)

    assert res.status_code == 200
    assert len(res.history) == 1
    assert res.request.path == "/login"
    assert b"user created successfully" in res.data


def test_login(client, db_user):
    res = client.post(
        "/login",
        data={"username": "test_user", "password": "test"},
        follow_redirects=True,
    )

    assert res.status_code == 200
    assert len(res.history) == 1
    assert res.request.path == "/view"
    assert b"welcome back test_user!" in res.data


def test_wrong_pass_login(client, db_user):

    res = client.post(
        "/login",
        data={"username": "test_user", "password": "wrong_password"},
        follow_redirects=True,
    )

    assert res.status_code == 200
    assert b"Invalid username or password" in res.data


def test_logout(logged_in_client):

    from flask_login import current_user

    assert current_user.is_authenticated

    res = logged_in_client.get(
        "/logout",
        follow_redirects=True,
    )

    assert current_user.is_authenticated == False
    assert b"bye!" in res.data


def test_edit_user(logged_in_client):
    form_data = {
        "username": "updated_uname",
        "first_name": "updated_fname",
        "last_name": "updated_lname",
        "email": "updated@updated.com",
        "password": "updated_password",
        "password2": "updated_password",
    }
    res = logged_in_client.post(
        "/user/edit",
        data=form_data,
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert b"user changed successfully!" in res.data
    assert b"Hi updated_fname" in res.data


def test_delete_user(logged_in_client):
    from flask_login import current_user

    form_data = {"delete_options": "none"}
    res = logged_in_client.post(
        "/user/delete", data=form_data, follow_redirects=True
    )

    assert res.status_code == 200
    assert current_user.is_authenticated == False
    assert b"user deleted, sorry to see you go test_user!" in res.data
