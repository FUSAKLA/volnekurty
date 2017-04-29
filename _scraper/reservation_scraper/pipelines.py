from scrapers.reservation_scraper.db_driver.mongo import MongoDriver
from scrapers.reservation_scraper.lib.reservation import Reservation


class ReservationScraperPipeline(object):
    @staticmethod
    def process_item(item, spider):
        reservation = Reservation(item["facility_id"], item["start_time"], item["end_time"], item["court_id"])
        for res_slice in reservation.get_sliced_reservation_generator(30):
            MongoDriver.insert_reservation(
                facility_id=res_slice.facility_id,
                court_id=res_slice.court_id,
                reservation_start=res_slice.reservation_start,
                reservation_end=res_slice.reservation_end
            )
        return item

