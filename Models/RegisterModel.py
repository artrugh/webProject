import pymongo
from pymongo import MongoClient


class RegisterModelCls:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codeWizard
        self.Users = self.db.users


    def insert_user(self, data):

        id = self.Users.insert({"username": data.username,"name": data.name, "password": data.password, "email": data.email })
        print("Uid is: ", id)

