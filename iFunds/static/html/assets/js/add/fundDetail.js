
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


//进行基金的Table画图
function init_fund_table() {
    var hold_fund_info_ls = get_hold_fund();
    var tableColums = [
        { field: "fund_name", title: "基金名", sortable: true },
        { field: "fund_code", title: "基金代号", sortable: true },
        { field: "hold_num", title: "持有份数", sortable: true },
        { field: "last_price", title: "上一交易日净值", sortable: true },
        { field: "current_price", title: "最新净值", sortable: true },
        { field: "current_amount", title: "总金额", sortable: true },
        { field: "current_profit", title: "累计收益", sortable: true },
        { field: "lastday_profit", title: "交易日收益", sortable: true },
        //不重要
        { field: "cost", title: "当前成本", sortable: true },
        { field: "last_time", title: "上一交易日", sortable: true },
        { field: "price_time", title: "最新交易日", sortable: true },
        {
            field: "operate",
            title: "操作",
            sortable: false,
            events: {
                'click #sale_button': function (e, value, row, index) {
                    var arr1 = [];
                    arr1.push(row.fund_code);
                    $("#myModal").modal({
                        // remote: "test/test.jsp";//可以填写一个url，会调用jquery load方法加载数据
                        backdrop: "static", //指定一个静态背景，当用户点击背景处，modal界面不会消失
                        keyboard: true //当按下esc键时，modal框消失
                    });

                    $("#confirm_button").unbind('click').click(function () {
                        var sale_num = parseFloat($("#saleNum").val());
                        if (sale_num > row.hold_num) {
                            // alert("卖出量比持有量多，请检查参数");
                            $("#TipsText").text("卖出量比持有量多，请检查参数");
                            $('#myModal').modal('hide');
                            $('#showTipsModal').modal('show');
                            return false;
                        }
                        var paras_set = { "fund_code": row.fund_code, "sale_flag": "1", "sale_num": sale_num };
                        if (trace_to_server(paras_set)) {
                            $('#myModal').modal('hide');
                            // init_fund_table();
                            hold_fund_info_ls = get_hold_fund();
                            $('#fund-table').bootstrapTable("removeAll");
                            $('#fund-table').bootstrapTable("load", hold_fund_info_ls);
                            $("#TipsText").text("已申请卖出");
                            $('#showTipsModal').modal('show');
                            // alert("成功申请卖出");
                        }
                        else {
                            $('#myModal').modal('hide');
                            $("#TipsText").text("申请卖出失败，请检查参数");
                            $('#showTipsModal').modal('show');
                            // alert("申请卖出失败，请检查参数");
                            return false;
                        }
                    });

                    $("#myModal").on("loaded.bs.modal", function () {
                        //在模态框加载的同时做一些动作
                        return;

                    });
                    $("#myModal").on("show.bs.modal", function () {

                        //在show方法后调用
                        return;

                    });
                    $("#myModal").on("shown.bs.modal", function () {

                        //在模态框完全展示出来做一些动作
                        $("#staticFundName").val(row.fund_name);
                        $("#staticFundCode").val(row.fund_code);
                        $("#staticHoldNum").val(row.hold_num);
                        $("#saleNum").val(row.hold_num);

                    });
                    $("#myModal").on("hide.bs.modal", function () {
                        //hide方法后调用
                    });
                }
            },
            formatter: function (value, row, index) {
                var result = "";
                result += '<button id="sale_button" class="btn btn-info" data-toggle="modal" data-target="#editModal">卖出</button>';
                // result += '<button id="delete" class="btn btn-danger" style="margin-left:10px;">取消关注</button>';
                return result;
            }
        }
    ];

    $('#fund-table').bootstrapTable(
        {
            columns: tableColums,
            data: hold_fund_info_ls,
            // fixedColumns: true,  //固定列
            // fixedNumber: 1, //固定列数
            // uniqueId: "accountId",
            // idField: "fund_code",
            pageSize: 10,
            pageNumber: 1,
            fixedColumns: true,
            fixedNumber: 1, //固定列数
            search: true,
            searchOnEnterKey: true,
        }
    );

}

function init_search_table() {

    $('#search-table').bootstrapTable("destroy");
    var search_fund_ls = $("#search-fund-text").val().split(",");
    var fund_ls_info = get_fund_info(search_fund_ls);
    var tableColums = [
        { field: "fund_name", title: "基金名", sortable: true },
        { field: "fund_code", title: "基金代号", sortable: true },
        { field: "current_price", title: "最新净值", sortable: true },
        { field: "syl_1m", title: "1月收益率(%)", sortable: true },
        { field: "syl_3m", title: "3月收益率(%)", sortable: true },
        { field: "syl_6m", title: "6月收益率(%)", sortable: true },
        { field: "syl_1y", title: "1年收益率(%)", sortable: true },
        { field: "rate", title: "费率(%)", sortable: true }
    ];

    $('#search-table').bootstrapTable(
        {
            columns: tableColums,
            data: fund_ls_info,
            // fixedColumns: true,  //固定列
            // fixedNumber: 1, //固定列数
            // uniqueId: "accountId",
            // idField: "fund_code",
            pageSize: 10,
            pageNumber: 1,
            fixedColumns: true,
            fixedNumber: 1, //固定列数
            search: true,
            searchOnEnterKey: true,
        }
    );
    init_fund_charts(fund_ls_info);

}

// function init_record_table() {

//     // $('#record-table').bootstrapTable("destroy");

//     var tableColums = [
//         { field: "id", title: "记录号", sortable: true },
//         { field: "fund_name", title: "基金名", sortable: true },
//         { field: "fund_code", title: "基金代号", sortable: true },
//         { field: "buy_or_sale", title: "买卖", sortable: true },
//         { field: "buy_money", title: "购买金额", sortable: true },
//         { field: "sale_number", title: "出售份额", sortable: true },
//         { field: "application_time", title: "申请时间", sortable: true },
//         { field: "status", title: "当前状态（0未处理，1处理）", sortable: true },
//         { field: "trace_price", title: "交易净值", sortable: true },
//         { field: "price_time", title: "净值时间", sortable: true },
//         { field: "trace_num", title: "交易份额", sortable: true },
//         { field: "trace_total", title: "交易金额", sortable: true },
//         { field: "trace_time", title: "交易时间", sortable: true },
//     ];

//     $('#record-table').bootstrapTable(
//         {
//             columns: tableColums,
//             data: get_trace_record(),
//             // fixedColumns: true,  //固定列
//             // fixedNumber: 1, //固定列数
//             // uniqueId: "accountId",
//             // idField: "fund_code",
//             pagination: true,
//             pageSize: 10,
//             pageNumber: 1,
//             fixedColumns: true,
//             fixedNumber: 2, //固定列数
//             search: true,
//             searchOnEnterKey: true,
//         }
//     );
// }

/**
 * 画x-y图
 * @param {*} id html中的元素id
 * @param {*} data_ls 数组
 */
function draw_amlinechart(id, data_ls, table_title) {
    if ($('#' + id).length) {
        var title = table_title;
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
            "legend": {
                "useGraphSettings": true
            },
            "valueAxes": [
                {    
                    "id":"v1",
                    "title": "净值",
                    "axisColor": "#0000FF",
                    "axisAlpha": 0.2,
                    "dashLength": 1,
                    "position": "left"
                },
                {   
                    "id":"v2",
                    "title": "涨跌",
                    "axisColor": "#FFD700",
                    "axisAlpha": 0.2,
                    "dashLength": 1,
                    "position": "right"
                }
            ],
            "mouseWheelZoomEnabled": true,
            "graphs": [
                {   
                    "valueAxis": "v1",
                    "useNegativeColorIfDown": true,
                    "id": "g1",
                    "balloonText": "[[value]]",
                    "bullet": "round",
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "hideBulletsCount": 50,
                    "lineColor": "#0000FF",
                    "title": "单位净值",
                    "valueField": "visits1",
                    "useLineColorForBulletBorder": true,
                    "balloon": {
                        "drop": true
                    },
                },
                {   
                    "valueAxis": "v2",
                    "useNegativeColorIfDown": true,
                    "id": "g2",
                    "balloonText": "[[value]]",
                    "bullet": "square",
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "hideBulletsCount": 50,
                    "lineColor": "#FFD700",
                    "title": "涨跌百分比",
                    "valueField": "visits2",
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
                // "limitToGraph": "g1",
                "categoryBalloonDateFormat": "YYYY-MM-DD",
                "cursorPosition": "mouse"
            },
            "categoryField": "date",
            "categoryAxis": {
                "minPeriod": "DD",
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
 * 画x-y图
 * @param {*} id html中的元素id
 * @param {*} data_ls 数组
 */
 function draw_amlinechart2(id, data_ls, table_title) {
    if ($('#' + id).length) {
        var title = table_title;
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
            "legend": {
                "useGraphSettings": true
            },
            "valueAxes": [
                {    
                    "id":"v1",
                    "title": "同类基金排名",
                    "axisColor": "#0000FF",
                    "axisAlpha": 0.2,
                    "dashLength": 1,
                    "position": "left"
                },
                {   
                    "id":"v2",
                    "title": "同类基金百分比",
                    "axisColor": "#FFD700",
                    "axisAlpha": 0.2,
                    "dashLength": 1,
                    "position": "right"
                },
                {   
                    "id":"v3",
                    "title": "同类基金总数",
                    "axisColor": "#FFD700",
                    "axisAlpha": 0.2,
                    "dashLength": 1,
                    "position": "left"
                }
            ],
            "mouseWheelZoomEnabled": true,
            "graphs": [
                {   
                    "valueAxis": "v1",
                    "useNegativeColorIfDown": true,
                    "id": "g1",
                    "balloonText": "[[value]]",
                    "bullet": "round",
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "hideBulletsCount": 50,
                    "lineColor": "#0000FF",
                    "title": "同类基金排名",
                    "valueField": "visits1",
                    "useLineColorForBulletBordtrueer": true,
                    "balloon": {
                        "drop": true
                    },
                },
                {   
                    "valueAxis": "v2",
                    "useNegativeColorIfDown": true,
                    "id": "g2",
                    "balloonText": "[[value]]",
                    "bullet": "square",
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "hideBulletsCount": 50,
                    "lineColor": "#FFD700",
                    "title": "同类基金排名百分比",
                    "valueField": "visits2",
                    "useLineColorForBulletBorder": true,
                    "balloon": {
                        "drop": true
                    }
                },
                {   
                    "valueAxis": "v3",
                    "useNegativeColorIfDown": true,
                    "id": "g3",
                    "balloonText": "[[value]]",
                    "bullet": "round",
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "hideBulletsCount": 50,
                    "lineColor": "#FFFFFF",
                    "title": "同类基金总数",
                    "valueField": "visits3",
                    "useLineColorForBulletBorder": true,
                    "balloon": {
                        "drop": true
                    },
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
                // "limitToGraph": "g1",
                "categoryBalloonDateFormat": "YYYY-MM-DD",
                "cursorPosition": "mouse"
            },
            "categoryField": "date",
            "categoryAxis": {
                "minPeriod": "DD",
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


function init_fund_charts(set_data_arr) {
    
    for(var i=1;i<11;i++){
        $('#card-id'+i).remove();
    }
    $.each(set_data_arr, function (index, set_data) {

        var fund_code = set_data.fund_code;
        var fund_name = set_data.fund_name;
        var net_worth_id = "amlinechart" + (index + 1);
        var rank_id = "amlinechart2-" + (index + 1);
        var card_id = "card-id"+(index+1);
        var net_worth_title = "净值：" + fund_name + "-" + fund_code;
        var rank_title = "同类排名：" + fund_name + "-" + fund_code;
        var html_template = '<div class="card" id="'+card_id+'"><div class="card-body"><div id="' + net_worth_id + '"></div><div id="'+rank_id +'"></div></div></div>';
        // $('#'+card_id).remove();
        $('#amcharts').append(html_template);
        var net_worth_trend = [];
        $.each(set_data.net_worth_trend, function (index, set1) {
            net_worth_trend.push({ date: getTime(set1.x), visits1: set1.y, visits2: set1.equityReturn })
        });
        var rank_trend = [];
        $.each(set_data.rate_in_similar_type, function (index, set1) {
            var sc= parseFloat(set1.sc);
            var present = (sc-set1.y)/sc;
            rank_trend.push({ date: getTime(set1.x), visits1: set1.y, visits2:present})
        });

        draw_amlinechart(net_worth_id, net_worth_trend, net_worth_title);
        // draw_amlinechart2(rank_id, rank_trend, rank_title);
        // var detail_info_id="detail-info"+(index+1);
        // var label = set_data
        // var html= '<div class="mb-3 row"><label for="'+ detail_info_id +'" class="col-sm-3 col-form-label"><i class="ti-email"></i>'+ label+'</label><div class="col-sm-9"><input type="text" readonly class="form-control-plaintext" id="'+detail_info_id +'" value=""></div></div>'


    });

}


$(document).ready(function () {
    show_user_info();
    logoutButton = $("#dd-logout");
    logoutButton.click(function () {
        logout();
    });

    init_fund_table();

    $("#search-button").click(function () {
        init_search_table();
    });


});