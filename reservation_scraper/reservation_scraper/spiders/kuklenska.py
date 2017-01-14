from reservation_scraper.reservation_system_spiders.bizzy import BizzySpider

class KuklenskaSpider(BizzySpider):
    name = "kuklenska"
    reservation_system_host = "sportkuklenska.e-rezervace.cz"
    additional_ajax_apyload = {
        "scheduleNavigForm:service_filter_menu": "40086"
    }

    def __init__(self):
        super().__init__(
            self.reservation_system_host,
            self.additional_ajax_apyload
        )
