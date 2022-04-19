
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
    url = "api/1.0/funds/hold";
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
        { field: "rate", title: "费率(%)", sortable: true },
        {
            field: "operate",
            title: "操作",
            sortable: false,
            events: {
                'click #buyButton': function (e, value, row, index) {
                    
                    $("#BuyModal").modal({
                        // remote: "test/test.jsp";//可以填写一个url，会调用jquery load方法加载数据
                        backdrop: "static", //指定一个静态背景，当用户点击背景处，modal界面不会消失
                        keyboard: true //当按下esc键时，modal框消失
                    });

                    $("#confirmBuyButton").unbind('click').click(function () {
                        $('#BuyModal').modal('hide');
                        var buy_money = parseFloat($("#buyMoney").val());
                        var paras_set = { "fund_code": row.fund_code, "buy_flag": "1", "buy_money": buy_money };
                        if (trace_to_server(paras_set)) {
                            $("#TipsText").text("已申请买入");
                            $('#showTipsModal').modal('show');
                            init_record_table();
                            // return false;
                        }
                        else {
                            $("#TipsText").text("申请买入失败，请检查参数");
                            $('#showTipsModal').modal('show');
                            // alert("申请卖出失败，请检查参数");
                            // return false;
                        }
                    });

                    $("#BuyModal").on("loaded.bs.modal", function () {
                        //在模态框加载的同时做一些动作
                        return;

                    });
                    $("#BuyModal").on("show.bs.modal", function () {

                        //在show方法后调用
                        return;

                    });
                    $("#BuyModal").on("shown.bs.modal", function () {

                        //在模态框完全展示出来做一些动作
                        $("#BuyFundName").val(row.fund_name);
                        $("#BuyFundCode").val(row.fund_code);
                        $("#buyMoney").val(5000);
                    });
                    $("#BuyModal").on("hide.bs.modal", function () {
                        //hide方法后调用
                    });
                }
            },
            formatter: function (value, row, index) {
                var result = "";
                result += '<button id="buyButton" class="btn btn-info" data-toggle="modal" data-target="#editModal">购买</button>';
                // result += '<button id="delete" class="btn btn-danger" style="margin-left:10px;">取消关注</button>';
                return result;
            }
        }
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
}

function init_record_table() {

    $('#record-table').bootstrapTable("destroy");
    // $('#record-table').bootstrapTable("refresh");
    var tableColums = [
        { field: "id", title: "记录号", sortable: true },
        { field: "fund_name", title: "基金名", sortable: true },
        { field: "fund_code", title: "基金代号", sortable: true },
        { field: "buy_or_sale", title: "买卖", sortable: true },
        { field: "buy_money", title: "购买金额", sortable: true },
        { field: "sale_number", title: "出售份额", sortable: true },
        { field: "application_time", title: "申请时间", sortable: true },
        { field: "status", title: "当前状态（0未处理，1处理）", sortable: true },
        { field: "trace_price", title: "交易净值", sortable: true },
        { field: "price_time", title: "净值时间", sortable: true },
        { field: "trace_num", title: "交易份额", sortable: true },
        { field: "trace_total", title: "交易金额", sortable: true },
        { field: "trace_time", title: "交易时间", sortable: true },
    ];

    $('#record-table').bootstrapTable(
        {
            columns: tableColums,
            data: get_trace_record(),
            // fixedColumns: true,  //固定列
            // fixedNumber: 1, //固定列数
            // uniqueId: "accountId",
            // idField: "fund_code",
            pagination:true,
            pageSize: 10,
            pageNumber: 1,
            fixedColumns: true,
            fixedNumber: 2, //固定列数
            search: true,
            searchOnEnterKey: true,
        }
    );

    
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
    init_record_table();


});