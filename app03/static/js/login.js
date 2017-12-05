function clearerror() {
    $('.loginerror').html('')
}


$('button[type=submit]').click(function () {
    var formData = new FormData();
    formData.append("username", $(":text").val());
    formData.append("password", $(":password").val());
    $.ajax({
        url: '/login/',
        type: 'POST',
        headers: {"X-CSRFToken": $.cookie('csrftoken')},
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            var data = JSON.parse(data);
            if (!data['flag']) {
                $('.loginerror').html('用户名或密码错误');
                setTimeout(clearerror, 3000)
            }
        }
    })


});