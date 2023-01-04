"""Usage:
  --buildlist    <text> <height> <width> <list-height> <tag1> <item1> <status1>...
  --calendar     <text> <height> <width> <day> <month> <year>
  --checklist    <text> <height> <width> <list height> <tag1> <item1> <status1>...
  --dselect      <directory> <height> <width>
  --editbox      <file> <height> <width>
  --form         <text> <height> <width> <form height> <label1> <l_y1> <l_x1> <item1> <i_y1> <i_x1> <flen1> <ilen1>...
  --fselect      <filepath> <height> <width>
  --gauge        <text> <height> <width> [<percent>]
  --infobox      <text> <height> <width>
  --inputbox     <text> <height> <width> [<init>]
  --inputmenu    <text> <height> <width> <menu height> <tag1> <item1>...
  --menu         <text> <height> <width> <menu height> <tag1> <item1>...
  --mixedform    <text> <height> <width> <form height> <label1> <l_y1> <l_x1> <item1> <i_y1> <i_x1> <flen1> <ilen1> <itype>...
  --mixedgauge   <text> <height> <width> <percent> <tag1> <item1>...
  --msgbox       <text> <height> <width>
  --passwordbox  <text> <height> <width> [<init>]
  --passwordform <text> <height> <width> <form height> <label1> <l_y1> <l_x1> <item1> <i_y1> <i_x1> <flen1> <ilen1>...
  --pause        <text> <height> <width> <seconds>
  --prgbox       <text> <command> <height> <width>
  --programbox   <text> <height> <width>
  --progressbox  <text> <height> <width>
  --radiolist    <text> <height> <width> <list height> <tag1> <item1> <status1>...
  --rangebox     <text> <height> <width> <min-value> <max-value> <default-value>
  --tailbox      <file> <height> <width>
  --tailboxbg    <file> <height> <width>
  --textbox      <file> <height> <width>
  --timebox      <text> <height> <width> <hour> <minute> <second>
  --treeview     <text> <height> <width> <list-height> <tag1> <item1> <status1> <depth1>...
  --yesno        <text> <height> <width>
"""

commonOpt = """[--ascii-lines] [--aspect <ratio>] [--backtitle <backtitle>] [--beep]
  [--beep-after] [--begin <y> <x>] [--cancel-label <str>] [--clear]
  [--colors] [--column-separator <str>] [--cr-wrap] [--cursor-off-label]
  [--date-format <str>] [--default-button <str>] [--default-item <str>]
  [--defaultno] [--erase-on-exit] [--exit-label <str>] [--extra-button]
  [--extra-label <str>] [--help-button] [--help-label <str>]
  [--help-status] [--help-tags] [--hfile <str>] [--hline <str>]
  [--ignore] [--input-fd <fd>] [--insecure] [--item-help] [--keep-tite]
  [--keep-window] [--last-key] [--max-input <n>] [--no-cancel]
  [--no-collapse] [--no-cr-wrap] [--no-items] [--no-kill]
  [--no-label <str>] [--no-lines] [--no-mouse] [--no-nl-expand]
  [--no-ok] [--no-shadow] [--no-tags] [--nook] [--ok-label <str>]
  [--output-fd <fd>] [--output-separator <str>] [--print-maxsize]
  [--print-size] [--print-text-only <text> <height> <width>]
  [--print-text-size <text> <height> <width>] [--print-version] [--quoted]
  [--reorder] [--scrollbar] [--separate-output] [--separate-widget <str>]
  [--shadow] [--single-quoted] [--size-err] [--sleep <secs>] [--stderr]
  [--stdout] [--tab-correct] [--tab-len <n>] [--time-format <str>]
  [--timeout <secs>] [--title <title>] [--trace <file>] [--trim]
  [--version] [--visit-items] [--week-start <str>] [--yes-label <str>]"""


import socket
import pprint
import sys
import os
import json

class ArgumentOpt:
    def __init__(self, optStr):
        self._arg = optStr.replace("]","")
        self._allarg = self._arg.split()
        self._optvalues = []

    def isAnOption(self, opt):
        return self._allarg[0] == opt

    def parseOption(self, n):
        for i in range(1,len(self._allarg)):
                self._optvalues.append(sys.argv[i+n])

    def isTheCommand(self, cmd ):
        return False

    def getData(self):
        return {self._allarg[0]:self._optvalues}


class Argument:
    def __init__(self, descStr):
        self._descStr = descStr.split()
        self._command = self._descStr[0]
        self.result={}

    def isTheCommand(self, cmd ):
        return cmd == self._command

    def parseOtherArg(self, args,idx):
        n = 1
        for a in self._descStr[1:]:
            print(a)
            self.result[a.replace("<","").replace(">","")] = args[idx+n]
            n = n + 1

    def isAnOption(self, opt):
        return False

    def getData(self):
        return {"cmd":self._command, "options": self.result}



TCP_IP = '127.0.0.1'
TCP_PORT = 7005
BUFFER_SIZE = 20

if __name__ == '__main__':

    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.connect((TCP_IP, TCP_PORT))

    strdoc = (__doc__)
    args = []

    commonOpt = commonOpt.replace("\n","")
    for opt in commonOpt.split("["):
       if len(opt.strip())>0:
           args.append(ArgumentOpt(opt))

    for s in strdoc.split("\n"):
        if s == "Usage:" or len(s)==0:
            continue
        args.append(Argument(s))

    optToSend = []
    for n,s in enumerate(sys.argv):
        for a in args:
            if a.isAnOption(s):
                a.parseOption(n)
                optToSend.append(a.getData())
                print("OPT FOUND ")
            if a.isTheCommand(s):
                a.parseOtherArg(sys.argv,n)
                print(optToSend)
                print(json.dumps({"cmd":a.getData(),"options":optToSend}),"utf-8")
                so.sendall(bytes(json.dumps({"cmd":a.getData(),"options":optToSend}),"utf-8"))
                data = so.recv(BUFFER_SIZE)
                so.close()
                os._exit(int(data))
                print ('received data: ', data)

