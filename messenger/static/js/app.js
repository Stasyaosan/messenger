$('.enter-click').keydown(function(e) {
       if(e.keyCode === 13) {
        sendMessage();
       }
   });

let m_2 = false;
        $('.click_chat').on('click', function(){
            if(m_2==false){
                $(this).next().hide();
                m_2=true;
            }else{

            }
        });

$('.show_error').hide();

function btn_reg (){
    let login = $('#login').val();
    let password = $('#password').val();
    let email = $('#email').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
            url: '/ajaxReg',
            method: 'post',
            dataType: 'html',
            data: {csrfmiddlewaretoken: token, login: login, password: password, email: email},
            success: function(data){
                if(data == 1){
                    $('.alert').show();
                $('.alert').addClass('alert-danger');
                $('.alert').removeClass('alert-success');
                $('.alert').text('Такой пользователь уже есть!');
                } else {
                $('.alert').show();
                $('.alert').addClass('alert-success');
                $('.alert').removeClass('alert-danger');
                $('.alert').text('Активируйте аккаунт в электронном письме!');
                }
            }
            });
    }

function btn_auth (){
    let password = $('#password').val();
    let email = $('#email').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
            url: '/ajaxAuth',
            method: 'post',
            dataType: 'html',
            data: {csrfmiddlewaretoken: token, password: password, email: email},
            success: function(data){
                if(data == 4){
                    $('.alert').show();
                    $('.alert').addClass('alert-danger');
                    $('.alert').removeClass('alert-success');
                    $('.alert').text('Такого пользователя не существует!');
                }
                else if (data == 1){
                    $('.alert').show();
                    $('.alert').addClass('alert-danger');
                    $('.alert').removeClass('alert-success');
                    $('.alert').text('Учётная запись не активирована!');
                }
                else if (data == 2){
                    $('.alert').show();
                    $('.alert').addClass('alert-danger');
                    $('.alert').removeClass('alert-success');
                    $('.alert').text('Неверный пароль!');
                } else {
                    document.location.href='/profile';
                }

            }
    });
}

