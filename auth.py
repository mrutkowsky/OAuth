from flask import Flask, request
import json
import hashlib
import authModel

@app.route("/client", methods=["POST", "DELETE"])
def client():
    if request.method == "POST":
        client_id = request.form.get("client_id")
        client_secret_input = request.form.get("is_admin")

        hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
        hashed_client_secret = hash_object.hexdigest()

        createResponse = authModel.create(client_id, hashed_client_secret, is_admin)
        return {'success' : createResponse}

    elif request.method == "DELETE":
        return {'success' : False}
    else:
        return {'success' : False}


@app.route("/auth", methods=["POST"])
def auth():    
    client_id = request.form.get("client_id")
    client_secret_input = request.form.get("client_secret")

    hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    authentication = authModel.authenticate(client_id, hashed_client_secret)
    if authentication == False:
        return {'success': False}
    else: 
        return json.dumps(authentication)

@app.route("/verify", methods=["POST"])
def verify():
    authorizationHeader = request.headers.get('authorization')    
    token = authorizationHeader.replace("Bearer ","")
    verification = authModel.verify(token)
    return verification

@app.route("/logout", methods=["POST"])
def logout():
    token = request.form.get("token")
    status = authModel.blacklist(token)
    return {'success': status}