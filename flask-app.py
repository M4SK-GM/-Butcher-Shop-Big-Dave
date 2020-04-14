import string
import random

from flask import Flask, render_template, request
from flask_login import login_manager, LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import Api
from werkzeug.utils import redirect

from data import db_session, confirm_form
from data.Dish import Dish
from data.User import User
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data import mail
from data import admin_form

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
            code = "".join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
            user = User(
                name=form.name.data,
                email=form.email.data,
                confirm_email=False,
                code=code,
                surname=form.surname.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/eatery')
    def menu():
        session = db_session.create_session()
        dish = session.query(Dish).all()
        return render_template('eatery-main.html', title='Закусочная', dish=dish)

    @app.route('/eatery/<int: id>', methods=['GET'])
    def menu(id):
        session = db_session.create_session()
        dish = session.query(Dish).get(id)
        return render_template('eatery-dish.html', title='Закусочная', dish=dish)

    @app.route('/motorcycle_workshop')
    def motorcycle():
        pass

    @app.route('/profile')
    def profile():
        if current_user.is_authenticated:
            return render_template('profile.html', title=f'{current_user.surname} {current_user.name}',
                                   user=current_user)
        else:
            return redirect('/login')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/confirm', methods=['GET', 'POST'])
    @login_required
    def confirm_email():
        form = confirm_form.ConfirmForm()
        mail.send_mail(current_user.email, current_user.code)
        if form.validate_on_submit():
            if form.code.data == current_user.code:
                session = db_session.create_session()
                user = session.query(User).filter(User.email == current_user.email).first()
                session.delete(user)
                session.commit()
                user = User(
                    name=current_user.name,
                    email=current_user.email,
                    confirm_email=True,
                    code="It now don't need",
                    surname=current_user.surname,
                    hashed_password=current_user.hashed_password,
                    created_date=current_user.created_date
                )
                session.add(user)
                session.commit()
                return redirect('/profile')
            else:
                return render_template('confirm-email.html', title='Подтверждение почты', form=form,
                                       message='Неверный код')
        return render_template('confirm-email.html', title='Подтверждение почты', form=form)

    @app.route('/admin')
    @login_required
    def admin():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            return render_template('admin-panel_main.html')

    @app.route('/admin/eatery')
    @login_required
    def admin_eatery():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            session = db_session.create_session()
            dish = session.query(Dish).all()
            return render_template('admin-panel_eatery.html', dish=dish)

    @app.route('/admin/eatery/add_dish', methods=['GET', 'POST'])
    def admin_eatery_add_dish():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            form = admin_form.Add_Dish_Form()
            if form.validate_on_submit():
                session = db_session.create_session()
                name_for_image = "_".join(form.name.data.split())
                print(name_for_image)
                dish = Dish(
                    name=form.name.data,
                    short_description=form.short_description.data,
                    full_description=form.full_description.data,
                    price=form.price.data,
                    photo=f'http://127.0.0.1:5000/static/img/{name_for_image}.jpg'
                )
                session.add(dish)
                session.commit()
                f = request.files['file']
                f.save(f'./static/img/{name_for_image}.jpg')
                return redirect('/admin/eatery')
            return render_template('admin-panel_eatery_add_dish.html', form=form)

    @app.route('/admin/motorcycle_workshop')
    @login_required
    def admin_motorcycle_workshop():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            return render_template('admin-panel_main.html')

    @app.route('/admin/profile')
    @login_required
    def admin_profile():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            return render_template('admin-panel_main.html')

    """@app.route('/sample_file_upload', methods=['POST', 'GET'])
    def sample_file_upload():
        if request.method == 'GET':
            return f'''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                 <link rel="stylesheet"
                                 href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                                 integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
                                 crossorigin="anonymous">
                                <title>Пример загрузки файла</title>
                              </head>
                              <body>
                                <h1>Загрузим файл</h1>
                                <form method="post" enctype="multipart/form-data">
                                   <div class="form-group">
                                        <label for="photo">Выберите файл</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                              </body>
                            </html>'''
        elif request.method == 'POST':
            f = request.files['file']
            print(f)
            f.save('./static/img/Без имени-1.jpg')
            return "Форма отправлена"""

    app.run()


if __name__ == '__main__':
    main()
