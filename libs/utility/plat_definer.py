#!/usr/bin/env python3
import platform

class Plat_define:
    def use_platform(self):
        sysstr = platform.system()
        os = ''
        if(sysstr =="Windows"):
            #print ("Windows")
            os = 'windows' 
        elif(sysstr == "Linux"):
            os = 'linux'
            #print ("Linux")
        elif(sysstr == 'Darwin'):
            os = 'mac'
            #print ("mac")
        else:
            os = 'other'
        return os

#UsePlatform()