---

---

# iMSG接口说明文档





## 1.接口简介



#### 1.1 接口功能概述

​	iMSG接口是用于发送消息的restful api，主要功能就是将实时的消息通过短信、微信或邮箱发送至用户指定的账号。

#### 1.2 接口概览

|               url                |        说明         |
| :------------------------------: | :---------------: |
| http://120.55.37.37/api/register |    添加新用户(网页需要）    |
|  http://120.55.37.37/api/login   |  获取access_token   |
|   http://120.55.37.37/api/send   |       发送消息        |
|  http://120.55.37.37/api/modify  | 更改发送消息频次（网页、调试需要） |
|  http://120.55.37.37/api/query   |  返回历史发送信息（网页需要）   |

#### 1.3 接口调用流程

- 如果用户信息未进行导入，登陆http://120.55.37.37，管理员账号admin密码123，进行创建和更改用户信息
- 用用户信息获取access_token
- 携带token访问接口url，进行信息的发送。在这里需要特别指出，微信号的openID比较难于识记，因此我们采用一个统一的标记去代openID。只需关注微信公众号，点击“获取我的openID“即可获得这个标记。



## 2.获取access_token

- 设置了一个用户名："天存-system-1001"  密码："123456"（也可自行到120.55.37.37添加用户）
- url：http://120.55.37.37/api/login
- 请求方式：POST
- 请求参数格式：JSON
- 请求参数

|          | 是否必须 | 数据类型 | 默认值  |  说明  |
| :------: | :--: | :--: | :--: | :--: |
| username |  是   | str  |  --  | 用户名  |
| password |  是   | str  |  --  |  密码  |



- 返回参数


|     返回字段     | 数据类型 |             说明             |
| :----------: | :--: | :------------------------: |
|  errorCode   | int  |   请求结果的错误码（成功为0，其他详见附表）    |
| errorMessage | str  |       错误的具体信息（详见附表）        |
|    token     | str  | 用于访问接口的access_token（成功时返回） |



- 返回示例

  - 成功

  ```json
  {
      "errorCode": 0,
      "errorMessage": "OK",	    			"token":"OTljMTUwZTljNmRkN2JlOTJiNTJkN2IzMzhmNWZjZDY6MTUwMzAzMDA5NS43NDA3NTc1OnpoYW5		nOmYxMDcxMWEwMmRjY2NkM2QxNmM3YTNiOTc1NzQ0NWMyZWZlMzlmNmE="
  }
  ```

  - 失败

  ```json
  {
      "errorCode": 10006,
      "errorMessage": "用户不存在"
  }
  ```





## 3.发送消息

- url：http://120.55.37.37/api/send
- 请求方式：POST
- 请求参数格式：JSON
- 请求参数

|            | 是否必须 |        数据类型        |                   参考值                    |              说明               |
| :--------: | :--: | :----------------: | :--------------------------------------: | :---------------------------: |
|   token    |  是   |        str         |                    --                    |             token             |
|     to     |  是   |   str或者list（群发）    | "##@163.com"或["159####1256","137####1235"] | 要发送给的用户名(注意：群发时列表内只能是同一种发送方式) |
|   method   |  是   |        str         |    “sms”（短信）、"smtp"（邮件）、"wechat"（微信）     |  发送方式（'smtp','sms','wechat'）  |
|  content   |  是   | 邮件为dict，其余str（见示例） | "明天下雨"(用于短信和微信)、{"subject":"开会通知","text":"下午两点半"}（用于邮件） |             发送内容              |
| attachment |  可选  |     dict（见示例）      | {"filename":"hello.md","file":"这里填读出文件b64encode的结果"} |           仅邮件发送时支持            |

- 请求示例

  - 不带附件邮件

    ```json
    {
    	"token":"###",
    	"to":"zhang@163.com",
    	"method":"smtp",
    	"content":{
    		"subject":"hello",
    		"text":"您好"
    	}
    }
    ```

  - 群发

  ```json
  {
  	"token":"###",
  	"to":["zhang@163.com","####@##.##","####@###.###"],
  	"method":"smtp",
  	"content":{
  		"subject":"hello",
  		"text":"您好"
  	}
  }
  ```

  ​

  - 带附件邮件

  ```json
  {
  	"token":"###",
  	"to":"zhang@163.com",
  	"method":"smtp",
  	"content":{
  		"subject":"hello",
  		"text":"您好"
  	},
    "attachment":{
  		"filename":"###.txt",
      	"file":"#####"
  	}
  }
  ```

  - 短信或微信

  ```json
  {
  	"token":"###",
  	"to":"####",
  	"method":"sms",
  	"content":"###"
  }
  ```

  - 群发

  ```json
  {
  	"token":"###",
  	"to":["####","####","####"],
  	"method":"sms",
  	"content":"###"
  }
  ```

- 返回结果示例

  - 成功

  ```json
  {
      "errorCode": 0,
      "errorMessage": "OK"
  }
  ```

  ​

  - 失败

  ```json
  {
      "errorCode": 10013,
      "errorMessage": "超出发送消息的频率限制"
  }
  ```

  ​


## 4.更改发送频次

- url：http://120.55.37.37/api/modify/<username>  （username是用户的名字）
- 请求方式：POST
- 请求参数格式：JSON
- 请求参数：

|           | 是否必须 | 默认值  |    说明    |
| :-------: | :--: | :--: | :------: |
|  per_day  |  是   |  20  |  每天发送频次  |
| per_hour  |  是   |  5   | 每小时发送频次  |
| available |  可选  | true | 发送功能是否开启 |



- 返回示例

  - 成功

  ```json
  {
      "errorCode": 0,
      "errorMessage": "OK"
  }
  ```

  - 失败

  ```json
  {
      "errorCode": 10017,
      "errorMessage": "错误参数的类型"
  }
  ```





## 5.查询历史消息

- url：http://120.55.37.37/api/query


- 请求方式：GET







## 6. 返回错误码列表

|   0   |        OK        |
| :---: | :--------------: |
| 10001 |     请求数据格式错误     |
| 10002 |     缺少必要请求参数     |
| 10003 | 用户电话或邮箱或微信号已经被注册 |
| 10004 |      用户名已存在      |
| 10005 |   token不存在或已失效   |
| 10006 |      用户不存在       |
| 10007 |       密码错误       |
| 10008 |     错误的发送方式      |
| 10009 |    错误的消息内容格式     |
| 10010 |    错误的附件内容格式     |
| 10011 |      无效的收件人      |
| 10012 |      系统内部错误      |
| 10013 |   超出发送消息的频率限制    |
| 10014 |    用户未关注微信公众号    |
| 10015 |     无此公众微信号      |
| 10016 |       见详情        |
| 10017 |     错误参数的类型      |

