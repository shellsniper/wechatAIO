#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cmd import Cmd
#from pathlib import Path
from colorama import init
from colorama import Fore, Back, Style
import signal
import json
import signal
import subprocess
import time
import os
import sys
#root_dir = str(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(root_dir)
#print(sys.path)
import platform
import atexit
import shlex
import textwrap
import importlib
import itchat
from util.__banner import *
from util.__Plat_define import *
from libs.User_API import *

PROMPT = Fore.MAGENTA + '(wechatAIO)' + Style.RESET_ALL
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class CLI(Cmd):
    #init
    init()
    #PROMPT = Fore.MAGENTA + '(wechatAIO)' + Style.RESET_ALL

    prompt = PROMPT + '> >_< > '
    intro = the_intro()
    helper = the_helper()
    #print(intro)

    ###########################################################
    # Inti and Communication commands
    ###########################################################
    def do_login_keep(self, input):
        plat = Plat_define()
        platform = plat.use_platform()
        print("Current OS: {}".format(platform))
        if platform == 'mac':
            terminal_dir = 'util/__terminal.py'
            login_keep_dir = 'libs/after_login.py'
            try:
                subprocess.call(['python3', terminal_dir, '--wait', 'python3', login_keep_dir]) 
                print('Message monitoring in the opening terminal...')
                time.sleep(1)
            except OSError as e:
                print(e.strerror)
        elif platform == 'windows':
            terminal_dir = DIR_PATH + '\\util\\__terminal.py'
            login_keep_dir = DIR_PATH + '\\libs\\after_login.py'
            print(login_keep_dir) 
            try:
                #subprocess.call(['python', terminal_dir, 'dir']) 
                subprocess.call('start /wait python3 {}'.format(login_keep_dir), shell=True)
                print('Message monitoring in the opening terminal...')
                time.sleep(1)
            except OSError as e:
                print(e.strerror)
        elif platform == 'linux':
            terminal_dir = 'util/__terminal.py'
            login_keep_dir =  'libs/after_login.py'
            try:
                subprocess.call(['python3', terminal_dir, '--wait', 'python3', login_keep_dir]) 
                print('Message monitoring in the opening terminal...')
                time.sleep(1)
            except OSError as e:
                print(e.strerror)
        else:
            print("Untested OS!")
       
    def help_login_keep(self):
        print('Keeping wechat connection for further operations.')
    ###########################################################
    def do_user_meta(self, input):         
        try:
            login = Login()
            login.get_user_info()
        except:
            print("retreving user_info failed!")
            
    def help_user_meta(self):
        print('login wechat to retrieving data.')
    ###########################################################
    def do_send(self, inputs):
        text = inputs.split(' ')[0]
        to_user = inputs.split(' ')[1]
        #print(inputs.split(' ')[1])
        itchat.auto_login(hotReload=True)
        itchat.send(text, toUserName = to_user)
        print('sent: {} to {}'.format(text, to_user))
    def help_send(self):
        print('send message to User or Group.')
    ###########################################################
    def do_list_friends(self, input):
        itchat.auto_login(hotReload=True)
        
        friends = itchat.get_friends(update=True)
        for f in range(1,len(friends)):#第0个好友是自己,不统计
            if friends[f]['RemarkName']: # 优先使用好友的备注名称，没有则使用昵称
                user_name = friends[f]['RemarkName']
            else:
                user_name = friends[f]['NickName']
            print(user_name)
        
    def help_list_friends(self):
        print('List all friends info.')    
    ###########################################################
    def do_search_friends(self, inputs):
        #print(inputs2)
        itchat.auto_login(hotReload=True)
        friend = itchat.search_friends(inputs)
        print(friend)
    def help_search_friends(self):
        print('search particular user.') 
    ###########################################################

    ###########################################################
    # Statistics Commands
    ###########################################################
    def do_backup(self, input):
        try:
            user_info = User_API()
            user_info.backup()
        except:
            print("backup failed!!")
    def help_backup(self):
        print('backing up user_info.json to the backup folder.')
    ###########################################################
    def do_wordcloud(self, input):
        user_info = User_API()
        user_info.word_cloud()

    def help_wordcloud(self):
        print('generate a word cloud figure based on your friends signatures.')
    ###########################################################
    def do_wordcloud_cn(self, input):
        try:
            user_info = User_API()
            user_info.word_cloud_cn()
            print('checking the opening window, back after closing')
        except OSError as e:
            pass
        except:
            print("generate wordcloud figure failed!!")
    def help_wordcloud_cn(self):
        print('generate a word cloud figure based on your friends signatures. 中文关键词模式')
    ###########################################################
    def do_gender(self, input):
        user_info = User_API()
        user_info.gender_chart()

    def help_gender(self):
        print('generate gender distribution charts.')
    ###########################################################
    def do_geo(self, input):
        user_info = User_API()
        user_info.state_chart()

    def help_geo(self):
        print('generate location distribution charts.') 
    ###########################################################

    #=========================================================
    # Operating command
    #=========================================================
    def do_exit(self, input):
        print(Fore.YELLOW + "Bye" + Fore.RESET)
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    #=========================================================
    #
    def do_clear(self, input):
        print(chr(27) + "[2J")
    def help_clear(self):
        print('clear all outputs.')
    #=========================================================
    def do_ls(self, input):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            print(f)
    def help_ls(self):
        print('Same as ls, list all files in current directory.')
    #=========================================================
    def do_dir_tree(self, input):
        startpath = str(os.path.dirname(os.path.abspath(__file__)))
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
    def help_dir_tree(self):
        print('show project directory/content tree.')
        
    #---------------------------------------------------------
    # can add more utility command below
    #---------------------------------------------------------
    def default(self, input):
        '''
        # func used to capture stdout in real-time
        def run_command_real_time(command):
            try:
                process = subprocess.Popen(
                    shlex.split(command), stdout=subprocess.PIPE)
                while True:
                    output = process.stdout.readline()
                    # output,error = process.communicate()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                rc = process.poll()
                return rc
            except OSError as e:
                # print("OSError > ",e.errno)
                print("OSError > {}".format(e.strerror))
                # print("OSError > ",e.filename)
                print(Fore.RED + "Note: Default Shell mode, please check you input" + Fore.RESET)
            except ValueError:
                pass
            except:
                print("Error > ", sys.exc_info()[0])
        '''
        if input == 'x' or input == 'q':
            return self.do_exit(input)
        #clear all    
        #elif input == 'clear':
            #print(chr(27) + "[2J")
        
        '''
        else:
            # "Run a shell command"
            print(
                Fore.GREEN + "\nRunning shell command in default: {}\n".format(input) + Fore.RESET)
            run_command_real_time(input)
        ’‘’
        '''
        

# main
if __name__ == '__main__':
    init()
    the_banner()
    original_sigint = signal.getsignal(signal.SIGINT)
    cli = CLI()
    cli.doc_header = cli.helper + "\n\nSupported Commands\n=============================="
    # cli.misc_header = '123'
    #cli.undoc_header = Fore.LIGHTYELLOW_EX + \
    #                   'Sub Modules \n===========================' + Fore.RESET
    cli.ruler = ''
    cli.cmdloop()
