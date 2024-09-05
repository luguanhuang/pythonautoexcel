# 项目说明

## 环境准备

``` shell 
├── config                  # 项目私有配置文件
│   └── setting.py
├── config.yaml             # 项目对外配置文件
├── dao                     # 所有与数据库的交互
│   ├── http
│   └── mqtt
│       └── devices.py
├── log                     # 日志文件夹
├── main_pserver_aiot.py    # 入口文件
├── readme.md               # 说明文件
├── services                # 所有的业务逻辑
│   ├── http
│   │   ├── ctwing.py
│   │   ├── public.py
│   │   └── server.py
└── utils                   # 封装的工具都放这个文件夹
    ├── load_yaml.py        # yaml 加载器
    ├── log.py              # 日志工具封装
    ├── mqtt_helper.py      # mqtt工具类
    ├── sign.py             # 签名封装
    └── sql_helper.py       # 数据库底层封装

```