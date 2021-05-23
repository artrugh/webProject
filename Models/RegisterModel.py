from pymongo import MongoClient
import bcrypt


class RegisterModelCls:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codeWizard
        self.Users = self.db.users

    def insert_user(self, data):

        if data['username'] == "" or data['password'] == "" or data['email'] == "":
            return 'missed data'

        user = self.Users.find_one({"email": data.email})

        if user:
            return 'user already exists'

        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        id = self.Users.insert(
            {"username": data.username, "name": data.name, "password": hashed, "email": data.email})
        print("Uid is: ", id)
        myuser = self.Users.find_one({"username": data.username})

        if bcrypt.checkpw("avocado1".encode(), myuser["password"]):
            print("this matches")
