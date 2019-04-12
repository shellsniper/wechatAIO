
# coding:utf-8

from User_API import *
from __prettytable import PrettyTable
from itchat.content import *
import logging
import json
import itchat
import threading
import time
import os
# os.chdir(os.path.dirname(__file__))
import re
import sys
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR + "/../util")
# print(sys.path)
# root_dir = str(os.path.dirname(os.path.abspath(__file__))
# sys.path.append(root_dir)


# 字典缓存
msg_friend = {}
msg_group = {}
# 自动回复开关
SWITCH_REPLY = 0
# 消息前缀开关
SWITCH_PREFIX = 1
# 消息前缀内容
PREFIX_CONTENT = "[自动回复]"
HELPER = '''
                【功能列表】
                1./help             显示功能列表
                2./auto_reply       自动回复开关
                '''
# 回复内容字典
REPLY_DICT = {}
# 文件临时存储文件夾
#friend_data_dir = os.path.join(os.getcwd(), '/data/friend/')

FRIEND_DIR = ROOT_DIR + '/../data/friend/'
# print(FRIEND_DIR)
#group_data_dir = os.path.join(os.getcwd(), '/data/group/')
GROUP_DIR = ROOT_DIR + '/../data/group/'
face_bug = None


# ------------------------------------------------------------------
#  functions
# ------------------------------------------------------------------
def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

# prettytable


def table(field, row):
    x = PrettyTable(header_style='upper', padding_width=0)
    x.field_names = field
    x.add_row(row)
    print(x)

# 保持登录状态


def keep_alive():
    text = "保持登录"
    itchat.send(text, toUserName="filehelper")
    friend_log.info("Sending text to FileHelper for Keeping Connection...")
    print("Sending text to FileHelper for Keeping Connection...")
    global timer1
    timer1 = threading.Timer(60*6, keep_alive)
    timer1.start()

# delay_reply


#--------------------------------------------------------------------------#
# itchat handlers
#--------------------------------------------------------------------------#

@itchat.msg_register([TEXT, PICTURE], isFriendChat=True, isGroupChat=False)
def auto_reply(msg):
    #('Starting to Replay')
    print('Starting to Replay')
    backend_log.info('Starting AUTO_REPLY')
    reply_content = PREFIX_CONTENT + "你好，我有空就会回复你"
    if SWITCH_REPLY == 1:
        itchat.send(reply_content, msg['FromUserName'])
    else:
        pass

@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    global facebug
    global SWITCH_REPLY
    global SWITCH_PREFIX
    global HELPER
    msg_time_rec = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime())  # 接受消息的时间
    msg_from = itchat.search_friends(userName=msg['FromUserName'])[
        'NickName']  # 在好友列表中查询发送信息的好友昵称
    msg_time = msg['CreateTime']  # 信息发送的时间
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐

    # print(msg['MsgId'])
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':  # 如果发送的消息是文本或者好友推荐
        msg_content = msg['Text']
        field = ['DateTime', 'From', 'Content', 'Type']
        row = [str(msg_time_rec), msg_from, msg_content, msg['Type']]
        friend_log.info("{}, {}, {}, {}".format(
            str(msg_time_rec), msg_from, msg_content, msg['Type']))
        table(field, row)
        #===============================================================#
        # handle custom setting
        #===============================================================#
        if msg['ToUserName'] == 'filehelper':
            Current_Setting = "Auto_Reply: {}\n, Switch_Prefix: {}".format(SWITCH_REPLY, SWITCH_PREFIX)
            args = msg_content.split(' ')
            if args[0] == '/help':
                itchat.send(HELPER, toUserName='filehelper')
            elif args[0] == '/auto_reply':
                if args[1] == '1':
                    SWITCH_REPLY = 1
                    itchat.send(Current_Setting, toUserName='filehelper')
                elif args[1] == '0':
                    SWITCH_REPLY = 0
                    itchat.send(Current_Setting, toUserName='filehelper')
                else:
                    SWITCH_REPLY = 0
                    itchat.send(Current_Setting, toUserName='filehelper')
        #===============================================================#
        #print("在{}: {}发送了: {}, 类型是{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type']))
        # print(msg_content)

    # 如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
            or msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording':
        msg_content = msg['FileName']  # 内容就是他们的文件名
        msg['Text'](FRIEND_DIR + str(msg_content))  # 下载文件
        field = ['DateTime', 'From', 'Content', 'Type', 'Dir']
        row = [str(msg_time_rec), msg_from,
               msg_content, msg['Type'], FRIEND_DIR]
        friend_log.info("{}, {}, {}, {}, {}".format(
            str(msg_time_rec), msg_from, msg_content, msg['Type'], FRIEND_DIR))
        table(field, row)
        #print("在{}: {}发送了: {}, 类型是{}, 已下载到{}目录下 ".format(str(msg_time_rec), msg_from, msg_content, msg['Type'], friend_data_dir))
        # print msg_content
    elif msg['Type'] == 'Card':  # 如果消息是推荐的名片
        # 内容就是推荐人的昵称和性别
        msg_content = msg['RecommendInfo']['NickName'] + u'name card'
        msg_user_name = msg['RecommendInfo']['UserName']
        if msg['RecommendInfo']['Sex'] == 1:
            msg_content += u'性别为男'
        else:
            msg_content += u'性别为女'
        field = ['DateTime', 'From', 'Content', "ID", 'Type']
        row = [str(msg_time_rec), msg_from, msg_content,
               msg_user_name, msg['Type']]
        friend_log.info("{}, {}, {}, {}, {}".format(
            str(msg_time_rec), msg_from, msg_content, msg_user_name, msg['Type']))
        table(field, row)
        #print("在{}: {}发送了: {}, 微信号为:{}, 类型是{} ".format(str(msg_time_rec), msg_from, msg_content, msg_user_name, msg['Type']))
    elif msg['Type'] == 'Map':  # 如果消息为分享的位置信息
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + u" 经度->" + y.__str__()  # 内容为详细的地址
        else:
            msg_content = r"" + location
        field = ['DateTime', 'From', 'Content', 'Type']
        row = [str(msg_time_rec), msg_from, msg_content, msg['Type']]
        friend_log.info("{}, {}, {}, {}".format(
            str(msg_time_rec), msg_from, msg_content,  msg_content, msg['Type']))
        table(field, row)
        #print("在{}: {}发送了: {}, 类型是{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type']))
    elif msg['Type'] == 'Sharing':  # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']  # 记录分享的url
        field = ['DateTime', 'From', 'Content', 'Type', "URL"]
        row = [str(msg_time_rec), msg_from, msg_content,
               msg['Type'], msg_share_url]
        friend_log.info("{}, {}, {}, {}, {}".format(
            str(msg_time_rec), msg_from, msg_content, msg['Type'], msg_share_url))
        table(field, row)
        #print("在{}: {}发送了: {}, 类型是{}, URL为:{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type'], msg_share_url))
    face_bug = msg_content

    # 将信息存储在字典中，每一个msg_id对应一条信息
    msg_friend.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )


@itchat.msg_register([TEXT, PICTURE, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def handle_group_msg(msg):
    #print("chatroom_ids: {}".format(chatroom_ids))
    # print(msg)
    # 消息来自于哪个群聊
    #m = json.dumps(msg)
    #open('msg.json', 'w').write(m)
    chatroom_id = msg['FromUserName']
    if chatroom_id in groups:
        chatroom_name = groups[chatroom_id]
    else:
        chatroom_name = 'Group Unsaved'
    # print("chatid:{}".format(chatroom_id))
    msg_time_rec = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime())  # 接受消息的时间
    msg_from = msg['ActualNickName']
    msg_time = msg['CreateTime']  # 信息发送的时间
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
    # print(msg['MsgId'])
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':  # 如果发送的消息是文本或者好友推荐
        msg_content = msg['Text']
        field = ['@GroupName', 'DateTime', 'From', 'Content', 'Type']
        row = [chatroom_name, str(msg_time_rec),
               msg_from, msg_content, msg['Type']]
        group_log.info("{}, {}, {}, {}, {}".format(chatroom_name, str(
            msg_time_rec), msg_from, msg_content, msg['Type']))
        table(field, row)
        #print("在{}: {}发送了: {}, 类型是{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type']))
        # print(msg_content)

    # 如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
            or msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording':
        msg_content = msg['FileName']  # 内容就是他们的文件名
        msg['Text'](GROUP_DIR + str(msg_content))  # 下载文件
        field = ['@GroupName', 'DateTime', 'From', 'Content', 'Type', "Dir"]
        row = [chatroom_name, str(msg_time_rec), msg_from,
               msg_content, msg['Type'], GROUP_DIR]
        group_log.info("{}, {}, {}, {}, {}, {}".format(chatroom_name, str(
            msg_time_rec), msg_from, msg_content, msg['Type'], GROUP_DIR))
        table(field, row)
        #print("在{}: {}发送了: {}, 类型是{}, 已下载到{}目录下 ".format(str(msg_time_rec), msg_from, msg_content, msg['Type'], group_data_dir))
        # print msg_content

    elif msg['Type'] == 'Sharing':  # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']  # 记录分享的url
        field = ['@GroupName', 'DateTime', 'From', 'Content', 'Type', "URL"]
        row = [chatroom_name, str(msg_time_rec), msg_from,
               msg_content, msg['Type'], msg_share_url]
        group_log.info("{}, {}, {}, {}, {}, {}".format(chatroom_name, str(
            msg_time_rec), msg_from, msg_content, msg['Type'], msg_share_url))
        table(field, row)

        #print("在{}: {}发送了: {}, 类型是{}, URL为:{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type'], msg_share_url))

    # 将信息存储在字典中，每一个msg_id对应一条信息
    msg_group.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )
# 消息防撤回
@itchat.msg_register([NOTE], isFriendChat=True, isGroupChat=True)
def send_msg_helper(msg):
    global face_bug
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) \
            is not None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>",
                               msg['Content']).group(1)
        old_msg = msg_group.get(old_msg_id, {})
        print(old_msg)
        if len(old_msg_id) < 11:
            itchat.send(old_msg, toUserName='filehelper')
        else:
            msg_body = "有人撤回消息" + "\n" \
                + old_msg.get('msg_from') + " 撤回了 " \
                + old_msg.get('msg_type') + " 消息" + "\n" \
                + old_msg.get('msg_time_rec') + "\n" \
                + r"" + old_msg.get('msg_content')
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个连接->" + old_msg.get('msg_share_url')
            itchat.send(msg_body, toUserName='filehelper')
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file_name = '/../data/group/{}'.format(old_msg['msg_content'])
                itchat.send(msg=file_name, toUserName='filehelper')
            msg_group.pop(old_msg_id)


def after_logout():
    itchat.logout()


'''
@itchat.msg_register([NOTE], isFriendChat=True, isGroupChat=True)
def revoke_msg(msg):
    if revoke_msg_compile.search(msg['Content']) is not None:
        old_msg_id = extract_msgid_compile.search(msg['Content']).group(1)
        old_msg = rec_msg_dict.get(old_msg_id, {})
        # 先发送一条文字信息
        itchat.send_msg(str(old_msg.get('msg_from_user') + "撤回了一条信息："
                            + old_msg.get('msg_content')), toUserName="filehelper")
        # 判断文msg_content是否存在，不存在说明可能是
        if os.path.exists(os.path.join(data_dir, old_msg.get('msg_content'))):
            if old_msg.get('msg_type') == 'Picture':
                itchat.send_image(os.path.join(data_dir, old_msg.get('msg_content')),
                                  toUserName="filehelper")
            elif old_msg.get('msg_type') == 'Video':
                itchat.send_video(os.path.join(data_dir, old_msg.get('msg_content')),
                                  toUserName="filehelper")
            elif old_msg.get('msg_type') == 'Attachment' \
                    or old_msg.get('msg_type') == 'Recording':
                itchat.send_file(os.path.join(data_dir, old_msg.get('msg_content')),
                                 toUserName="filehelper") 
'''
if __name__ == '__main__':
    #################################
    # log init()
    #################################
    setup_logger('friend_log', 'log/friend.log')
    setup_logger('group_log', 'log/group.log')
    setup_logger('backend_log', 'log/backend.log')
    friend_log = logging.getLogger('friend_log')
    group_log = logging.getLogger('group_log')
    backend_log = logging.getLogger('backend_log')
    #################################
    # print(FRIEND_DIR)
    if not os.path.exists(FRIEND_DIR):
        os.mkdir(FRIEND_DIR)
    if not os.path.exists(GROUP_DIR):
        os.mkdir(GROUP_DIR)
    #################################
    itchat.auto_login(hotReload=True, exitCallback=after_logout)
    #################################
    # Download User info as JSON
    # 排除自己
    friends = itchat.get_friends(update=True)[1:]
    #friends = ['1', '2', '3']
    user_meta = Login()
    user_info_dir = "{}/../user_info.json".format(ROOT_DIR)
    #################################
    try:
        backend_log.info(
            "Note:\nUser_Info.json has been stored at: {}...\n".format(user_info_dir))
        print("Note:\nUser_Info.json has been stored at: {}...\n".format(user_info_dir))
        f = open(user_info_dir, 'r')
        os.remove(user_info_dir)
        for friend in friends:
            json_info = json.dumps(friend)
            with open(user_info_dir, "a", encoding="utf-8") as f:
                f.write(json_info)
                f.write('\n')
            f.close()
    except FileNotFoundError:
        backend_log.warning("Retrieving Data from Wecaht... ")
        print("Note:\nUser_Info.json has been stored at: {}...\n".format(user_info_dir))
        for friend in friends:
            json_info = json.dumps(friend)
            with open(user_info_dir, "a", encoding="utf-8") as f:
                f.write(json_info)
                f.write('\n')
            f.close()
    ##################################
    # Thread to keep connection
    timer1 = threading.Timer(60*6, keep_alive)
    timer1.start()

#    timer2=threading.Timer(DELAY_TIME, reply)
 #   timer2.start()
    ###############################
    # init group info
    chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
    #s = json.dumps(chatrooms)
    # open("chatroom.json","w").write(s)
    print(Fore.LIGHTYELLOW_EX + '---------------------------\nNumber of Monitoring Groups: {}\n-----------------------------\n'.format(str(len(chatrooms))))
    print("You need set 'Save to Contacts' for your groups in your Wechat APP, otherwise, unsaved group would not be up-to-date\n" + Fore.RESET)
    groups = {}
    tb = PrettyTable(header_style='upper', padding_width=0)
    tb.field_names = ['GroupName', 'GroupID']
    for item in chatrooms:
        groups[item['UserName']] = (item['NickName'])
        tb.add_row([item['NickName'], item['UserName']])
    print(tb)
    print('\n\n')
    #g = json.dumps(groups)
    # open("group.json","w").write(g)
    itchat.run()
