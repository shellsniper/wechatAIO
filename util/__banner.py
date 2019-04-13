#!/usr/bin/env python
# encoding: utf-8
from colorama import init
init()
from colorama import Fore
import os, sys
root_dir = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from __prettytable import PrettyTable
#from libs.utility.prettytable import PrettyTable

# prettytable
def table(field, row):
    x = PrettyTable(header_style='upper', padding_width=0)
    x.field_names = field
    x.add_row(row)
    return x

def the_banner():
    banner_logo = Fore.LIGHTGREEN_EX + """
==================================================================\n
                      _           _            _____ ____  
                     | |         | |     /\   |_   _/ __ \ 
   __      _____  ___| |__   __ _| |_   /  \    | || |  | |
   \ \ /\ / / _ \/ __| '_ \ / _` | __| / /\ \   | || |  | |
    \ V  V /  __/ (__| | | | (_| | |_ / ____ \ _| || |__| |
     \_/\_/ \___|\___|_| |_|\__,_|\__/_/    \_\_____\____/ 
   
                                        ver: v1.3
                                        git: github.com/levoncf/
                                        gmail: levoncf@gmail.com
                                        blog: chenfengnie.com
==================================================================\n
    v1.3 Update:\n 1. Added auto_reply feature
                \n 2. Added chat log feature
                \n 3. Improve UI designs
                \n 4. Improve overall performance by adjusting subprocesses
                \n 5. fix bugs
                \n 6. Added delete and reset feature in main_CLI
==================================================================\n

""" + Fore.LIGHTGREEN_EX
    print(banner_logo)

def the_intro():
    intro = Fore.CYAN + "\
    Welcome!\n\
    If it is your first time, please run 'user_meta' or 'login_keep' first \nto retrieving data from your Wechat,\n\n\
    Note you will be asked to scan the QR Code by your wechat app, it is just like you login the wechat web app\n\
    \nand all DATA will be stored ON YOUR SIDE ONLY.\n\n\
    Hit ?/help to check all commands...\n\n" + Fore.RESET
    return intro

def the_helper():
    helper = Fore.CYAN + "Welcome! Here is the  ver1.0 of wechatAIO\n\n\
    If it is your first time, please run 'login' first to retrieving data from your Wechat \n\n\
    1. Core Commands:\n\
    ==============================================\n \
    user_meta\t\t log in and retrieving data by QR Code, log out when retrieved data\n \
    -------------------------------------------\n \
    login_keep\t\t Create an terminal subprocess, then login wechat, keep connection and monitoring messages\n \
    ==============================================\n\n \
    2. Statistic Commands:\n\
    ==============================================\n \
    backup\t\t backing up user info\n \
    geo\t\t generate location distribution chart\n \
    wordcloud\t\t generate a word cloud chart\n \
    wordcloud_cn\t\t generate a word cloud chart with CN only\n \
    gender\t\t generate a chart for gender Distribution\n \
    ==============================================\n\n \
    3. Messaging Commands:\n\
    ==============================================\n\
    send\t\t sending message to specific username\n\
    list_friends\t\t retrieving all friends' info\n\
    search_friends\t\t search friend's info\n\
    ==============================================\n\n \
    4. Utility Commands:\n\
    ==============================================\n \
    erase_logs\t\t deleting all stored data such as media files and logs\n \
    reset_all\t\t reset to factory settings, which means remove all sensitive data for you\n \
    clear\t\t clear the output\n \
    exit or q\t\t exit the CLI\n\n \
    Type ? to list full commands\n \
    And you can type help or ? <command> to get detail, e.g. ?login_keep\n \
    --------------------------------------------------" + Fore.RESET
    return helper

