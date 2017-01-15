from datetime import datetime

from pymongo import MongoClient
from facility_information_scraper.db_driver.generic_driver import GenericDbDriver


class MongoDriver(GenericDbDriver):
    client = MongoClient('localhost', 27017)
    volnekurty_db = client.volnekurty
    reservations = volnekurty_db.reservations
    facilities = volnekurty_db.facilities

    @classmethod
    def get_facility_reservations(cls, facility_id: str):
        return cls.facilities.find({'facility_id': facility_id})

    @classmethod
    def insert_reservation(cls, facility_id=None, court_id=None, reservation_start=None, reservation_end=None):
        cls.reservations.insert_one({
            "facility_id": facility_id,
            "court_id": court_id,
            "reservation_start": reservation_start,
            "reservation_end": reservation_end
        })

    @classmethod
    def delete_all_future_facility_reservations(cls, facility_id: str):
        cls.reservations.delete_many({
            "facility_id": facility_id,
            "$gt": {
                "reservation_start": datetime.now()
            }
        })

    @classmethod
    def delete_all_reservations(cls):
        cls.reservations.delete_many({})

    @classmethod
    def insert_facility(cls, name=None, address=None, opening_time=None, closing_time=None, position_x=None, position_y=None, telephone=None, price=None):
        cls.facilities.insert_one({
            "name": name,
            "address": address,
            "opening_time": opening_time,
            "closing_time": closing_time,
            "position_x": position_x,
            "position_y": position_y,
            "telephone": telephone,
            "price": price
        })

    @classmethod
    def update_facility(cls, facility_id, name=None, address=None, opening_time=None, closing_time=None, position_x=None, position_y=None, telephone=None, price=None):
        update = {}
        if name:
            update["name"] = name
        if address:
            update["address"] = address
        if opening_time:
            opening_time["opening_time"] = name
        if closing_time:
            update["closing_time"] = closing_time
        if position_x:
            update["position_x"] = position_x
        if position_y:
            update["position_y"] = position_y
        if telephone:
            update["telephone"] = telephone
        if price:
            update["price"] = price

        cls.facilities.update_one(
            {"_id": facility_id},
            {"$set": update}
        )

    @classmethod
    def delete_facility(cls, facility_id):
        cls.facilities.delete_one({
            "_id": facility_id
        })

    @classmethod
    def select_facility_by_name(cls, name: str):
        return cls.facilities.find_one({'name': name})

    @classmethod
    def select_facility_by_id(cls, facility_id: str):
        return cls.facilities.find_one({'_id': facility_id})