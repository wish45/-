function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    //모든 ajax요청 전에 호출되는 함수를 지정
    beforeSend: function(xhr, settings) {
      //csrf token 설정이 필요한 요청이면
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            //토큰값을 가져와서 요청 헤더에 심어준다.
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//장고에서는 모든 post요청에 대해 csrftoken체크를 하도록 되어있다.