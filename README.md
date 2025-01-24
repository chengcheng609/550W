代码简介
1. 导入必要的库
python
import json
import bcrypt
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
json: 用于读取和写入用户数据文件。
bcrypt: 用于安全地存储和验证用户密码。
chatterbot: 用于创建和训练聊天机器人。
logging: 用于记录程序运行过程中的日志信息。
2. 设置日志记录
python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
配置日志记录级别为INFO，并创建一个日志记录器。
3. 文件路径
python
USERS_FILE = 'users.json'
定义用户数据文件的路径。
4. 加载用户数据
python
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning("用户文件未找到，创建新的用户文件。")
        return {}
从users.json文件中加载用户数据。
如果文件不存在，记录警告并返回一个空字典。
5. 保存用户数据
python
def save_users(users):
    try:
        with open(USERS_FILE, 'w') as file:
            json.dump(users, file)
    except IOError as e:
        logger.error(f"保存用户文件时出错: {e}")
将用户数据保存到users.json文件中。
如果保存过程中出现错误，记录错误信息。
6. 注册用户
python
def register_user(users):
    username = input("请输入用户名：")
    if username in users:
        print("用户名已存在，请重新输入。")
        return
    password = input("请输入密码：")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password.decode('utf-8')
    save_users(users)
    print("注册成功")
提示用户输入用户名和密码。
检查用户名是否已存在，如果存在则提示重新输入。
使用bcrypt对密码进行哈希处理，并将用户名和哈希后的密码存储到用户数据中。
保存用户数据到文件。
7. 初始化聊天机器人
python
def init_chatbot():
    try:
        chatbot = ChatBot('SimpleAI')
        trainer = ChatterBotCorpusTrainer(chatbot)
        trainer.train("chatterbot.corpus.chinese")
        return chatbot
    except Exception as e:
        logger.error(f"初始化聊天机器人时出错: {e}")
        return None
创建一个名为SimpleAI的聊天机器人。
使用ChatterBotCorpusTrainer训练聊天机器人，训练数据来自chatterbot.corpus.chinese。
如果初始化过程中出现错误，记录错误信息并返回None。
8. 登录用户
python
def login_user(users):
    username = input("请输入用户名：")
    password = input("请输入密码：")
    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username].encode('utf-8')):
        print("登录成功")
        is_root = False  # 添加一个标志变量来标识是否处于root状态
        chatbot = init_chatbot()  # 初始化聊天机器人
        if chatbot is None:
            return
        while True:
            if is_root:
                code_input = input("已开启 root 权限 >>>")  # 修改提示信息以显示root状态
            else:
                code_input = input(">>>")
            if code_input.lower() == "exit":
                break
            if code_input.lower() == "root":
                print("新输入: root 是开启 root 权限")
                is_root = True  # 设置root标志变量为True
                continue
            if is_root:
                try:
                    exec(code_input)
                except NameError as e:
                    print(f"not code {e}")
                except Exception as e:
                    print(f"not code {e}")
            else:
                response = chatbot.get_response(code_input)  # 使用聊天机器人响应
                print(response)
    else:
        print("登录失败")
提示用户输入用户名和密码。
验证用户名和密码是否匹配。
如果验证成功，进入代码界面。
使用is_root标志变量来标识是否处于root权限状态。
如果处于root权限状态，允许用户执行任意Python代码。
如果处于普通用户状态，使用聊天机器人响应用户的输入。
支持root命令来切换到root权限状态。
支持exit命令来退出当前会话。
9. 主程序
python
def main():
    users = load_users()
    while True:
        print("1 注册 2 登录  3 退出")
        input_num = input("请输入数字：")
        if input_num == "1":
            register_user(users)
        elif input_num == "2":
            login_user(users)
        elif input_num == "3":
            print("退出")
            exit()
        else:
            print("无效的输入，请重新输入。")

if __name__ == "__main__":
    main()
加载用户数据。
提供一个循环菜单，允许用户选择注册、登录或退出。
根据用户的选择调用相应的函数。
总结
用户管理：支持用户注册和登录，使用bcrypt对密码进行安全存储。
聊天机器人：集成chatterbot库，提供中文对话功能。
权限管理：支持root权限，允许执行任意Python代码。
日志记录：记录程序运行过程中的重要信息，便于调试和维护。
