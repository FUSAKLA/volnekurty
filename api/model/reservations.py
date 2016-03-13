import psycopg2


class ReservationsDbWorker(object):
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

    def __del__(self):
        self._db_conn.close()


reservations_db_worker = ReservationsDbWorker()