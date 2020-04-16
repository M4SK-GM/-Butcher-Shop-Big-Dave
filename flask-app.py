import string
import random

from flask import Flask, render_template, request
from flask_login import login_manager, LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import Api, abort
from werkzeug.utils import redirect

from data import db_session, confirm_form
from data.Cart import Cart
from data.Services import Services
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

discounts = [  # Скидки. [id блюда, id услуги, скидка(без %)]
    [1, 1, 5]
]


def main():
    db_session.global_init("db/profile.db")

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    # Основа
    @app.route('/')
    def index():
        return render_template('index.html', title='Основная')

    # ===ПРОФИЛЬ===
    # Профиль|Логин
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

    # Профиль|Регистрация
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

    # Профиль|Страница профиля
    @app.route('/profile')
    def profile():
        if current_user.is_authenticated:
            return render_template('profile.html', title=f'{current_user.surname} {current_user.name}',
                                   user=current_user)
        else:
            return redirect('/login')

    # Профиль|Выход
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    # Профиль|Подтверждение почты
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

    # ===ЗАКУСОЧНАЯ===
    # Закусочная|Основа
    @app.route('/eatery')
    def menu():
        session = db_session.create_session()
        dish = session.query(Dish).all()
        return render_template('eatery-main.html', title='Закусочная', dish=dish)

    # Закусочная|Отдельная страница блюда
    @app.route('/eatery/<int:id>', methods=['GET'])
    def current_dish(id):
        session = db_session.create_session()
        dish = session.query(Dish).get(id)
        return render_template('eatery-dish.html', title=dish.name, dish=dish)

    # ===МОТОМАСТЕРСКАЯ===
    # Мотомастерская|Основа
    @app.route('/motorcycle_workshop')
    def motorcycle():
        session = db_session.create_session()
        services = session.query(Services).all()
        return render_template('motorcycle_workshop-main.html', title='Мотомастерская', services=services)

    # Мотомастерская|Отдельная страница услуги
    @app.route('/motorcycle_workshop/<int:id>', methods=['GET'])
    def current_services(id):
        session = db_session.create_session()
        services = session.query(Services).get(id)
        return render_template('motorcycle_workshop_services.html', title=services.name, services=services)

    # ===КОРЗИНА===
    # Корзина|Основа
    @app.route('/cart')
    def cart_main():
        session = db_session.create_session()
        cart = session.query(Cart).filter(User.id == current_user.id).all()
        all_price = 0
        for i in cart:
            if i.dish:
                all_price += i.dish.price
            else:
                all_price += i.services.price
        return render_template('cart-main.html', title='Корзина', cart=cart, all_price=all_price)

    # Корзина|Удалить всё
    @app.route('/cart/clear')
    def cart_delete():
        session = db_session.create_session()
        cart = session.query(Cart).filter(User.id == current_user.id).all()
        for item in cart:
            session.delete(item)
        session.commit()
        return redirect('/cart')

    # Корзина|Добавить блюдо
    @app.route('/cart/add_dish/<int:id>')
    def add_dish_in_cart(id):
        session = db_session.create_session()
        dish = session.query(Dish).get(id)
        user = session.query(User).get(current_user.id)
        cart = Cart(
            type='dish',
            user=user,
            dish=dish
        )
        session.add(cart)
        session.commit()
        return redirect('/eatery')

    # Корзина|Добавить услугу
    @app.route('/cart/add_services/<int:id>')
    def add_services_in_cart(id):
        session = db_session.create_session()
        services = session.query(Services).get(id)
        user = session.query(User).get(current_user.id)
        cart = Cart(
            type='service',
            user=user,
            services=services
        )
        session.add(cart)
        session.commit()
        return redirect('/motorcycle_workshop')

    # ===АДМИН-ПАНЕЛЬ===
    # Админ|Основа
    @app.route('/admin')
    @login_required
    def admin():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            return render_template('admin-panel_main.html')

    # Админ|Закусочная
    @app.route('/admin/eatery')
    @login_required
    def admin_eatery():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            session = db_session.create_session()
            dish = session.query(Dish).all()
            return render_template('admin-panel_eatery.html', dish=dish)

    # Админ|Закусочная|Добавление блюда
    @app.route('/admin/eatery/add_dish', methods=['GET', 'POST'])
    def admin_eatery_add_dish():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            form = admin_form.Add_Dish_Form()
            if form.validate_on_submit():
                session = db_session.create_session()
                name_for_image = "_".join(form.name.data.split())
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

    # Админ|Закусочная|Удалить блюдо
    @app.route('/admin/eatery/delete/<int:id>', methods=['GET', 'POST'])
    def delete_eatery(id):
        if current_user.status != 'admin':
            return redirect('/')
        else:
            session = db_session.create_session()
            dish = session.query(Dish).get(id)
            session.delete(dish)
            session.commit()
            return redirect('/admin/eatery')

    # Админ|Закусочная|Изменить блюдо
    @app.route('/admin/eatery/<int:id>', methods=['GET', 'POST'])
    def redact_dish(id):
        if current_user.status != 'admin':
            return redirect('/')
        else:
            form = admin_form.Add_Dish_Form()
            if request.method == "GET":
                session = db_session.create_session()
                dish = session.query(Dish).filter(Dish.id == id).first()
                if dish:
                    form.name.data = dish.name
                    form.short_description.data = dish.short_description
                    form.full_description.data = dish.full_description
                    form.price.data = dish.price
                else:
                    abort(404)
            if form.validate_on_submit():
                session = db_session.create_session()
                dish = session.query(Dish).filter(Dish.id == id).first()
                if dish:
                    dish.name = form.name.data
                    dish.short_description = form.short_description.data
                    dish.full_description = form.full_description.data
                    dish.price = form.price.data
                    session.commit()
                    return redirect('/admin/eatery')
                else:
                    abort(404)
            return render_template('admin-panel_eatery_add_dish.html', form=form)

    # Админ|Мотомастерская|Основа
    @app.route('/admin/motorcycle_workshop')
    @login_required
    def admin_motorcycle_workshop():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            session = db_session.create_session()
            services = session.query(Services).all()
            return render_template('admin-panel_motorcycle_workshop.html', services=services)

    # Админ|Мотомастерская|Добавление услуги
    @app.route('/admin/motorcycle_workshop/add_services', methods=['GET', 'POST'])
    def admin_motorcycle_workshop_services():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            form = admin_form.Add_Services()
            if form.validate_on_submit():
                session = db_session.create_session()
                name_for_image = "_".join(form.name.data.split())
                services = Services(
                    name=form.name.data,
                    short_description=form.short_description.data,
                    full_description=form.full_description.data,
                    price=form.price.data,
                    photo=f'http://127.0.0.1:5000/static/img/{name_for_image}.jpg'
                )
                session.add(services)
                session.commit()
                f = request.files['file']
                f.save(f'./static/img/{name_for_image}.jpg')
                return redirect('/admin/motorcycle_workshop')
            return render_template('admin-panel_eatery_add_dish.html', form=form)

    # Админ|Мотомастерская|Удалить услугу
    @app.route('/admin/motorcycle_workshop/delete/<int:id>', methods=['GET', 'POST'])
    def delete_service(id):
        if current_user.status != 'admin':
            return redirect('/')
        else:
            session = db_session.create_session()
            services = session.query(Services).get(id)
            session.delete(services)
            session.commit()
            return redirect('/admin/motorcycle_workshop')

    # Админ|Мотомастерская|Изменить услугу
    @app.route('/admin/motorcycle_workshop/<int:id>', methods=['GET', 'POST'])
    def redact_service(id):
        if current_user.status != 'admin':
            return redirect('/')
        else:
            form = admin_form.Add_Services()
            if request.method == "GET":
                session = db_session.create_session()
                services = session.query(Services).filter(Services.id == id).first()
                if services:
                    form.name.data = services.name
                    form.short_description.data = services.short_description
                    form.full_description.data = services.full_description
                    form.price.data = services.price
                else:
                    abort(404)
            if form.validate_on_submit():
                session = db_session.create_session()
                services = session.query(Services).filter(Services.id == id).first()
                if services:
                    services.name = form.name.data
                    services.short_description = form.short_description.data
                    services.full_description = form.full_description.data
                    services.price = form.price.data
                    session.commit()
                    return redirect('/admin/motorcycle_workshop')
                else:
                    abort(404)
            return render_template('admin-panel_eatery_add_dish.html', form=form)

    # Админ|Профиль|Основа
    @app.route('/admin/profile')
    @login_required
    def admin_profile():
        if current_user.status != 'admin':
            return redirect('/')
        else:
            return render_template('admin-panel_main.html')

    app.run()


if __name__ == '__main__':
    main()
