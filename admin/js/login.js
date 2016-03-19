


function login(el){
    var form = $(el).parent().parent();
    $.ajax({
            url: 'http://api.volnekurty.cz/login',
            method: 'POST',
            data: {
                username: form.find('input#inputEmail').val(),
                password: form.find('input#inputPassword').val()
            }

    }
    )
}

