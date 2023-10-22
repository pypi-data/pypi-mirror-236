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
version_now ="0.0.6"#line:57
usergroup ="用户组=0"#line:58
setting_cfg =""#line:59
csdir =str (os .path .dirname (__file__ ))#line:61
csdir =csdir +csdir .split ("treadtools")[0 ][-1 ]#line:62
def extract_zip_file (OO0O0O0OOOO0000OO ,OO000OOOOO0OOOOOO ):#line:71
    import zipfile #line:73
    if OO000OOOOO0OOOOOO =="":#line:74
        return 0 #line:75
    with zipfile .ZipFile (OO0O0O0OOOO0000OO ,'r')as OO00O0O00OO00000O :#line:76
        for O000OOO0000O0000O in OO00O0O00OO00000O .infolist ():#line:77
            O000OOO0000O0000O .filename =O000OOO0000O0000O .filename .encode ('cp437').decode ('gbk')#line:79
            OO00O0O00OO00000O .extract (O000OOO0000O0000O ,OO000OOOOO0OOOOOO )#line:80
def get_directory_path (O0000OOO0OOOO00O0 ):#line:86
    global csdir #line:88
    if not (os .path .isfile (os .path .join (O0000OOO0OOOO00O0 ,'规则文件.xls'))):#line:90
        extract_zip_file (csdir +"def.py",O0000OOO0OOOO00O0 )#line:95
    if O0000OOO0OOOO00O0 =="":#line:97
        quit ()#line:98
    return O0000OOO0OOOO00O0 #line:99
def convert_and_compare_dates (OOO00OOOOO00O0000 ):#line:103
    import datetime #line:104
    O0O00OO0O0000OO00 =datetime .datetime .now ()#line:105
    try :#line:107
       OO0OOOO00O0000O0O =datetime .datetime .strptime (str (int (int (OOO00OOOOO00O0000 )/4 )),"%Y%m%d")#line:108
    except :#line:109
        print ("fail")#line:110
        return "已过期"#line:111
    if OO0OOOO00O0000O0O >O0O00OO0O0000OO00 :#line:113
        return "未过期"#line:115
    else :#line:116
        return "已过期"#line:117
def read_setting_cfg ():#line:119
    global csdir #line:120
    if os .path .exists (csdir +'setting.cfg'):#line:122
        text .insert (END ,"已完成初始化\n")#line:123
        with open (csdir +'setting.cfg','r')as O000OOOO0OOOOO0O0 :#line:124
            OO00O0OOO00O0O0OO =eval (O000OOOO0OOOOO0O0 .read ())#line:125
    else :#line:126
        O000O00O0O000OOOO =csdir +'setting.cfg'#line:128
        with open (O000O00O0O000OOOO ,'w')as O000OOOO0OOOOO0O0 :#line:129
            O000OOOO0OOOOO0O0 .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:130
        text .insert (END ,"未初始化，正在初始化...\n")#line:131
        OO00O0OOO00O0O0OO =read_setting_cfg ()#line:132
    return OO00O0OOO00O0O0OO #line:133
def open_setting_cfg ():#line:136
    global csdir #line:137
    with open (csdir +"setting.cfg","r")as O00O0OOOO0OOOO0OO :#line:139
        O0OOOOOOO0OOOO0OO =eval (O00O0OOOO0OOOO0OO .read ())#line:141
    return O0OOOOOOO0OOOO0OO #line:142
def update_setting_cfg (OOOO0O0OO0OOOOO0O ,O00O000000O00OO0O ):#line:144
    global csdir #line:145
    with open (csdir +"setting.cfg","r")as OOOOO0OOO0O0OOO00 :#line:147
        OOO0OO000OO0O0OO0 =eval (OOOOO0OOO0O0OOO00 .read ())#line:149
    if OOO0OO000OO0O0OO0 [OOOO0O0OO0OOOOO0O ]==0 or OOO0OO000OO0O0OO0 [OOOO0O0OO0OOOOO0O ]=="11111180000808":#line:151
        OOO0OO000OO0O0OO0 [OOOO0O0OO0OOOOO0O ]=O00O000000O00OO0O #line:152
        with open (csdir +"setting.cfg","w")as OOOOO0OOO0O0OOO00 :#line:154
            OOOOO0OOO0O0OOO00 .write (str (OOO0OO000OO0O0OO0 ))#line:155
def generate_random_file ():#line:158
    OO000OO0O0OO0OO0O =random .randint (200000 ,299999 )#line:160
    update_setting_cfg ("sidori",OO000OO0O0OO0OO0O )#line:162
def display_random_number ():#line:164
    global csdir #line:165
    O0OO0O0O0O00O00O0 =Toplevel ()#line:166
    O0OO0O0O0O00O00O0 .title ("ID")#line:167
    O0OO0O0O0O00O0OO0 =O0OO0O0O0O00O00O0 .winfo_screenwidth ()#line:169
    O000OO00O0OO00OOO =O0OO0O0O0O00O00O0 .winfo_screenheight ()#line:170
    O0O0OO0OOO0000O0O =80 #line:172
    O0O0OOOOOO0O000OO =70 #line:173
    O0O0OO0OO0OO00OOO =(O0OO0O0O0O00O0OO0 -O0O0OO0OOO0000O0O )/2 #line:175
    OOOOO00000O000000 =(O000OO00O0OO00OOO -O0O0OOOOOO0O000OO )/2 #line:176
    O0OO0O0O0O00O00O0 .geometry ("%dx%d+%d+%d"%(O0O0OO0OOO0000O0O ,O0O0OOOOOO0O000OO ,O0O0OO0OO0OO00OOO ,OOOOO00000O000000 ))#line:177
    with open (csdir +"setting.cfg","r")as O0OO00OOO0OOOOO00 :#line:180
        O0O0000O00OOO0O00 =eval (O0OO00OOO0OOOOO00 .read ())#line:182
    O0O000000000OO00O =int (O0O0000O00OOO0O00 ["sidori"])#line:183
    OOO0OO00O0000OO0O =O0O000000000OO00O *2 +183576 #line:184
    print (OOO0OO00O0000OO0O )#line:186
    O00000000OO0OOO00 =ttk .Label (O0OO0O0O0O00O00O0 ,text =f"机器码: {O0O000000000OO00O}")#line:188
    OOOOOO00OO0O0O0OO =ttk .Entry (O0OO0O0O0O00O00O0 )#line:189
    O00000000OO0OOO00 .pack ()#line:192
    OOOOOO00OO0O0O0OO .pack ()#line:193
    ttk .Button (O0OO0O0O0O00O00O0 ,text ="验证",command =lambda :check_input (OOOOOO00OO0O0O0OO .get (),OOO0OO00O0000OO0O )).pack ()#line:197
def check_input (O0OO0OO0O0OO00OOO ,OO000OOOOOOOOOOOO ):#line:199
    try :#line:203
        O000O000O0O00O0O0 =int (str (O0OO0OO0O0OO00OOO )[0 :6 ])#line:204
        OO00OO0000O000O00 =convert_and_compare_dates (str (O0OO0OO0O0OO00OOO )[6 :14 ])#line:205
    except :#line:206
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:207
        return 0 #line:208
    if O000O000O0O00O0O0 ==OO000OOOOOOOOOOOO and OO00OO0000O000O00 =="未过期":#line:210
        update_setting_cfg ("sidfinal",O0OO0OO0O0OO00OOO )#line:211
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:212
        quit ()#line:213
    else :#line:214
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:215
def update_software (OOO0000O0O0000000 ):#line:219
    global version_now #line:221
    O00000O00O00OOO00 =requests .get (f"https://pypi.org/pypi/{OOO0000O0O0000000}/json").json ()["info"]["version"]#line:222
    text .insert (END ,"当前版本为："+version_now )#line:223
    if O00000O00O00OOO00 >version_now :#line:224
        text .insert (END ,"\n最新版本为："+O00000O00O00OOO00 +",正在尝试自动更新....")#line:225
        pip .main (['install',OOO0000O0O0000000 ,'--upgrade'])#line:227
        text .insert (END ,"\n您可以开展工作。")#line:228
def Tread_TOOLS_fileopen (OOOO000OOOO0000OO ):#line:232
    ""#line:233
    global TT_ori #line:234
    global TT_ori_backup #line:235
    global TT_biaozhun #line:236
    warnings .filterwarnings ('ignore')#line:237
    if OOOO000OOOO0000OO ==0 :#line:239
        O0O000O0OOOOO0OOO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:240
        O0O00O000OOO0000O =[pd .read_excel (O00000O00OOOO00OO ,header =0 ,sheet_name =0 )for O00000O00OOOO00OO in O0O000O0OOOOO0OOO ]#line:241
        O0O00OOOOOOOOOOOO =pd .concat (O0O00O000OOO0000O ,ignore_index =True ).drop_duplicates ()#line:242
        try :#line:243
            O0O00OOOOOOOOOOOO =O0O00OOOOOOOOOOOO .loc [:,~TT_ori .columns .str .contains ("^Unnamed")]#line:244
        except :#line:245
            pass #line:246
        TT_ori_backup =O0O00OOOOOOOOOOOO .copy ()#line:247
        TT_ori =Tread_TOOLS_CLEAN (O0O00OOOOOOOOOOOO ).copy ()#line:248
        text .insert (END ,"\n原始数据导入成功，行数："+str (len (TT_ori )))#line:250
        text .insert (END ,"\n数据校验：\n")#line:251
        text .insert (END ,TT_ori )#line:252
        text .see (END )#line:253
    if OOOO000OOOO0000OO ==1 :#line:255
        O0O000O0000OOOOOO =filedialog .askopenfilename (filetypes =[("XLS",".xls")])#line:256
        TT_biaozhun ["关键字表"]=pd .read_excel (O0O000O0000OOOOOO ,sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:257
        TT_biaozhun ["产品批号"]=pd .read_excel (O0O000O0000OOOOOO ,sheet_name ="产品批号",header =0 ,index_col =0 ,).reset_index ()#line:258
        TT_biaozhun ["事件发生月份"]=pd .read_excel (O0O000O0000OOOOOO ,sheet_name ="事件发生月份",header =0 ,index_col =0 ,).reset_index ()#line:259
        TT_biaozhun ["事件发生季度"]=pd .read_excel (O0O000O0000OOOOOO ,sheet_name ="事件发生季度",header =0 ,index_col =0 ,).reset_index ()#line:260
        TT_biaozhun ["规格"]=pd .read_excel (O0O000O0000OOOOOO ,sheet_name ="规格",header =0 ,index_col =0 ,).reset_index ()#line:261
        TT_biaozhun ["型号"]=pd .read_excel (O0O000O0000OOOOOO ,sheet_name ="型号",header =0 ,index_col =0 ,).reset_index ()#line:262
        TT_biaozhun ["设置"]=pd .read_excel (O0O000O0000OOOOOO ,sheet_name ="设置",header =0 ,index_col =0 ,).reset_index ()#line:263
        Tread_TOOLS_check (TT_ori ,TT_biaozhun ["关键字表"],0 )#line:264
        text .insert (END ,"\n标准导入成功，行数："+str (len (TT_biaozhun )))#line:265
        text .see (END )#line:266
def Tread_TOOLS_check (OOO0O000OOO0OOOOO ,O0O0O00O0O00000OO ,O0000OOOOO000O00O ):#line:268
        ""#line:269
        global TT_ori #line:270
        O00OO00O0O0O0OOOO =Tread_TOOLS_Countall (OOO0O000OOO0OOOOO ).df_psur (O0O0O00O0O00000OO )#line:271
        if O0000OOOOO000O00O ==0 :#line:273
            Tread_TOOLS_tree_Level_2 (O00OO00O0O0O0OOOO ,0 ,TT_ori .copy ())#line:275
        O00OO00O0O0O0OOOO ["核验"]=0 #line:278
        O00OO00O0O0O0OOOO .loc [(O00OO00O0O0O0OOOO ["关键字标记"].str .contains ("-其他关键字-",na =False )),"核验"]=O00OO00O0O0O0OOOO .loc [(O00OO00O0O0O0OOOO ["关键字标记"].str .contains ("-其他关键字-",na =False )),"总数量"]#line:279
        if O00OO00O0O0O0OOOO ["核验"].sum ()>0 :#line:280
            showinfo (title ="温馨提示",message ="存在未定义类型的报告"+str (O00OO00O0O0O0OOOO ["核验"].sum ())+"条，趋势分析可能会存在遗漏，建议修正该错误再进行下一步。")#line:281
def Tread_TOOLS_tree_Level_2 (O0O0O00OOO0OO0O0O ,O0O00O00OOOOOO000 ,O0000OO0O0OO00O0O ,*OO0000O0OOOO0O000 ):#line:283
    ""#line:284
    global TT_ori_backup #line:286
    OO0OO00OO0O0O00O0 =O0O0O00OOO0OO0O0O .columns .values .tolist ()#line:288
    O0O00O00OOOOOO000 =0 #line:289
    O0000O0O0O000O0O0 =O0O0O00OOO0OO0O0O .loc [:]#line:290
    OO0000OO000OOOO00 =0 #line:294
    try :#line:295
        O00O0O00000O00O00 =OO0000O0OOOO0O000 [0 ]#line:296
        OO0000OO000OOOO00 =1 #line:297
    except :#line:298
        pass #line:299
    O0O000OOO0O0O000O =Toplevel ()#line:302
    O0O000OOO0O0O000O .title ("报表查看器")#line:303
    OOOO0O0OO00O0OO00 =O0O000OOO0O0O000O .winfo_screenwidth ()#line:304
    O00OOOOOO0OOOO0OO =O0O000OOO0O0O000O .winfo_screenheight ()#line:306
    O0OO00OO0O00OOOO0 =1300 #line:308
    OOO0O0000000O000O =600 #line:309
    O00OO0OOOO0000OO0 =(OOOO0O0OO00O0OO00 -O0OO00OO0O00OOOO0 )/2 #line:311
    OO0OO00OOO00O0OO0 =(O00OOOOOO0OOOO0OO -OOO0O0000000O000O )/2 #line:312
    O0O000OOO0O0O000O .geometry ("%dx%d+%d+%d"%(O0OO00OO0O00OOOO0 ,OOO0O0000000O000O ,O00OO0OOOO0000OO0 ,OO0OO00OOO00O0OO0 ))#line:313
    OOOO0O00OOOOO0OO0 =ttk .Frame (O0O000OOO0O0O000O ,width =1300 ,height =20 )#line:314
    OOOO0O00OOOOO0OO0 .pack (side =BOTTOM )#line:315
    O0O0OO0O000O00OOO =ttk .Frame (O0O000OOO0O0O000O ,width =1300 ,height =20 )#line:317
    O0O0OO0O000O00OOO .pack (side =TOP )#line:318
    if 1 >0 :#line:322
        O0O0000O00OO0OOOO =Button (OOOO0O00OOOOO0OO0 ,text ="控制图(所有)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0000O0O0O000O0O0 [:-1 ],O00O0O00000O00O00 ,[O00O000000OOOO000 for O00O000000OOOO000 in O0000O0O0O000O0O0 .columns if (O00O000000OOOO000 not in [O00O0O00000O00O00 ])],"关键字趋势图",100 ),)#line:332
        if OO0000OO000OOOO00 ==1 :#line:333
            O0O0000O00OO0OOOO .pack (side =LEFT )#line:334
        O0O0000O00OO0OOOO =Button (OOOO0O00OOOOO0OO0 ,text ="控制图(总数量)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0000O0O0O000O0O0 [:-1 ],O00O0O00000O00O00 ,[O0OO0OOOOO0O0000O for O0OO0OOOOO0O0000O in O0000O0O0O000O0O0 .columns if (O0OO0OOOOO0O0000O in ["该元素总数量"])],"关键字趋势图",100 ),)#line:344
        if OO0000OO000OOOO00 ==1 :#line:345
            O0O0000O00OO0OOOO .pack (side =LEFT )#line:346
        O0O0OO000000OO0OO =Button (OOOO0O00OOOOO0OO0 ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (O0000O0O0O000O0O0 ),)#line:356
        O0O0OO000000OO0OO .pack (side =LEFT )#line:357
        O0O0OO000000OO0OO =Button (OOOO0O00OOOOO0OO0 ,text ="发生率测算",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_fashenglv (O0000O0O0O000O0O0 ,O00O0O00000O00O00 ),)#line:367
        if "关键字标记"not in O0000O0O0O000O0O0 .columns and "报告编码"not in O0000O0O0O000O0O0 .columns :#line:368
            if "对象"not in O0000O0O0O000O0O0 .columns :#line:369
                O0O0OO000000OO0OO .pack (side =LEFT )#line:370
        O0O0OO000000OO0OO =Button (OOOO0O00OOOOO0OO0 ,text ="直方图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_histbar (O0000O0O0O000O0O0 .copy ()),)#line:380
        if "对象"in O0000O0O0O000O0O0 .columns :#line:381
            O0O0OO000000OO0OO .pack (side =LEFT )#line:382
        O0OO000O0O00O00OO =Button (OOOO0O00OOOOO0OO0 ,text ="行数:"+str (len (O0000O0O0O000O0O0 )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:392
        O0OO000O0O00O00OO .pack (side =LEFT )#line:393
    O00O0OOO0O000O0O0 =O0000O0O0O000O0O0 .values .tolist ()#line:396
    O0OOOO0O0OO00O0O0 =O0000O0O0O000O0O0 .columns .values .tolist ()#line:397
    OO0OOO000OO0O000O =ttk .Treeview (O0O0OO0O000O00OOO ,columns =O0OOOO0O0OO00O0O0 ,show ="headings",height =45 )#line:398
    for O0OOOO0OO00000O00 in O0OOOO0O0OO00O0O0 :#line:400
        OO0OOO000OO0O000O .heading (O0OOOO0OO00000O00 ,text =O0OOOO0OO00000O00 )#line:401
    for OO00OO0O0OO0O00OO in O00O0OOO0O000O0O0 :#line:402
        OO0OOO000OO0O000O .insert ("","end",values =OO00OO0O0OO0O00OO )#line:403
    for O0OOO0OO0O0O00O0O in O0OOOO0O0OO00O0O0 :#line:404
        OO0OOO000OO0O000O .column (O0OOO0OO0O0O00O0O ,minwidth =0 ,width =120 ,stretch =NO )#line:405
    O00O000O0O0000000 =Scrollbar (O0O0OO0O000O00OOO ,orient ="vertical")#line:407
    O00O000O0O0000000 .pack (side =RIGHT ,fill =Y )#line:408
    O00O000O0O0000000 .config (command =OO0OOO000OO0O000O .yview )#line:409
    OO0OOO000OO0O000O .config (yscrollcommand =O00O000O0O0000000 .set )#line:410
    O000O0000OOOO0O00 =Scrollbar (O0O0OO0O000O00OOO ,orient ="horizontal")#line:412
    O000O0000OOOO0O00 .pack (side =BOTTOM ,fill =X )#line:413
    O000O0000OOOO0O00 .config (command =OO0OOO000OO0O000O .xview )#line:414
    OO0OOO000OO0O000O .config (yscrollcommand =O00O000O0O0000000 .set )#line:415
    def O0OO0000OO0OOO0OO (O00000000O00OOOO0 ,OOOO0OO00OO0O0O00 ,OOO0O00OOO00O0OOO ):#line:417
        for OO0OOOOOO000O0O00 in OO0OOO000OO0O000O .selection ():#line:420
            OOO00OOO0OO0OO0OO =OO0OOO000OO0O000O .item (OO0OOOOOO000O0O00 ,"values")#line:421
            OO0OO0O0O0OOO0000 =dict (zip (OOOO0OO00OO0O0O00 ,OOO00OOO0OO0OO0OO ))#line:422
        if "该分类下各项计数"in OOOO0OO00OO0O0O00 :#line:424
            OOOOO00OO0OOOOO0O =O0000OO0O0OO00O0O .copy ()#line:425
            OOOOO00OO0OOOOO0O ["关键字查找列"]=""#line:426
            for O0OO0000O0O00O00O in TOOLS_get_list (OO0OO0O0O0OOO0000 ["查找位置"]):#line:427
                OOOOO00OO0OOOOO0O ["关键字查找列"]=OOOOO00OO0OOOOO0O ["关键字查找列"]+OOOOO00OO0OOOOO0O [O0OO0000O0O00O00O ].astype ("str")#line:428
            O0OOOOO0OOOOOOO0O =OOOOO00OO0OOOOO0O .loc [OOOOO00OO0OOOOO0O ["关键字查找列"].str .contains (OO0OO0O0O0OOO0000 ["关键字标记"],na =False )].copy ()#line:429
            O0OOOOO0OOOOOOO0O =O0OOOOO0OOOOOOO0O .loc [~O0OOOOO0OOOOOOO0O ["关键字查找列"].str .contains (OO0OO0O0O0OOO0000 ["排除值"],na =False )].copy ()#line:430
            Tread_TOOLS_tree_Level_2 (O0OOOOO0OOOOOOO0O ,0 ,O0OOOOO0OOOOOOO0O )#line:436
            return 0 #line:437
        if "报告编码"in OOOO0OO00OO0O0O00 :#line:439
            OO0OO0OOOO00O0000 =Toplevel ()#line:440
            OO0000OO0O00000O0 =OO0OO0OOOO00O0000 .winfo_screenwidth ()#line:441
            OOO0OO0000O0OO0OO =OO0OO0OOOO00O0000 .winfo_screenheight ()#line:443
            O000OOOO0O00000OO =800 #line:445
            O00OOO0OO0OOO0OO0 =600 #line:446
            O0OO0000O0O00O00O =(OO0000OO0O00000O0 -O000OOOO0O00000OO )/2 #line:448
            OO0OO0O0000O000O0 =(OOO0OO0000O0OO0OO -O00OOO0OO0OOO0OO0 )/2 #line:449
            OO0OO0OOOO00O0000 .geometry ("%dx%d+%d+%d"%(O000OOOO0O00000OO ,O00OOO0OO0OOO0OO0 ,O0OO0000O0O00O00O ,OO0OO0O0000O000O0 ))#line:450
            O00OOO0OO00O0OO0O =ScrolledText (OO0OO0OOOO00O0000 ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:454
            O00OOO0OO00O0OO0O .pack (padx =10 ,pady =10 )#line:455
            def OOOO0OO0OO0000000 (event =None ):#line:456
                O00OOO0OO00O0OO0O .event_generate ('<<Copy>>')#line:457
            def OO000OOOOOOO0O0O0 (OOOOOOO0000O0OOO0 ,O000000O0OOOOOOOO ):#line:458
                O000O0O000OO000O0 =open (O000000O0OOOOOOOO ,"w",encoding ='utf-8')#line:459
                O000O0O000OO000O0 .write (OOOOOOO0000O0OOO0 )#line:460
                O000O0O000OO000O0 .flush ()#line:462
                showinfo (title ="提示信息",message ="保存成功。")#line:463
            OOO00OOO00O0000OO =Menu (O00OOO0OO00O0OO0O ,tearoff =False ,)#line:465
            OOO00OOO00O0000OO .add_command (label ="复制",command =OOOO0OO0OO0000000 )#line:466
            OOO00OOO00O0000OO .add_command (label ="导出",command =lambda :thread_it (OO000OOOOOOO0O0O0 ,O00OOO0OO00O0OO0O .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =OO0OO0O0O0OOO0000 ["报告编码"],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:467
            def O000OOO0OO000O00O (OO0OO000O0O0OO0OO ):#line:469
                OOO00OOO00O0000OO .post (OO0OO000O0O0OO0OO .x_root ,OO0OO000O0O0OO0OO .y_root )#line:470
            O00OOO0OO00O0OO0O .bind ("<Button-3>",O000OOO0OO000O00O )#line:471
            OO0OO0OOOO00O0000 .title (OO0OO0O0O0OOO0000 ["报告编码"])#line:473
            for O0O00O0OO0O00OO00 in range (len (OOOO0OO00OO0O0O00 )):#line:474
                O00OOO0OO00O0OO0O .insert (END ,OOOO0OO00OO0O0O00 [O0O00O0OO0O00OO00 ])#line:476
                O00OOO0OO00O0OO0O .insert (END ,"：")#line:477
                O00OOO0OO00O0OO0O .insert (END ,OO0OO0O0O0OOO0000 [OOOO0OO00OO0O0O00 [O0O00O0OO0O00OO00 ]])#line:478
                O00OOO0OO00O0OO0O .insert (END ,"\n")#line:479
            O00OOO0OO00O0OO0O .config (state =DISABLED )#line:480
            return 0 #line:481
        OO0OO0O0000O000O0 =OOO00OOO0OO0OO0OO [1 :-1 ]#line:484
        O0OO0000O0O00O00O =OOO0O00OOO00O0OOO .columns .tolist ()#line:486
        O0OO0000O0O00O00O =O0OO0000O0O00O00O [1 :-1 ]#line:487
        O00O00OO000OOO0OO ={'关键词':O0OO0000O0O00O00O ,'数量':OO0OO0O0000O000O0 }#line:489
        O00O00OO000OOO0OO =pd .DataFrame .from_dict (O00O00OO000OOO0OO )#line:490
        O00O00OO000OOO0OO ["数量"]=O00O00OO000OOO0OO ["数量"].astype (float )#line:491
        Tread_TOOLS_draw (O00O00OO000OOO0OO ,"帕累托图",'关键词','数量',"帕累托图")#line:492
        return 0 #line:493
    OO0OOO000OO0O000O .bind ("<Double-1>",lambda O0O0OOO00O00O0O0O :O0OO0000OO0OOO0OO (O0O0OOO00O00O0O0O ,O0OOOO0O0OO00O0O0 ,O0000O0O0O000O0O0 ),)#line:501
    OO0OOO000OO0O000O .pack ()#line:502
class Tread_TOOLS_Countall ():#line:504
    ""#line:505
    def __init__ (OO00O000O0OOO0OOO ,O00OOO0OOOOOOO0O0 ):#line:506
        ""#line:507
        OO00O000O0OOO0OOO .df =O00OOO0OOOOOOO0O0 #line:508
    def df_psur (OOO0O0O0OOO0O0000 ,O00O0OOO0OOO00OOO ,*OO0000OO0O00O0000 ):#line:510
        ""#line:511
        global TT_biaozhun #line:512
        O0O00O0OO00O00OOO =OOO0O0O0OOO0O0000 .df .copy ()#line:513
        O00O000OO0OO00OOO =len (O0O00O0OO00O00OOO .drop_duplicates ("报告编码"))#line:515
        OOOOOO0000O00OO0O =O00O0OOO0OOO00OOO .copy ()#line:518
        O0000OOOO000O000O =TT_biaozhun ["设置"]#line:521
        if O0000OOOO000O000O .loc [1 ,"值"]:#line:522
            OO0OOOO0O0OOO0O00 =O0000OOOO000O000O .loc [1 ,"值"]#line:523
        else :#line:524
            OO0OOOO0O0OOO0O00 ="透视列"#line:525
            O0O00O0OO00O00OOO [OO0OOOO0O0OOO0O00 ]="未正确设置"#line:526
        O0OOOOO0O0OOO0O0O =""#line:528
        OOO000OO0OO0OOOOO ="-其他关键字-"#line:529
        for O0OO00O0O00OOO000 ,O0O00OOOO00OO0O0O in OOOOOO0000O00OO0O .iterrows ():#line:530
            OOO000OO0OO0OOOOO =OOO000OO0OO0OOOOO +"|"+str (O0O00OOOO00OO0O0O ["值"])#line:531
            OOO0000O0000O0OOO =O0O00OOOO00OO0O0O #line:532
        OOO0000O0000O0OOO [3 ]=OOO000OO0OO0OOOOO #line:533
        OOO0000O0000O0OOO [2 ]="-其他关键字-|"#line:534
        OOOOOO0000O00OO0O .loc [len (OOOOOO0000O00OO0O )]=OOO0000O0000O0OOO #line:535
        OOOOOO0000O00OO0O =OOOOOO0000O00OO0O .reset_index (drop =True )#line:536
        O0O00O0OO00O00OOO ["关键字查找列"]=""#line:540
        for O0O00OOO0OOO0OO00 in TOOLS_get_list (OOOOOO0000O00OO0O .loc [0 ,"查找位置"]):#line:541
            O0O00O0OO00O00OOO ["关键字查找列"]=O0O00O0OO00O00OOO ["关键字查找列"]+O0O00O0OO00O00OOO [O0O00OOO0OOO0OO00 ].astype ("str")#line:542
        O0000O0O000000O0O =[]#line:545
        for O0OO00O0O00OOO000 ,O0O00OOOO00OO0O0O in OOOOOO0000O00OO0O .iterrows ():#line:546
            O00O0O0O00O0O0000 =O0O00OOOO00OO0O0O ["值"]#line:547
            O000O000O0OOOO00O =O0O00O0OO00O00OOO .loc [O0O00O0OO00O00OOO ["关键字查找列"].str .contains (O00O0O0O00O0O0000 ,na =False )].copy ()#line:548
            if str (O0O00OOOO00OO0O0O ["排除值"])!="nan":#line:549
                O000O000O0OOOO00O =O000O000O0OOOO00O .loc [~O000O000O0OOOO00O ["关键字查找列"].str .contains (str (O0O00OOOO00OO0O0O ["排除值"]),na =False )].copy ()#line:550
            O000O000O0OOOO00O ["关键字标记"]=str (O00O0O0O00O0O0000 )#line:552
            O000O000O0OOOO00O ["关键字计数"]=1 #line:553
            if len (O000O000O0OOOO00O )>0 :#line:555
                O0000OOOO0OO000O0 =pd .pivot_table (O000O000O0OOOO00O .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns =OO0OOOO0O0OOO0O00 ,aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:565
                O0000OOOO0OO000O0 =O0000OOOO0OO000O0 [:-1 ]#line:566
                O0000OOOO0OO000O0 .columns =O0000OOOO0OO000O0 .columns .droplevel (0 )#line:567
                O0000OOOO0OO000O0 =O0000OOOO0OO000O0 .reset_index ()#line:568
                if len (O0000OOOO0OO000O0 )>0 :#line:571
                    O0O0OO000OOOO0OO0 =str (Counter (TOOLS_get_list0 ("use(关键字查找列).file",O000O000O0OOOO00O ,1000 ))).replace ("Counter({","{")#line:572
                    O0O0OO000OOOO0OO0 =O0O0OO000OOOO0OO0 .replace ("})","}")#line:573
                    O0O0OO000OOOO0OO0 =ast .literal_eval (O0O0OO000OOOO0OO0 )#line:574
                    O0000OOOO0OO000O0 .loc [0 ,"事件分类"]=str (TOOLS_get_list (O0000OOOO0OO000O0 .loc [0 ,"关键字标记"])[0 ])#line:576
                    O0000OOOO0OO000O0 .loc [0 ,"该分类下各项计数"]=str ({O0OOO000000O00OO0 :O0OOO00O0O0OOO0OO for O0OOO000000O00OO0 ,O0OOO00O0O0OOO0OO in O0O0OO000OOOO0OO0 .items ()if STAT_judge_x (str (O0OOO000000O00OO0 ),TOOLS_get_list (O00O0O0O00O0O0000 ))==1 })#line:577
                    O0000OOOO0OO000O0 .loc [0 ,"其他分类各项计数"]=str ({O00O00O000O00OOOO :OOOO00000OO00O0O0 for O00O00O000O00OOOO ,OOOO00000OO00O0O0 in O0O0OO000OOOO0OO0 .items ()if STAT_judge_x (str (O00O00O000O00OOOO ),TOOLS_get_list (O00O0O0O00O0O0000 ))!=1 })#line:578
                    O0000OOOO0OO000O0 ["查找位置"]=O0O00OOOO00OO0O0O ["查找位置"]#line:579
                    O0000O0O000000O0O .append (O0000OOOO0OO000O0 )#line:582
        O0OOOOO0O0OOO0O0O =pd .concat (O0000O0O000000O0O )#line:583
        O0OOOOO0O0OOO0O0O =O0OOOOO0O0OOO0O0O .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:588
        O0OOOOO0O0OOO0O0O =O0OOOOO0O0OOO0O0O .reset_index ()#line:589
        O0OOOOO0O0OOO0O0O ["All占比"]=round (O0OOOOO0O0OOO0O0O ["All"]/O00O000OO0OO00OOO *100 ,2 )#line:591
        O0OOOOO0O0OOO0O0O =O0OOOOO0O0OOO0O0O .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:592
        for OOO00OOOO00OOOO0O ,O0O00O0O00O00O0O0 in OOOOOO0000O00OO0O .iterrows ():#line:595
            O0OOOOO0O0OOO0O0O .loc [(O0OOOOO0O0OOO0O0O ["关键字标记"].astype (str )==str (O0O00O0O00O00O0O0 ["值"])),"排除值"]=O0O00O0O00O00O0O0 ["排除值"]#line:596
            O0OOOOO0O0OOO0O0O .loc [(O0OOOOO0O0OOO0O0O ["关键字标记"].astype (str )==str (O0O00O0O00O00O0O0 ["值"])),"查找位置"]=O0O00O0O00O00O0O0 ["查找位置"]#line:597
        O0OOOOO0O0OOO0O0O ["排除值"]=O0OOOOO0O0OOO0O0O ["排除值"].fillna ("-没有排除值-")#line:599
        O0OOOOO0O0OOO0O0O ["报表类型"]="PSUR"#line:602
        del O0OOOOO0O0OOO0O0O ["index"]#line:603
        try :#line:604
            del O0OOOOO0O0OOO0O0O ["未正确设置"]#line:605
        except :#line:606
            pass #line:607
        return O0OOOOO0O0OOO0O0O #line:608
    def df_find_all_keword_risk (O0OOO0O0000OO00O0 ,O0OOO0O0000OO0O0O ,*O00O00OO000O0O000 ):#line:611
        ""#line:612
        global TT_biaozhun #line:613
        OOO0O00OO00OO0000 =O0OOO0O0000OO00O0 .df .copy ()#line:615
        O0OOO0OOO000O000O =time .time ()#line:616
        O0000000OO0OO00OO =TT_biaozhun ["关键字表"].copy ()#line:618
        O0O0O0OOO0OOOO000 ="作用对象"#line:620
        OO0OOO0O00OOO00O0 ="报告编码"#line:622
        O0O0OOO00O0O0O0O0 =OOO0O00OO00OO0000 .groupby ([O0O0O0OOO0OOOO000 ]).agg (总数量 =(OO0OOO0O00OOO00O0 ,"nunique"),).reset_index ()#line:625
        OOO0OO00000O00O0O =[O0O0O0OOO0OOOO000 ,O0OOO0O0000OO0O0O ]#line:627
        OO00O00O0OOO0OO00 =OOO0O00OO00OO0000 .groupby (OOO0OO00000O00O0O ).agg (该元素总数量 =(O0O0O0OOO0OOOO000 ,"count"),).reset_index ()#line:631
        OO0O0OOO0O000OOO0 =[]#line:633
        O0O0O0OOO000OOOOO =0 #line:637
        O0OOO00OO00O000OO =int (len (O0O0OOO00O0O0O0O0 ))#line:638
        for OOO0O0O0O0OO000OO ,OOO0O00O00O00O0OO in zip (O0O0OOO00O0O0O0O0 [O0O0O0OOO0OOOO000 ].values ,O0O0OOO00O0O0O0O0 ["总数量"].values ):#line:639
            O0O0O0OOO000OOOOO +=1 #line:640
            O00O000O000O00O00 =OOO0O00OO00OO0000 [(OOO0O00OO00OO0000 [O0O0O0OOO0OOOO000 ]==OOO0O0O0O0OO000OO )].copy ()#line:641
            for OOO000000O00OO000 ,O0O00O00000000OO0 ,O0OO0O00O0OO0OOO0 in zip (O0000000OO0OO00OO ["值"].values ,O0000000OO0OO00OO ["查找位置"].values ,O0000000OO0OO00OO ["排除值"].values ):#line:643
                    O0OOOOOO0OO0000O0 =O00O000O000O00O00 .copy ()#line:644
                    OOOOO0OOOO00O000O =TOOLS_get_list (OOO000000O00OO000 )[0 ]#line:645
                    O0OOOOOO0OO0000O0 ["关键字查找列"]=""#line:647
                    for OOOOOOO00O0000O0O in TOOLS_get_list (O0O00O00000000OO0 ):#line:648
                        O0OOOOOO0OO0000O0 ["关键字查找列"]=O0OOOOOO0OO0000O0 ["关键字查找列"]+O0OOOOOO0OO0000O0 [OOOOOOO00O0000O0O ].astype ("str")#line:649
                    O0OOOOOO0OO0000O0 .loc [O0OOOOOO0OO0000O0 ["关键字查找列"].str .contains (OOO000000O00OO000 ,na =False ),"关键字"]=OOOOO0OOOO00O000O #line:651
                    if str (O0OO0O00O0OO0OOO0 )!="nan":#line:656
                        O0OOOOOO0OO0000O0 =O0OOOOOO0OO0000O0 .loc [~O0OOOOOO0OO0000O0 ["关键字查找列"].str .contains (O0OO0O00O0OO0OOO0 ,na =False )].copy ()#line:657
                    if (len (O0OOOOOO0OO0000O0 ))<1 :#line:659
                        continue #line:661
                    O0OO000OO0OOOOOO0 =STAT_find_keyword_risk (O0OOOOOO0OO0000O0 ,[O0O0O0OOO0OOOO000 ,"关键字"],"关键字",O0OOO0O0000OO0O0O ,int (OOO0O00O00O00O0OO ))#line:663
                    if len (O0OO000OO0OOOOOO0 )>0 :#line:664
                        O0OO000OO0OOOOOO0 ["关键字组合"]=OOO000000O00OO000 #line:665
                        O0OO000OO0OOOOOO0 ["排除值"]=O0OO0O00O0OO0OOO0 #line:666
                        O0OO000OO0OOOOOO0 ["关键字查找列"]=O0O00O00000000OO0 #line:667
                        OO0O0OOO0O000OOO0 .append (O0OO000OO0OOOOOO0 )#line:668
        if len (OO0O0OOO0O000OOO0 )<1 :#line:671
            showinfo (title ="错误信息",message ="该注册证号未检索到任何关键字，规则制定存在缺陷。")#line:672
            return 0 #line:673
        OO0000OOOOOOOOO00 =pd .concat (OO0O0OOO0O000OOO0 )#line:674
        OO0000OOOOOOOOO00 =pd .merge (OO0000OOOOOOOOO00 ,OO00O00O0OOO0OO00 ,on =OOO0OO00000O00O0O ,how ="left")#line:677
        OO0000OOOOOOOOO00 ["关键字数量比例"]=round (OO0000OOOOOOOOO00 ["计数"]/OO0000OOOOOOOOO00 ["该元素总数量"],2 )#line:678
        OO0000OOOOOOOOO00 =OO0000OOOOOOOOO00 .reset_index (drop =True )#line:680
        if len (OO0000OOOOOOOOO00 )>0 :#line:683
            OO0000OOOOOOOOO00 ["风险评分"]=0 #line:684
            OO0000OOOOOOOOO00 ["报表类型"]="keyword_findrisk"+O0OOO0O0000OO0O0O #line:685
            OO0000OOOOOOOOO00 .loc [(OO0000OOOOOOOOO00 ["计数"]>=3 ),"风险评分"]=OO0000OOOOOOOOO00 ["风险评分"]+3 #line:686
            OO0000OOOOOOOOO00 .loc [(OO0000OOOOOOOOO00 ["计数"]>=(OO0000OOOOOOOOO00 ["数量均值"]+OO0000OOOOOOOOO00 ["数量标准差"])),"风险评分"]=OO0000OOOOOOOOO00 ["风险评分"]+1 #line:687
            OO0000OOOOOOOOO00 .loc [(OO0000OOOOOOOOO00 ["计数"]>=OO0000OOOOOOOOO00 ["数量CI"]),"风险评分"]=OO0000OOOOOOOOO00 ["风险评分"]+1 #line:688
            OO0000OOOOOOOOO00 .loc [(OO0000OOOOOOOOO00 ["关键字数量比例"]>0.5 )&(OO0000OOOOOOOOO00 ["计数"]>=3 ),"风险评分"]=OO0000OOOOOOOOO00 ["风险评分"]+1 #line:689
            OO0000OOOOOOOOO00 =OO0000OOOOOOOOO00 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:691
        OOOO00OO0OO0OOOOO =OO0000OOOOOOOOO00 .columns .to_list ()#line:701
        O0O0O00OOO0OOOO0O =OOOO00OO0OO0OOOOO [OOOO00OO0OO0OOOOO .index ("关键字")+1 ]#line:702
        O0000O0OOO0O0O0OO =pd .pivot_table (OO0000OOOOOOOOO00 ,index =O0O0O00OOO0OOOO0O ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:713
        O0000O0OOO0O0O0OO .columns =O0000O0OOO0O0O0OO .columns .droplevel (0 )#line:714
        O0000O0OOO0O0O0OO =pd .merge (O0000O0OOO0O0O0OO ,OO0000OOOOOOOOO00 [[O0O0O00OOO0OOOO0O ,"该元素总数量"]].drop_duplicates (O0O0O00OOO0OOOO0O ),on =[O0O0O00OOO0OOOO0O ],how ="left")#line:717
        del O0000O0OOO0O0O0OO ["All"]#line:719
        O0000O0OOO0O0O0OO .iloc [-1 ,-1 ]=O0000O0OOO0O0O0OO ["该元素总数量"].sum (axis =0 )#line:720
        print ("耗时：",(time .time ()-O0OOO0OOO000O000O ))#line:722
        return O0000O0OOO0O0O0OO #line:725
def Tread_TOOLS_bar (OO0OO0O00OOO00OO0 ):#line:733
         ""#line:734
         O0O000000OOOO0OOO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:735
         O0O00OO00O00OO000 =[pd .read_excel (OO0OO00O00O00OOO0 ,header =0 ,sheet_name =0 )for OO0OO00O00O00OOO0 in O0O000000OOOO0OOO ]#line:736
         OO00OOOOO0OOO0O00 =pd .concat (O0O00OO00O00OO000 ,ignore_index =True )#line:737
         O0OOOO0OOO0O0O000 =pd .pivot_table (OO00OOOOO0OOO0O00 ,index ="对象",columns ="关键词",values =OO0OO0O00OOO00OO0 ,aggfunc ="sum",fill_value ="0",margins =True ,dropna =False ,).reset_index ()#line:747
         del O0OOOO0OOO0O0O000 ["All"]#line:749
         O0OOOO0OOO0O0O000 =O0OOOO0OOO0O0O000 [:-1 ]#line:750
         Tread_TOOLS_tree_Level_2 (O0OOOO0OOO0O0O000 ,0 ,0 )#line:752
def Tread_TOOLS_analysis (OOO0OOOO00OOOO000 ):#line:757
    ""#line:758
    import datetime #line:759
    global TT_ori #line:760
    global TT_biaozhun #line:761
    if len (TT_ori )==0 :#line:763
       showinfo (title ="提示",message ="您尚未导入原始数据。")#line:764
       return 0 #line:765
    if len (TT_biaozhun )==0 :#line:766
       showinfo (title ="提示",message ="您尚未导入规则。")#line:767
       return 0 #line:768
    OOOOOOOOO0O0OO0O0 =TT_biaozhun ["设置"]#line:770
    TT_ori ["作用对象"]=""#line:771
    for O0000OOO00000OOOO in TOOLS_get_list (OOOOOOOOO0O0OO0O0 .loc [0 ,"值"]):#line:772
        TT_ori ["作用对象"]=TT_ori ["作用对象"]+"-"+TT_ori [O0000OOO00000OOOO ].fillna ("未填写").astype ("str")#line:773
    O0O0OO0OOOOO00OOO =Toplevel ()#line:776
    O0O0OO0OOOOO00OOO .title ("单品分析")#line:777
    O0O0OOOO0OOO0000O =O0O0OO0OOOOO00OOO .winfo_screenwidth ()#line:778
    O00OOOO00O0O0O00O =O0O0OO0OOOOO00OOO .winfo_screenheight ()#line:780
    O0OOO000O00OOO0O0 =580 #line:782
    O00O0O0OOO0OO0O00 =80 #line:783
    OO0O0O00OO0OOO00O =(O0O0OOOO0OOO0000O -O0OOO000O00OOO0O0 )/1.7 #line:785
    OO0OOOO0O0OO00O0O =(O00OOOO00O0O0O00O -O00O0O0OOO0OO0O00 )/2 #line:786
    O0O0OO0OOOOO00OOO .geometry ("%dx%d+%d+%d"%(O0OOO000O00OOO0O0 ,O00O0O0OOO0OO0O00 ,OO0O0O00OO0OOO00O ,OO0OOOO0O0OO00O0O ))#line:787
    O00O0O0O0000000OO =Label (O0O0OO0OOOOO00OOO ,text ="作用对象：")#line:790
    O00O0O0O0000000OO .grid (row =1 ,column =0 ,sticky ="w")#line:791
    O000O00O00OOOO0O0 =StringVar ()#line:792
    OO000O0000O0O0OOO =ttk .Combobox (O0O0OO0OOOOO00OOO ,width =25 ,height =10 ,state ="readonly",textvariable =O000O00O00OOOO0O0 )#line:795
    OO000O0000O0O0OOO ["values"]=list (set (TT_ori ["作用对象"].to_list ()))#line:796
    OO000O0000O0O0OOO .current (0 )#line:797
    OO000O0000O0O0OOO .grid (row =1 ,column =1 )#line:798
    O0O0O0O000OO000O0 =Label (O0O0OO0OOOOO00OOO ,text ="分析对象：")#line:800
    O0O0O0O000OO000O0 .grid (row =1 ,column =2 ,sticky ="w")#line:801
    O0000OOOOOO00OO0O =StringVar ()#line:804
    OOO000000O0OOO0O0 =ttk .Combobox (O0O0OO0OOOOO00OOO ,width =15 ,height =10 ,state ="readonly",textvariable =O0000OOOOOO00OO0O )#line:807
    OOO000000O0OOO0O0 ["values"]=["事件发生月份","事件发生季度","产品批号","型号","规格"]#line:808
    OOO000000O0OOO0O0 .current (0 )#line:810
    OOO000000O0OOO0O0 .grid (row =1 ,column =3 )#line:811
    O0OO0OOO0O000OO00 =Label (O0O0OO0OOOOO00OOO ,text ="事件发生起止时间：")#line:816
    O0OO0OOO0O000OO00 .grid (row =2 ,column =0 ,sticky ="w")#line:817
    O00O0O0OO0OO00000 =Entry (O0O0OO0OOOOO00OOO ,width =10 )#line:819
    O00O0O0OO0OO00000 .insert (0 ,min (TT_ori ["事件发生日期"].dt .date ))#line:820
    O00O0O0OO0OO00000 .grid (row =2 ,column =1 ,sticky ="w")#line:821
    OOO0OO00OO0OOOO0O =Entry (O0O0OO0OOOOO00OOO ,width =10 )#line:823
    OOO0OO00OO0OOOO0O .insert (0 ,max (TT_ori ["事件发生日期"].dt .date ))#line:824
    OOO0OO00OO0OOOO0O .grid (row =2 ,column =2 ,sticky ="w")#line:825
    O0OOO00O0000000O0 =Button (O0O0OO0OOOOO00OOO ,text ="原始查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OO000O0000O0O0OOO .get (),OOO000000O0OOO0O0 .get (),O00O0O0OO0OO00000 .get (),OOO0OO00OO0OOOO0O .get (),1 ))#line:835
    O0OOO00O0000000O0 .grid (row =3 ,column =2 ,sticky ="w")#line:836
    O0OOO00O0000000O0 =Button (O0O0OO0OOOOO00OOO ,text ="分类查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OO000O0000O0O0OOO .get (),OOO000000O0OOO0O0 .get (),O00O0O0OO0OO00000 .get (),OOO0OO00OO0OOOO0O .get (),0 ))#line:846
    O0OOO00O0000000O0 .grid (row =3 ,column =3 ,sticky ="w")#line:847
    O0OOO00O0000000O0 =Button (O0O0OO0OOOOO00OOO ,text ="趋势分析",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OO000O0000O0O0OOO .get (),OOO000000O0OOO0O0 .get (),O00O0O0OO0OO00000 .get (),OOO0OO00OO0OOOO0O .get (),2 ))#line:857
    O0OOO00O0000000O0 .grid (row =3 ,column =1 ,sticky ="w")#line:858
def Tread_TOOLS_doing (OO0O00O00OO000OO0 ,O0OO0O0O0OOOOO0OO ,OOOO0000OOO00OO00 ,O0OOO0OOOO000OOOO ,OO0O0O0O0O0000O0O ,OO0O0OO0000O0OO00 ):#line:860
    ""#line:861
    global TT_biaozhun #line:862
    OO0O00O00OO000OO0 =OO0O00O00OO000OO0 [(OO0O00O00OO000OO0 ["作用对象"]==O0OO0O0O0OOOOO0OO )].copy ()#line:863
    O0OOO0OOOO000OOOO =pd .to_datetime (O0OOO0OOOO000OOOO )#line:865
    OO0O0O0O0O0000O0O =pd .to_datetime (OO0O0O0O0O0000O0O )#line:866
    OO0O00O00OO000OO0 =OO0O00O00OO000OO0 [((OO0O00O00OO000OO0 ["事件发生日期"]>=O0OOO0OOOO000OOOO )&(OO0O00O00OO000OO0 ["事件发生日期"]<=OO0O0O0O0O0000O0O ))]#line:867
    text .insert (END ,"\n数据数量："+str (len (OO0O00O00OO000OO0 )))#line:868
    text .see (END )#line:869
    if OO0O0OO0000O0OO00 ==0 :#line:871
        Tread_TOOLS_check (OO0O00O00OO000OO0 ,TT_biaozhun ["关键字表"],0 )#line:872
        return 0 #line:873
    if OO0O0OO0000O0OO00 ==1 :#line:874
        Tread_TOOLS_tree_Level_2 (OO0O00O00OO000OO0 ,1 ,OO0O00O00OO000OO0 )#line:875
        return 0 #line:876
    if len (OO0O00O00OO000OO0 )<1 :#line:877
        showinfo (title ="错误信息",message ="没有符合筛选条件的报告。")#line:878
        return 0 #line:879
    Tread_TOOLS_check (OO0O00O00OO000OO0 ,TT_biaozhun ["关键字表"],1 )#line:880
    Tread_TOOLS_tree_Level_2 (Tread_TOOLS_Countall (OO0O00O00OO000OO0 ).df_find_all_keword_risk (OOOO0000OOO00OO00 ),1 ,0 ,OOOO0000OOO00OO00 )#line:883
def STAT_countx (OO000O00O0O0000OO ):#line:893
    ""#line:894
    return OO000O00O0O0000OO .value_counts ().to_dict ()#line:895
def STAT_countpx (O00OOO00O0O000O0O ,OOOO00O00OOO000OO ):#line:897
    ""#line:898
    return len (O00OOO00O0O000O0O [(O00OOO00O0O000O0O ==OOOO00O00OOO000OO )])#line:899
def STAT_countnpx (O0OOO00O00O0OO0OO ,OO0O00OOO0OOO00O0 ):#line:901
    ""#line:902
    return len (O0OOO00O00O0OO0OO [(O0OOO00O00O0OO0OO not in OO0O00OOO0OOO00O0 )])#line:903
def STAT_get_max (OOOOO00OO00000000 ):#line:905
    ""#line:906
    return OOOOO00OO00000000 .value_counts ().max ()#line:907
def STAT_get_mean (OOOO0OOO000OOOO00 ):#line:909
    ""#line:910
    return round (OOOO0OOO000OOOO00 .value_counts ().mean (),2 )#line:911
def STAT_get_std (O00OOOO0000O0O00O ):#line:913
    ""#line:914
    return round (O00OOOO0000O0O00O .value_counts ().std (ddof =1 ),2 )#line:915
def STAT_get_95ci (OO00O00000O0000OO ):#line:917
    ""#line:918
    return round (np .percentile (OO00O00000O0000OO .value_counts (),97.5 ),2 )#line:919
def STAT_get_mean_std_ci (O0OO0OO0OOOOO00O0 ,OO0OOOOO000000000 ):#line:921
    ""#line:922
    warnings .filterwarnings ("ignore")#line:923
    OOOO00OO0000O00O0 =TOOLS_strdict_to_pd (str (O0OO0OO0OOOOO00O0 ))["content"].values /OO0OOOOO000000000 #line:924
    O00O0OO00OOO000OO =round (OOOO00OO0000O00O0 .mean (),2 )#line:925
    O000O0000O000OO0O =round (OOOO00OO0000O00O0 .std (ddof =1 ),2 )#line:926
    OOOO0O00000OO0OO0 =round (np .percentile (OOOO00OO0000O00O0 ,97.5 ),2 )#line:927
    return pd .Series ((O00O0OO00OOO000OO ,O000O0000O000OO0O ,OOOO0O00000OO0OO0 ))#line:928
def STAT_findx_value (O0O00O0O0000O00O0 ,O000O0OO0O0OO00OO ):#line:930
    ""#line:931
    warnings .filterwarnings ("ignore")#line:932
    O00O0O000000OOO00 =TOOLS_strdict_to_pd (str (O0O00O0O0000O00O0 ))#line:933
    OOOOO0000O00OO0OO =O00O0O000000OOO00 .where (O00O0O000000OOO00 ["index"]==str (O000O0OO0O0OO00OO ))#line:935
    print (OOOOO0000O00OO0OO )#line:936
    return OOOOO0000O00OO0OO #line:937
def STAT_judge_x (OO00000OO000O00OO ,OOOOO0OOO0O0OOOO0 ):#line:939
    ""#line:940
    for O00OOOO0OO00000OO in OOOOO0OOO0O0OOOO0 :#line:941
        if OO00000OO000O00OO .find (O00OOOO0OO00000OO )>-1 :#line:942
            return 1 #line:943
def STAT_basic_risk (O000000000O000O00 ,O000OOOOOOOOOOO00 ,O0O000OOOO0OO00OO ,OO0000OOOO000000O ,O000OOO000O0O0000 ):#line:946
    ""#line:947
    O000000000O000O00 ["风险评分"]=0 #line:948
    O000000000O000O00 .loc [((O000000000O000O00 [O000OOOOOOOOOOO00 ]>=3 )&(O000000000O000O00 [O0O000OOOO0OO00OO ]>=1 ))|(O000000000O000O00 [O000OOOOOOOOOOO00 ]>=5 ),"风险评分"]=O000000000O000O00 ["风险评分"]+5 #line:949
    O000000000O000O00 .loc [(O000000000O000O00 [O0O000OOOO0OO00OO ]>=3 ),"风险评分"]=O000000000O000O00 ["风险评分"]+1 #line:950
    O000000000O000O00 .loc [(O000000000O000O00 [OO0000OOOO000000O ]>=1 ),"风险评分"]=O000000000O000O00 ["风险评分"]+10 #line:951
    O000000000O000O00 ["风险评分"]=O000000000O000O00 ["风险评分"]+O000000000O000O00 [O000OOO000O0O0000 ]/100 #line:952
    return O000000000O000O00 #line:953
def STAT_find_keyword_risk (O0O0O0O0OOOOOO000 ,O0O0OO0O0OO0OO0OO ,O00OO00O0O0000O00 ,O0OO0O0OOO000O00O ,O0OO00000000OO0OO ):#line:957
        ""#line:958
        O0OO000OOO0OOOO0O =O0O0O0O0OOOOOO000 .groupby (O0O0OO0O0OO0OO0OO ).agg (证号关键字总数量 =(O00OO00O0O0000O00 ,"count"),包含元素个数 =(O0OO0O0OOO000O00O ,"nunique"),包含元素 =(O0OO0O0OOO000O00O ,STAT_countx ),).reset_index ()#line:963
        OO0O00O00OO0OOOO0 =O0O0OO0O0OO0OO0OO .copy ()#line:965
        OO0O00O00OO0OOOO0 .append (O0OO0O0OOO000O00O )#line:966
        O0000OO0OOO0O0O0O =O0O0O0O0OOOOOO000 .groupby (OO0O00O00OO0OOOO0 ).agg (计数 =(O0OO0O0OOO000O00O ,"count"),).reset_index ()#line:969
        OOO00O0OO0O000O00 =OO0O00O00OO0OOOO0 .copy ()#line:972
        OOO00O0OO0O000O00 .remove ("关键字")#line:973
        OOOO0OO000O00O0O0 =O0O0O0O0OOOOOO000 .groupby (OOO00O0OO0O000O00 ).agg (该元素总数 =(O0OO0O0OOO000O00O ,"count"),).reset_index ()#line:976
        O0000OO0OOO0O0O0O ["证号总数"]=O0OO00000000OO0OO #line:978
        OO0O0OOOOO000O00O =pd .merge (O0000OO0OOO0O0O0O ,O0OO000OOO0OOOO0O ,on =O0O0OO0O0OO0OO0OO ,how ="left")#line:979
        if len (OO0O0OOOOO000O00O )>0 :#line:981
            OO0O0OOOOO000O00O [['数量均值','数量标准差','数量CI']]=OO0O0OOOOO000O00O .包含元素 .apply (lambda OO000O00OOO0OO0OO :STAT_get_mean_std_ci (OO000O00OOO0OO0OO ,1 ))#line:982
        return OO0O0OOOOO000O00O #line:983
def STAT_find_risk (O0O00O00OOO0000OO ,OO00OOO0000O0000O ,OOOOOOOOOO0O0O0O0 ,OO00O0OO00OOOO00O ):#line:989
        ""#line:990
        O0O0OOOOO0O0O0000 =O0O00O00OOO0000OO .groupby (OO00OOO0000O0000O ).agg (证号总数量 =(OOOOOOOOOO0O0O0O0 ,"count"),包含元素个数 =(OO00O0OO00OOOO00O ,"nunique"),包含元素 =(OO00O0OO00OOOO00O ,STAT_countx ),均值 =(OO00O0OO00OOOO00O ,STAT_get_mean ),标准差 =(OO00O0OO00OOOO00O ,STAT_get_std ),CI上限 =(OO00O0OO00OOOO00O ,STAT_get_95ci ),).reset_index ()#line:998
        O00OOO0O00OO0O0O0 =OO00OOO0000O0000O .copy ()#line:1000
        O00OOO0O00OO0O0O0 .append (OO00O0OO00OOOO00O )#line:1001
        OO0O0O0OOO0000O0O =O0O00O00OOO0000OO .groupby (O00OOO0O00OO0O0O0 ).agg (计数 =(OO00O0OO00OOOO00O ,"count"),严重伤害数 =("伤害",lambda OO0O0O000OO00000O :STAT_countpx (OO0O0O000OO00000O .values ,"严重伤害")),死亡数量 =("伤害",lambda O000OOOO0OOO0000O :STAT_countpx (O000OOOO0OOO0000O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:1008
        OOO0OOO0OO0000O0O =pd .merge (OO0O0O0OOO0000O0O ,O0O0OOOOO0O0O0000 ,on =OO00OOO0000O0000O ,how ="left")#line:1010
        OOO0OOO0OO0000O0O ["风险评分"]=0 #line:1012
        OOO0OOO0OO0000O0O ["报表类型"]="dfx_findrisk"+OO00O0OO00OOOO00O #line:1013
        OOO0OOO0OO0000O0O .loc [((OOO0OOO0OO0000O0O ["计数"]>=3 )&(OOO0OOO0OO0000O0O ["严重伤害数"]>=1 )|(OOO0OOO0OO0000O0O ["计数"]>=5 )),"风险评分"]=OOO0OOO0OO0000O0O ["风险评分"]+5 #line:1014
        OOO0OOO0OO0000O0O .loc [(OOO0OOO0OO0000O0O ["计数"]>=(OOO0OOO0OO0000O0O ["均值"]+OOO0OOO0OO0000O0O ["标准差"])),"风险评分"]=OOO0OOO0OO0000O0O ["风险评分"]+1 #line:1015
        OOO0OOO0OO0000O0O .loc [(OOO0OOO0OO0000O0O ["计数"]>=OOO0OOO0OO0000O0O ["CI上限"]),"风险评分"]=OOO0OOO0OO0000O0O ["风险评分"]+1 #line:1016
        OOO0OOO0OO0000O0O .loc [(OOO0OOO0OO0000O0O ["严重伤害数"]>=3 )&(OOO0OOO0OO0000O0O ["风险评分"]>=7 ),"风险评分"]=OOO0OOO0OO0000O0O ["风险评分"]+1 #line:1017
        OOO0OOO0OO0000O0O .loc [(OOO0OOO0OO0000O0O ["死亡数量"]>=1 ),"风险评分"]=OOO0OOO0OO0000O0O ["风险评分"]+10 #line:1018
        OOO0OOO0OO0000O0O ["风险评分"]=OOO0OOO0OO0000O0O ["风险评分"]+OOO0OOO0OO0000O0O ["单位个数"]/100 #line:1019
        OOO0OOO0OO0000O0O =OOO0OOO0OO0000O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:1020
        return OOO0OOO0OO0000O0O #line:1022
def TOOLS_get_list (OO0O0O00O0OOO00O0 ):#line:1024
    ""#line:1025
    OO0O0O00O0OOO00O0 =str (OO0O0O00O0OOO00O0 )#line:1026
    O000O000OO0O00O0O =[]#line:1027
    O000O000OO0O00O0O .append (OO0O0O00O0OOO00O0 )#line:1028
    O000O000OO0O00O0O =",".join (O000O000OO0O00O0O )#line:1029
    O000O000OO0O00O0O =O000O000OO0O00O0O .split ("|")#line:1030
    OO0000O0OOO0OO0O0 =O000O000OO0O00O0O [:]#line:1031
    O000O000OO0O00O0O =list (set (O000O000OO0O00O0O ))#line:1032
    O000O000OO0O00O0O .sort (key =OO0000O0OOO0OO0O0 .index )#line:1033
    return O000O000OO0O00O0O #line:1034
def TOOLS_get_list0 (OOOO0000OOOO00OO0 ,OO00O0O0OOO0OO00O ,*O00O0OOOOO00OO0OO ):#line:1036
    ""#line:1037
    OOOO0000OOOO00OO0 =str (OOOO0000OOOO00OO0 )#line:1038
    if pd .notnull (OOOO0000OOOO00OO0 ):#line:1040
        try :#line:1041
            if "use("in str (OOOO0000OOOO00OO0 ):#line:1042
                O0O0OO0OOOO0O0OO0 =OOOO0000OOOO00OO0 #line:1043
                O0O0O0000000OOOO0 =re .compile (r"[(](.*?)[)]",re .S )#line:1044
                O00O0000OO000O0OO =re .findall (O0O0O0000000OOOO0 ,O0O0OO0OOOO0O0OO0 )#line:1045
                O00O000OO000000O0 =[]#line:1046
                if ").list"in OOOO0000OOOO00OO0 :#line:1047
                    O00OOOOOOO0OO0OO0 ="配置表/"+str (O00O0000OO000O0OO [0 ])+".xls"#line:1048
                    O00O0O0OOO0OO0O0O =pd .read_excel (O00OOOOOOO0OO0OO0 ,sheet_name =O00O0000OO000O0OO [0 ],header =0 ,index_col =0 ).reset_index ()#line:1051
                    O00O0O0OOO0OO0O0O ["检索关键字"]=O00O0O0OOO0OO0O0O ["检索关键字"].astype (str )#line:1052
                    O00O000OO000000O0 =O00O0O0OOO0OO0O0O ["检索关键字"].tolist ()+O00O000OO000000O0 #line:1053
                if ").file"in OOOO0000OOOO00OO0 :#line:1054
                    O00O000OO000000O0 =OO00O0O0OOO0OO00O [O00O0000OO000O0OO [0 ]].astype (str ).tolist ()+O00O000OO000000O0 #line:1056
                try :#line:1059
                    if "报告类型-新的"in OO00O0O0OOO0OO00O .columns :#line:1060
                        O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1061
                        O00O000OO000000O0 =O00O000OO000000O0 .split (";")#line:1062
                        O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1063
                        O00O000OO000000O0 =O00O000OO000000O0 .split ("；")#line:1064
                        O00O000OO000000O0 =[O0O0000OO00OO0OOO .replace ("（严重）","")for O0O0000OO00OO0OOO in O00O000OO000000O0 ]#line:1065
                        O00O000OO000000O0 =[OO0O0O000O000O000 .replace ("（一般）","")for OO0O0O000O000O000 in O00O000OO000000O0 ]#line:1066
                except :#line:1067
                    pass #line:1068
                O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1071
                O00O000OO000000O0 =O00O000OO000000O0 .split ("、")#line:1072
                O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1073
                O00O000OO000000O0 =O00O000OO000000O0 .split ("，")#line:1074
                O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1075
                O00O000OO000000O0 =O00O000OO000000O0 .split (",")#line:1076
                O0OOOO0000O0OO000 =O00O000OO000000O0 [:]#line:1078
                try :#line:1079
                    if O00O0OOOOO00OO0OO [0 ]==1000 :#line:1080
                      pass #line:1081
                except :#line:1082
                      O00O000OO000000O0 =list (set (O00O000OO000000O0 ))#line:1083
                O00O000OO000000O0 .sort (key =O0OOOO0000O0OO000 .index )#line:1084
            else :#line:1086
                OOOO0000OOOO00OO0 =str (OOOO0000OOOO00OO0 )#line:1087
                O00O000OO000000O0 =[]#line:1088
                O00O000OO000000O0 .append (OOOO0000OOOO00OO0 )#line:1089
                O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1090
                O00O000OO000000O0 =O00O000OO000000O0 .split ("、")#line:1091
                O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1092
                O00O000OO000000O0 =O00O000OO000000O0 .split ("，")#line:1093
                O00O000OO000000O0 =",".join (O00O000OO000000O0 )#line:1094
                O00O000OO000000O0 =O00O000OO000000O0 .split (",")#line:1095
                O0OOOO0000O0OO000 =O00O000OO000000O0 [:]#line:1097
                try :#line:1098
                    if O00O0OOOOO00OO0OO [0 ]==1000 :#line:1099
                      O00O000OO000000O0 =list (set (O00O000OO000000O0 ))#line:1100
                except :#line:1101
                      pass #line:1102
                O00O000OO000000O0 .sort (key =O0OOOO0000O0OO000 .index )#line:1103
                O00O000OO000000O0 .sort (key =O0OOOO0000O0OO000 .index )#line:1104
        except ValueError2 :#line:1106
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:1107
            return False #line:1108
    return O00O000OO000000O0 #line:1110
def TOOLS_strdict_to_pd (OOOO0OOO00OO00OO0 ):#line:1111
    ""#line:1112
    return pd .DataFrame .from_dict (eval (OOOO0OOO00OO00OO0 ),orient ="index",columns =["content"]).reset_index ()#line:1113
def Tread_TOOLS_view_dict (OO0O0000000OOO0OO ,OO00OO0OO0OO0O0O0 ):#line:1115
    ""#line:1116
    OO0OOOO00O0OO0000 =Toplevel ()#line:1117
    OO0OOOO00O0OO0000 .title ("查看数据")#line:1118
    OO0OOOO00O0OO0000 .geometry ("700x500")#line:1119
    OO0OO0OOOO0OOO0O0 =Scrollbar (OO0OOOO00O0OO0000 )#line:1121
    OOOO00OOOO0OO00O0 =Text (OO0OOOO00O0OO0000 ,height =100 ,width =150 )#line:1122
    OO0OO0OOOO0OOO0O0 .pack (side =RIGHT ,fill =Y )#line:1123
    OOOO00OOOO0OO00O0 .pack ()#line:1124
    OO0OO0OOOO0OOO0O0 .config (command =OOOO00OOOO0OO00O0 .yview )#line:1125
    OOOO00OOOO0OO00O0 .config (yscrollcommand =OO0OO0OOOO0OOO0O0 .set )#line:1126
    if OO00OO0OO0OO0O0O0 ==1 :#line:1127
        OOOO00OOOO0OO00O0 .insert (END ,OO0O0000000OOO0OO )#line:1129
        OOOO00OOOO0OO00O0 .insert (END ,"\n\n")#line:1130
        return 0 #line:1131
    for OOOOOO00O00OOO000 in range (len (OO0O0000000OOO0OO )):#line:1132
        OOOO00OOOO0OO00O0 .insert (END ,OO0O0000000OOO0OO .iloc [OOOOOO00O00OOO000 ,0 ])#line:1133
        OOOO00OOOO0OO00O0 .insert (END ,":")#line:1134
        OOOO00OOOO0OO00O0 .insert (END ,OO0O0000000OOO0OO .iloc [OOOOOO00O00OOO000 ,1 ])#line:1135
        OOOO00OOOO0OO00O0 .insert (END ,"\n\n")#line:1136
def Tread_TOOLS_fashenglv (O000OOO0OO0OO0000 ,OOO0OOO0000OO0O0O ):#line:1139
    global TT_biaozhun #line:1140
    O000OOO0OO0OO0000 =pd .merge (O000OOO0OO0OO0000 ,TT_biaozhun [OOO0OOO0000OO0O0O ],on =[OOO0OOO0000OO0O0O ],how ="left").reset_index (drop =True )#line:1141
    O00O000O00O0OOOO0 =O000OOO0OO0OO0000 ["使用次数"].mean ()#line:1143
    O000OOO0OO0OO0000 ["使用次数"]=O000OOO0OO0OO0000 ["使用次数"].fillna (int (O00O000O00O0OOOO0 ))#line:1144
    O0000O0000OO0O000 =O000OOO0OO0OO0000 ["使用次数"][:-1 ].sum ()#line:1145
    O000OOO0OO0OO0000 .iloc [-1 ,-1 ]=O0000O0000OO0O000 #line:1146
    OOO000O0O00O0OOOO =[OOOO0000OO0O0OO00 for OOOO0000OO0O0OO00 in O000OOO0OO0OO0000 .columns if (OOOO0000OO0O0OO00 not in ["使用次数",OOO0OOO0000OO0O0O ])]#line:1147
    for O0O0O00O0O0000000 ,OO00O000O0OO000O0 in O000OOO0OO0OO0000 .iterrows ():#line:1148
        for O000000O0O00O0O0O in OOO000O0O00O0OOOO :#line:1149
            O000OOO0OO0OO0000 .loc [O0O0O00O0O0000000 ,O000000O0O00O0O0O ]=int (OO00O000O0OO000O0 [O000000O0O00O0O0O ])/int (OO00O000O0OO000O0 ["使用次数"])#line:1150
    del O000OOO0OO0OO0000 ["使用次数"]#line:1151
    Tread_TOOLS_tree_Level_2 (O000OOO0OO0OO0000 ,1 ,1 ,OOO0OOO0000OO0O0O )#line:1152
def TOOLS_save_dict (OO0OO0O000OOOO000 ):#line:1154
    ""#line:1155
    OO000OOOOOO0O0OOO =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="【排序后的原始数据】.xls",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1161
    try :#line:1162
        OO0OO0O000OOOO000 ["详细描述T"]=OO0OO0O000OOOO000 ["详细描述T"].astype (str )#line:1163
    except :#line:1164
        pass #line:1165
    try :#line:1166
        OO0OO0O000OOOO000 ["报告编码"]=OO0OO0O000OOOO000 ["报告编码"].astype (str )#line:1167
    except :#line:1168
        pass #line:1169
    try :#line:1170
        OOOOOOO000O0O000O =re .search ("\【(.*?)\】",OO000OOOOOO0O0OOO )#line:1171
        OO0OO0O000OOOO000 ["对象"]=OOOOOOO000O0O000O .group (1 )#line:1172
    except :#line:1173
        pass #line:1174
    O00000O00000OOO00 =pd .ExcelWriter (OO000OOOOOO0O0OOO ,engine ="xlsxwriter")#line:1175
    OO0OO0O000OOOO000 .to_excel (O00000O00000OOO00 ,sheet_name ="字典数据")#line:1176
    O00000O00000OOO00 .close ()#line:1177
    showinfo (title ="提示",message ="文件写入成功。")#line:1178
def Tread_TOOLS_DRAW_histbar (O0O0O00OO0O00O00O ):#line:1182
    ""#line:1183
    OOO00OOOO0O00OOO0 =Toplevel ()#line:1186
    OOO00OOOO0O00OOO0 .title ("直方图")#line:1187
    O00O0OOOOOOOOOO00 =ttk .Frame (OOO00OOOO0O00OOO0 ,height =20 )#line:1188
    O00O0OOOOOOOOOO00 .pack (side =TOP )#line:1189
    O0OOO0O0O00O000OO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1191
    O0O0O000000O0O0O0 =FigureCanvasTkAgg (O0OOO0O0O00O000OO ,master =OOO00OOOO0O00OOO0 )#line:1192
    O0O0O000000O0O0O0 .draw ()#line:1193
    O0O0O000000O0O0O0 .get_tk_widget ().pack (expand =1 )#line:1194
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1196
    plt .rcParams ['axes.unicode_minus']=False #line:1197
    OOO0OO0OO000OOO00 =NavigationToolbar2Tk (O0O0O000000O0O0O0 ,OOO00OOOO0O00OOO0 )#line:1199
    OOO0OO0OO000OOO00 .update ()#line:1200
    O0O0O000000O0O0O0 .get_tk_widget ().pack ()#line:1201
    O000OO0O0000O0O0O =O0OOO0O0O00O000OO .add_subplot (111 )#line:1203
    O000OO0O0000O0O0O .set_title ("直方图")#line:1205
    OOO00OO0OO000OOO0 =O0O0O00OO0O00O00O .columns .to_list ()#line:1207
    OOO00OO0OO000OOO0 .remove ("对象")#line:1208
    O0O0O00000OO000OO =np .arange (len (OOO00OO0OO000OOO0 ))#line:1209
    for OO0OO0OO00OOO0OO0 in OOO00OO0OO000OOO0 :#line:1213
        O0O0O00OO0O00O00O [OO0OO0OO00OOO0OO0 ]=O0O0O00OO0O00O00O [OO0OO0OO00OOO0OO0 ].astype (float )#line:1214
    O0O0O00OO0O00O00O ['数据']=O0O0O00OO0O00O00O [OOO00OO0OO000OOO0 ].values .tolist ()#line:1216
    O000000O00000000O =0 #line:1217
    for O00O00OO00000OO0O ,O000O0OO0OOO00000 in O0O0O00OO0O00O00O .iterrows ():#line:1218
        O000OO0O0000O0O0O .bar ([OO0OO0O000O0000OO +O000000O00000000O for OO0OO0O000O0000OO in O0O0O00000OO000OO ],O0O0O00OO0O00O00O .loc [O00O00OO00000OO0O ,'数据'],label =OOO00OO0OO000OOO0 ,width =0.1 )#line:1219
        for O00O0O0OO0OOO000O ,OOOO00OOO0O0O0OOO in zip ([O00O0O0O0O0000OOO +O000000O00000000O for O00O0O0O0O0000OOO in O0O0O00000OO000OO ],O0O0O00OO0O00O00O .loc [O00O00OO00000OO0O ,'数据']):#line:1222
           O000OO0O0000O0O0O .text (O00O0O0OO0OOO000O -0.015 ,OOOO00OOO0O0O0OOO +0.07 ,str (int (OOOO00OOO0O0O0OOO )),color ='black',size =8 )#line:1223
        O000000O00000000O =O000000O00000000O +0.1 #line:1225
    O000OO0O0000O0O0O .set_xticklabels (O0O0O00OO0O00O00O .columns .to_list (),rotation =-90 ,fontsize =8 )#line:1227
    O000OO0O0000O0O0O .legend (O0O0O00OO0O00O00O ["对象"])#line:1231
    O0O0O000000O0O0O0 .draw ()#line:1234
def Tread_TOOLS_DRAW_make_risk_plot (OO00OOOO0OO000000 ,O00O0O0O0O00O00OO ,O0OOOO000OOO00000 ,O0OOO00O00000O0O0 ,OO0OOOOO0OO000OO0 ):#line:1236
    ""#line:1237
    O00OOO0O0OOO0OOOO =Toplevel ()#line:1240
    O00OOO0O0OOO0OOOO .title (O0OOO00O00000O0O0 )#line:1241
    OO0OO0O000OOOO00O =ttk .Frame (O00OOO0O0OOO0OOOO ,height =20 )#line:1242
    OO0OO0O000OOOO00O .pack (side =TOP )#line:1243
    OO0O00O00OO000OOO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1245
    OO00000O00OOOOOOO =FigureCanvasTkAgg (OO0O00O00OO000OOO ,master =O00OOO0O0OOO0OOOO )#line:1246
    OO00000O00OOOOOOO .draw ()#line:1247
    OO00000O00OOOOOOO .get_tk_widget ().pack (expand =1 )#line:1248
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1250
    plt .rcParams ['axes.unicode_minus']=False #line:1251
    O0OOOO0000000000O =NavigationToolbar2Tk (OO00000O00OOOOOOO ,O00OOO0O0OOO0OOOO )#line:1253
    O0OOOO0000000000O .update ()#line:1254
    OO00000O00OOOOOOO .get_tk_widget ().pack ()#line:1255
    O0OOO00OOOO000O00 =OO0O00O00OO000OOO .add_subplot (111 )#line:1257
    O0OOO00OOOO000O00 .set_title (O0OOO00O00000O0O0 )#line:1259
    O0O0OO0O000OO0OO0 =OO00OOOO0OO000000 [O00O0O0O0O00O00OO ]#line:1260
    if OO0OOOOO0OO000OO0 !=999 :#line:1263
        O0OOO00OOOO000O00 .set_xticklabels (O0O0OO0O000OO0OO0 ,rotation =-90 ,fontsize =8 )#line:1264
    O000O00O0O00O0OO0 =range (0 ,len (O0O0OO0O000OO0OO0 ),1 )#line:1267
    for O0OO0OO00OOOO0OO0 in O0OOOO000OOO00000 :#line:1272
        O00O00OOOOOOO00O0 =OO00OOOO0OO000000 [O0OO0OO00OOOO0OO0 ].astype (float )#line:1273
        if O0OO0OO00OOOO0OO0 =="关注区域":#line:1275
            O0OOO00OOOO000O00 .plot (list (O0O0OO0O000OO0OO0 ),list (O00O00OOOOOOO00O0 ),label =str (O0OO0OO00OOOO0OO0 ),color ="red")#line:1276
        else :#line:1277
            O0OOO00OOOO000O00 .plot (list (O0O0OO0O000OO0OO0 ),list (O00O00OOOOOOO00O0 ),label =str (O0OO0OO00OOOO0OO0 ))#line:1278
        if OO0OOOOO0OO000OO0 ==100 :#line:1281
            for O0OOO00O0000OOO00 ,OO0O0O0OO0000000O in zip (O0O0OO0O000OO0OO0 ,O00O00OOOOOOO00O0 ):#line:1282
                if OO0O0O0OO0000000O ==max (O00O00OOOOOOO00O0 )and OO0O0O0OO0000000O >=3 and len (O0OOOO000OOO00000 )!=1 :#line:1283
                     O0OOO00OOOO000O00 .text (O0OOO00O0000OOO00 ,OO0O0O0OO0000000O ,(str (O0OO0OO00OOOO0OO0 )+":"+str (int (OO0O0O0OO0000000O ))),color ='black',size =8 )#line:1284
                if len (O0OOOO000OOO00000 )==1 and OO0O0O0OO0000000O >=0.01 :#line:1285
                     O0OOO00OOOO000O00 .text (O0OOO00O0000OOO00 ,OO0O0O0OO0000000O ,str (int (OO0O0O0OO0000000O )),color ='black',size =8 )#line:1286
    if len (O0OOOO000OOO00000 )==1 :#line:1296
        O0OOOO000OO0OOOOO =OO00OOOO0OO000000 [O0OOOO000OOO00000 ].astype (float ).values #line:1297
        O0O00O000O0O0O000 =O0OOOO000OO0OOOOO .mean ()#line:1298
        O000OOO0000OO0OOO =O0OOOO000OO0OOOOO .std ()#line:1299
        OOO00OO0OOOOO00O0 =O0O00O000O0O0O000 +3 *O000OOO0000OO0OOO #line:1300
        OO0OO0O0OOO0O00OO =O000OOO0000OO0OOO -3 *O000OOO0000OO0OOO #line:1301
        O0OOO00OOOO000O00 .axhline (O0O00O000O0O0O000 ,color ='r',linestyle ='--',label ='Mean')#line:1303
        O0OOO00OOOO000O00 .axhline (OOO00OO0OOOOO00O0 ,color ='g',linestyle ='--',label ='UCL(μ+3σ)')#line:1304
        O0OOO00OOOO000O00 .axhline (OO0OO0O0OOO0O00OO ,color ='g',linestyle ='--',label ='LCL(μ-3σ)')#line:1305
    O0OOO00OOOO000O00 .set_title ("控制图")#line:1307
    O0OOO00OOOO000O00 .set_xlabel ("项")#line:1308
    OO0O00O00OO000OOO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1309
    O0OO00OOO0OO0O0OO =O0OOO00OOOO000O00 .get_position ()#line:1310
    O0OOO00OOOO000O00 .set_position ([O0OO00OOO0OO0O0OO .x0 ,O0OO00OOO0OO0O0OO .y0 ,O0OO00OOO0OO0O0OO .width *0.7 ,O0OO00OOO0OO0O0OO .height ])#line:1311
    O0OOO00OOOO000O00 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1312
    OOOOO00OOO0OO000O =StringVar ()#line:1315
    O00O0OOOO0OOO0OO0 =ttk .Combobox (OO0OO0O000OOOO00O ,width =15 ,textvariable =OOOOO00OOO0OO000O ,state ='readonly')#line:1316
    O00O0OOOO0OOO0OO0 ['values']=O0OOOO000OOO00000 #line:1317
    O00O0OOOO0OOO0OO0 .pack (side =LEFT )#line:1318
    O00O0OOOO0OOO0OO0 .current (0 )#line:1319
    OOO0O0O0O00O0O0OO =Button (OO0OO0O000OOOO00O ,text ="控制图（单项）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00OOOO0OO000000 ,O00O0O0O0O00O00OO ,[OOOO0O0OOO0OOO0O0 for OOOO0O0OOO0OOO0O0 in O0OOOO000OOO00000 if OOOOO00OOO0OO000O .get ()in OOOO0O0OOO0OOO0O0 ],O0OOO00O00000O0O0 ,OO0OOOOO0OO000OO0 ))#line:1329
    OOO0O0O0O00O0O0OO .pack (side =LEFT ,anchor ="ne")#line:1330
    O00O0O0O0OOOO0O0O =Button (OO0OO0O000OOOO00O ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00OOOO0OO000000 ,O00O0O0O0O00O00OO ,O0OOOO000OOO00000 ,O0OOO00O00000O0O0 ,0 ))#line:1338
    O00O0O0O0OOOO0O0O .pack (side =LEFT ,anchor ="ne")#line:1340
    OO00000O00OOOOOOO .draw ()#line:1341
def Tread_TOOLS_draw (OOO0O0OO000OO0O00 ,O00O00OOO000O0O00 ,OOO000OO000OO00OO ,O0000000OO0O0OO0O ,O0OO0OO0OO000OO0O ):#line:1343
    ""#line:1344
    warnings .filterwarnings ("ignore")#line:1345
    O0O0OO00O0OOOOOO0 =Toplevel ()#line:1346
    O0O0OO00O0OOOOOO0 .title (O00O00OOO000O0O00 )#line:1347
    O0OO0O000O0O0OOO0 =ttk .Frame (O0O0OO00O0OOOOOO0 ,height =20 )#line:1348
    O0OO0O000O0O0OOO0 .pack (side =TOP )#line:1349
    OO0O0O0O00O0OOOOO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1351
    OOOO0O00OOO0O0OOO =FigureCanvasTkAgg (OO0O0O0O00O0OOOOO ,master =O0O0OO00O0OOOOOO0 )#line:1352
    OOOO0O00OOO0O0OOO .draw ()#line:1353
    OOOO0O00OOO0O0OOO .get_tk_widget ().pack (expand =1 )#line:1354
    OO0O0O0OOOO0O0000 =OO0O0O0O00O0OOOOO .add_subplot (111 )#line:1355
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1357
    plt .rcParams ['axes.unicode_minus']=False #line:1358
    OOO0OOOOO000O0O00 =NavigationToolbar2Tk (OOOO0O00OOO0O0OOO ,O0O0OO00O0OOOOOO0 )#line:1360
    OOO0OOOOO000O0O00 .update ()#line:1361
    OOOO0O00OOO0O0OOO .get_tk_widget ().pack ()#line:1363
    try :#line:1366
        O0OO0OO0OO0OOO0O0 =OOO0O0OO000OO0O00 .columns #line:1367
        OOO0O0OO000OO0O00 =OOO0O0OO000OO0O00 .sort_values (by =O0000000OO0O0OO0O ,ascending =[False ],na_position ="last")#line:1368
    except :#line:1369
        O000O00O0000000OO =eval (OOO0O0OO000OO0O00 )#line:1370
        O000O00O0000000OO =pd .DataFrame .from_dict (O000O00O0000000OO ,TT_orient =OOO000OO000OO00OO ,columns =[O0000000OO0O0OO0O ]).reset_index ()#line:1373
        OOO0O0OO000OO0O00 =O000O00O0000000OO .sort_values (by =O0000000OO0O0OO0O ,ascending =[False ],na_position ="last")#line:1374
    if ("日期"in O00O00OOO000O0O00 or "时间"in O00O00OOO000O0O00 or "季度"in O00O00OOO000O0O00 )and "饼图"not in O0OO0OO0OO000OO0O :#line:1378
        OOO0O0OO000OO0O00 [OOO000OO000OO00OO ]=pd .to_datetime (OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],format ="%Y/%m/%d").dt .date #line:1379
        OOO0O0OO000OO0O00 =OOO0O0OO000OO0O00 .sort_values (by =OOO000OO000OO00OO ,ascending =[True ],na_position ="last")#line:1380
    elif "批号"in O00O00OOO000O0O00 :#line:1381
        OOO0O0OO000OO0O00 [OOO000OO000OO00OO ]=OOO0O0OO000OO0O00 [OOO000OO000OO00OO ].astype (str )#line:1382
        OOO0O0OO000OO0O00 =OOO0O0OO000OO0O00 .sort_values (by =OOO000OO000OO00OO ,ascending =[True ],na_position ="last")#line:1383
        OO0O0O0OOOO0O0000 .set_xticklabels (OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],rotation =-90 ,fontsize =8 )#line:1384
    else :#line:1385
        OOO0O0OO000OO0O00 [OOO000OO000OO00OO ]=OOO0O0OO000OO0O00 [OOO000OO000OO00OO ].astype (str )#line:1386
        OO0O0O0OOOO0O0000 .set_xticklabels (OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],rotation =-90 ,fontsize =8 )#line:1387
    O000OO00OO0OO0O0O =OOO0O0OO000OO0O00 [O0000000OO0O0OO0O ]#line:1389
    OOOO0O0OOOO0O0OOO =range (0 ,len (O000OO00OO0OO0O0O ),1 )#line:1390
    OO0O0O0OOOO0O0000 .set_title (O00O00OOO000O0O00 )#line:1392
    if O0OO0OO0OO000OO0O =="柱状图":#line:1396
        OO0O0O0OOOO0O0000 .bar (x =OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],height =O000OO00OO0OO0O0O ,width =0.2 ,color ="#87CEFA")#line:1397
    elif O0OO0OO0OO000OO0O =="饼图":#line:1398
        OO0O0O0OOOO0O0000 .pie (x =O000OO00OO0OO0O0O ,labels =OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],autopct ="%0.2f%%")#line:1399
    elif O0OO0OO0OO000OO0O =="折线图":#line:1400
        OO0O0O0OOOO0O0000 .plot (OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],O000OO00OO0OO0O0O ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:1401
    elif "帕累托图"in str (O0OO0OO0OO000OO0O ):#line:1403
        O00OOOOOOOO00OOO0 =OOO0O0OO000OO0O00 [O0000000OO0O0OO0O ].fillna (0 )#line:1404
        OOO00O000OOO00O00 =O00OOOOOOOO00OOO0 .cumsum ()/O00OOOOOOOO00OOO0 .sum ()*100 #line:1408
        OOO0O0OO000OO0O00 ["百分比"]=round (OOO0O0OO000OO0O00 ["数量"]/O00OOOOOOOO00OOO0 .sum ()*100 ,2 )#line:1409
        OOO0O0OO000OO0O00 ["累计百分比"]=round (OOO00O000OOO00O00 ,2 )#line:1410
        OOOO0OOOOOO000000 =OOO00O000OOO00O00 [OOO00O000OOO00O00 >0.8 ].index [0 ]#line:1411
        O0O00OO000OOOO0OO =O00OOOOOOOO00OOO0 .index .tolist ().index (OOOO0OOOOOO000000 )#line:1412
        OO0O0O0OOOO0O0000 .bar (x =OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],height =O00OOOOOOOO00OOO0 ,color ="C0",label =O0000000OO0O0OO0O )#line:1416
        OOO000OO0OOO0OOOO =OO0O0O0OOOO0O0000 .twinx ()#line:1417
        OOO000OO0OOO0OOOO .plot (OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],OOO00O000OOO00O00 ,color ="C1",alpha =0.6 ,label ="累计比例")#line:1418
        OOO000OO0OOO0OOOO .yaxis .set_major_formatter (PercentFormatter ())#line:1419
        OO0O0O0OOOO0O0000 .tick_params (axis ="y",colors ="C0")#line:1424
        OOO000OO0OOO0OOOO .tick_params (axis ="y",colors ="C1")#line:1425
        for OOOOO0O00OO0OO00O ,OOO00OOOO0OOOO00O ,OO0OO0O0000OO0OOO ,OO0O00000OOO0O0O0 in zip (OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],O00OOOOOOOO00OOO0 ,OOO0O0OO000OO0O00 ["百分比"],OOO0O0OO000OO0O00 ["累计百分比"]):#line:1427
            OO0O0O0OOOO0O0000 .text (OOOOO0O00OO0OO00O ,OOO00OOOO0OOOO00O +0.1 ,str (int (OOO00OOOO0OOOO00O ))+", "+str (int (OO0OO0O0000OO0OOO ))+"%,"+str (int (OO0O00000OOO0O0O0 ))+"%",color ='black',size =8 )#line:1428
        if "超级帕累托图"in str (O0OO0OO0OO000OO0O ):#line:1431
            O00O00000OOO0O0O0 =re .compile (r'[(](.*?)[)]',re .S )#line:1432
            O000OO00OO00O0OO0 =re .findall (O00O00000OOO0O0O0 ,O0OO0OO0OO000OO0O )[0 ]#line:1433
            OO0O0O0OOOO0O0000 .bar (x =OOO0O0OO000OO0O00 [OOO000OO000OO00OO ],height =OOO0O0OO000OO0O00 [O000OO00OO00O0OO0 ],color ="orangered",label =O000OO00OO00O0OO0 )#line:1434
    OO0O0O0O00O0OOOOO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1439
    OOO0O0OOO0O0O0OOO =OO0O0O0OOOO0O0000 .get_position ()#line:1440
    OO0O0O0OOOO0O0000 .set_position ([OOO0O0OOO0O0O0OOO .x0 ,OOO0O0OOO0O0O0OOO .y0 ,OOO0O0OOO0O0O0OOO .width *0.7 ,OOO0O0OOO0O0O0OOO .height ])#line:1441
    OO0O0O0OOOO0O0000 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1442
    OOOO0O00OOO0O0OOO .draw ()#line:1445
    if len (O000OO00OO0OO0O0O )<=20 and O0OO0OO0OO000OO0O !="饼图"and O0OO0OO0OO000OO0O !="帕累托图":#line:1448
        for O0OOO000OO00O0000 ,O00OO0OOOO0OO000O in zip (OOOO0O0OOOO0O0OOO ,O000OO00OO0OO0O0O ):#line:1449
            O0OO000O0O0O00O0O =str (O00OO0OOOO0OO000O )#line:1450
            O000OO000OOO000O0 =(O0OOO000OO00O0000 ,O00OO0OOOO0OO000O +0.3 )#line:1451
            OO0O0O0OOOO0O0000 .annotate (O0OO000O0O0O00O0O ,xy =O000OO000OOO000O0 ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:1452
    O00OO000O0O000O00 =Button (O0OO0O000O0O0OOO0 ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OOO0O0OO000OO0O00 ),)#line:1462
    O00OO000O0O000O00 .pack (side =RIGHT )#line:1463
    OOO0O000O0000OOO0 =Button (O0OO0O000O0O0OOO0 ,relief =GROOVE ,text ="查看原始数据",command =lambda :Tread_TOOLS_view_dict (OOO0O0OO000OO0O00 ,1 ))#line:1467
    OOO0O000O0000OOO0 .pack (side =RIGHT )#line:1468
    O0O00OOO0OOOOO0OO =Button (O0OO0O000O0O0OOO0 ,relief =GROOVE ,text ="饼图",command =lambda :Tread_TOOLS_draw (OOO0O0OO000OO0O00 ,O00O00OOO000O0O00 ,OOO000OO000OO00OO ,O0000000OO0O0OO0O ,"饼图"),)#line:1476
    O0O00OOO0OOOOO0OO .pack (side =LEFT )#line:1477
    O0O00OOO0OOOOO0OO =Button (O0OO0O000O0O0OOO0 ,relief =GROOVE ,text ="柱状图",command =lambda :Tread_TOOLS_draw (OOO0O0OO000OO0O00 ,O00O00OOO000O0O00 ,OOO000OO000OO00OO ,O0000000OO0O0OO0O ,"柱状图"),)#line:1484
    O0O00OOO0OOOOO0OO .pack (side =LEFT )#line:1485
    O0O00OOO0OOOOO0OO =Button (O0OO0O000O0O0OOO0 ,relief =GROOVE ,text ="折线图",command =lambda :Tread_TOOLS_draw (OOO0O0OO000OO0O00 ,O00O00OOO000O0O00 ,OOO000OO000OO00OO ,O0000000OO0O0OO0O ,"折线图"),)#line:1491
    O0O00OOO0OOOOO0OO .pack (side =LEFT )#line:1492
    O0O00OOO0OOOOO0OO =Button (O0OO0O000O0O0OOO0 ,relief =GROOVE ,text ="帕累托图",command =lambda :Tread_TOOLS_draw (OOO0O0OO000OO0O00 ,O00O00OOO000O0O00 ,OOO000OO000OO00OO ,O0000000OO0O0OO0O ,"帕累托图"),)#line:1499
    O0O00OOO0OOOOO0OO .pack (side =LEFT )#line:1500
def helper ():#line:1506
    ""#line:1507
    OO000OOO0O0O0O0O0 =Toplevel ()#line:1508
    OO000OOO0O0O0O0O0 .title ("程序使用帮助")#line:1509
    OO000OOO0O0O0O0O0 .geometry ("700x500")#line:1510
    O000O000OOOO0O0OO =Scrollbar (OO000OOO0O0O0O0O0 )#line:1512
    O000000OO0000O000 =Text (OO000OOO0O0O0O0O0 ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1513
    O000O000OOOO0O0OO .pack (side =RIGHT ,fill =Y )#line:1514
    O000000OO0000O000 .pack ()#line:1515
    O000O000OOOO0O0OO .config (command =O000000OO0000O000 .yview )#line:1516
    O000000OO0000O000 .config (yscrollcommand =O000O000OOOO0O0OO .set )#line:1517
    O000000OO0000O000 .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1522
    O000000OO0000O000 .config (state =DISABLED )#line:1523
def Tread_TOOLS_CLEAN (OOO00OOOO0OOO00OO ):#line:1527
        ""#line:1528
        OOO00OOOO0OOO00OO ["报告编码"]=OOO00OOOO0OOO00OO ["报告编码"].astype ("str")#line:1530
        OOO00OOOO0OOO00OO ["产品批号"]=OOO00OOOO0OOO00OO ["产品批号"].astype ("str")#line:1532
        OOO00OOOO0OOO00OO ["型号"]=OOO00OOOO0OOO00OO ["型号"].astype ("str")#line:1533
        OOO00OOOO0OOO00OO ["规格"]=OOO00OOOO0OOO00OO ["规格"].astype ("str")#line:1534
        OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"]=OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1536
        OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"]=OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1537
        OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"]=OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1538
        OOO00OOOO0OOO00OO ["产品名称"]=OOO00OOOO0OOO00OO ["产品名称"].str .replace ("*","※",regex =False )#line:1540
        OOO00OOOO0OOO00OO ["产品批号"]=OOO00OOOO0OOO00OO ["产品批号"].str .replace ("(","（",regex =False )#line:1542
        OOO00OOOO0OOO00OO ["产品批号"]=OOO00OOOO0OOO00OO ["产品批号"].str .replace (")","）",regex =False )#line:1543
        OOO00OOOO0OOO00OO ["产品批号"]=OOO00OOOO0OOO00OO ["产品批号"].str .replace ("*","※",regex =False )#line:1544
        OOO00OOOO0OOO00OO ['事件发生日期']=pd .to_datetime (OOO00OOOO0OOO00OO ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1547
        OOO00OOOO0OOO00OO ["事件发生月份"]=OOO00OOOO0OOO00OO ["事件发生日期"].dt .to_period ("M").astype (str )#line:1551
        OOO00OOOO0OOO00OO ["事件发生季度"]=OOO00OOOO0OOO00OO ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1552
        OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"]=OOO00OOOO0OOO00OO ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1556
        OOO00OOOO0OOO00OO ["产品批号"]=OOO00OOOO0OOO00OO ["产品批号"].fillna ("未填写")#line:1557
        OOO00OOOO0OOO00OO ["型号"]=OOO00OOOO0OOO00OO ["型号"].fillna ("未填写")#line:1558
        OOO00OOOO0OOO00OO ["规格"]=OOO00OOOO0OOO00OO ["规格"].fillna ("未填写")#line:1559
        return OOO00OOOO0OOO00OO #line:1561
def thread_it (O000O0OOO000O0O0O ,*O00OOO0OOO00O0OOO ):#line:1565
    ""#line:1566
    O0O00OOOOO0OO00OO =threading .Thread (target =O000O0OOO000O0O0O ,args =O00OOO0OOO00O0OOO )#line:1568
    O0O00OOOOO0OO00OO .setDaemon (True )#line:1570
    O0O00OOOOO0OO00OO .start ()#line:1572
def showWelcome ():#line:1575
    ""#line:1576
    O0O000OOOOO000O00 =roox .winfo_screenwidth ()#line:1577
    O0OO0OO00OO00OO0O =roox .winfo_screenheight ()#line:1579
    roox .overrideredirect (True )#line:1581
    roox .attributes ("-alpha",1 )#line:1582
    OO0OO0O00O0OOO00O =(O0O000OOOOO000O00 -475 )/2 #line:1583
    O0OO00OOO0OO0OOO0 =(O0OO0OO00OO00OO0O -200 )/2 #line:1584
    roox .geometry ("675x140+%d+%d"%(OO0OO0O00O0OOO00O ,O0OO00OOO0OO0OOO0 ))#line:1586
    roox ["bg"]="royalblue"#line:1587
    O00OOOO0000O000O0 =Label (roox ,text ="医疗器械警戒趋势分析工具",fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:1590
    O00OOOO0000O000O0 .place (x =0 ,y =15 ,width =675 ,height =90 )#line:1591
    OO0O0O00OO00O0O0O =Label (roox ,text ="Trend Analysis Tools V"+str (version_now ),fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ),)#line:1598
    OO0O0O00OO00O0O0O .place (x =0 ,y =90 ,width =675 ,height =50 )#line:1599
def closeWelcome ():#line:1602
    ""#line:1603
    for OOO0O000OO00OOOOO in range (2 ):#line:1604
        root .attributes ("-alpha",0 )#line:1605
        time .sleep (1 )#line:1606
    root .attributes ("-alpha",1 )#line:1607
    roox .destroy ()#line:1608
if __name__ =='__main__':#line:1612
    pass #line:1613
root =Tk ()#line:1614
root .title ("医疗器械警戒趋势分析工具Trend Analysis Tools V"+str (version_now ))#line:1615
sw_root =root .winfo_screenwidth ()#line:1616
sh_root =root .winfo_screenheight ()#line:1618
ww_root =700 #line:1620
wh_root =620 #line:1621
x_root =(sw_root -ww_root )/2 #line:1623
y_root =(sh_root -wh_root )/2 #line:1624
root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:1625
root .configure (bg ="steelblue")#line:1626
try :#line:1629
    frame0 =ttk .Frame (root ,width =100 ,height =20 )#line:1630
    frame0 .pack (side =LEFT )#line:1631
    B_open_files1 =Button (frame0 ,text ="导入原始数据",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,0 ),)#line:1644
    B_open_files1 .pack ()#line:1645
    B_open_files3 =Button (frame0 ,text ="导入分析规则",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,1 ),)#line:1658
    B_open_files3 .pack ()#line:1659
    B_open_files3 =Button (frame0 ,text ="趋势统计分析",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_analysis ,0 ),)#line:1674
    B_open_files3 .pack ()#line:1675
    B_open_files3 =Button (frame0 ,text ="直方图（数量）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"数量"))#line:1688
    B_open_files3 .pack ()#line:1689
    B_open_files3 =Button (frame0 ,text ="直方图（占比）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"百分比"))#line:1700
    B_open_files3 .pack ()#line:1701
    B_open_files3 =Button (frame0 ,text ="查看帮助文件",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (helper ))#line:1712
    B_open_files3 .pack ()#line:1713
    B_open_files3 =Button (frame0 ,text ="变更注册状态",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (display_random_number ))#line:1724
    B_open_files3 .pack ()#line:1725
except :#line:1726
    pass #line:1727
text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF",font ="微软雅黑")#line:1731
text .pack ()#line:1732
text .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1737
text .insert (END ,"\n\n")#line:1738
def A000 ():#line:1740
    pass #line:1741
setting_cfg =read_setting_cfg ()#line:1745
generate_random_file ()#line:1746
setting_cfg =open_setting_cfg ()#line:1747
if setting_cfg ["settingdir"]==0 :#line:1748
    showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:1749
    filepathu =filedialog .askdirectory ()#line:1750
    path =get_directory_path (filepathu )#line:1751
    update_setting_cfg ("settingdir",path )#line:1752
setting_cfg =open_setting_cfg ()#line:1753
random_number =int (setting_cfg ["sidori"])#line:1754
input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:1755
day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:1756
sid =random_number *2 +183576 #line:1757
if input_number ==sid and day_end =="未过期":#line:1758
    usergroup ="用户组=1"#line:1759
    text .insert (END ,usergroup +"   有效期至：")#line:1760
    text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:1761
else :#line:1762
    text .insert (END ,usergroup )#line:1763
text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:1764
update_software ("treadtools")#line:1765
roox =Toplevel ()#line:1769
tMain =threading .Thread (target =showWelcome )#line:1770
tMain .start ()#line:1771
t1 =threading .Thread (target =closeWelcome )#line:1772
t1 .start ()#line:1773
root .lift ()#line:1774
root .attributes ("-topmost",True )#line:1775
root .attributes ("-topmost",False )#line:1776
root .mainloop ()#line:1778
