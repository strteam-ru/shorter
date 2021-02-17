$(document).ready(function () {
    console.log("ready!");

    $("#write_link").on("click", function () {
        var formData = $("form").serialize();
        $.ajax({
            url: "/",
            type: 'post',
            data: formData,
            success: function (data) {
                if (data) {
                    data = JSON.parse(data);
                    console.log(data)
                    if (data.result == true) {
                        $('.error_note').addClass('d-none');
                        $('.success_note').empty()
                        $('.success_note').html('Ссылка успешно сохранена <a href="/">Ок</a>')
                        $('.success_note').removeClass('d-none');
                    } else {
                        $('.error_note').empty()
                        if (typeof (data.errors) == 'string') {
                            text = data.errors
                        } else {
                            text = $.param(data.errors)
                            console.log(text)
                        }
                        $('.error_note').empty()
                        $('.error_note').text(decodeURIComponent(text));
                        $('.error_note').removeClass('d-none');
                    }

                } else {
                    $('.error_note').empty()
                    $('.error_note').text('Ошибка сервера');
                    $('.error_note').removeClass('d-none');
                }
            },
            error: function () {
                $('.error_note').empty()
                $('.error_note').text('Ошибка сервера');
                $('.error_note').removeClass('d-none');
            }
        });
    });

    $("[name='short_link']").on('change', function () {
        var formData = $("form").serialize();
        $.ajax({
            url: "/ajax/check_short_link",
            type: 'post',
            data: formData,
            success: function (data) {
                if (data) {
                    data = JSON.parse(data);
                    console.log(data)
                    if (data.result == true) {
                        $('.error_note').addClass('d-none');
                        $('[name="short_link"]').val(data.value);
                    } else {
                        $('.error_note').empty()

                        $('.error_note').text(data.value);
                        $('.error_note').removeClass('d-none');
                    }

                } else {
                    $('.error_note').empty()
                    $('.error_note').text('Ошибка сервера');
                    $('.error_note').removeClass('d-none');
                }
            },
            error: function () {
                $('.error_note').empty()
                $('.error_note').text('Ошибка сервера');
                $('.error_note').removeClass('d-none');
            }
        });
    });
});