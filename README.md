# 前言
基于Odoo实现的Addons，聚合了微信登录、微信支付、二维码生成等

__注：此项目属企业开发前的练习项目，本网站属于微信H5页面__
# 技术栈  
Odoo12 + Qweb + JS/CSS/HTML
# 项目环境
阿里云ECS Ubuntu18.04 + nginx + python3.6.8 + pip3 
> 本项目使用服务器系统root用户模式
# 关于教程

此项目的详细教程请参见[Odoo12开发手册](https://alanhou.org/odoo-12-development/)。

当然也可以阅读官方教程 [Odoo documentation](https://www.odoo.com/documentation/12.0/)。

最推荐的方式：查阅odoo内核源码，查看相关模块或方法的应用实例。

# 说明

>  如果对您有帮助，您可以点右上角 "Star" 支持一下 谢谢！ ^_^

>  或者您可以 "follow" 一下，我会不断开源更多的有趣的项目

>  开发环境 Ubuntu 18.04 + PyCharm + 微信web开发者工具

>  如有问题请直接在 Issues 中提，或者您发现问题并有非常好的解决方案，欢迎 PR 👍


# 效果演示

[查看demo请戳这里](http://odoo.wanbowen.com)（请用chrome预览）

# 目标功能
- [x] 微信网页授权 -- 完成
- [x] 微信支付 -- 完成
- [x] 页面二维码分享 -- 完成
- [x] 活动过期自动关闭购买渠道 -- 完成

# 总结

1. 项目目标实现微信支付，作为平台接入商家销售各类优惠券

2. 商家在平台上出售定量优惠券

3. 用户购买优惠券后可进入卡包查看所购优惠券

4. 本项目包括前后台近10个页面

# 最终目标

用Odoo 12 实现商城 + 微信支付 + 官网宣传网站
# 项目下载
进入你的odoo项目目录，在与odoo内核同级目录下：
```
git clone https://gitee.com/wanbowen2019/odoo-addons.git
```
添加该目录至 addons 路径：
```buildoutcfg
./odoo/odoo-bin -d testdb --addons-path="odoo-addons,odoo/addons" --save
```
> –save 参数将选项保存至配置文件中，这样我们就无需在每次启动服务时输入参数，只需运行./odoo-bin 即可使用上次使用的参数。

装载运行该模块：
```
ctrl + c
./odoo/odoo-bin -i juan_tong
```
> -i 表示装载模块


# #其他相关内容#
# Odoo配置
> 详细odoo学习及配置教程[odoo12开发手册](https://alanhou.org/odoo-12-development/)

## 安装 PostgreSQL 数据库
Odoo 要使用到 PostgreSQL服务，典型的开发设置是使用安装 Odoo 的同一台机器安装PostgreSQL。下面我们就来安装数据库服务：
```
sudo apt update
sudo apt install postgresql -y # 安装PostgreSQL
sudo su -c "createuser -s $USER" postgres # 创建数据库超级用户
```
手动启动PostgreSQL服务执行：`sudo service postgresql start`

## 安装 npm 包用于后续前端接入微信支付
```
sudo apt install npm # 安装Node.js和包管理器
```
下一步需要将配置文件放到系统的配置文件目录/etc 下，命令如下：
```
sudo mkdir /etc/odoo
sudo cp /home/odoo/.odoorc /etc/odoo/odoo.conf
sudo chown -R odoo /etc/odoo
sudo chmod u=r,g=rw,o=r /etc/odoo/odoo.conf # 安全加固使用
```
为 Odoo 服务创建一个存储日志文件的目录，放在/var/log目录下，命令如下：
```
sudo mkdir /var/log/odoo
sudo chown odoo /var/log/odoo
```
执行下面操作运行服务器配置：
```
~/odoo-dev/odoo/odoo-bin -c /etc/odoo/odoo.conf
```
## 为Odoo设置进程守护（系统服务）
要在系统中添加服务，只需创建一个描述服务的文件。我们创建`/lib/systemd/system/odoo.service`
文件：
```
vim /lib/systemd/system/odoo.service
```
并加入如下内容：
```
Description=Odoo
After=postgresql.service
 
[Service]
Type=simple
User=root
Group=root
ExecStart=/root/odoo-dev/odoo/odoo-bin -c /etc/odoo/odoo.conf
 
[Install]
WantedBy=multi-user.target
```

下一步我们需要使用如下命令来注册这个新服务：
```
sudo systemctl enable odoo.service
```
使用如下命令启动该服务：
```
sudo systemctl start odoo # 关闭stop
```
使用如下命令检查该服务状态：
```
sudo systemctl status odoo
```
得到如下：
```
Active: active(running)
```
状态正常！
> 若发生异常请查阅[odoo开发手册](https://alanhou.org/odoo12-deployment/)中——设置Odoo为系统服务

接下来进入到nginx的配置

# nginx配置
> 使用nginx来为不同的服务所对应的不同的端口来提供反向代理，因只有一台服务器就没有配置负载均衡
首先安装nginx：
```
sudo apt-get install nginx -y
sudo service nginx start # 如尚未启动，启动Nginx服务
```
Nginx配置文件和Apache的方式基本相同，存储在/etc/nginx/available-sites/中，并可通过在/etc/nginx/enabled-sites/中添加软链接来激活。注意应同时关闭Nginx安装时默认带有的配置：
```
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/odoo
sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/odoo
```
使用nano或vi等编辑器来编辑 Nginx配置文件：
```
vim /etc/nginx/sites-available/odoo
```
配置内容如下：
```
upstream odoo {
    server 120.79.147.13:8069; # 反向代理端口
}
upstream odoochat {
    server 120.79.147.13:8072;
}
server {
     listen 80;
     server_name odoo.wanbowen.com www.ai-solution.cn;# 更改为自己的域名
     # Add Headers for odoo proxy mode
     proxy_set_header X-Forwarded-Host $host;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
     proxy_set_header X-Real-IP $remote_addr;

     # log
     access_log /var/log/nginx/odoo.access.log;
     error_log /var/log/nginx/odoo.error.log;
     # Redirect longpoll requests to odoo longpolling port
     location /longpolling {
        proxy_set_header Host $host;
        proxy_pass http://odoochat;
     }
     # 通配符匹配
     location / {
         proxy_redirect off;
         proxy_set_header Host $host;
         proxy_pass http://odoo;
     }
     # common gzip
    gzip_types text/css text/scss text/plain text/xml application/xml application/json application/javascript;
    gzip on;
}
```
> 对nginx配置文件中location部分有不理解的请查阅 [nginx的location配置详解](https://segmentfault.com/a/1190000013267839)
在配置文件的最后，可以看到两条gzip相关的命令，它们用于对一些文件进行压缩，提升性能。可通过如下命令测试配置是否正确：
```
nginx -t
```
返回如下内容：
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
接下来重启nginx服务：
```
sudo /etc/init.d/nginx reload
```
or
```
sudo systemctl reload nginx
```
通过如下命令可确认 Nginx 是否将访问流量重定向到了后台Odoo服务中：
```
curl http://localhost
```
返回如下：
```
<html><head><script>window.location = '/web' + location.hash;</script></head></html>
```
运行到这一步nginx的配置也完成了，接下来开始项目的运行

# 项目运行

首先关闭之前开启的服务：
> 这里统一使用service来管理服务（与systemctl效果一致，只是指令不同）
```
service odoo stop
service wxpay stop
```
更新odoo模块：
```
~/odoo-12/odoo-bin -c /etc/odoo/odoo.conf -u base --stop-after-init
```
现在所有的端口及服务都已开启，接下来进入浏览器进行测试。

输入：
```
http://120.79.147.13:8069 # 返回odoo官方登录页 则odoo正常开启
```
输入：
```
http://www.ai-solution.cn # 返回odoo官方登录页 则正常
```
#### NOTE
其他内容请跟随 Odoo开发手册 进一步学习！
