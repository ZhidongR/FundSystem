function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

var uuid = "";
var last_uuid = '';

function generateImageCode() {
    uuid = generateUUID();  //生成UUID
    // /api/1.0/verify_img?phone=15512345679&uuid=1234567&last_uuid=99999
    var url = '/api/1.0/verify_img?uuid=' + uuid + '&last_uuid=' + last_uuid;   //拼接请求地址
    $('#img_check').attr('src', url);  //设置img的src属性
    last_uuid = uuid;  //设置上一个UUID
}


//需要通过JavaScript代码来做的两件事情
//1.button被按下的时候，需要将文本框中的数据获取到，然后发送给服务器端，最后接收服务器返回的数据，填充到我们预留的div中，这样用户就可以看到结果
//2.文本框上，用户按键之后，需要判断文本框中的内容是否为空，如果不为空，继续执行
//3.进行登录接口调用，如登录接口返回登录成功，则跳转到login.index中
$(document).ready(function () {
    //这里面的内容就是页面装载完成后需要执行的代码

    // $("#exampleAccount").focus(function () {
    //     $("#account-err").hide();
    // });

    generateImageCode();

    $("#img_check").click(function () {
        generateImageCode();
    });

    $("#exampleName").focus(function () {
        $("#name-err").hide();
    })
    $("#examplePhone").focus(function () {
        $("#phone-err").hide();
    })
    $("#examplePassword1").focus(function () {
        $("#password1-err").hide();
    })
    $("#examplePassword2").focus(function () {
        $("#password2-err").hide();
    })
    $("#checkcode").focus(function () {
        $("#checkcode-err").hide();
    })

    //需要找到button按钮，注册事件
    $("#form_submit").click(function () {
        //获取文本框的内容
        var username = $("#exampleName").val();
        var phone = $("#examplePhone").val();
        var password1 = $("#examplePassword1").val();
        var password2 = $("#examplePassword2").val();
        var image_code = $("#checkcode").val();
        
        if (username == "") {
            $("#name-err span").html("name can't be null!");
            $("#name-err").show();
            return false;
        }
        if (phone == "") {
            $("#phone-err span").html("phone can't be null!");
            $("#phone-err").show();
            return false;
        }
        if (password1 == "") {
            $("#password1-err span").html("password1 can't be null!");
            $("#password1-err").show();
            return false;
        }
        if (password2 == "") {
            $("#password2-err span").html("password2 can't be null!");
            $("#password2-err").show();
            return false;
        }
        if (password1 != password2) {
            $("#password-not-equal span").html("password1 != password2");            
            $("#password-not-equal").show();
            setTimeout(function(){
                $("#password-not-equal").hide();
                },2000);
            return false;
        }
        if (image_code == "") {
            $("#checkcode-err span").html("check code can't be null!");
            $("#checkcode-err").show();
            return false;
        }
        var params={
            'uuid':uuid,
            'phone':phone,
            'image_code':image_code,
            'name': username,
            'password1':password1,
            'password2':password2
        };

        // url:'/api/1.0/user'',
        $.ajax({
            async: true,//false同步，页面会出现假死，直至ajax代码执行完;true异步
            url: 'api/1.0/user',
            type: 'post',
            data: JSON.stringify(params),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': getCookie('csrf_token') },
            success: function (res) {
                if (res.code == '0') {
                    alert(res.msg);
                    location.href = '/login.html';
                } else {
                    alert(res.msg);
                    return false;
                }
            },
            error: function (res) {
                alert(res);
                alert(res.code);
                alert(res.msg);
                return false;
            }
        });
        return false; //不清楚为什么加了这句，ajax内的代码能够在这句之后正常执行，时间差关系？ //https://blog.csdn.net/lezizai_happy/article/details/51627794
    });
});