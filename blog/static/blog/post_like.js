$(function(){
   $(".post_like_button").click(function () {
        var like_url = $(this).data('url');
        var target_id = $(this).data('target-id');
        $.get(like_url).
            done(function (data) {
                $('#'+target_id).html(data.like_count);
        }).
            fail(function () {
                alert('failed');
        });
        return false;
   });
});