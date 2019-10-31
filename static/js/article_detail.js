$("#div_digg .action").click(function () {


    if ($('.info').attr('username')) {
        //点赞或踩灭
        var is_up = $(this).hasClass('diggit');
        // var article_id = '{{ article.pk }}';
        var article_id = $('.info').attr('article_id');

        //ajax
        $.ajax({
            url: '/blog/up_down/',
            type: 'post',
            data: {
                is_up: is_up,
                article_id: article_id,
            },
            success: function (data) {
                console.log(data)
                //点赞或者取消，成功
                if (data.state) {
                    //is_up是在上边的变量
                    if (is_up) {
                        var val = $("#digg_count").text();
                        val = parseInt(val) + 1;
                        $("#digg_count").text(val)
                    } else {
                        var val = $("#bury_count").text();
                        val = parseInt(val) + 1;
                        $("#bury_count").text(val)
                    }
                } else {
                    if (data.first_action) {
                        $('#digg_tips').html('你已经推荐过')
                    } else {
                        $('#digg_tips').html('你已经反对过')
                    }
                    setTimeout(function () {
                        $('#digg_tips').html("")
                    }, 1000)
                }
            }
        })
    } else {
        location.href = "/login/"
    }
});