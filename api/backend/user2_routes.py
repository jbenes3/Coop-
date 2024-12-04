from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# create blueprint object
users = Blueprint('customers', __name__)

# Get users from specific industries:
@users.route('/users/<userID>', methods=['PUT'])
def get_users_by_industry():

    # log and make cursor
    current_app.logger.info('PUT /users/<userID> route')
    cursor = db.get_db().cursor()

    user_id = user_info['userID']
    occupation = user_info['occupation']
    name = user_info['name']
    company = user_info['company']

    query = 'UPDATE customers SET first_name = %s, last_name = %s, company = %s where id = %s'
    data = (first, last, company, cust_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'

