import web
from Models import RegisterModel
from Models import LogiModel
from Models import Posts

web.config.debug = False

urls = (
    "/", "Home",
    "/register", "Register",
    "/login", "Login",
    "/logout", "Logout",
    "/signup", "SignUp",
    "/check-login", "CheckLogin",
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
        data = type('obj', (object,), {
                    "username": "qazi1", "password": "doubledoor"})

        login = LogiModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data["user"] = isCorrect

        post_model = Posts.Posts()
        posts = post_model.get_all_posts()

        return render.Home(posts)


class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        return render.Login()


class SignUp:
    def POST(self):
        data = web.input()
        reg_model = RegisterModel.RegisterModelCls()
        reg_model.insert_user(data)
        return data.username


class CheckLogin:
    def POST(self):
        data = web.input()
        login = LogiModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect

        return "error"


class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        post_model.insert_post(data)
        return "success"


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


if __name__ == "__main__":
    app.run()
