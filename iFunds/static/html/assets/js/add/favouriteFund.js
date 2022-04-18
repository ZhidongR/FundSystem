
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
    url = "api/1.0/funds";

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
                'click #delete': function (e, value, row, index) {
                    var arr1 = [];
                    arr1.push(row.fund_code);
                    var bool_delete = delete_favourite_fund(arr1);
                    if (bool_delete) {
                        $('#fund-table').bootstrapTable('remove', { field: "fund_code", values: arr1 });
                    }
                }
            },
            formatter: function (value, row, index) {
                var result = "";
                // result += '<button id="edit" class="btn btn-info" data-toggle="modal" data-target="#editModal">编辑</button>';
                result += '<button id="delete" class="btn btn-danger" style="margin-left:10px;">取消关注</button>';
                return result;
            }
        }
    ];

    $('#fund-table').bootstrapTable(
        {
            method: 'post', // 请求方式
            contentType: 'application/json',
            url: 'api/1.0/funds', //请求地址 
            queryParams: function () {
                var user_favourite_fund_set = get_favourite_fund();
                var fund_code_ls = [];
                $.each(user_favourite_fund_set, function (key, value) {
                    fund_code_ls.push(key);
                });
                var params = {
                    "fund_code_ls": fund_code_ls
                };
                return params;
            },
            dataType: 'json', //服务端返回的数据类型
            // headers: { 'X-CSRFToken': getCookie('csrf_token') },
            responseHandler: function (res) {
                if (res.code == '0') {
                    // 返回成功并正常
                    return res.data;
                }
                else {
                    console.log(res.code);
                    console.log(res.msg);
                    return false;
                }
            },
            columns: tableColums,
            // data: table_data,
            // uniqueId: "accountId",
            idField: "fund_code",
            pageSize: 10,
            pageNumber: 1,
            fixedColumns: true,
            fixedNumber: 1
        }
    );
}

function init_search_table(fund_code_ls) {
   

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
                'click #add-favourite': function (e, value, row, index) {
                    var arr1 = [];
                    arr1.push(row.fund_code);
                    if (add_favourite_fund(arr1)) {
                        //按钮变
                        $("#add-favourite").text("已添加喜爱");
                        $("#fund-table").bootstrapTable("append", row);
                    };
                }
            },
            formatter: function (value, row, index) {
                var result = "";
                result += '<button id="add-favourite" class="btn btn-info" data-toggle="modal" data-target="#editModal">添加关注</button>';
                // result += '<button id="delete" class="btn btn-danger" style="margin-left:10px;">添加关注</button>';
                return result;
            }
        }
    ];

    var params = {
        "fund_code_ls": search_fund_ls
    };
    $('#search-table').bootstrapTable(
        {
            method: 'post', // 请求方式
            contentType: 'application/json',
            url: 'api/1.0/funds', //请求地址 
            queryParams: params,
            dataType: 'json', //服务端返回的数据类型
            responseHandler: function (res) {
                if (res.code == '0') {
                    // 返回成功并正常
                    return res.data;
                }
                else {
                    console.log(res.code);
                    console.log(res.msg);
                    return false;
                }
            },
            columns: tableColums,
            // data: table_data,
            // uniqueId: "accountId",
            idField: "fund_code",
            papeSize: 10,
            papeNumber: 1,
        }
    );
}


$(document).ready(function () {
    show_user_info();
    logoutButton = $("#dd-logout");
    logoutButton.click(function () {
        logout();
    });
    var fund_code_ls = ["004855", "001767", "165525", "001766", "005224", "001595"];
    // add_favourite_fund(fund_code_ls);
    init_fund_table(fund_code_ls);

    $("#search-button").click(function () {
        var arr_fund_code = $("#search-fund-text").val().split(",");
        init_search_table(arr_fund_code);
    });
});