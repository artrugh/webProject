import web
from Models import RegisterModel
from Models import LogiModel

web.config.debug = False

urls = (
    "/", "Home",
    "/register", "Register",
    "/login", "Login",
    "/logout", "Logout",
    "/post", "PostRegistration",
    "/check-login", "CheckLogin",
)
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout", globals={'session': session_data, 'current_user': session_data["user"]})


# Classes/routes

class Home:
    def GET(self):
        return render.Home()


class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        return render.Login()


class PostRegistration:
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


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


if __name__ == "__main__":
    app.run()
