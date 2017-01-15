from reservation_scraper.reservation_system_spiders.bizzy import BizzySpider


class ZideniceSpider(BizzySpider):
    name = "zidenice"
    reservation_system_host = "rezervace.badmintonzidenice.cz"
    additional_ajax_apyload = {
        "scheduleNavigForm:service_filter_menu": "40086"
    }

    def __init__(self):
        super().__init__(
            self.reservation_system_host,
            self.additional_ajax_apyload
        )
