#coding=utf-8
from User_API import *


'''
class Login:
    def write_to_file(self, user_dict):
        json_info = json.dumps(user_dict)
        with open('user_info.json', "a", encoding = "utf-8") as f:
            f.write(json_info)
            f.write('\n')
        f.close()

    def get_user_info(self):
        itchat.auto_login(hotReload=True)
        time.sleep(2)
        friends = itchat.get_friends(update=True)[1:]
        for friend in friends:
            self.write_to_file(friend)
'''

if __name__ == '__main__':
    login = Login()
    login.get_user_info()
    
    #itchat.send("文件助手你好哦", toUserName="filehelper")
    #itchat.run()