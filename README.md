# xxqg_2020
学习强国自动学习

使用说明：
1、添加用户名和密码
(1)如果你有多个账户需要学习, 那么请将这些信息依次填入,其中name可以随便填, username和passwd对应的用户名和密码需有效
{
        "userlist":[
                {
                        "name":"xxx",
                        "username": "13xxxxxxxx7",
                        "passwd": "xxxxxxxx"
                },
                {
                        "name":"yyy",
                        "username": "13yyyyyyyy7",
                        "passwd": "yyyyyyyy"
                }
        ]
}

(2)如果你只有一个账户需要学习, 那么是如下格式. 注意逗号.
{
        "userlist":[
                {
                        "name":"yyy",
                        "username": "13yyyyyyyy7",
                        "passwd": "yyyyyyyy"
                }
        ]
}

2、执行命令 : python3 uiauto.py auto
   命令执行完后,就可以自动学习了.

3、注意, 手机首次使用某个账号时,登录需要短信验证码,这时需手动填入.
4、步骤2的命令执行一次,学习一遍. 如果你想每天挂着学习,请将uiauto.py中的schedule_task=0行改成schedule_task=1. excute_every_time="01:01"这句表示每天凌晨1点1分开始学习,这个时间你可以更改

