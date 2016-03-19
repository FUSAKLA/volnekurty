
from flask import request
from model.centers import centers_db_worker
from api import app
from flaskext.auth.auth import login_required


@app.route("/centers/add", methods=['POST', 'PUT'])
def add_center():
    centers_db_worker.add_center(
        name=request.form['name'],
        url=request.form['url'],
        opening_time=request.form['opening_time'],
        closing_time=request.form['closing_time'],
        description=request.form['description'],
        host_name=request.form['host_name']
    )
    return '{}'


@app.route("/centers/update", methods=['POST'])
def update_center():
    centers_db_worker.update_center_info(**request.form)
    return '{}'


@app.route("/centers/remove", methods=['POST'])
def remove_center():
    centers_db_worker.remove_center(request.form['guid'])
    return '{}'


@app.route("/centers/all", methods=['GET'])
@login_required()
def get_centers():
    return centers_db_worker.get_centers()
