from flask.json import jsonify
import psycopg2


class CentersDbWorker(object):
    _db_conn = None
    _db_cur = None

    def __init__(self):
        self._db_conn = psycopg2.connect(
            host='localhost',
            database='volnekurty',
            user='postgres',
            password='Martin39'
        )
        self._db_cur = self._db_conn.cursor()

    def get_centers(self):
        try:
            sql = """
                SELECT
                    c.guid,c.name,c.description,c.opening_time,c.closing_time,
                    c.adress,c.url,c.telephone,c.host_name,c.last_reservation_update,
                    count(r.fk_sport_center)
                FROM
                    reservation_data.sport_center as c
                    LEFT JOIN reservation_data.badminton_reservations as r ON c.guid = r.fk_sport_center
                GROUP BY
                    c.guid
            """
            self._db_cur.execute(sql)
        except psycopg2.DatabaseError as e:
            print e
        else:
            res = self._db_cur.fetchall()
            res_set = []
            for r in res:
                item_dict = {
                    'guid': r[0],
                    'name': r[1],
                    'description': r[2],
                    'opening_time': r[3],
                    'closing_time': r[4],
                    'adress': r[5],
                    'url': r[6],
                    'telephone': r[7],
                    'host_name': r[8],
                    'last_reservation_update': r[9],
                    'reservation_count': r[10]
                }
                res_set.append(item_dict)
            return jsonify({'sport_centers': res_set})

    def get_updated_centers(self, last_client_update):
        try:
            sql = """
                SELECT
                    *
                FROM
                    reservation_data.sport_center
                WHERE
                    last_reservation_update > %s
            """
            self._db_cur.execute(sql, (last_client_update,))
        except psycopg2.DatabaseError as e:
            print e
        else:
            res = self._db_cur.fetchall()
            return res

    def update_center_info(self, **kwargs):
        try:
            sql = """
                UPDATE
                    reservation_data.sport_center
                SET
             """
            for arg in kwargs.keys():
                if arg != 'guid':
                    sql += arg + ' = %s, '
            sql = sql[:-2] + """
                WHERE
                    guid = %s
            """
            guid = kwargs.pop('guid')[0]
            params = []
            for a in kwargs.values():
                params.append(a[0])
            params.append(guid)
            self._db_cur.execute(sql, params)
        except psycopg2.DatabaseError as e:
            print e
        else:
            self._db_conn.commit()

    def add_center(self, name, url, opening_time, closing_time, description, host_name):
        try:
            sql = """
                INSERT INTO
                    reservation_data.sport_center(
                        name,url,opening_time,closing_time,description,host_name
                    )
                VALUES (%s,%s,%s,%s,%s,%s)
            """
            self._db_cur.execute(sql, (name, url, opening_time, closing_time, description, host_name))
        except psycopg2.DatabaseError as e:
            print e
        else:
            self._db_conn.commit()

    def remove_center(self, guid):
        try:
            sql = """
                DELETE FROM
                    reservation_data.sport_center
                WHERE
                    guid = %s
            """
            self._db_cur.execute(sql, (guid,))
        except psycopg2.DatabaseError as e:
            print e
        else:
            self._db_conn.commit()




    def __del__(self):
        self._db_conn.close()


centers_db_worker = CentersDbWorker()