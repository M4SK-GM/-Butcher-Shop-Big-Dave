import flask
from flask import jsonify

from data import db_session
from data.Dish import Dish
from data.Services import Services

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/services')
def get_services():
    session = db_session.create_session()
    service = session.query(Services).all()
    return jsonify(
        {
            'services':
                [item.to_dict(only=('name', 'short_description', 'full_description', 'price'))
                 for item in service]
        }
    )


@blueprint.route('/api/dishes')
def get_dishes():
    session = db_session.create_session()
    dishes = session.query(Dish).all()
    return jsonify(
        {
            'dishes':
                [item.to_dict(only=('name', 'short_description', 'full_description', 'price'))
                 for item in dishes]
        }
    )


@blueprint.route('/api/services/<int:services_id>', methods=['GET'])
def get_one_service(services_id):
    session = db_session.create_session()
    service = session.query(Services).get(services_id)
    if not service:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'service': service.to_dict(only=('name', 'short_description', 'full_description', 'price'))
        }
    )


@blueprint.route('/api/dishes/<int:dish_id>', methods=['GET'])
def get_one_dish(dish_id):
    session = db_session.create_session()
    dish = session.query(Services).get(dish_id)
    if not dish:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'dish': dish.to_dict(only=('name', 'short_description', 'full_description', 'price'))
        }
    )


