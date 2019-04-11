
# coding:utf-8

import os
#os.chdir(os.path.dirname(__file__))
import re
import sys
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR + "/../util")
#print(sys.path)
#root_dir = str(os.path.dirname(os.path.abspath(__file__))
#sys.path.append(root_dir)
import time
import threading
import itchat
from itchat.content import *
from __prettytable import PrettyTable
from User_API import *

#字典缓存
msg_friend = {}
msg_group = {}

# 文件临时存储文件夾
#friend_data_dir = os.path.join(os.getcwd(), '/data/friend/')

FRIEND_DIR = ROOT_DIR + '/../data/friend'
#print(FRIEND_DIR)
#group_data_dir = os.path.join(os.getcwd(), '/data/group/')
GROUP_DIR = ROOT_DIR + '/../data/group'


# prettytable
def table(field, row):
    x = PrettyTable(header_style='upper', padding_width=0)
    x.field_names = field
    x.add_row(row)
    print(x)

# 保持登录状态    
def keep_alive():
    text="保持登录"
    itchat.send(text, toUserName="filehelper")
    print("Sending text to FileHelper for Keeping Connection...")
    global timer1
    timer1 = threading.Timer(60*6, keep_alive)
    timer1.start()

@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
            msg_time_rec = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())  # 接受消息的时间
            msg_from = itchat.search_friends(userName=msg['FromUserName'])[
                                             'NickName']  # 在好友列表中查询发送信息的好友昵称
            msg_time = msg['CreateTime']  # 信息发送的时间
            msg_id = msg['MsgId']  # 每条信息的id
            msg_content = None  # 储存信息的内容
            msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
            
            #print(msg['MsgId'])
            if msg['Type'] == 'Text' or msg['Type'] == 'Friends':  # 如果发送的消息是文本或者好友推荐
                msg_content = msg['Text']
                field = ['DateTime', 'From', 'Content', 'Type']
                row = [str(msg_time_rec), msg_from, msg_content, msg['Type']]
                table(field, row)
                #print("在{}: {}发送了: {}, 类型是{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type']))
                #print(msg_content)

            # 如果发送的消息是附件、视屏、图片、语音
            elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
                    or msg['Type'] == 'Picture' \
                    or msg['Type'] == 'Recording':
                msg_content = msg['FileName']  # 内容就是他们的文件名
                msg['Text'](FRIEND_DIR + str(msg_content))  # 下载文件
                field = ['DateTime', 'From', 'Content', 'Type', 'Dir']
                row = [str(msg_time_rec), msg_from, msg_content, msg['Type'], FRIEND_DIR]
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
                row = [str(msg_time_rec), msg_from, msg_content, msg_user_name, msg['Type']]
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
                table(field, row)
                #print("在{}: {}发送了: {}, 类型是{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type']))
            elif msg['Type'] == 'Sharing':  # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
                msg_content = msg['Text']
                msg_share_url = msg['Url']  # 记录分享的url
                field = ['DateTime', 'From', 'Content', 'Type', "URL"]
                row = [str(msg_time_rec), msg_from, msg_content, msg['Type'], msg_share_url]
                table(field, row)
                #print("在{}: {}发送了: {}, 类型是{}, URL为:{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type'], msg_share_url))

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
            msg_time_rec = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())  # 接受消息的时间
            msg_from = msg['ActualNickName']
            msg_time = msg['CreateTime']  # 信息发送的时间
            msg_id = msg['MsgId']  # 每条信息的id
            msg_content = None  # 储存信息的内容
            msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
            
            #print(msg['MsgId'])
            if msg['Type'] == 'Text' or msg['Type'] == 'Friends':  # 如果发送的消息是文本或者好友推荐
                msg_content = msg['Text']
                field = ['DateTime', 'From', 'Content', 'Type']
                row = [str(msg_time_rec), msg_from, msg_content, msg['Type']]
                table(field, row)
                #print("在{}: {}发送了: {}, 类型是{} ".format(str(msg_time_rec), msg_from, msg_content, msg['Type']))
                #print(msg_content)

            # 如果发送的消息是附件、视屏、图片、语音
            elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
                    or msg['Type'] == 'Picture' \
                    or msg['Type'] == 'Recording':
                msg_content = msg['FileName']  # 内容就是他们的文件名
                msg['Text'](GROUP_DIR + str(msg_content))  # 下载文件
                field = ['DateTime', 'From', 'Content', 'Type', "Dir"]
                row = [str(msg_time_rec), msg_from, msg_content, msg['Type'], GROUP_DIR]
                table(field, row)
                #print("在{}: {}发送了: {}, 类型是{}, 已下载到{}目录下 ".format(str(msg_time_rec), msg_from, msg_content, msg['Type'], group_data_dir))
                # print msg_content

            elif msg['Type'] == 'Sharing':  # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
                msg_content = msg['Text']
                msg_share_url = msg['Url']  # 记录分享的url
                field = ['DateTime', 'From', 'Content', 'Type', "URL"]
                row = [str(msg_time_rec), msg_from, msg_content, msg['Type'], msg_share_url]
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
    #print(FRIEND_DIR)
    if not os.path.exists(FRIEND_DIR):
        os.mkdir(FRIEND_DIR)
    if not os.path.exists(GROUP_DIR):
        os.mkdir(GROUP_DIR)
    #################################
    itchat.auto_login(hotReload=True, exitCallback=after_logout)
    #Thread to keep connection
    timer1 = threading.Timer(60*6,keep_alive)
    timer1.start()

    ################################
    ## Download User info as JSON
    #排除自己
    friends = itchat.get_friends(update=True)[1:]
    #friends = ['1', '2', '3']
    user_meta = Login()
    user_info_dir = "{}/../user_info.json".format(ROOT_DIR)
    try:   
        print("用户信息已保存在:{} 目录下".format(user_info_dir))
        f = open(user_info_dir, 'r')
        os.remove(user_info_dir)
        for friend in friends:
            json_info = json.dumps(friend)
            with open(user_info_dir, "a", encoding = "utf-8") as f:
                f.write(json_info)
                f.write('\n')
            f.close()

    except FileNotFoundError:
        print("Retrieving Data from Wecaht... ")
        for friend in friends:
            json_info = json.dumps(friend)
            with open(user_info_dir, "a", encoding = "utf-8") as f:
                f.write(json_info)
                f.write('\n')
            f.close()

   
    time.sleep(2)
    itchat.run()
