from reservation_scraper.reservation_system_spiders.member_pro import MemberProSpider


class SprintSpider(MemberProSpider):
    name = "sprint"
    reservation_system_host = "onlinememberpro.cz"
    url_name = "sprint"

    def __init__(self):
        super().__init__(
            self.reservation_system_host,
            self.url_name
        )

