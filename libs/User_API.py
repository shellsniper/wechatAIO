#!/usr/bin/env python3
#coding:utf-8
import datetime
import json
import os
import re
import shutil
import sys
root_dir = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
#print(sys.path)
import time

import itchat
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from utility.plat_definer import *
from wordcloud import STOPWORDS, ImageColorGenerator, WordCloud
import PIL.Image as Image
import numpy as np


plat = Plat_define()
platform = plat.use_platform()
if platform == 'mac':
    font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size = 10)
elif platform == 'windows':
    font = FontProperties(fname='C:\Windows\Fonts\simsun.ttf', size = 10)  
elif platform == 'linux':
    font = "none"
else:
    pass
#font = root_dir + "/../font/"
class Login:
    def write_to_file(self, user_dict):
        json_info = json.dumps(user_dict)
        with open('user_info.json', "a", encoding = "utf-8") as f:
            f.write(json_info)
            f.write('\n')
        f.close()

    def get_user_info(self):
        #itchat.auto_login(hotReload=True)
        itchat.auto_login()
        time.sleep(2)
        #排除自己
        friends = itchat.get_friends(update=True)[1:]
        try:
            f = open('user_info.json', 'r')
            os.remove('user_info.json')
            for friend in friends:
                self.write_to_file(friend)
        except FileNotFoundError:
            print("Retrieving Data from Wecaht... ")
            for friend in friends:
                self.write_to_file(friend)
        time.sleep(2)
        itchat.logout()

    def after_login(self):
        print("Log in success!")


    def after_logout(self):
        print("Log out success")


class User_API:
    file_name = 'user_info.json'
    #return gender dic {"male": #, "female": #, "other": #}
    def backup(self):
        if os.path.exists("user_info.json"):
            shutil.copyfile("user_info.json", "backup/user_info({}).json".format(str(datetime.datetime.now())))
            print('user_info({}) has been backed up in the /backup folder'.format(str(datetime.datetime.now())))
        else:
            print("user_info.json does not exist! Please run login command first")
             
    def gender_calc(self):
        gender = {"male": 0, "female": 0, "other": 0}
        with open(User_API.file_name, 'r') as f:
            for item in f.readlines():
                dic = json.loads(item)
                if dic['Sex'] == 1: #male
                    gender['male'] = gender['male'] + 1 
                elif dic['Sex'] == 2:
                    gender['female'] = gender['female'] + 1 
                else:
                    gender['other'] = gender['other'] + 1 
        return gender

    def gender_chart(self):
        gender_data = self.gender_calc()
        label =["Male", "Female", "Other"]
        sizes = [gender_data['male'], gender_data['female'], gender_data['other']]
        
        #Create Two plot to reflect gender distribution
        plt.subplot(1,2,1)
        x_pos = [i for i, _ in enumerate(label)]
        plt.bar(x_pos, sizes)
        plt.xticks(x_pos, label)
        plt.ylabel('numbers')
        plt.title("Gender Count")

        #pie chart
        plt.subplot(1,2,2)
        colors = ['lightskyblue', 'lightcoral', 'yellowgreen']
        #explode = (1 ,1 ,0)
        plt.pie(sizes, labels=label, colors = colors, autopct ='%1.1f%%', shadow = True)
        plt.title("Gender Distribution")
        plt.axis('equal')
        plt.show()
        

    def signature_proc(self):
        sig_dic = dict()
        sig_list = []
        with open(User_API.file_name, 'r') as f:
            for item in f.readlines():
                dic = json.loads(item)
                user_name = dic["NickName"]
                if dic['Signature'] is '':
                    sig_dic[user_name] = 'None'
                else:
                    sig_mod = dic['Signature'].strip().replace("emoji", "").replace("span","").replace("class","")
                    sig_dic[user_name] = sig_mod
                    sig_list.append(sig_mod)
        return sig_dic, sig_list
    
    #generate wordcloud no filter
    def word_cloud(self):
        masking = np.array(Image.open("{}{}".format(root_dir, "/../template/num.jpg")))
        #font_type_1 = ImageFont.truetype(fm.findfont(fm.FontProperties(family=combo.get())),18)
        _, word = self.signature_proc()
        word_proc = str(word)
        #print(word_proc)
        # 设置停用词 
        sw = set(STOPWORDS) 
        sw.add("1f512")
        sw.add("1f440")
        #sw.add("")
        wc = WordCloud(
            scale = 4,
            background_color = "white",
            mask = masking,
            max_words = 200,
            font_path = '/System/Library/Fonts/PingFang.ttc',
            #height = 1000,
            #width = 1000,
            stopwords = sw,
            max_font_size = 60,
            random_state = 20,
        )
        myword = wc.generate(word_proc)
        plt.imshow(myword)
        plt.axis('off')
        plt.show()
        wc.to_file('{}/../signature.png'.format(root_dir))
        print("signature.png has been stored at root dir...")

    #generate wordcloud filter EN, keep CN
    def word_cloud_cn(self):
        masking = np.array(Image.open("{}{}".format(root_dir, "/../template/num.jpg")))
        _, word = self.signature_proc()
        word_proc = str(word)

        #print(word_proc)
        # 设置停用词 
        sw = set(STOPWORDS) 
        sw.add("1f512")
        sw.add("1f440")
        #sw.add("")
        # 去掉英文，保留中文 
        resultword=re.sub("[A-Za-z0-9\!\%\[\]\,\.]", "", word_proc)
        wordlist_after_jieba = jieba.cut(resultword) 
        wl_space_split = " ".join(wordlist_after_jieba)

        wc = WordCloud(
            scale = 4,
            background_color = "white",
            mask = masking,
            max_words = 200,
            font_path = '/System/Library/Fonts/PingFang.ttc',
            #height = 1000,
            #width = 1000,
            stopwords = sw,
            max_font_size = 80,
            random_state = 20,
        )
        myword = wc.generate(wl_space_split)
        plt.imshow(myword)
        plt.axis('off')
        plt.show()
        wc.to_file('{}/../signature_cn.png'.format(root_dir))
        print("signature_cn.png has been stored at root dir...")

    #function to analyze friends' geo locaitons
    # @return list of city, list of state
    def geo_proc(self):
        city_list = []
        state_list = []
        with open(User_API.file_name, 'r') as f:
            for item in f.readlines():
                dic = json.loads(item, encoding = 'utf-8')
                state_list.append(dic['Province'])
                city_list.append(dic['City'])
        return city_list, state_list
    
    def state_chart(self):
        _, states = self.geo_proc()
        china =[]
        china_ctr = 0
        oversea = []
        oversea_ctr = 0
        undefined = 0
        #去重 统计数量
        for state in states:
            if state == '':
                undefined += 1
            elif self.if_contain_cn(state) is False:
                oversea.append(state)
                oversea_ctr +=1
            else:
                china.append(state)
                china_ctr +=1
        total_ctr = undefined + oversea_ctr + china_ctr
        china_dic = dict()
        oversea_dic = dict()
        for key in china:
            china_dic[key] = china_dic.get(key, 0) + 1
        for key in oversea:
            oversea_dic[key] = oversea_dic.get(key, 0) + 1
        #排序
        #china_dic = [(k, china_dic[k]) for k in sorted(china_dic, key = china_dic.get, reverse = True)]
        #oversea_dic = [(k, oversea_dic[k]) for k in sorted(oversea_dic, key = oversea_dic.get, reverse = True)]

        #print(oversea_dic)
        #setting = Settings()
        #setting.set_matplot_zh_font()
        plt.figure(figsize = (20,20))
        #Create Two plot to reflect gender distribution
        plt.subplot(1,2,1)
        plt.barh(range(len(china_dic)), list(china_dic.values()))
        plt.yticks(range(len(china_dic)), list(china_dic.keys()), FontProperties = font)
        plt.xlabel('numbers')
        plt.title("Total: {}，In China: {} / Undefined: {}".format(total_ctr, china_ctr, undefined), FontProperties = font)

        #pie chart
        plt.subplot(1,2,2)
        plt.barh(range(len(oversea_dic)), list(oversea_dic.values()))
        plt.yticks(range(len(oversea_dic)), list(oversea_dic.keys()), FontProperties = font)
        plt.xlabel('numbers')
        plt.title("Total: {}， Oversea: {} / Undefined: {}".format(total_ctr, oversea_ctr, undefined),FontProperties = font)
        plt.show()

    def if_contain_cn(self, strs):
        result = False
        for char in strs:
            if char >= u'\u4e00' and char <= u'\u9fa5':
                return True
            else:
                result == False
        return False
        
#if __name__ == "__main__":
    ## TEST
    #user = User_API()
    #user.gender_chart()
    #sig = user.signature_proc()
    #user.word_cloud()
    #user.state_chart()
