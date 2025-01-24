import json
import bcrypt
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 文件路径
USERS_FILE = 'users.json'

# 加载用户数据
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning("用户文件未找到，创建新的用户文件。")
        return {}

# 保存用户数据
def save_users(users):
    try:
        with open(USERS_FILE, 'w') as file:
            json.dump(users, file)
    except IOError as e:
        logger.error(f"保存用户文件时出错: {e}")

# 注册用户
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

# 初始化聊天机器人
def init_chatbot():
    try:
        chatbot = ChatBot('SimpleAI')
        trainer = ChatterBotCorpusTrainer(chatbot)
        trainer.train("chatterbot.corpus.chinese")
        return chatbot
    except Exception as e:
        logger.error(f"初始化聊天机器人时出错: {e}")
        return None

# 登录用户
def login_user(users):
    username = input("请输入用户名：")
    password = input("请输入密码：")
    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username].encode('utf-8')):
        print("登录成功")
        # 进入代码界面
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
            # 检查是否输入了特权命令
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

# 主程序
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