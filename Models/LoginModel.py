import bcrypt
from pymongo import MongoClient


class LoginModel:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codeWizard
        self.Users = self.db.users

    def check_user(self, data):
        user = self.Users.find_one({"email": data['email']})

        if user:
            if bcrypt.checkpw(data['password'].encode(), user["password"]):
                return user
            else:
                return False
        else:
            return False

    def update_info(self, data):
        self.Users.update_one({'email': data['email']}, {
            "$set": data
        })

        return True

    def get_profile(self, user):
        user_info = self.Users.find_one({"email": user['email']})
        return user_info

    def update_img(self, data):
        updated = self.Users.update_one({'_id': data['user_id']}, {
            "$set": {data["type"]: data["img"]}
        })

        return updated
