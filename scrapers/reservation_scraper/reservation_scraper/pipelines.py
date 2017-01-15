from reservation_scraper.db_driver.mongo import MongoDriver
from reservation_scraper.db_driver.file_worker import FileWorker
from reservation_scraper.lib.reservation import Reservation


class ReservationScraperPipeline(object):

    def process_item(self, item, spider):
        reservation = Reservation(item["facility_id"], item["start_time"], item["end_time"], item["court_id"])
        for res_slice in reservation.get_sliced_reservation_generator(30):
            MongoDriver.insert_reservation(
                facility_id=res_slice.facility_id,
                court_id=res_slice.court_id,
                reservation_start=res_slice.reservation_start,
                reservation_end=res_slice.reservation_end
            )
            # for sake of debugging
            # FileWorker.insert_reservation_item(res_slice, item["html_id"])
        return item

