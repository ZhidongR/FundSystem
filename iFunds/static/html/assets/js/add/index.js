// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }

// // 将时间戳转化为时间
// function getTime(nS) {
//     if (nS.length == 10) {
//         var date = new Date(parseInt(nS) * 1000);
//     }
//     else {
//         var date = new Date(parseInt(nS))
//     }
//     var year = date.getFullYear();
//     var mon = date.getMonth() + 1;
//     var day = date.getDate();
//     var hours = date.getHours();
//     var minu = date.getMinutes();
//     var sec = date.getSeconds();
//     // return year+'/'+mon+'/'+day+' '+hours+':'+minu+':'+sec;
//     return year + '/' + mon + '/' + day;
// }

// // 将字符串yyyy-MM-dd hh:mm转化为时间
// function converDateFromString(dateString) {
//     if(dateString){
//         var arr1=dateString.split(" ");
//         var sdate=arr1[0].split("-");
//         var stime=arr1[1].split(":");
//         var date=new Date(sdate[0],sdate[1]-1,sdate[2],stime[0],stime[1]);
//         return date;
//     }
// }


// //---------------纯接口函数开始------------------------

// /**
//  * @function 用户注册
//  * @param {Map} params 字典需要包含name，phone,password1,password2,image_code,uuid
//  * @return true or false
//  */
// function register(params_data) {
//     //
//     var bool_flag = false;
//     var params = {
//         "name": params_data.name,
//         "phone": params_data.phone,
//         "password1": params_data.password1,
//         "password2": params_data.password2,
//         "image_code": params_data.image_code,
//         "uuid": params_data.uuid,
//     };

//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/user',
//         type: 'POST',
//         data: params,
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 bool_flag = true;
//                 return bool_flag;
//             } else {
//                 bool_flag = false;
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             console.log(res.msg);
//             bool_flag = false;
//             return false;
//         }
//     });
//     return bool_flag;

// }

// /** 
// * @function 用户登录
// * @param account {String} 用户账号
// * @param password {String} 用户密码
// * @return {Boolean} true:登录成功;false:登录失败
// */
// function login(account, password) {
//     // 定义登录状态布尔值
//     var bool_flag = false;
//     var params = {
//         'phone': account,
//         'password': password
//     };
//     // url:'http://127.0.0.1:5000/api/1.0/sessions',
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/sessions',
//         type: 'post',
//         data: JSON.stringify(params),
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 // 登录成功
//                 // alert(res.msg);
//                 bool_flag = true;
//                 return true;
//             } else {
//                 console.log(res.msg);
//                 bool_flag = false;
//                 return false;
//             }
//         },
//         error: function (res) {
//             bool_flag = false;
//             console.log(res);
//             return false;
//         }
//     });
//     return bool_flag;
// }

// /** 
// * @function 用户退出登录
// * @return {Boolean} true:退出登录成功;false:退出登录失败
// */
// function logout() {
//     // 定义登录状态布尔值
//     var bool_flag = false;
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/sessions',
//         type: 'delete',
//         data: null,
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 bool_flag = true;
//                 location.href = "/login.html";
//             } else {
//                 bool_flag = false;
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             console.log(res.msg);
//             bool_flag = false;
//             return false;
//         }
//     });
//     return bool_flag;
// }


// /** 
// * @function 获取用户基本信息,成功则返回json数据
// * @return {string} 用户名，后续会继续有头像等信息
// */
// function get_user_info() {
//     //定义返回值
//     var re_map = {};
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/sessions',
//         type: 'get',
//         data: null,
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 // console.log(res.msg);
//                 var user_name = res.data.name;
//                 re_map["name"] = user_name;
//                 return user_name;
//             } else {
//                 re_map = {};
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             re_map = {};
//             console.log(res.msg);
//             return false;
//         }
//     });
//     return re_map;
// }


// /**
//  * @function 添加用户的喜爱基金
//  * @param {*} fund_code_ls 数组,喜爱基金的数组
//  * @return {boolean} true or false
//  */
// function add_favourite_fund(fund_code_ls) {
//     //定义返回的值
//     var bool_flag = false;
//     var params = {
//         "favourite_fund_ls": fund_code_ls
//     };

//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/funds/favourite',
//         type: 'post',
//         data: JSON.stringify(params),
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 console.log("添加成功");
//                 bool_flag = true;
//                 return true;
//             } else {
//                 bool_flag = false;
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             bool_flag = false;
//             console.log(res.msg);
//             return false;
//         }
//     });
//     return bool_flag;
// }

// /**
//  * @function 获取用户喜爱的基金列表信息
//  * @return 用户喜爱基金列表的字典类型
//  */
// function get_favourite_fund() {
//     //定义函数体返回的字典变量
//     var re_map = {};
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/funds/favourite',
//         type: 'get',
//         data: null,
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 re_map = res.data;
//             } else {
//                 re_map = {};
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             re_map = {};
//             console.log(res.msg);
//             return false;
//         }
//     });
//     return re_map;
// }


// /**
//  * @function 删除用户的喜爱基金
//  * @param {*} delete_fund_ls 数组,需要删除喜爱基金的数组
//  * @return {boolean} true or false
//  */
// function delete_favourite_fund(delete_fund_ls) {
//     //定义函数返回结果的bool变量
//     var bool_flag = false;
//     var params = {
//         "delete_fund_ls": delete_fund_ls
//     };

//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/funds/favourite',
//         type: 'delete',
//         data: JSON.stringify(params),
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 bool_flag = true;
//                 console.log(res.msg)
//             } else {
//                 bool_flag = false;
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             bool_flag = false;
//             console.log(res.msg);
//             return false;
//         }
//     });
//     return bool_flag;
// }

// /**
//  * @function 通过基金代号获取基金的信息
//  * @param {*} fund_code_ls 由基金代号组成的数组
//  * @return 包含基金信息字典的数组
//  */
// function get_fund_info(fund_code_ls) {
//     //定义函数返回的数组
//     var table_data = [];

//     var params = {
//         "fund_code_ls": fund_code_ls
//     };
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/funds',
//         type: 'post',
//         data: JSON.stringify(params),
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 // 返回成功并正常
//                 $.each(res.data, function (index, value) {
//                     if (-1 != $.inArray(index, fund_code_ls)) {
//                         var table_data_dict = {};
//                         table_data_dict.fund_name = value.fund_name;
//                         table_data_dict.fund_code = value.fund_code;
//                         table_data_dict.syl_1m = value.syl_1m;
//                         table_data_dict.syl_3m = value.syl_3m;
//                         table_data_dict.syl_6m = value.syl_6m;
//                         table_data_dict.syl_1y = value.syl_1y;
//                         table_data.push(table_data_dict);
//                     }
//                 });
//                 return table_data;
//             } else {
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             return false;
//         }
//     });
//     return table_data;

// }


// function get_news() {
//     //用于存返回变量
//     var re_data = [];
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/news',
//         type: 'get',
//         data: null,
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 // 返回成功并正常
//                 re_data = res.data;
//                 return re_data;
//             } else {
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             return false;
//         }
//     });
//     return re_data;
// }


// /**
//  * @function 获取大盘的行情数据，
//  * @returns array内嵌套字典
//  */
// function get_generate_fund_data() {
//     var re_data = [];
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/funds/generate',
//         type: 'get',
//         data: null,
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 // 返回成功并正常
//                 re_data = res.data;
//                 return re_data;
//             } else {
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             return false;
//         }
//     });
//     return re_data;
// }

// function trace_to_server(set_data){
//     var bool_flag = false;
//     var params = set_data;
//     var return_data={};
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/trace',
//         type: 'post',
//         data: JSON.stringify(params),
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 bool_flag = true;
//                 console.log(res.data);
//                 return_data=res.data;
//                 return true;
//             } else {
//                 bool_flag = false;
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             bool_flag = false;
//             console.log(res.msg);
//             return false;
//         }
//     });
//     return bool_flag,return_data;

// }


// function get_trace_record(days){
//     var bool_flindexag = false;
//     var return_data={};
//     $.ajax({
//         async: false,//false同步，页面会出现假死，直至ajax代码执行完;true异步
//         url: 'api/1.0/trace',
//         type: 'get',
//         data: days,
//         contentType: 'application/json',
//         headers: { 'X-CSRFToken': getCookie('csrf_token') },
//         success: function (res) {
//             if (res.code == '0') {
//                 bool_flag = true;
//                 console.log(res.data);
//                 return_data=res.data;
//                 return true;
//             } else {
//                 bool_flag = false;
//                 console.log(res.msg);
//                 return false;
//             }
//         },
//         error: function (res) {
//             bool_flag = false;
//             console.log(res.msg);
//             return false;
//         }
//     });
//     return bool_flag,return_data;

// }

// //---------------纯接口函数结束------------------------

//用户登录状态下，更新显示用户的头像

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


//进行基金的Table画图
function init_fund_table(fund_code_ls) {
    // var fund_code_ls = ["001766", "165525", "379010"];
    var table_data = get_fund_info(fund_code_ls);
    // var table_data = new Array(demoa(fund_code_ls));
    var tableColums = [
        { field: "fund_name", title: "基金名", sortable: true },
        { field: "fund_code", title: "基金代号", sortable: true },
        { field: "current_price", title: "最新净值", sortable: true },
        { field: "syl_1m", title: "1月收益率(%)", sortable: true },
        { field: "syl_3m", title: "3月收益率(%)", sortable: true },
        { field: "syl_6m", title: "6月收益率(%)", sortable: true },
        { field: "syl_1y", title: "1年收益率(%)", sortable: true },
        { field: "rate", title: "费率(%)", sortable: true },
    ];
    $('#fund-table').bootstrapTable(
        {
            columns: tableColums,
            data: table_data,
            pageSize: 10,
            pageNumber: 1,
            fixedColumns: true, 
            fixedNumber: 1, //固定列数
        }
    );
 }



// 更新图表数据并调用画图函数，ac_worth_trend净值趋势
/**
 * 向后端请求x-y数据，显示xy轴的图
 * @param {array} fund_code_ls 数组
 * @returns 
 */
function update_overview(fund_code_ls) {

    var params = {
        "fund_code_ls": fund_code_ls
    };
    $.ajax({
        async: true,//false同步，页面会出现假死，直至ajax代码执行完;true异步
        url: 'api/1.0/funds',
        type: 'post',
        data: JSON.stringify(params),
        contentType: 'application/json',
        headers: { 'X-CSRFToken': getCookie('csrf_token') },
        success: function (res) {
            if (res.code == '0') {
                // 返回成功并正常
                var k = 1;
                var html_template="";
                $.each(res.data, function (index, val) {
                    if (-1 != $.inArray(index, fund_code_ls)) {
                        var ac_trend_worth_dict = [];
                        var ac_worth_trend = val.ac_worth_trend;
                        for (var i = 0; i < ac_worth_trend.length; i++) {
                            // 将时间戳转化为时间
                            ac_worth_trend[i][0] = getTime(ac_worth_trend[i][0])
                            ac_trend_worth_dict.push({ date: ac_worth_trend[i][0], visits: ac_worth_trend[i][1] });
                        }
                        var id = 'amlinechart' + k;
                        html_template = '<div class="card""><div class="card-body"><div id="'+ id +'"></div></div></div>';
                        $('#amcharts').append(html_template);
                        console.log(ac_trend_worth_dict);
                        draw_amlinechart3(id, ac_trend_worth_dict, val.fund_name+"-"+val.fund_code);
                        k = k + 1;

                    }
                });
            } else {
                console.log(res.msg);
                return false;
            }
        },
        error: function (res) {
            return false;
        }
    });
    return false;
}

function draw_generate_graphs() {

    var data_ls_set=get_generate_fund_data();// array中内嵌set
    // for(var i=0; i<data_ls_set.length;i++){

    // }
    $.each(data_ls_set, function(index1, data_set) {
        trends_array = data_set.trends;
        fund_code = data_set.code;
        fund_name = data_set.name;
        var ls_set_data=[];
        var id ="amlinechart"+(index1+1);
        var table_title=fund_name+"-"+fund_code;
        $.each(trends_array,function (index2,trend){
            //"2022-04-13 09:30,989.66,989.66,994.44,989.66,20796,92971949.00,992.523"
            var trend1 = trend.split(",");
            // var date_time= getTime(trend1[0]);
            // var date_time = $.datepicker.parseDate("yy-mm-dd HH:mm",  trend1[0]);
            var date_time=trend1[0];
            var avr_value= 0.0;
            var sum=0.0;
            for(var i=1;i<5;i++){
                sum+=parseFloat(trend1[i]);
            }
            avr_value = sum/4.0;
            ls_set_data.push({date: date_time, visits: avr_value});
        });
        var html_template = '<div class="card""><div class="card-body"><div id="'+ id +'"></div></div></div>';
        $('#amcharts').append(html_template);
        draw_amlinechart3(id,ls_set_data,table_title);
    });

}

/**
 * 画x-y图
 * @param {*} id html中的元素id
 * @param {*} data_ls 数组
 */
function draw_amlinechart3(id, data_ls,table_title) {
    if ($('#' + id).length) {
        var title=table_title;
        var chartData = data_ls;
        // var chartData = generateChartData();
        var chart = AmCharts.makeChart(id, {   //verview-shart, amlinechart3
            "autoMargins": true, //自动调整边框
            "type": "serial",
            "theme": "light",
            "marginRight": 20,
            "autoMarginOffset": 20,
            "marginTop": 7,
            "dataProvider": chartData,
            "titles": [
                {
                  "text": title,
                  "size": 20
                }
              ],
            "valueAxes": [{
                "axisAlpha": 0.2,
                "dashLength": 1,
                "position": "left"
            }],
            "mouseWheelZoomEnabled": true,
            "graphs": [{
                "useNegativeColorIfDown": true,
                "id": "g1",
                "balloonText": "[[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "bulletColor": "#FFFFFF",
                "hideBulletsCount": 50,
                "title": "red line",
                "valueField": "visits",
                "useLineColorForBulletBorder": true,
                "balloon": {
                    "drop": true
                }
            }],
            "chartScrollbar": {
                "autoGridCount": true,
                "graph": "g1",
                "scrollbarHeight": 40,
                "color": "#fff",
                "selectedBackgroundAlpha": 1,
                "selectedBackgroundColor": "#815BF6",
                "selectedGraphFillAlpha": 0,
                "selectedGraphFillColor": "#8918FE",
                "graphLineAlpha": 0.2,
                "graphLineColor": "#c2c2c2",
                "selectedGraphLineColor": "#fff",
                "selectedGraphLineAlpha": 1
            },
            "chartCursor": {
                "limitToGraph": "g1",
                "categoryBalloonDateFormat": "MM-DD JJ:NN",
                "cursorPosition": "mouse"
            },
            "categoryField": "date",
            "categoryAxis": {
                "minPeriod": "mm",
                "parseDates": true,
                // "equalSpacing":true,
                "axisColor": "#DADADA",
                "dashLength": 1,
                "minorGridEnabled": true,
                "minorGridAlpha": 0.01
            },
            "export": {
                "enabled": false
            }
        });
        chart.addListener("rendered", zoomChart);
        zoomChart();
        // this method is called when chart is first inited as we listen for "rendered" event
        function zoomChart() {
            // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
            chart.zoomToIndexes(chartData.length - 40, chartData.length - 1);
        }
        
        window.onresize = chart.resize;

        // generate some random data, quite different range
        function generateChartData() {
            var chartData = [];
            var firstDate = new Date();
            firstDate.setDate(firstDate.getDate() - 5);
            var visits = 1200;
            for (var i = 0; i < 1000; i++) {
                // we create date objects here. In your data, you can have date strings
                // and then set format of your dates using chart.dataDateFormat property,
                // however when possible, use date objects, as this will speed up chart rendering.
                var newDate = new Date(firstDate);
                newDate.setDate(newDate.getDate() + i);

                visits += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);

                chartData.push({
                    date: newDate,
                    visits: visits
                });
            }
            return chartData;
        }
    }
    /*-------------- 3 line chart amchart end ------------*/

}


/**
 * 显示新闻的图片和标题，简要
 */
function show_news() {
    var news_array = get_news();
    $.each(news_array, function (i, news) {
        if (i < 5) { //展示5条新闻
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
        }
    });

    // $.each(news_array,function(news){
    //     $.each(news,function(key,value){
    //         console.log(key,value);
    //     }
    // })
}


$(document).ready(function () {

    show_user_info();
    var fund_code_ls = ["004855", "001767", "165525", "001766", "005224", "001595"];
    // update_overview(fund_code_ls);
    draw_generate_graphs();
    logoutButton = $("#dd-logout");
    logoutButton.click(function () {
        logout();
    });
    init_fund_table(fund_code_ls);

    // add_favourite_fund(fund_code_ls);
    // delete_favourite_fund(fund_code_ls);
    show_news();
    // var set_data1={'fund_code':"320007","buy_flag":"1","buy_money":10000.99};
    // var set_data2={"fund_code":"320007","sale_flag":"1","sale_num":1000.22};
    // trace_to_server(set_data1);
    // trace_to_server(set_data2);
    // get_trace_record(5);
});