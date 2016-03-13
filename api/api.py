from flask import Flask, request, jsonify

app = Flask(__name__)

import datetime
from db_worker import db_worker


@app.route("/reservations/all", methods=['GET', 'POST'])
def get_reservations():
    last_client_update = None
    if request.method == 'POST':
        if 'last_client_update' in request.form.keys():
            last_client_update = datetime.datetime.strptime(request.form['last_client_update'], '%d.%m.%Y %h:%m')

    if not last_client_update:
        last_client_update = datetime.datetime.now() - datetime.timedelta(days=100)

    updatet_centers = db_worker.get_updated_centers(last_client_update)
    data = []
    for center in updatet_centers:
        center_reservations = db_worker.get_center_reservations(center[0])
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


@app.route("/centers/add", methods=['POST', 'PUT'])
def add_center():
    db_worker.add_center(
        name=request.form['name'],
        url=request.form['url'],
        opening_time=request.form['opening_time'],
        closing_time=request.form['closing_time'],
        description=request.form['description'],
        host_name=request.form['host_name']
    )
    return ''


@app.route("/centers/update", methods=['POST'])
def update_center():
    db_worker.update_center_info(**request.form)
    return ''


@app.route("/centers/remove", methods=['POST'])
def remove_center():
    db_worker.remove_center(request.form['guid'])
    return ''


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
