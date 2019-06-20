'''
dict 客户端
功能：根据用户输入，发送请求，得到结果
结构：一级界面--->注册  登录  退出
     二级界面 --->查单词 历史记录  注销
'''
from socket import *
from getpass import getpass  # 运行使用终端
import sys

# 服务器地址
ADDR = ('127.0.0.1', 8000)
# 搭建客户端网络
s = socket()
s.connect(ADDR)


def do_register():
    while True:
        name = input("User:")
        password = getpass()
        password_ = getpass("Again:")
        if (" " in name) or (' ' in password):
            print("用户名或密码不能有空格")
            continue
        if password != password_:
            print('两次密码不一致')
            continue
        msg = "R %s %s" % (name, password)
        s.send(msg.encode())  # 发送请求
        data = s.recv(128).decode()  # 接收反馈信息
        if data == 'OK':
            print('注册成功')
            login(name)
        else:
            print('注册失败')
        return


def do_login():
    name = input('User:')
    password = getpass()
    msg = 'L %s %s' % (name, password)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        print('登录成功')
        login(name)

    else:
        print('登录失败')


def do_query(name):
    while True:
        word = input("请输入查询单词:")
        if word == '##':  # 结束单词查询
            break
        msg = 'Q %s %s' % (name, word)
        s.send(msg.encode())
        # 直接接收查询结果（或者没找到）
        data = s.recv(2048)
        print(data.decode())


def do_hist(name):
    msg = "H %s" % name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("没有历史记录")


def login(name):
    while True:
        print('''===================Query=================
                1.查单词           2.历史记录                    3.注销''')
        cmd = input("输入选项")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_hist(name)

        elif cmd == "3":
            return
        else:
            print("请输入正确选项")


def main():
    while True:
        print('''===================Welcome=================
                1.注册           2.登录                    3.退出''')
        cmd = input("输入选项")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()

        elif cmd == "3":
            return
        else:
            print("请输入正确选项")


if __name__ == '__main__':
    main()
