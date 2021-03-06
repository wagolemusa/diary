from functools import wraps

import datetime

from flask import jsonify, Flask, request, session
from my_class import ExternalFunctions

app = Flask(__name__)
app.config["SECRET_KEY"] = 'kkkoech'
user_details = dict()
diary_entries = dict()


@app.route("/api/v1", methods=['GET'])
def home():
    return jsonify({"message":"welcome to my diary"})
@app.route("/api/v1/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        fname = data["fname"]
        lname = data["lname"]
        email = data["email"]
        username = data["username"]
        password = data["password"]
        cpassword = data["cpassword"]
        if ExternalFunctions.valid_email(email):
            if ExternalFunctions.password_verify(password, cpassword):
                if fname.strip() == '' or lname.strip() == '' or \
                username.strip() == '' or password.strip() == '':
                    return jsonify("fields cannot be empty"), 422
                else:
                    if username not in user_details:
                        user_details.update({username:{"name":fname+" "+lname, \
                        "email":email, "password":password}})
                    else:
                        return jsonify({"message":"such user already exists"}), 409
            else:
                return jsonify({"message":"password and confirm password do not match"}), 403
        else:
            return jsonify("email is invalid"), 403
        return jsonify({"message":"success ! you can now login to continue"}), 200
    except KeyError:
        return jsonify('fname, lname, email, username, password, cpassword should be provided'), 422

@app.route("/api/v1/login", methods=['POST'])
def login():
    try:
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        if username in user_details:
            if password == user_details[username]["password"]:
                session['username'] = username
                session['logged_in'] = True
                return jsonify({"message":"you are successfully logged in "}), 200
            return jsonify({"message":"wrong password, try again"}), 401
        return jsonify({"message":"you are not a registered user"}), 403
    except KeyError:
        return jsonify('username and passwordshould be provided'), 422
def on_session(t):
    @wraps(t)
    def decorator(*a, **kw):
        if "logged_in" in session:
            return t(*a, **kw)
        return jsonify({"message":"please login first"}), 401
    return decorator

@app.route("/api/v1/create_entry", methods=['POST'])
@on_session
def create_entry():
    try:
        comment = request.get_json()["comment"]
        username = session.get('username')
        if username not in diary_entries:
            diary_entries.update({username:{1:str(datetime.datetime.utcnow())+" "+comment}})
        else:
            diary_entries[username].update\
            ({len(diary_entries[username])+1:str(datetime.datetime.utcnow())+" "+comment})
        return jsonify(diary_entries[username]), 200
    except KeyError:
        return jsonify('comment should be provided'), 422

@app.route("/api/v1/entries", methods=['GET'])
@on_session
def entries():
    try:
        username = session.get('username')
        return jsonify(diary_entries[username]), 200
    except KeyError:
        return jsonify('ensure that you have made entries before'), 422

@app.route("/api/v1/view_entry/<int:entry_id>", methods=["GET"])
@on_session
def view_entry(entry_id):
    username = session.get('username')
    return jsonify({"entry "+str(entry_id):diary_entries[username][entry_id]}), 200

@app.route("/api/v1/delete_entry/<int:entry_id>", methods=["DELETE"])
@on_session
def delete_entry(entry_id):
    try:
        username = session.get('username')
        del diary_entries[username][entry_id]
        return jsonify({"message":"deleted successfully"}), 202
    except KeyError:
        return jsonify('you can only delete an \
        entry you made. please confirm you have an entry of id \
        '+str(entry_id)+' in http://127.0.0.1:5555/api/v1/entries'), 422
@app.route("/api/v1/modify_entry/<int:entry_id>", methods=["PUT"])
def modify_entry(entry_id):
    try:
        comment = request.get_json()["comment"]
        username = session.get('username')
        del diary_entries[username][entry_id]
        diary_entries[username].update({entry_id:str(datetime.datetime.utcnow())+" "+comment})
        return jsonify({"message":"successfully edited an entry"}), 200
    except KeyError:
        return jsonify('comment should be provided \
        and you should have made more than'+str(entry_id)+' comments to modify an entry'), 422

@app.route("/api/v1/account", methods=['GET'])
def account():
    username = session.get('username')
    my_details = {"name":user_details[username]['name'], "email":user_details[username]['email']}
    return jsonify(my_details), 200


@app.route("/api/v1/logout", methods=['GET'])
def logout():
    session.clear()
    return jsonify({"message":"successful"}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
