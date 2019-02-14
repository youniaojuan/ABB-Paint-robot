#!/usr/bin/python
#coding:utf-8
# (C) Copyright 2012 ABB
#

"""Paint Protocol Client Implementation."""

import socket
import time
import sys
import os
import requests
import httplib
import json
import xml.dom.minidom
from requests.auth import HTTPDigestAuth
auth=HTTPDigestAuth('Default User','robotics')
headers = {'Content-Type':'application/x-www-form-urlencoded'}

def parse_serial(put):  
    '''''读取并解析xml文件 
       in_path: xml路径 
       return: ElementTree'''
    dom = xml.dom.minidom.parseString(put)
    root=dom.documentElement
    #print root.ELEMENT_NODE
    xmlNodeList = root.getElementsByTagName('span')
    #print xmlNodeList
    return xmlNodeList[0].childNodes[0].nodeValue

def outdata(resp):
    dom = xml.dom.minidom.parseString(resp)
    root=dom.documentElement
    xmlNodeList = root.getElementsByTagName('span')

    for item in xmlNodeList:
        #print str(item.childNodes[0].nodeValue)
        #if item.childNodes[0].nodeValue == '':
        #        item.childNodes[0].nodeValue = "0"
        if item.childNodes != []:
            print item.getAttribute("class") + "----" + str(item.childNodes[0].nodeValue)

def outdata_signal(resp):
    dom = xml.dom.minidom.parseString(resp)
    root=dom.documentElement
    xmlNodeList = root.getElementsByTagName('span')
    #print xmlNodeList
    list_item=["name","type","lvalue"]
    print "name" +" "*26 + "type" + " "*26 +"value"
    print "-" * 80
    for item in xmlNodeList:
        #print str(item.childNodes[0].nodeValue)
        #if item.childNodes[0].nodeValue == '':
        #        item.childNodes[0].nodeValue = "0"
        if item.getAttribute("class") in list_item[0:2]:            
            print str(item.childNodes[0].nodeValue)+" "*(30-len(item.childNodes[0].nodeValue)),
        if item.getAttribute("class") in list_item[2]:            
            print str(item.childNodes[0].nodeValue)+" "*(30-len(item.childNodes[0].nodeValue))            


def check_ip(ipaddr): 
        addr=ipaddr.strip().split('.')   
        #print addr 
        if len(addr) != 4:   
                print ("check ip address failed!")
                time.sleep(3)
                sys.exit() 
        for i in range(4): 
                try: 
                        addr[i]=int(addr[i])
                except: 
                        print "check ip address failed!"
                        time.sleep(3)
                        sys.exit() 
                if addr[i]<=255 and addr[i]>=0:
                        pass
                else: 
                        print "check ip address failed!"
                        time.sleep(3)
                        sys.exit() 
                i+=1
        else: 
                pass
                #print "check ip address success!"

if __name__ == "__main__":

        if len(sys.argv) < 2:

                ip=raw_input("ip:")
                check_ip(ip)
                url='http://'+ip+'/rw/paint/command?action=send'
                resp=requests.session()
                request_post='http://'+ip+'/rw/mastership/rapid?action=request'
                release_post='http://'+ip+'/rw/mastership/rapid?action=release'
                print "Commands:"
                print "quit                 - Terminate shell"
                print "cmd <COMMAND> [ARGS] - Send COMMAND with ARGS"
                while True:
                        cmd = raw_input("PP> ").split()
                        if len(cmd) == 0:
                                continue

                        if cmd[0] == 'quit' or cmd[0] == 'exit':
                                resp.post(release_post, auth=auth,headers = headers)
                                #self._client.abort()
                                exit()

                        elif cmd[0] ==  'cmd':
                                data={'number':''}
                                if len(cmd) >= 2:
                                        if len(cmd) >= 2:
                                                resp.post(request_post, auth=auth,headers = headers)
                                                #data['number']=' '.join(cmd[1:])
                                                arg=[0]*10
                                                cmd1 = cmd[1];
                                                if len(cmd)>=3:
                                                        for i in range(0,len(cmd)-2):
                                                                arg[i] = cmd[i+2] 
                                                for i in range(len(cmd)-2,10):
                                                        arg[i]="0"                                               
                                                data = "number=" + cmd1 + "&" + "arg01=" + arg[0] + "&" + "arg02=" + arg[1] + "&" + "arg03=" + arg[2] + "&" + "arg04=" + arg[3] + "&" + "arg05=" + arg[4] + "&" + "arg06=" + arg[5] + "&" + "arg07=" + arg[6] + "&" + "arg08=" + arg[7] + "&" + "arg09=" + arg[8] + "&" + "arg10=" + arg[9]
                                                r=resp.put(url,auth=auth,data=data)
                                                #print r.text
                                                serial=str(parse_serial(r.text))
                                                r= resp.post(release_post, auth=auth,headers = headers)
                                                #print serial
                                                #print type(serial)


                                                #print resp
                                                '''dom = xml.dom.minidom.parseString(r.text)
                                                root=dom.documentElement
                                                #print root.ELEMENT_NODE
                                                xmlNodeList = root.getElementsByTagName('span')
                                                #return xmlNodeList.childNodes[0].nodeValue
                                                serial=xmlNodeList.childNodes[0].nodeValue'''
                                                #serial="1"

                                                #url_cmdresult = 'http://'+ip+'/rw/paint/command/' + "1";
                                                url_cmdresult = 'http://'+ip+'/rw/paint/command/' + serial;
                                                time.sleep(2)
                                                response = resp.get(url_cmdresult);
                                                #print response.text
                                                #print type(response.text)
                                                #print response.content
                                                outdata(response.text)


                                                #self._client.command(0, cmd[1], ",".join(cmd[2:]))
                                        else:
                                                print "?"
                                                #self._client.command(0, cmd[1])
                        elif cmd[0] == 'speed':
                                speed_post='http://'+ip+'/rw/panel/speedratio?action=setspeedratio'
                                #print speed_post
                                resp.post(speed_post, auth=auth,headers = headers,data="speed-ratio="+cmd[1])
                        elif cmd[0] == 'restart':
                                switch = {
                                        "1": "restart",
                                        "2": "shutdown",
                                        "3": "xstart",
                                        "4": "istart",
                                        "5": "pstart",
                                        "6": "bstart"
                                        }
                                try:
                                        switch[cmd[1]]
                                except  KeyError as e:
                                        pass
                                restart_post='http://'+ip+'/ctrl'
                                #print speed_post
                                resp.post(restart_post, auth=auth,headers = headers,data="restart-mode="+switch[cmd[1]])
                        elif cmd[0] == "ls" :
                                signals_list='http://' + ip + '/rw/iosystem/signals'
                                r = resp.post(signals_list, auth=auth,headers = headers)
                                response = resp.get(signals_list)
                                #print response.text
                                outdata_signal(response.text)
                        elif cmd[0] == "nonmotion" :
                                switch = {
                                        "set":"ON",
                                        "reset":"OFF"
                                        }
                                try:
                                        switch[cmd[1]]
                                except  KeyError as e:
                                        pass
                                nonmotion_call = 'http://' +ip +'/rw/motionsystem/nonmotionexecution?action=set-mode'
                                nonmotion_state = 'http://' +ip +'/rw/motionsystem/nonmotionexecution'
                                resp.post(nonmotion_call,auth=auth,headers=headers,data="mode="+switch[cmd[1]])
                                response = resp.get(nonmotion_state)
                                outdata(response.text)
                        elif cmd[0] == "options":
                                system_options = 'http://' + ip +'/rw/system/options'
                                response = resp.get(system_options)
                                outdata(response.text)
                        elif cmd[0] == "backup":
                                backup_create = 'http://'+ip+'/ctrl/backup?action=backup'
                                resp.post(backup_create, auth=auth, headers=headers,data="backup=fileservice/$syspar/tempfolder")

                        else:
                                print "?"
        #elif len(sys.argv) == 2:
        #       shell = PPClientShell(sys.argv[1])
        else:
                exit()
        #       shell = PPClientShell(sys.argv[1], sys.argv[2])

        shell.run()

        sys.exit(0)

