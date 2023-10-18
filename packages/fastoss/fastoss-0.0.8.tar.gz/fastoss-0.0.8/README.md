# fastoss

#### 介绍
快速使用阿里云的oss产品

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip install fastoss
```
2.  pip安装（使用阿里云镜像加速）
```shell script
pip install fastoss -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1.  demo
```python
import fastoss
query_res = fastoss.upload_file(file_dir='test.txt', key='test.txt')
```