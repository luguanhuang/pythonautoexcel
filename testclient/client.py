import requests


    
data =  {
            # "times": "today"
            # "times": "yesterday"
            # "times": "recentlythreedays"
            # "times": "recentlyoneweek"
            "times": "recentlyonemonth"
        }

data =  {
            "times": "recentlyonemonth"
        }

# data =  {
#             "times": "yesterday"
#         }

# response = requests.post("http://127.0.0.1:5680/aiot/nbdata", json=data)
# data =  {
#             "area": "北京"
#         }


# data =  {
#             "username": "test1",
#             "passwd": "test1"
#         }

# response = requests.post("http://47.115.38.13:5680/UserLogin", json=data)
# data =  {
#             "area": "北京"
#         }
# response = requests.post("http://47.115.38.13:5680/Servproductdata")
# response = requests.post("http://47.115.38.13:5680/Servproductdata")
# response = requests.post("http://127.0.0.1:5680/Keywordpopularity", json=data)
# response = requests.post("http://127.0.0.1:5680/Keywordpopularity")
# response = requests.post("http://127.0.0.1:5680/Servicepopularity")
# response = requests.post("http://127.0.0.1:5680/ServiceRanking")
# response = requests.post("http://127.0.0.1:5680/getnews", json=data)

# data =  {
#             "username": "spoce",
#             "passwd":'langup.cn'
#         }
# response = requests.post("http://47.115.38.13:5680/UserLogin", json=data)
# response = requests.post("http://127.0.0.1:5680/UserLogin", json=data)
# response = requests.post("http://127.0.0.1:5680/DialogueData")
# response = requests.post("http://127.0.0.1:5680/DataOverview")
response = requests.post("http://127.0.0.1:5680/KeywordProdRelat")
# response = requests.post("http://127.0.0.1:5680/ScriptsCategoryRelat")
content = response.content
print("content112=", content);


# import socket
 
# # 创建一个TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# # 连接服务器
# server_address = ('localhost', 8990)  # 服务器地址和端口
# sock.connect(server_address)
 
# # 发送数据
# message = b'Hello, World!'  # 使用bytes对象发送消息
# sock.sendall(message)
 
# # # 接收服务器响应（如果有的话）
# # response = sock.recv(1024)
 
# # print('Received:', response)
 
# # 关闭连接
# sock.close()