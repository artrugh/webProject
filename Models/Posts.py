from pymongo import MongoClient


class Posts:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codeWizard
        self.Users = self.db.users
        self.Posts = self.db.posts

    def insert_post(self, data):

        if data['content'] == '':
            return
        self.Posts.insert(
            {"username": data.username, "content": data.content, "user-id": data._id})
        return True

    def get_all_posts(self):
        all_posts = self.Posts.find()
        new_posts = []

        for post in all_posts:
            post["user"] = self.Users.find_one({"_id": post["user-id"]})
            new_posts.append(post)

        return new_posts

    def get_user_posts(self, user):
        all_posts = self.Posts.find(
            {"user-id":  user["_id"]}).sort("date-added", -1)
        new_posts = []

        for post in all_posts:
            post["user"] = self.Users.find_one({"_id": post["user-id"]})
            new_posts.append(post)

        return new_posts
