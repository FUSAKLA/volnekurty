import psycopg2


class DbWorker(object):
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

    def get_center_reservations(self, guid):
        try:
            sql = """
                SELECT
                    r.court_number, r.start_time, r.end_time
                FROM
                    reservation_data.sport_center as c
                    JOIN reservation_data.badminton_reservations as r
                        ON c.guid =  r.fk_sport_center
                WHERE
                    c.guid = %s
            """
            self._db_cur.execute(sql, (guid,))
        except psycopg2.DatabaseError as e:
            print e
        else:
            res = self._db_cur.fetchall()
            res_set = []
            for r in res:
                item_dict = {
                    'court_number': r[0],
                    'start_time': r[1],
                    'end_time': r[2]
                }
                res_set.append(item_dict)

            return res_set

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


db_worker = DbWorker()