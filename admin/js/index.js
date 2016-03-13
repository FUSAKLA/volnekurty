

var sport_centers = [];

$(window).on('load', function () {
        $.ajax({
            url: "http://api.volnekurty.cz/centers/all",
            crossDomain: true,
            contentType: 'application/json',
            dataType: 'json',
            'Access-Control-Allow-Origin': '*'
        }).done(function(data) {
            console.log(data);
            var data_json = data;
            sport_centers = data_json['sport_centers'];
            set_data_counter(sport_centers.length, '#sport_centers_counter');
            set_data_counter(count_reservations(sport_centers), '#reservations_counter');
            set_data_counter(sport_centers.length, '#scrape_counter');
        });
  })


function set_data_counter(value, counter_selector){
    var counter = $(counter_selector);
    $({i: 0, f: 10}).animate(
        {
            i: parseInt(value),
            f: 40
        },
        {
            duration: 1000,
            specialEasing: {
              i: "easeOutCubic",
              f: "easeOutBounce"
            },
            step: function() {
                counter.text(Math.round(this.i));
                counter.css('font-size',Math.round(this.f))
            }

        }
    )
}


function count_reservations(sport_centers){
    var count = 0;
    $.each(sport_centers, function(id,center){
        console.log(center);
        count += parseInt(center['reservation_count'])
    });
     return count;
};