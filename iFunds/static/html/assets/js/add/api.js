function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 将时间戳转化为时间
function getTime(nS) {
    if (nS.length == 10) {
        var date = new Date(parseInt(nS) * 1000);
    }
    else {
        var date = new Date(parseInt(nS))
    }
    var year = date.getFullYear();
    var mon = date.getMonth() + 1;
    var day = date.getDate();
    var hours = date.getHours();
    var minu = date.getMinutes();
    var sec = date.getSeconds();
    // return year+'/'+mon+'/'+day+' '+hours+':'+minu+':'+sec;
    return year + '/' + mon + '/' + day;
}

// 将字符串yyyy-MM-dd hh:mm转化为时间
function converDateFromString(dateString) {
    if(dateString){
        var arr1=dateString.split(" ");
        var sdate=arr1[0].split("-");
        var stime=arr1[1].split(":");
        var date=new Date(sdate[0],sdate[1]-1,sdate[2],stime[0],stime[1]);
        return date;
    }
}


//---------------纯接口函数开始------------------------

/**
 * @function 用户注册
 * @param {Map} params 字典需要包含name，phone,password1,password2,image_code,uuid
 * @return true or false
 */
function register(params_data) {
    //
    var bool_flag = false;
    var params = {
        "name": params_data.name,
        "phone": params_data.phone,
        "password1": params_data.password1,
        "password2": params_data.password2,
        "image_code": params_data.image_code,
        "uuid": params_data.uuid,
    };

    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/user',
        type: 'POST',
        data: params,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                bool_flag = true;
                return bool_flag;
            } else {
                bool_flag = false;
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            console.log(res.msg);
            bool_flag = false;
            return false;
        }
    });
    return bool_flag;

}

/** 
* @function 用户登录
* @param account {String} 用户账号
* @param password {String} 用户密码
* @return {Boolean} true:登录成功;false:登录失败
*/
function login(account, password) {
    // 定义登录状态布尔值
    var bool_flag = false;
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
                bool_flag = true;
                return true;
            } else {
                console.log(res.msg);
                bool_flag = false;
                return false;
            }
        },
        error: function (res) {
            bool_flag = false;
            console.log(res);
            return false;
        }
    });
    return bool_flag;
}

/** 
* @function 用户退出登录
* @return {Boolean} true:退出登录成功;false:退出登录失败
*/
function logout() {
    // 定义登录状态布尔值
    var bool_flag = false;
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/sessions',
        type: 'delete',
        data: null,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                bool_flag = true;
                location.href = "/login.html";
            } else {
                bool_flag = false;
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            console.log(res.msg);
            bool_flag = false;
            return false;
        }
    });
    return bool_flag;
}


/** 
* @function 获取用户基本信息,成功则返回json数据
* @return {string} 用户名，后续会继续有头像等信息
*/
function check_login_or_not() {
    //定义返回值
    var re_map = {};
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/sessions',
        type: 'get',
        data: null,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                re_map= res.data
                return re_map;
            } else {
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            console.log(res.msg);
            return false;
        }
    });
    return re_map;
}

function get_user_info() {
    //定义返回值
    var re_map = {};
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/user',
        type: 'get',
        data: null,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                re_map= res.data
                return re_map;
            } else {
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            console.log(res.msg);
            return false;
        }
    });
    return re_map;
}


/**
 * @function 添加用户的喜爱基金
 * @param {*} fund_code_ls 数组,喜爱基金的数组
 * @return {boolean} true or false
 */
function add_favourite_fund(fund_code_ls) {
    //定义返回的值
    var bool_flag = false;
    var params = {
        "favourite_fund_ls": fund_code_ls
    };

    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/funds/favourite',
        type: 'post',
        data: JSON.stringify(params),
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                console.log("添加成功");
                bool_flag = true;
                return true;
            } else {
                bool_flag = false;
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            bool_flag = false;
            console.log(res.msg);
            return false;
        }
    });
    return bool_flag;
}

/**
 * @function 获取用户喜爱的基金列表信息
 * @return 用户喜爱基金列表,列表每个元素为字典类型
 */
function get_favourite_fund() {
    //定义函数体返回的字典变量
    var re_arry = [];
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/funds/favourite',
        type: 'get',
        data: null,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                re_arry = res.data;
            } else {
                re_arry = [];
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            re_arry = [];
            console.log(res.msg);
            return false;
        }
    });
    return re_arry;
}


/**
 * @function 删除用户的喜爱基金
 * @param {*} delete_fund_ls 数组,需要删除喜爱基金的数组
 * @return {boolean} true or false
 */
function delete_favourite_fund(delete_fund_ls) {
    //定义函数返回结果的bool变量
    var bool_flag = false;
    var params = {
        "delete_fund_ls": delete_fund_ls
    };

    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/funds/favourite',
        type: 'delete',
        data: JSON.stringify(params),
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                bool_flag = true;
                console.log(res.msg)
            } else {
                bool_flag = false;
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            bool_flag = false;
            console.log(res.msg);
            return false;
        }
    });
    return bool_flag;
}

/**
 * @function 通过基金代号获取基金的信息
 * @param {*} fund_code_ls 由基金代号组成的数组
 * @return 包含基金信息字典的数组
 */
function get_fund_info(fund_code_ls) {
    //定义函数返回的数组
    var table_data = [];

    var params = {
        "fund_code_ls": fund_code_ls
    };
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/funds',
        type: 'post',
        data: JSON.stringify(params),
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                // 返回成功并正常
                table_data = res.data;
                return table_data;
            } else {
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            return false;
        }
    });
    return table_data;

}


/**
 * @function 获取用户持有的基金列表信息
 * @return 用户喜爱基金列表的array：内嵌set的元素
 */
 function get_hold_fund() {
    //定义函数体返回的字典变量
    var re_arr = [];
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/funds/hold',
        type: 'get',
        data: null,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                re_arr = res.data;
            } else {
                re_arr = [];
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            re_arr = [];
            console.log(res.msg);
            return false;
        }
    });
    return re_arr;
}


function get_news() {
    //用于存返回变量
    var re_data = [];
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/news',
        type: 'get',
        data: null,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                // 返回成功并正常
                re_data = res.data;
                return re_data;
            } else {
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            return false;
        }
    });
    return re_data;
}


/**
 * @function 获取大盘的行情数据，
 * @returns array内嵌套字典
 */
function get_generate_fund_data() {
    var re_data = [];
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/funds/generate',
        type: 'get',
        data: null,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                // 返回成功并正常
                re_data = res.data;
                return re_data;
            } else {
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            return false;
        }
    });
    return re_data;
}

/**
 * 交易基金接口，可以出售或者买入
 * @param {*} set_data 字典，参数例子：1. 买入：{"fund_code":"165525","buy_flag":"1","buy_money":5555.99}；2.出售：{"fund_code":"165525","sale_flag":"1","sale_num":8999.56}
 * @returns 买入成功返回2个参数，1为ture，2为data={"fund_code":"165525","buy_money":10000.99,"accept_time":"20220101 14:50:00"};
 * 卖出成功返回2个参数，1为true,2为data={"fund_code":"165525","sale_num":8999.56,"accept_time":"20220101 14:50:00"}。
 * 失败仅返回一个false.
 */
function trace_to_server(set_data){
    var bool_flag = false;
    var params = set_data;
    var return_data={};
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/trace',
        type: 'post',
        data: JSON.stringify(params),
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                bool_flag = true;
                console.log(res.data);
                return_data=res.data;
                return true;
            } else {
                bool_flag = false;
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            bool_flag = false;
            console.log(res.msg);
            return false;
        }
    });
    return bool_flag,return_data;

}

/**
 * 
 * @param {*} days 最近天数
 * @returns 第一个参数为True or False，第二个参数为array，每个元素为字典
 */
function get_trace_record(days){
    var bool_flag = false;
    var re_arr=[];
    $.ajax({
        async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/trace',
        type: 'get',
        data: days,
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                bool_flag = true;
                re_arr=res.data;
                return re_arr;
            } else {
                bool_flag = false;
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            bool_flag = false;
            console.log(res.msg);
            return false;
        }
    });
    if (bool_flag){
        return re_arr;
    }
    else{
        return bool_flag;
    }


}

//---------------纯接口函数结束------------------------