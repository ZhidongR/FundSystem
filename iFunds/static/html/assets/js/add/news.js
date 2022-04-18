function show_user_info() {

    //更新页面
    function update_user_name(user_name) {
        //Kumkum Rai <i class="fa fa-angle-down"></i>
        //此处如果class有多个（即空格隔开），可以用.class1.class2来处理
        $(".user-name.dropdown-toggle").html(user_name + '<i class="fa fa-angle-down"></i>');
        return true;
    };

    var map1 = get_user_info();
    update_user_name(map1.name);
    return true;
}


/**
 * 显示新闻的图片和标题，简要
 */
function show_news() {
    var news_array = get_news();
    $.each(news_array, function (i, news) {
        var img_id = 'news' + (i + 1) + '-img';
        var content_id = 'news' + (i + 1) + '-content';
        var createobj = $("#news1-img").parent().prop("outerHTML");
        createobj = createobj.replace("news1-img", img_id);
        createobj = createobj.replace("news1-content", content_id);
        if (i + 1 > 2) {
            $("#news-list").append(createobj);
        }
        $('#' + img_id).children("img").attr('src', news.imgurl);
        $('#' + img_id).children("img").width("95%");
        var a_href='<a href="'+news.docurl +'">'+ news.title +'</a>';
        $('#' + content_id).children("h2").html(a_href);
    });

    // $.each(news_array,function(news){
    //     $.each(news,function(key,value){
    //         console.log(key,value);
    //     }
    // })
}


$(document).ready(function () {

    show_user_info();
    logoutButton = $("#dd-logout");
    logoutButton.click(function () {
        logout();
    });
    show_news();
 
});