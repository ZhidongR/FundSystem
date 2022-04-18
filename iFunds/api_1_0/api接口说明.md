所有接口都是基于 http://127.0.0.1:5000这一个uri。

用户相关接口： /user
---------

A.获取单个用户信息

1. 方法：GET
2. 输入参数：
    1. phone:用户登录的手机号
    2. token:当前用户的登录token
3. 返回参数：
    1. phone:用户手机号
    2. name:用户名
    3. balance：用户的账号余额
    4. last_day_profit：上一交易日的收益
    5. hold_funds_amount:持有基金的总金额
    6. hold_profit:持有收益
    7. all_profit:累计收益
4. 案例
    1. GET方式，./user?phone=15521123650&token=xxxxxxxxxxxxxxxx
    2. 返回数据：{"re_code":"0","msg":"获取用户信息成功", "data":{"phone":"15521123650"}}********_
       ``
       B.更新当前登录用户的信息
1. 方法： POST
2. 输入体Body参数：
    1. phone:用户登录的手机号
    2. token:当前用户的登录token
    3. 可选需要修改的数据，json格式