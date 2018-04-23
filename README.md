源项目：https://github.com/antojoseph/diff-gui

**搜索frida时发现的项目，frida的webgui形式。**

简单二次开发了下，升级内容：

* 优化了页面布局，去掉diff-droid标志（增大ace区域为了自用）
* 从py2改为支持py3，修改部分bug
* js模板中统一将Dalvik替换为JAVA，frida高版本已经不支持Dalvik
* 添加重启进程功能应对程序ANR及多重hook
* 修改hook按钮server端处理逻辑，修复多次hook会被首次hook功能覆盖的问题

#### 启动

这里用docker封装免安装frida、redis环境一键配置

运行server：

```
docker-compose up -d
```

手机端开启远程adb：

```
setprop service.adb.tcp.port 5555
stop adbd
start adbd
```
尝试使用 adb connect ip:5555 查看是否连接成功。

运行frida-server：

```
./fs77 -l mobileIP
```

浏览器访问 http://0.0.0.0:5000

#### 使用

1. 启动需要被注入的app
2. web界面输入手机ip
3. 选择需要注入的进程
4. 选择模板进行编辑
5. 编写完js点击hook按钮实现frida动态hook，右边会打印hook返回结果。