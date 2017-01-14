import psycopg2
import db_exceptions


class DbWorker(object):
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = psycopg2.connect(
            host='localhost',
            database='volnekurty',
            user='postgres',
            password='heslo'
        )
        self._db_cur = self._db_connection.cursor()

    def insert_reservation_item(self, item):
        try:
            self._db_cur.execute(
                """INSERT INTO reservation_data.badminton_reservations(
                        fk_sport_center,
                        court_number,
                        start_time,
                        end_time
                    ) VALUES(%s, %s, %s, %s)
                """,
                (
                    item.get('fk_sport_center'),
                    item.get('court_number'),
                    item.get('start_time'),
                    item.get('end_time')
                )
            )
        except psycopg2.DatabaseError as e:
            print("Error: {}".format(e))
        else:
            self._db_connection.commit()

    def remove_center_reservations(self, guid):
        try:
            self._db_cur.execute(
                """
                DELETE FROM reservation_data.badminton_reservations
                WHERE fk_sport_center = %s
                """,
                (guid,)
            )
        except psycopg2.DatabaseError as e:
            print("Error: {}".format(e))
        else:
            self._db_connection.commit()

    def get_center_guid(self, host_name):
        try:
            self._db_cur.execute(
                """
                SELECT guid FROM
                reservation_data.sport_center
                WHERE host_name = %s
                """,
                (host_name,)
            )
        except psycopg2.DatabaseError as e:
            print("Error: {}".format(e))
        else:
            res = self._db_cur.fetchone()
            if res:
                return res[0]
            else:
                raise db_exceptions.SportCenterNotFound(
                    "Dane sportoviste nebylo nalezeno v databazi"
                )

    def update_center_last_edited(self, guid):
        try:
            self._db_cur.execute(
                """
                UPDATE reservation_data.sport_center
                SET last_reservation_update = now()
                WHERE guid = %s
                """,
                (guid,)
            )
        except psycopg2.DatabaseError as e:
            print("Error: {}".format(e))
        else:
            self._db_connection.commit()

    def __del__(self):
        self._db_connection.close()


#db_worker = DbWorker()

