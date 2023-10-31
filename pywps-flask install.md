##### pywps-flask安装文档

----

[pywps-flask-fork](https://github.com/zhangyongjian258/pywps-flask)

> 前置条件

需要安装QGIS

- 在pycharm中设置QGIS python设置为pywps-flask解释器

目录为QGIS安装目录下：`QGIS 3.32.1\bin\python-qgis.bat`

我这里目录为`C:\Program Files\QGIS 3.32.1\bin\python-qgis.bat`

![image-20231031191253528](E:%5Cprojects%5Cpc-projects%5Cpywps-flask%5CREADME.assets%5Cimage-20231031191253528.png)

> 注意

```
在pycharm中设置QGIS python-qgis为解释器时无法通过pycharm终端安装依赖
```

- 邮件以管理员权限打开`OSGeo4W Shell`

![image-20231031191557825](E:%5Cprojects%5Cpc-projects%5Cpywps-flask%5CREADME.assets%5Cimage-20231031191557825.png)

执行以下命令：

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install pywps -i https://pypi.tuna.tsinghua.edu.cn/simple

