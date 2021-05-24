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
            {"username": data.username, "content": data.content, "user_id": data._id, 'created_at': datetime.datetime.now()})
        return True

    def get_all_posts(self):
        all_posts = self.Posts.find()
        new_posts = []

        for post in all_posts:
            post["user"] = self.Users.find_one({"_id": post["user_id"]})
            post["timestamp"] = humanize.naturaltime(
                datetime.datetime.now() - post['created_at'])
            comments = self.Comments.find(
                {"post_id": str(post["_id"])})
            post["old_comments"] = comments
            post["comments"] = []

            for comment in post["old_comments"]:
                comment['user'] = self.Users.find_one(
                    {"_id": comment["user_id"]})
                comment["timestamp"] = humanize.naturaltime(
                    datetime.datetime.now() - comment['created_at'])
                post["comments"].append(comment)

            new_posts.append(post)

        return new_posts

    def get_user_posts(self, user):
        all_posts = self.Posts.find(
            {"user_id":  user["_id"]}).sort("created_at", -1)
        new_posts = []

        for post in all_posts:
            post["user"] = self.Users.find_one({"_id": post["user_id"]})
            new_posts.append(post)

        return new_posts

    def add_comment(self, data):

        if data['comment-content'] == '':
            return False
        inserted_comment = self.Comments.insert_one(
            {"post_id": data["post_id"], "content": data["comment-content"], 'created_at': datetime.datetime.now(), "user_id": data["user_id"]})

        return inserted_comment
