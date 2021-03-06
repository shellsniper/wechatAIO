
![wechatAIO](/template/logo.png "wechatAIO")

---
## Warning:
### Now is Alpha version, there are still lots of bugs, especially in the Windows OS, and more features will be come out soon. I will make an announcement when everything seems okay to release.
---

## 2019-4-13 update:
      v1.3 Update:
                1. Added auto_reply feature
                2. Added chat log feature
                3. Improve UI designs
                4. Improve overall performance by adjusting subprocesses
                5. fix bugs
                6. Added delete and reset feature in main_CLI
## <del> 2019-4-12 update: 第一阶段框架将继续测试，接下来会慢慢完善保持连接的功能，比如在命令行与别人聊天
## <del> 2019-4-11 update: macos测试通过，windows上一些python lib需要手动安装出现的问题见FAQ，linux上字体需要自己设置，不然中文会出现乱码
## <del> 2019-4-10 update:正在修复不同系统上terminal的问题

---
Wechat All in One(wechatAIO) 使用Python 3.x 开发，提供可扩展的命令行交互界面，调用itchat API，提供一个扩展微信功能的框架，方便大家实践和扩展
<br/>
欢迎大家issue问题，求star，求follow！

---
![Alt Text](/template/interface.gif "main_cli")

目前支持的功能有:
  
  * **框架类**
   
    - [x] 友好的命令行交互式界面
    - [x] 模块化设计，支持自定义扩展，易于加入新功能的代码框架
    - [x] 方便打包封装和发布
    - [x] 非阻塞，多进程设计
    - [x] 在命令行界面按tab自动补全命令
    - [x] 每个function提供可自定义的helper提示
    - [x] 自定义banner
    - [ ] Django Web API
    
  * **统计图类**
  
    - [x] 微信好友的性别比例和人数统计图
    ![Alt Text](/template/gender.gif "gender_distribution")
    - [x] 基于好友个性签名制成的云图
    ![Alt Text](/template/wordcloud.gif "wc")
    ![Alt Text](/template/wordcloud_cn.gif "main_cli")
      * 支持图片蒙版
      * 支持英文过滤
      * 关键词模式
          
    - [x] 微信好友的国内外地域分布统计图
    ![Alt Text](/template/geo.gif "geo_distribution")
    - [ ] 生成好友头像的拼接
    - [ ] 根据聊天内容做词云

  
  * **监听信息类**
  
    ![ALt Text](/template/login_keep.gif "login_keep")
    
    - [x] 监听好友信息，包括文字，语音，视频，图片，分享链接，名片和地图
    - [x] 监听群消息，包括文字，语音，视频，图片，分享链接
    - [x] 监听撤回信息，并发送至 文件管理器 和保存下来
    - [x] 信息自动下载保存在好友和群信息文件夹内
    - [x] 多线程保持连接登录状态
    - [ ] 关键词监听
    - [ ] 媒体文件去重，设置规则管理日志和媒体文件，定时清理缓存
  
  * **信息功能扩展类**
    - [x] 一键群发消息
    - [x] 提供给指定好友或者群发信息的接口，

---
安装：
---
1. 下载源代码<br/>
   `git clone https://github.com/levoncf/wechatAIO.git`
   <br/><br/>
2. 在project目录下安装所需libs，注意请使用python 3.x版本执行<br/>
   `sudo pip3 install -r requirements.txt`
   <br/><br/>
   
3. 执行， main_CLI.py是命令行界面的主程序<br/>
   `python3 main_CLI.py`
---
使用：
---
  1. 执行 `python3 main_CLI.py`后 进入主界面，按？可以查看支持的功能<br/>
      1. 按 ？<command> 可以查看功能的详细使用情况， 比如 ?geo
      2. 输入`clear`可以清除输出
      3. 输入`tab`键可以自动补全命令
   <br/>
  2. 如果只是想生成统计类的图表，只需输入 `user_meta`, 获取到用户信息后就自动登出，不会占用微信web API的连接 <br/> <br/>
  
  3. 如果想执行监听类命令，请使用`login_keep`，这将会产生独立的一个保持连接的进程，与主交互界面不会阻塞 <br/> <br/>
  4.  待续 <br/>
---

FAQ
---
Q: 出现 Command "python setup.py egg_info" failed with error code 1 in C:\Users\CTA\AppData\Local\Temp\pip-install-sxo0fmjy\matplotlib\的问题<br/><br/>

A: 解决办法参照 https://github.com/googleapis/google-cloud-python/issues/3884
   <br/><br/>
   如果是Windows系统需要有VC++ 2017 的build tools
  
Q: Windows OS pip install wordcloud ERROR
A: <br/><br/>
  Download wordcloud‑1.3.2‑cp36‑cp36m‑win_amd64.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud<br/>

  <br/> Copy the file to your current working directory

  <br/> Open command prompt from Tools

  <br/> Python -m pip install wordcloud-1.5.0-cp37-cp37m-win32.whl
Reference：
---

https://github.com/xiaoxiaoyao/MyApp/blob/24a359c62f01777aeb36b89d8fe683cffe2c652c/jupyter_notebook/WeChat_image.ipynb
https://www.jianshu.com/p/8f432c31dec7
