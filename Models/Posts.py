from pymongo import MongoClient
import datetime
import humanize


class Posts:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codeWizard
        self.Users = self.db.users
        self.Posts = self.db.posts
        self.Comments = self.db.comments

    def insert_post(self, data):

        if data['content'] == '':
            return
        self.Posts.insert(
            {"username": data.username, "content": data.content, "user-id": data._id, 'created_at': datetime.datetime.now()})
        return True

    def get_all_posts(self):
        all_posts = self.Posts.find()
        new_posts = []

        for post in all_posts:
            post["user"] = self.Users.find_one({"_id": post["user-id"]})
            post["timestamp"] = humanize.naturaltime(
                datetime.datetime.now() - post['created_at'])
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

    def add_comment(self, data):
        if data['comment-content'] == '':
            return False
        inserted_comment = self.Comments.insert_one(
            {"post_id": data["post_id"], "content": data["comment-content"], 'created_at': datetime.datetime.now(), "user_id": data["user_id"]})

        return inserted_comment
