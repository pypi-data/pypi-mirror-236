#!/usr/bin/env python
import warnings #line:7
import traceback #line:8
import ast #line:9
import re #line:10
import xlrd #line:11
import xlwt #line:12
import openpyxl #line:13
import pandas as pd #line:14
import numpy as np #line:15
import math #line:16
import tkinter as Tk #line:17
from tkinter import ttk #line:18
from tkinter import *#line:19
import tkinter .font as tkFont #line:20
from tkinter import filedialog ,dialog ,PhotoImage #line:21
from tkinter .messagebox import showinfo #line:22
from tkinter .scrolledtext import ScrolledText #line:23
import collections #line:24
from collections import Counter #line:25
import datetime #line:26
from datetime import datetime ,timedelta #line:27
from tkinter import END #line:28
import xlsxwriter #line:29
import os #line:30
import time #line:31
import threading #line:32
import pip #line:33
import matplotlib as plt #line:34
import requests #line:35
import random #line:36
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:38
from matplotlib .figure import Figure #line:39
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:40
from matplotlib .ticker import PercentFormatter #line:41
from tkinter import ttk ,Menu ,Frame ,Canvas ,StringVar ,LEFT ,RIGHT ,TOP ,BOTTOM ,BOTH ,Y ,X ,YES ,NO ,DISABLED ,END ,Button ,LabelFrame ,GROOVE ,Toplevel ,Label ,Entry ,Scrollbar ,Text ,filedialog ,dialog ,PhotoImage #line:42
global TT_ori #line:45
global TT_biaozhun #line:46
global TT_modex #line:47
global TT_ori_backup #line:48
global version_now #line:49
global usergroup #line:50
global setting_cfg #line:51
global csdir #line:52
TT_biaozhun ={}#line:53
TT_ori =""#line:54
TT_modex =0 #line:55
TT_ori_backup =""#line:56
version_now ="0.0.2"#line:57
usergroup ="用户组=0"#line:58
setting_cfg =""#line:59
csdir =str (os .path .dirname (__file__ ))+"\\"#line:61
#print (csdir )#line:62
def extract_zip_file (OOO0OO000O0OO0O00 ,O00OO00OO0O00OO0O ):#line:70
    import zipfile #line:72
    with zipfile .ZipFile (OOO0OO000O0OO0O00 ,'r')as O00OO0O0OO00O0OOO :#line:73
        for OO0O00OO0OOOO0OO0 in O00OO0O0OO00O0OOO .infolist ():#line:74
            OO0O00OO0OOOO0OO0 .filename =OO0O00OO0OOOO0OO0 .filename .encode ('cp437').decode ('gbk')#line:76
            O00OO0O0OO00O0OOO .extract (OO0O00OO0OOOO0OO0 ,O00OO00OO0O00OO0O )#line:77
def get_directory_path (O0OO0OO0OO0O00000 ):#line:83
    global csdir #line:85
    if not (os .path .isfile (os .path .join (O0OO0OO0OO0O00000 ,'规则文件.xls'))):#line:87
        extract_zip_file (csdir +"def.py",O0OO0OO0OO0O00000 )#line:92
    if O0OO0OO0OO0O00000 =="":#line:94
        quit ()#line:95
    return O0OO0OO0OO0O00000 #line:96
def convert_and_compare_dates (O0O000OOOO0OO000O ):#line:100
    import datetime #line:101
    OO00O000OO0000OOO =datetime .datetime .now ()#line:102
    try :#line:104
       O0O0OOOO0O0OO0OOO =datetime .datetime .strptime (str (int (int (O0O000OOOO0OO000O )/4 )),"%Y%m%d")#line:105
    except :#line:106
        print ("fail")#line:107
        return "已过期"#line:108
    if O0O0OOOO0O0OO0OOO >OO00O000OO0000OOO :#line:110
        return "未过期"#line:112
    else :#line:113
        return "已过期"#line:114
def read_setting_cfg ():#line:116
    global csdir #line:117
    if os .path .exists (csdir +'setting.cfg'):#line:119
        text .insert (END ,"已完成初始化\n")#line:120
        with open (csdir +'setting.cfg','r')as O00O00O0O0O0OOOOO :#line:121
            O0O00OO00OO000O0O =eval (O00O00O0O0O0OOOOO .read ())#line:122
    else :#line:123
        O000OO000OO0O0O0O =csdir +'setting.cfg'#line:125
        with open (O000OO000OO0O0O0O ,'w')as O00O00O0O0O0OOOOO :#line:126
            O00O00O0O0O0OOOOO .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:127
        text .insert (END ,"未初始化，正在初始化...\n")#line:128
        O0O00OO00OO000O0O =read_setting_cfg ()#line:129
    return O0O00OO00OO000O0O #line:130
def open_setting_cfg ():#line:133
    global csdir #line:134
    with open (csdir +"setting.cfg","r")as O0000000O0O0O0000 :#line:136
        O00O0O00OO00OOOO0 =eval (O0000000O0O0O0000 .read ())#line:138
    return O00O0O00OO00OOOO0 #line:139
def update_setting_cfg (OO00OO000O0000O0O ,OOO000OOOO00OOO0O ):#line:141
    global csdir #line:142
    with open (csdir +"setting.cfg","r")as O0OOOO0OOO000OOOO :#line:144
        OO00O000OO0OO00O0 =eval (O0OOOO0OOO000OOOO .read ())#line:146
    if OO00O000OO0OO00O0 [OO00OO000O0000O0O ]==0 or OO00O000OO0OO00O0 [OO00OO000O0000O0O ]=="11111180000808":#line:148
        OO00O000OO0OO00O0 [OO00OO000O0000O0O ]=OOO000OOOO00OOO0O #line:149
        with open (csdir +"setting.cfg","w")as O0OOOO0OOO000OOOO :#line:151
            O0OOOO0OOO000OOOO .write (str (OO00O000OO0OO00O0 ))#line:152
def generate_random_file ():#line:155
    O00O0O000OOOOOO00 =random .randint (200000 ,299999 )#line:157
    update_setting_cfg ("sidori",O00O0O000OOOOOO00 )#line:159
def display_random_number ():#line:161
    global csdir #line:162
    O0000O0O00OO0O000 =Toplevel ()#line:163
    O0000O0O00OO0O000 .title ("ID")#line:164
    OO00OO0O00O000000 =O0000O0O00OO0O000 .winfo_screenwidth ()#line:166
    OO00OO000OO0000OO =O0000O0O00OO0O000 .winfo_screenheight ()#line:167
    OOOO00OO00O0000O0 =80 #line:169
    O00OO00OO000000OO =70 #line:170
    O0O00OO0O0O0O00O0 =(OO00OO0O00O000000 -OOOO00OO00O0000O0 )/2 #line:172
    OO0OO000OOOO00OO0 =(OO00OO000OO0000OO -O00OO00OO000000OO )/2 #line:173
    O0000O0O00OO0O000 .geometry ("%dx%d+%d+%d"%(OOOO00OO00O0000O0 ,O00OO00OO000000OO ,O0O00OO0O0O0O00O0 ,OO0OO000OOOO00OO0 ))#line:174
    with open (csdir +"setting.cfg","r")as O0O0OOOO0O00000OO :#line:177
        O0OOO0O0O0000OOO0 =eval (O0O0OOOO0O00000OO .read ())#line:179
    OO00O000OOO0O00O0 =int (O0OOO0O0O0000OOO0 ["sidori"])#line:180
    O00O00OOO00OOO00O =OO00O000OOO0O00O0 *2 +183576 #line:181
    print (O00O00OOO00OOO00O )#line:183
    O00OO0OOOOO0000O0 =ttk .Label (O0000O0O00OO0O000 ,text =f"机器码: {OO00O000OOO0O00O0}")#line:185
    OO00OOO00OOO0O0OO =ttk .Entry (O0000O0O00OO0O000 )#line:186
    O00OO0OOOOO0000O0 .pack ()#line:189
    OO00OOO00OOO0O0OO .pack ()#line:190
    ttk .Button (O0000O0O00OO0O000 ,text ="验证",command =lambda :check_input (OO00OOO00OOO0O0OO .get (),O00O00OOO00OOO00O )).pack ()#line:194
def check_input (O00OO0OOO0O0O0000 ,O00O00OOOO0O000OO ):#line:196
    try :#line:200
        OO0OOOOOOO0OOOO0O =int (str (O00OO0OOO0O0O0000 )[0 :6 ])#line:201
        OOOO000OO0OOOO0O0 =convert_and_compare_dates (str (O00OO0OOO0O0O0000 )[6 :14 ])#line:202
    except :#line:203
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:204
        return 0 #line:205
    if OO0OOOOOOO0OOOO0O ==O00O00OOOO0O000OO and OOOO000OO0OOOO0O0 =="未过期":#line:207
        update_setting_cfg ("sidfinal",O00OO0OOO0O0O0000 )#line:208
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:209
        quit ()#line:210
    else :#line:211
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:212
def update_software (O0000OO0000O0OOO0 ):#line:216
    global version_now #line:218
    import pkg_resources #line:219
    try :#line:220
        OOO0O0OO0O0O0OOOO =pkg_resources .require ("treadmdr")[0 ].version #line:221
        version_now =OOO0O0OO0O0O0OOOO #line:222
    except :#line:223
        OOO0O0OO0O0O0OOOO =version_now #line:224
    O000OO00O00000OO0 =requests .get (f"https://pypi.org/pypi/{O0000OO0000O0OOO0}/json").json ()["info"]["version"]#line:225
    text .insert (END ,"当前版本为："+OOO0O0OO0O0O0OOOO )#line:226
    if O000OO00O00000OO0 >OOO0O0OO0O0O0OOOO :#line:227
        text .insert (END ,"\n最新版本为："+O000OO00O00000OO0 +",正在尝试自动更新....")#line:228
        pip .main (['install',O0000OO0000O0OOO0 ,'--upgrade'])#line:230
        text .insert (END ,"\n您可以开展工作。")#line:231
def Tread_TOOLS_fileopen (O0O000O0OOO0OO0O0 ):#line:235
    ""#line:236
    global TT_ori #line:237
    global TT_ori_backup #line:238
    global TT_biaozhun #line:239
    warnings .filterwarnings ('ignore')#line:240
    if O0O000O0OOO0OO0O0 ==0 :#line:242
        OO000000OOOO00O0O =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:243
        O000O000OOO00O0OO =[pd .read_excel (OO00O0OOO0OOOO0O0 ,header =0 ,sheet_name =0 )for OO00O0OOO0OOOO0O0 in OO000000OOOO00O0O ]#line:244
        OO000O00O000O0000 =pd .concat (O000O000OOO00O0OO ,ignore_index =True ).drop_duplicates ()#line:245
        try :#line:246
            OO000O00O000O0000 =OO000O00O000O0000 .loc [:,~TT_ori .columns .str .contains ("^Unnamed")]#line:247
        except :#line:248
            pass #line:249
        TT_ori_backup =OO000O00O000O0000 .copy ()#line:250
        TT_ori =Tread_TOOLS_CLEAN (OO000O00O000O0000 ).copy ()#line:251
        text .insert (END ,"\n原始数据导入成功，行数："+str (len (TT_ori )))#line:253
        text .insert (END ,"\n数据校验：\n")#line:254
        text .insert (END ,TT_ori )#line:255
        text .see (END )#line:256
    if O0O000O0OOO0OO0O0 ==1 :#line:258
        O0OOOO0OO0O000OOO =filedialog .askopenfilename (filetypes =[("XLS",".xls")])#line:259
        TT_biaozhun ["关键字表"]=pd .read_excel (O0OOOO0OO0O000OOO ,sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:260
        TT_biaozhun ["产品批号"]=pd .read_excel (O0OOOO0OO0O000OOO ,sheet_name ="产品批号",header =0 ,index_col =0 ,).reset_index ()#line:261
        TT_biaozhun ["事件发生月份"]=pd .read_excel (O0OOOO0OO0O000OOO ,sheet_name ="事件发生月份",header =0 ,index_col =0 ,).reset_index ()#line:262
        TT_biaozhun ["事件发生季度"]=pd .read_excel (O0OOOO0OO0O000OOO ,sheet_name ="事件发生季度",header =0 ,index_col =0 ,).reset_index ()#line:263
        TT_biaozhun ["规格"]=pd .read_excel (O0OOOO0OO0O000OOO ,sheet_name ="规格",header =0 ,index_col =0 ,).reset_index ()#line:264
        TT_biaozhun ["型号"]=pd .read_excel (O0OOOO0OO0O000OOO ,sheet_name ="型号",header =0 ,index_col =0 ,).reset_index ()#line:265
        TT_biaozhun ["设置"]=pd .read_excel (O0OOOO0OO0O000OOO ,sheet_name ="设置",header =0 ,index_col =0 ,).reset_index ()#line:266
        Tread_TOOLS_check (TT_ori ,TT_biaozhun ["关键字表"],0 )#line:267
        text .insert (END ,"\n标准导入成功，行数："+str (len (TT_biaozhun )))#line:268
        text .see (END )#line:269
def Tread_TOOLS_check (O0O0000O000O0O0O0 ,OOO0OO0OO0OOO00OO ,O000OOO00OOO0OO0O ):#line:271
        ""#line:272
        global TT_ori #line:273
        OOOO0O0OOO0OO0O00 =Tread_TOOLS_Countall (O0O0000O000O0O0O0 ).df_psur (OOO0OO0OO0OOO00OO )#line:274
        if O000OOO00OOO0OO0O ==0 :#line:276
            Tread_TOOLS_tree_Level_2 (OOOO0O0OOO0OO0O00 ,0 ,TT_ori .copy ())#line:278
        OOOO0O0OOO0OO0O00 ["核验"]=0 #line:281
        OOOO0O0OOO0OO0O00 .loc [(OOOO0O0OOO0OO0O00 ["关键字标记"].str .contains ("-其他关键字-",na =False )),"核验"]=OOOO0O0OOO0OO0O00 .loc [(OOOO0O0OOO0OO0O00 ["关键字标记"].str .contains ("-其他关键字-",na =False )),"总数量"]#line:282
        if OOOO0O0OOO0OO0O00 ["核验"].sum ()>0 :#line:283
            showinfo (title ="温馨提示",message ="存在未定义类型的报告"+str (OOOO0O0OOO0OO0O00 ["核验"].sum ())+"条，趋势分析可能会存在遗漏，建议修正该错误再进行下一步。")#line:284
def Tread_TOOLS_tree_Level_2 (OOOO00OOOOOO000OO ,O0000O000O0OO0000 ,O0000O00000OO00OO ,*O0OOO00OO00OO0000 ):#line:286
    ""#line:287
    global TT_ori_backup #line:289
    OOOOO0O0OOOO0O000 =OOOO00OOOOOO000OO .columns .values .tolist ()#line:291
    O0000O000O0OO0000 =0 #line:292
    O000O000OOOOO0000 =OOOO00OOOOOO000OO .loc [:]#line:293
    O00OO00O00OO00O00 =0 #line:297
    try :#line:298
        O0OO000OO00O00O00 =O0OOO00OO00OO0000 [0 ]#line:299
        O00OO00O00OO00O00 =1 #line:300
    except :#line:301
        pass #line:302
    OO00OO0OOOO0O0O0O =Toplevel ()#line:305
    OO00OO0OOOO0O0O0O .title ("报表查看器")#line:306
    O00O0O000OOO0O0OO =OO00OO0OOOO0O0O0O .winfo_screenwidth ()#line:307
    O00O0OO0O00O0O000 =OO00OO0OOOO0O0O0O .winfo_screenheight ()#line:309
    OOO0O000O0OO00OOO =1300 #line:311
    OOO00O0OO00O0OOOO =600 #line:312
    OOOOOO00O0OO000O0 =(O00O0O000OOO0O0OO -OOO0O000O0OO00OOO )/2 #line:314
    O00OO00OOOOOO0OOO =(O00O0OO0O00O0O000 -OOO00O0OO00O0OOOO )/2 #line:315
    OO00OO0OOOO0O0O0O .geometry ("%dx%d+%d+%d"%(OOO0O000O0OO00OOO ,OOO00O0OO00O0OOOO ,OOOOOO00O0OO000O0 ,O00OO00OOOOOO0OOO ))#line:316
    O0OOO0O0OO00OO000 =ttk .Frame (OO00OO0OOOO0O0O0O ,width =1300 ,height =20 )#line:317
    O0OOO0O0OO00OO000 .pack (side =BOTTOM )#line:318
    O0000OOO0000OOOO0 =ttk .Frame (OO00OO0OOOO0O0O0O ,width =1300 ,height =20 )#line:320
    O0000OOO0000OOOO0 .pack (side =TOP )#line:321
    if 1 >0 :#line:325
        O00000000OOOOO000 =Button (O0OOO0O0OO00OO000 ,text ="控制图(所有)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O000O000OOOOO0000 [:-1 ],O0OO000OO00O00O00 ,[OOOO000OO00O0O000 for OOOO000OO00O0O000 in O000O000OOOOO0000 .columns if (OOOO000OO00O0O000 not in [O0OO000OO00O00O00 ])],"关键字趋势图",100 ),)#line:335
        if O00OO00O00OO00O00 ==1 :#line:336
            O00000000OOOOO000 .pack (side =LEFT )#line:337
        O00000000OOOOO000 =Button (O0OOO0O0OO00OO000 ,text ="控制图(总数量)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O000O000OOOOO0000 [:-1 ],O0OO000OO00O00O00 ,[OO00O0OO00000000O for OO00O0OO00000000O in O000O000OOOOO0000 .columns if (OO00O0OO00000000O in ["该元素总数量"])],"关键字趋势图",100 ),)#line:347
        if O00OO00O00OO00O00 ==1 :#line:348
            O00000000OOOOO000 .pack (side =LEFT )#line:349
        OOO00000O00O0O000 =Button (O0OOO0O0OO00OO000 ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (O000O000OOOOO0000 ),)#line:359
        OOO00000O00O0O000 .pack (side =LEFT )#line:360
        OOO00000O00O0O000 =Button (O0OOO0O0OO00OO000 ,text ="发生率测算",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_fashenglv (O000O000OOOOO0000 ,O0OO000OO00O00O00 ),)#line:370
        if "关键字标记"not in O000O000OOOOO0000 .columns and "报告编码"not in O000O000OOOOO0000 .columns :#line:371
            if "对象"not in O000O000OOOOO0000 .columns :#line:372
                OOO00000O00O0O000 .pack (side =LEFT )#line:373
        OOO00000O00O0O000 =Button (O0OOO0O0OO00OO000 ,text ="直方图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_histbar (O000O000OOOOO0000 .copy ()),)#line:383
        if "对象"in O000O000OOOOO0000 .columns :#line:384
            OOO00000O00O0O000 .pack (side =LEFT )#line:385
        O00000OO00OOOOO00 =Button (O0OOO0O0OO00OO000 ,text ="行数:"+str (len (O000O000OOOOO0000 )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:395
        O00000OO00OOOOO00 .pack (side =LEFT )#line:396
    O00000OO0O0OOO000 =O000O000OOOOO0000 .values .tolist ()#line:399
    OO00O000OOO000OO0 =O000O000OOOOO0000 .columns .values .tolist ()#line:400
    OOO00000O0OOOOO00 =ttk .Treeview (O0000OOO0000OOOO0 ,columns =OO00O000OOO000OO0 ,show ="headings",height =45 )#line:401
    for OO0OOO00000OO0OOO in OO00O000OOO000OO0 :#line:403
        OOO00000O0OOOOO00 .heading (OO0OOO00000OO0OOO ,text =OO0OOO00000OO0OOO )#line:404
    for O000OOOO00O000OO0 in O00000OO0O0OOO000 :#line:405
        OOO00000O0OOOOO00 .insert ("","end",values =O000OOOO00O000OO0 )#line:406
    for OO0O00O0O0OOO0000 in OO00O000OOO000OO0 :#line:407
        OOO00000O0OOOOO00 .column (OO0O00O0O0OOO0000 ,minwidth =0 ,width =120 ,stretch =NO )#line:408
    OO0O0OO0O00OOO000 =Scrollbar (O0000OOO0000OOOO0 ,orient ="vertical")#line:410
    OO0O0OO0O00OOO000 .pack (side =RIGHT ,fill =Y )#line:411
    OO0O0OO0O00OOO000 .config (command =OOO00000O0OOOOO00 .yview )#line:412
    OOO00000O0OOOOO00 .config (yscrollcommand =OO0O0OO0O00OOO000 .set )#line:413
    O0OO0OO0O000000O0 =Scrollbar (O0000OOO0000OOOO0 ,orient ="horizontal")#line:415
    O0OO0OO0O000000O0 .pack (side =BOTTOM ,fill =X )#line:416
    O0OO0OO0O000000O0 .config (command =OOO00000O0OOOOO00 .xview )#line:417
    OOO00000O0OOOOO00 .config (yscrollcommand =OO0O0OO0O00OOO000 .set )#line:418
    def O0O0OO0OO0OOO0OO0 (O000OOO0OO0OOO000 ,OOO0OO000O00OOO00 ,O0O0OO00O0OO00O00 ):#line:420
        for O0O000OOOOOOOOO00 in OOO00000O0OOOOO00 .selection ():#line:423
            O0O0O00OOO00OOO0O =OOO00000O0OOOOO00 .item (O0O000OOOOOOOOO00 ,"values")#line:424
            OOO00OOO0O00OO0O0 =dict (zip (OOO0OO000O00OOO00 ,O0O0O00OOO00OOO0O ))#line:425
        if "该分类下各项计数"in OOO0OO000O00OOO00 :#line:427
            O00000OOOO000O0O0 =O0000O00000OO00OO .copy ()#line:428
            O00000OOOO000O0O0 ["关键字查找列"]=""#line:429
            for OO000OOOOOOOOO0O0 in TOOLS_get_list (OOO00OOO0O00OO0O0 ["查找位置"]):#line:430
                O00000OOOO000O0O0 ["关键字查找列"]=O00000OOOO000O0O0 ["关键字查找列"]+O00000OOOO000O0O0 [OO000OOOOOOOOO0O0 ].astype ("str")#line:431
            OOO0O0O00000O0OO0 =O00000OOOO000O0O0 .loc [O00000OOOO000O0O0 ["关键字查找列"].str .contains (OOO00OOO0O00OO0O0 ["关键字标记"],na =False )].copy ()#line:432
            OOO0O0O00000O0OO0 =OOO0O0O00000O0OO0 .loc [~OOO0O0O00000O0OO0 ["关键字查找列"].str .contains (OOO00OOO0O00OO0O0 ["排除值"],na =False )].copy ()#line:433
            Tread_TOOLS_tree_Level_2 (OOO0O0O00000O0OO0 ,0 ,OOO0O0O00000O0OO0 )#line:439
            return 0 #line:440
        if "报告编码"in OOO0OO000O00OOO00 :#line:442
            OO0OOO000O0OO00OO =Toplevel ()#line:443
            OOOOOOOOOOO00O000 =OO0OOO000O0OO00OO .winfo_screenwidth ()#line:444
            O0O0OOOOOO000OOOO =OO0OOO000O0OO00OO .winfo_screenheight ()#line:446
            OOOO0OO000OO0OOOO =800 #line:448
            OOOOOO00OO0O000O0 =600 #line:449
            OO000OOOOOOOOO0O0 =(OOOOOOOOOOO00O000 -OOOO0OO000OO0OOOO )/2 #line:451
            O00OOO00O0OO00OOO =(O0O0OOOOOO000OOOO -OOOOOO00OO0O000O0 )/2 #line:452
            OO0OOO000O0OO00OO .geometry ("%dx%d+%d+%d"%(OOOO0OO000OO0OOOO ,OOOOOO00OO0O000O0 ,OO000OOOOOOOOO0O0 ,O00OOO00O0OO00OOO ))#line:453
            OOO0000OOO0O0OO00 =ScrolledText (OO0OOO000O0OO00OO ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:457
            OOO0000OOO0O0OO00 .pack (padx =10 ,pady =10 )#line:458
            def O0OO0O00000O0O00O (event =None ):#line:459
                OOO0000OOO0O0OO00 .event_generate ('<<Copy>>')#line:460
            def OOO0O00O00000O000 (O000OOO00OOO000OO ,OO00OO0OO0OOO000O ):#line:461
                O0000OO00OO0O0OO0 =open (OO00OO0OO0OOO000O ,"w",encoding ='utf-8')#line:462
                O0000OO00OO0O0OO0 .write (O000OOO00OOO000OO )#line:463
                O0000OO00OO0O0OO0 .flush ()#line:465
                showinfo (title ="提示信息",message ="保存成功。")#line:466
            OO0OOO000O000O00O =Menu (OOO0000OOO0O0OO00 ,tearoff =False ,)#line:468
            OO0OOO000O000O00O .add_command (label ="复制",command =O0OO0O00000O0O00O )#line:469
            OO0OOO000O000O00O .add_command (label ="导出",command =lambda :thread_it (OOO0O00O00000O000 ,OOO0000OOO0O0OO00 .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =OOO00OOO0O00OO0O0 ["报告编码"],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:470
            def O0OO0O00OO0000O00 (O0000OOOOO0OOOOOO ):#line:472
                OO0OOO000O000O00O .post (O0000OOOOO0OOOOOO .x_root ,O0000OOOOO0OOOOOO .y_root )#line:473
            OOO0000OOO0O0OO00 .bind ("<Button-3>",O0OO0O00OO0000O00 )#line:474
            OO0OOO000O0OO00OO .title (OOO00OOO0O00OO0O0 ["报告编码"])#line:476
            for OO0OO000OO0O00O0O in range (len (OOO0OO000O00OOO00 )):#line:477
                OOO0000OOO0O0OO00 .insert (END ,OOO0OO000O00OOO00 [OO0OO000OO0O00O0O ])#line:479
                OOO0000OOO0O0OO00 .insert (END ,"：")#line:480
                OOO0000OOO0O0OO00 .insert (END ,OOO00OOO0O00OO0O0 [OOO0OO000O00OOO00 [OO0OO000OO0O00O0O ]])#line:481
                OOO0000OOO0O0OO00 .insert (END ,"\n")#line:482
            OOO0000OOO0O0OO00 .config (state =DISABLED )#line:483
            return 0 #line:484
        O00OOO00O0OO00OOO =O0O0O00OOO00OOO0O [1 :-1 ]#line:487
        OO000OOOOOOOOO0O0 =O0O0OO00O0OO00O00 .columns .tolist ()#line:489
        OO000OOOOOOOOO0O0 =OO000OOOOOOOOO0O0 [1 :-1 ]#line:490
        OO00OO0000OO0OOOO ={'关键词':OO000OOOOOOOOO0O0 ,'数量':O00OOO00O0OO00OOO }#line:492
        OO00OO0000OO0OOOO =pd .DataFrame .from_dict (OO00OO0000OO0OOOO )#line:493
        OO00OO0000OO0OOOO ["数量"]=OO00OO0000OO0OOOO ["数量"].astype (float )#line:494
        Tread_TOOLS_draw (OO00OO0000OO0OOOO ,"帕累托图",'关键词','数量',"帕累托图")#line:495
        return 0 #line:496
    OOO00000O0OOOOO00 .bind ("<Double-1>",lambda O0O0O000O0O0O0OOO :O0O0OO0OO0OOO0OO0 (O0O0O000O0O0O0OOO ,OO00O000OOO000OO0 ,O000O000OOOOO0000 ),)#line:504
    OOO00000O0OOOOO00 .pack ()#line:505
class Tread_TOOLS_Countall ():#line:507
    ""#line:508
    def __init__ (O0OO00O00OOO000OO ,O0000O00O00OO00O0 ):#line:509
        ""#line:510
        O0OO00O00OOO000OO .df =O0000O00O00OO00O0 #line:511
    def df_psur (O0O00OOO00OO0O000 ,O0O000O0000OO0OO0 ,*O0OO0OO00000O0O00 ):#line:513
        ""#line:514
        global TT_biaozhun #line:515
        OO0OO000O000OOOO0 =O0O00OOO00OO0O000 .df .copy ()#line:516
        OO00O0O000000O000 =len (OO0OO000O000OOOO0 .drop_duplicates ("报告编码"))#line:518
        OOO0OO0O0OOOOOOOO =O0O000O0000OO0OO0 .copy ()#line:521
        O0O00OO0O0OO0OOOO =TT_biaozhun ["设置"]#line:524
        if O0O00OO0O0OO0OOOO .loc [1 ,"值"]:#line:525
            OO00000O0OO0OO000 =O0O00OO0O0OO0OOOO .loc [1 ,"值"]#line:526
        else :#line:527
            OO00000O0OO0OO000 ="透视列"#line:528
            OO0OO000O000OOOO0 [OO00000O0OO0OO000 ]="未正确设置"#line:529
        O00OOOO0O0OOOOO00 =""#line:531
        OO00OO0OO0000O000 ="-其他关键字-"#line:532
        for O0O00O00000O0O000 ,O0O000000O00O0O00 in OOO0OO0O0OOOOOOOO .iterrows ():#line:533
            OO00OO0OO0000O000 =OO00OO0OO0000O000 +"|"+str (O0O000000O00O0O00 ["值"])#line:534
            O0OO00000OOOO0000 =O0O000000O00O0O00 #line:535
        O0OO00000OOOO0000 [3 ]=OO00OO0OO0000O000 #line:536
        O0OO00000OOOO0000 [2 ]="-其他关键字-|"#line:537
        OOO0OO0O0OOOOOOOO .loc [len (OOO0OO0O0OOOOOOOO )]=O0OO00000OOOO0000 #line:538
        OOO0OO0O0OOOOOOOO =OOO0OO0O0OOOOOOOO .reset_index (drop =True )#line:539
        OO0OO000O000OOOO0 ["关键字查找列"]=""#line:543
        for O0O0OOO000O0O000O in TOOLS_get_list (OOO0OO0O0OOOOOOOO .loc [0 ,"查找位置"]):#line:544
            OO0OO000O000OOOO0 ["关键字查找列"]=OO0OO000O000OOOO0 ["关键字查找列"]+OO0OO000O000OOOO0 [O0O0OOO000O0O000O ].astype ("str")#line:545
        OOOO0O0OO00O000O0 =[]#line:548
        for O0O00O00000O0O000 ,O0O000000O00O0O00 in OOO0OO0O0OOOOOOOO .iterrows ():#line:549
            O0O0OO0OOOOO00O00 =O0O000000O00O0O00 ["值"]#line:550
            O0O000O0O0OOO0O0O =OO0OO000O000OOOO0 .loc [OO0OO000O000OOOO0 ["关键字查找列"].str .contains (O0O0OO0OOOOO00O00 ,na =False )].copy ()#line:551
            if str (O0O000000O00O0O00 ["排除值"])!="nan":#line:552
                O0O000O0O0OOO0O0O =O0O000O0O0OOO0O0O .loc [~O0O000O0O0OOO0O0O ["关键字查找列"].str .contains (str (O0O000000O00O0O00 ["排除值"]),na =False )].copy ()#line:553
            O0O000O0O0OOO0O0O ["关键字标记"]=str (O0O0OO0OOOOO00O00 )#line:555
            O0O000O0O0OOO0O0O ["关键字计数"]=1 #line:556
            if len (O0O000O0O0OOO0O0O )>0 :#line:558
                OOO00O00OOOO0O0OO =pd .pivot_table (O0O000O0O0OOO0O0O .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns =OO00000O0OO0OO000 ,aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:568
                OOO00O00OOOO0O0OO =OOO00O00OOOO0O0OO [:-1 ]#line:569
                OOO00O00OOOO0O0OO .columns =OOO00O00OOOO0O0OO .columns .droplevel (0 )#line:570
                OOO00O00OOOO0O0OO =OOO00O00OOOO0O0OO .reset_index ()#line:571
                if len (OOO00O00OOOO0O0OO )>0 :#line:574
                    OOOO000000000OOOO =str (Counter (TOOLS_get_list0 ("use(关键字查找列).file",O0O000O0O0OOO0O0O ,1000 ))).replace ("Counter({","{")#line:575
                    OOOO000000000OOOO =OOOO000000000OOOO .replace ("})","}")#line:576
                    OOOO000000000OOOO =ast .literal_eval (OOOO000000000OOOO )#line:577
                    OOO00O00OOOO0O0OO .loc [0 ,"事件分类"]=str (TOOLS_get_list (OOO00O00OOOO0O0OO .loc [0 ,"关键字标记"])[0 ])#line:579
                    OOO00O00OOOO0O0OO .loc [0 ,"该分类下各项计数"]=str ({OO0O00O0OOO00OOO0 :OOO0O000OOO00O0OO for OO0O00O0OOO00OOO0 ,OOO0O000OOO00O0OO in OOOO000000000OOOO .items ()if STAT_judge_x (str (OO0O00O0OOO00OOO0 ),TOOLS_get_list (O0O0OO0OOOOO00O00 ))==1 })#line:580
                    OOO00O00OOOO0O0OO .loc [0 ,"其他分类各项计数"]=str ({OO00000OO0OO0OO0O :OO0O00O0OO0O0O000 for OO00000OO0OO0OO0O ,OO0O00O0OO0O0O000 in OOOO000000000OOOO .items ()if STAT_judge_x (str (OO00000OO0OO0OO0O ),TOOLS_get_list (O0O0OO0OOOOO00O00 ))!=1 })#line:581
                    OOO00O00OOOO0O0OO ["查找位置"]=O0O000000O00O0O00 ["查找位置"]#line:582
                    OOOO0O0OO00O000O0 .append (OOO00O00OOOO0O0OO )#line:585
        O00OOOO0O0OOOOO00 =pd .concat (OOOO0O0OO00O000O0 )#line:586
        O00OOOO0O0OOOOO00 =O00OOOO0O0OOOOO00 .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:591
        O00OOOO0O0OOOOO00 =O00OOOO0O0OOOOO00 .reset_index ()#line:592
        O00OOOO0O0OOOOO00 ["All占比"]=round (O00OOOO0O0OOOOO00 ["All"]/OO00O0O000000O000 *100 ,2 )#line:594
        O00OOOO0O0OOOOO00 =O00OOOO0O0OOOOO00 .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:595
        for O00OOOOO00000O0O0 ,OOOOO0OOO00OO00OO in OOO0OO0O0OOOOOOOO .iterrows ():#line:598
            O00OOOO0O0OOOOO00 .loc [(O00OOOO0O0OOOOO00 ["关键字标记"].astype (str )==str (OOOOO0OOO00OO00OO ["值"])),"排除值"]=OOOOO0OOO00OO00OO ["排除值"]#line:599
            O00OOOO0O0OOOOO00 .loc [(O00OOOO0O0OOOOO00 ["关键字标记"].astype (str )==str (OOOOO0OOO00OO00OO ["值"])),"查找位置"]=OOOOO0OOO00OO00OO ["查找位置"]#line:600
        O00OOOO0O0OOOOO00 ["排除值"]=O00OOOO0O0OOOOO00 ["排除值"].fillna ("-没有排除值-")#line:602
        O00OOOO0O0OOOOO00 ["报表类型"]="PSUR"#line:605
        del O00OOOO0O0OOOOO00 ["index"]#line:606
        try :#line:607
            del O00OOOO0O0OOOOO00 ["未正确设置"]#line:608
        except :#line:609
            pass #line:610
        return O00OOOO0O0OOOOO00 #line:611
    def df_find_all_keword_risk (OO00OOOO0OO00OOOO ,O0OOO00000OO0OO00 ,*O00OO0OOO0O00OO0O ):#line:614
        ""#line:615
        global TT_biaozhun #line:616
        O0O0OOOO0O000O0O0 =OO00OOOO0OO00OOOO .df .copy ()#line:618
        OOOOO00O000O00OOO =time .time ()#line:619
        OO0O0OOOO00O0OOOO =TT_biaozhun ["关键字表"].copy ()#line:621
        O0O00000OO00OOO0O ="作用对象"#line:623
        OO000O00000O0OOOO ="报告编码"#line:625
        O0000000OO0O0OOOO =O0O0OOOO0O000O0O0 .groupby ([O0O00000OO00OOO0O ]).agg (总数量 =(OO000O00000O0OOOO ,"nunique"),).reset_index ()#line:628
        OO0000OO000OOO000 =[O0O00000OO00OOO0O ,O0OOO00000OO0OO00 ]#line:630
        OO0O0O0O0O0OOO00O =O0O0OOOO0O000O0O0 .groupby (OO0000OO000OOO000 ).agg (该元素总数量 =(O0O00000OO00OOO0O ,"count"),).reset_index ()#line:634
        OOO00OO000OO0O0OO =[]#line:636
        OO0OO0OO0000O00O0 =0 #line:640
        OO0O0OOOO00OO0O0O =int (len (O0000000OO0O0OOOO ))#line:641
        for OO0OOO0O000O000OO ,OOOOO00O00O00O0O0 in zip (O0000000OO0O0OOOO [O0O00000OO00OOO0O ].values ,O0000000OO0O0OOOO ["总数量"].values ):#line:642
            OO0OO0OO0000O00O0 +=1 #line:643
            O0OO000O00OO00OO0 =O0O0OOOO0O000O0O0 [(O0O0OOOO0O000O0O0 [O0O00000OO00OOO0O ]==OO0OOO0O000O000OO )].copy ()#line:644
            for OOOOOO00000OO00O0 ,OO0000OOOOOOOOO00 ,OO0OOO00OOOOO0OO0 in zip (OO0O0OOOO00O0OOOO ["值"].values ,OO0O0OOOO00O0OOOO ["查找位置"].values ,OO0O0OOOO00O0OOOO ["排除值"].values ):#line:646
                    O00OOOOOO0O00O000 =O0OO000O00OO00OO0 .copy ()#line:647
                    OO0OO00O00O0OOO0O =TOOLS_get_list (OOOOOO00000OO00O0 )[0 ]#line:648
                    O00OOOOOO0O00O000 ["关键字查找列"]=""#line:650
                    for OO0OOO00O000OO0OO in TOOLS_get_list (OO0000OOOOOOOOO00 ):#line:651
                        O00OOOOOO0O00O000 ["关键字查找列"]=O00OOOOOO0O00O000 ["关键字查找列"]+O00OOOOOO0O00O000 [OO0OOO00O000OO0OO ].astype ("str")#line:652
                    O00OOOOOO0O00O000 .loc [O00OOOOOO0O00O000 ["关键字查找列"].str .contains (OOOOOO00000OO00O0 ,na =False ),"关键字"]=OO0OO00O00O0OOO0O #line:654
                    if str (OO0OOO00OOOOO0OO0 )!="nan":#line:659
                        O00OOOOOO0O00O000 =O00OOOOOO0O00O000 .loc [~O00OOOOOO0O00O000 ["关键字查找列"].str .contains (OO0OOO00OOOOO0OO0 ,na =False )].copy ()#line:660
                    if (len (O00OOOOOO0O00O000 ))<1 :#line:662
                        continue #line:664
                    O00OOO0O00O00OOOO =STAT_find_keyword_risk (O00OOOOOO0O00O000 ,[O0O00000OO00OOO0O ,"关键字"],"关键字",O0OOO00000OO0OO00 ,int (OOOOO00O00O00O0O0 ))#line:666
                    if len (O00OOO0O00O00OOOO )>0 :#line:667
                        O00OOO0O00O00OOOO ["关键字组合"]=OOOOOO00000OO00O0 #line:668
                        O00OOO0O00O00OOOO ["排除值"]=OO0OOO00OOOOO0OO0 #line:669
                        O00OOO0O00O00OOOO ["关键字查找列"]=OO0000OOOOOOOOO00 #line:670
                        OOO00OO000OO0O0OO .append (O00OOO0O00O00OOOO )#line:671
        if len (OOO00OO000OO0O0OO )<1 :#line:674
            showinfo (title ="错误信息",message ="该注册证号未检索到任何关键字，规则制定存在缺陷。")#line:675
            return 0 #line:676
        O0O0OOO000O0OOOO0 =pd .concat (OOO00OO000OO0O0OO )#line:677
        O0O0OOO000O0OOOO0 =pd .merge (O0O0OOO000O0OOOO0 ,OO0O0O0O0O0OOO00O ,on =OO0000OO000OOO000 ,how ="left")#line:680
        O0O0OOO000O0OOOO0 ["关键字数量比例"]=round (O0O0OOO000O0OOOO0 ["计数"]/O0O0OOO000O0OOOO0 ["该元素总数量"],2 )#line:681
        O0O0OOO000O0OOOO0 =O0O0OOO000O0OOOO0 .reset_index (drop =True )#line:683
        if len (O0O0OOO000O0OOOO0 )>0 :#line:686
            O0O0OOO000O0OOOO0 ["风险评分"]=0 #line:687
            O0O0OOO000O0OOOO0 ["报表类型"]="keyword_findrisk"+O0OOO00000OO0OO00 #line:688
            O0O0OOO000O0OOOO0 .loc [(O0O0OOO000O0OOOO0 ["计数"]>=3 ),"风险评分"]=O0O0OOO000O0OOOO0 ["风险评分"]+3 #line:689
            O0O0OOO000O0OOOO0 .loc [(O0O0OOO000O0OOOO0 ["计数"]>=(O0O0OOO000O0OOOO0 ["数量均值"]+O0O0OOO000O0OOOO0 ["数量标准差"])),"风险评分"]=O0O0OOO000O0OOOO0 ["风险评分"]+1 #line:690
            O0O0OOO000O0OOOO0 .loc [(O0O0OOO000O0OOOO0 ["计数"]>=O0O0OOO000O0OOOO0 ["数量CI"]),"风险评分"]=O0O0OOO000O0OOOO0 ["风险评分"]+1 #line:691
            O0O0OOO000O0OOOO0 .loc [(O0O0OOO000O0OOOO0 ["关键字数量比例"]>0.5 )&(O0O0OOO000O0OOOO0 ["计数"]>=3 ),"风险评分"]=O0O0OOO000O0OOOO0 ["风险评分"]+1 #line:692
            O0O0OOO000O0OOOO0 =O0O0OOO000O0OOOO0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:694
        O00000OO0OOO00OOO =O0O0OOO000O0OOOO0 .columns .to_list ()#line:704
        OOOO00OO00O00OOO0 =O00000OO0OOO00OOO [O00000OO0OOO00OOO .index ("关键字")+1 ]#line:705
        O0000O000OO00000O =pd .pivot_table (O0O0OOO000O0OOOO0 ,index =OOOO00OO00O00OOO0 ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:716
        O0000O000OO00000O .columns =O0000O000OO00000O .columns .droplevel (0 )#line:717
        O0000O000OO00000O =pd .merge (O0000O000OO00000O ,O0O0OOO000O0OOOO0 [[OOOO00OO00O00OOO0 ,"该元素总数量"]].drop_duplicates (OOOO00OO00O00OOO0 ),on =[OOOO00OO00O00OOO0 ],how ="left")#line:720
        del O0000O000OO00000O ["All"]#line:722
        O0000O000OO00000O .iloc [-1 ,-1 ]=O0000O000OO00000O ["该元素总数量"].sum (axis =0 )#line:723
        print ("耗时：",(time .time ()-OOOOO00O000O00OOO ))#line:725
        return O0000O000OO00000O #line:728
def Tread_TOOLS_bar (OO0O0O00O0OO0OOOO ):#line:736
         ""#line:737
         O0OO00O00OO00O0OO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:738
         O0000O00O0OOOOO0O =[pd .read_excel (OOOO0O0O0OOO00000 ,header =0 ,sheet_name =0 )for OOOO0O0O0OOO00000 in O0OO00O00OO00O0OO ]#line:739
         OOO000O0000000OO0 =pd .concat (O0000O00O0OOOOO0O ,ignore_index =True )#line:740
         O0O0O00O0OOOO0O00 =pd .pivot_table (OOO000O0000000OO0 ,index ="对象",columns ="关键词",values =OO0O0O00O0OO0OOOO ,aggfunc ="sum",fill_value ="0",margins =True ,dropna =False ,).reset_index ()#line:750
         del O0O0O00O0OOOO0O00 ["All"]#line:752
         O0O0O00O0OOOO0O00 =O0O0O00O0OOOO0O00 [:-1 ]#line:753
         Tread_TOOLS_tree_Level_2 (O0O0O00O0OOOO0O00 ,0 ,0 )#line:755
def Tread_TOOLS_analysis (O0OO0O0O0O00OO00O ):#line:760
    ""#line:761
    import datetime #line:762
    global TT_ori #line:763
    global TT_biaozhun #line:764
    if len (TT_ori )==0 :#line:766
       showinfo (title ="提示",message ="您尚未导入原始数据。")#line:767
       return 0 #line:768
    if len (TT_biaozhun )==0 :#line:769
       showinfo (title ="提示",message ="您尚未导入规则。")#line:770
       return 0 #line:771
    O0O00000OO00OO0OO =TT_biaozhun ["设置"]#line:773
    TT_ori ["作用对象"]=""#line:774
    for OO0000000O0O00O00 in TOOLS_get_list (O0O00000OO00OO0OO .loc [0 ,"值"]):#line:775
        TT_ori ["作用对象"]=TT_ori ["作用对象"]+"-"+TT_ori [OO0000000O0O00O00 ].fillna ("未填写").astype ("str")#line:776
    O0OO0O0O000O0O000 =Toplevel ()#line:779
    O0OO0O0O000O0O000 .title ("单品分析")#line:780
    OO0O0OOOOO000000O =O0OO0O0O000O0O000 .winfo_screenwidth ()#line:781
    OO0O0O000OOO0OOOO =O0OO0O0O000O0O000 .winfo_screenheight ()#line:783
    OOO00O00O0OO00O00 =580 #line:785
    OOO00O00O00OOOOOO =80 #line:786
    OOOO0000O0000O000 =(OO0O0OOOOO000000O -OOO00O00O0OO00O00 )/1.7 #line:788
    OOO0000O00O0O0000 =(OO0O0O000OOO0OOOO -OOO00O00O00OOOOOO )/2 #line:789
    O0OO0O0O000O0O000 .geometry ("%dx%d+%d+%d"%(OOO00O00O0OO00O00 ,OOO00O00O00OOOOOO ,OOOO0000O0000O000 ,OOO0000O00O0O0000 ))#line:790
    OOO0O00OO0OOO0000 =Label (O0OO0O0O000O0O000 ,text ="作用对象：")#line:793
    OOO0O00OO0OOO0000 .grid (row =1 ,column =0 ,sticky ="w")#line:794
    OO000OOOOOOO000O0 =StringVar ()#line:795
    OOO0O0OO0O000O000 =ttk .Combobox (O0OO0O0O000O0O000 ,width =25 ,height =10 ,state ="readonly",textvariable =OO000OOOOOOO000O0 )#line:798
    OOO0O0OO0O000O000 ["values"]=list (set (TT_ori ["作用对象"].to_list ()))#line:799
    OOO0O0OO0O000O000 .current (0 )#line:800
    OOO0O0OO0O000O000 .grid (row =1 ,column =1 )#line:801
    OO0OO0OO00000O0O0 =Label (O0OO0O0O000O0O000 ,text ="分析对象：")#line:803
    OO0OO0OO00000O0O0 .grid (row =1 ,column =2 ,sticky ="w")#line:804
    OOO00OO0O0OOOO0O0 =StringVar ()#line:807
    OO0O000OO0000OOO0 =ttk .Combobox (O0OO0O0O000O0O000 ,width =15 ,height =10 ,state ="readonly",textvariable =OOO00OO0O0OOOO0O0 )#line:810
    OO0O000OO0000OOO0 ["values"]=["事件发生月份","事件发生季度","产品批号","型号","规格"]#line:811
    OO0O000OO0000OOO0 .current (0 )#line:813
    OO0O000OO0000OOO0 .grid (row =1 ,column =3 )#line:814
    O0000O0OO00OO000O =Label (O0OO0O0O000O0O000 ,text ="事件发生起止时间：")#line:819
    O0000O0OO00OO000O .grid (row =2 ,column =0 ,sticky ="w")#line:820
    O0O0OOOOO0000OO0O =Entry (O0OO0O0O000O0O000 ,width =10 )#line:822
    O0O0OOOOO0000OO0O .insert (0 ,min (TT_ori ["事件发生日期"].dt .date ))#line:823
    O0O0OOOOO0000OO0O .grid (row =2 ,column =1 ,sticky ="w")#line:824
    O0O00O0O0OO0O0O00 =Entry (O0OO0O0O000O0O000 ,width =10 )#line:826
    O0O00O0O0OO0O0O00 .insert (0 ,max (TT_ori ["事件发生日期"].dt .date ))#line:827
    O0O00O0O0OO0O0O00 .grid (row =2 ,column =2 ,sticky ="w")#line:828
    O0OO0OO0000OO00OO =Button (O0OO0O0O000O0O000 ,text ="原始查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OOO0O0OO0O000O000 .get (),OO0O000OO0000OOO0 .get (),O0O0OOOOO0000OO0O .get (),O0O00O0O0OO0O0O00 .get (),1 ))#line:838
    O0OO0OO0000OO00OO .grid (row =3 ,column =2 ,sticky ="w")#line:839
    O0OO0OO0000OO00OO =Button (O0OO0O0O000O0O000 ,text ="分类查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OOO0O0OO0O000O000 .get (),OO0O000OO0000OOO0 .get (),O0O0OOOOO0000OO0O .get (),O0O00O0O0OO0O0O00 .get (),0 ))#line:849
    O0OO0OO0000OO00OO .grid (row =3 ,column =3 ,sticky ="w")#line:850
    O0OO0OO0000OO00OO =Button (O0OO0O0O000O0O000 ,text ="趋势分析",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OOO0O0OO0O000O000 .get (),OO0O000OO0000OOO0 .get (),O0O0OOOOO0000OO0O .get (),O0O00O0O0OO0O0O00 .get (),2 ))#line:860
    O0OO0OO0000OO00OO .grid (row =3 ,column =1 ,sticky ="w")#line:861
def Tread_TOOLS_doing (OO00OOO000O0O0O0O ,OOO0OOOOO000OOOOO ,O0O0O0O000O0O0000 ,OO00OOOOOOOOO000O ,O0OOOOOO00OO000OO ,O00O0O0000OO00O0O ):#line:863
    ""#line:864
    global TT_biaozhun #line:865
    OO00OOO000O0O0O0O =OO00OOO000O0O0O0O [(OO00OOO000O0O0O0O ["作用对象"]==OOO0OOOOO000OOOOO )].copy ()#line:866
    OO00OOOOOOOOO000O =pd .to_datetime (OO00OOOOOOOOO000O )#line:868
    O0OOOOOO00OO000OO =pd .to_datetime (O0OOOOOO00OO000OO )#line:869
    OO00OOO000O0O0O0O =OO00OOO000O0O0O0O [((OO00OOO000O0O0O0O ["事件发生日期"]>=OO00OOOOOOOOO000O )&(OO00OOO000O0O0O0O ["事件发生日期"]<=O0OOOOOO00OO000OO ))]#line:870
    text .insert (END ,"\n数据数量："+str (len (OO00OOO000O0O0O0O )))#line:871
    text .see (END )#line:872
    if O00O0O0000OO00O0O ==0 :#line:874
        Tread_TOOLS_check (OO00OOO000O0O0O0O ,TT_biaozhun ["关键字表"],0 )#line:875
        return 0 #line:876
    if O00O0O0000OO00O0O ==1 :#line:877
        Tread_TOOLS_tree_Level_2 (OO00OOO000O0O0O0O ,1 ,OO00OOO000O0O0O0O )#line:878
        return 0 #line:879
    if len (OO00OOO000O0O0O0O )<1 :#line:880
        showinfo (title ="错误信息",message ="没有符合筛选条件的报告。")#line:881
        return 0 #line:882
    Tread_TOOLS_check (OO00OOO000O0O0O0O ,TT_biaozhun ["关键字表"],1 )#line:883
    Tread_TOOLS_tree_Level_2 (Tread_TOOLS_Countall (OO00OOO000O0O0O0O ).df_find_all_keword_risk (O0O0O0O000O0O0000 ),1 ,0 ,O0O0O0O000O0O0000 )#line:886
def STAT_countx (O0O0OO0O000O000OO ):#line:896
    ""#line:897
    return O0O0OO0O000O000OO .value_counts ().to_dict ()#line:898
def STAT_countpx (OOOOOOOOO0O0O0OO0 ,O0O00OO000O0OOOOO ):#line:900
    ""#line:901
    return len (OOOOOOOOO0O0O0OO0 [(OOOOOOOOO0O0O0OO0 ==O0O00OO000O0OOOOO )])#line:902
def STAT_countnpx (OOO0OOO0O000O0OO0 ,OO00OO0OOO00O0O00 ):#line:904
    ""#line:905
    return len (OOO0OOO0O000O0OO0 [(OOO0OOO0O000O0OO0 not in OO00OO0OOO00O0O00 )])#line:906
def STAT_get_max (OO0OO00000O00OO00 ):#line:908
    ""#line:909
    return OO0OO00000O00OO00 .value_counts ().max ()#line:910
def STAT_get_mean (OOOOOO0O0O00OOOO0 ):#line:912
    ""#line:913
    return round (OOOOOO0O0O00OOOO0 .value_counts ().mean (),2 )#line:914
def STAT_get_std (O0OOOO0O0OO0O000O ):#line:916
    ""#line:917
    return round (O0OOOO0O0OO0O000O .value_counts ().std (ddof =1 ),2 )#line:918
def STAT_get_95ci (O0O0O000O0O0OO0O0 ):#line:920
    ""#line:921
    return round (np .percentile (O0O0O000O0O0OO0O0 .value_counts (),97.5 ),2 )#line:922
def STAT_get_mean_std_ci (O00OO00OOOO0000OO ,O0O00OOOOOOOOO00O ):#line:924
    ""#line:925
    warnings .filterwarnings ("ignore")#line:926
    OOOOO0OO0OOO0O0OO =TOOLS_strdict_to_pd (str (O00OO00OOOO0000OO ))["content"].values /O0O00OOOOOOOOO00O #line:927
    O0OO0O00O00O0000O =round (OOOOO0OO0OOO0O0OO .mean (),2 )#line:928
    O0OO0OO00OO000O0O =round (OOOOO0OO0OOO0O0OO .std (ddof =1 ),2 )#line:929
    OO00O00O00O000OOO =round (np .percentile (OOOOO0OO0OOO0O0OO ,97.5 ),2 )#line:930
    return pd .Series ((O0OO0O00O00O0000O ,O0OO0OO00OO000O0O ,OO00O00O00O000OOO ))#line:931
def STAT_findx_value (OOO000000OOOOO0O0 ,O0O0OOO0O0O000OO0 ):#line:933
    ""#line:934
    warnings .filterwarnings ("ignore")#line:935
    OO00OOOOO000OO00O =TOOLS_strdict_to_pd (str (OOO000000OOOOO0O0 ))#line:936
    O0OO00OOOOO0OO0O0 =OO00OOOOO000OO00O .where (OO00OOOOO000OO00O ["index"]==str (O0O0OOO0O0O000OO0 ))#line:938
    print (O0OO00OOOOO0OO0O0 )#line:939
    return O0OO00OOOOO0OO0O0 #line:940
def STAT_judge_x (O00O00000OO0O0O0O ,O0O0OOO0O0O0OO00O ):#line:942
    ""#line:943
    for O00OO0O0OOO000OOO in O0O0OOO0O0O0OO00O :#line:944
        if O00O00000OO0O0O0O .find (O00OO0O0OOO000OOO )>-1 :#line:945
            return 1 #line:946
def STAT_basic_risk (OO00O0O00000O00O0 ,O0O0OO0000000OOO0 ,O0O0O0OO00OO0O0O0 ,OOO00OO00OO0OOOOO ,O0OOOO0O0OOOO00O0 ):#line:949
    ""#line:950
    OO00O0O00000O00O0 ["风险评分"]=0 #line:951
    OO00O0O00000O00O0 .loc [((OO00O0O00000O00O0 [O0O0OO0000000OOO0 ]>=3 )&(OO00O0O00000O00O0 [O0O0O0OO00OO0O0O0 ]>=1 ))|(OO00O0O00000O00O0 [O0O0OO0000000OOO0 ]>=5 ),"风险评分"]=OO00O0O00000O00O0 ["风险评分"]+5 #line:952
    OO00O0O00000O00O0 .loc [(OO00O0O00000O00O0 [O0O0O0OO00OO0O0O0 ]>=3 ),"风险评分"]=OO00O0O00000O00O0 ["风险评分"]+1 #line:953
    OO00O0O00000O00O0 .loc [(OO00O0O00000O00O0 [OOO00OO00OO0OOOOO ]>=1 ),"风险评分"]=OO00O0O00000O00O0 ["风险评分"]+10 #line:954
    OO00O0O00000O00O0 ["风险评分"]=OO00O0O00000O00O0 ["风险评分"]+OO00O0O00000O00O0 [O0OOOO0O0OOOO00O0 ]/100 #line:955
    return OO00O0O00000O00O0 #line:956
def STAT_find_keyword_risk (OOO000000O00OOO00 ,OO0O000O0OOOO00O0 ,OOOOO000OO0OOO0OO ,O0O000O0OO0000OOO ,OOO0OO0OOO00O0OO0 ):#line:960
        ""#line:961
        OOOOOO00OO0000OO0 =OOO000000O00OOO00 .groupby (OO0O000O0OOOO00O0 ).agg (证号关键字总数量 =(OOOOO000OO0OOO0OO ,"count"),包含元素个数 =(O0O000O0OO0000OOO ,"nunique"),包含元素 =(O0O000O0OO0000OOO ,STAT_countx ),).reset_index ()#line:966
        OOO0000000O0OO0O0 =OO0O000O0OOOO00O0 .copy ()#line:968
        OOO0000000O0OO0O0 .append (O0O000O0OO0000OOO )#line:969
        O0OOO000OO0O0O0O0 =OOO000000O00OOO00 .groupby (OOO0000000O0OO0O0 ).agg (计数 =(O0O000O0OO0000OOO ,"count"),).reset_index ()#line:972
        OO0OOO0O000000OOO =OOO0000000O0OO0O0 .copy ()#line:975
        OO0OOO0O000000OOO .remove ("关键字")#line:976
        O00O0O000OO000OO0 =OOO000000O00OOO00 .groupby (OO0OOO0O000000OOO ).agg (该元素总数 =(O0O000O0OO0000OOO ,"count"),).reset_index ()#line:979
        O0OOO000OO0O0O0O0 ["证号总数"]=OOO0OO0OOO00O0OO0 #line:981
        OO0O00OOOO0OO000O =pd .merge (O0OOO000OO0O0O0O0 ,OOOOOO00OO0000OO0 ,on =OO0O000O0OOOO00O0 ,how ="left")#line:982
        if len (OO0O00OOOO0OO000O )>0 :#line:984
            OO0O00OOOO0OO000O [['数量均值','数量标准差','数量CI']]=OO0O00OOOO0OO000O .包含元素 .apply (lambda O0OO0O000000O00O0 :STAT_get_mean_std_ci (O0OO0O000000O00O0 ,1 ))#line:985
        return OO0O00OOOO0OO000O #line:986
def STAT_find_risk (OO0O000OO000O0000 ,OOOOOO000O00O0000 ,OOO00000OO00OO000 ,O000000OOOOO0000O ):#line:992
        ""#line:993
        O000O00OO00O0O0O0 =OO0O000OO000O0000 .groupby (OOOOOO000O00O0000 ).agg (证号总数量 =(OOO00000OO00OO000 ,"count"),包含元素个数 =(O000000OOOOO0000O ,"nunique"),包含元素 =(O000000OOOOO0000O ,STAT_countx ),均值 =(O000000OOOOO0000O ,STAT_get_mean ),标准差 =(O000000OOOOO0000O ,STAT_get_std ),CI上限 =(O000000OOOOO0000O ,STAT_get_95ci ),).reset_index ()#line:1001
        O0O0OO0000O00O00O =OOOOOO000O00O0000 .copy ()#line:1003
        O0O0OO0000O00O00O .append (O000000OOOOO0000O )#line:1004
        O000O0OO0O00O000O =OO0O000OO000O0000 .groupby (O0O0OO0000O00O00O ).agg (计数 =(O000000OOOOO0000O ,"count"),严重伤害数 =("伤害",lambda OOOO0000000O0O00O :STAT_countpx (OOOO0000000O0O00O .values ,"严重伤害")),死亡数量 =("伤害",lambda O0OO0O0O0OO0OOO00 :STAT_countpx (O0OO0O0O0OO0OOO00 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:1011
        O0OO0OO0O0O000O0O =pd .merge (O000O0OO0O00O000O ,O000O00OO00O0O0O0 ,on =OOOOOO000O00O0000 ,how ="left")#line:1013
        O0OO0OO0O0O000O0O ["风险评分"]=0 #line:1015
        O0OO0OO0O0O000O0O ["报表类型"]="dfx_findrisk"+O000000OOOOO0000O #line:1016
        O0OO0OO0O0O000O0O .loc [((O0OO0OO0O0O000O0O ["计数"]>=3 )&(O0OO0OO0O0O000O0O ["严重伤害数"]>=1 )|(O0OO0OO0O0O000O0O ["计数"]>=5 )),"风险评分"]=O0OO0OO0O0O000O0O ["风险评分"]+5 #line:1017
        O0OO0OO0O0O000O0O .loc [(O0OO0OO0O0O000O0O ["计数"]>=(O0OO0OO0O0O000O0O ["均值"]+O0OO0OO0O0O000O0O ["标准差"])),"风险评分"]=O0OO0OO0O0O000O0O ["风险评分"]+1 #line:1018
        O0OO0OO0O0O000O0O .loc [(O0OO0OO0O0O000O0O ["计数"]>=O0OO0OO0O0O000O0O ["CI上限"]),"风险评分"]=O0OO0OO0O0O000O0O ["风险评分"]+1 #line:1019
        O0OO0OO0O0O000O0O .loc [(O0OO0OO0O0O000O0O ["严重伤害数"]>=3 )&(O0OO0OO0O0O000O0O ["风险评分"]>=7 ),"风险评分"]=O0OO0OO0O0O000O0O ["风险评分"]+1 #line:1020
        O0OO0OO0O0O000O0O .loc [(O0OO0OO0O0O000O0O ["死亡数量"]>=1 ),"风险评分"]=O0OO0OO0O0O000O0O ["风险评分"]+10 #line:1021
        O0OO0OO0O0O000O0O ["风险评分"]=O0OO0OO0O0O000O0O ["风险评分"]+O0OO0OO0O0O000O0O ["单位个数"]/100 #line:1022
        O0OO0OO0O0O000O0O =O0OO0OO0O0O000O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:1023
        return O0OO0OO0O0O000O0O #line:1025
def TOOLS_get_list (O00OO0O0OOO0OOO00 ):#line:1027
    ""#line:1028
    O00OO0O0OOO0OOO00 =str (O00OO0O0OOO0OOO00 )#line:1029
    O0O00O00OO00OOOO0 =[]#line:1030
    O0O00O00OO00OOOO0 .append (O00OO0O0OOO0OOO00 )#line:1031
    O0O00O00OO00OOOO0 =",".join (O0O00O00OO00OOOO0 )#line:1032
    O0O00O00OO00OOOO0 =O0O00O00OO00OOOO0 .split ("|")#line:1033
    OOO0OOOO0O0000OOO =O0O00O00OO00OOOO0 [:]#line:1034
    O0O00O00OO00OOOO0 =list (set (O0O00O00OO00OOOO0 ))#line:1035
    O0O00O00OO00OOOO0 .sort (key =OOO0OOOO0O0000OOO .index )#line:1036
    return O0O00O00OO00OOOO0 #line:1037
def TOOLS_get_list0 (O00O00OOOO0OOO00O ,OO0000OOOOOO00O0O ,*O0O00OO0OO0OO0O00 ):#line:1039
    ""#line:1040
    O00O00OOOO0OOO00O =str (O00O00OOOO0OOO00O )#line:1041
    if pd .notnull (O00O00OOOO0OOO00O ):#line:1043
        try :#line:1044
            if "use("in str (O00O00OOOO0OOO00O ):#line:1045
                OOO0000O00OOO0O0O =O00O00OOOO0OOO00O #line:1046
                O0OOOO000OOO00O0O =re .compile (r"[(](.*?)[)]",re .S )#line:1047
                O00OO00OO0000O00O =re .findall (O0OOOO000OOO00O0O ,OOO0000O00OOO0O0O )#line:1048
                O000000O00O0O0000 =[]#line:1049
                if ").list"in O00O00OOOO0OOO00O :#line:1050
                    O0OO00OO0O00OO0OO ="配置表/"+str (O00OO00OO0000O00O [0 ])+".xls"#line:1051
                    OOOO00O00O00O0000 =pd .read_excel (O0OO00OO0O00OO0OO ,sheet_name =O00OO00OO0000O00O [0 ],header =0 ,index_col =0 ).reset_index ()#line:1054
                    OOOO00O00O00O0000 ["检索关键字"]=OOOO00O00O00O0000 ["检索关键字"].astype (str )#line:1055
                    O000000O00O0O0000 =OOOO00O00O00O0000 ["检索关键字"].tolist ()+O000000O00O0O0000 #line:1056
                if ").file"in O00O00OOOO0OOO00O :#line:1057
                    O000000O00O0O0000 =OO0000OOOOOO00O0O [O00OO00OO0000O00O [0 ]].astype (str ).tolist ()+O000000O00O0O0000 #line:1059
                try :#line:1062
                    if "报告类型-新的"in OO0000OOOOOO00O0O .columns :#line:1063
                        O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1064
                        O000000O00O0O0000 =O000000O00O0O0000 .split (";")#line:1065
                        O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1066
                        O000000O00O0O0000 =O000000O00O0O0000 .split ("；")#line:1067
                        O000000O00O0O0000 =[O0000O0OOO000OOOO .replace ("（严重）","")for O0000O0OOO000OOOO in O000000O00O0O0000 ]#line:1068
                        O000000O00O0O0000 =[OO0000OOO00OO0OO0 .replace ("（一般）","")for OO0000OOO00OO0OO0 in O000000O00O0O0000 ]#line:1069
                except :#line:1070
                    pass #line:1071
                O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1074
                O000000O00O0O0000 =O000000O00O0O0000 .split ("、")#line:1075
                O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1076
                O000000O00O0O0000 =O000000O00O0O0000 .split ("，")#line:1077
                O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1078
                O000000O00O0O0000 =O000000O00O0O0000 .split (",")#line:1079
                O0O00O0O00OO00O00 =O000000O00O0O0000 [:]#line:1081
                try :#line:1082
                    if O0O00OO0OO0OO0O00 [0 ]==1000 :#line:1083
                      pass #line:1084
                except :#line:1085
                      O000000O00O0O0000 =list (set (O000000O00O0O0000 ))#line:1086
                O000000O00O0O0000 .sort (key =O0O00O0O00OO00O00 .index )#line:1087
            else :#line:1089
                O00O00OOOO0OOO00O =str (O00O00OOOO0OOO00O )#line:1090
                O000000O00O0O0000 =[]#line:1091
                O000000O00O0O0000 .append (O00O00OOOO0OOO00O )#line:1092
                O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1093
                O000000O00O0O0000 =O000000O00O0O0000 .split ("、")#line:1094
                O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1095
                O000000O00O0O0000 =O000000O00O0O0000 .split ("，")#line:1096
                O000000O00O0O0000 =",".join (O000000O00O0O0000 )#line:1097
                O000000O00O0O0000 =O000000O00O0O0000 .split (",")#line:1098
                O0O00O0O00OO00O00 =O000000O00O0O0000 [:]#line:1100
                try :#line:1101
                    if O0O00OO0OO0OO0O00 [0 ]==1000 :#line:1102
                      O000000O00O0O0000 =list (set (O000000O00O0O0000 ))#line:1103
                except :#line:1104
                      pass #line:1105
                O000000O00O0O0000 .sort (key =O0O00O0O00OO00O00 .index )#line:1106
                O000000O00O0O0000 .sort (key =O0O00O0O00OO00O00 .index )#line:1107
        except ValueError2 :#line:1109
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:1110
            return False #line:1111
    return O000000O00O0O0000 #line:1113
def TOOLS_strdict_to_pd (O0O00O0O00O0O0OO0 ):#line:1114
    ""#line:1115
    return pd .DataFrame .from_dict (eval (O0O00O0O00O0O0OO0 ),orient ="index",columns =["content"]).reset_index ()#line:1116
def Tread_TOOLS_view_dict (O00OO0000OOO0O000 ,OO00O0O0O0OO00OOO ):#line:1118
    ""#line:1119
    O0OOOOO0OOOOOOO00 =Toplevel ()#line:1120
    O0OOOOO0OOOOOOO00 .title ("查看数据")#line:1121
    O0OOOOO0OOOOOOO00 .geometry ("700x500")#line:1122
    O0O0O000O0OO0OOO0 =Scrollbar (O0OOOOO0OOOOOOO00 )#line:1124
    O0O00O00OOOO0O0OO =Text (O0OOOOO0OOOOOOO00 ,height =100 ,width =150 )#line:1125
    O0O0O000O0OO0OOO0 .pack (side =RIGHT ,fill =Y )#line:1126
    O0O00O00OOOO0O0OO .pack ()#line:1127
    O0O0O000O0OO0OOO0 .config (command =O0O00O00OOOO0O0OO .yview )#line:1128
    O0O00O00OOOO0O0OO .config (yscrollcommand =O0O0O000O0OO0OOO0 .set )#line:1129
    if OO00O0O0O0OO00OOO ==1 :#line:1130
        O0O00O00OOOO0O0OO .insert (END ,O00OO0000OOO0O000 )#line:1132
        O0O00O00OOOO0O0OO .insert (END ,"\n\n")#line:1133
        return 0 #line:1134
    for OOOOOO0O0O0O0OO00 in range (len (O00OO0000OOO0O000 )):#line:1135
        O0O00O00OOOO0O0OO .insert (END ,O00OO0000OOO0O000 .iloc [OOOOOO0O0O0O0OO00 ,0 ])#line:1136
        O0O00O00OOOO0O0OO .insert (END ,":")#line:1137
        O0O00O00OOOO0O0OO .insert (END ,O00OO0000OOO0O000 .iloc [OOOOOO0O0O0O0OO00 ,1 ])#line:1138
        O0O00O00OOOO0O0OO .insert (END ,"\n\n")#line:1139
def Tread_TOOLS_fashenglv (O00O0O0O000O00O0O ,OO0OOOOOOOOO00OO0 ):#line:1142
    global TT_biaozhun #line:1143
    O00O0O0O000O00O0O =pd .merge (O00O0O0O000O00O0O ,TT_biaozhun [OO0OOOOOOOOO00OO0 ],on =[OO0OOOOOOOOO00OO0 ],how ="left").reset_index (drop =True )#line:1144
    OO000OOOOOO0O00O0 =O00O0O0O000O00O0O ["使用次数"].mean ()#line:1146
    O00O0O0O000O00O0O ["使用次数"]=O00O0O0O000O00O0O ["使用次数"].fillna (int (OO000OOOOOO0O00O0 ))#line:1147
    O0000O000OO0O0000 =O00O0O0O000O00O0O ["使用次数"][:-1 ].sum ()#line:1148
    O00O0O0O000O00O0O .iloc [-1 ,-1 ]=O0000O000OO0O0000 #line:1149
    O0O0OOOO00OO0O00O =[OOO0OOOO0000OO0O0 for OOO0OOOO0000OO0O0 in O00O0O0O000O00O0O .columns if (OOO0OOOO0000OO0O0 not in ["使用次数",OO0OOOOOOOOO00OO0 ])]#line:1150
    for OOO0OOOOOO00O00OO ,O00O000OO0000OOO0 in O00O0O0O000O00O0O .iterrows ():#line:1151
        for OOOO00O00O000OOOO in O0O0OOOO00OO0O00O :#line:1152
            O00O0O0O000O00O0O .loc [OOO0OOOOOO00O00OO ,OOOO00O00O000OOOO ]=int (O00O000OO0000OOO0 [OOOO00O00O000OOOO ])/int (O00O000OO0000OOO0 ["使用次数"])#line:1153
    del O00O0O0O000O00O0O ["使用次数"]#line:1154
    Tread_TOOLS_tree_Level_2 (O00O0O0O000O00O0O ,1 ,1 ,OO0OOOOOOOOO00OO0 )#line:1155
def TOOLS_save_dict (OO00OO000O0OOO00O ):#line:1157
    ""#line:1158
    OO000000000000OOO =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="【排序后的原始数据】",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1164
    try :#line:1165
        OO00OO000O0OOO00O ["详细描述T"]=OO00OO000O0OOO00O ["详细描述T"].astype (str )#line:1166
    except :#line:1167
        pass #line:1168
    try :#line:1169
        OO00OO000O0OOO00O ["报告编码"]=OO00OO000O0OOO00O ["报告编码"].astype (str )#line:1170
    except :#line:1171
        pass #line:1172
    try :#line:1173
        O0O0000OOO000O00O =re .search ("\【(.*?)\】",OO000000000000OOO )#line:1174
        OO00OO000O0OOO00O ["对象"]=O0O0000OOO000O00O .group (1 )#line:1175
    except :#line:1176
        pass #line:1177
    OO0O00OO0OO000OO0 =pd .ExcelWriter (OO000000000000OOO ,engine ="xlsxwriter")#line:1178
    OO00OO000O0OOO00O .to_excel (OO0O00OO0OO000OO0 ,sheet_name ="字典数据")#line:1179
    OO0O00OO0OO000OO0 .close ()#line:1180
    showinfo (title ="提示",message ="文件写入成功。")#line:1181
def Tread_TOOLS_DRAW_histbar (OO00OOO0O00O00000 ):#line:1185
    ""#line:1186
    OO000OO0O000OOO00 =Toplevel ()#line:1189
    OO000OO0O000OOO00 .title ("直方图")#line:1190
    O00OOOOOOOOOOOOOO =ttk .Frame (OO000OO0O000OOO00 ,height =20 )#line:1191
    O00OOOOOOOOOOOOOO .pack (side =TOP )#line:1192
    OO0O0O000OO0OO00O =Figure (figsize =(12 ,6 ),dpi =100 )#line:1194
    OOO0O00000O00O00O =FigureCanvasTkAgg (OO0O0O000OO0OO00O ,master =OO000OO0O000OOO00 )#line:1195
    OOO0O00000O00O00O .draw ()#line:1196
    OOO0O00000O00O00O .get_tk_widget ().pack (expand =1 )#line:1197
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1199
    plt .rcParams ['axes.unicode_minus']=False #line:1200
    OO0OO0O0OOO000OO0 =NavigationToolbar2Tk (OOO0O00000O00O00O ,OO000OO0O000OOO00 )#line:1202
    OO0OO0O0OOO000OO0 .update ()#line:1203
    OOO0O00000O00O00O .get_tk_widget ().pack ()#line:1204
    OOO00OOO00OOOOOO0 =OO0O0O000OO0OO00O .add_subplot (111 )#line:1206
    OOO00OOO00OOOOOO0 .set_title ("直方图")#line:1208
    OOO00OOOOO0O00O00 =OO00OOO0O00O00000 .columns .to_list ()#line:1210
    OOO00OOOOO0O00O00 .remove ("对象")#line:1211
    O0O00OO0O0O0OO00O =np .arange (len (OOO00OOOOO0O00O00 ))#line:1212
    for OO00O00000O0OO0OO in OOO00OOOOO0O00O00 :#line:1216
        OO00OOO0O00O00000 [OO00O00000O0OO0OO ]=OO00OOO0O00O00000 [OO00O00000O0OO0OO ].astype (float )#line:1217
    OO00OOO0O00O00000 ['数据']=OO00OOO0O00O00000 [OOO00OOOOO0O00O00 ].values .tolist ()#line:1219
    O0000000O000O00OO =0 #line:1220
    for O0OOOOOO00OOOO00O ,O00O0OOO000O00OO0 in OO00OOO0O00O00000 .iterrows ():#line:1221
        OOO00OOO00OOOOOO0 .bar ([OOOOOO0O00O0O00O0 +O0000000O000O00OO for OOOOOO0O00O0O00O0 in O0O00OO0O0O0OO00O ],OO00OOO0O00O00000 .loc [O0OOOOOO00OOOO00O ,'数据'],label =OOO00OOOOO0O00O00 ,width =0.1 )#line:1222
        for O0OOO0OO0O0O000O0 ,OO0O0O0OO00O00O00 in zip ([OOO000O0OOOO0O0OO +O0000000O000O00OO for OOO000O0OOOO0O0OO in O0O00OO0O0O0OO00O ],OO00OOO0O00O00000 .loc [O0OOOOOO00OOOO00O ,'数据']):#line:1225
           OOO00OOO00OOOOOO0 .text (O0OOO0OO0O0O000O0 -0.015 ,OO0O0O0OO00O00O00 +0.07 ,str (int (OO0O0O0OO00O00O00 )),color ='black',size =8 )#line:1226
        O0000000O000O00OO =O0000000O000O00OO +0.1 #line:1228
    OOO00OOO00OOOOOO0 .set_xticklabels (OO00OOO0O00O00000 .columns .to_list (),rotation =-90 ,fontsize =8 )#line:1230
    OOO00OOO00OOOOOO0 .legend (OO00OOO0O00O00000 ["对象"])#line:1234
    OOO0O00000O00O00O .draw ()#line:1237
def Tread_TOOLS_DRAW_make_risk_plot (O0OOO00OO00O00O00 ,O00O00000OO0OOO0O ,O000000O0O00OOOO0 ,OO000OO0000O00O00 ,OO0O0O000O0OOO000 ):#line:1239
    ""#line:1240
    O0O00OO0O00000000 =Toplevel ()#line:1243
    O0O00OO0O00000000 .title (OO000OO0000O00O00 )#line:1244
    O00O0OOOO0000O000 =ttk .Frame (O0O00OO0O00000000 ,height =20 )#line:1245
    O00O0OOOO0000O000 .pack (side =TOP )#line:1246
    O0O00OOO0OOOOOO0O =Figure (figsize =(12 ,6 ),dpi =100 )#line:1248
    OOO0OO000O0000O00 =FigureCanvasTkAgg (O0O00OOO0OOOOOO0O ,master =O0O00OO0O00000000 )#line:1249
    OOO0OO000O0000O00 .draw ()#line:1250
    OOO0OO000O0000O00 .get_tk_widget ().pack (expand =1 )#line:1251
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1253
    plt .rcParams ['axes.unicode_minus']=False #line:1254
    O000OO00O0000OOO0 =NavigationToolbar2Tk (OOO0OO000O0000O00 ,O0O00OO0O00000000 )#line:1256
    O000OO00O0000OOO0 .update ()#line:1257
    OOO0OO000O0000O00 .get_tk_widget ().pack ()#line:1258
    O00OOO0O00O00O00O =O0O00OOO0OOOOOO0O .add_subplot (111 )#line:1260
    O00OOO0O00O00O00O .set_title (OO000OO0000O00O00 )#line:1262
    O0OO00O0OOOO00OO0 =O0OOO00OO00O00O00 [O00O00000OO0OOO0O ]#line:1263
    if OO0O0O000O0OOO000 !=999 :#line:1266
        O00OOO0O00O00O00O .set_xticklabels (O0OO00O0OOOO00OO0 ,rotation =-90 ,fontsize =8 )#line:1267
    OOOO00O000O0OOO0O =range (0 ,len (O0OO00O0OOOO00OO0 ),1 )#line:1270
    for OOOO0OOO00OO00O0O in O000000O0O00OOOO0 :#line:1275
        O0O000O0O0O000O00 =O0OOO00OO00O00O00 [OOOO0OOO00OO00O0O ].astype (float )#line:1276
        if OOOO0OOO00OO00O0O =="关注区域":#line:1278
            O00OOO0O00O00O00O .plot (list (O0OO00O0OOOO00OO0 ),list (O0O000O0O0O000O00 ),label =str (OOOO0OOO00OO00O0O ),color ="red")#line:1279
        else :#line:1280
            O00OOO0O00O00O00O .plot (list (O0OO00O0OOOO00OO0 ),list (O0O000O0O0O000O00 ),label =str (OOOO0OOO00OO00O0O ))#line:1281
        if OO0O0O000O0OOO000 ==100 :#line:1284
            for O0OO000OOOO00O000 ,OOO0O0OO0OOO0O0O0 in zip (O0OO00O0OOOO00OO0 ,O0O000O0O0O000O00 ):#line:1285
                if OOO0O0OO0OOO0O0O0 ==max (O0O000O0O0O000O00 )and OOO0O0OO0OOO0O0O0 >=3 and len (O000000O0O00OOOO0 )!=1 :#line:1286
                     O00OOO0O00O00O00O .text (O0OO000OOOO00O000 ,OOO0O0OO0OOO0O0O0 ,(str (OOOO0OOO00OO00O0O )+":"+str (int (OOO0O0OO0OOO0O0O0 ))),color ='black',size =8 )#line:1287
                if len (O000000O0O00OOOO0 )==1 and OOO0O0OO0OOO0O0O0 >=0.01 :#line:1288
                     O00OOO0O00O00O00O .text (O0OO000OOOO00O000 ,OOO0O0OO0OOO0O0O0 ,str (int (OOO0O0OO0OOO0O0O0 )),color ='black',size =8 )#line:1289
    if len (O000000O0O00OOOO0 )==1 :#line:1299
        O00000OOO0OO0OO0O =O0OOO00OO00O00O00 [O000000O0O00OOOO0 ].astype (float ).values #line:1300
        O00OOOOOOO00000OO =O00000OOO0OO0OO0O .mean ()#line:1301
        OO0000OOO0OO0O000 =O00000OOO0OO0OO0O .std ()#line:1302
        O000OOOOO0OO0OOO0 =O00OOOOOOO00000OO +3 *OO0000OOO0OO0O000 #line:1303
        O0O0O0O0OOO000OO0 =OO0000OOO0OO0O000 -3 *OO0000OOO0OO0O000 #line:1304
        O00OOO0O00O00O00O .axhline (O00OOOOOOO00000OO ,color ='r',linestyle ='--',label ='Mean')#line:1306
        O00OOO0O00O00O00O .axhline (O000OOOOO0OO0OOO0 ,color ='g',linestyle ='--',label ='UCL(μ+3σ)')#line:1307
        O00OOO0O00O00O00O .axhline (O0O0O0O0OOO000OO0 ,color ='g',linestyle ='--',label ='LCL(μ-3σ)')#line:1308
    O00OOO0O00O00O00O .set_title ("控制图")#line:1310
    O00OOO0O00O00O00O .set_xlabel ("项")#line:1311
    O0O00OOO0OOOOOO0O .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1312
    OOOOOOOOOOOO0O00O =O00OOO0O00O00O00O .get_position ()#line:1313
    O00OOO0O00O00O00O .set_position ([OOOOOOOOOOOO0O00O .x0 ,OOOOOOOOOOOO0O00O .y0 ,OOOOOOOOOOOO0O00O .width *0.7 ,OOOOOOOOOOOO0O00O .height ])#line:1314
    O00OOO0O00O00O00O .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1315
    OO0O0OO00OO000000 =StringVar ()#line:1318
    OO0OOO00O0O000OO0 =ttk .Combobox (O00O0OOOO0000O000 ,width =15 ,textvariable =OO0O0OO00OO000000 ,state ='readonly')#line:1319
    OO0OOO00O0O000OO0 ['values']=O000000O0O00OOOO0 #line:1320
    OO0OOO00O0O000OO0 .pack (side =LEFT )#line:1321
    OO0OOO00O0O000OO0 .current (0 )#line:1322
    OOOOO0OOOOO000000 =Button (O00O0OOOO0000O000 ,text ="控制图（单项）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0OOO00OO00O00O00 ,O00O00000OO0OOO0O ,[OO00000O000O0OOOO for OO00000O000O0OOOO in O000000O0O00OOOO0 if OO0O0OO00OO000000 .get ()in OO00000O000O0OOOO ],OO000OO0000O00O00 ,OO0O0O000O0OOO000 ))#line:1332
    OOOOO0OOOOO000000 .pack (side =LEFT ,anchor ="ne")#line:1333
    OO0OOO0OOO0OOOOO0 =Button (O00O0OOOO0000O000 ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0OOO00OO00O00O00 ,O00O00000OO0OOO0O ,O000000O0O00OOOO0 ,OO000OO0000O00O00 ,0 ))#line:1341
    OO0OOO0OOO0OOOOO0 .pack (side =LEFT ,anchor ="ne")#line:1343
    OOO0OO000O0000O00 .draw ()#line:1344
def Tread_TOOLS_draw (O000000O0OOO00OOO ,OOO00O0000OOO0O0O ,O0O0O0OO00OOO000O ,OO00O0000O0O0OO0O ,OO0000OO0OOOO000O ):#line:1346
    ""#line:1347
    warnings .filterwarnings ("ignore")#line:1348
    OO00O00OO0OO0O0O0 =Toplevel ()#line:1349
    OO00O00OO0OO0O0O0 .title (OOO00O0000OOO0O0O )#line:1350
    OO0OO0O00OO00OO0O =ttk .Frame (OO00O00OO0OO0O0O0 ,height =20 )#line:1351
    OO0OO0O00OO00OO0O .pack (side =TOP )#line:1352
    OOOO00O000OOOO000 =Figure (figsize =(12 ,6 ),dpi =100 )#line:1354
    OOO000OOOOOOOOO00 =FigureCanvasTkAgg (OOOO00O000OOOO000 ,master =OO00O00OO0OO0O0O0 )#line:1355
    OOO000OOOOOOOOO00 .draw ()#line:1356
    OOO000OOOOOOOOO00 .get_tk_widget ().pack (expand =1 )#line:1357
    O0OOO00O00OO00OOO =OOOO00O000OOOO000 .add_subplot (111 )#line:1358
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1360
    plt .rcParams ['axes.unicode_minus']=False #line:1361
    OOOOOOOOOOOO0OO0O =NavigationToolbar2Tk (OOO000OOOOOOOOO00 ,OO00O00OO0OO0O0O0 )#line:1363
    OOOOOOOOOOOO0OO0O .update ()#line:1364
    OOO000OOOOOOOOO00 .get_tk_widget ().pack ()#line:1366
    try :#line:1369
        O0000O000OO000O00 =O000000O0OOO00OOO .columns #line:1370
        O000000O0OOO00OOO =O000000O0OOO00OOO .sort_values (by =OO00O0000O0O0OO0O ,ascending =[False ],na_position ="last")#line:1371
    except :#line:1372
        O00O0OOO0000O0O0O =eval (O000000O0OOO00OOO )#line:1373
        O00O0OOO0000O0O0O =pd .DataFrame .from_dict (O00O0OOO0000O0O0O ,TT_orient =O0O0O0OO00OOO000O ,columns =[OO00O0000O0O0OO0O ]).reset_index ()#line:1376
        O000000O0OOO00OOO =O00O0OOO0000O0O0O .sort_values (by =OO00O0000O0O0OO0O ,ascending =[False ],na_position ="last")#line:1377
    if ("日期"in OOO00O0000OOO0O0O or "时间"in OOO00O0000OOO0O0O or "季度"in OOO00O0000OOO0O0O )and "饼图"not in OO0000OO0OOOO000O :#line:1381
        O000000O0OOO00OOO [O0O0O0OO00OOO000O ]=pd .to_datetime (O000000O0OOO00OOO [O0O0O0OO00OOO000O ],format ="%Y/%m/%d").dt .date #line:1382
        O000000O0OOO00OOO =O000000O0OOO00OOO .sort_values (by =O0O0O0OO00OOO000O ,ascending =[True ],na_position ="last")#line:1383
    elif "批号"in OOO00O0000OOO0O0O :#line:1384
        O000000O0OOO00OOO [O0O0O0OO00OOO000O ]=O000000O0OOO00OOO [O0O0O0OO00OOO000O ].astype (str )#line:1385
        O000000O0OOO00OOO =O000000O0OOO00OOO .sort_values (by =O0O0O0OO00OOO000O ,ascending =[True ],na_position ="last")#line:1386
        O0OOO00O00OO00OOO .set_xticklabels (O000000O0OOO00OOO [O0O0O0OO00OOO000O ],rotation =-90 ,fontsize =8 )#line:1387
    else :#line:1388
        O000000O0OOO00OOO [O0O0O0OO00OOO000O ]=O000000O0OOO00OOO [O0O0O0OO00OOO000O ].astype (str )#line:1389
        O0OOO00O00OO00OOO .set_xticklabels (O000000O0OOO00OOO [O0O0O0OO00OOO000O ],rotation =-90 ,fontsize =8 )#line:1390
    O0OOOOO000O00OOOO =O000000O0OOO00OOO [OO00O0000O0O0OO0O ]#line:1392
    OO0O0OOO0O0O0O0O0 =range (0 ,len (O0OOOOO000O00OOOO ),1 )#line:1393
    O0OOO00O00OO00OOO .set_title (OOO00O0000OOO0O0O )#line:1395
    if OO0000OO0OOOO000O =="柱状图":#line:1399
        O0OOO00O00OO00OOO .bar (x =O000000O0OOO00OOO [O0O0O0OO00OOO000O ],height =O0OOOOO000O00OOOO ,width =0.2 ,color ="#87CEFA")#line:1400
    elif OO0000OO0OOOO000O =="饼图":#line:1401
        O0OOO00O00OO00OOO .pie (x =O0OOOOO000O00OOOO ,labels =O000000O0OOO00OOO [O0O0O0OO00OOO000O ],autopct ="%0.2f%%")#line:1402
    elif OO0000OO0OOOO000O =="折线图":#line:1403
        O0OOO00O00OO00OOO .plot (O000000O0OOO00OOO [O0O0O0OO00OOO000O ],O0OOOOO000O00OOOO ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:1404
    elif "帕累托图"in str (OO0000OO0OOOO000O ):#line:1406
        O000OOOOO0O0OO0O0 =O000000O0OOO00OOO [OO00O0000O0O0OO0O ].fillna (0 )#line:1407
        O00000O000O0O0OOO =O000OOOOO0O0OO0O0 .cumsum ()/O000OOOOO0O0OO0O0 .sum ()*100 #line:1411
        O000000O0OOO00OOO ["百分比"]=round (O000000O0OOO00OOO ["数量"]/O000OOOOO0O0OO0O0 .sum ()*100 ,2 )#line:1412
        O000000O0OOO00OOO ["累计百分比"]=round (O00000O000O0O0OOO ,2 )#line:1413
        O0O0OO0O00O00O00O =O00000O000O0O0OOO [O00000O000O0O0OOO >0.8 ].index [0 ]#line:1414
        OOO00O000OOO0OOO0 =O000OOOOO0O0OO0O0 .index .tolist ().index (O0O0OO0O00O00O00O )#line:1415
        O0OOO00O00OO00OOO .bar (x =O000000O0OOO00OOO [O0O0O0OO00OOO000O ],height =O000OOOOO0O0OO0O0 ,color ="C0",label =OO00O0000O0O0OO0O )#line:1419
        OO0OOO0OOOO0O00O0 =O0OOO00O00OO00OOO .twinx ()#line:1420
        OO0OOO0OOOO0O00O0 .plot (O000000O0OOO00OOO [O0O0O0OO00OOO000O ],O00000O000O0O0OOO ,color ="C1",alpha =0.6 ,label ="累计比例")#line:1421
        OO0OOO0OOOO0O00O0 .yaxis .set_major_formatter (PercentFormatter ())#line:1422
        O0OOO00O00OO00OOO .tick_params (axis ="y",colors ="C0")#line:1427
        OO0OOO0OOOO0O00O0 .tick_params (axis ="y",colors ="C1")#line:1428
        for OO00O00O0O00O0O00 ,OOO0OOO0OOOOO0O0O ,O0OOOOOO0O000OO0O ,OOO00000OO0O0O00O in zip (O000000O0OOO00OOO [O0O0O0OO00OOO000O ],O000OOOOO0O0OO0O0 ,O000000O0OOO00OOO ["百分比"],O000000O0OOO00OOO ["累计百分比"]):#line:1430
            O0OOO00O00OO00OOO .text (OO00O00O0O00O0O00 ,OOO0OOO0OOOOO0O0O +0.1 ,str (int (OOO0OOO0OOOOO0O0O ))+", "+str (int (O0OOOOOO0O000OO0O ))+"%,"+str (int (OOO00000OO0O0O00O ))+"%",color ='black',size =8 )#line:1431
        if "超级帕累托图"in str (OO0000OO0OOOO000O ):#line:1434
            OO00O0000000O0O00 =re .compile (r'[(](.*?)[)]',re .S )#line:1435
            O00OO0O0O000O0OOO =re .findall (OO00O0000000O0O00 ,OO0000OO0OOOO000O )[0 ]#line:1436
            O0OOO00O00OO00OOO .bar (x =O000000O0OOO00OOO [O0O0O0OO00OOO000O ],height =O000000O0OOO00OOO [O00OO0O0O000O0OOO ],color ="orangered",label =O00OO0O0O000O0OOO )#line:1437
    OOOO00O000OOOO000 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1442
    OOO0OO000O000O000 =O0OOO00O00OO00OOO .get_position ()#line:1443
    O0OOO00O00OO00OOO .set_position ([OOO0OO000O000O000 .x0 ,OOO0OO000O000O000 .y0 ,OOO0OO000O000O000 .width *0.7 ,OOO0OO000O000O000 .height ])#line:1444
    O0OOO00O00OO00OOO .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1445
    OOO000OOOOOOOOO00 .draw ()#line:1448
    if len (O0OOOOO000O00OOOO )<=20 and OO0000OO0OOOO000O !="饼图"and OO0000OO0OOOO000O !="帕累托图":#line:1451
        for OOO00OO0000O0OO0O ,O00O000000O0OOOO0 in zip (OO0O0OOO0O0O0O0O0 ,O0OOOOO000O00OOOO ):#line:1452
            OOOO0OOO00O000000 =str (O00O000000O0OOOO0 )#line:1453
            OOOO0O0OOO000OOOO =(OOO00OO0000O0OO0O ,O00O000000O0OOOO0 +0.3 )#line:1454
            O0OOO00O00OO00OOO .annotate (OOOO0OOO00O000000 ,xy =OOOO0O0OOO000OOOO ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:1455
    OOOO000OO0O0OO0O0 =Button (OO0OO0O00OO00OO0O ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (O000000O0OOO00OOO ),)#line:1465
    OOOO000OO0O0OO0O0 .pack (side =RIGHT )#line:1466
    O0O0OOOOOO000OO0O =Button (OO0OO0O00OO00OO0O ,relief =GROOVE ,text ="查看原始数据",command =lambda :Tread_TOOLS_view_dict (O000000O0OOO00OOO ,1 ))#line:1470
    O0O0OOOOOO000OO0O .pack (side =RIGHT )#line:1471
    OO00OOO00O0OO0OOO =Button (OO0OO0O00OO00OO0O ,relief =GROOVE ,text ="饼图",command =lambda :Tread_TOOLS_draw (O000000O0OOO00OOO ,OOO00O0000OOO0O0O ,O0O0O0OO00OOO000O ,OO00O0000O0O0OO0O ,"饼图"),)#line:1479
    OO00OOO00O0OO0OOO .pack (side =LEFT )#line:1480
    OO00OOO00O0OO0OOO =Button (OO0OO0O00OO00OO0O ,relief =GROOVE ,text ="柱状图",command =lambda :Tread_TOOLS_draw (O000000O0OOO00OOO ,OOO00O0000OOO0O0O ,O0O0O0OO00OOO000O ,OO00O0000O0O0OO0O ,"柱状图"),)#line:1487
    OO00OOO00O0OO0OOO .pack (side =LEFT )#line:1488
    OO00OOO00O0OO0OOO =Button (OO0OO0O00OO00OO0O ,relief =GROOVE ,text ="折线图",command =lambda :Tread_TOOLS_draw (O000000O0OOO00OOO ,OOO00O0000OOO0O0O ,O0O0O0OO00OOO000O ,OO00O0000O0O0OO0O ,"折线图"),)#line:1494
    OO00OOO00O0OO0OOO .pack (side =LEFT )#line:1495
    OO00OOO00O0OO0OOO =Button (OO0OO0O00OO00OO0O ,relief =GROOVE ,text ="帕累托图",command =lambda :Tread_TOOLS_draw (O000000O0OOO00OOO ,OOO00O0000OOO0O0O ,O0O0O0OO00OOO000O ,OO00O0000O0O0OO0O ,"帕累托图"),)#line:1502
    OO00OOO00O0OO0OOO .pack (side =LEFT )#line:1503
def helper ():#line:1509
    ""#line:1510
    OOO000OOO0000O0OO =Toplevel ()#line:1511
    OOO000OOO0000O0OO .title ("程序使用帮助")#line:1512
    OOO000OOO0000O0OO .geometry ("700x500")#line:1513
    OO000000O00O0OOOO =Scrollbar (OOO000OOO0000O0OO )#line:1515
    OOO0O000OO00O00O0 =Text (OOO000OOO0000O0OO ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1516
    OO000000O00O0OOOO .pack (side =RIGHT ,fill =Y )#line:1517
    OOO0O000OO00O00O0 .pack ()#line:1518
    OO000000O00O0OOOO .config (command =OOO0O000OO00O00O0 .yview )#line:1519
    OOO0O000OO00O00O0 .config (yscrollcommand =OO000000O00O0OOOO .set )#line:1520
    OOO0O000OO00O00O0 .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1525
    OOO0O000OO00O00O0 .config (state =DISABLED )#line:1526
def Tread_TOOLS_CLEAN (OOO0O000O000OO0OO ):#line:1530
        ""#line:1531
        OOO0O000O000OO0OO ["报告编码"]=OOO0O000O000OO0OO ["报告编码"].astype ("str")#line:1533
        OOO0O000O000OO0OO ["产品批号"]=OOO0O000O000OO0OO ["产品批号"].astype ("str")#line:1535
        OOO0O000O000OO0OO ["型号"]=OOO0O000O000OO0OO ["型号"].astype ("str")#line:1536
        OOO0O000O000OO0OO ["规格"]=OOO0O000O000OO0OO ["规格"].astype ("str")#line:1537
        OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"]=OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1539
        OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"]=OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1540
        OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"]=OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1541
        OOO0O000O000OO0OO ["产品名称"]=OOO0O000O000OO0OO ["产品名称"].str .replace ("*","※",regex =False )#line:1543
        OOO0O000O000OO0OO ["产品批号"]=OOO0O000O000OO0OO ["产品批号"].str .replace ("(","（",regex =False )#line:1545
        OOO0O000O000OO0OO ["产品批号"]=OOO0O000O000OO0OO ["产品批号"].str .replace (")","）",regex =False )#line:1546
        OOO0O000O000OO0OO ["产品批号"]=OOO0O000O000OO0OO ["产品批号"].str .replace ("*","※",regex =False )#line:1547
        OOO0O000O000OO0OO ['事件发生日期']=pd .to_datetime (OOO0O000O000OO0OO ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1550
        OOO0O000O000OO0OO ["事件发生月份"]=OOO0O000O000OO0OO ["事件发生日期"].dt .to_period ("M").astype (str )#line:1554
        OOO0O000O000OO0OO ["事件发生季度"]=OOO0O000O000OO0OO ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1555
        OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"]=OOO0O000O000OO0OO ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1559
        OOO0O000O000OO0OO ["产品批号"]=OOO0O000O000OO0OO ["产品批号"].fillna ("未填写")#line:1560
        OOO0O000O000OO0OO ["型号"]=OOO0O000O000OO0OO ["型号"].fillna ("未填写")#line:1561
        OOO0O000O000OO0OO ["规格"]=OOO0O000O000OO0OO ["规格"].fillna ("未填写")#line:1562
        return OOO0O000O000OO0OO #line:1564
def thread_it (O00OOO0O0OOOOO000 ,*OOOO00O00O00OO0OO ):#line:1568
    ""#line:1569
    O0OO00000O0OOOO0O =threading .Thread (target =O00OOO0O0OOOOO000 ,args =OOOO00O00O00OO0OO )#line:1571
    O0OO00000O0OOOO0O .setDaemon (True )#line:1573
    O0OO00000O0OOOO0O .start ()#line:1575
def showWelcome ():#line:1578
    ""#line:1579
    O00OO0O0OOO0O00O0 =roox .winfo_screenwidth ()#line:1580
    O00000O0O000000O0 =roox .winfo_screenheight ()#line:1582
    roox .overrideredirect (True )#line:1584
    roox .attributes ("-alpha",1 )#line:1585
    OOO000O000OOO0OOO =(O00OO0O0OOO0O00O0 -475 )/2 #line:1586
    OOO0OO0OO00OO0000 =(O00000O0O000000O0 -200 )/2 #line:1587
    roox .geometry ("675x140+%d+%d"%(OOO000O000OOO0OOO ,OOO0OO0OO00OO0000 ))#line:1589
    roox ["bg"]="royalblue"#line:1590
    OO0O000OOOOO0000O =Label (roox ,text ="医疗器械警戒趋势分析工具",fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:1593
    OO0O000OOOOO0000O .place (x =0 ,y =15 ,width =675 ,height =90 )#line:1594
    O00OO000OO0OO0O00 =Label (roox ,text ="Trend Analysis Tools V"+str (version_now ),fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ),)#line:1601
    O00OO000OO0OO0O00 .place (x =0 ,y =90 ,width =675 ,height =50 )#line:1602
def closeWelcome ():#line:1605
    ""#line:1606
    for O00O0000OO0OOO000 in range (2 ):#line:1607
        root .attributes ("-alpha",0 )#line:1608
        time .sleep (1 )#line:1609
    root .attributes ("-alpha",1 )#line:1610
    roox .destroy ()#line:1611
if __name__ =='__main__':#line:1615
    pass #line:1616
root =Tk ()#line:1617
root .title ("医疗器械警戒趋势分析工具Trend Analysis Tools V"+str (version_now ))#line:1618
sw_root =root .winfo_screenwidth ()#line:1619
sh_root =root .winfo_screenheight ()#line:1621
ww_root =700 #line:1623
wh_root =620 #line:1624
x_root =(sw_root -ww_root )/2 #line:1626
y_root =(sh_root -wh_root )/2 #line:1627
root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:1628
root .configure (bg ="steelblue")#line:1629
try :#line:1632
    frame0 =ttk .Frame (root ,width =100 ,height =20 )#line:1633
    frame0 .pack (side =LEFT )#line:1634
    B_open_files1 =Button (frame0 ,text ="导入原始数据",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,0 ),)#line:1647
    B_open_files1 .pack ()#line:1648
    B_open_files3 =Button (frame0 ,text ="导入分析规则",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,1 ),)#line:1661
    B_open_files3 .pack ()#line:1662
    B_open_files3 =Button (frame0 ,text ="趋势统计分析",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_analysis ,0 ),)#line:1677
    B_open_files3 .pack ()#line:1678
    B_open_files3 =Button (frame0 ,text ="直方图（数量）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"数量"))#line:1691
    B_open_files3 .pack ()#line:1692
    B_open_files3 =Button (frame0 ,text ="直方图（占比）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"百分比"))#line:1703
    B_open_files3 .pack ()#line:1704
    B_open_files3 =Button (frame0 ,text ="查看帮助文件",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (helper ))#line:1715
    B_open_files3 .pack ()#line:1716
    B_open_files3 =Button (frame0 ,text ="变更注册状态",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (display_random_number ))#line:1727
    B_open_files3 .pack ()#line:1728
except :#line:1729
    pass #line:1730
text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF",font ="微软雅黑")#line:1734
text .pack ()#line:1735
text .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1740
text .insert (END ,"\n\n")#line:1741
def A000 ():#line:1743
    pass #line:1744
setting_cfg =read_setting_cfg ()#line:1748
generate_random_file ()#line:1749
setting_cfg =open_setting_cfg ()#line:1750
if setting_cfg ["settingdir"]==0 :#line:1751
    showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:1752
    filepathu =filedialog .askdirectory ()#line:1753
    path =get_directory_path (filepathu )#line:1754
    update_setting_cfg ("settingdir",path )#line:1755
setting_cfg =open_setting_cfg ()#line:1756
random_number =int (setting_cfg ["sidori"])#line:1757
input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:1758
day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:1759
sid =random_number *2 +183576 #line:1760
if input_number ==sid and day_end =="未过期":#line:1761
    usergroup ="用户组=1"#line:1762
    text .insert (END ,usergroup +"   有效期至：")#line:1763
    text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:1764
else :#line:1765
    text .insert (END ,usergroup )#line:1766
text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:1767
roox =Toplevel ()#line:1772
tMain =threading .Thread (target =showWelcome )#line:1773
tMain .start ()#line:1774
t1 =threading .Thread (target =closeWelcome )#line:1775
t1 .start ()#line:1776
root .lift ()#line:1777
root .attributes ("-topmost",True )#line:1778
root .attributes ("-topmost",False )#line:1779
root .mainloop ()#line:1781
