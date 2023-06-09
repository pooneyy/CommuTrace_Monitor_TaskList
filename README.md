# CommuTrace_Monitor_TaskList
监听CommuTrace共迹算力平台任务列表

使用GPL 3.0协议

### 对于不便的用户

现有一个已部署的demo，使用微信扫码，也可接收消息推送：

<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQGt7zwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAybWtkbUVkMDVjWEQxako3dWhBY3QAAgTtejZkAwQAjScA" alt="showqrcode"  />

这个二维码**有效期至2023年05月11日**

### 使用说明

```bash
python index.py
```

或下载运行[index.exe](https://github.com/pooneyy/CommuTrace_Monitor_TaskList/releases/latest)

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
0.2.1 (2023.03.31) 修复：某些情况下“远程主机强迫关闭了一个现有的连接”时，报错退出的问题。

0.2   (2023.03.25) 更新：
                   1、登录时将Cookies保存到文件，并优先从文件载入Cookies；
                   2、新增检查更新。
                   修复：
                   1、修复了某些情况下订单解析失败的问题；
                   2、修复了Cookies失效后，重新登录失败的问题。

0.1.4 (2023.03.22) 修复：
                   1、当订单数=0时，重复登录的问题；
                   2、调整了输出的消息的格式，并做了精简，避免过多无意义内容。

0.1.3 (2023.03.20) 修复：当订单数>1时，只显示首个订单的问题。

0.1.2 (2023.03.19) 修复：
                   1、当无订单时崩溃的问题；
                   2、当订单数>1时，订单创建时间解析错误的问题；
                   3、修复其它错误。

0.1.1 (2023.03.16) 若干更新：
                   1、令当连接出错时自动重试；
                   2、令当验证码识别出错时自动重试；
                   3、处理其他报错。

0.1   (2023.03.16) 初版。
```

