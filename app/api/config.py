ERROR = [
    {"errorCode": 0, "errorMessage": "OK"},
    {"errorCode": 10001, "errorMessage": u"请求数据格式错误"},
    {"errorCode": 10002, "errorMessage": u"缺少必要请求参数"},
    {"errorCode": 10003, "errorMessage": u"用户电话或邮箱或微信号已经被注册"},
    {"errorCode": 10004, "errorMessage": u"用户名已存在"},
    {"errorCode": 10005, "errorMessage": u"token不存在或已失效"},
    {"errorCode": 10006, "errorMessage": u"用户不存在"},
    {"errorCode": 10007, "errorMessage": u"密码错误"},
    {"errorCode": 10008, "errorMessage": u"错误的发送方式"},
    {"errorCode": 10009, "errorMessage": u"错误的消息内容格式"},
    {"errorCode": 10010, "errorMessage": u"错误的附件内容格式"},
    {"errorCode": 10011, "errorMessage": u"无效的收件人"},
    {"errorCode": 10012, "errorMessage": u"系统内部错误"},
    {"errorCode": 10013, "errorMessage": u"超出发送消息的频率限制或发送权限被关闭"},
    {"errorCode": 10014, "errorMessage": u"用户未关注微信公众号"},
    {"errorCode": 10015, "errorMessage": u"无此公众微信号"},
    {"errorCode": 10016, "errorMessage": u"见详情"},
    {"errorCode": 10017, "errorMessage": u"错误参数的类型"}
]


class SMTP:
    SERVER = 'smtp.163.com'
    PORT = 25
    USERNAME = 'eeach_test'
    PASSWORD = 'zxl123456'
    ADDRESS = '@163.com'


class SMS:
    PARAMETERS = {
        'Format': 'JSON',
        'Version': '2017-05-25',
        'AccessKeyId': 'LTAI8k5R9SLp49Dh',
        'SignatureVersion': '1.0',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': None,
        'RegionId': 'cn-hangzhou',
        'Timestamp': None
    }

    USER_PARAMS = {
        'Action': 'SendSms', 'TemplateParam': None,
        'PhoneNumbers': None, 'SignName': 'iMSG平台',
        'TemplateCode': 'SMS_84585008'
    }

    TEMPLATE_PARAM = {
        'errorCode': '23333',
        'errorMessage': None
    }

    KEY_ID = 'LTAI8k5R9SLp49Dh'
    KEY_SECRET = 'om3WttcF0ugQ1gpES3PqOOsyYzt36x'
    SERVER = 'https://dysmsapi.aliyuncs.com'


class WECHAT:
    APPID = 'wxfeee112304c755ea'
    APPSECRET = '6c19249d9fa4074bd9207dc1269fac5c'
    TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
    MESSAGE_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="
