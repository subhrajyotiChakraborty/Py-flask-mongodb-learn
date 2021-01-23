import jsonschema
from flask import Flask, request, jsonify, Response,json
from pymongo import MongoClient
from flask_jsonschema_validator import JSONSchemaValidator


app = Flask(__name__)
JSONSchemaValidator(app=app, root="schemas")

client = MongoClient('mongodb://localhost:27017/')
db = client['test-database']
collection = db['test-collection']


@app.errorhandler( jsonschema.ValidationError )
def onValidationError( e ):
  return Response( "There was a validation error: " + str( e ), 400 )


@app.route("/register", methods=["POST"])
@app.validate( 'users', 'register' )
def register_user():
    user = request.json

    try:
        users = db.users
        users.insert_one(user)
    except:
        print("Unable to insert user")
        return  {"message": "Unable to insert user"}, 500

    return {"message": "User created successfully"}, 201


@app.route("/get-user",)
def get_users():
    try:
        documents = db.users.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        response = output
    except:
        return {"message": "Unable to fetch users"}, 400

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
