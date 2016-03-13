import datetime
from flask import request
from flask.json import jsonify
from model.reservations import reservations_db_worker
from model.centers import centers_db_worker
from api import app


@app.route("/reservations/all", methods=['GET', 'POST'])
def get_reservations():
    last_client_update = None
    if request.method == 'POST':
        if 'last_client_update' in request.form.keys():
            last_client_update = datetime.datetime.strptime(request.form['last_client_update'], '%d.%m.%Y %h:%m')

    if not last_client_update:
        last_client_update = datetime.datetime.now() - datetime.timedelta(days=100)

    updatet_centers = centers_db_worker.get_updated_centers(last_client_update)
    data = []
    for center in updatet_centers:
        center_reservations = reservations_db_worker.get_center_reservations(center[0])
        center_data = {
            'name': center[1],
            'address': center[2],
            'telephone': center[3],
            'opening_time': center[4],
            'closing_time': center[5],
            'reservations': center_reservations
        }
        data.append(center_data)

    return jsonify({'sport_centers': data})


@app.route('/reservations/statistics', methods=['GET'])
def get_reservations_statistics():
    statistics = {
        
    }
    return statistics