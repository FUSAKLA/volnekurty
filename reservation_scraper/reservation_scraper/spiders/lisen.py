from reservation_scraper.reservation_system_spiders.bizzy import BizzySpider


class LisenSpider(BizzySpider):
    name = "lisen"
    reservation_system_host = "badmintonlisen.e-rezervace.cz"

    additional_ajax_payload = {
        "scheduleNavigForm:j_id232": "41439",
        "scheduleNavigForm:j_id227": "scheduleNavigForm:j_id227"
    }

    def __init__(self):
        super().__init__(
            self.reservation_system_host,
            self.additional_ajax_payload
        )
