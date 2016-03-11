from flask import Flask
app = Flask(__name__)

import psycopg2

@app.route("/")
def hello():
    db_connection = psycopg2.connect(
            host='localhost',
            database='volnekurty',
            user='postgres',
            password='Martin39'
        )
    db_cur = db_connection.cursor()

    try:
        db_cur.execute("""
            select s.host_name,r.*
            from
                reservation_data.sport_center as s
                join reservation_data.badminton_reservations as r on s.guid = r.fk_sport_center
            order by
                s.host_name, r.start_time
        """)
    except:
        return "Chyba v DB!"

    res = db_cur.fetchall()
    if res:
        out = ''
        for r in res:
            out += ', '.join([str(x) for x in r])+'</br>'
        return out
    else:
        "nic to nestahlo"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')