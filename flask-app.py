from flask import Flask, render_template
from flask_login import login_manager, LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import Api
from werkzeug.utils import redirect

from data import db_session
from data.User import User
from data.login_form import LoginForm
from data.register_form import RegisterForm

app = Flask(__name__)
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/profile.db")

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/')
    def index():
        return render_template('index.html', title='Основная')

    @app.route('/login', methods=['GET', 'POST'])
    def register_login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                surname=form.surname.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/eatery')
    def menu():
        pass

    @app.route('/motorcycle_workshop')
    def motorcycle():
        pass

    @app.route('/profile')
    def profile():
        if current_user.is_authenticated:
            print(current_user)
            return render_template('profile.html', title=f'{current_user.surname} {current_user.name}',
                                   user=current_user)
        else:
            return redirect('/login')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    app.run()


if __name__ == '__main__':
    main()
