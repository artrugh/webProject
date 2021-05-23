from pymongo import MongoClient
import bcrypt
import json


class SignupModelCls:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codeWizard
        self.Users = self.db.users

    def insert_user(self, data):

        if data['username'] == "" or data['password'] == "" or data['email'] == "":
            return json.dumps({"error": True, "msg": "missed data"})

        user = self.Users.find_one({"email": data.email})

        if user:
            return json.dumps({"error": True, "msg": "user already exists"})

        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        id = self.Users.insert(
            {"username": data.username, "password": hashed, "email": data.email})
        print("Uid is: ", id)
        myuser = self.Users.find_one({"username": data.username})

        if bcrypt.checkpw(data['password'].encode(), myuser["password"]):
            print("this matches")
            return json.dumps({"username": data.username})
