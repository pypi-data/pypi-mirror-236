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
version_now ="0.0.4"#line:57
usergroup ="用户组=0"#line:58
setting_cfg =""#line:59
csdir =str (os .path .dirname (__file__ ))#line:61
csdir =csdir +csdir .split ("统计")[0 ][-1 ]#line:62
def extract_zip_file (O00O0O00O0OOO000O ,O0OO0O000O000OOOO ):#line:71
    import zipfile #line:73
    if O0OO0O000O000OOOO =="":#line:74
        return 0 #line:75
    with zipfile .ZipFile (O00O0O00O0OOO000O ,'r')as O0O0O0O0O0O00O0OO :#line:76
        for O0OOO00000000OO00 in O0O0O0O0O0O00O0OO .infolist ():#line:77
            O0OOO00000000OO00 .filename =O0OOO00000000OO00 .filename .encode ('cp437').decode ('gbk')#line:79
            O0O0O0O0O0O00O0OO .extract (O0OOO00000000OO00 ,O0OO0O000O000OOOO )#line:80
def get_directory_path (O0O00OOOOOOOOO0OO ):#line:86
    global csdir #line:88
    if not (os .path .isfile (os .path .join (O0O00OOOOOOOOO0OO ,'规则文件.xls'))):#line:90
        extract_zip_file (csdir +"def.py",O0O00OOOOOOOOO0OO )#line:95
    if O0O00OOOOOOOOO0OO =="":#line:97
        quit ()#line:98
    return O0O00OOOOOOOOO0OO #line:99
def convert_and_compare_dates (OOOOO00O0O000OO0O ):#line:103
    import datetime #line:104
    O0OO00OO00OOOO000 =datetime .datetime .now ()#line:105
    try :#line:107
       O000O0OO0OOO00OO0 =datetime .datetime .strptime (str (int (int (OOOOO00O0O000OO0O )/4 )),"%Y%m%d")#line:108
    except :#line:109
        print ("fail")#line:110
        return "已过期"#line:111
    if O000O0OO0OOO00OO0 >O0OO00OO00OOOO000 :#line:113
        return "未过期"#line:115
    else :#line:116
        return "已过期"#line:117
def read_setting_cfg ():#line:119
    global csdir #line:120
    if os .path .exists (csdir +'setting.cfg'):#line:122
        text .insert (END ,"已完成初始化\n")#line:123
        with open (csdir +'setting.cfg','r')as OOO0O00OOOOOOO0OO :#line:124
            O0O0O000O0O0OO0O0 =eval (OOO0O00OOOOOOO0OO .read ())#line:125
    else :#line:126
        O000OOO0O00OOOO0O =csdir +'setting.cfg'#line:128
        with open (O000OOO0O00OOOO0O ,'w')as OOO0O00OOOOOOO0OO :#line:129
            OOO0O00OOOOOOO0OO .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:130
        text .insert (END ,"未初始化，正在初始化...\n")#line:131
        O0O0O000O0O0OO0O0 =read_setting_cfg ()#line:132
    return O0O0O000O0O0OO0O0 #line:133
def open_setting_cfg ():#line:136
    global csdir #line:137
    with open (csdir +"setting.cfg","r")as O000O00O0O0O0O00O :#line:139
        O0OOO0OO00OO0OO00 =eval (O000O00O0O0O0O00O .read ())#line:141
    return O0OOO0OO00OO0OO00 #line:142
def update_setting_cfg (OO000O00OO00O00OO ,OOOO0O000OOO0OOOO ):#line:144
    global csdir #line:145
    with open (csdir +"setting.cfg","r")as O0O0OOOOO00O00000 :#line:147
        OOOO000O00OOOOOO0 =eval (O0O0OOOOO00O00000 .read ())#line:149
    if OOOO000O00OOOOOO0 [OO000O00OO00O00OO ]==0 or OOOO000O00OOOOOO0 [OO000O00OO00O00OO ]=="11111180000808":#line:151
        OOOO000O00OOOOOO0 [OO000O00OO00O00OO ]=OOOO0O000OOO0OOOO #line:152
        with open (csdir +"setting.cfg","w")as O0O0OOOOO00O00000 :#line:154
            O0O0OOOOO00O00000 .write (str (OOOO000O00OOOOOO0 ))#line:155
def generate_random_file ():#line:158
    OO0O0OOOOOO00OOOO =random .randint (200000 ,299999 )#line:160
    update_setting_cfg ("sidori",OO0O0OOOOOO00OOOO )#line:162
def display_random_number ():#line:164
    global csdir #line:165
    OO000O0000OO0OOO0 =Toplevel ()#line:166
    OO000O0000OO0OOO0 .title ("ID")#line:167
    OO0O00O0O0O00OOOO =OO000O0000OO0OOO0 .winfo_screenwidth ()#line:169
    OOO0OO0OO00OO00O0 =OO000O0000OO0OOO0 .winfo_screenheight ()#line:170
    OO0O00O00OO000OO0 =80 #line:172
    O00O000O0OO000O0O =70 #line:173
    O0O0000O00O0OO000 =(OO0O00O0O0O00OOOO -OO0O00O00OO000OO0 )/2 #line:175
    O000OOO00O00O00OO =(OOO0OO0OO00OO00O0 -O00O000O0OO000O0O )/2 #line:176
    OO000O0000OO0OOO0 .geometry ("%dx%d+%d+%d"%(OO0O00O00OO000OO0 ,O00O000O0OO000O0O ,O0O0000O00O0OO000 ,O000OOO00O00O00OO ))#line:177
    with open (csdir +"setting.cfg","r")as OO0O00OO0OOOO0O0O :#line:180
        OOOOO000OOOO00000 =eval (OO0O00OO0OOOO0O0O .read ())#line:182
    O0OOO000OO00OO000 =int (OOOOO000OOOO00000 ["sidori"])#line:183
    OO0O000OO00OO0OO0 =O0OOO000OO00OO000 *2 +183576 #line:184
    print (OO0O000OO00OO0OO0 )#line:186
    OOOOO000OO00OOOO0 =ttk .Label (OO000O0000OO0OOO0 ,text =f"机器码: {O0OOO000OO00OO000}")#line:188
    OO0O0OO0O0O0O0000 =ttk .Entry (OO000O0000OO0OOO0 )#line:189
    OOOOO000OO00OOOO0 .pack ()#line:192
    OO0O0OO0O0O0O0000 .pack ()#line:193
    ttk .Button (OO000O0000OO0OOO0 ,text ="验证",command =lambda :check_input (OO0O0OO0O0O0O0000 .get (),OO0O000OO00OO0OO0 )).pack ()#line:197
def check_input (O0O0000OO00OOO000 ,OO000OO0OOO0OOOO0 ):#line:199
    try :#line:203
        O00O0O00OO0O0O00O =int (str (O0O0000OO00OOO000 )[0 :6 ])#line:204
        OO000OO0OO0O0OO0O =convert_and_compare_dates (str (O0O0000OO00OOO000 )[6 :14 ])#line:205
    except :#line:206
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:207
        return 0 #line:208
    if O00O0O00OO0O0O00O ==OO000OO0OOO0OOOO0 and OO000OO0OO0O0OO0O =="未过期":#line:210
        update_setting_cfg ("sidfinal",O0O0000OO00OOO000 )#line:211
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:212
        quit ()#line:213
    else :#line:214
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:215
def update_software (OO0OO000000000OO0 ):#line:219
    global version_now #line:221
    OOO0OOOOOOO00OO00 =requests .get (f"https://pypi.org/pypi/{OO0OO000000000OO0}/json").json ()["info"]["version"]#line:222
    text .insert (END ,"当前版本为："+version_now )#line:223
    if OOO0OOOOOOO00OO00 >version_now :#line:224
        text .insert (END ,"\n最新版本为："+OOO0OOOOOOO00OO00 +",正在尝试自动更新....")#line:225
        pip .main (['install',OO0OO000000000OO0 ,'--upgrade'])#line:227
        text .insert (END ,"\n您可以开展工作。")#line:228
def Tread_TOOLS_fileopen (O000OO0OOOO00OO0O ):#line:232
    ""#line:233
    global TT_ori #line:234
    global TT_ori_backup #line:235
    global TT_biaozhun #line:236
    warnings .filterwarnings ('ignore')#line:237
    if O000OO0OOOO00OO0O ==0 :#line:239
        O00O000000O0OO000 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:240
        OO0OOO000OO0O00O0 =[pd .read_excel (O0OOO0OOO00OO0O00 ,header =0 ,sheet_name =0 )for O0OOO0OOO00OO0O00 in O00O000000O0OO000 ]#line:241
        OOOOO0OOOO00O0OO0 =pd .concat (OO0OOO000OO0O00O0 ,ignore_index =True ).drop_duplicates ()#line:242
        try :#line:243
            OOOOO0OOOO00O0OO0 =OOOOO0OOOO00O0OO0 .loc [:,~TT_ori .columns .str .contains ("^Unnamed")]#line:244
        except :#line:245
            pass #line:246
        TT_ori_backup =OOOOO0OOOO00O0OO0 .copy ()#line:247
        TT_ori =Tread_TOOLS_CLEAN (OOOOO0OOOO00O0OO0 ).copy ()#line:248
        text .insert (END ,"\n原始数据导入成功，行数："+str (len (TT_ori )))#line:250
        text .insert (END ,"\n数据校验：\n")#line:251
        text .insert (END ,TT_ori )#line:252
        text .see (END )#line:253
    if O000OO0OOOO00OO0O ==1 :#line:255
        OOOO00OOOOO00O000 =filedialog .askopenfilename (filetypes =[("XLS",".xls")])#line:256
        TT_biaozhun ["关键字表"]=pd .read_excel (OOOO00OOOOO00O000 ,sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:257
        TT_biaozhun ["产品批号"]=pd .read_excel (OOOO00OOOOO00O000 ,sheet_name ="产品批号",header =0 ,index_col =0 ,).reset_index ()#line:258
        TT_biaozhun ["事件发生月份"]=pd .read_excel (OOOO00OOOOO00O000 ,sheet_name ="事件发生月份",header =0 ,index_col =0 ,).reset_index ()#line:259
        TT_biaozhun ["事件发生季度"]=pd .read_excel (OOOO00OOOOO00O000 ,sheet_name ="事件发生季度",header =0 ,index_col =0 ,).reset_index ()#line:260
        TT_biaozhun ["规格"]=pd .read_excel (OOOO00OOOOO00O000 ,sheet_name ="规格",header =0 ,index_col =0 ,).reset_index ()#line:261
        TT_biaozhun ["型号"]=pd .read_excel (OOOO00OOOOO00O000 ,sheet_name ="型号",header =0 ,index_col =0 ,).reset_index ()#line:262
        TT_biaozhun ["设置"]=pd .read_excel (OOOO00OOOOO00O000 ,sheet_name ="设置",header =0 ,index_col =0 ,).reset_index ()#line:263
        Tread_TOOLS_check (TT_ori ,TT_biaozhun ["关键字表"],0 )#line:264
        text .insert (END ,"\n标准导入成功，行数："+str (len (TT_biaozhun )))#line:265
        text .see (END )#line:266
def Tread_TOOLS_check (OO0OO000OOO0O000O ,OO00O00OOO0O00O0O ,O000OO00OO0OOOO0O ):#line:268
        ""#line:269
        global TT_ori #line:270
        O0O0OOOO0O0OOO0O0 =Tread_TOOLS_Countall (OO0OO000OOO0O000O ).df_psur (OO00O00OOO0O00O0O )#line:271
        if O000OO00OO0OOOO0O ==0 :#line:273
            Tread_TOOLS_tree_Level_2 (O0O0OOOO0O0OOO0O0 ,0 ,TT_ori .copy ())#line:275
        O0O0OOOO0O0OOO0O0 ["核验"]=0 #line:278
        O0O0OOOO0O0OOO0O0 .loc [(O0O0OOOO0O0OOO0O0 ["关键字标记"].str .contains ("-其他关键字-",na =False )),"核验"]=O0O0OOOO0O0OOO0O0 .loc [(O0O0OOOO0O0OOO0O0 ["关键字标记"].str .contains ("-其他关键字-",na =False )),"总数量"]#line:279
        if O0O0OOOO0O0OOO0O0 ["核验"].sum ()>0 :#line:280
            showinfo (title ="温馨提示",message ="存在未定义类型的报告"+str (O0O0OOOO0O0OOO0O0 ["核验"].sum ())+"条，趋势分析可能会存在遗漏，建议修正该错误再进行下一步。")#line:281
def Tread_TOOLS_tree_Level_2 (OOO0000000OOO000O ,O0OOOO0O0O0OO0000 ,OOO0OOO00O0O0000O ,*OOO0OO0O0OOOO0000 ):#line:283
    ""#line:284
    global TT_ori_backup #line:286
    OOOO00O0000OO000O =OOO0000000OOO000O .columns .values .tolist ()#line:288
    O0OOOO0O0O0OO0000 =0 #line:289
    OOOOOO0O0OO00OO0O =OOO0000000OOO000O .loc [:]#line:290
    O0000000OO00000OO =0 #line:294
    try :#line:295
        O000O0O000O0000OO =OOO0OO0O0OOOO0000 [0 ]#line:296
        O0000000OO00000OO =1 #line:297
    except :#line:298
        pass #line:299
    O0O00000OOO00OOOO =Toplevel ()#line:302
    O0O00000OOO00OOOO .title ("报表查看器")#line:303
    O00O00OOO000O0OOO =O0O00000OOO00OOOO .winfo_screenwidth ()#line:304
    O0000000000O0O000 =O0O00000OOO00OOOO .winfo_screenheight ()#line:306
    OO0O0000OOO00OOO0 =1300 #line:308
    O00OOO000000O00OO =600 #line:309
    O000O00OO0000O0OO =(O00O00OOO000O0OOO -OO0O0000OOO00OOO0 )/2 #line:311
    O000O000O0OO0O0OO =(O0000000000O0O000 -O00OOO000000O00OO )/2 #line:312
    O0O00000OOO00OOOO .geometry ("%dx%d+%d+%d"%(OO0O0000OOO00OOO0 ,O00OOO000000O00OO ,O000O00OO0000O0OO ,O000O000O0OO0O0OO ))#line:313
    O0O0OOO0OOO00O000 =ttk .Frame (O0O00000OOO00OOOO ,width =1300 ,height =20 )#line:314
    O0O0OOO0OOO00O000 .pack (side =BOTTOM )#line:315
    O000O0OO0OOOOOOO0 =ttk .Frame (O0O00000OOO00OOOO ,width =1300 ,height =20 )#line:317
    O000O0OO0OOOOOOO0 .pack (side =TOP )#line:318
    if 1 >0 :#line:322
        O00O0O0O0000OO00O =Button (O0O0OOO0OOO00O000 ,text ="控制图(所有)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OOOOOO0O0OO00OO0O [:-1 ],O000O0O000O0000OO ,[O00OO000O0O0000OO for O00OO000O0O0000OO in OOOOOO0O0OO00OO0O .columns if (O00OO000O0O0000OO not in [O000O0O000O0000OO ])],"关键字趋势图",100 ),)#line:332
        if O0000000OO00000OO ==1 :#line:333
            O00O0O0O0000OO00O .pack (side =LEFT )#line:334
        O00O0O0O0000OO00O =Button (O0O0OOO0OOO00O000 ,text ="控制图(总数量)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OOOOOO0O0OO00OO0O [:-1 ],O000O0O000O0000OO ,[O00O00O00O0OO0000 for O00O00O00O0OO0000 in OOOOOO0O0OO00OO0O .columns if (O00O00O00O0OO0000 in ["该元素总数量"])],"关键字趋势图",100 ),)#line:344
        if O0000000OO00000OO ==1 :#line:345
            O00O0O0O0000OO00O .pack (side =LEFT )#line:346
        OO0OOO0O00000O00O =Button (O0O0OOO0OOO00O000 ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (OOOOOO0O0OO00OO0O ),)#line:356
        OO0OOO0O00000O00O .pack (side =LEFT )#line:357
        OO0OOO0O00000O00O =Button (O0O0OOO0OOO00O000 ,text ="发生率测算",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_fashenglv (OOOOOO0O0OO00OO0O ,O000O0O000O0000OO ),)#line:367
        if "关键字标记"not in OOOOOO0O0OO00OO0O .columns and "报告编码"not in OOOOOO0O0OO00OO0O .columns :#line:368
            if "对象"not in OOOOOO0O0OO00OO0O .columns :#line:369
                OO0OOO0O00000O00O .pack (side =LEFT )#line:370
        OO0OOO0O00000O00O =Button (O0O0OOO0OOO00O000 ,text ="直方图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_histbar (OOOOOO0O0OO00OO0O .copy ()),)#line:380
        if "对象"in OOOOOO0O0OO00OO0O .columns :#line:381
            OO0OOO0O00000O00O .pack (side =LEFT )#line:382
        OOOO0O00OOO0OOO00 =Button (O0O0OOO0OOO00O000 ,text ="行数:"+str (len (OOOOOO0O0OO00OO0O )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:392
        OOOO0O00OOO0OOO00 .pack (side =LEFT )#line:393
    OOOO00OOO0000O00O =OOOOOO0O0OO00OO0O .values .tolist ()#line:396
    OOOOOOOOOO000O000 =OOOOOO0O0OO00OO0O .columns .values .tolist ()#line:397
    OOOOO0O0000OO0000 =ttk .Treeview (O000O0OO0OOOOOOO0 ,columns =OOOOOOOOOO000O000 ,show ="headings",height =45 )#line:398
    for OO000000000OOO000 in OOOOOOOOOO000O000 :#line:400
        OOOOO0O0000OO0000 .heading (OO000000000OOO000 ,text =OO000000000OOO000 )#line:401
    for O00OO00OO000OO0OO in OOOO00OOO0000O00O :#line:402
        OOOOO0O0000OO0000 .insert ("","end",values =O00OO00OO000OO0OO )#line:403
    for OO0000OOO0OO0OO00 in OOOOOOOOOO000O000 :#line:404
        OOOOO0O0000OO0000 .column (OO0000OOO0OO0OO00 ,minwidth =0 ,width =120 ,stretch =NO )#line:405
    O00O0000O0OO0000O =Scrollbar (O000O0OO0OOOOOOO0 ,orient ="vertical")#line:407
    O00O0000O0OO0000O .pack (side =RIGHT ,fill =Y )#line:408
    O00O0000O0OO0000O .config (command =OOOOO0O0000OO0000 .yview )#line:409
    OOOOO0O0000OO0000 .config (yscrollcommand =O00O0000O0OO0000O .set )#line:410
    OOO0000O0OOO000O0 =Scrollbar (O000O0OO0OOOOOOO0 ,orient ="horizontal")#line:412
    OOO0000O0OOO000O0 .pack (side =BOTTOM ,fill =X )#line:413
    OOO0000O0OOO000O0 .config (command =OOOOO0O0000OO0000 .xview )#line:414
    OOOOO0O0000OO0000 .config (yscrollcommand =O00O0000O0OO0000O .set )#line:415
    def O0OOOOOOO000O0OOO (O0OO000O00OO000OO ,O00O0O0OOOO0O0O00 ,OO0OO0O0OOO0OOO00 ):#line:417
        for O00O00O0000O0000O in OOOOO0O0000OO0000 .selection ():#line:420
            O0OOOOOO0000O0OO0 =OOOOO0O0000OO0000 .item (O00O00O0000O0000O ,"values")#line:421
            OOOOOO00OOO00OOOO =dict (zip (O00O0O0OOOO0O0O00 ,O0OOOOOO0000O0OO0 ))#line:422
        if "该分类下各项计数"in O00O0O0OOOO0O0O00 :#line:424
            O000O0OO00O0O0O0O =OOO0OOO00O0O0000O .copy ()#line:425
            O000O0OO00O0O0O0O ["关键字查找列"]=""#line:426
            for OOOOO00O0O0O0OO00 in TOOLS_get_list (OOOOOO00OOO00OOOO ["查找位置"]):#line:427
                O000O0OO00O0O0O0O ["关键字查找列"]=O000O0OO00O0O0O0O ["关键字查找列"]+O000O0OO00O0O0O0O [OOOOO00O0O0O0OO00 ].astype ("str")#line:428
            OO0O0OOO0O00O0OO0 =O000O0OO00O0O0O0O .loc [O000O0OO00O0O0O0O ["关键字查找列"].str .contains (OOOOOO00OOO00OOOO ["关键字标记"],na =False )].copy ()#line:429
            OO0O0OOO0O00O0OO0 =OO0O0OOO0O00O0OO0 .loc [~OO0O0OOO0O00O0OO0 ["关键字查找列"].str .contains (OOOOOO00OOO00OOOO ["排除值"],na =False )].copy ()#line:430
            Tread_TOOLS_tree_Level_2 (OO0O0OOO0O00O0OO0 ,0 ,OO0O0OOO0O00O0OO0 )#line:436
            return 0 #line:437
        if "报告编码"in O00O0O0OOOO0O0O00 :#line:439
            O0OOO0OO0O0OO0OO0 =Toplevel ()#line:440
            OO00000OOO000OO0O =O0OOO0OO0O0OO0OO0 .winfo_screenwidth ()#line:441
            OOO000O0O000OO00O =O0OOO0OO0O0OO0OO0 .winfo_screenheight ()#line:443
            O00OO0O0000000OOO =800 #line:445
            O0OOOOO00OO000OOO =600 #line:446
            OOOOO00O0O0O0OO00 =(OO00000OOO000OO0O -O00OO0O0000000OOO )/2 #line:448
            OOOOOO0OO0O0O00O0 =(OOO000O0O000OO00O -O0OOOOO00OO000OOO )/2 #line:449
            O0OOO0OO0O0OO0OO0 .geometry ("%dx%d+%d+%d"%(O00OO0O0000000OOO ,O0OOOOO00OO000OOO ,OOOOO00O0O0O0OO00 ,OOOOOO0OO0O0O00O0 ))#line:450
            O0O000OOO0O0O0OOO =ScrolledText (O0OOO0OO0O0OO0OO0 ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:454
            O0O000OOO0O0O0OOO .pack (padx =10 ,pady =10 )#line:455
            def O0O000OO00OOOO0OO (event =None ):#line:456
                O0O000OOO0O0O0OOO .event_generate ('<<Copy>>')#line:457
            def OOO0000O000OOO0O0 (O000OOOOO0O00000O ,O0000OO0000O00OOO ):#line:458
                O00OO0OO0O0O0OO00 =open (O0000OO0000O00OOO ,"w",encoding ='utf-8')#line:459
                O00OO0OO0O0O0OO00 .write (O000OOOOO0O00000O )#line:460
                O00OO0OO0O0O0OO00 .flush ()#line:462
                showinfo (title ="提示信息",message ="保存成功。")#line:463
            O000O000OO0OO0OOO =Menu (O0O000OOO0O0O0OOO ,tearoff =False ,)#line:465
            O000O000OO0OO0OOO .add_command (label ="复制",command =O0O000OO00OOOO0OO )#line:466
            O000O000OO0OO0OOO .add_command (label ="导出",command =lambda :thread_it (OOO0000O000OOO0O0 ,O0O000OOO0O0O0OOO .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =OOOOOO00OOO00OOOO ["报告编码"],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:467
            def O00O00O00OOO00O0O (OO0OOOOO0O0O0O000 ):#line:469
                O000O000OO0OO0OOO .post (OO0OOOOO0O0O0O000 .x_root ,OO0OOOOO0O0O0O000 .y_root )#line:470
            O0O000OOO0O0O0OOO .bind ("<Button-3>",O00O00O00OOO00O0O )#line:471
            O0OOO0OO0O0OO0OO0 .title (OOOOOO00OOO00OOOO ["报告编码"])#line:473
            for O0OOOO00OOO0OOOO0 in range (len (O00O0O0OOOO0O0O00 )):#line:474
                O0O000OOO0O0O0OOO .insert (END ,O00O0O0OOOO0O0O00 [O0OOOO00OOO0OOOO0 ])#line:476
                O0O000OOO0O0O0OOO .insert (END ,"：")#line:477
                O0O000OOO0O0O0OOO .insert (END ,OOOOOO00OOO00OOOO [O00O0O0OOOO0O0O00 [O0OOOO00OOO0OOOO0 ]])#line:478
                O0O000OOO0O0O0OOO .insert (END ,"\n")#line:479
            O0O000OOO0O0O0OOO .config (state =DISABLED )#line:480
            return 0 #line:481
        OOOOOO0OO0O0O00O0 =O0OOOOOO0000O0OO0 [1 :-1 ]#line:484
        OOOOO00O0O0O0OO00 =OO0OO0O0OOO0OOO00 .columns .tolist ()#line:486
        OOOOO00O0O0O0OO00 =OOOOO00O0O0O0OO00 [1 :-1 ]#line:487
        O000O0OO0000OO0OO ={'关键词':OOOOO00O0O0O0OO00 ,'数量':OOOOOO0OO0O0O00O0 }#line:489
        O000O0OO0000OO0OO =pd .DataFrame .from_dict (O000O0OO0000OO0OO )#line:490
        O000O0OO0000OO0OO ["数量"]=O000O0OO0000OO0OO ["数量"].astype (float )#line:491
        Tread_TOOLS_draw (O000O0OO0000OO0OO ,"帕累托图",'关键词','数量',"帕累托图")#line:492
        return 0 #line:493
    OOOOO0O0000OO0000 .bind ("<Double-1>",lambda OO0O00OO0O0O00000 :O0OOOOOOO000O0OOO (OO0O00OO0O0O00000 ,OOOOOOOOOO000O000 ,OOOOOO0O0OO00OO0O ),)#line:501
    OOOOO0O0000OO0000 .pack ()#line:502
class Tread_TOOLS_Countall ():#line:504
    ""#line:505
    def __init__ (O0OOOO0OO00OOOOOO ,OOOOO0OOOO000OOOO ):#line:506
        ""#line:507
        O0OOOO0OO00OOOOOO .df =OOOOO0OOOO000OOOO #line:508
    def df_psur (O0O00OO0OO0O0O0OO ,OO00OO00000OO0OO0 ,*O0000OOO0OOO0O0O0 ):#line:510
        ""#line:511
        global TT_biaozhun #line:512
        O00OO0O00OOO00000 =O0O00OO0OO0O0O0OO .df .copy ()#line:513
        O0O0OOO0O0O0OO0OO =len (O00OO0O00OOO00000 .drop_duplicates ("报告编码"))#line:515
        O0O0OO000O00OO0OO =OO00OO00000OO0OO0 .copy ()#line:518
        OO00O00O00OOO0O00 =TT_biaozhun ["设置"]#line:521
        if OO00O00O00OOO0O00 .loc [1 ,"值"]:#line:522
            OO0OOO0O00O00O0OO =OO00O00O00OOO0O00 .loc [1 ,"值"]#line:523
        else :#line:524
            OO0OOO0O00O00O0OO ="透视列"#line:525
            O00OO0O00OOO00000 [OO0OOO0O00O00O0OO ]="未正确设置"#line:526
        O0000OOOO0OO000OO =""#line:528
        O0OOOOOO00O00O0OO ="-其他关键字-"#line:529
        for O0O0OOOOOO00OO0O0 ,OO00OOO0O00OO0O0O in O0O0OO000O00OO0OO .iterrows ():#line:530
            O0OOOOOO00O00O0OO =O0OOOOOO00O00O0OO +"|"+str (OO00OOO0O00OO0O0O ["值"])#line:531
            O000OOOOOOOOO0OO0 =OO00OOO0O00OO0O0O #line:532
        O000OOOOOOOOO0OO0 [3 ]=O0OOOOOO00O00O0OO #line:533
        O000OOOOOOOOO0OO0 [2 ]="-其他关键字-|"#line:534
        O0O0OO000O00OO0OO .loc [len (O0O0OO000O00OO0OO )]=O000OOOOOOOOO0OO0 #line:535
        O0O0OO000O00OO0OO =O0O0OO000O00OO0OO .reset_index (drop =True )#line:536
        O00OO0O00OOO00000 ["关键字查找列"]=""#line:540
        for O00O00000OOO0OOO0 in TOOLS_get_list (O0O0OO000O00OO0OO .loc [0 ,"查找位置"]):#line:541
            O00OO0O00OOO00000 ["关键字查找列"]=O00OO0O00OOO00000 ["关键字查找列"]+O00OO0O00OOO00000 [O00O00000OOO0OOO0 ].astype ("str")#line:542
        O00OOOOO0O00O0000 =[]#line:545
        for O0O0OOOOOO00OO0O0 ,OO00OOO0O00OO0O0O in O0O0OO000O00OO0OO .iterrows ():#line:546
            OOOOO0OOO00O00OOO =OO00OOO0O00OO0O0O ["值"]#line:547
            O0O00OO00O00000OO =O00OO0O00OOO00000 .loc [O00OO0O00OOO00000 ["关键字查找列"].str .contains (OOOOO0OOO00O00OOO ,na =False )].copy ()#line:548
            if str (OO00OOO0O00OO0O0O ["排除值"])!="nan":#line:549
                O0O00OO00O00000OO =O0O00OO00O00000OO .loc [~O0O00OO00O00000OO ["关键字查找列"].str .contains (str (OO00OOO0O00OO0O0O ["排除值"]),na =False )].copy ()#line:550
            O0O00OO00O00000OO ["关键字标记"]=str (OOOOO0OOO00O00OOO )#line:552
            O0O00OO00O00000OO ["关键字计数"]=1 #line:553
            if len (O0O00OO00O00000OO )>0 :#line:555
                O0000O0O0OOO0O00O =pd .pivot_table (O0O00OO00O00000OO .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns =OO0OOO0O00O00O0OO ,aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:565
                O0000O0O0OOO0O00O =O0000O0O0OOO0O00O [:-1 ]#line:566
                O0000O0O0OOO0O00O .columns =O0000O0O0OOO0O00O .columns .droplevel (0 )#line:567
                O0000O0O0OOO0O00O =O0000O0O0OOO0O00O .reset_index ()#line:568
                if len (O0000O0O0OOO0O00O )>0 :#line:571
                    O0OO0OO0O0O000O0O =str (Counter (TOOLS_get_list0 ("use(关键字查找列).file",O0O00OO00O00000OO ,1000 ))).replace ("Counter({","{")#line:572
                    O0OO0OO0O0O000O0O =O0OO0OO0O0O000O0O .replace ("})","}")#line:573
                    O0OO0OO0O0O000O0O =ast .literal_eval (O0OO0OO0O0O000O0O )#line:574
                    O0000O0O0OOO0O00O .loc [0 ,"事件分类"]=str (TOOLS_get_list (O0000O0O0OOO0O00O .loc [0 ,"关键字标记"])[0 ])#line:576
                    O0000O0O0OOO0O00O .loc [0 ,"该分类下各项计数"]=str ({O00OO0O000O00OO0O :OOO0OO0OO0O0000OO for O00OO0O000O00OO0O ,OOO0OO0OO0O0000OO in O0OO0OO0O0O000O0O .items ()if STAT_judge_x (str (O00OO0O000O00OO0O ),TOOLS_get_list (OOOOO0OOO00O00OOO ))==1 })#line:577
                    O0000O0O0OOO0O00O .loc [0 ,"其他分类各项计数"]=str ({O00OO0O000O0O00OO :OO0O0O0000000O0OO for O00OO0O000O0O00OO ,OO0O0O0000000O0OO in O0OO0OO0O0O000O0O .items ()if STAT_judge_x (str (O00OO0O000O0O00OO ),TOOLS_get_list (OOOOO0OOO00O00OOO ))!=1 })#line:578
                    O0000O0O0OOO0O00O ["查找位置"]=OO00OOO0O00OO0O0O ["查找位置"]#line:579
                    O00OOOOO0O00O0000 .append (O0000O0O0OOO0O00O )#line:582
        O0000OOOO0OO000OO =pd .concat (O00OOOOO0O00O0000 )#line:583
        O0000OOOO0OO000OO =O0000OOOO0OO000OO .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:588
        O0000OOOO0OO000OO =O0000OOOO0OO000OO .reset_index ()#line:589
        O0000OOOO0OO000OO ["All占比"]=round (O0000OOOO0OO000OO ["All"]/O0O0OOO0O0O0OO0OO *100 ,2 )#line:591
        O0000OOOO0OO000OO =O0000OOOO0OO000OO .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:592
        for O00O0O00O00OO000O ,O0O0O0O0OO00OOO00 in O0O0OO000O00OO0OO .iterrows ():#line:595
            O0000OOOO0OO000OO .loc [(O0000OOOO0OO000OO ["关键字标记"].astype (str )==str (O0O0O0O0OO00OOO00 ["值"])),"排除值"]=O0O0O0O0OO00OOO00 ["排除值"]#line:596
            O0000OOOO0OO000OO .loc [(O0000OOOO0OO000OO ["关键字标记"].astype (str )==str (O0O0O0O0OO00OOO00 ["值"])),"查找位置"]=O0O0O0O0OO00OOO00 ["查找位置"]#line:597
        O0000OOOO0OO000OO ["排除值"]=O0000OOOO0OO000OO ["排除值"].fillna ("-没有排除值-")#line:599
        O0000OOOO0OO000OO ["报表类型"]="PSUR"#line:602
        del O0000OOOO0OO000OO ["index"]#line:603
        try :#line:604
            del O0000OOOO0OO000OO ["未正确设置"]#line:605
        except :#line:606
            pass #line:607
        return O0000OOOO0OO000OO #line:608
    def df_find_all_keword_risk (OOO00OO0O0O0000O0 ,OO0000OOO0OO0OO0O ,*O0O00OO000O000O00 ):#line:611
        ""#line:612
        global TT_biaozhun #line:613
        O000OOO0OOOO0O00O =OOO00OO0O0O0000O0 .df .copy ()#line:615
        O00OOO00OO0O0OO00 =time .time ()#line:616
        O00O00OO0OO0O0OOO =TT_biaozhun ["关键字表"].copy ()#line:618
        O0O0OO00OOOO00OO0 ="作用对象"#line:620
        OO0OO000OOOOOOOOO ="报告编码"#line:622
        O000OO0O0OOOOO0O0 =O000OOO0OOOO0O00O .groupby ([O0O0OO00OOOO00OO0 ]).agg (总数量 =(OO0OO000OOOOOOOOO ,"nunique"),).reset_index ()#line:625
        O0O000OOO000000OO =[O0O0OO00OOOO00OO0 ,OO0000OOO0OO0OO0O ]#line:627
        O0000O00OOO00000O =O000OOO0OOOO0O00O .groupby (O0O000OOO000000OO ).agg (该元素总数量 =(O0O0OO00OOOO00OO0 ,"count"),).reset_index ()#line:631
        OO00OO0OO0O0000OO =[]#line:633
        O0OO00O0OO0O0OO00 =0 #line:637
        O0OOO0000OO00000O =int (len (O000OO0O0OOOOO0O0 ))#line:638
        for OOOO0000OOO000OOO ,OOOOOO0000O0OOO00 in zip (O000OO0O0OOOOO0O0 [O0O0OO00OOOO00OO0 ].values ,O000OO0O0OOOOO0O0 ["总数量"].values ):#line:639
            O0OO00O0OO0O0OO00 +=1 #line:640
            O0O00O000O0OOO0O0 =O000OOO0OOOO0O00O [(O000OOO0OOOO0O00O [O0O0OO00OOOO00OO0 ]==OOOO0000OOO000OOO )].copy ()#line:641
            for OO00O0O0O000OO000 ,O000000O000OOOOOO ,O0OOOO0OOOOO000O0 in zip (O00O00OO0OO0O0OOO ["值"].values ,O00O00OO0OO0O0OOO ["查找位置"].values ,O00O00OO0OO0O0OOO ["排除值"].values ):#line:643
                    O0OOO000O00O000O0 =O0O00O000O0OOO0O0 .copy ()#line:644
                    O0000O0OO0O0OO00O =TOOLS_get_list (OO00O0O0O000OO000 )[0 ]#line:645
                    O0OOO000O00O000O0 ["关键字查找列"]=""#line:647
                    for O000OOO0O0O000OO0 in TOOLS_get_list (O000000O000OOOOOO ):#line:648
                        O0OOO000O00O000O0 ["关键字查找列"]=O0OOO000O00O000O0 ["关键字查找列"]+O0OOO000O00O000O0 [O000OOO0O0O000OO0 ].astype ("str")#line:649
                    O0OOO000O00O000O0 .loc [O0OOO000O00O000O0 ["关键字查找列"].str .contains (OO00O0O0O000OO000 ,na =False ),"关键字"]=O0000O0OO0O0OO00O #line:651
                    if str (O0OOOO0OOOOO000O0 )!="nan":#line:656
                        O0OOO000O00O000O0 =O0OOO000O00O000O0 .loc [~O0OOO000O00O000O0 ["关键字查找列"].str .contains (O0OOOO0OOOOO000O0 ,na =False )].copy ()#line:657
                    if (len (O0OOO000O00O000O0 ))<1 :#line:659
                        continue #line:661
                    OOO00O0000O0OO0OO =STAT_find_keyword_risk (O0OOO000O00O000O0 ,[O0O0OO00OOOO00OO0 ,"关键字"],"关键字",OO0000OOO0OO0OO0O ,int (OOOOOO0000O0OOO00 ))#line:663
                    if len (OOO00O0000O0OO0OO )>0 :#line:664
                        OOO00O0000O0OO0OO ["关键字组合"]=OO00O0O0O000OO000 #line:665
                        OOO00O0000O0OO0OO ["排除值"]=O0OOOO0OOOOO000O0 #line:666
                        OOO00O0000O0OO0OO ["关键字查找列"]=O000000O000OOOOOO #line:667
                        OO00OO0OO0O0000OO .append (OOO00O0000O0OO0OO )#line:668
        if len (OO00OO0OO0O0000OO )<1 :#line:671
            showinfo (title ="错误信息",message ="该注册证号未检索到任何关键字，规则制定存在缺陷。")#line:672
            return 0 #line:673
        O0O0O0O00000O0O0O =pd .concat (OO00OO0OO0O0000OO )#line:674
        O0O0O0O00000O0O0O =pd .merge (O0O0O0O00000O0O0O ,O0000O00OOO00000O ,on =O0O000OOO000000OO ,how ="left")#line:677
        O0O0O0O00000O0O0O ["关键字数量比例"]=round (O0O0O0O00000O0O0O ["计数"]/O0O0O0O00000O0O0O ["该元素总数量"],2 )#line:678
        O0O0O0O00000O0O0O =O0O0O0O00000O0O0O .reset_index (drop =True )#line:680
        if len (O0O0O0O00000O0O0O )>0 :#line:683
            O0O0O0O00000O0O0O ["风险评分"]=0 #line:684
            O0O0O0O00000O0O0O ["报表类型"]="keyword_findrisk"+OO0000OOO0OO0OO0O #line:685
            O0O0O0O00000O0O0O .loc [(O0O0O0O00000O0O0O ["计数"]>=3 ),"风险评分"]=O0O0O0O00000O0O0O ["风险评分"]+3 #line:686
            O0O0O0O00000O0O0O .loc [(O0O0O0O00000O0O0O ["计数"]>=(O0O0O0O00000O0O0O ["数量均值"]+O0O0O0O00000O0O0O ["数量标准差"])),"风险评分"]=O0O0O0O00000O0O0O ["风险评分"]+1 #line:687
            O0O0O0O00000O0O0O .loc [(O0O0O0O00000O0O0O ["计数"]>=O0O0O0O00000O0O0O ["数量CI"]),"风险评分"]=O0O0O0O00000O0O0O ["风险评分"]+1 #line:688
            O0O0O0O00000O0O0O .loc [(O0O0O0O00000O0O0O ["关键字数量比例"]>0.5 )&(O0O0O0O00000O0O0O ["计数"]>=3 ),"风险评分"]=O0O0O0O00000O0O0O ["风险评分"]+1 #line:689
            O0O0O0O00000O0O0O =O0O0O0O00000O0O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:691
        O0OO0OOO0O0O0OOO0 =O0O0O0O00000O0O0O .columns .to_list ()#line:701
        OOO0OO0O0O00OO000 =O0OO0OOO0O0O0OOO0 [O0OO0OOO0O0O0OOO0 .index ("关键字")+1 ]#line:702
        OOOO00O000O00O00O =pd .pivot_table (O0O0O0O00000O0O0O ,index =OOO0OO0O0O00OO000 ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:713
        OOOO00O000O00O00O .columns =OOOO00O000O00O00O .columns .droplevel (0 )#line:714
        OOOO00O000O00O00O =pd .merge (OOOO00O000O00O00O ,O0O0O0O00000O0O0O [[OOO0OO0O0O00OO000 ,"该元素总数量"]].drop_duplicates (OOO0OO0O0O00OO000 ),on =[OOO0OO0O0O00OO000 ],how ="left")#line:717
        del OOOO00O000O00O00O ["All"]#line:719
        OOOO00O000O00O00O .iloc [-1 ,-1 ]=OOOO00O000O00O00O ["该元素总数量"].sum (axis =0 )#line:720
        print ("耗时：",(time .time ()-O00OOO00OO0O0OO00 ))#line:722
        return OOOO00O000O00O00O #line:725
def Tread_TOOLS_bar (O0O00OOO00O0OOO00 ):#line:733
         ""#line:734
         OO0000O0O0O000000 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:735
         OOO00O0OOO00000O0 =[pd .read_excel (OOO0O00OOOO00OOOO ,header =0 ,sheet_name =0 )for OOO0O00OOOO00OOOO in OO0000O0O0O000000 ]#line:736
         O00O0000O00O0O0O0 =pd .concat (OOO00O0OOO00000O0 ,ignore_index =True )#line:737
         OO0O0O000O0O00O00 =pd .pivot_table (O00O0000O00O0O0O0 ,index ="对象",columns ="关键词",values =O0O00OOO00O0OOO00 ,aggfunc ="sum",fill_value ="0",margins =True ,dropna =False ,).reset_index ()#line:747
         del OO0O0O000O0O00O00 ["All"]#line:749
         OO0O0O000O0O00O00 =OO0O0O000O0O00O00 [:-1 ]#line:750
         Tread_TOOLS_tree_Level_2 (OO0O0O000O0O00O00 ,0 ,0 )#line:752
def Tread_TOOLS_analysis (O00O00OO000O0000O ):#line:757
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
    O0OO000000O0O0000 =TT_biaozhun ["设置"]#line:770
    TT_ori ["作用对象"]=""#line:771
    for O0OOOOO0O00000O0O in TOOLS_get_list (O0OO000000O0O0000 .loc [0 ,"值"]):#line:772
        TT_ori ["作用对象"]=TT_ori ["作用对象"]+"-"+TT_ori [O0OOOOO0O00000O0O ].fillna ("未填写").astype ("str")#line:773
    O00OOOOO000OO0O00 =Toplevel ()#line:776
    O00OOOOO000OO0O00 .title ("单品分析")#line:777
    O0000OOOO0O00O000 =O00OOOOO000OO0O00 .winfo_screenwidth ()#line:778
    OOO0OOOOOO0O0O0OO =O00OOOOO000OO0O00 .winfo_screenheight ()#line:780
    OOO0O0O0OO0O000O0 =580 #line:782
    OO00O0OO0O0000OOO =80 #line:783
    O0O00O0O00OOOOO00 =(O0000OOOO0O00O000 -OOO0O0O0OO0O000O0 )/1.7 #line:785
    OOOOOO00O000O0OOO =(OOO0OOOOOO0O0O0OO -OO00O0OO0O0000OOO )/2 #line:786
    O00OOOOO000OO0O00 .geometry ("%dx%d+%d+%d"%(OOO0O0O0OO0O000O0 ,OO00O0OO0O0000OOO ,O0O00O0O00OOOOO00 ,OOOOOO00O000O0OOO ))#line:787
    OO00OOO000O000O00 =Label (O00OOOOO000OO0O00 ,text ="作用对象：")#line:790
    OO00OOO000O000O00 .grid (row =1 ,column =0 ,sticky ="w")#line:791
    O00O0O00O0OO0OO00 =StringVar ()#line:792
    OOOOO00OOOO0000O0 =ttk .Combobox (O00OOOOO000OO0O00 ,width =25 ,height =10 ,state ="readonly",textvariable =O00O0O00O0OO0OO00 )#line:795
    OOOOO00OOOO0000O0 ["values"]=list (set (TT_ori ["作用对象"].to_list ()))#line:796
    OOOOO00OOOO0000O0 .current (0 )#line:797
    OOOOO00OOOO0000O0 .grid (row =1 ,column =1 )#line:798
    OO0O0O0O0OOOOO000 =Label (O00OOOOO000OO0O00 ,text ="分析对象：")#line:800
    OO0O0O0O0OOOOO000 .grid (row =1 ,column =2 ,sticky ="w")#line:801
    OO0OOO00OOO000000 =StringVar ()#line:804
    OOOOO00O0O0O000O0 =ttk .Combobox (O00OOOOO000OO0O00 ,width =15 ,height =10 ,state ="readonly",textvariable =OO0OOO00OOO000000 )#line:807
    OOOOO00O0O0O000O0 ["values"]=["事件发生月份","事件发生季度","产品批号","型号","规格"]#line:808
    OOOOO00O0O0O000O0 .current (0 )#line:810
    OOOOO00O0O0O000O0 .grid (row =1 ,column =3 )#line:811
    O00O0O00000O000OO =Label (O00OOOOO000OO0O00 ,text ="事件发生起止时间：")#line:816
    O00O0O00000O000OO .grid (row =2 ,column =0 ,sticky ="w")#line:817
    OOO000O000O0OOOO0 =Entry (O00OOOOO000OO0O00 ,width =10 )#line:819
    OOO000O000O0OOOO0 .insert (0 ,min (TT_ori ["事件发生日期"].dt .date ))#line:820
    OOO000O000O0OOOO0 .grid (row =2 ,column =1 ,sticky ="w")#line:821
    O000000OOOO0O00OO =Entry (O00OOOOO000OO0O00 ,width =10 )#line:823
    O000000OOOO0O00OO .insert (0 ,max (TT_ori ["事件发生日期"].dt .date ))#line:824
    O000000OOOO0O00OO .grid (row =2 ,column =2 ,sticky ="w")#line:825
    OO000OO00OO0O0OOO =Button (O00OOOOO000OO0O00 ,text ="原始查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OOOOO00OOOO0000O0 .get (),OOOOO00O0O0O000O0 .get (),OOO000O000O0OOOO0 .get (),O000000OOOO0O00OO .get (),1 ))#line:835
    OO000OO00OO0O0OOO .grid (row =3 ,column =2 ,sticky ="w")#line:836
    OO000OO00OO0O0OOO =Button (O00OOOOO000OO0O00 ,text ="分类查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OOOOO00OOOO0000O0 .get (),OOOOO00O0O0O000O0 .get (),OOO000O000O0OOOO0 .get (),O000000OOOO0O00OO .get (),0 ))#line:846
    OO000OO00OO0O0OOO .grid (row =3 ,column =3 ,sticky ="w")#line:847
    OO000OO00OO0O0OOO =Button (O00OOOOO000OO0O00 ,text ="趋势分析",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,OOOOO00OOOO0000O0 .get (),OOOOO00O0O0O000O0 .get (),OOO000O000O0OOOO0 .get (),O000000OOOO0O00OO .get (),2 ))#line:857
    OO000OO00OO0O0OOO .grid (row =3 ,column =1 ,sticky ="w")#line:858
def Tread_TOOLS_doing (OOOOOO000O0O0OO0O ,O0OOO00O0O000OO0O ,O0O00OOO000OO0O0O ,O000O00O0OO0OOOO0 ,O0OO00O00OO0OOOO0 ,OOOOO00O0O000O00O ):#line:860
    ""#line:861
    global TT_biaozhun #line:862
    OOOOOO000O0O0OO0O =OOOOOO000O0O0OO0O [(OOOOOO000O0O0OO0O ["作用对象"]==O0OOO00O0O000OO0O )].copy ()#line:863
    O000O00O0OO0OOOO0 =pd .to_datetime (O000O00O0OO0OOOO0 )#line:865
    O0OO00O00OO0OOOO0 =pd .to_datetime (O0OO00O00OO0OOOO0 )#line:866
    OOOOOO000O0O0OO0O =OOOOOO000O0O0OO0O [((OOOOOO000O0O0OO0O ["事件发生日期"]>=O000O00O0OO0OOOO0 )&(OOOOOO000O0O0OO0O ["事件发生日期"]<=O0OO00O00OO0OOOO0 ))]#line:867
    text .insert (END ,"\n数据数量："+str (len (OOOOOO000O0O0OO0O )))#line:868
    text .see (END )#line:869
    if OOOOO00O0O000O00O ==0 :#line:871
        Tread_TOOLS_check (OOOOOO000O0O0OO0O ,TT_biaozhun ["关键字表"],0 )#line:872
        return 0 #line:873
    if OOOOO00O0O000O00O ==1 :#line:874
        Tread_TOOLS_tree_Level_2 (OOOOOO000O0O0OO0O ,1 ,OOOOOO000O0O0OO0O )#line:875
        return 0 #line:876
    if len (OOOOOO000O0O0OO0O )<1 :#line:877
        showinfo (title ="错误信息",message ="没有符合筛选条件的报告。")#line:878
        return 0 #line:879
    Tread_TOOLS_check (OOOOOO000O0O0OO0O ,TT_biaozhun ["关键字表"],1 )#line:880
    Tread_TOOLS_tree_Level_2 (Tread_TOOLS_Countall (OOOOOO000O0O0OO0O ).df_find_all_keword_risk (O0O00OOO000OO0O0O ),1 ,0 ,O0O00OOO000OO0O0O )#line:883
def STAT_countx (OOOO0O0O0OOOOOOOO ):#line:893
    ""#line:894
    return OOOO0O0O0OOOOOOOO .value_counts ().to_dict ()#line:895
def STAT_countpx (O000OO0OOOO0OO0O0 ,O0000O00O0000OOO0 ):#line:897
    ""#line:898
    return len (O000OO0OOOO0OO0O0 [(O000OO0OOOO0OO0O0 ==O0000O00O0000OOO0 )])#line:899
def STAT_countnpx (OOOOO0OO00O0OOO00 ,O00000O000OOO0000 ):#line:901
    ""#line:902
    return len (OOOOO0OO00O0OOO00 [(OOOOO0OO00O0OOO00 not in O00000O000OOO0000 )])#line:903
def STAT_get_max (OO0O0O00OO0O0OOO0 ):#line:905
    ""#line:906
    return OO0O0O00OO0O0OOO0 .value_counts ().max ()#line:907
def STAT_get_mean (O00OOOO00O0O0O0O0 ):#line:909
    ""#line:910
    return round (O00OOOO00O0O0O0O0 .value_counts ().mean (),2 )#line:911
def STAT_get_std (OO0OO0000O0O0O00O ):#line:913
    ""#line:914
    return round (OO0OO0000O0O0O00O .value_counts ().std (ddof =1 ),2 )#line:915
def STAT_get_95ci (O00O0000O0O0OOOOO ):#line:917
    ""#line:918
    return round (np .percentile (O00O0000O0O0OOOOO .value_counts (),97.5 ),2 )#line:919
def STAT_get_mean_std_ci (O0O0OOO0O0O0O0OO0 ,OOOOOOO0O000OOO0O ):#line:921
    ""#line:922
    warnings .filterwarnings ("ignore")#line:923
    OO0OOOO00000000O0 =TOOLS_strdict_to_pd (str (O0O0OOO0O0O0O0OO0 ))["content"].values /OOOOOOO0O000OOO0O #line:924
    OOOOO0OOOOO0OOO0O =round (OO0OOOO00000000O0 .mean (),2 )#line:925
    O0OOO0O0OO00OO00O =round (OO0OOOO00000000O0 .std (ddof =1 ),2 )#line:926
    O0OOO0O0O0OO0OO0O =round (np .percentile (OO0OOOO00000000O0 ,97.5 ),2 )#line:927
    return pd .Series ((OOOOO0OOOOO0OOO0O ,O0OOO0O0OO00OO00O ,O0OOO0O0O0OO0OO0O ))#line:928
def STAT_findx_value (OOO0OO0O0OO00OOOO ,O000O0000O00OO00O ):#line:930
    ""#line:931
    warnings .filterwarnings ("ignore")#line:932
    OO0O0O0O000O00O0O =TOOLS_strdict_to_pd (str (OOO0OO0O0OO00OOOO ))#line:933
    O0O00000O0OOO00O0 =OO0O0O0O000O00O0O .where (OO0O0O0O000O00O0O ["index"]==str (O000O0000O00OO00O ))#line:935
    print (O0O00000O0OOO00O0 )#line:936
    return O0O00000O0OOO00O0 #line:937
def STAT_judge_x (O0O000O00O00OO000 ,OOOOO000OO00OO0O0 ):#line:939
    ""#line:940
    for O00OOOO000O0O0O00 in OOOOO000OO00OO0O0 :#line:941
        if O0O000O00O00OO000 .find (O00OOOO000O0O0O00 )>-1 :#line:942
            return 1 #line:943
def STAT_basic_risk (O000OO0O00OOOO00O ,OOOOO0000000OO00O ,OOOO0O0OO0O0OOOOO ,O00OO000OOOOOOOO0 ,O00OOO00OOOO0O0OO ):#line:946
    ""#line:947
    O000OO0O00OOOO00O ["风险评分"]=0 #line:948
    O000OO0O00OOOO00O .loc [((O000OO0O00OOOO00O [OOOOO0000000OO00O ]>=3 )&(O000OO0O00OOOO00O [OOOO0O0OO0O0OOOOO ]>=1 ))|(O000OO0O00OOOO00O [OOOOO0000000OO00O ]>=5 ),"风险评分"]=O000OO0O00OOOO00O ["风险评分"]+5 #line:949
    O000OO0O00OOOO00O .loc [(O000OO0O00OOOO00O [OOOO0O0OO0O0OOOOO ]>=3 ),"风险评分"]=O000OO0O00OOOO00O ["风险评分"]+1 #line:950
    O000OO0O00OOOO00O .loc [(O000OO0O00OOOO00O [O00OO000OOOOOOOO0 ]>=1 ),"风险评分"]=O000OO0O00OOOO00O ["风险评分"]+10 #line:951
    O000OO0O00OOOO00O ["风险评分"]=O000OO0O00OOOO00O ["风险评分"]+O000OO0O00OOOO00O [O00OOO00OOOO0O0OO ]/100 #line:952
    return O000OO0O00OOOO00O #line:953
def STAT_find_keyword_risk (OOO00O0O00OOOOOO0 ,O00OOOO000O0O0OOO ,O0OOO000O000O000O ,OO0OOOOOOOO0O00OO ,OOOOO00000OO000OO ):#line:957
        ""#line:958
        O0O0OO0O00OOOOO0O =OOO00O0O00OOOOOO0 .groupby (O00OOOO000O0O0OOO ).agg (证号关键字总数量 =(O0OOO000O000O000O ,"count"),包含元素个数 =(OO0OOOOOOOO0O00OO ,"nunique"),包含元素 =(OO0OOOOOOOO0O00OO ,STAT_countx ),).reset_index ()#line:963
        OO0OOOO000OOOOO00 =O00OOOO000O0O0OOO .copy ()#line:965
        OO0OOOO000OOOOO00 .append (OO0OOOOOOOO0O00OO )#line:966
        OO0O0000O000000O0 =OOO00O0O00OOOOOO0 .groupby (OO0OOOO000OOOOO00 ).agg (计数 =(OO0OOOOOOOO0O00OO ,"count"),).reset_index ()#line:969
        OO0O0O0O0O0OO00O0 =OO0OOOO000OOOOO00 .copy ()#line:972
        OO0O0O0O0O0OO00O0 .remove ("关键字")#line:973
        O00O0OO0O0OO00OOO =OOO00O0O00OOOOOO0 .groupby (OO0O0O0O0O0OO00O0 ).agg (该元素总数 =(OO0OOOOOOOO0O00OO ,"count"),).reset_index ()#line:976
        OO0O0000O000000O0 ["证号总数"]=OOOOO00000OO000OO #line:978
        OOO0OOOO000OO0000 =pd .merge (OO0O0000O000000O0 ,O0O0OO0O00OOOOO0O ,on =O00OOOO000O0O0OOO ,how ="left")#line:979
        if len (OOO0OOOO000OO0000 )>0 :#line:981
            OOO0OOOO000OO0000 [['数量均值','数量标准差','数量CI']]=OOO0OOOO000OO0000 .包含元素 .apply (lambda O000O00OOO000000O :STAT_get_mean_std_ci (O000O00OOO000000O ,1 ))#line:982
        return OOO0OOOO000OO0000 #line:983
def STAT_find_risk (O0O00O00OO00O0O0O ,O0O00O00OOO0O000O ,O00O0OOOO0O000OOO ,OOOOOOOOOOOO0O0O0 ):#line:989
        ""#line:990
        O0000O000O0OO0O00 =O0O00O00OO00O0O0O .groupby (O0O00O00OOO0O000O ).agg (证号总数量 =(O00O0OOOO0O000OOO ,"count"),包含元素个数 =(OOOOOOOOOOOO0O0O0 ,"nunique"),包含元素 =(OOOOOOOOOOOO0O0O0 ,STAT_countx ),均值 =(OOOOOOOOOOOO0O0O0 ,STAT_get_mean ),标准差 =(OOOOOOOOOOOO0O0O0 ,STAT_get_std ),CI上限 =(OOOOOOOOOOOO0O0O0 ,STAT_get_95ci ),).reset_index ()#line:998
        O0OOOOO0O00OOO0O0 =O0O00O00OOO0O000O .copy ()#line:1000
        O0OOOOO0O00OOO0O0 .append (OOOOOOOOOOOO0O0O0 )#line:1001
        O0OO00O0000O0OO00 =O0O00O00OO00O0O0O .groupby (O0OOOOO0O00OOO0O0 ).agg (计数 =(OOOOOOOOOOOO0O0O0 ,"count"),严重伤害数 =("伤害",lambda OOOO000000OOO000O :STAT_countpx (OOOO000000OOO000O .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0OO00OO000OO00O :STAT_countpx (OO0OO00OO000OO00O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:1008
        OOOOO0OO00O0O0O00 =pd .merge (O0OO00O0000O0OO00 ,O0000O000O0OO0O00 ,on =O0O00O00OOO0O000O ,how ="left")#line:1010
        OOOOO0OO00O0O0O00 ["风险评分"]=0 #line:1012
        OOOOO0OO00O0O0O00 ["报表类型"]="dfx_findrisk"+OOOOOOOOOOOO0O0O0 #line:1013
        OOOOO0OO00O0O0O00 .loc [((OOOOO0OO00O0O0O00 ["计数"]>=3 )&(OOOOO0OO00O0O0O00 ["严重伤害数"]>=1 )|(OOOOO0OO00O0O0O00 ["计数"]>=5 )),"风险评分"]=OOOOO0OO00O0O0O00 ["风险评分"]+5 #line:1014
        OOOOO0OO00O0O0O00 .loc [(OOOOO0OO00O0O0O00 ["计数"]>=(OOOOO0OO00O0O0O00 ["均值"]+OOOOO0OO00O0O0O00 ["标准差"])),"风险评分"]=OOOOO0OO00O0O0O00 ["风险评分"]+1 #line:1015
        OOOOO0OO00O0O0O00 .loc [(OOOOO0OO00O0O0O00 ["计数"]>=OOOOO0OO00O0O0O00 ["CI上限"]),"风险评分"]=OOOOO0OO00O0O0O00 ["风险评分"]+1 #line:1016
        OOOOO0OO00O0O0O00 .loc [(OOOOO0OO00O0O0O00 ["严重伤害数"]>=3 )&(OOOOO0OO00O0O0O00 ["风险评分"]>=7 ),"风险评分"]=OOOOO0OO00O0O0O00 ["风险评分"]+1 #line:1017
        OOOOO0OO00O0O0O00 .loc [(OOOOO0OO00O0O0O00 ["死亡数量"]>=1 ),"风险评分"]=OOOOO0OO00O0O0O00 ["风险评分"]+10 #line:1018
        OOOOO0OO00O0O0O00 ["风险评分"]=OOOOO0OO00O0O0O00 ["风险评分"]+OOOOO0OO00O0O0O00 ["单位个数"]/100 #line:1019
        OOOOO0OO00O0O0O00 =OOOOO0OO00O0O0O00 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:1020
        return OOOOO0OO00O0O0O00 #line:1022
def TOOLS_get_list (OO000O0O0OO0O0O0O ):#line:1024
    ""#line:1025
    OO000O0O0OO0O0O0O =str (OO000O0O0OO0O0O0O )#line:1026
    O0O00O0O0OOOO0OO0 =[]#line:1027
    O0O00O0O0OOOO0OO0 .append (OO000O0O0OO0O0O0O )#line:1028
    O0O00O0O0OOOO0OO0 =",".join (O0O00O0O0OOOO0OO0 )#line:1029
    O0O00O0O0OOOO0OO0 =O0O00O0O0OOOO0OO0 .split ("|")#line:1030
    O0O00O00O0OO0O00O =O0O00O0O0OOOO0OO0 [:]#line:1031
    O0O00O0O0OOOO0OO0 =list (set (O0O00O0O0OOOO0OO0 ))#line:1032
    O0O00O0O0OOOO0OO0 .sort (key =O0O00O00O0OO0O00O .index )#line:1033
    return O0O00O0O0OOOO0OO0 #line:1034
def TOOLS_get_list0 (OOO0O0OO0O0O0OO00 ,O0OOO0OO000000OOO ,*OO0O0OO000O0O0000 ):#line:1036
    ""#line:1037
    OOO0O0OO0O0O0OO00 =str (OOO0O0OO0O0O0OO00 )#line:1038
    if pd .notnull (OOO0O0OO0O0O0OO00 ):#line:1040
        try :#line:1041
            if "use("in str (OOO0O0OO0O0O0OO00 ):#line:1042
                OO000O000000OO0OO =OOO0O0OO0O0O0OO00 #line:1043
                OOO0O000O0O0O000O =re .compile (r"[(](.*?)[)]",re .S )#line:1044
                OOOOOO00OOO0O0OO0 =re .findall (OOO0O000O0O0O000O ,OO000O000000OO0OO )#line:1045
                O00OOOOOOOO0OOO0O =[]#line:1046
                if ").list"in OOO0O0OO0O0O0OO00 :#line:1047
                    O0OO0OOO0O00O0O0O ="配置表/"+str (OOOOOO00OOO0O0OO0 [0 ])+".xls"#line:1048
                    O00OOOOO0000OOOO0 =pd .read_excel (O0OO0OOO0O00O0O0O ,sheet_name =OOOOOO00OOO0O0OO0 [0 ],header =0 ,index_col =0 ).reset_index ()#line:1051
                    O00OOOOO0000OOOO0 ["检索关键字"]=O00OOOOO0000OOOO0 ["检索关键字"].astype (str )#line:1052
                    O00OOOOOOOO0OOO0O =O00OOOOO0000OOOO0 ["检索关键字"].tolist ()+O00OOOOOOOO0OOO0O #line:1053
                if ").file"in OOO0O0OO0O0O0OO00 :#line:1054
                    O00OOOOOOOO0OOO0O =O0OOO0OO000000OOO [OOOOOO00OOO0O0OO0 [0 ]].astype (str ).tolist ()+O00OOOOOOOO0OOO0O #line:1056
                try :#line:1059
                    if "报告类型-新的"in O0OOO0OO000000OOO .columns :#line:1060
                        O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1061
                        O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split (";")#line:1062
                        O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1063
                        O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split ("；")#line:1064
                        O00OOOOOOOO0OOO0O =[O000000O0OOO0O000 .replace ("（严重）","")for O000000O0OOO0O000 in O00OOOOOOOO0OOO0O ]#line:1065
                        O00OOOOOOOO0OOO0O =[O00O0OO0OOO0O00O0 .replace ("（一般）","")for O00O0OO0OOO0O00O0 in O00OOOOOOOO0OOO0O ]#line:1066
                except :#line:1067
                    pass #line:1068
                O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1071
                O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split ("、")#line:1072
                O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1073
                O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split ("，")#line:1074
                O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1075
                O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split (",")#line:1076
                O0OOO00O00OO00OO0 =O00OOOOOOOO0OOO0O [:]#line:1078
                try :#line:1079
                    if OO0O0OO000O0O0000 [0 ]==1000 :#line:1080
                      pass #line:1081
                except :#line:1082
                      O00OOOOOOOO0OOO0O =list (set (O00OOOOOOOO0OOO0O ))#line:1083
                O00OOOOOOOO0OOO0O .sort (key =O0OOO00O00OO00OO0 .index )#line:1084
            else :#line:1086
                OOO0O0OO0O0O0OO00 =str (OOO0O0OO0O0O0OO00 )#line:1087
                O00OOOOOOOO0OOO0O =[]#line:1088
                O00OOOOOOOO0OOO0O .append (OOO0O0OO0O0O0OO00 )#line:1089
                O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1090
                O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split ("、")#line:1091
                O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1092
                O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split ("，")#line:1093
                O00OOOOOOOO0OOO0O =",".join (O00OOOOOOOO0OOO0O )#line:1094
                O00OOOOOOOO0OOO0O =O00OOOOOOOO0OOO0O .split (",")#line:1095
                O0OOO00O00OO00OO0 =O00OOOOOOOO0OOO0O [:]#line:1097
                try :#line:1098
                    if OO0O0OO000O0O0000 [0 ]==1000 :#line:1099
                      O00OOOOOOOO0OOO0O =list (set (O00OOOOOOOO0OOO0O ))#line:1100
                except :#line:1101
                      pass #line:1102
                O00OOOOOOOO0OOO0O .sort (key =O0OOO00O00OO00OO0 .index )#line:1103
                O00OOOOOOOO0OOO0O .sort (key =O0OOO00O00OO00OO0 .index )#line:1104
        except ValueError2 :#line:1106
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:1107
            return False #line:1108
    return O00OOOOOOOO0OOO0O #line:1110
def TOOLS_strdict_to_pd (O0O000O0OO0OO0O00 ):#line:1111
    ""#line:1112
    return pd .DataFrame .from_dict (eval (O0O000O0OO0OO0O00 ),orient ="index",columns =["content"]).reset_index ()#line:1113
def Tread_TOOLS_view_dict (O0000OOOO0OOOO0O0 ,O000O0O0O0O000O00 ):#line:1115
    ""#line:1116
    OOO0000O00O00OO00 =Toplevel ()#line:1117
    OOO0000O00O00OO00 .title ("查看数据")#line:1118
    OOO0000O00O00OO00 .geometry ("700x500")#line:1119
    O0OO0000O0000O0OO =Scrollbar (OOO0000O00O00OO00 )#line:1121
    OO00O0O00O000000O =Text (OOO0000O00O00OO00 ,height =100 ,width =150 )#line:1122
    O0OO0000O0000O0OO .pack (side =RIGHT ,fill =Y )#line:1123
    OO00O0O00O000000O .pack ()#line:1124
    O0OO0000O0000O0OO .config (command =OO00O0O00O000000O .yview )#line:1125
    OO00O0O00O000000O .config (yscrollcommand =O0OO0000O0000O0OO .set )#line:1126
    if O000O0O0O0O000O00 ==1 :#line:1127
        OO00O0O00O000000O .insert (END ,O0000OOOO0OOOO0O0 )#line:1129
        OO00O0O00O000000O .insert (END ,"\n\n")#line:1130
        return 0 #line:1131
    for O00000O0OO0000O0O in range (len (O0000OOOO0OOOO0O0 )):#line:1132
        OO00O0O00O000000O .insert (END ,O0000OOOO0OOOO0O0 .iloc [O00000O0OO0000O0O ,0 ])#line:1133
        OO00O0O00O000000O .insert (END ,":")#line:1134
        OO00O0O00O000000O .insert (END ,O0000OOOO0OOOO0O0 .iloc [O00000O0OO0000O0O ,1 ])#line:1135
        OO00O0O00O000000O .insert (END ,"\n\n")#line:1136
def Tread_TOOLS_fashenglv (O00O0OOOOOO00OOO0 ,O00OO0000OO000O0O ):#line:1139
    global TT_biaozhun #line:1140
    O00O0OOOOOO00OOO0 =pd .merge (O00O0OOOOOO00OOO0 ,TT_biaozhun [O00OO0000OO000O0O ],on =[O00OO0000OO000O0O ],how ="left").reset_index (drop =True )#line:1141
    O0OO00O0O0OO0OOOO =O00O0OOOOOO00OOO0 ["使用次数"].mean ()#line:1143
    O00O0OOOOOO00OOO0 ["使用次数"]=O00O0OOOOOO00OOO0 ["使用次数"].fillna (int (O0OO00O0O0OO0OOOO ))#line:1144
    OOO0000OOOOO0O0OO =O00O0OOOOOO00OOO0 ["使用次数"][:-1 ].sum ()#line:1145
    O00O0OOOOOO00OOO0 .iloc [-1 ,-1 ]=OOO0000OOOOO0O0OO #line:1146
    OOO000O0O0OO000OO =[OO000000OOOO000OO for OO000000OOOO000OO in O00O0OOOOOO00OOO0 .columns if (OO000000OOOO000OO not in ["使用次数",O00OO0000OO000O0O ])]#line:1147
    for O00OOO00O0OO0OO00 ,O00OOO0OO0000OOO0 in O00O0OOOOOO00OOO0 .iterrows ():#line:1148
        for OOO0OOOO0O0OO00OO in OOO000O0O0OO000OO :#line:1149
            O00O0OOOOOO00OOO0 .loc [O00OOO00O0OO0OO00 ,OOO0OOOO0O0OO00OO ]=int (O00OOO0OO0000OOO0 [OOO0OOOO0O0OO00OO ])/int (O00OOO0OO0000OOO0 ["使用次数"])#line:1150
    del O00O0OOOOOO00OOO0 ["使用次数"]#line:1151
    Tread_TOOLS_tree_Level_2 (O00O0OOOOOO00OOO0 ,1 ,1 ,O00OO0000OO000O0O )#line:1152
def TOOLS_save_dict (O0OOO0O0O00O00000 ):#line:1154
    ""#line:1155
    O0000O0OO0000OOO0 =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="【排序后的原始数据】",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1161
    try :#line:1162
        O0OOO0O0O00O00000 ["详细描述T"]=O0OOO0O0O00O00000 ["详细描述T"].astype (str )#line:1163
    except :#line:1164
        pass #line:1165
    try :#line:1166
        O0OOO0O0O00O00000 ["报告编码"]=O0OOO0O0O00O00000 ["报告编码"].astype (str )#line:1167
    except :#line:1168
        pass #line:1169
    try :#line:1170
        OO0OOOO000OO000OO =re .search ("\【(.*?)\】",O0000O0OO0000OOO0 )#line:1171
        O0OOO0O0O00O00000 ["对象"]=OO0OOOO000OO000OO .group (1 )#line:1172
    except :#line:1173
        pass #line:1174
    O0O00O0O0OO0O0000 =pd .ExcelWriter (O0000O0OO0000OOO0 ,engine ="xlsxwriter")#line:1175
    O0OOO0O0O00O00000 .to_excel (O0O00O0O0OO0O0000 ,sheet_name ="字典数据")#line:1176
    O0O00O0O0OO0O0000 .close ()#line:1177
    showinfo (title ="提示",message ="文件写入成功。")#line:1178
def Tread_TOOLS_DRAW_histbar (OO00OO0OO0OO0000O ):#line:1182
    ""#line:1183
    OO0O0000O0O0OO000 =Toplevel ()#line:1186
    OO0O0000O0O0OO000 .title ("直方图")#line:1187
    OOOOO00O000OO00O0 =ttk .Frame (OO0O0000O0O0OO000 ,height =20 )#line:1188
    OOOOO00O000OO00O0 .pack (side =TOP )#line:1189
    OO000OO00OOOO00OO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1191
    O0O0O000O00OO0000 =FigureCanvasTkAgg (OO000OO00OOOO00OO ,master =OO0O0000O0O0OO000 )#line:1192
    O0O0O000O00OO0000 .draw ()#line:1193
    O0O0O000O00OO0000 .get_tk_widget ().pack (expand =1 )#line:1194
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1196
    plt .rcParams ['axes.unicode_minus']=False #line:1197
    OOOO0000O00OO000O =NavigationToolbar2Tk (O0O0O000O00OO0000 ,OO0O0000O0O0OO000 )#line:1199
    OOOO0000O00OO000O .update ()#line:1200
    O0O0O000O00OO0000 .get_tk_widget ().pack ()#line:1201
    O00O0OOO0O000OO00 =OO000OO00OOOO00OO .add_subplot (111 )#line:1203
    O00O0OOO0O000OO00 .set_title ("直方图")#line:1205
    O00OOOOO0OOOO0O00 =OO00OO0OO0OO0000O .columns .to_list ()#line:1207
    O00OOOOO0OOOO0O00 .remove ("对象")#line:1208
    O00O0000OOOOO0OOO =np .arange (len (O00OOOOO0OOOO0O00 ))#line:1209
    for OO00O0OO000O0OO0O in O00OOOOO0OOOO0O00 :#line:1213
        OO00OO0OO0OO0000O [OO00O0OO000O0OO0O ]=OO00OO0OO0OO0000O [OO00O0OO000O0OO0O ].astype (float )#line:1214
    OO00OO0OO0OO0000O ['数据']=OO00OO0OO0OO0000O [O00OOOOO0OOOO0O00 ].values .tolist ()#line:1216
    OOO0O0OO0OOO000OO =0 #line:1217
    for O0000OOOO00OO0OO0 ,OOOOOOOOOO0OOOO0O in OO00OO0OO0OO0000O .iterrows ():#line:1218
        O00O0OOO0O000OO00 .bar ([O00O0OOOO0O00OO00 +OOO0O0OO0OOO000OO for O00O0OOOO0O00OO00 in O00O0000OOOOO0OOO ],OO00OO0OO0OO0000O .loc [O0000OOOO00OO0OO0 ,'数据'],label =O00OOOOO0OOOO0O00 ,width =0.1 )#line:1219
        for OO00OO0O0O0000OO0 ,OOOOOOOOOO0000O0O in zip ([O00O000O0OO0O00OO +OOO0O0OO0OOO000OO for O00O000O0OO0O00OO in O00O0000OOOOO0OOO ],OO00OO0OO0OO0000O .loc [O0000OOOO00OO0OO0 ,'数据']):#line:1222
           O00O0OOO0O000OO00 .text (OO00OO0O0O0000OO0 -0.015 ,OOOOOOOOOO0000O0O +0.07 ,str (int (OOOOOOOOOO0000O0O )),color ='black',size =8 )#line:1223
        OOO0O0OO0OOO000OO =OOO0O0OO0OOO000OO +0.1 #line:1225
    O00O0OOO0O000OO00 .set_xticklabels (OO00OO0OO0OO0000O .columns .to_list (),rotation =-90 ,fontsize =8 )#line:1227
    O00O0OOO0O000OO00 .legend (OO00OO0OO0OO0000O ["对象"])#line:1231
    O0O0O000O00OO0000 .draw ()#line:1234
def Tread_TOOLS_DRAW_make_risk_plot (O00O000O0O0O0O000 ,O0000O0O00OOO00O0 ,O00O00000OOO00OOO ,O00O0O0O0OO0O0OOO ,OO0O000OO0OOO000O ):#line:1236
    ""#line:1237
    OOO00OOOO0O0O00O0 =Toplevel ()#line:1240
    OOO00OOOO0O0O00O0 .title (O00O0O0O0OO0O0OOO )#line:1241
    O0OOO00OO0O0O00OO =ttk .Frame (OOO00OOOO0O0O00O0 ,height =20 )#line:1242
    O0OOO00OO0O0O00OO .pack (side =TOP )#line:1243
    O00O0000OO0OO00OO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1245
    O000OO0OO0O00OOO0 =FigureCanvasTkAgg (O00O0000OO0OO00OO ,master =OOO00OOOO0O0O00O0 )#line:1246
    O000OO0OO0O00OOO0 .draw ()#line:1247
    O000OO0OO0O00OOO0 .get_tk_widget ().pack (expand =1 )#line:1248
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1250
    plt .rcParams ['axes.unicode_minus']=False #line:1251
    O0O00O00OOO00O0OO =NavigationToolbar2Tk (O000OO0OO0O00OOO0 ,OOO00OOOO0O0O00O0 )#line:1253
    O0O00O00OOO00O0OO .update ()#line:1254
    O000OO0OO0O00OOO0 .get_tk_widget ().pack ()#line:1255
    O00O0000000O00O00 =O00O0000OO0OO00OO .add_subplot (111 )#line:1257
    O00O0000000O00O00 .set_title (O00O0O0O0OO0O0OOO )#line:1259
    O0OO00O00OOO0000O =O00O000O0O0O0O000 [O0000O0O00OOO00O0 ]#line:1260
    if OO0O000OO0OOO000O !=999 :#line:1263
        O00O0000000O00O00 .set_xticklabels (O0OO00O00OOO0000O ,rotation =-90 ,fontsize =8 )#line:1264
    O00O0000OO00OOOO0 =range (0 ,len (O0OO00O00OOO0000O ),1 )#line:1267
    for OO00000O00O0000OO in O00O00000OOO00OOO :#line:1272
        OO0O00O0O0000OOOO =O00O000O0O0O0O000 [OO00000O00O0000OO ].astype (float )#line:1273
        if OO00000O00O0000OO =="关注区域":#line:1275
            O00O0000000O00O00 .plot (list (O0OO00O00OOO0000O ),list (OO0O00O0O0000OOOO ),label =str (OO00000O00O0000OO ),color ="red")#line:1276
        else :#line:1277
            O00O0000000O00O00 .plot (list (O0OO00O00OOO0000O ),list (OO0O00O0O0000OOOO ),label =str (OO00000O00O0000OO ))#line:1278
        if OO0O000OO0OOO000O ==100 :#line:1281
            for OO0000OO0000O0O00 ,O0OOO0O000OO0O00O in zip (O0OO00O00OOO0000O ,OO0O00O0O0000OOOO ):#line:1282
                if O0OOO0O000OO0O00O ==max (OO0O00O0O0000OOOO )and O0OOO0O000OO0O00O >=3 and len (O00O00000OOO00OOO )!=1 :#line:1283
                     O00O0000000O00O00 .text (OO0000OO0000O0O00 ,O0OOO0O000OO0O00O ,(str (OO00000O00O0000OO )+":"+str (int (O0OOO0O000OO0O00O ))),color ='black',size =8 )#line:1284
                if len (O00O00000OOO00OOO )==1 and O0OOO0O000OO0O00O >=0.01 :#line:1285
                     O00O0000000O00O00 .text (OO0000OO0000O0O00 ,O0OOO0O000OO0O00O ,str (int (O0OOO0O000OO0O00O )),color ='black',size =8 )#line:1286
    if len (O00O00000OOO00OOO )==1 :#line:1296
        OOO000OOOO000O0OO =O00O000O0O0O0O000 [O00O00000OOO00OOO ].astype (float ).values #line:1297
        O0O0OOO0O000O0OOO =OOO000OOOO000O0OO .mean ()#line:1298
        OOOOO0O00O000O000 =OOO000OOOO000O0OO .std ()#line:1299
        OOOOO0O00OOOOOOOO =O0O0OOO0O000O0OOO +3 *OOOOO0O00O000O000 #line:1300
        O00O0O000OOOO0O00 =OOOOO0O00O000O000 -3 *OOOOO0O00O000O000 #line:1301
        O00O0000000O00O00 .axhline (O0O0OOO0O000O0OOO ,color ='r',linestyle ='--',label ='Mean')#line:1303
        O00O0000000O00O00 .axhline (OOOOO0O00OOOOOOOO ,color ='g',linestyle ='--',label ='UCL(μ+3σ)')#line:1304
        O00O0000000O00O00 .axhline (O00O0O000OOOO0O00 ,color ='g',linestyle ='--',label ='LCL(μ-3σ)')#line:1305
    O00O0000000O00O00 .set_title ("控制图")#line:1307
    O00O0000000O00O00 .set_xlabel ("项")#line:1308
    O00O0000OO0OO00OO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1309
    O0O0OO0O0OO0OO000 =O00O0000000O00O00 .get_position ()#line:1310
    O00O0000000O00O00 .set_position ([O0O0OO0O0OO0OO000 .x0 ,O0O0OO0O0OO0OO000 .y0 ,O0O0OO0O0OO0OO000 .width *0.7 ,O0O0OO0O0OO0OO000 .height ])#line:1311
    O00O0000000O00O00 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1312
    O0O00O0O000O0O0O0 =StringVar ()#line:1315
    OOOOOO00O0O0O0000 =ttk .Combobox (O0OOO00OO0O0O00OO ,width =15 ,textvariable =O0O00O0O000O0O0O0 ,state ='readonly')#line:1316
    OOOOOO00O0O0O0000 ['values']=O00O00000OOO00OOO #line:1317
    OOOOOO00O0O0O0000 .pack (side =LEFT )#line:1318
    OOOOOO00O0O0O0000 .current (0 )#line:1319
    OOO0O00O0OOOOOOO0 =Button (O0OOO00OO0O0O00OO ,text ="控制图（单项）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O00O000O0O0O0O000 ,O0000O0O00OOO00O0 ,[O0O000OOOO0OO00OO for O0O000OOOO0OO00OO in O00O00000OOO00OOO if O0O00O0O000O0O0O0 .get ()in O0O000OOOO0OO00OO ],O00O0O0O0OO0O0OOO ,OO0O000OO0OOO000O ))#line:1329
    OOO0O00O0OOOOOOO0 .pack (side =LEFT ,anchor ="ne")#line:1330
    OO00OOOOOO0O0O0O0 =Button (O0OOO00OO0O0O00OO ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O00O000O0O0O0O000 ,O0000O0O00OOO00O0 ,O00O00000OOO00OOO ,O00O0O0O0OO0O0OOO ,0 ))#line:1338
    OO00OOOOOO0O0O0O0 .pack (side =LEFT ,anchor ="ne")#line:1340
    O000OO0OO0O00OOO0 .draw ()#line:1341
def Tread_TOOLS_draw (OOO0OO00O00OO0OO0 ,OO0O00O0O000OO0O0 ,OOOO0OOO00OO000OO ,O000O0OOO00O00O00 ,O0OOOO0OOOO0O00O0 ):#line:1343
    ""#line:1344
    warnings .filterwarnings ("ignore")#line:1345
    OO000O0O0O0OO00OO =Toplevel ()#line:1346
    OO000O0O0O0OO00OO .title (OO0O00O0O000OO0O0 )#line:1347
    O0O00OOO0OO0000O0 =ttk .Frame (OO000O0O0O0OO00OO ,height =20 )#line:1348
    O0O00OOO0OO0000O0 .pack (side =TOP )#line:1349
    O00OOO0OOOOOO0000 =Figure (figsize =(12 ,6 ),dpi =100 )#line:1351
    O00O00OO0O0OO00O0 =FigureCanvasTkAgg (O00OOO0OOOOOO0000 ,master =OO000O0O0O0OO00OO )#line:1352
    O00O00OO0O0OO00O0 .draw ()#line:1353
    O00O00OO0O0OO00O0 .get_tk_widget ().pack (expand =1 )#line:1354
    OOO0O0O000OO0O0O0 =O00OOO0OOOOOO0000 .add_subplot (111 )#line:1355
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1357
    plt .rcParams ['axes.unicode_minus']=False #line:1358
    O0OO000OO0O000OOO =NavigationToolbar2Tk (O00O00OO0O0OO00O0 ,OO000O0O0O0OO00OO )#line:1360
    O0OO000OO0O000OOO .update ()#line:1361
    O00O00OO0O0OO00O0 .get_tk_widget ().pack ()#line:1363
    try :#line:1366
        O0OOOOOO0000O0O00 =OOO0OO00O00OO0OO0 .columns #line:1367
        OOO0OO00O00OO0OO0 =OOO0OO00O00OO0OO0 .sort_values (by =O000O0OOO00O00O00 ,ascending =[False ],na_position ="last")#line:1368
    except :#line:1369
        OO00O0O000OO0OOO0 =eval (OOO0OO00O00OO0OO0 )#line:1370
        OO00O0O000OO0OOO0 =pd .DataFrame .from_dict (OO00O0O000OO0OOO0 ,TT_orient =OOOO0OOO00OO000OO ,columns =[O000O0OOO00O00O00 ]).reset_index ()#line:1373
        OOO0OO00O00OO0OO0 =OO00O0O000OO0OOO0 .sort_values (by =O000O0OOO00O00O00 ,ascending =[False ],na_position ="last")#line:1374
    if ("日期"in OO0O00O0O000OO0O0 or "时间"in OO0O00O0O000OO0O0 or "季度"in OO0O00O0O000OO0O0 )and "饼图"not in O0OOOO0OOOO0O00O0 :#line:1378
        OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ]=pd .to_datetime (OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],format ="%Y/%m/%d").dt .date #line:1379
        OOO0OO00O00OO0OO0 =OOO0OO00O00OO0OO0 .sort_values (by =OOOO0OOO00OO000OO ,ascending =[True ],na_position ="last")#line:1380
    elif "批号"in OO0O00O0O000OO0O0 :#line:1381
        OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ]=OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ].astype (str )#line:1382
        OOO0OO00O00OO0OO0 =OOO0OO00O00OO0OO0 .sort_values (by =OOOO0OOO00OO000OO ,ascending =[True ],na_position ="last")#line:1383
        OOO0O0O000OO0O0O0 .set_xticklabels (OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],rotation =-90 ,fontsize =8 )#line:1384
    else :#line:1385
        OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ]=OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ].astype (str )#line:1386
        OOO0O0O000OO0O0O0 .set_xticklabels (OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],rotation =-90 ,fontsize =8 )#line:1387
    OOO0000O0OOOO0O0O =OOO0OO00O00OO0OO0 [O000O0OOO00O00O00 ]#line:1389
    OO000O0O0OOO0O00O =range (0 ,len (OOO0000O0OOOO0O0O ),1 )#line:1390
    OOO0O0O000OO0O0O0 .set_title (OO0O00O0O000OO0O0 )#line:1392
    if O0OOOO0OOOO0O00O0 =="柱状图":#line:1396
        OOO0O0O000OO0O0O0 .bar (x =OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],height =OOO0000O0OOOO0O0O ,width =0.2 ,color ="#87CEFA")#line:1397
    elif O0OOOO0OOOO0O00O0 =="饼图":#line:1398
        OOO0O0O000OO0O0O0 .pie (x =OOO0000O0OOOO0O0O ,labels =OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],autopct ="%0.2f%%")#line:1399
    elif O0OOOO0OOOO0O00O0 =="折线图":#line:1400
        OOO0O0O000OO0O0O0 .plot (OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],OOO0000O0OOOO0O0O ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:1401
    elif "帕累托图"in str (O0OOOO0OOOO0O00O0 ):#line:1403
        OOOO00O0OO0O0000O =OOO0OO00O00OO0OO0 [O000O0OOO00O00O00 ].fillna (0 )#line:1404
        O000OO0O00OO00OO0 =OOOO00O0OO0O0000O .cumsum ()/OOOO00O0OO0O0000O .sum ()*100 #line:1408
        OOO0OO00O00OO0OO0 ["百分比"]=round (OOO0OO00O00OO0OO0 ["数量"]/OOOO00O0OO0O0000O .sum ()*100 ,2 )#line:1409
        OOO0OO00O00OO0OO0 ["累计百分比"]=round (O000OO0O00OO00OO0 ,2 )#line:1410
        O00O000OOO0OOOO00 =O000OO0O00OO00OO0 [O000OO0O00OO00OO0 >0.8 ].index [0 ]#line:1411
        O0000OO0O00OO0O00 =OOOO00O0OO0O0000O .index .tolist ().index (O00O000OOO0OOOO00 )#line:1412
        OOO0O0O000OO0O0O0 .bar (x =OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],height =OOOO00O0OO0O0000O ,color ="C0",label =O000O0OOO00O00O00 )#line:1416
        O0OO0OOO00OOO0O00 =OOO0O0O000OO0O0O0 .twinx ()#line:1417
        O0OO0OOO00OOO0O00 .plot (OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],O000OO0O00OO00OO0 ,color ="C1",alpha =0.6 ,label ="累计比例")#line:1418
        O0OO0OOO00OOO0O00 .yaxis .set_major_formatter (PercentFormatter ())#line:1419
        OOO0O0O000OO0O0O0 .tick_params (axis ="y",colors ="C0")#line:1424
        O0OO0OOO00OOO0O00 .tick_params (axis ="y",colors ="C1")#line:1425
        for O0O00OOO0000OOOOO ,O0000O0OO00O000O0 ,OOO0OO0000O0O0OO0 ,O000OO0O0000OOO0O in zip (OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],OOOO00O0OO0O0000O ,OOO0OO00O00OO0OO0 ["百分比"],OOO0OO00O00OO0OO0 ["累计百分比"]):#line:1427
            OOO0O0O000OO0O0O0 .text (O0O00OOO0000OOOOO ,O0000O0OO00O000O0 +0.1 ,str (int (O0000O0OO00O000O0 ))+", "+str (int (OOO0OO0000O0O0OO0 ))+"%,"+str (int (O000OO0O0000OOO0O ))+"%",color ='black',size =8 )#line:1428
        if "超级帕累托图"in str (O0OOOO0OOOO0O00O0 ):#line:1431
            O0OOO0OO00O0O00O0 =re .compile (r'[(](.*?)[)]',re .S )#line:1432
            OO0OO000O00OO00OO =re .findall (O0OOO0OO00O0O00O0 ,O0OOOO0OOOO0O00O0 )[0 ]#line:1433
            OOO0O0O000OO0O0O0 .bar (x =OOO0OO00O00OO0OO0 [OOOO0OOO00OO000OO ],height =OOO0OO00O00OO0OO0 [OO0OO000O00OO00OO ],color ="orangered",label =OO0OO000O00OO00OO )#line:1434
    O00OOO0OOOOOO0000 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1439
    OO0OOOOOO0O0O0OO0 =OOO0O0O000OO0O0O0 .get_position ()#line:1440
    OOO0O0O000OO0O0O0 .set_position ([OO0OOOOOO0O0O0OO0 .x0 ,OO0OOOOOO0O0O0OO0 .y0 ,OO0OOOOOO0O0O0OO0 .width *0.7 ,OO0OOOOOO0O0O0OO0 .height ])#line:1441
    OOO0O0O000OO0O0O0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1442
    O00O00OO0O0OO00O0 .draw ()#line:1445
    if len (OOO0000O0OOOO0O0O )<=20 and O0OOOO0OOOO0O00O0 !="饼图"and O0OOOO0OOOO0O00O0 !="帕累托图":#line:1448
        for OO0O000OO0OO0OO00 ,OO0OO000O00000O0O in zip (OO000O0O0OOO0O00O ,OOO0000O0OOOO0O0O ):#line:1449
            O0OOOOOO0OO0OOO00 =str (OO0OO000O00000O0O )#line:1450
            OO000OO00O0O0000O =(OO0O000OO0OO0OO00 ,OO0OO000O00000O0O +0.3 )#line:1451
            OOO0O0O000OO0O0O0 .annotate (O0OOOOOO0OO0OOO00 ,xy =OO000OO00O0O0000O ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:1452
    OO00O0O00OOOOOO0O =Button (O0O00OOO0OO0000O0 ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OOO0OO00O00OO0OO0 ),)#line:1462
    OO00O0O00OOOOOO0O .pack (side =RIGHT )#line:1463
    O00000OOOO0000OOO =Button (O0O00OOO0OO0000O0 ,relief =GROOVE ,text ="查看原始数据",command =lambda :Tread_TOOLS_view_dict (OOO0OO00O00OO0OO0 ,1 ))#line:1467
    O00000OOOO0000OOO .pack (side =RIGHT )#line:1468
    OOO00OO0O0O00OOO0 =Button (O0O00OOO0OO0000O0 ,relief =GROOVE ,text ="饼图",command =lambda :Tread_TOOLS_draw (OOO0OO00O00OO0OO0 ,OO0O00O0O000OO0O0 ,OOOO0OOO00OO000OO ,O000O0OOO00O00O00 ,"饼图"),)#line:1476
    OOO00OO0O0O00OOO0 .pack (side =LEFT )#line:1477
    OOO00OO0O0O00OOO0 =Button (O0O00OOO0OO0000O0 ,relief =GROOVE ,text ="柱状图",command =lambda :Tread_TOOLS_draw (OOO0OO00O00OO0OO0 ,OO0O00O0O000OO0O0 ,OOOO0OOO00OO000OO ,O000O0OOO00O00O00 ,"柱状图"),)#line:1484
    OOO00OO0O0O00OOO0 .pack (side =LEFT )#line:1485
    OOO00OO0O0O00OOO0 =Button (O0O00OOO0OO0000O0 ,relief =GROOVE ,text ="折线图",command =lambda :Tread_TOOLS_draw (OOO0OO00O00OO0OO0 ,OO0O00O0O000OO0O0 ,OOOO0OOO00OO000OO ,O000O0OOO00O00O00 ,"折线图"),)#line:1491
    OOO00OO0O0O00OOO0 .pack (side =LEFT )#line:1492
    OOO00OO0O0O00OOO0 =Button (O0O00OOO0OO0000O0 ,relief =GROOVE ,text ="帕累托图",command =lambda :Tread_TOOLS_draw (OOO0OO00O00OO0OO0 ,OO0O00O0O000OO0O0 ,OOOO0OOO00OO000OO ,O000O0OOO00O00O00 ,"帕累托图"),)#line:1499
    OOO00OO0O0O00OOO0 .pack (side =LEFT )#line:1500
def helper ():#line:1506
    ""#line:1507
    O0000O0O0OOO00OO0 =Toplevel ()#line:1508
    O0000O0O0OOO00OO0 .title ("程序使用帮助")#line:1509
    O0000O0O0OOO00OO0 .geometry ("700x500")#line:1510
    O0O0OO00000000O00 =Scrollbar (O0000O0O0OOO00OO0 )#line:1512
    O00000000OOOO0000 =Text (O0000O0O0OOO00OO0 ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1513
    O0O0OO00000000O00 .pack (side =RIGHT ,fill =Y )#line:1514
    O00000000OOOO0000 .pack ()#line:1515
    O0O0OO00000000O00 .config (command =O00000000OOOO0000 .yview )#line:1516
    O00000000OOOO0000 .config (yscrollcommand =O0O0OO00000000O00 .set )#line:1517
    O00000000OOOO0000 .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1522
    O00000000OOOO0000 .config (state =DISABLED )#line:1523
def Tread_TOOLS_CLEAN (O0OO0O0OO0OOOOO0O ):#line:1527
        ""#line:1528
        O0OO0O0OO0OOOOO0O ["报告编码"]=O0OO0O0OO0OOOOO0O ["报告编码"].astype ("str")#line:1530
        O0OO0O0OO0OOOOO0O ["产品批号"]=O0OO0O0OO0OOOOO0O ["产品批号"].astype ("str")#line:1532
        O0OO0O0OO0OOOOO0O ["型号"]=O0OO0O0OO0OOOOO0O ["型号"].astype ("str")#line:1533
        O0OO0O0OO0OOOOO0O ["规格"]=O0OO0O0OO0OOOOO0O ["规格"].astype ("str")#line:1534
        O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"]=O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1536
        O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"]=O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1537
        O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"]=O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1538
        O0OO0O0OO0OOOOO0O ["产品名称"]=O0OO0O0OO0OOOOO0O ["产品名称"].str .replace ("*","※",regex =False )#line:1540
        O0OO0O0OO0OOOOO0O ["产品批号"]=O0OO0O0OO0OOOOO0O ["产品批号"].str .replace ("(","（",regex =False )#line:1542
        O0OO0O0OO0OOOOO0O ["产品批号"]=O0OO0O0OO0OOOOO0O ["产品批号"].str .replace (")","）",regex =False )#line:1543
        O0OO0O0OO0OOOOO0O ["产品批号"]=O0OO0O0OO0OOOOO0O ["产品批号"].str .replace ("*","※",regex =False )#line:1544
        O0OO0O0OO0OOOOO0O ['事件发生日期']=pd .to_datetime (O0OO0O0OO0OOOOO0O ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1547
        O0OO0O0OO0OOOOO0O ["事件发生月份"]=O0OO0O0OO0OOOOO0O ["事件发生日期"].dt .to_period ("M").astype (str )#line:1551
        O0OO0O0OO0OOOOO0O ["事件发生季度"]=O0OO0O0OO0OOOOO0O ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1552
        O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"]=O0OO0O0OO0OOOOO0O ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1556
        O0OO0O0OO0OOOOO0O ["产品批号"]=O0OO0O0OO0OOOOO0O ["产品批号"].fillna ("未填写")#line:1557
        O0OO0O0OO0OOOOO0O ["型号"]=O0OO0O0OO0OOOOO0O ["型号"].fillna ("未填写")#line:1558
        O0OO0O0OO0OOOOO0O ["规格"]=O0OO0O0OO0OOOOO0O ["规格"].fillna ("未填写")#line:1559
        return O0OO0O0OO0OOOOO0O #line:1561
def thread_it (O0O000000O000O0OO ,*O000O000OO00OO000 ):#line:1565
    ""#line:1566
    OO0O000OOOO00000O =threading .Thread (target =O0O000000O000O0OO ,args =O000O000OO00OO000 )#line:1568
    OO0O000OOOO00000O .setDaemon (True )#line:1570
    OO0O000OOOO00000O .start ()#line:1572
def showWelcome ():#line:1575
    ""#line:1576
    OO000OO0O0O0O000O =roox .winfo_screenwidth ()#line:1577
    OO0000OO0O0OOO000 =roox .winfo_screenheight ()#line:1579
    roox .overrideredirect (True )#line:1581
    roox .attributes ("-alpha",1 )#line:1582
    OO000O0O0000O00OO =(OO000OO0O0O0O000O -475 )/2 #line:1583
    O0O000OO0OO0O0000 =(OO0000OO0O0OOO000 -200 )/2 #line:1584
    roox .geometry ("675x140+%d+%d"%(OO000O0O0000O00OO ,O0O000OO0OO0O0000 ))#line:1586
    roox ["bg"]="royalblue"#line:1587
    OOOOO00O00O0000O0 =Label (roox ,text ="医疗器械警戒趋势分析工具",fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:1590
    OOOOO00O00O0000O0 .place (x =0 ,y =15 ,width =675 ,height =90 )#line:1591
    O0OOOOOOO0O00O000 =Label (roox ,text ="Trend Analysis Tools V"+str (version_now ),fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ),)#line:1598
    O0OOOOOOO0O00O000 .place (x =0 ,y =90 ,width =675 ,height =50 )#line:1599
def closeWelcome ():#line:1602
    ""#line:1603
    for OOO0O0OO000O000OO in range (2 ):#line:1604
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
