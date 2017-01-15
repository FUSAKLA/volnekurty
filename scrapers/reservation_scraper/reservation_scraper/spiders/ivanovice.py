from reservation_scraper.reservation_system_spiders.member_pro import MemberProSpider


class IvanoviceSpider(MemberProSpider):
    name = "ivanovice"
    reservation_system_host = "onlinememberpro.cz"
    url_name = "ivanovice"

    additional_payload = {
        "BTN5": "Badminton+hala",
    }

    def __init__(self):
        super().__init__(
            self.reservation_system_host,
            self.url_name,
            self.additional_payload
        )
