import time
# a = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
# print(a)
import uuid
import hmac, secrets, base64

# print(uuid.uuid1())
# key = str(uuid.uuid1())
# print('key',key)
# message = 'eeach'
# ts_str = str(time.time() + 300)
# sha1_str = hmac.new(key.encode('utf-8'), ts_str.encode('utf-8'), 'sha1').hexdigest()
# print('sha1_str=', sha1_str)
# random_token = secrets.token_hex(16)
# print('random=', random_token)
# token = random_token + ':' + ts_str + ':' + message + ':' + sha1_str
# print('token', token)
# base64_token = base64.urlsafe_b64encode(token.encode('utf-8')).decode('utf-8')
# print('base64', base64_token,type(base64_token))
# haha=base64.urlsafe_b64decode(base64_token).decode('utf-8')
# print(haha)
# class A():
#     def __init__(self, str):
#         self.data = str + "haha"
#
#     def set_data(self, str_add):
#         self.data += str_add
#
#     def return_data(self):
#         return self.data
#
#     def get_data(self):
#         return (self.data + 'kl')
#
#
# class B():
#     def __init__(self, str):
#         self.data = str
#
#     def get_data(self):
#         return self.data + '这是B'
#
#
# class C(A, B):
#     def __init__(self, str):
#         A.__init__(self, str)
#         self.sdata = super().return_data()
#         B.__init__(self, self.sdata)
#
#     def show(self):
#         print(super().return_data())
#         # print(super().get_data())
#         print(B.get_data(self))
#         # super(C, self).show()


if __name__ == '__main__':
    # b = {'username': 'eeach','sad':'asd' ,'pssword': 'zxl123'}
    # if 'username' in b.keys() and 'password' in b.keys():
    #     print('可以')
    # # if b.has_key('username'):
    # #     print("这个也可以")
    # print(list(b.keys()),type(b.keys()))
    # if ['username','passqord'] in list(b.keys()):
    #     print('成功一半')
    # a = C('eeach')
    # a.show()
    a = '{"message":"你好","Raskdl":"asdasd"}'
    b = a.split('"')
    print(b)
    # c=dict(b)
