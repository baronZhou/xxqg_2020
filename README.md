# 学习强国自动学习

## 使用说明:

$\color{rgb(255,0,0)}{本工具以学习为目的. 刷分可耻. 请适可而止}$


 `本工具以学习为目的. 刷分可耻. 请适可而止. `

 `请放心使用本工具, 任意两个步骤之间的延迟都是随机的, 可用做到防监测、防封号 `

### 1、添加用户名和密码

(1)如果你有多个账户需要学习, 那么请将这些信息依次填入,其中name可以随便填, username和passwd对应的用户名和密码需有效
```
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
```
(2)如果你只有一个账户需要学习, 那么是如下格式. 注意逗号.
```
{
        "userlist":[
                {
                        "name":"yyy",
                        "username": "13yyyyyyyy7",
                        "passwd": "yyyyyyyy"
                }
        ]
}
```

###  2、执行命令:

执行命令之前,确保手机adb可用
(1)、先执行:sudo python3 -m uiautomator2 init, 该命令会在手机上安装一个app 
(2)、再执行命令 : python3 uiauto.py auto, 开始自动学习

### 3、注意事项

手机首次使用某个账号时,登录需要短信验证码,这时需手动填入.

###  4、开启每天定时学习功能

步骤2的命令执行一次,学习一遍. 如果你想每天挂着学习,请将uiauto.py中的schedule_task=0行改成schedule_task=1. excute_every_time="01:01"这句表示每天凌晨1点1分开始学习,这个时间你可以更改

