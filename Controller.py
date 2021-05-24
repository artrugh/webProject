import web
from Models import SignupModel, LoginModel, Posts

web.config.debug = False

urls = (
    # views
    "/", "Home",
    "/signup", "SignUp",
    "/login", "Login",
    "/profile/(.*)", "UserInfo",
    "/settings", "UserSetttings",
    "/profile/(.*)", "UserProfile",

    # apis
    "/api/signup", "ControllerSignUp",
    "/api/login", "ControllerLogin",
    "/api/logout", "ControllerLogout",
    "/api/post-activity", "PostActivity",
    "/api/update-settings", "ControllerUpdateUserSettings",
    "/api/add-comment", "ControllerAddComment"
)
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore(
    "sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout", globals={
                             'session': session_data, 'current_user': session_data["user"]})


# Classes/routes

class Home:
    def GET(self):

        # auto-login
        data = {"email": "nick@nick.com", "password": "nick"}

        login = LoginModel.LoginModel()
        user = login.check_user(data)

        if user:
            session_data["user"] = user

        post_model = Posts.Posts()
        posts = post_model.get_all_posts()

        return render.Home(posts)


class SignUp:
    def GET(self):
        return render.SignUp()


class Login:
    def GET(self):
        return render.Login()


class ControllerSignUp:
    def POST(self):
        data = web.input()
        reg_model = SignupModel.SignupModelCls()
        res = reg_model.insert_user(data)
        if res != None:
            return res


class ControllerLogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        user = login.check_user(data)

        if user == False:
            return "error"

        session_data["user"] = user
        return user


class ControllerLogout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


class PostActivity:
    def POST(self):
        data = web.input()
        data['username'] = session_data['user']['username']
        data["_id"] = session_data['user']['_id']
        post_model = Posts.Posts()
        post_model.insert_post(data)
        return "success"


class UserProfile:
    def GET(self, user):
        # auto-login
        data = {"email": "nick@nick.com", "password": "nick"}

        login = LoginModel.LoginModel()
        user = login.check_user(data)

        if user:
            session_data["user"] = user

        post_model = Posts.Posts()
        posts = post_model.get_user_posts(user)

        user_info = login.get_profile(user)

        return render.Profile(posts, user_info)


class UserInfo:
    def GET(self, user):
        # auto-login
        data = {"email": "nick@nick.com", "password": "nick"}

        login = LoginModel.LoginModel()
        user = login.check_user(data)

        if user:
            session_data["user"] = user

        user_info = login.get_profile(user)

        return render.Info(user_info)


class UserSetttings:
    def GET(self):
        # auto-login
        data = {"email": "nick@nick.com", "password": "nick"}

        login = LoginModel.LoginModel()
        user = login.check_user(data)

        if user:
            session_data["user"] = user
        return render.Settings()


class ControllerUpdateUserSettings:
    def POST(self):
        data = web.input()

        setting_model = LoginModel.LoginModel()
        data['email'] = session_data["user"]['email']

        res = setting_model.update_info(data)

        if res:
            session_data["user"]['username'] = data['username']
            return 'success'
        else:
            return 'A fatal error has occured.'


class ControllerAddComment:
    def POST(self):
        comment = web.input()
        comment['user_id'] = session_data["user"]['_id']

        post_model = Posts.Posts()
        added_comment = post_model.add_comment(comment)

        if added_comment:
            return added_comment

        return {"error": "403"}


if __name__ == "__main__":
    app.run()
