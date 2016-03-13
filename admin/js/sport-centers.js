


var sport_centers = [];

$(window).on('load', function () {
        load_centers_data()
  })


function load_centers_data(){
    $.ajax({
            url: "http://api.volnekurty.cz/centers/all",
            crossDomain: true,
            contentType: 'application/json',
            dataType: 'json',
            'Access-Control-Allow-Origin': '*'
        }).done(function(data) {
            sport_centers = data['sport_centers'];
            load_centers_table(sport_centers)
        });
}


function load_centers_table(sport_centers){
    $('#sport_centers_table').find('> tbody').html('');
    $.each(sport_centers, function(i,center){
        var row = $('<tr>');
        row.attr('id',center['guid']);
        row.append($('<td>').html(center['name']));
        row.append($('<td>').html(center['description']));
        row.append($('<td>').html(center['adress']));
        row.append($('<td>').html(center['telephone']));
        row.append($('<td>').html(center['opening_time']));
        row.append($('<td>').html(center['closing_time']));
        row.append($('<td>').html(center['url']));
        row.append($('<td>').html(center['host_name']));
        row.append($('<td>').html(center['last_reservation_update']));
        row.append($('<td>').html(center['reservation_count']));
        row.append($('<td class="center_control">').html('<a href="edit-sport-center.html"><i class="fa fa-fw fa-pencil"></i></a>'));
        row.append($('<td class="center_control">').html('<a href="#"  onclick="remove_center(this)"><i class="fa fa-fw fa-trash"></i>'));
        $('#sport_centers_table').find('> tbody:last-child').append(row);
    })
}


function remove_center(el){
    var r = confirm("Do you really want to remove this sport center?");
    if (r != true) {
        return
    }
    var guid = $(el).parents('tr').attr('id');
    $.ajax({
            url: "http://api.volnekurty.cz/centers/remove",
            data: {'guid':guid},
            method: 'POST'
        }).done(function() {
            load_centers_data()
        });
}