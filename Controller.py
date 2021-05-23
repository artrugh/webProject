import web
from Models import SignupModel
from Models import LoginModel
from Models import Posts

web.config.debug = False

urls = (
    # views
    "/", "Home",
    "/signup", "SignUp",
    "/login", "Login",

    # apis
    "/api/signup", "ControllerSignUp",
    "/api/login", "ControllerLogin",
    "/api/logout", "ControllerLogout",
    "/post-activity", "PostActivity",
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
        # data = type('obj', (object,), {
        #             "username": "qazi1", "password": "doubledoor"})

        # login = LoginModel.LoginModel()
        # isCorrect = login.check_user(data)

        # if isCorrect:
        #     session_data["user"] = isCorrect

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
        print('user', user['username'])

        if user == False:
            return "error"

        session_data["user"] = user
        return user


class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        post_model.insert_post(data)
        return "success"


class ControllerLogout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


if __name__ == "__main__":
    app.run()
