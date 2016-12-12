For now all you need is Python 2 and Scrapy


### TODO:

### Scraper:

  * check if scapers are up to date and working
     * in case of not fix them
  * transfer to python3
  * dockerize reservation_scraper with scrapyd daemon
  * lear how to deploy code to the scrapyd docker container and solve scraper versioning probelm(mount or what).


### Monitoring:

  * add to project docker image for prometheus and grafana
  * probably will use prometheus pushgateway so add image also
  * add to scrapers metrics pushing to gateway
     * probably create method wrapping scrapy.Request
     * create base class for scrapers to generalize metrics management
  * create dashboard in grafana


### Database:

  * *keep it webscale!!!* no rly probaably will use MongoDB
  * (for now docker will do, no replication no sharding)
  * one table with sport centers
  * one table with upcoming dates where srapers will insert the new reservations
  * drop all records for actually scraped sport center and insert just the new ones
            (ideally remove just those that are newer than now so we can store the old ones)
  * figure out how to move older reservations for datamining (som job to transfer them to `log_table` for aggregation)
  * one table where the old reservations will be stored (for now unused but will do so baby doll will do so)


### Backend:

   * do i need one? how about ReactJS accessing directly the MongoDB?
   * in case not i will need api to access DB data



### Frontend:

   * figure out what technologies to use for frontend (probably ReactJS)
   * create simple visualization of data for testing
             (like rly.. do just fukken stupid table)
   * do some brainstorm about UI and some designs and than ask friends on opinion


