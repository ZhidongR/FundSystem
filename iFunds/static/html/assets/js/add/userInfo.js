
//用户登录状态下，更新显示用户的信息
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


function show_user_detail() {
    var user_info=get_user_info();
    
    $("#userName").val(user_info.name);
    $("#userEamil").val(user_info.emali);
    $("#userPhone").val(user_info.phone);
    $("#userMoney").val(user_info.balance);
    $("#userAmount").val(user_info.hold_fund_amount);
    $("#userProfit").val(user_info.hold_fund_profit);
    $("#dayProfit").val(user_info.last_profit);
    $("#updateTime").val(user_info.current_time);

}


$(document).ready(function () {
    show_user_info();
    show_user_detail();
    logoutButton = $("#dd-logout");
    logoutButton.click(function () {
        logout();
    });
});