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
version_now ="0.0.5"#line:57
usergroup ="用户组=0"#line:58
setting_cfg =""#line:59
csdir =str (os .path .dirname (__file__ ))#line:61
csdir =csdir +csdir .split ("treadtools")[0 ][-1 ]#line:62
def extract_zip_file (OO0OOOOOOOOO00O0O ,OOOO000O0O000O00O ):#line:71
    import zipfile #line:73
    if OOOO000O0O000O00O =="":#line:74
        return 0 #line:75
    with zipfile .ZipFile (OO0OOOOOOOOO00O0O ,'r')as OO0OOO0OOOO0OO0OO :#line:76
        for OOO00OO0O00OO0000 in OO0OOO0OOOO0OO0OO .infolist ():#line:77
            OOO00OO0O00OO0000 .filename =OOO00OO0O00OO0000 .filename .encode ('cp437').decode ('gbk')#line:79
            OO0OOO0OOOO0OO0OO .extract (OOO00OO0O00OO0000 ,OOOO000O0O000O00O )#line:80
def get_directory_path (OO000000O00OOOOOO ):#line:86
    global csdir #line:88
    if not (os .path .isfile (os .path .join (OO000000O00OOOOOO ,'规则文件.xls'))):#line:90
        extract_zip_file (csdir +"def.py",OO000000O00OOOOOO )#line:95
    if OO000000O00OOOOOO =="":#line:97
        quit ()#line:98
    return OO000000O00OOOOOO #line:99
def convert_and_compare_dates (O0O0O00OOO00O00O0 ):#line:103
    import datetime #line:104
    OO0OO00OO00OOOOOO =datetime .datetime .now ()#line:105
    try :#line:107
       OO0OO00OOOO0OOOO0 =datetime .datetime .strptime (str (int (int (O0O0O00OOO00O00O0 )/4 )),"%Y%m%d")#line:108
    except :#line:109
        print ("fail")#line:110
        return "已过期"#line:111
    if OO0OO00OOOO0OOOO0 >OO0OO00OO00OOOOOO :#line:113
        return "未过期"#line:115
    else :#line:116
        return "已过期"#line:117
def read_setting_cfg ():#line:119
    global csdir #line:120
    if os .path .exists (csdir +'setting.cfg'):#line:122
        text .insert (END ,"已完成初始化\n")#line:123
        with open (csdir +'setting.cfg','r')as O000O000O000O0000 :#line:124
            OOOOO0OOOOO0O00O0 =eval (O000O000O000O0000 .read ())#line:125
    else :#line:126
        OOOO00OOOOOOO0000 =csdir +'setting.cfg'#line:128
        with open (OOOO00OOOOOOO0000 ,'w')as O000O000O000O0000 :#line:129
            O000O000O000O0000 .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:130
        text .insert (END ,"未初始化，正在初始化...\n")#line:131
        OOOOO0OOOOO0O00O0 =read_setting_cfg ()#line:132
    return OOOOO0OOOOO0O00O0 #line:133
def open_setting_cfg ():#line:136
    global csdir #line:137
    with open (csdir +"setting.cfg","r")as OO0000O0OOO000OO0 :#line:139
        O0OO00O00O0OO00O0 =eval (OO0000O0OOO000OO0 .read ())#line:141
    return O0OO00O00O0OO00O0 #line:142
def update_setting_cfg (O000O00OO0O0OOOO0 ,OOO0O0OO0OO000O0O ):#line:144
    global csdir #line:145
    with open (csdir +"setting.cfg","r")as OOOOOOO0000000OO0 :#line:147
        OOO0OO0OO0OO0O0O0 =eval (OOOOOOO0000000OO0 .read ())#line:149
    if OOO0OO0OO0OO0O0O0 [O000O00OO0O0OOOO0 ]==0 or OOO0OO0OO0OO0O0O0 [O000O00OO0O0OOOO0 ]=="11111180000808":#line:151
        OOO0OO0OO0OO0O0O0 [O000O00OO0O0OOOO0 ]=OOO0O0OO0OO000O0O #line:152
        with open (csdir +"setting.cfg","w")as OOOOOOO0000000OO0 :#line:154
            OOOOOOO0000000OO0 .write (str (OOO0OO0OO0OO0O0O0 ))#line:155
def generate_random_file ():#line:158
    OOOO00000OOOOO00O =random .randint (200000 ,299999 )#line:160
    update_setting_cfg ("sidori",OOOO00000OOOOO00O )#line:162
def display_random_number ():#line:164
    global csdir #line:165
    OOOOOO0000OO00OOO =Toplevel ()#line:166
    OOOOOO0000OO00OOO .title ("ID")#line:167
    OO0O0O0O000OO0O00 =OOOOOO0000OO00OOO .winfo_screenwidth ()#line:169
    OO0OOO0000O00OO0O =OOOOOO0000OO00OOO .winfo_screenheight ()#line:170
    OO0OOO0OO00OOOO0O =80 #line:172
    OO000O0OO00000OO0 =70 #line:173
    O000O0OO0OOO0OOOO =(OO0O0O0O000OO0O00 -OO0OOO0OO00OOOO0O )/2 #line:175
    OO00O000OOOOOOO00 =(OO0OOO0000O00OO0O -OO000O0OO00000OO0 )/2 #line:176
    OOOOOO0000OO00OOO .geometry ("%dx%d+%d+%d"%(OO0OOO0OO00OOOO0O ,OO000O0OO00000OO0 ,O000O0OO0OOO0OOOO ,OO00O000OOOOOOO00 ))#line:177
    with open (csdir +"setting.cfg","r")as O00OO0OOO0O0O0OOO :#line:180
        OOOO0OOOO0O0OOO00 =eval (O00OO0OOO0O0O0OOO .read ())#line:182
    O000OO000000OOO00 =int (OOOO0OOOO0O0OOO00 ["sidori"])#line:183
    OOOOOO0O0O00O00OO =O000OO000000OOO00 *2 +183576 #line:184
    print (OOOOOO0O0O00O00OO )#line:186
    O0OO00000OO0OO000 =ttk .Label (OOOOOO0000OO00OOO ,text =f"机器码: {O000OO000000OOO00}")#line:188
    OO00O00OO0O000OO0 =ttk .Entry (OOOOOO0000OO00OOO )#line:189
    O0OO00000OO0OO000 .pack ()#line:192
    OO00O00OO0O000OO0 .pack ()#line:193
    ttk .Button (OOOOOO0000OO00OOO ,text ="验证",command =lambda :check_input (OO00O00OO0O000OO0 .get (),OOOOOO0O0O00O00OO )).pack ()#line:197
def check_input (OO0O00O00O0OOOOOO ,OO0O0O0O0OO0O0O0O ):#line:199
    try :#line:203
        O0OOOO0OO00O00OO0 =int (str (OO0O00O00O0OOOOOO )[0 :6 ])#line:204
        O0OO00OOO0O0O000O =convert_and_compare_dates (str (OO0O00O00O0OOOOOO )[6 :14 ])#line:205
    except :#line:206
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:207
        return 0 #line:208
    if O0OOOO0OO00O00OO0 ==OO0O0O0O0OO0O0O0O and O0OO00OOO0O0O000O =="未过期":#line:210
        update_setting_cfg ("sidfinal",OO0O00O00O0OOOOOO )#line:211
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:212
        quit ()#line:213
    else :#line:214
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:215
def update_software (O0OO0OOOO0OO00000 ):#line:219
    global version_now #line:221
    O00O000OO000O0O0O =requests .get (f"https://pypi.org/pypi/{O0OO0OOOO0OO00000}/json").json ()["info"]["version"]#line:222
    text .insert (END ,"当前版本为："+version_now )#line:223
    if O00O000OO000O0O0O >version_now :#line:224
        text .insert (END ,"\n最新版本为："+O00O000OO000O0O0O +",正在尝试自动更新....")#line:225
        pip .main (['install',O0OO0OOOO0OO00000 ,'--upgrade'])#line:227
        text .insert (END ,"\n您可以开展工作。")#line:228
def Tread_TOOLS_fileopen (OOOO00O0O0O0O000O ):#line:232
    ""#line:233
    global TT_ori #line:234
    global TT_ori_backup #line:235
    global TT_biaozhun #line:236
    warnings .filterwarnings ('ignore')#line:237
    if OOOO00O0O0O0O000O ==0 :#line:239
        O0O00OO0O00O0OO00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:240
        O00O00O0OO0OOO00O =[pd .read_excel (OOO0OOO00000OO0OO ,header =0 ,sheet_name =0 )for OOO0OOO00000OO0OO in O0O00OO0O00O0OO00 ]#line:241
        OO0OO0000OO000OOO =pd .concat (O00O00O0OO0OOO00O ,ignore_index =True ).drop_duplicates ()#line:242
        try :#line:243
            OO0OO0000OO000OOO =OO0OO0000OO000OOO .loc [:,~TT_ori .columns .str .contains ("^Unnamed")]#line:244
        except :#line:245
            pass #line:246
        TT_ori_backup =OO0OO0000OO000OOO .copy ()#line:247
        TT_ori =Tread_TOOLS_CLEAN (OO0OO0000OO000OOO ).copy ()#line:248
        text .insert (END ,"\n原始数据导入成功，行数："+str (len (TT_ori )))#line:250
        text .insert (END ,"\n数据校验：\n")#line:251
        text .insert (END ,TT_ori )#line:252
        text .see (END )#line:253
    if OOOO00O0O0O0O000O ==1 :#line:255
        OO000O0OOOO000OO0 =filedialog .askopenfilename (filetypes =[("XLS",".xls")])#line:256
        TT_biaozhun ["关键字表"]=pd .read_excel (OO000O0OOOO000OO0 ,sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:257
        TT_biaozhun ["产品批号"]=pd .read_excel (OO000O0OOOO000OO0 ,sheet_name ="产品批号",header =0 ,index_col =0 ,).reset_index ()#line:258
        TT_biaozhun ["事件发生月份"]=pd .read_excel (OO000O0OOOO000OO0 ,sheet_name ="事件发生月份",header =0 ,index_col =0 ,).reset_index ()#line:259
        TT_biaozhun ["事件发生季度"]=pd .read_excel (OO000O0OOOO000OO0 ,sheet_name ="事件发生季度",header =0 ,index_col =0 ,).reset_index ()#line:260
        TT_biaozhun ["规格"]=pd .read_excel (OO000O0OOOO000OO0 ,sheet_name ="规格",header =0 ,index_col =0 ,).reset_index ()#line:261
        TT_biaozhun ["型号"]=pd .read_excel (OO000O0OOOO000OO0 ,sheet_name ="型号",header =0 ,index_col =0 ,).reset_index ()#line:262
        TT_biaozhun ["设置"]=pd .read_excel (OO000O0OOOO000OO0 ,sheet_name ="设置",header =0 ,index_col =0 ,).reset_index ()#line:263
        Tread_TOOLS_check (TT_ori ,TT_biaozhun ["关键字表"],0 )#line:264
        text .insert (END ,"\n标准导入成功，行数："+str (len (TT_biaozhun )))#line:265
        text .see (END )#line:266
def Tread_TOOLS_check (OO0O00OO0000O0OO0 ,OOO000OO0000OO000 ,O0OOO0OOO0OOOO000 ):#line:268
        ""#line:269
        global TT_ori #line:270
        OO000O0O00O00O00O =Tread_TOOLS_Countall (OO0O00OO0000O0OO0 ).df_psur (OOO000OO0000OO000 )#line:271
        if O0OOO0OOO0OOOO000 ==0 :#line:273
            Tread_TOOLS_tree_Level_2 (OO000O0O00O00O00O ,0 ,TT_ori .copy ())#line:275
        OO000O0O00O00O00O ["核验"]=0 #line:278
        OO000O0O00O00O00O .loc [(OO000O0O00O00O00O ["关键字标记"].str .contains ("-其他关键字-",na =False )),"核验"]=OO000O0O00O00O00O .loc [(OO000O0O00O00O00O ["关键字标记"].str .contains ("-其他关键字-",na =False )),"总数量"]#line:279
        if OO000O0O00O00O00O ["核验"].sum ()>0 :#line:280
            showinfo (title ="温馨提示",message ="存在未定义类型的报告"+str (OO000O0O00O00O00O ["核验"].sum ())+"条，趋势分析可能会存在遗漏，建议修正该错误再进行下一步。")#line:281
def Tread_TOOLS_tree_Level_2 (O00OOO0O0O00O00OO ,OO000O00O0OOO00O0 ,O0000000O0OOOOO00 ,*O000O00OOOOO00OO0 ):#line:283
    ""#line:284
    global TT_ori_backup #line:286
    OOOOOO0O00OO00O00 =O00OOO0O0O00O00OO .columns .values .tolist ()#line:288
    OO000O00O0OOO00O0 =0 #line:289
    O0OO0OOOO0O0O000O =O00OOO0O0O00O00OO .loc [:]#line:290
    O00O0O0OO0O0O0OOO =0 #line:294
    try :#line:295
        O0OO0OOOO0O0OOOO0 =O000O00OOOOO00OO0 [0 ]#line:296
        O00O0O0OO0O0O0OOO =1 #line:297
    except :#line:298
        pass #line:299
    O0O0O0OO0OOO0OOOO =Toplevel ()#line:302
    O0O0O0OO0OOO0OOOO .title ("报表查看器")#line:303
    OO00OO0O00OO000O0 =O0O0O0OO0OOO0OOOO .winfo_screenwidth ()#line:304
    O00OOOOOO0O00O000 =O0O0O0OO0OOO0OOOO .winfo_screenheight ()#line:306
    OO00OOO00O000OO00 =1300 #line:308
    OO0OO0OOO0O000OO0 =600 #line:309
    O00000OO0OO0000OO =(OO00OO0O00OO000O0 -OO00OOO00O000OO00 )/2 #line:311
    OOO00O0OOO0O0OO0O =(O00OOOOOO0O00O000 -OO0OO0OOO0O000OO0 )/2 #line:312
    O0O0O0OO0OOO0OOOO .geometry ("%dx%d+%d+%d"%(OO00OOO00O000OO00 ,OO0OO0OOO0O000OO0 ,O00000OO0OO0000OO ,OOO00O0OOO0O0OO0O ))#line:313
    O0O0OO00O0O000O0O =ttk .Frame (O0O0O0OO0OOO0OOOO ,width =1300 ,height =20 )#line:314
    O0O0OO00O0O000O0O .pack (side =BOTTOM )#line:315
    OOO0OO00O000OOO0O =ttk .Frame (O0O0O0OO0OOO0OOOO ,width =1300 ,height =20 )#line:317
    OOO0OO00O000OOO0O .pack (side =TOP )#line:318
    if 1 >0 :#line:322
        O00O0000OO0OO0O00 =Button (O0O0OO00O0O000O0O ,text ="控制图(所有)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0OO0OOOO0O0O000O [:-1 ],O0OO0OOOO0O0OOOO0 ,[O0OOO000O0000000O for O0OOO000O0000000O in O0OO0OOOO0O0O000O .columns if (O0OOO000O0000000O not in [O0OO0OOOO0O0OOOO0 ])],"关键字趋势图",100 ),)#line:332
        if O00O0O0OO0O0O0OOO ==1 :#line:333
            O00O0000OO0OO0O00 .pack (side =LEFT )#line:334
        O00O0000OO0OO0O00 =Button (O0O0OO00O0O000O0O ,text ="控制图(总数量)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0OO0OOOO0O0O000O [:-1 ],O0OO0OOOO0O0OOOO0 ,[O0O0O0OO00000000O for O0O0O0OO00000000O in O0OO0OOOO0O0O000O .columns if (O0O0O0OO00000000O in ["该元素总数量"])],"关键字趋势图",100 ),)#line:344
        if O00O0O0OO0O0O0OOO ==1 :#line:345
            O00O0000OO0OO0O00 .pack (side =LEFT )#line:346
        O00OOOOOO0OO0OOO0 =Button (O0O0OO00O0O000O0O ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (O0OO0OOOO0O0O000O ),)#line:356
        O00OOOOOO0OO0OOO0 .pack (side =LEFT )#line:357
        O00OOOOOO0OO0OOO0 =Button (O0O0OO00O0O000O0O ,text ="发生率测算",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_fashenglv (O0OO0OOOO0O0O000O ,O0OO0OOOO0O0OOOO0 ),)#line:367
        if "关键字标记"not in O0OO0OOOO0O0O000O .columns and "报告编码"not in O0OO0OOOO0O0O000O .columns :#line:368
            if "对象"not in O0OO0OOOO0O0O000O .columns :#line:369
                O00OOOOOO0OO0OOO0 .pack (side =LEFT )#line:370
        O00OOOOOO0OO0OOO0 =Button (O0O0OO00O0O000O0O ,text ="直方图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_histbar (O0OO0OOOO0O0O000O .copy ()),)#line:380
        if "对象"in O0OO0OOOO0O0O000O .columns :#line:381
            O00OOOOOO0OO0OOO0 .pack (side =LEFT )#line:382
        OOO0O0O0O00OOOOO0 =Button (O0O0OO00O0O000O0O ,text ="行数:"+str (len (O0OO0OOOO0O0O000O )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:392
        OOO0O0O0O00OOOOO0 .pack (side =LEFT )#line:393
    OO00O0OO000000O00 =O0OO0OOOO0O0O000O .values .tolist ()#line:396
    O0OO000000000O000 =O0OO0OOOO0O0O000O .columns .values .tolist ()#line:397
    OO000O0000000OOO0 =ttk .Treeview (OOO0OO00O000OOO0O ,columns =O0OO000000000O000 ,show ="headings",height =45 )#line:398
    for OO0OO0OO000OOO0O0 in O0OO000000000O000 :#line:400
        OO000O0000000OOO0 .heading (OO0OO0OO000OOO0O0 ,text =OO0OO0OO000OOO0O0 )#line:401
    for OOOOOO0O0OO0OOOOO in OO00O0OO000000O00 :#line:402
        OO000O0000000OOO0 .insert ("","end",values =OOOOOO0O0OO0OOOOO )#line:403
    for O0O00OO0O00OO0O00 in O0OO000000000O000 :#line:404
        OO000O0000000OOO0 .column (O0O00OO0O00OO0O00 ,minwidth =0 ,width =120 ,stretch =NO )#line:405
    O000O0O00000OOO0O =Scrollbar (OOO0OO00O000OOO0O ,orient ="vertical")#line:407
    O000O0O00000OOO0O .pack (side =RIGHT ,fill =Y )#line:408
    O000O0O00000OOO0O .config (command =OO000O0000000OOO0 .yview )#line:409
    OO000O0000000OOO0 .config (yscrollcommand =O000O0O00000OOO0O .set )#line:410
    O00OO0OOOO0000000 =Scrollbar (OOO0OO00O000OOO0O ,orient ="horizontal")#line:412
    O00OO0OOOO0000000 .pack (side =BOTTOM ,fill =X )#line:413
    O00OO0OOOO0000000 .config (command =OO000O0000000OOO0 .xview )#line:414
    OO000O0000000OOO0 .config (yscrollcommand =O000O0O00000OOO0O .set )#line:415
    def O0O0OO0000OO0O0OO (O0O0OOOOOOO0O0OO0 ,OO00OO00OOO0OO0O0 ,O0O000O00O0O0OOOO ):#line:417
        for OOOOO000O000O000O in OO000O0000000OOO0 .selection ():#line:420
            O00O000OOOO0O0OOO =OO000O0000000OOO0 .item (OOOOO000O000O000O ,"values")#line:421
            O0O0O0OO0000OOOO0 =dict (zip (OO00OO00OOO0OO0O0 ,O00O000OOOO0O0OOO ))#line:422
        if "该分类下各项计数"in OO00OO00OOO0OO0O0 :#line:424
            OO00O0000O0OO0OO0 =O0000000O0OOOOO00 .copy ()#line:425
            OO00O0000O0OO0OO0 ["关键字查找列"]=""#line:426
            for O0000000OOO0O00OO in TOOLS_get_list (O0O0O0OO0000OOOO0 ["查找位置"]):#line:427
                OO00O0000O0OO0OO0 ["关键字查找列"]=OO00O0000O0OO0OO0 ["关键字查找列"]+OO00O0000O0OO0OO0 [O0000000OOO0O00OO ].astype ("str")#line:428
            O00000OOO0000O0O0 =OO00O0000O0OO0OO0 .loc [OO00O0000O0OO0OO0 ["关键字查找列"].str .contains (O0O0O0OO0000OOOO0 ["关键字标记"],na =False )].copy ()#line:429
            O00000OOO0000O0O0 =O00000OOO0000O0O0 .loc [~O00000OOO0000O0O0 ["关键字查找列"].str .contains (O0O0O0OO0000OOOO0 ["排除值"],na =False )].copy ()#line:430
            Tread_TOOLS_tree_Level_2 (O00000OOO0000O0O0 ,0 ,O00000OOO0000O0O0 )#line:436
            return 0 #line:437
        if "报告编码"in OO00OO00OOO0OO0O0 :#line:439
            O00OO00OO00000O00 =Toplevel ()#line:440
            OO0O0O00O000O0O0O =O00OO00OO00000O00 .winfo_screenwidth ()#line:441
            O0O00OO0O00OOOO0O =O00OO00OO00000O00 .winfo_screenheight ()#line:443
            OOO0O00OO00OOOO00 =800 #line:445
            O00OO00OOOO00O0OO =600 #line:446
            O0000000OOO0O00OO =(OO0O0O00O000O0O0O -OOO0O00OO00OOOO00 )/2 #line:448
            O0OOO0OOO0OO0OO00 =(O0O00OO0O00OOOO0O -O00OO00OOOO00O0OO )/2 #line:449
            O00OO00OO00000O00 .geometry ("%dx%d+%d+%d"%(OOO0O00OO00OOOO00 ,O00OO00OOOO00O0OO ,O0000000OOO0O00OO ,O0OOO0OOO0OO0OO00 ))#line:450
            O0000O0000OO00OOO =ScrolledText (O00OO00OO00000O00 ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:454
            O0000O0000OO00OOO .pack (padx =10 ,pady =10 )#line:455
            def OO0OOO00000O00000 (event =None ):#line:456
                O0000O0000OO00OOO .event_generate ('<<Copy>>')#line:457
            def OOOO0000O0O0OO0O0 (O0OO0OOO00O00OOOO ,O0OO0000000000O0O ):#line:458
                O00O000000OOOOOOO =open (O0OO0000000000O0O ,"w",encoding ='utf-8')#line:459
                O00O000000OOOOOOO .write (O0OO0OOO00O00OOOO )#line:460
                O00O000000OOOOOOO .flush ()#line:462
                showinfo (title ="提示信息",message ="保存成功。")#line:463
            OOO000O000OOOO00O =Menu (O0000O0000OO00OOO ,tearoff =False ,)#line:465
            OOO000O000OOOO00O .add_command (label ="复制",command =OO0OOO00000O00000 )#line:466
            OOO000O000OOOO00O .add_command (label ="导出",command =lambda :thread_it (OOOO0000O0O0OO0O0 ,O0000O0000OO00OOO .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =O0O0O0OO0000OOOO0 ["报告编码"],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:467
            def O00000O0O0OOO00O0 (OOO0OO0O00O0OOO00 ):#line:469
                OOO000O000OOOO00O .post (OOO0OO0O00O0OOO00 .x_root ,OOO0OO0O00O0OOO00 .y_root )#line:470
            O0000O0000OO00OOO .bind ("<Button-3>",O00000O0O0OOO00O0 )#line:471
            O00OO00OO00000O00 .title (O0O0O0OO0000OOOO0 ["报告编码"])#line:473
            for OOOOOO0O00OO0OOO0 in range (len (OO00OO00OOO0OO0O0 )):#line:474
                O0000O0000OO00OOO .insert (END ,OO00OO00OOO0OO0O0 [OOOOOO0O00OO0OOO0 ])#line:476
                O0000O0000OO00OOO .insert (END ,"：")#line:477
                O0000O0000OO00OOO .insert (END ,O0O0O0OO0000OOOO0 [OO00OO00OOO0OO0O0 [OOOOOO0O00OO0OOO0 ]])#line:478
                O0000O0000OO00OOO .insert (END ,"\n")#line:479
            O0000O0000OO00OOO .config (state =DISABLED )#line:480
            return 0 #line:481
        O0OOO0OOO0OO0OO00 =O00O000OOOO0O0OOO [1 :-1 ]#line:484
        O0000000OOO0O00OO =O0O000O00O0O0OOOO .columns .tolist ()#line:486
        O0000000OOO0O00OO =O0000000OOO0O00OO [1 :-1 ]#line:487
        OOOOOOOOOOO0OOOOO ={'关键词':O0000000OOO0O00OO ,'数量':O0OOO0OOO0OO0OO00 }#line:489
        OOOOOOOOOOO0OOOOO =pd .DataFrame .from_dict (OOOOOOOOOOO0OOOOO )#line:490
        OOOOOOOOOOO0OOOOO ["数量"]=OOOOOOOOOOO0OOOOO ["数量"].astype (float )#line:491
        Tread_TOOLS_draw (OOOOOOOOOOO0OOOOO ,"帕累托图",'关键词','数量',"帕累托图")#line:492
        return 0 #line:493
    OO000O0000000OOO0 .bind ("<Double-1>",lambda OO0O00O0000OOOOOO :O0O0OO0000OO0O0OO (OO0O00O0000OOOOOO ,O0OO000000000O000 ,O0OO0OOOO0O0O000O ),)#line:501
    OO000O0000000OOO0 .pack ()#line:502
class Tread_TOOLS_Countall ():#line:504
    ""#line:505
    def __init__ (O0O0OO0000O00O0OO ,OOO000OOOO0O0OOOO ):#line:506
        ""#line:507
        O0O0OO0000O00O0OO .df =OOO000OOOO0O0OOOO #line:508
    def df_psur (OOO0OO00OOO0O0000 ,O0OO0OO00O00O0OOO ,*O0000OO00O000O000 ):#line:510
        ""#line:511
        global TT_biaozhun #line:512
        O0OO00OOO0O0O00O0 =OOO0OO00OOO0O0000 .df .copy ()#line:513
        OO0OO00000O0OOO00 =len (O0OO00OOO0O0O00O0 .drop_duplicates ("报告编码"))#line:515
        O0O00O0O0O000OO00 =O0OO0OO00O00O0OOO .copy ()#line:518
        O00O00000O0000O00 =TT_biaozhun ["设置"]#line:521
        if O00O00000O0000O00 .loc [1 ,"值"]:#line:522
            OOOOO00O00O0OOO00 =O00O00000O0000O00 .loc [1 ,"值"]#line:523
        else :#line:524
            OOOOO00O00O0OOO00 ="透视列"#line:525
            O0OO00OOO0O0O00O0 [OOOOO00O00O0OOO00 ]="未正确设置"#line:526
        OO00O000OO00000OO =""#line:528
        OO000O0O00O0O0OOO ="-其他关键字-"#line:529
        for O0O00O0O0O0O0OO0O ,O0OO000O0OOO00OOO in O0O00O0O0O000OO00 .iterrows ():#line:530
            OO000O0O00O0O0OOO =OO000O0O00O0O0OOO +"|"+str (O0OO000O0OOO00OOO ["值"])#line:531
            OOO00O0OOOO0OO0O0 =O0OO000O0OOO00OOO #line:532
        OOO00O0OOOO0OO0O0 [3 ]=OO000O0O00O0O0OOO #line:533
        OOO00O0OOOO0OO0O0 [2 ]="-其他关键字-|"#line:534
        O0O00O0O0O000OO00 .loc [len (O0O00O0O0O000OO00 )]=OOO00O0OOOO0OO0O0 #line:535
        O0O00O0O0O000OO00 =O0O00O0O0O000OO00 .reset_index (drop =True )#line:536
        O0OO00OOO0O0O00O0 ["关键字查找列"]=""#line:540
        for O0OOOO00O0OOO000O in TOOLS_get_list (O0O00O0O0O000OO00 .loc [0 ,"查找位置"]):#line:541
            O0OO00OOO0O0O00O0 ["关键字查找列"]=O0OO00OOO0O0O00O0 ["关键字查找列"]+O0OO00OOO0O0O00O0 [O0OOOO00O0OOO000O ].astype ("str")#line:542
        O0000OO0OOO00O000 =[]#line:545
        for O0O00O0O0O0O0OO0O ,O0OO000O0OOO00OOO in O0O00O0O0O000OO00 .iterrows ():#line:546
            OOO000OOO0OO0OOOO =O0OO000O0OOO00OOO ["值"]#line:547
            OOO000O0OO0O0O00O =O0OO00OOO0O0O00O0 .loc [O0OO00OOO0O0O00O0 ["关键字查找列"].str .contains (OOO000OOO0OO0OOOO ,na =False )].copy ()#line:548
            if str (O0OO000O0OOO00OOO ["排除值"])!="nan":#line:549
                OOO000O0OO0O0O00O =OOO000O0OO0O0O00O .loc [~OOO000O0OO0O0O00O ["关键字查找列"].str .contains (str (O0OO000O0OOO00OOO ["排除值"]),na =False )].copy ()#line:550
            OOO000O0OO0O0O00O ["关键字标记"]=str (OOO000OOO0OO0OOOO )#line:552
            OOO000O0OO0O0O00O ["关键字计数"]=1 #line:553
            if len (OOO000O0OO0O0O00O )>0 :#line:555
                O00OOOOO00000000O =pd .pivot_table (OOO000O0OO0O0O00O .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns =OOOOO00O00O0OOO00 ,aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:565
                O00OOOOO00000000O =O00OOOOO00000000O [:-1 ]#line:566
                O00OOOOO00000000O .columns =O00OOOOO00000000O .columns .droplevel (0 )#line:567
                O00OOOOO00000000O =O00OOOOO00000000O .reset_index ()#line:568
                if len (O00OOOOO00000000O )>0 :#line:571
                    OOOOOOO0000O00OOO =str (Counter (TOOLS_get_list0 ("use(关键字查找列).file",OOO000O0OO0O0O00O ,1000 ))).replace ("Counter({","{")#line:572
                    OOOOOOO0000O00OOO =OOOOOOO0000O00OOO .replace ("})","}")#line:573
                    OOOOOOO0000O00OOO =ast .literal_eval (OOOOOOO0000O00OOO )#line:574
                    O00OOOOO00000000O .loc [0 ,"事件分类"]=str (TOOLS_get_list (O00OOOOO00000000O .loc [0 ,"关键字标记"])[0 ])#line:576
                    O00OOOOO00000000O .loc [0 ,"该分类下各项计数"]=str ({O0O0OOO000OOO00O0 :OOO0O00OO00000OO0 for O0O0OOO000OOO00O0 ,OOO0O00OO00000OO0 in OOOOOOO0000O00OOO .items ()if STAT_judge_x (str (O0O0OOO000OOO00O0 ),TOOLS_get_list (OOO000OOO0OO0OOOO ))==1 })#line:577
                    O00OOOOO00000000O .loc [0 ,"其他分类各项计数"]=str ({OO00O0OO00000OOO0 :O0OO0OOO0O0O0O0O0 for OO00O0OO00000OOO0 ,O0OO0OOO0O0O0O0O0 in OOOOOOO0000O00OOO .items ()if STAT_judge_x (str (OO00O0OO00000OOO0 ),TOOLS_get_list (OOO000OOO0OO0OOOO ))!=1 })#line:578
                    O00OOOOO00000000O ["查找位置"]=O0OO000O0OOO00OOO ["查找位置"]#line:579
                    O0000OO0OOO00O000 .append (O00OOOOO00000000O )#line:582
        OO00O000OO00000OO =pd .concat (O0000OO0OOO00O000 )#line:583
        OO00O000OO00000OO =OO00O000OO00000OO .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:588
        OO00O000OO00000OO =OO00O000OO00000OO .reset_index ()#line:589
        OO00O000OO00000OO ["All占比"]=round (OO00O000OO00000OO ["All"]/OO0OO00000O0OOO00 *100 ,2 )#line:591
        OO00O000OO00000OO =OO00O000OO00000OO .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:592
        for O00O0O0O0000O0O00 ,O0O00OO0O0000O0OO in O0O00O0O0O000OO00 .iterrows ():#line:595
            OO00O000OO00000OO .loc [(OO00O000OO00000OO ["关键字标记"].astype (str )==str (O0O00OO0O0000O0OO ["值"])),"排除值"]=O0O00OO0O0000O0OO ["排除值"]#line:596
            OO00O000OO00000OO .loc [(OO00O000OO00000OO ["关键字标记"].astype (str )==str (O0O00OO0O0000O0OO ["值"])),"查找位置"]=O0O00OO0O0000O0OO ["查找位置"]#line:597
        OO00O000OO00000OO ["排除值"]=OO00O000OO00000OO ["排除值"].fillna ("-没有排除值-")#line:599
        OO00O000OO00000OO ["报表类型"]="PSUR"#line:602
        del OO00O000OO00000OO ["index"]#line:603
        try :#line:604
            del OO00O000OO00000OO ["未正确设置"]#line:605
        except :#line:606
            pass #line:607
        return OO00O000OO00000OO #line:608
    def df_find_all_keword_risk (O00OOOOO000O00OOO ,O000OOO0O0O0O0O0O ,*OOOO0000OOOO00000 ):#line:611
        ""#line:612
        global TT_biaozhun #line:613
        O0OOO0000O0O0OOO0 =O00OOOOO000O00OOO .df .copy ()#line:615
        OOO00OOO00O00OOO0 =time .time ()#line:616
        O0000O0OO00000000 =TT_biaozhun ["关键字表"].copy ()#line:618
        O00O000O000OO000O ="作用对象"#line:620
        O00O0OOO0O00000OO ="报告编码"#line:622
        O00OO0O00O0O000OO =O0OOO0000O0O0OOO0 .groupby ([O00O000O000OO000O ]).agg (总数量 =(O00O0OOO0O00000OO ,"nunique"),).reset_index ()#line:625
        OO00O0O0OOO0OO0OO =[O00O000O000OO000O ,O000OOO0O0O0O0O0O ]#line:627
        O00O0OO0OO0O00000 =O0OOO0000O0O0OOO0 .groupby (OO00O0O0OOO0OO0OO ).agg (该元素总数量 =(O00O000O000OO000O ,"count"),).reset_index ()#line:631
        O00000O00OOO000O0 =[]#line:633
        O0OOOO0O0O0OOO0OO =0 #line:637
        O0OO0OO0OO0O000OO =int (len (O00OO0O00O0O000OO ))#line:638
        for OO00OOO0O00O000O0 ,OOOO00O00OO0O000O in zip (O00OO0O00O0O000OO [O00O000O000OO000O ].values ,O00OO0O00O0O000OO ["总数量"].values ):#line:639
            O0OOOO0O0O0OOO0OO +=1 #line:640
            O0OOO0O0OO0000000 =O0OOO0000O0O0OOO0 [(O0OOO0000O0O0OOO0 [O00O000O000OO000O ]==OO00OOO0O00O000O0 )].copy ()#line:641
            for O000O0000O0000OO0 ,OO00OO000OOO00O00 ,O0O000OOOO0OOO0O0 in zip (O0000O0OO00000000 ["值"].values ,O0000O0OO00000000 ["查找位置"].values ,O0000O0OO00000000 ["排除值"].values ):#line:643
                    O00OO0OOO0OOOO00O =O0OOO0O0OO0000000 .copy ()#line:644
                    O00O0O0O0OO000O0O =TOOLS_get_list (O000O0000O0000OO0 )[0 ]#line:645
                    O00OO0OOO0OOOO00O ["关键字查找列"]=""#line:647
                    for O0OOO00OOO0O0OOOO in TOOLS_get_list (OO00OO000OOO00O00 ):#line:648
                        O00OO0OOO0OOOO00O ["关键字查找列"]=O00OO0OOO0OOOO00O ["关键字查找列"]+O00OO0OOO0OOOO00O [O0OOO00OOO0O0OOOO ].astype ("str")#line:649
                    O00OO0OOO0OOOO00O .loc [O00OO0OOO0OOOO00O ["关键字查找列"].str .contains (O000O0000O0000OO0 ,na =False ),"关键字"]=O00O0O0O0OO000O0O #line:651
                    if str (O0O000OOOO0OOO0O0 )!="nan":#line:656
                        O00OO0OOO0OOOO00O =O00OO0OOO0OOOO00O .loc [~O00OO0OOO0OOOO00O ["关键字查找列"].str .contains (O0O000OOOO0OOO0O0 ,na =False )].copy ()#line:657
                    if (len (O00OO0OOO0OOOO00O ))<1 :#line:659
                        continue #line:661
                    O0O0O00OO0O0OOO00 =STAT_find_keyword_risk (O00OO0OOO0OOOO00O ,[O00O000O000OO000O ,"关键字"],"关键字",O000OOO0O0O0O0O0O ,int (OOOO00O00OO0O000O ))#line:663
                    if len (O0O0O00OO0O0OOO00 )>0 :#line:664
                        O0O0O00OO0O0OOO00 ["关键字组合"]=O000O0000O0000OO0 #line:665
                        O0O0O00OO0O0OOO00 ["排除值"]=O0O000OOOO0OOO0O0 #line:666
                        O0O0O00OO0O0OOO00 ["关键字查找列"]=OO00OO000OOO00O00 #line:667
                        O00000O00OOO000O0 .append (O0O0O00OO0O0OOO00 )#line:668
        if len (O00000O00OOO000O0 )<1 :#line:671
            showinfo (title ="错误信息",message ="该注册证号未检索到任何关键字，规则制定存在缺陷。")#line:672
            return 0 #line:673
        O0OO0O0O0000OOOO0 =pd .concat (O00000O00OOO000O0 )#line:674
        O0OO0O0O0000OOOO0 =pd .merge (O0OO0O0O0000OOOO0 ,O00O0OO0OO0O00000 ,on =OO00O0O0OOO0OO0OO ,how ="left")#line:677
        O0OO0O0O0000OOOO0 ["关键字数量比例"]=round (O0OO0O0O0000OOOO0 ["计数"]/O0OO0O0O0000OOOO0 ["该元素总数量"],2 )#line:678
        O0OO0O0O0000OOOO0 =O0OO0O0O0000OOOO0 .reset_index (drop =True )#line:680
        if len (O0OO0O0O0000OOOO0 )>0 :#line:683
            O0OO0O0O0000OOOO0 ["风险评分"]=0 #line:684
            O0OO0O0O0000OOOO0 ["报表类型"]="keyword_findrisk"+O000OOO0O0O0O0O0O #line:685
            O0OO0O0O0000OOOO0 .loc [(O0OO0O0O0000OOOO0 ["计数"]>=3 ),"风险评分"]=O0OO0O0O0000OOOO0 ["风险评分"]+3 #line:686
            O0OO0O0O0000OOOO0 .loc [(O0OO0O0O0000OOOO0 ["计数"]>=(O0OO0O0O0000OOOO0 ["数量均值"]+O0OO0O0O0000OOOO0 ["数量标准差"])),"风险评分"]=O0OO0O0O0000OOOO0 ["风险评分"]+1 #line:687
            O0OO0O0O0000OOOO0 .loc [(O0OO0O0O0000OOOO0 ["计数"]>=O0OO0O0O0000OOOO0 ["数量CI"]),"风险评分"]=O0OO0O0O0000OOOO0 ["风险评分"]+1 #line:688
            O0OO0O0O0000OOOO0 .loc [(O0OO0O0O0000OOOO0 ["关键字数量比例"]>0.5 )&(O0OO0O0O0000OOOO0 ["计数"]>=3 ),"风险评分"]=O0OO0O0O0000OOOO0 ["风险评分"]+1 #line:689
            O0OO0O0O0000OOOO0 =O0OO0O0O0000OOOO0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:691
        O0000OO0OOO000OO0 =O0OO0O0O0000OOOO0 .columns .to_list ()#line:701
        OO00O00O000000OOO =O0000OO0OOO000OO0 [O0000OO0OOO000OO0 .index ("关键字")+1 ]#line:702
        OOO0O0OOO0000O0OO =pd .pivot_table (O0OO0O0O0000OOOO0 ,index =OO00O00O000000OOO ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:713
        OOO0O0OOO0000O0OO .columns =OOO0O0OOO0000O0OO .columns .droplevel (0 )#line:714
        OOO0O0OOO0000O0OO =pd .merge (OOO0O0OOO0000O0OO ,O0OO0O0O0000OOOO0 [[OO00O00O000000OOO ,"该元素总数量"]].drop_duplicates (OO00O00O000000OOO ),on =[OO00O00O000000OOO ],how ="left")#line:717
        del OOO0O0OOO0000O0OO ["All"]#line:719
        OOO0O0OOO0000O0OO .iloc [-1 ,-1 ]=OOO0O0OOO0000O0OO ["该元素总数量"].sum (axis =0 )#line:720
        print ("耗时：",(time .time ()-OOO00OOO00O00OOO0 ))#line:722
        return OOO0O0OOO0000O0OO #line:725
def Tread_TOOLS_bar (O000O000OOOOO0000 ):#line:733
         ""#line:734
         O0O000O0O00O00O0O =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:735
         OO0O0OO00O00OOO00 =[pd .read_excel (O0OOO000O0000O00O ,header =0 ,sheet_name =0 )for O0OOO000O0000O00O in O0O000O0O00O00O0O ]#line:736
         OO0O0000OOO0O00O0 =pd .concat (OO0O0OO00O00OOO00 ,ignore_index =True )#line:737
         OO000OOOO0O0O000O =pd .pivot_table (OO0O0000OOO0O00O0 ,index ="对象",columns ="关键词",values =O000O000OOOOO0000 ,aggfunc ="sum",fill_value ="0",margins =True ,dropna =False ,).reset_index ()#line:747
         del OO000OOOO0O0O000O ["All"]#line:749
         OO000OOOO0O0O000O =OO000OOOO0O0O000O [:-1 ]#line:750
         Tread_TOOLS_tree_Level_2 (OO000OOOO0O0O000O ,0 ,0 )#line:752
def Tread_TOOLS_analysis (O0O0OO0OO0OOO0OO0 ):#line:757
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
    O00O000000OO0OO00 =TT_biaozhun ["设置"]#line:770
    TT_ori ["作用对象"]=""#line:771
    for OOOOOOOOO000OOO00 in TOOLS_get_list (O00O000000OO0OO00 .loc [0 ,"值"]):#line:772
        TT_ori ["作用对象"]=TT_ori ["作用对象"]+"-"+TT_ori [OOOOOOOOO000OOO00 ].fillna ("未填写").astype ("str")#line:773
    OO0O0O0O00O000OO0 =Toplevel ()#line:776
    OO0O0O0O00O000OO0 .title ("单品分析")#line:777
    OOOOO00OO0OO0OO00 =OO0O0O0O00O000OO0 .winfo_screenwidth ()#line:778
    O00000OO0OO00OO00 =OO0O0O0O00O000OO0 .winfo_screenheight ()#line:780
    O00OOO00OOOOO0O00 =580 #line:782
    OO000O0OO0OO0OOO0 =80 #line:783
    OO00O00OO000OOOO0 =(OOOOO00OO0OO0OO00 -O00OOO00OOOOO0O00 )/1.7 #line:785
    O000O0OOOO0000O00 =(O00000OO0OO00OO00 -OO000O0OO0OO0OOO0 )/2 #line:786
    OO0O0O0O00O000OO0 .geometry ("%dx%d+%d+%d"%(O00OOO00OOOOO0O00 ,OO000O0OO0OO0OOO0 ,OO00O00OO000OOOO0 ,O000O0OOOO0000O00 ))#line:787
    O0O0O0O0O0OO00OO0 =Label (OO0O0O0O00O000OO0 ,text ="作用对象：")#line:790
    O0O0O0O0O0OO00OO0 .grid (row =1 ,column =0 ,sticky ="w")#line:791
    O000000O0OO0000OO =StringVar ()#line:792
    O0OO0O00000000000 =ttk .Combobox (OO0O0O0O00O000OO0 ,width =25 ,height =10 ,state ="readonly",textvariable =O000000O0OO0000OO )#line:795
    O0OO0O00000000000 ["values"]=list (set (TT_ori ["作用对象"].to_list ()))#line:796
    O0OO0O00000000000 .current (0 )#line:797
    O0OO0O00000000000 .grid (row =1 ,column =1 )#line:798
    O0O000OO000OOO0OO =Label (OO0O0O0O00O000OO0 ,text ="分析对象：")#line:800
    O0O000OO000OOO0OO .grid (row =1 ,column =2 ,sticky ="w")#line:801
    O0O0OO00000OOO0OO =StringVar ()#line:804
    O0O000OO000O000O0 =ttk .Combobox (OO0O0O0O00O000OO0 ,width =15 ,height =10 ,state ="readonly",textvariable =O0O0OO00000OOO0OO )#line:807
    O0O000OO000O000O0 ["values"]=["事件发生月份","事件发生季度","产品批号","型号","规格"]#line:808
    O0O000OO000O000O0 .current (0 )#line:810
    O0O000OO000O000O0 .grid (row =1 ,column =3 )#line:811
    OO0O000O000OO0O00 =Label (OO0O0O0O00O000OO0 ,text ="事件发生起止时间：")#line:816
    OO0O000O000OO0O00 .grid (row =2 ,column =0 ,sticky ="w")#line:817
    O00OO00O0OO0O00OO =Entry (OO0O0O0O00O000OO0 ,width =10 )#line:819
    O00OO00O0OO0O00OO .insert (0 ,min (TT_ori ["事件发生日期"].dt .date ))#line:820
    O00OO00O0OO0O00OO .grid (row =2 ,column =1 ,sticky ="w")#line:821
    O0000O0O00OO0000O =Entry (OO0O0O0O00O000OO0 ,width =10 )#line:823
    O0000O0O00OO0000O .insert (0 ,max (TT_ori ["事件发生日期"].dt .date ))#line:824
    O0000O0O00OO0000O .grid (row =2 ,column =2 ,sticky ="w")#line:825
    OOOO00OO00OO0OOOO =Button (OO0O0O0O00O000OO0 ,text ="原始查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O0OO0O00000000000 .get (),O0O000OO000O000O0 .get (),O00OO00O0OO0O00OO .get (),O0000O0O00OO0000O .get (),1 ))#line:835
    OOOO00OO00OO0OOOO .grid (row =3 ,column =2 ,sticky ="w")#line:836
    OOOO00OO00OO0OOOO =Button (OO0O0O0O00O000OO0 ,text ="分类查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O0OO0O00000000000 .get (),O0O000OO000O000O0 .get (),O00OO00O0OO0O00OO .get (),O0000O0O00OO0000O .get (),0 ))#line:846
    OOOO00OO00OO0OOOO .grid (row =3 ,column =3 ,sticky ="w")#line:847
    OOOO00OO00OO0OOOO =Button (OO0O0O0O00O000OO0 ,text ="趋势分析",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O0OO0O00000000000 .get (),O0O000OO000O000O0 .get (),O00OO00O0OO0O00OO .get (),O0000O0O00OO0000O .get (),2 ))#line:857
    OOOO00OO00OO0OOOO .grid (row =3 ,column =1 ,sticky ="w")#line:858
def Tread_TOOLS_doing (OOO00OOO00O00O000 ,O00OO000OO00OOO0O ,OO0OO0OOO00000OOO ,OO0OOO00OOO0OO00O ,OO0O0OO000OO0O0OO ,OOO0OO000O0O000OO ):#line:860
    ""#line:861
    global TT_biaozhun #line:862
    OOO00OOO00O00O000 =OOO00OOO00O00O000 [(OOO00OOO00O00O000 ["作用对象"]==O00OO000OO00OOO0O )].copy ()#line:863
    OO0OOO00OOO0OO00O =pd .to_datetime (OO0OOO00OOO0OO00O )#line:865
    OO0O0OO000OO0O0OO =pd .to_datetime (OO0O0OO000OO0O0OO )#line:866
    OOO00OOO00O00O000 =OOO00OOO00O00O000 [((OOO00OOO00O00O000 ["事件发生日期"]>=OO0OOO00OOO0OO00O )&(OOO00OOO00O00O000 ["事件发生日期"]<=OO0O0OO000OO0O0OO ))]#line:867
    text .insert (END ,"\n数据数量："+str (len (OOO00OOO00O00O000 )))#line:868
    text .see (END )#line:869
    if OOO0OO000O0O000OO ==0 :#line:871
        Tread_TOOLS_check (OOO00OOO00O00O000 ,TT_biaozhun ["关键字表"],0 )#line:872
        return 0 #line:873
    if OOO0OO000O0O000OO ==1 :#line:874
        Tread_TOOLS_tree_Level_2 (OOO00OOO00O00O000 ,1 ,OOO00OOO00O00O000 )#line:875
        return 0 #line:876
    if len (OOO00OOO00O00O000 )<1 :#line:877
        showinfo (title ="错误信息",message ="没有符合筛选条件的报告。")#line:878
        return 0 #line:879
    Tread_TOOLS_check (OOO00OOO00O00O000 ,TT_biaozhun ["关键字表"],1 )#line:880
    Tread_TOOLS_tree_Level_2 (Tread_TOOLS_Countall (OOO00OOO00O00O000 ).df_find_all_keword_risk (OO0OO0OOO00000OOO ),1 ,0 ,OO0OO0OOO00000OOO )#line:883
def STAT_countx (O00O0OOO00OO0OO00 ):#line:893
    ""#line:894
    return O00O0OOO00OO0OO00 .value_counts ().to_dict ()#line:895
def STAT_countpx (O000OOOOO00O00O0O ,OOOOO00OOOOOO0OOO ):#line:897
    ""#line:898
    return len (O000OOOOO00O00O0O [(O000OOOOO00O00O0O ==OOOOO00OOOOOO0OOO )])#line:899
def STAT_countnpx (O00O00000O00O00OO ,OO000OO000OO0000O ):#line:901
    ""#line:902
    return len (O00O00000O00O00OO [(O00O00000O00O00OO not in OO000OO000OO0000O )])#line:903
def STAT_get_max (OOO00O0OO00OO0O0O ):#line:905
    ""#line:906
    return OOO00O0OO00OO0O0O .value_counts ().max ()#line:907
def STAT_get_mean (OOO0OO00000000O00 ):#line:909
    ""#line:910
    return round (OOO0OO00000000O00 .value_counts ().mean (),2 )#line:911
def STAT_get_std (O0OOOOO0OOOO0OOO0 ):#line:913
    ""#line:914
    return round (O0OOOOO0OOOO0OOO0 .value_counts ().std (ddof =1 ),2 )#line:915
def STAT_get_95ci (OO0O0OO00OOO0OO0O ):#line:917
    ""#line:918
    return round (np .percentile (OO0O0OO00OOO0OO0O .value_counts (),97.5 ),2 )#line:919
def STAT_get_mean_std_ci (OOO00000O0OOOO0O0 ,O0OO0O00000O00000 ):#line:921
    ""#line:922
    warnings .filterwarnings ("ignore")#line:923
    OO0O0OOOO0000OOOO =TOOLS_strdict_to_pd (str (OOO00000O0OOOO0O0 ))["content"].values /O0OO0O00000O00000 #line:924
    O00OO0O00O00OOOO0 =round (OO0O0OOOO0000OOOO .mean (),2 )#line:925
    O000OOO0000OOO000 =round (OO0O0OOOO0000OOOO .std (ddof =1 ),2 )#line:926
    OO0OOO00OO0OO00OO =round (np .percentile (OO0O0OOOO0000OOOO ,97.5 ),2 )#line:927
    return pd .Series ((O00OO0O00O00OOOO0 ,O000OOO0000OOO000 ,OO0OOO00OO0OO00OO ))#line:928
def STAT_findx_value (O0O0O0O0000O0O0O0 ,OOO0O00O0OO000OO0 ):#line:930
    ""#line:931
    warnings .filterwarnings ("ignore")#line:932
    O0OOOOO000O0000O0 =TOOLS_strdict_to_pd (str (O0O0O0O0000O0O0O0 ))#line:933
    OO0OO0O0OO0O00OOO =O0OOOOO000O0000O0 .where (O0OOOOO000O0000O0 ["index"]==str (OOO0O00O0OO000OO0 ))#line:935
    print (OO0OO0O0OO0O00OOO )#line:936
    return OO0OO0O0OO0O00OOO #line:937
def STAT_judge_x (OOOOO0OOO0OO00OOO ,OO00OO0000OOO0O00 ):#line:939
    ""#line:940
    for OO0OO000000O00OO0 in OO00OO0000OOO0O00 :#line:941
        if OOOOO0OOO0OO00OOO .find (OO0OO000000O00OO0 )>-1 :#line:942
            return 1 #line:943
def STAT_basic_risk (OO0OOOO0O00O00O00 ,O00000OO00OO0OOOO ,OOOOO00O00OOO0O00 ,O0000OO00000O0OOO ,O00O00O0O0OO00O00 ):#line:946
    ""#line:947
    OO0OOOO0O00O00O00 ["风险评分"]=0 #line:948
    OO0OOOO0O00O00O00 .loc [((OO0OOOO0O00O00O00 [O00000OO00OO0OOOO ]>=3 )&(OO0OOOO0O00O00O00 [OOOOO00O00OOO0O00 ]>=1 ))|(OO0OOOO0O00O00O00 [O00000OO00OO0OOOO ]>=5 ),"风险评分"]=OO0OOOO0O00O00O00 ["风险评分"]+5 #line:949
    OO0OOOO0O00O00O00 .loc [(OO0OOOO0O00O00O00 [OOOOO00O00OOO0O00 ]>=3 ),"风险评分"]=OO0OOOO0O00O00O00 ["风险评分"]+1 #line:950
    OO0OOOO0O00O00O00 .loc [(OO0OOOO0O00O00O00 [O0000OO00000O0OOO ]>=1 ),"风险评分"]=OO0OOOO0O00O00O00 ["风险评分"]+10 #line:951
    OO0OOOO0O00O00O00 ["风险评分"]=OO0OOOO0O00O00O00 ["风险评分"]+OO0OOOO0O00O00O00 [O00O00O0O0OO00O00 ]/100 #line:952
    return OO0OOOO0O00O00O00 #line:953
def STAT_find_keyword_risk (OO00O000OO0OO0O0O ,OOOOO00OOOOO0O0O0 ,O00O0OOO00OOO00O0 ,O0OO0OOOOO0OOO0OO ,O0O000OOOO000OOOO ):#line:957
        ""#line:958
        O00OO000O00000000 =OO00O000OO0OO0O0O .groupby (OOOOO00OOOOO0O0O0 ).agg (证号关键字总数量 =(O00O0OOO00OOO00O0 ,"count"),包含元素个数 =(O0OO0OOOOO0OOO0OO ,"nunique"),包含元素 =(O0OO0OOOOO0OOO0OO ,STAT_countx ),).reset_index ()#line:963
        OO0OO00O000000O00 =OOOOO00OOOOO0O0O0 .copy ()#line:965
        OO0OO00O000000O00 .append (O0OO0OOOOO0OOO0OO )#line:966
        O0000O0O0O0O0O0OO =OO00O000OO0OO0O0O .groupby (OO0OO00O000000O00 ).agg (计数 =(O0OO0OOOOO0OOO0OO ,"count"),).reset_index ()#line:969
        O0OOO000OOO0O0OOO =OO0OO00O000000O00 .copy ()#line:972
        O0OOO000OOO0O0OOO .remove ("关键字")#line:973
        OO000OOO0000OO0OO =OO00O000OO0OO0O0O .groupby (O0OOO000OOO0O0OOO ).agg (该元素总数 =(O0OO0OOOOO0OOO0OO ,"count"),).reset_index ()#line:976
        O0000O0O0O0O0O0OO ["证号总数"]=O0O000OOOO000OOOO #line:978
        OO00OO00OOO0OO0OO =pd .merge (O0000O0O0O0O0O0OO ,O00OO000O00000000 ,on =OOOOO00OOOOO0O0O0 ,how ="left")#line:979
        if len (OO00OO00OOO0OO0OO )>0 :#line:981
            OO00OO00OOO0OO0OO [['数量均值','数量标准差','数量CI']]=OO00OO00OOO0OO0OO .包含元素 .apply (lambda O0OO00O000000O0O0 :STAT_get_mean_std_ci (O0OO00O000000O0O0 ,1 ))#line:982
        return OO00OO00OOO0OO0OO #line:983
def STAT_find_risk (O00OO00OO0O0O0O0O ,OOOO00OO0O0OOOO0O ,OO0OO00000OO000OO ,OOOO0O000OO000OO0 ):#line:989
        ""#line:990
        O00O00OO0O000OO00 =O00OO00OO0O0O0O0O .groupby (OOOO00OO0O0OOOO0O ).agg (证号总数量 =(OO0OO00000OO000OO ,"count"),包含元素个数 =(OOOO0O000OO000OO0 ,"nunique"),包含元素 =(OOOO0O000OO000OO0 ,STAT_countx ),均值 =(OOOO0O000OO000OO0 ,STAT_get_mean ),标准差 =(OOOO0O000OO000OO0 ,STAT_get_std ),CI上限 =(OOOO0O000OO000OO0 ,STAT_get_95ci ),).reset_index ()#line:998
        OO00OOO00000OOOOO =OOOO00OO0O0OOOO0O .copy ()#line:1000
        OO00OOO00000OOOOO .append (OOOO0O000OO000OO0 )#line:1001
        OO00OO0O00O0000O0 =O00OO00OO0O0O0O0O .groupby (OO00OOO00000OOOOO ).agg (计数 =(OOOO0O000OO000OO0 ,"count"),严重伤害数 =("伤害",lambda OO0O00O0O00OOO00O :STAT_countpx (OO0O00O0O00OOO00O .values ,"严重伤害")),死亡数量 =("伤害",lambda O0OOOOOOOO0OO0O0O :STAT_countpx (O0OOOOOOOO0OO0O0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:1008
        OO0OOO000OO000O0O =pd .merge (OO00OO0O00O0000O0 ,O00O00OO0O000OO00 ,on =OOOO00OO0O0OOOO0O ,how ="left")#line:1010
        OO0OOO000OO000O0O ["风险评分"]=0 #line:1012
        OO0OOO000OO000O0O ["报表类型"]="dfx_findrisk"+OOOO0O000OO000OO0 #line:1013
        OO0OOO000OO000O0O .loc [((OO0OOO000OO000O0O ["计数"]>=3 )&(OO0OOO000OO000O0O ["严重伤害数"]>=1 )|(OO0OOO000OO000O0O ["计数"]>=5 )),"风险评分"]=OO0OOO000OO000O0O ["风险评分"]+5 #line:1014
        OO0OOO000OO000O0O .loc [(OO0OOO000OO000O0O ["计数"]>=(OO0OOO000OO000O0O ["均值"]+OO0OOO000OO000O0O ["标准差"])),"风险评分"]=OO0OOO000OO000O0O ["风险评分"]+1 #line:1015
        OO0OOO000OO000O0O .loc [(OO0OOO000OO000O0O ["计数"]>=OO0OOO000OO000O0O ["CI上限"]),"风险评分"]=OO0OOO000OO000O0O ["风险评分"]+1 #line:1016
        OO0OOO000OO000O0O .loc [(OO0OOO000OO000O0O ["严重伤害数"]>=3 )&(OO0OOO000OO000O0O ["风险评分"]>=7 ),"风险评分"]=OO0OOO000OO000O0O ["风险评分"]+1 #line:1017
        OO0OOO000OO000O0O .loc [(OO0OOO000OO000O0O ["死亡数量"]>=1 ),"风险评分"]=OO0OOO000OO000O0O ["风险评分"]+10 #line:1018
        OO0OOO000OO000O0O ["风险评分"]=OO0OOO000OO000O0O ["风险评分"]+OO0OOO000OO000O0O ["单位个数"]/100 #line:1019
        OO0OOO000OO000O0O =OO0OOO000OO000O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:1020
        return OO0OOO000OO000O0O #line:1022
def TOOLS_get_list (O000000OOO0OO00O0 ):#line:1024
    ""#line:1025
    O000000OOO0OO00O0 =str (O000000OOO0OO00O0 )#line:1026
    O0O00O0O000O0O000 =[]#line:1027
    O0O00O0O000O0O000 .append (O000000OOO0OO00O0 )#line:1028
    O0O00O0O000O0O000 =",".join (O0O00O0O000O0O000 )#line:1029
    O0O00O0O000O0O000 =O0O00O0O000O0O000 .split ("|")#line:1030
    OO0OO000O0O00OO0O =O0O00O0O000O0O000 [:]#line:1031
    O0O00O0O000O0O000 =list (set (O0O00O0O000O0O000 ))#line:1032
    O0O00O0O000O0O000 .sort (key =OO0OO000O0O00OO0O .index )#line:1033
    return O0O00O0O000O0O000 #line:1034
def TOOLS_get_list0 (OO00O0O00OOOOO0OO ,OO00OO00O000OOOOO ,*OO00O0O0O00O000OO ):#line:1036
    ""#line:1037
    OO00O0O00OOOOO0OO =str (OO00O0O00OOOOO0OO )#line:1038
    if pd .notnull (OO00O0O00OOOOO0OO ):#line:1040
        try :#line:1041
            if "use("in str (OO00O0O00OOOOO0OO ):#line:1042
                OOO00O0O000OO0000 =OO00O0O00OOOOO0OO #line:1043
                O0000O0OO00OO0O00 =re .compile (r"[(](.*?)[)]",re .S )#line:1044
                OO0000O0OO00000OO =re .findall (O0000O0OO00OO0O00 ,OOO00O0O000OO0000 )#line:1045
                OOO00OO0O0OOOOOO0 =[]#line:1046
                if ").list"in OO00O0O00OOOOO0OO :#line:1047
                    O0OO000000OO00O0O ="配置表/"+str (OO0000O0OO00000OO [0 ])+".xls"#line:1048
                    O0O0OO0O0O0O000O0 =pd .read_excel (O0OO000000OO00O0O ,sheet_name =OO0000O0OO00000OO [0 ],header =0 ,index_col =0 ).reset_index ()#line:1051
                    O0O0OO0O0O0O000O0 ["检索关键字"]=O0O0OO0O0O0O000O0 ["检索关键字"].astype (str )#line:1052
                    OOO00OO0O0OOOOOO0 =O0O0OO0O0O0O000O0 ["检索关键字"].tolist ()+OOO00OO0O0OOOOOO0 #line:1053
                if ").file"in OO00O0O00OOOOO0OO :#line:1054
                    OOO00OO0O0OOOOOO0 =OO00OO00O000OOOOO [OO0000O0OO00000OO [0 ]].astype (str ).tolist ()+OOO00OO0O0OOOOOO0 #line:1056
                try :#line:1059
                    if "报告类型-新的"in OO00OO00O000OOOOO .columns :#line:1060
                        OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1061
                        OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split (";")#line:1062
                        OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1063
                        OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split ("；")#line:1064
                        OOO00OO0O0OOOOOO0 =[OO0O00000O000000O .replace ("（严重）","")for OO0O00000O000000O in OOO00OO0O0OOOOOO0 ]#line:1065
                        OOO00OO0O0OOOOOO0 =[O0OO000O0000O0OOO .replace ("（一般）","")for O0OO000O0000O0OOO in OOO00OO0O0OOOOOO0 ]#line:1066
                except :#line:1067
                    pass #line:1068
                OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1071
                OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split ("、")#line:1072
                OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1073
                OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split ("，")#line:1074
                OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1075
                OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split (",")#line:1076
                OOO00OOO0O00O0O00 =OOO00OO0O0OOOOOO0 [:]#line:1078
                try :#line:1079
                    if OO00O0O0O00O000OO [0 ]==1000 :#line:1080
                      pass #line:1081
                except :#line:1082
                      OOO00OO0O0OOOOOO0 =list (set (OOO00OO0O0OOOOOO0 ))#line:1083
                OOO00OO0O0OOOOOO0 .sort (key =OOO00OOO0O00O0O00 .index )#line:1084
            else :#line:1086
                OO00O0O00OOOOO0OO =str (OO00O0O00OOOOO0OO )#line:1087
                OOO00OO0O0OOOOOO0 =[]#line:1088
                OOO00OO0O0OOOOOO0 .append (OO00O0O00OOOOO0OO )#line:1089
                OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1090
                OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split ("、")#line:1091
                OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1092
                OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split ("，")#line:1093
                OOO00OO0O0OOOOOO0 =",".join (OOO00OO0O0OOOOOO0 )#line:1094
                OOO00OO0O0OOOOOO0 =OOO00OO0O0OOOOOO0 .split (",")#line:1095
                OOO00OOO0O00O0O00 =OOO00OO0O0OOOOOO0 [:]#line:1097
                try :#line:1098
                    if OO00O0O0O00O000OO [0 ]==1000 :#line:1099
                      OOO00OO0O0OOOOOO0 =list (set (OOO00OO0O0OOOOOO0 ))#line:1100
                except :#line:1101
                      pass #line:1102
                OOO00OO0O0OOOOOO0 .sort (key =OOO00OOO0O00O0O00 .index )#line:1103
                OOO00OO0O0OOOOOO0 .sort (key =OOO00OOO0O00O0O00 .index )#line:1104
        except ValueError2 :#line:1106
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:1107
            return False #line:1108
    return OOO00OO0O0OOOOOO0 #line:1110
def TOOLS_strdict_to_pd (OO0O00OO0OO000OOO ):#line:1111
    ""#line:1112
    return pd .DataFrame .from_dict (eval (OO0O00OO0OO000OOO ),orient ="index",columns =["content"]).reset_index ()#line:1113
def Tread_TOOLS_view_dict (OO0O00O0OO0000000 ,O00OO0OOO0000O0OO ):#line:1115
    ""#line:1116
    OOO000OO0OOOOO0OO =Toplevel ()#line:1117
    OOO000OO0OOOOO0OO .title ("查看数据")#line:1118
    OOO000OO0OOOOO0OO .geometry ("700x500")#line:1119
    OO000O0OO0OO00000 =Scrollbar (OOO000OO0OOOOO0OO )#line:1121
    O00O00000OOO0OO00 =Text (OOO000OO0OOOOO0OO ,height =100 ,width =150 )#line:1122
    OO000O0OO0OO00000 .pack (side =RIGHT ,fill =Y )#line:1123
    O00O00000OOO0OO00 .pack ()#line:1124
    OO000O0OO0OO00000 .config (command =O00O00000OOO0OO00 .yview )#line:1125
    O00O00000OOO0OO00 .config (yscrollcommand =OO000O0OO0OO00000 .set )#line:1126
    if O00OO0OOO0000O0OO ==1 :#line:1127
        O00O00000OOO0OO00 .insert (END ,OO0O00O0OO0000000 )#line:1129
        O00O00000OOO0OO00 .insert (END ,"\n\n")#line:1130
        return 0 #line:1131
    for OO00OOOOO0OO00O0O in range (len (OO0O00O0OO0000000 )):#line:1132
        O00O00000OOO0OO00 .insert (END ,OO0O00O0OO0000000 .iloc [OO00OOOOO0OO00O0O ,0 ])#line:1133
        O00O00000OOO0OO00 .insert (END ,":")#line:1134
        O00O00000OOO0OO00 .insert (END ,OO0O00O0OO0000000 .iloc [OO00OOOOO0OO00O0O ,1 ])#line:1135
        O00O00000OOO0OO00 .insert (END ,"\n\n")#line:1136
def Tread_TOOLS_fashenglv (OO0OO00OOO0O0O00O ,O0000O00000000OO0 ):#line:1139
    global TT_biaozhun #line:1140
    OO0OO00OOO0O0O00O =pd .merge (OO0OO00OOO0O0O00O ,TT_biaozhun [O0000O00000000OO0 ],on =[O0000O00000000OO0 ],how ="left").reset_index (drop =True )#line:1141
    O0O0OO000O00OO0O0 =OO0OO00OOO0O0O00O ["使用次数"].mean ()#line:1143
    OO0OO00OOO0O0O00O ["使用次数"]=OO0OO00OOO0O0O00O ["使用次数"].fillna (int (O0O0OO000O00OO0O0 ))#line:1144
    O0OO0OO00OOO0OOO0 =OO0OO00OOO0O0O00O ["使用次数"][:-1 ].sum ()#line:1145
    OO0OO00OOO0O0O00O .iloc [-1 ,-1 ]=O0OO0OO00OOO0OOO0 #line:1146
    O0000OO0O0OO00000 =[OO00O00O00OO000O0 for OO00O00O00OO000O0 in OO0OO00OOO0O0O00O .columns if (OO00O00O00OO000O0 not in ["使用次数",O0000O00000000OO0 ])]#line:1147
    for OOO00O0O0OO0O00O0 ,O00O00OO0OO0O0O00 in OO0OO00OOO0O0O00O .iterrows ():#line:1148
        for OO000000000O00OO0 in O0000OO0O0OO00000 :#line:1149
            OO0OO00OOO0O0O00O .loc [OOO00O0O0OO0O00O0 ,OO000000000O00OO0 ]=int (O00O00OO0OO0O0O00 [OO000000000O00OO0 ])/int (O00O00OO0OO0O0O00 ["使用次数"])#line:1150
    del OO0OO00OOO0O0O00O ["使用次数"]#line:1151
    Tread_TOOLS_tree_Level_2 (OO0OO00OOO0O0O00O ,1 ,1 ,O0000O00000000OO0 )#line:1152
def TOOLS_save_dict (O0000OOO0O0000O00 ):#line:1154
    ""#line:1155
    OOO0000O00O0O00OO =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="【排序后的原始数据】",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1161
    try :#line:1162
        O0000OOO0O0000O00 ["详细描述T"]=O0000OOO0O0000O00 ["详细描述T"].astype (str )#line:1163
    except :#line:1164
        pass #line:1165
    try :#line:1166
        O0000OOO0O0000O00 ["报告编码"]=O0000OOO0O0000O00 ["报告编码"].astype (str )#line:1167
    except :#line:1168
        pass #line:1169
    try :#line:1170
        O00OOOO000OOO0OOO =re .search ("\【(.*?)\】",OOO0000O00O0O00OO )#line:1171
        O0000OOO0O0000O00 ["对象"]=O00OOOO000OOO0OOO .group (1 )#line:1172
    except :#line:1173
        pass #line:1174
    O00000OOOO00O0OOO =pd .ExcelWriter (OOO0000O00O0O00OO ,engine ="xlsxwriter")#line:1175
    O0000OOO0O0000O00 .to_excel (O00000OOOO00O0OOO ,sheet_name ="字典数据")#line:1176
    O00000OOOO00O0OOO .close ()#line:1177
    showinfo (title ="提示",message ="文件写入成功。")#line:1178
def Tread_TOOLS_DRAW_histbar (OOOOO0OOOO0O00OO0 ):#line:1182
    ""#line:1183
    OOOOO0O0OO000O0OO =Toplevel ()#line:1186
    OOOOO0O0OO000O0OO .title ("直方图")#line:1187
    O00O0O00OO00OO000 =ttk .Frame (OOOOO0O0OO000O0OO ,height =20 )#line:1188
    O00O0O00OO00OO000 .pack (side =TOP )#line:1189
    O00OO0OOOOO0OOO00 =Figure (figsize =(12 ,6 ),dpi =100 )#line:1191
    O00O0000O000OOOO0 =FigureCanvasTkAgg (O00OO0OOOOO0OOO00 ,master =OOOOO0O0OO000O0OO )#line:1192
    O00O0000O000OOOO0 .draw ()#line:1193
    O00O0000O000OOOO0 .get_tk_widget ().pack (expand =1 )#line:1194
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1196
    plt .rcParams ['axes.unicode_minus']=False #line:1197
    O00O0000000OOO00O =NavigationToolbar2Tk (O00O0000O000OOOO0 ,OOOOO0O0OO000O0OO )#line:1199
    O00O0000000OOO00O .update ()#line:1200
    O00O0000O000OOOO0 .get_tk_widget ().pack ()#line:1201
    O00OO0O00OO0O00OO =O00OO0OOOOO0OOO00 .add_subplot (111 )#line:1203
    O00OO0O00OO0O00OO .set_title ("直方图")#line:1205
    OOO00OO00O0O00OOO =OOOOO0OOOO0O00OO0 .columns .to_list ()#line:1207
    OOO00OO00O0O00OOO .remove ("对象")#line:1208
    OOOOOOO0OOOO00OO0 =np .arange (len (OOO00OO00O0O00OOO ))#line:1209
    for OOO0O0O00OO0O00O0 in OOO00OO00O0O00OOO :#line:1213
        OOOOO0OOOO0O00OO0 [OOO0O0O00OO0O00O0 ]=OOOOO0OOOO0O00OO0 [OOO0O0O00OO0O00O0 ].astype (float )#line:1214
    OOOOO0OOOO0O00OO0 ['数据']=OOOOO0OOOO0O00OO0 [OOO00OO00O0O00OOO ].values .tolist ()#line:1216
    OOOOOO0OO00OO0O00 =0 #line:1217
    for OO000OO000O000O00 ,OO00000O000O0OOOO in OOOOO0OOOO0O00OO0 .iterrows ():#line:1218
        O00OO0O00OO0O00OO .bar ([O0O00O0OOO0000000 +OOOOOO0OO00OO0O00 for O0O00O0OOO0000000 in OOOOOOO0OOOO00OO0 ],OOOOO0OOOO0O00OO0 .loc [OO000OO000O000O00 ,'数据'],label =OOO00OO00O0O00OOO ,width =0.1 )#line:1219
        for OO000O0OO0OO0O0O0 ,OOO00O00000O000O0 in zip ([OO0OOOO00OO00OOO0 +OOOOOO0OO00OO0O00 for OO0OOOO00OO00OOO0 in OOOOOOO0OOOO00OO0 ],OOOOO0OOOO0O00OO0 .loc [OO000OO000O000O00 ,'数据']):#line:1222
           O00OO0O00OO0O00OO .text (OO000O0OO0OO0O0O0 -0.015 ,OOO00O00000O000O0 +0.07 ,str (int (OOO00O00000O000O0 )),color ='black',size =8 )#line:1223
        OOOOOO0OO00OO0O00 =OOOOOO0OO00OO0O00 +0.1 #line:1225
    O00OO0O00OO0O00OO .set_xticklabels (OOOOO0OOOO0O00OO0 .columns .to_list (),rotation =-90 ,fontsize =8 )#line:1227
    O00OO0O00OO0O00OO .legend (OOOOO0OOOO0O00OO0 ["对象"])#line:1231
    O00O0000O000OOOO0 .draw ()#line:1234
def Tread_TOOLS_DRAW_make_risk_plot (O0OOOO0O00OOO000O ,OOOO0000000OO0OO0 ,O0O0O0OOOO0O0OO00 ,OO000O000OO0OOOO0 ,O0OOO000O0O00OOO0 ):#line:1236
    ""#line:1237
    O0O0OO000OOO0O00O =Toplevel ()#line:1240
    O0O0OO000OOO0O00O .title (OO000O000OO0OOOO0 )#line:1241
    O0O00OOOO0O0O0OO0 =ttk .Frame (O0O0OO000OOO0O00O ,height =20 )#line:1242
    O0O00OOOO0O0O0OO0 .pack (side =TOP )#line:1243
    O0O00O00000O0OO00 =Figure (figsize =(12 ,6 ),dpi =100 )#line:1245
    O000O0O0O00O0OOOO =FigureCanvasTkAgg (O0O00O00000O0OO00 ,master =O0O0OO000OOO0O00O )#line:1246
    O000O0O0O00O0OOOO .draw ()#line:1247
    O000O0O0O00O0OOOO .get_tk_widget ().pack (expand =1 )#line:1248
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1250
    plt .rcParams ['axes.unicode_minus']=False #line:1251
    OOO0O000000OO000O =NavigationToolbar2Tk (O000O0O0O00O0OOOO ,O0O0OO000OOO0O00O )#line:1253
    OOO0O000000OO000O .update ()#line:1254
    O000O0O0O00O0OOOO .get_tk_widget ().pack ()#line:1255
    OO0000000OOO00O00 =O0O00O00000O0OO00 .add_subplot (111 )#line:1257
    OO0000000OOO00O00 .set_title (OO000O000OO0OOOO0 )#line:1259
    OO0OO0OO0OOO0OOO0 =O0OOOO0O00OOO000O [OOOO0000000OO0OO0 ]#line:1260
    if O0OOO000O0O00OOO0 !=999 :#line:1263
        OO0000000OOO00O00 .set_xticklabels (OO0OO0OO0OOO0OOO0 ,rotation =-90 ,fontsize =8 )#line:1264
    O0OO0000O00OO0O0O =range (0 ,len (OO0OO0OO0OOO0OOO0 ),1 )#line:1267
    for O0OOO00000OO00OOO in O0O0O0OOOO0O0OO00 :#line:1272
        OOOOO0OO0O00OOOOO =O0OOOO0O00OOO000O [O0OOO00000OO00OOO ].astype (float )#line:1273
        if O0OOO00000OO00OOO =="关注区域":#line:1275
            OO0000000OOO00O00 .plot (list (OO0OO0OO0OOO0OOO0 ),list (OOOOO0OO0O00OOOOO ),label =str (O0OOO00000OO00OOO ),color ="red")#line:1276
        else :#line:1277
            OO0000000OOO00O00 .plot (list (OO0OO0OO0OOO0OOO0 ),list (OOOOO0OO0O00OOOOO ),label =str (O0OOO00000OO00OOO ))#line:1278
        if O0OOO000O0O00OOO0 ==100 :#line:1281
            for O0O000O00O00O0OOO ,OOO00OOOO00O000OO in zip (OO0OO0OO0OOO0OOO0 ,OOOOO0OO0O00OOOOO ):#line:1282
                if OOO00OOOO00O000OO ==max (OOOOO0OO0O00OOOOO )and OOO00OOOO00O000OO >=3 and len (O0O0O0OOOO0O0OO00 )!=1 :#line:1283
                     OO0000000OOO00O00 .text (O0O000O00O00O0OOO ,OOO00OOOO00O000OO ,(str (O0OOO00000OO00OOO )+":"+str (int (OOO00OOOO00O000OO ))),color ='black',size =8 )#line:1284
                if len (O0O0O0OOOO0O0OO00 )==1 and OOO00OOOO00O000OO >=0.01 :#line:1285
                     OO0000000OOO00O00 .text (O0O000O00O00O0OOO ,OOO00OOOO00O000OO ,str (int (OOO00OOOO00O000OO )),color ='black',size =8 )#line:1286
    if len (O0O0O0OOOO0O0OO00 )==1 :#line:1296
        OOO0000O0O0OO00OO =O0OOOO0O00OOO000O [O0O0O0OOOO0O0OO00 ].astype (float ).values #line:1297
        OOOOOO00OO0000O0O =OOO0000O0O0OO00OO .mean ()#line:1298
        O00OOO00O0OO0O0O0 =OOO0000O0O0OO00OO .std ()#line:1299
        O00OO00OOOOOOO0OO =OOOOOO00OO0000O0O +3 *O00OOO00O0OO0O0O0 #line:1300
        OOO0OOOO00O00OOOO =O00OOO00O0OO0O0O0 -3 *O00OOO00O0OO0O0O0 #line:1301
        OO0000000OOO00O00 .axhline (OOOOOO00OO0000O0O ,color ='r',linestyle ='--',label ='Mean')#line:1303
        OO0000000OOO00O00 .axhline (O00OO00OOOOOOO0OO ,color ='g',linestyle ='--',label ='UCL(μ+3σ)')#line:1304
        OO0000000OOO00O00 .axhline (OOO0OOOO00O00OOOO ,color ='g',linestyle ='--',label ='LCL(μ-3σ)')#line:1305
    OO0000000OOO00O00 .set_title ("控制图")#line:1307
    OO0000000OOO00O00 .set_xlabel ("项")#line:1308
    O0O00O00000O0OO00 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1309
    O00OOO0OOOO000000 =OO0000000OOO00O00 .get_position ()#line:1310
    OO0000000OOO00O00 .set_position ([O00OOO0OOOO000000 .x0 ,O00OOO0OOOO000000 .y0 ,O00OOO0OOOO000000 .width *0.7 ,O00OOO0OOOO000000 .height ])#line:1311
    OO0000000OOO00O00 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1312
    OOOO0O00000O0OOO0 =StringVar ()#line:1315
    OO0O000O00O0O0O0O =ttk .Combobox (O0O00OOOO0O0O0OO0 ,width =15 ,textvariable =OOOO0O00000O0OOO0 ,state ='readonly')#line:1316
    OO0O000O00O0O0O0O ['values']=O0O0O0OOOO0O0OO00 #line:1317
    OO0O000O00O0O0O0O .pack (side =LEFT )#line:1318
    OO0O000O00O0O0O0O .current (0 )#line:1319
    O00O0OO0O0OOO0O0O =Button (O0O00OOOO0O0O0OO0 ,text ="控制图（单项）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0OOOO0O00OOO000O ,OOOO0000000OO0OO0 ,[O00O0OO0OO00000OO for O00O0OO0OO00000OO in O0O0O0OOOO0O0OO00 if OOOO0O00000O0OOO0 .get ()in O00O0OO0OO00000OO ],OO000O000OO0OOOO0 ,O0OOO000O0O00OOO0 ))#line:1329
    O00O0OO0O0OOO0O0O .pack (side =LEFT ,anchor ="ne")#line:1330
    O00OO0OOO00O0O00O =Button (O0O00OOOO0O0O0OO0 ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O0OOOO0O00OOO000O ,OOOO0000000OO0OO0 ,O0O0O0OOOO0O0OO00 ,OO000O000OO0OOOO0 ,0 ))#line:1338
    O00OO0OOO00O0O00O .pack (side =LEFT ,anchor ="ne")#line:1340
    O000O0O0O00O0OOOO .draw ()#line:1341
def Tread_TOOLS_draw (OO0OOO00000O000OO ,O0OO000O0OOOO0OOO ,O00OOOOOOO0OOO0O0 ,OO0000O00O0000O0O ,O0O0O000000OOO0O0 ):#line:1343
    ""#line:1344
    warnings .filterwarnings ("ignore")#line:1345
    O00OOOOOO000OO0OO =Toplevel ()#line:1346
    O00OOOOOO000OO0OO .title (O0OO000O0OOOO0OOO )#line:1347
    O00OOOO00OO000OOO =ttk .Frame (O00OOOOOO000OO0OO ,height =20 )#line:1348
    O00OOOO00OO000OOO .pack (side =TOP )#line:1349
    O00OOO00OOO00OOOO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1351
    O0O0OOOOOO00000O0 =FigureCanvasTkAgg (O00OOO00OOO00OOOO ,master =O00OOOOOO000OO0OO )#line:1352
    O0O0OOOOOO00000O0 .draw ()#line:1353
    O0O0OOOOOO00000O0 .get_tk_widget ().pack (expand =1 )#line:1354
    O000OOOO0OO00O000 =O00OOO00OOO00OOOO .add_subplot (111 )#line:1355
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1357
    plt .rcParams ['axes.unicode_minus']=False #line:1358
    O0O000OOO0O00000O =NavigationToolbar2Tk (O0O0OOOOOO00000O0 ,O00OOOOOO000OO0OO )#line:1360
    O0O000OOO0O00000O .update ()#line:1361
    O0O0OOOOOO00000O0 .get_tk_widget ().pack ()#line:1363
    try :#line:1366
        OO0OO0O0OO00OOO0O =OO0OOO00000O000OO .columns #line:1367
        OO0OOO00000O000OO =OO0OOO00000O000OO .sort_values (by =OO0000O00O0000O0O ,ascending =[False ],na_position ="last")#line:1368
    except :#line:1369
        OOO0OO00O0O0O0O00 =eval (OO0OOO00000O000OO )#line:1370
        OOO0OO00O0O0O0O00 =pd .DataFrame .from_dict (OOO0OO00O0O0O0O00 ,TT_orient =O00OOOOOOO0OOO0O0 ,columns =[OO0000O00O0000O0O ]).reset_index ()#line:1373
        OO0OOO00000O000OO =OOO0OO00O0O0O0O00 .sort_values (by =OO0000O00O0000O0O ,ascending =[False ],na_position ="last")#line:1374
    if ("日期"in O0OO000O0OOOO0OOO or "时间"in O0OO000O0OOOO0OOO or "季度"in O0OO000O0OOOO0OOO )and "饼图"not in O0O0O000000OOO0O0 :#line:1378
        OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ]=pd .to_datetime (OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],format ="%Y/%m/%d").dt .date #line:1379
        OO0OOO00000O000OO =OO0OOO00000O000OO .sort_values (by =O00OOOOOOO0OOO0O0 ,ascending =[True ],na_position ="last")#line:1380
    elif "批号"in O0OO000O0OOOO0OOO :#line:1381
        OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ]=OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ].astype (str )#line:1382
        OO0OOO00000O000OO =OO0OOO00000O000OO .sort_values (by =O00OOOOOOO0OOO0O0 ,ascending =[True ],na_position ="last")#line:1383
        O000OOOO0OO00O000 .set_xticklabels (OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],rotation =-90 ,fontsize =8 )#line:1384
    else :#line:1385
        OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ]=OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ].astype (str )#line:1386
        O000OOOO0OO00O000 .set_xticklabels (OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],rotation =-90 ,fontsize =8 )#line:1387
    O0OO0O00O0OOO0000 =OO0OOO00000O000OO [OO0000O00O0000O0O ]#line:1389
    O0000O0OO0OOO0OOO =range (0 ,len (O0OO0O00O0OOO0000 ),1 )#line:1390
    O000OOOO0OO00O000 .set_title (O0OO000O0OOOO0OOO )#line:1392
    if O0O0O000000OOO0O0 =="柱状图":#line:1396
        O000OOOO0OO00O000 .bar (x =OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],height =O0OO0O00O0OOO0000 ,width =0.2 ,color ="#87CEFA")#line:1397
    elif O0O0O000000OOO0O0 =="饼图":#line:1398
        O000OOOO0OO00O000 .pie (x =O0OO0O00O0OOO0000 ,labels =OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],autopct ="%0.2f%%")#line:1399
    elif O0O0O000000OOO0O0 =="折线图":#line:1400
        O000OOOO0OO00O000 .plot (OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],O0OO0O00O0OOO0000 ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:1401
    elif "帕累托图"in str (O0O0O000000OOO0O0 ):#line:1403
        OO0OO00OOO0OO000O =OO0OOO00000O000OO [OO0000O00O0000O0O ].fillna (0 )#line:1404
        O000OO0O00O0000O0 =OO0OO00OOO0OO000O .cumsum ()/OO0OO00OOO0OO000O .sum ()*100 #line:1408
        OO0OOO00000O000OO ["百分比"]=round (OO0OOO00000O000OO ["数量"]/OO0OO00OOO0OO000O .sum ()*100 ,2 )#line:1409
        OO0OOO00000O000OO ["累计百分比"]=round (O000OO0O00O0000O0 ,2 )#line:1410
        OO0O00OOO000OO000 =O000OO0O00O0000O0 [O000OO0O00O0000O0 >0.8 ].index [0 ]#line:1411
        O000O0OO00O0OO0O0 =OO0OO00OOO0OO000O .index .tolist ().index (OO0O00OOO000OO000 )#line:1412
        O000OOOO0OO00O000 .bar (x =OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],height =OO0OO00OOO0OO000O ,color ="C0",label =OO0000O00O0000O0O )#line:1416
        O00OOO0OO0O0O0OO0 =O000OOOO0OO00O000 .twinx ()#line:1417
        O00OOO0OO0O0O0OO0 .plot (OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],O000OO0O00O0000O0 ,color ="C1",alpha =0.6 ,label ="累计比例")#line:1418
        O00OOO0OO0O0O0OO0 .yaxis .set_major_formatter (PercentFormatter ())#line:1419
        O000OOOO0OO00O000 .tick_params (axis ="y",colors ="C0")#line:1424
        O00OOO0OO0O0O0OO0 .tick_params (axis ="y",colors ="C1")#line:1425
        for OOO00OOOO0OO00OO0 ,OOO00O00OOO0O00OO ,O0O0O000OO00OO00O ,OO0O000O0O0OOOOOO in zip (OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],OO0OO00OOO0OO000O ,OO0OOO00000O000OO ["百分比"],OO0OOO00000O000OO ["累计百分比"]):#line:1427
            O000OOOO0OO00O000 .text (OOO00OOOO0OO00OO0 ,OOO00O00OOO0O00OO +0.1 ,str (int (OOO00O00OOO0O00OO ))+", "+str (int (O0O0O000OO00OO00O ))+"%,"+str (int (OO0O000O0O0OOOOOO ))+"%",color ='black',size =8 )#line:1428
        if "超级帕累托图"in str (O0O0O000000OOO0O0 ):#line:1431
            O0OOOO0OOO0000OO0 =re .compile (r'[(](.*?)[)]',re .S )#line:1432
            OO0OO0O0OO0O0O0O0 =re .findall (O0OOOO0OOO0000OO0 ,O0O0O000000OOO0O0 )[0 ]#line:1433
            O000OOOO0OO00O000 .bar (x =OO0OOO00000O000OO [O00OOOOOOO0OOO0O0 ],height =OO0OOO00000O000OO [OO0OO0O0OO0O0O0O0 ],color ="orangered",label =OO0OO0O0OO0O0O0O0 )#line:1434
    O00OOO00OOO00OOOO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1439
    OO0OO0OOO0000OO00 =O000OOOO0OO00O000 .get_position ()#line:1440
    O000OOOO0OO00O000 .set_position ([OO0OO0OOO0000OO00 .x0 ,OO0OO0OOO0000OO00 .y0 ,OO0OO0OOO0000OO00 .width *0.7 ,OO0OO0OOO0000OO00 .height ])#line:1441
    O000OOOO0OO00O000 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1442
    O0O0OOOOOO00000O0 .draw ()#line:1445
    if len (O0OO0O00O0OOO0000 )<=20 and O0O0O000000OOO0O0 !="饼图"and O0O0O000000OOO0O0 !="帕累托图":#line:1448
        for OO0O00OO0OO00O000 ,OO000O00OO00OOOOO in zip (O0000O0OO0OOO0OOO ,O0OO0O00O0OOO0000 ):#line:1449
            OO00O0O00OO000000 =str (OO000O00OO00OOOOO )#line:1450
            O0OO0O0O00OO0O0OO =(OO0O00OO0OO00O000 ,OO000O00OO00OOOOO +0.3 )#line:1451
            O000OOOO0OO00O000 .annotate (OO00O0O00OO000000 ,xy =O0OO0O0O00OO0O0OO ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:1452
    OO0OOOOO0OO0OO0OO =Button (O00OOOO00OO000OOO ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OO0OOO00000O000OO ),)#line:1462
    OO0OOOOO0OO0OO0OO .pack (side =RIGHT )#line:1463
    OOO0OOO000OO0O00O =Button (O00OOOO00OO000OOO ,relief =GROOVE ,text ="查看原始数据",command =lambda :Tread_TOOLS_view_dict (OO0OOO00000O000OO ,1 ))#line:1467
    OOO0OOO000OO0O00O .pack (side =RIGHT )#line:1468
    O00OOO00O0O000O0O =Button (O00OOOO00OO000OOO ,relief =GROOVE ,text ="饼图",command =lambda :Tread_TOOLS_draw (OO0OOO00000O000OO ,O0OO000O0OOOO0OOO ,O00OOOOOOO0OOO0O0 ,OO0000O00O0000O0O ,"饼图"),)#line:1476
    O00OOO00O0O000O0O .pack (side =LEFT )#line:1477
    O00OOO00O0O000O0O =Button (O00OOOO00OO000OOO ,relief =GROOVE ,text ="柱状图",command =lambda :Tread_TOOLS_draw (OO0OOO00000O000OO ,O0OO000O0OOOO0OOO ,O00OOOOOOO0OOO0O0 ,OO0000O00O0000O0O ,"柱状图"),)#line:1484
    O00OOO00O0O000O0O .pack (side =LEFT )#line:1485
    O00OOO00O0O000O0O =Button (O00OOOO00OO000OOO ,relief =GROOVE ,text ="折线图",command =lambda :Tread_TOOLS_draw (OO0OOO00000O000OO ,O0OO000O0OOOO0OOO ,O00OOOOOOO0OOO0O0 ,OO0000O00O0000O0O ,"折线图"),)#line:1491
    O00OOO00O0O000O0O .pack (side =LEFT )#line:1492
    O00OOO00O0O000O0O =Button (O00OOOO00OO000OOO ,relief =GROOVE ,text ="帕累托图",command =lambda :Tread_TOOLS_draw (OO0OOO00000O000OO ,O0OO000O0OOOO0OOO ,O00OOOOOOO0OOO0O0 ,OO0000O00O0000O0O ,"帕累托图"),)#line:1499
    O00OOO00O0O000O0O .pack (side =LEFT )#line:1500
def helper ():#line:1506
    ""#line:1507
    O000OOOOOOOOO0O0O =Toplevel ()#line:1508
    O000OOOOOOOOO0O0O .title ("程序使用帮助")#line:1509
    O000OOOOOOOOO0O0O .geometry ("700x500")#line:1510
    OO00OO00O0OO0OO00 =Scrollbar (O000OOOOOOOOO0O0O )#line:1512
    O00OO0OOOOOO0O0OO =Text (O000OOOOOOOOO0O0O ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1513
    OO00OO00O0OO0OO00 .pack (side =RIGHT ,fill =Y )#line:1514
    O00OO0OOOOOO0O0OO .pack ()#line:1515
    OO00OO00O0OO0OO00 .config (command =O00OO0OOOOOO0O0OO .yview )#line:1516
    O00OO0OOOOOO0O0OO .config (yscrollcommand =OO00OO00O0OO0OO00 .set )#line:1517
    O00OO0OOOOOO0O0OO .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1522
    O00OO0OOOOOO0O0OO .config (state =DISABLED )#line:1523
def Tread_TOOLS_CLEAN (OO0O0O0OOOOOOO00O ):#line:1527
        ""#line:1528
        OO0O0O0OOOOOOO00O ["报告编码"]=OO0O0O0OOOOOOO00O ["报告编码"].astype ("str")#line:1530
        OO0O0O0OOOOOOO00O ["产品批号"]=OO0O0O0OOOOOOO00O ["产品批号"].astype ("str")#line:1532
        OO0O0O0OOOOOOO00O ["型号"]=OO0O0O0OOOOOOO00O ["型号"].astype ("str")#line:1533
        OO0O0O0OOOOOOO00O ["规格"]=OO0O0O0OOOOOOO00O ["规格"].astype ("str")#line:1534
        OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"]=OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1536
        OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"]=OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1537
        OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"]=OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1538
        OO0O0O0OOOOOOO00O ["产品名称"]=OO0O0O0OOOOOOO00O ["产品名称"].str .replace ("*","※",regex =False )#line:1540
        OO0O0O0OOOOOOO00O ["产品批号"]=OO0O0O0OOOOOOO00O ["产品批号"].str .replace ("(","（",regex =False )#line:1542
        OO0O0O0OOOOOOO00O ["产品批号"]=OO0O0O0OOOOOOO00O ["产品批号"].str .replace (")","）",regex =False )#line:1543
        OO0O0O0OOOOOOO00O ["产品批号"]=OO0O0O0OOOOOOO00O ["产品批号"].str .replace ("*","※",regex =False )#line:1544
        OO0O0O0OOOOOOO00O ['事件发生日期']=pd .to_datetime (OO0O0O0OOOOOOO00O ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1547
        OO0O0O0OOOOOOO00O ["事件发生月份"]=OO0O0O0OOOOOOO00O ["事件发生日期"].dt .to_period ("M").astype (str )#line:1551
        OO0O0O0OOOOOOO00O ["事件发生季度"]=OO0O0O0OOOOOOO00O ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1552
        OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"]=OO0O0O0OOOOOOO00O ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1556
        OO0O0O0OOOOOOO00O ["产品批号"]=OO0O0O0OOOOOOO00O ["产品批号"].fillna ("未填写")#line:1557
        OO0O0O0OOOOOOO00O ["型号"]=OO0O0O0OOOOOOO00O ["型号"].fillna ("未填写")#line:1558
        OO0O0O0OOOOOOO00O ["规格"]=OO0O0O0OOOOOOO00O ["规格"].fillna ("未填写")#line:1559
        return OO0O0O0OOOOOOO00O #line:1561
def thread_it (OOOO0OOOOOOO0OO0O ,*O0000000O0O00OO0O ):#line:1565
    ""#line:1566
    O000O0O0000O0OOO0 =threading .Thread (target =OOOO0OOOOOOO0OO0O ,args =O0000000O0O00OO0O )#line:1568
    O000O0O0000O0OOO0 .setDaemon (True )#line:1570
    O000O0O0000O0OOO0 .start ()#line:1572
def showWelcome ():#line:1575
    ""#line:1576
    OOOOOOOO0O0O00OO0 =roox .winfo_screenwidth ()#line:1577
    O0O0OO0OO00000000 =roox .winfo_screenheight ()#line:1579
    roox .overrideredirect (True )#line:1581
    roox .attributes ("-alpha",1 )#line:1582
    O00O0O000O0O0OO00 =(OOOOOOOO0O0O00OO0 -475 )/2 #line:1583
    O00OOO0O0000OO000 =(O0O0OO0OO00000000 -200 )/2 #line:1584
    roox .geometry ("675x140+%d+%d"%(O00O0O000O0O0OO00 ,O00OOO0O0000OO000 ))#line:1586
    roox ["bg"]="royalblue"#line:1587
    OOO0OO0O000O0000O =Label (roox ,text ="医疗器械警戒趋势分析工具",fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:1590
    OOO0OO0O000O0000O .place (x =0 ,y =15 ,width =675 ,height =90 )#line:1591
    OOO0000O00O0OOOO0 =Label (roox ,text ="Trend Analysis Tools V"+str (version_now ),fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ),)#line:1598
    OOO0000O00O0OOOO0 .place (x =0 ,y =90 ,width =675 ,height =50 )#line:1599
def closeWelcome ():#line:1602
    ""#line:1603
    for OOO00OO0OOOO0OOO0 in range (2 ):#line:1604
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
