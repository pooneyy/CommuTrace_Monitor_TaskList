# CommuTrace_Monitor_TaskList
监听CommuTrace共迹算力平台任务列表

使用GPL 3.0协议

### 对于不便的用户

现有一个已部署的demo，使用微信扫码，也可接收消息推送：

<img src="https://s2.loli.net/2023/03/16/ebVOMoZwFRliA3q.jpg" alt="showqrcode" style="zoom: 33%;" />

这个二维码**有效期至2023年4月15日**

### 使用说明

```bash
python index.py
```

或下载运行[index.exe](https://github.com/pooneyy/CommuTrace_Monitor_TaskList/releases/)

![image-20230316165557606](https://s2.loli.net/2023/03/16/tscoEFUr5X6SG2i.png)

##### 首次运行时你需要准备：

1. 平台账号、密码 [注册帐号](http://39.101.72.182/index.php/Home/Login/reg.html)

2. [TrueCaptcha](https://truecaptcha.org/profile.html)的`userid`和`apikey`用于验证码识别。

   ![](https://s2.loli.net/2023/03/16/lO5sJq4NjHTrzvP.png)

3. [PushPlus](http://www.pushplus.plus/)的`token`用于消息推送

   ![image-20230316161929749](https://s2.loli.net/2023/03/16/m28Pc7BJQinXMZh.png)
   - （选填）群组编码：用于PushPlus发送一对多消息（群发消息）。详见[一对多消息|pushplus(推送加)](http://www.pushplus.plus/push2.html)，留空时发送一对一消息。

### 更新日志

```
0.1.2 (2023.03.19) 修复：
                   1、当无订单时崩溃的问题；
                   2、当订单数>1时，订单创建时间解析错误的问题；
                   3、修复其它错误。

0.1.1 (2023.03.16) 若干更新：
                   1、令当连接出错时自动重试；
                   2、令当验证码识别出错时自动重试；
                   3、处理其他报错。

0.1   (2023.03.16) 初版
```

