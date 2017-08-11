# iMsg

## 概念

### 自营消息平台

iMsg是一个自营消息平台，对外提供`restful api`，用户使用自己的账号信息通过认证后，进行发送信息，可以发送`wechat`，`sms`，`email`三种方式的消息。

### restful api

微服务的典型接口方式。通过HTTP协议的`GET`,`POST`,`PUT`,`DELETE`等`METHOD`，实现对资源的访问和管理。传输的内容为`json`格式。

### token

令牌，访问资源时候的凭证。用户向接口发送自己的帐户/密码等信息，获取一个`token`，访问资源时携带该`token`作为凭证。`token`过期/失效后，需要重新获取新的`token`。设计良好的token可以增强安全性，防止接口滥用，方便帐户/权限的管控等。

### 消息发送方式

真正发送消息的功能，调用一些服务商的接口实现。

#### wchat

微信接口。需开通微信公众号，开发阶段可以使用微信开发者平台申请的测试用公众号。调用微信的API实现信息的发送。

#### sms

短信接口。需开通阿里云的短信服务。使用它的API实现信息的发送

#### email

邮件接口。需有一个可用的邮箱作为发件人，使用常规的SMTP进行发送。



## 小目标:可用的邮件接口

- 实现一个restful风格的api ，功能为，收到用户的请求后，使用已有的邮箱帐户，发送`email`。

  - 可能的请求参数为:

  ```json
  {
      "channel": "email",
      "titile": "邮件标题",
      "content": "邮件内容",
      "to": [
          "user1@user1.com",
          "user2@user2.com"
      ]
  }
  ```

  - 该api可能的回复

    - 成功了返回

      ```json
      {
          "success": true,
          "message": "ok"
      }
      ```

    - 失败了返回

      ```json
      {
          "success": false,
          "message": "错误原因"
      }
      ```

      ​




## 中目标：带token验证的3种消息接口 

功能

- 具有简单的用户信息管理
  - 事先保存的用户名，密码列表作为验证依据
- 实现两个接口
  - `token`接口
    - 请求数据包含`username`, `password`
    - 回复数据
      - 成功，说明成功
      - 失败，携带错误原因
  - 消息发送接口
    - 需要验证token有效性
    - 支持`wechat`, `sms`,  `email`




## 大目标：完整的自营消息平台

### 功能

- 用户信息管理/配置
  - 用户帐户信息的录入/导入
  - 用户启用/停用信息发送功能
- 消息管理
  - `wechat`, `sms`, `email` 后台消息接口的参数配置
  - 消息发送失败的处理机制
  - 消息发送频度控制
    - 全局频度控制
    - 针对用户的频度控制
  - 消息历史记录查询
    - 可以查询和统计，包括，不限于
      - 时间
      - 内容
      - 用户
      - 方式
      - 接收方
      - 发送结果
      - 成功发送时间
- 要求具有web界面实现以上功能
  - 具有一个管理员帐户。该帐户不可以发送任何消息
  - web界面需要管理员登录后才可以访问



## 补充说明

每个目标完成后，需要附带有相应的对api测试的测试程序。







注册接口

```json
{
	"username":"eeach",
	"password":"zxl123456",
	"PhoneNumbers":"1590217331",
	"mail":"1326244348@qq.com",
	"openID":"oLMsSw3UBKRwnWeDgzG7eLCQFxJE"
}
```



登陆接口

```json
{
	"username":"eeach",
	"password":"zxl123456"
}
```



微信

```json
{
  "to":"somebady",
  "method":"wechat",
  "content":"..."
}
```

出参

```json
{
    "errorCode": 2001,
    "errorMessage": "token不存在或已失效",
    "success": false
}
```



短信

```json
{
  "to":"somebady",
  "method":"wechat",
  "content":{
  			"errorCode":"45454",
    		"errorMessage":"电脑爆炸"
		}
}
```



邮件

```json
{
  "to":"somebady",
  "method":"smtp",
  "content":{
  		"Subject":"subject",
    	"text":"text"
	},
  "attachment":{
  				"type":"image",
    			"attachment":"...",
    			"name":"image.jpg"
	}
}
```

数据查询（get）

```json
{
    "1": {
        "content": "你好",
        "method": "wechat",
        "result": 0,
        "time": "2017-08-11 13:25:19.959958",
        "touser": "eeach"
    },
    "2": {
        "content": "你好",
        "method": "wechat",
        "result": 1,
        "time": "2017-08-11 13:27:06.526159",
        "touser": "eeach"
    },
    "3": {
        "content": "{'errorCode': '547', 'errorMessage': '电脑哈哈'}",
        "method": "sms",
        "result": 1,
        "time": "2017-08-11 13:34:46.567361",
        "touser": "eeach"
    },
    "4": {
        "content": "haha",
        "method": "smtp",
        "result": 1,
        "time": "2017-08-11 13:38:06.219762",
        "touser": "1326244348@qq.com"
    },
    "5": {
        "content": "{'Subject': '你好', 'text': 'haha'}",
        "method": "smtp",
        "result": 1,
        "time": "2017-08-11 13:38:57.597162",
        "touser": "1326244348@qq.com"
    },
    "6": {
        "content": "{'Subject': '你好', 'text': 'haha'}",
        "method": "smtp",
        "result": 0,
        "time": "2017-08-11 13:42:06.108163",
        "touser": "eeach"
    },
    "7": {
        "content": "{'errorCode': 'sa', 'errorMessage': 'sa'}",
        "method": "sms",
        "result": 0,
        "time": "2017-08-11 13:43:38.140563",
        "touser": "eeach"
    },
    "8": {
        "content": "sad",
        "method": "wechat",
        "result": 0,
        "time": "2017-08-11 13:44:14.838563",
        "touser": "eeach"
    }
}
```



秘钥:



761e51dcb6ba2a52a1a3aa5e57a30053




