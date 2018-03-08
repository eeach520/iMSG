# iMSG平台使用说明





### 1、下载iMSG包或代码，网址：（http://github.com/eeach520/iMSG）





## 2、打开配置文件进行更改（app/api/config.py）

​	这里配置的是一些平台的参数，如果要使用本平台，必须将发送邮件的邮箱、服务器、短信服务的openid、secret、模板以及微信号的openid、secret进行更改。

- 1、邮箱参数的更改（代码23行，class  SMTP）
  - SERVER：邮箱的服务器
  - PORT：登陆邮箱的端口
  - USERNAME：邮箱账户的"@"前半部分
  - PASSWORD：邮箱授权登陆码（注意：不是邮箱的密码）
  - ADDRESS：邮箱账户的“@”后半部分
- 2、短信参数的更改（代码31行，class  SMS）
  - PARAMETERS：post阿里云短信接口的参数
    - 'Format'：请求数据格式，不用改
    - ‘Version’：目前最新就是‘2017-05-25’，以后有可能需要进行更改
    - ‘AccessKeyId'’：阿里云短信服务的id
    - 其余一般不做更改
  - USER_PARAMS
    - ‘Action’：发送短信的方式，不用作更改
    - ‘SignName’：短信签名，开通短信服务的时候进行申请
    - ‘TemplateCode’：发送短信的模板，开通短信服务时进行申请
  - TEMPLATE_PARAM
    - 模板具体的形式。我这里直接是写死了，只接受一个参数
  - KEY-ID：短信服务appid
  - KEY_SECRET：短信服务的secret
  - SERVER：阿里云服务器地址
- 3、微信参数的更改
  - APPID：微信公众号APPID
  - APPSECRET：微信公众号的secret
  - 其余是微信接口地址，不做更改



## 3、环境准备

- 安装python3.6（代码中引用了少数几个python3.6才有的库，尽量使用python3.6）



- 安装根目录下requirement.txt文件所提及的库



- 可用``pip3 install -r requirements.txt``进行安装





## 4、配置服务器



- flask框架可以直接运行manage.py，从而进行使用



- 也可根据个人情况进行配置





## 5、消息管理



- 后台网页实现

  ​