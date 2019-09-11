import pymongo, bcrypt
from pymongo import MongoClient


class Posts:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codeWizard
        self.Users = self.db.users
        self.Posts = self.db.posts

    def insert_post(self, data):
        inserted = self.Posts.insert({"username": data.username, "content": data.content})
        return True

