function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//需要通过JavaScript代码来做的两件事情
//1.button被按下的时候，需要将文本框中的数据获取到，然后发送给服务器端，最后接收服务器返回的数据，填充到我们预留的div中，这样用户就可以看到结果
//2.文本框上，用户按键之后，需要判断文本框中的内容是否为空，如果不为空，继续执行
//3.进行登录接口调用，如登录接口返回登录成功，则跳转到主页index.html
$(document).ready(function () {
    //这里面的内容就是页面装载完成后需要执行的代码

    $("#exampleAccount").focus(function () {
        $("#account-err").hide();
    });
    $("#examplePassword").focus(function () {
        $("#password-err").hide();
    });


    //需要找到button按钮，注册事件
    $("#form_submit").click(function () {
        //获取文本框的内容
        var account = $("#exampleAccount").val();
        var password = $("#examplePassword").val();
        //将这个内容发送给服务器端
        if (account == "") {
            // alert("用户名不能为空");
            $("#account-err span").html("Account can't be null!");
            $("#account-err").show();
            return;
        }
        if (password == "") {
            // alert("密码不能为空");
            $("#password-err span").html("Password can't be null!");
            $("#password-err").show();
            return;
        }
        var params = {
            'phone': account,
            'password': password
        };
        // url:'http://127.0.0.1:5000/api/1.0/sessions',
        $.ajax({
            async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
            url: 'api/1.0/sessions',
            type: 'post',
            data: JSON.stringify(params),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': getCookie('csrf_token') },
            success: function (res) {
                if (res.code == '0') {
                    // 登录成功
                    // alert(res.msg);
                    location.href = '/index.html';
                } else {
                    alert(res.msg);
                    return false;
                }
            },
            error: function (res) {
                alert(res);
                return false;
            }
        });
        return false; //不清楚为什么加了这句，ajax内的代码能够在这句之后正常执行，时间差关系？ //https://blog.csdn.net/lezizai_happy/article/details/51627794
    });
});