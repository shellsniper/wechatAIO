#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from cmd import Cmd
from colorama import Fore, Back
import signal
import json
import signal
import subprocess
import time
import os
import sys
import platform
import atexit
import shlex
import textwrap
import importlib
import itchat
from banner import *

PROMPT = Fore.GREEN + "wechatAIO" + Fore.RESET


class CLI(Cmd):
    #init
    prompt = PROMPT + '> '
    intro = the_intro()
    helper = the_helper()
    #print(intro)

    ###########################################################
    # Inti and Communication commands
    ###########################################################
    def do_login_keep(self, input):
        try:
            subprocess.call(['python3', 'libs/terminal.py', '--wait', 'python3', 'libs/after_login.py']) 
            print('Message monitoring in the opening terminal...')
            time.sleep(1)
        except OSError as e:
            print(e.strerror)
    def help_login_keep(self):
        print('Keeping wechat connection for further operations.')
    ###########################################################
    def do_user_meta(self, input):
        try:
            subprocess.call(['python3', 'libs/user_meta.py'])
            print('Processing...')
        except OSError as e:
            print(e.strerror)
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
            subprocess.call(['python3', 'libs/backup.py'])
        except OSError as e:
            print(e.strerror)

    def help_backup(self):
        print('backing up user_info.json to the backup folder.')
    ###########################################################
    def do_wordcloud(self, input):
        try:
            subprocess.call(['python3', 'libs/word_cloud.py'])
            print('checking the opening window, back after closing')
        except OSError as e:
            print(e.strerror)

    def help_wordcloud(self):
        print('generate a word cloud figure based on your friends signatures.')
    ###########################################################
    def do_wordcloud_cn(self, input):
        try:
            subprocess.call(['python3', 'libs/word_cloud_cn.py'])
            print('checking the opening window, back after closing')
        except OSError as e:
            print(e.strerror)

    def help_wordcloud_cn(self):
        print('generate a word cloud figure based on your friends signatures. 中文关键词模式')
    ###########################################################
    def do_gender(self, input):
        try:
            subprocess.call(['python3', 'libs/gender_analysis.py'])
            print('checking the opening window, back after closing')
        except OSError as e:
            print(e.strerror)

    def help_gender(self):
        print('generate gender distribution charts.')
    ###########################################################
    def do_geo(self, input):
        try:
            subprocess.call(['python3', 'libs/geo_chart.py'])
            print('checking the opening window, back after closing')
        except OSError as e:
            print(e.strerror)

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
    the_banner()
    original_sigint = signal.getsignal(signal.SIGINT)
    cli = CLI()
    cli.doc_header = cli.helper + "\n\nSupported Commands\n=============================="
    # cli.misc_header = '123'
    #cli.undoc_header = Fore.LIGHTYELLOW_EX + \
    #                   'Sub Modules \n===========================' + Fore.RESET
    cli.ruler = ''
    cli.cmdloop()
