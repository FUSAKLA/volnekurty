from datetime import datetime, timedelta


class Reservation:
    def __init__(self, facility_id: str, reservation_start: datetime, reservation_end: datetime, court_id: str) -> None:
        self.facility_id = facility_id
        self.reservation_start = reservation_start
        self.reservation_end = reservation_end
        self.court_id = court_id

    def get_reservation_duration(self):
        return self.reservation_end - self.reservation_start

    def get_reservation_date(self):
        return self.reservation_start.date()

    def get_sliced_reservation_generator(self, slice_length):
        reservation_slice_length = timedelta(minutes=slice_length)
        interval_start = self.reservation_start
        interval_end = self.reservation_start
        while interval_end <= self.reservation_end:
            interval_end = interval_start + reservation_slice_length
            new_slice = Reservation(
                facility_id=self.facility_id,
                court_id=self.court_id,
                reservation_start=self.reservation_start,
                reservation_end=self.reservation_end
            )
            interval_start += reservation_slice_length
            yield new_slice






