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
TT_biaozhun ={}#line:52
TT_ori =""#line:53
TT_modex =0 #line:54
TT_ori_backup =""#line:55
version_now ="1.0.2"#line:56
usergroup ="用户组=0"#line:57
setting_cfg =""#line:58
def get_directory_path (O0O0O0OOO00000000 ):#line:64
    import zipfile #line:66
    if not (os .path .isfile (os .path .join (O0O0O0OOO00000000 ,'A.txt'))):#line:69
        with zipfile .ZipFile ("def.zip",'r')as OO00O00OO00O00O0O :#line:71
            OO00O00OO00O00O0O .extractall (O0O0O0OOO00000000 )#line:72
    if O0O0O0OOO00000000 =="":#line:75
        quit ()#line:76
    return O0O0O0OOO00000000 #line:77
def convert_and_compare_dates (O0O0O0O0OOO000O0O ):#line:81
    import datetime #line:82
    OO000O00000O000OO =datetime .datetime .now ()#line:83
    try :#line:85
       O0000OO000OOOOOOO =datetime .datetime .strptime (str (int (int (O0O0O0O0OOO000O0O )/4 )),"%Y%m%d")#line:86
    except :#line:87
        print ("fail")#line:88
        return "已过期"#line:89
    if O0000OO000OOOOOOO >OO000O00000O000OO :#line:91
        return "未过期"#line:93
    else :#line:94
        return "已过期"#line:95
def read_setting_cfg ():#line:97
    if os .path .exists ('setting.cfg'):#line:99
        text .insert (END ,"已完成初始化\n")#line:100
        with open ('setting.cfg','r')as OO0OO0O00O00O00OO :#line:101
            OOO0O0OOOO0O0OO00 =eval (OO0OO0O00O00O00OO .read ())#line:102
    else :#line:103
        O0000O00O00O00000 ='setting.cfg'#line:105
        with open (O0000O00O00O00000 ,'w')as OO0OO0O00O00O00OO :#line:106
            OO0OO0O00O00O00OO .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:107
        text .insert (END ,"未初始化，正在初始化...\n")#line:108
        OOO0O0OOOO0O0OO00 =read_setting_cfg ()#line:109
    return OOO0O0OOOO0O0OO00 #line:110
def open_setting_cfg ():#line:113
    with open ("setting.cfg","r")as OOOOO00O0000OO00O :#line:115
        O00O0000OO0000000 =eval (OOOOO00O0000OO00O .read ())#line:117
    return O00O0000OO0000000 #line:118
def update_setting_cfg (OOOO0OOOO0OO000OO ,OOOOO0O000O0O0O00 ):#line:120
    with open ("setting.cfg","r")as O0O000OO00O00O000 :#line:122
        OOOOOO0OOO0OOOOOO =eval (O0O000OO00O00O000 .read ())#line:124
    if OOOOOO0OOO0OOOOOO [OOOO0OOOO0OO000OO ]==0 or OOOOOO0OOO0OOOOOO [OOOO0OOOO0OO000OO ]=="11111180000808":#line:126
        OOOOOO0OOO0OOOOOO [OOOO0OOOO0OO000OO ]=OOOOO0O000O0O0O00 #line:127
        with open ("setting.cfg","w")as O0O000OO00O00O000 :#line:129
            O0O000OO00O00O000 .write (str (OOOOOO0OOO0OOOOOO ))#line:130
def generate_random_file ():#line:133
    O00O0OOO00OOOO0OO =random .randint (200000 ,299999 )#line:135
    update_setting_cfg ("sidori",O00O0OOO00OOOO0OO )#line:137
def display_random_number ():#line:139
    O00OOO000OOOO000O =Toplevel ()#line:140
    O00OOO000OOOO000O .title ("ID")#line:141
    OOO0OO0O0000OO0O0 =O00OOO000OOOO000O .winfo_screenwidth ()#line:143
    OOOOOOO0OO0OOOOOO =O00OOO000OOOO000O .winfo_screenheight ()#line:144
    OOOO0OOO00O000000 =80 #line:146
    OOO0O0OOO0OOO000O =70 #line:147
    OO0O00000O0O0OOO0 =(OOO0OO0O0000OO0O0 -OOOO0OOO00O000000 )/2 #line:149
    O0000OO0OO00000OO =(OOOOOOO0OO0OOOOOO -OOO0O0OOO0OOO000O )/2 #line:150
    O00OOO000OOOO000O .geometry ("%dx%d+%d+%d"%(OOOO0OOO00O000000 ,OOO0O0OOO0OOO000O ,OO0O00000O0O0OOO0 ,O0000OO0OO00000OO ))#line:151
    with open ("setting.cfg","r")as O00O00O0OOO000O00 :#line:154
        OOO0OO00000O000O0 =eval (O00O00O0OOO000O00 .read ())#line:156
    OOO0OO0OO000O00O0 =int (OOO0OO00000O000O0 ["sidori"])#line:157
    O0O0O00OO00000OOO =OOO0OO0OO000O00O0 *2 +183576 #line:158
    print (O0O0O00OO00000OOO )#line:160
    OOO0O00O0OOO0OO0O =ttk .Label (O00OOO000OOOO000O ,text =f"机器码: {OOO0OO0OO000O00O0}")#line:162
    O0O00OO0000000000 =ttk .Entry (O00OOO000OOOO000O )#line:163
    OOO0O00O0OOO0OO0O .pack ()#line:166
    O0O00OO0000000000 .pack ()#line:167
    ttk .Button (O00OOO000OOOO000O ,text ="验证",command =lambda :check_input (O0O00OO0000000000 .get (),O0O0O00OO00000OOO )).pack ()#line:171
def check_input (O00O0OO0OOOOOO000 ,OO00O0O0OOO00OOOO ):#line:173
    try :#line:177
        O0O0OOO00OOO0O0OO =int (str (O00O0OO0OOOOOO000 )[0 :6 ])#line:178
        OOOOOO0000OOO00O0 =convert_and_compare_dates (str (O00O0OO0OOOOOO000 )[6 :14 ])#line:179
    except :#line:180
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:181
        return 0 #line:182
    if O0O0OOO00OOO0O0OO ==OO00O0O0OOO00OOOO and OOOOOO0000OOO00O0 =="未过期":#line:184
        update_setting_cfg ("sidfinal",O00O0OO0OOOOOO000 )#line:185
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:186
        quit ()#line:187
    else :#line:188
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:189
def update_software (OO00O000OOOO0O0O0 ):#line:193
    global version_now #line:195
    import pkg_resources #line:196
    try :#line:197
        O00O00O0O0OO0OO0O =pkg_resources .require ("treadmdr")[0 ].version #line:198
        version_now =O00O00O0O0OO0OO0O #line:199
    except :#line:200
        O00O00O0O0OO0OO0O =version_now #line:201
    OO0000O0OO00OO0OO =requests .get (f"https://pypi.org/pypi/{OO00O000OOOO0O0O0}/json").json ()["info"]["version"]#line:202
    text .insert (END ,"当前版本为："+O00O00O0O0OO0OO0O )#line:203
    if OO0000O0OO00OO0OO >O00O00O0O0OO0OO0O :#line:204
        text .insert (END ,"\n最新版本为："+OO0000O0OO00OO0OO +",正在尝试自动更新....")#line:205
        pip .main (['install',OO00O000OOOO0O0O0 ,'--upgrade'])#line:207
        text .insert (END ,"\n您可以开展工作。")#line:208
def Tread_TOOLS_fileopen (O000OOO00OOO0OOO0 ):#line:212
    ""#line:213
    global TT_ori #line:214
    global TT_ori_backup #line:215
    global TT_biaozhun #line:216
    warnings .filterwarnings ('ignore')#line:217
    if O000OOO00OOO0OOO0 ==0 :#line:219
        OOOO0OO0O00000O00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:220
        O0O0O00OO0OOO0O0O =[pd .read_excel (OOOOO000O0OO00OO0 ,header =0 ,sheet_name =0 )for OOOOO000O0OO00OO0 in OOOO0OO0O00000O00 ]#line:221
        O0OOOOO000O000000 =pd .concat (O0O0O00OO0OOO0O0O ,ignore_index =True ).drop_duplicates ()#line:222
        try :#line:223
            O0OOOOO000O000000 =O0OOOOO000O000000 .loc [:,~TT_ori .columns .str .contains ("^Unnamed")]#line:224
        except :#line:225
            pass #line:226
        TT_ori_backup =O0OOOOO000O000000 .copy ()#line:227
        TT_ori =Tread_TOOLS_CLEAN (O0OOOOO000O000000 ).copy ()#line:228
        text .insert (END ,"\n原始数据导入成功，行数："+str (len (TT_ori )))#line:230
        text .insert (END ,"\n数据校验：\n")#line:231
        text .insert (END ,TT_ori )#line:232
        text .see (END )#line:233
    if O000OOO00OOO0OOO0 ==1 :#line:235
        OOO0O0O00O00OOO0O =filedialog .askopenfilename (filetypes =[("XLS",".xls")])#line:236
        TT_biaozhun ["关键字表"]=pd .read_excel (OOO0O0O00O00OOO0O ,sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:237
        TT_biaozhun ["产品批号"]=pd .read_excel (OOO0O0O00O00OOO0O ,sheet_name ="产品批号",header =0 ,index_col =0 ,).reset_index ()#line:238
        TT_biaozhun ["事件发生月份"]=pd .read_excel (OOO0O0O00O00OOO0O ,sheet_name ="事件发生月份",header =0 ,index_col =0 ,).reset_index ()#line:239
        TT_biaozhun ["事件发生季度"]=pd .read_excel (OOO0O0O00O00OOO0O ,sheet_name ="事件发生季度",header =0 ,index_col =0 ,).reset_index ()#line:240
        TT_biaozhun ["规格"]=pd .read_excel (OOO0O0O00O00OOO0O ,sheet_name ="规格",header =0 ,index_col =0 ,).reset_index ()#line:241
        TT_biaozhun ["型号"]=pd .read_excel (OOO0O0O00O00OOO0O ,sheet_name ="型号",header =0 ,index_col =0 ,).reset_index ()#line:242
        TT_biaozhun ["设置"]=pd .read_excel (OOO0O0O00O00OOO0O ,sheet_name ="设置",header =0 ,index_col =0 ,).reset_index ()#line:243
        Tread_TOOLS_check (TT_ori ,TT_biaozhun ["关键字表"],0 )#line:244
        text .insert (END ,"\n标准导入成功，行数："+str (len (TT_biaozhun )))#line:245
        text .see (END )#line:246
def Tread_TOOLS_check (O000O0OOOOOO0O0O0 ,O000000OO0OOO0OO0 ,OOOO0O0O0OO0OOOO0 ):#line:248
        ""#line:249
        global TT_ori #line:250
        O0000O000000O000O =Tread_TOOLS_Countall (O000O0OOOOOO0O0O0 ).df_psur (O000000OO0OOO0OO0 )#line:251
        if OOOO0O0O0OO0OOOO0 ==0 :#line:253
            Tread_TOOLS_tree_Level_2 (O0000O000000O000O ,0 ,TT_ori .copy ())#line:255
        O0000O000000O000O ["核验"]=0 #line:258
        O0000O000000O000O .loc [(O0000O000000O000O ["关键字标记"].str .contains ("-其他关键字-",na =False )),"核验"]=O0000O000000O000O .loc [(O0000O000000O000O ["关键字标记"].str .contains ("-其他关键字-",na =False )),"总数量"]#line:259
        if O0000O000000O000O ["核验"].sum ()>0 :#line:260
            showinfo (title ="温馨提示",message ="存在未定义类型的报告"+str (O0000O000000O000O ["核验"].sum ())+"条，趋势分析可能会存在遗漏，建议修正该错误再进行下一步。")#line:261
def Tread_TOOLS_tree_Level_2 (O0O0O00OOO0OOOO0O ,OO0OOOOO0OO0OOO00 ,OOO00000OO00O0O00 ,*OO00OOO00O00OO000 ):#line:263
    ""#line:264
    global TT_ori_backup #line:266
    O0OOOOO0OOOO0O00O =O0O0O00OOO0OOOO0O .columns .values .tolist ()#line:268
    OO0OOOOO0OO0OOO00 =0 #line:269
    OO00OOO0O0O0O0O00 =O0O0O00OOO0OOOO0O .loc [:]#line:270
    OO00O00O000O0OOO0 =0 #line:274
    try :#line:275
        OO000OO0O0OO0O00O =OO00OOO00O00OO000 [0 ]#line:276
        OO00O00O000O0OOO0 =1 #line:277
    except :#line:278
        pass #line:279
    OO00O00000OO0O000 =Toplevel ()#line:282
    OO00O00000OO0O000 .title ("报表查看器")#line:283
    OOO000OOO0O000O00 =OO00O00000OO0O000 .winfo_screenwidth ()#line:284
    O0OOO000OOO0O0O0O =OO00O00000OO0O000 .winfo_screenheight ()#line:286
    OO000OO0OO000O000 =1300 #line:288
    O0O0O0OOOOO000O0O =600 #line:289
    O0O000OOOOOOO000O =(OOO000OOO0O000O00 -OO000OO0OO000O000 )/2 #line:291
    O0000O00O0000O00O =(O0OOO000OOO0O0O0O -O0O0O0OOOOO000O0O )/2 #line:292
    OO00O00000OO0O000 .geometry ("%dx%d+%d+%d"%(OO000OO0OO000O000 ,O0O0O0OOOOO000O0O ,O0O000OOOOOOO000O ,O0000O00O0000O00O ))#line:293
    O00O0OOO0OO00O000 =ttk .Frame (OO00O00000OO0O000 ,width =1300 ,height =20 )#line:294
    O00O0OOO0OO00O000 .pack (side =BOTTOM )#line:295
    O00O0OOOOO0O0O000 =ttk .Frame (OO00O00000OO0O000 ,width =1300 ,height =20 )#line:297
    O00O0OOOOO0O0O000 .pack (side =TOP )#line:298
    if 1 >0 :#line:302
        O0000O0O0000O00O0 =Button (O00O0OOO0OO00O000 ,text ="控制图(所有)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00OOO0O0O0O0O00 [:-1 ],OO000OO0O0OO0O00O ,[O00O0OO0OOO0OO0OO for O00O0OO0OOO0OO0OO in OO00OOO0O0O0O0O00 .columns if (O00O0OO0OOO0OO0OO not in [OO000OO0O0OO0O00O ])],"关键字趋势图",100 ),)#line:312
        if OO00O00O000O0OOO0 ==1 :#line:313
            O0000O0O0000O00O0 .pack (side =LEFT )#line:314
        O0000O0O0000O00O0 =Button (O00O0OOO0OO00O000 ,text ="控制图(总数量)",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (OO00OOO0O0O0O0O00 [:-1 ],OO000OO0O0OO0O00O ,[OOOO0OO0000OOO0O0 for OOOO0OO0000OOO0O0 in OO00OOO0O0O0O0O00 .columns if (OOOO0OO0000OOO0O0 in ["该元素总数量"])],"关键字趋势图",100 ),)#line:324
        if OO00O00O000O0OOO0 ==1 :#line:325
            O0000O0O0000O00O0 .pack (side =LEFT )#line:326
        OOOO0O000O0O0O00O =Button (O00O0OOO0OO00O000 ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (OO00OOO0O0O0O0O00 ),)#line:336
        OOOO0O000O0O0O00O .pack (side =LEFT )#line:337
        OOOO0O000O0O0O00O =Button (O00O0OOO0OO00O000 ,text ="发生率测算",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_fashenglv (OO00OOO0O0O0O0O00 ,OO000OO0O0OO0O00O ),)#line:347
        if "关键字标记"not in OO00OOO0O0O0O0O00 .columns and "报告编码"not in OO00OOO0O0O0O0O00 .columns :#line:348
            if "对象"not in OO00OOO0O0O0O0O00 .columns :#line:349
                OOOO0O000O0O0O00O .pack (side =LEFT )#line:350
        OOOO0O000O0O0O00O =Button (O00O0OOO0OO00O000 ,text ="直方图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_histbar (OO00OOO0O0O0O0O00 .copy ()),)#line:360
        if "对象"in OO00OOO0O0O0O0O00 .columns :#line:361
            OOOO0O000O0O0O00O .pack (side =LEFT )#line:362
        O000OO0O000OO0O0O =Button (O00O0OOO0OO00O000 ,text ="行数:"+str (len (OO00OOO0O0O0O0O00 )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:372
        O000OO0O000OO0O0O .pack (side =LEFT )#line:373
    O000O0000O000O0O0 =OO00OOO0O0O0O0O00 .values .tolist ()#line:376
    OOOO00O000OOOOO0O =OO00OOO0O0O0O0O00 .columns .values .tolist ()#line:377
    O00OO00O0OO000O0O =ttk .Treeview (O00O0OOOOO0O0O000 ,columns =OOOO00O000OOOOO0O ,show ="headings",height =45 )#line:378
    for OOOOOO00OO0O0OO00 in OOOO00O000OOOOO0O :#line:380
        O00OO00O0OO000O0O .heading (OOOOOO00OO0O0OO00 ,text =OOOOOO00OO0O0OO00 )#line:381
    for OO00O000OO00OOO0O in O000O0000O000O0O0 :#line:382
        O00OO00O0OO000O0O .insert ("","end",values =OO00O000OO00OOO0O )#line:383
    for O0O0O0O0000OO00O0 in OOOO00O000OOOOO0O :#line:384
        O00OO00O0OO000O0O .column (O0O0O0O0000OO00O0 ,minwidth =0 ,width =120 ,stretch =NO )#line:385
    O0OO0OOO0OOO0O00O =Scrollbar (O00O0OOOOO0O0O000 ,orient ="vertical")#line:387
    O0OO0OOO0OOO0O00O .pack (side =RIGHT ,fill =Y )#line:388
    O0OO0OOO0OOO0O00O .config (command =O00OO00O0OO000O0O .yview )#line:389
    O00OO00O0OO000O0O .config (yscrollcommand =O0OO0OOO0OOO0O00O .set )#line:390
    O0OOO0O000000OOO0 =Scrollbar (O00O0OOOOO0O0O000 ,orient ="horizontal")#line:392
    O0OOO0O000000OOO0 .pack (side =BOTTOM ,fill =X )#line:393
    O0OOO0O000000OOO0 .config (command =O00OO00O0OO000O0O .xview )#line:394
    O00OO00O0OO000O0O .config (yscrollcommand =O0OO0OOO0OOO0O00O .set )#line:395
    def O00O000OO0O0OOOO0 (OOO0OOOO0OO0OO0OO ,O0O00OO0O000OO00O ,O0O0OOO000O00O0OO ):#line:397
        for OOO00000O00O00000 in O00OO00O0OO000O0O .selection ():#line:400
            OOO0O00O0O000OOOO =O00OO00O0OO000O0O .item (OOO00000O00O00000 ,"values")#line:401
            OOOOOO0O0O00OOO0O =dict (zip (O0O00OO0O000OO00O ,OOO0O00O0O000OOOO ))#line:402
        if "该分类下各项计数"in O0O00OO0O000OO00O :#line:404
            OO00OOO0OOO0OOOOO =OOO00000OO00O0O00 .copy ()#line:405
            OO00OOO0OOO0OOOOO ["关键字查找列"]=""#line:406
            for O00OO00OOO0O0O0O0 in TOOLS_get_list (OOOOOO0O0O00OOO0O ["查找位置"]):#line:407
                OO00OOO0OOO0OOOOO ["关键字查找列"]=OO00OOO0OOO0OOOOO ["关键字查找列"]+OO00OOO0OOO0OOOOO [O00OO00OOO0O0O0O0 ].astype ("str")#line:408
            O0O00OOO0OOOOOOO0 =OO00OOO0OOO0OOOOO .loc [OO00OOO0OOO0OOOOO ["关键字查找列"].str .contains (OOOOOO0O0O00OOO0O ["关键字标记"],na =False )].copy ()#line:409
            O0O00OOO0OOOOOOO0 =O0O00OOO0OOOOOOO0 .loc [~O0O00OOO0OOOOOOO0 ["关键字查找列"].str .contains (OOOOOO0O0O00OOO0O ["排除值"],na =False )].copy ()#line:410
            Tread_TOOLS_tree_Level_2 (O0O00OOO0OOOOOOO0 ,0 ,O0O00OOO0OOOOOOO0 )#line:416
            return 0 #line:417
        if "报告编码"in O0O00OO0O000OO00O :#line:419
            OO0000O000OOO00OO =Toplevel ()#line:420
            O00O0OOOOO000OOO0 =OO0000O000OOO00OO .winfo_screenwidth ()#line:421
            OOO0OOO0O000O0OOO =OO0000O000OOO00OO .winfo_screenheight ()#line:423
            OOOO00OO0O0O0O0OO =800 #line:425
            O000O00000O0OO00O =600 #line:426
            O00OO00OOO0O0O0O0 =(O00O0OOOOO000OOO0 -OOOO00OO0O0O0O0OO )/2 #line:428
            O0000O00O0OOOO0OO =(OOO0OOO0O000O0OOO -O000O00000O0OO00O )/2 #line:429
            OO0000O000OOO00OO .geometry ("%dx%d+%d+%d"%(OOOO00OO0O0O0O0OO ,O000O00000O0OO00O ,O00OO00OOO0O0O0O0 ,O0000O00O0OOOO0OO ))#line:430
            O0OOOO0O0OO00OOOO =ScrolledText (OO0000O000OOO00OO ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:434
            O0OOOO0O0OO00OOOO .pack (padx =10 ,pady =10 )#line:435
            def O00OOO0O000O00OO0 (event =None ):#line:436
                O0OOOO0O0OO00OOOO .event_generate ('<<Copy>>')#line:437
            def O000O00000OO000OO (OO0OO00O00OO0000O ,O00000OOO0OOOOOO0 ):#line:438
                OO00O00OOOO000O00 =open (O00000OOO0OOOOOO0 ,"w",encoding ='utf-8')#line:439
                OO00O00OOOO000O00 .write (OO0OO00O00OO0000O )#line:440
                OO00O00OOOO000O00 .flush ()#line:442
                showinfo (title ="提示信息",message ="保存成功。")#line:443
            O0O0O000OOOO0O00O =Menu (O0OOOO0O0OO00OOOO ,tearoff =False ,)#line:445
            O0O0O000OOOO0O00O .add_command (label ="复制",command =O00OOO0O000O00OO0 )#line:446
            O0O0O000OOOO0O00O .add_command (label ="导出",command =lambda :thread_it (O000O00000OO000OO ,O0OOOO0O0OO00OOOO .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =OOOOOO0O0O00OOO0O ["报告编码"],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:447
            def OOOOOOO0O0O0O00O0 (O0OOO0OOO0OOO000O ):#line:449
                O0O0O000OOOO0O00O .post (O0OOO0OOO0OOO000O .x_root ,O0OOO0OOO0OOO000O .y_root )#line:450
            O0OOOO0O0OO00OOOO .bind ("<Button-3>",OOOOOOO0O0O0O00O0 )#line:451
            OO0000O000OOO00OO .title (OOOOOO0O0O00OOO0O ["报告编码"])#line:453
            for OOO0O0OOOO0O0OOOO in range (len (O0O00OO0O000OO00O )):#line:454
                O0OOOO0O0OO00OOOO .insert (END ,O0O00OO0O000OO00O [OOO0O0OOOO0O0OOOO ])#line:456
                O0OOOO0O0OO00OOOO .insert (END ,"：")#line:457
                O0OOOO0O0OO00OOOO .insert (END ,OOOOOO0O0O00OOO0O [O0O00OO0O000OO00O [OOO0O0OOOO0O0OOOO ]])#line:458
                O0OOOO0O0OO00OOOO .insert (END ,"\n")#line:459
            O0OOOO0O0OO00OOOO .config (state =DISABLED )#line:460
            return 0 #line:461
        O0000O00O0OOOO0OO =OOO0O00O0O000OOOO [1 :-1 ]#line:464
        O00OO00OOO0O0O0O0 =O0O0OOO000O00O0OO .columns .tolist ()#line:466
        O00OO00OOO0O0O0O0 =O00OO00OOO0O0O0O0 [1 :-1 ]#line:467
        OOOO0000O00OO0OO0 ={'关键词':O00OO00OOO0O0O0O0 ,'数量':O0000O00O0OOOO0OO }#line:469
        OOOO0000O00OO0OO0 =pd .DataFrame .from_dict (OOOO0000O00OO0OO0 )#line:470
        OOOO0000O00OO0OO0 ["数量"]=OOOO0000O00OO0OO0 ["数量"].astype (float )#line:471
        Tread_TOOLS_draw (OOOO0000O00OO0OO0 ,"帕累托图",'关键词','数量',"帕累托图")#line:472
        return 0 #line:473
    O00OO00O0OO000O0O .bind ("<Double-1>",lambda OOOO00OOO0OOOOO00 :O00O000OO0O0OOOO0 (OOOO00OOO0OOOOO00 ,OOOO00O000OOOOO0O ,OO00OOO0O0O0O0O00 ),)#line:481
    O00OO00O0OO000O0O .pack ()#line:482
class Tread_TOOLS_Countall ():#line:484
    ""#line:485
    def __init__ (O0O0000OOO0O0OO00 ,OOO00O00O000OOO00 ):#line:486
        ""#line:487
        O0O0000OOO0O0OO00 .df =OOO00O00O000OOO00 #line:488
    def df_psur (O0OO000OOO0OOO0OO ,OO0OO000O0O0000OO ,*O0O000O0OOO0OOOO0 ):#line:490
        ""#line:491
        global TT_biaozhun #line:492
        O00OO00OO00O0OOO0 =O0OO000OOO0OOO0OO .df .copy ()#line:493
        O00O0OOOOOOOOO0O0 =len (O00OO00OO00O0OOO0 .drop_duplicates ("报告编码"))#line:495
        OOOOO0O00OOO00000 =OO0OO000O0O0000OO .copy ()#line:498
        OO000OOO00O0OO0O0 =TT_biaozhun ["设置"]#line:501
        if OO000OOO00O0OO0O0 .loc [1 ,"值"]:#line:502
            OOOO00OOO00O000O0 =OO000OOO00O0OO0O0 .loc [1 ,"值"]#line:503
        else :#line:504
            OOOO00OOO00O000O0 ="透视列"#line:505
            O00OO00OO00O0OOO0 [OOOO00OOO00O000O0 ]="未正确设置"#line:506
        O0OOO0OOO0000O0O0 =""#line:508
        O0OOO00000000O0OO ="-其他关键字-"#line:509
        for OO00OOO00O000O0OO ,O0OOO0000O0OO00O0 in OOOOO0O00OOO00000 .iterrows ():#line:510
            O0OOO00000000O0OO =O0OOO00000000O0OO +"|"+str (O0OOO0000O0OO00O0 ["值"])#line:511
            O0OOOO0OO0OO00O00 =O0OOO0000O0OO00O0 #line:512
        O0OOOO0OO0OO00O00 [3 ]=O0OOO00000000O0OO #line:513
        O0OOOO0OO0OO00O00 [2 ]="-其他关键字-|"#line:514
        OOOOO0O00OOO00000 .loc [len (OOOOO0O00OOO00000 )]=O0OOOO0OO0OO00O00 #line:515
        OOOOO0O00OOO00000 =OOOOO0O00OOO00000 .reset_index (drop =True )#line:516
        O00OO00OO00O0OOO0 ["关键字查找列"]=""#line:520
        for OOOO0OOO000OOOOOO in TOOLS_get_list (OOOOO0O00OOO00000 .loc [0 ,"查找位置"]):#line:521
            O00OO00OO00O0OOO0 ["关键字查找列"]=O00OO00OO00O0OOO0 ["关键字查找列"]+O00OO00OO00O0OOO0 [OOOO0OOO000OOOOOO ].astype ("str")#line:522
        O00OO0OOO00OO0000 =[]#line:525
        for OO00OOO00O000O0OO ,O0OOO0000O0OO00O0 in OOOOO0O00OOO00000 .iterrows ():#line:526
            O0O000OOO000O0OOO =O0OOO0000O0OO00O0 ["值"]#line:527
            O000OO000O00OO0O0 =O00OO00OO00O0OOO0 .loc [O00OO00OO00O0OOO0 ["关键字查找列"].str .contains (O0O000OOO000O0OOO ,na =False )].copy ()#line:528
            if str (O0OOO0000O0OO00O0 ["排除值"])!="nan":#line:529
                O000OO000O00OO0O0 =O000OO000O00OO0O0 .loc [~O000OO000O00OO0O0 ["关键字查找列"].str .contains (str (O0OOO0000O0OO00O0 ["排除值"]),na =False )].copy ()#line:530
            O000OO000O00OO0O0 ["关键字标记"]=str (O0O000OOO000O0OOO )#line:532
            O000OO000O00OO0O0 ["关键字计数"]=1 #line:533
            if len (O000OO000O00OO0O0 )>0 :#line:535
                OO0OOOO000O0OO000 =pd .pivot_table (O000OO000O00OO0O0 .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns =OOOO00OOO00O000O0 ,aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:545
                OO0OOOO000O0OO000 =OO0OOOO000O0OO000 [:-1 ]#line:546
                OO0OOOO000O0OO000 .columns =OO0OOOO000O0OO000 .columns .droplevel (0 )#line:547
                OO0OOOO000O0OO000 =OO0OOOO000O0OO000 .reset_index ()#line:548
                if len (OO0OOOO000O0OO000 )>0 :#line:551
                    O000O00OOOOO0O0OO =str (Counter (TOOLS_get_list0 ("use(关键字查找列).file",O000OO000O00OO0O0 ,1000 ))).replace ("Counter({","{")#line:552
                    O000O00OOOOO0O0OO =O000O00OOOOO0O0OO .replace ("})","}")#line:553
                    O000O00OOOOO0O0OO =ast .literal_eval (O000O00OOOOO0O0OO )#line:554
                    OO0OOOO000O0OO000 .loc [0 ,"事件分类"]=str (TOOLS_get_list (OO0OOOO000O0OO000 .loc [0 ,"关键字标记"])[0 ])#line:556
                    OO0OOOO000O0OO000 .loc [0 ,"该分类下各项计数"]=str ({O000O00O000OOO0OO :O0000O0OO0O000O0O for O000O00O000OOO0OO ,O0000O0OO0O000O0O in O000O00OOOOO0O0OO .items ()if STAT_judge_x (str (O000O00O000OOO0OO ),TOOLS_get_list (O0O000OOO000O0OOO ))==1 })#line:557
                    OO0OOOO000O0OO000 .loc [0 ,"其他分类各项计数"]=str ({O0OO0O00O00OO00OO :OOO000O0OO0OO0OO0 for O0OO0O00O00OO00OO ,OOO000O0OO0OO0OO0 in O000O00OOOOO0O0OO .items ()if STAT_judge_x (str (O0OO0O00O00OO00OO ),TOOLS_get_list (O0O000OOO000O0OOO ))!=1 })#line:558
                    OO0OOOO000O0OO000 ["查找位置"]=O0OOO0000O0OO00O0 ["查找位置"]#line:559
                    O00OO0OOO00OO0000 .append (OO0OOOO000O0OO000 )#line:562
        O0OOO0OOO0000O0O0 =pd .concat (O00OO0OOO00OO0000 )#line:563
        O0OOO0OOO0000O0O0 =O0OOO0OOO0000O0O0 .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:568
        O0OOO0OOO0000O0O0 =O0OOO0OOO0000O0O0 .reset_index ()#line:569
        O0OOO0OOO0000O0O0 ["All占比"]=round (O0OOO0OOO0000O0O0 ["All"]/O00O0OOOOOOOOO0O0 *100 ,2 )#line:571
        O0OOO0OOO0000O0O0 =O0OOO0OOO0000O0O0 .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:572
        for O0O0000OOOO0OO0O0 ,OOOO0O00OO00OO0O0 in OOOOO0O00OOO00000 .iterrows ():#line:575
            O0OOO0OOO0000O0O0 .loc [(O0OOO0OOO0000O0O0 ["关键字标记"].astype (str )==str (OOOO0O00OO00OO0O0 ["值"])),"排除值"]=OOOO0O00OO00OO0O0 ["排除值"]#line:576
            O0OOO0OOO0000O0O0 .loc [(O0OOO0OOO0000O0O0 ["关键字标记"].astype (str )==str (OOOO0O00OO00OO0O0 ["值"])),"查找位置"]=OOOO0O00OO00OO0O0 ["查找位置"]#line:577
        O0OOO0OOO0000O0O0 ["排除值"]=O0OOO0OOO0000O0O0 ["排除值"].fillna ("-没有排除值-")#line:579
        O0OOO0OOO0000O0O0 ["报表类型"]="PSUR"#line:582
        del O0OOO0OOO0000O0O0 ["index"]#line:583
        try :#line:584
            del O0OOO0OOO0000O0O0 ["未正确设置"]#line:585
        except :#line:586
            pass #line:587
        return O0OOO0OOO0000O0O0 #line:588
    def df_find_all_keword_risk (OOOO000OO0OOOO000 ,O00OOO0OO00O0O0OO ,*OOO000000OOOO00OO ):#line:591
        ""#line:592
        global TT_biaozhun #line:593
        O000O00OO0OO0000O =OOOO000OO0OOOO000 .df .copy ()#line:595
        OOOOO000OOO0OO000 =time .time ()#line:596
        O0O0O0O0OOO000OO0 =TT_biaozhun ["关键字表"].copy ()#line:598
        OOOO0O000OO0O0OO0 ="作用对象"#line:600
        O0O0O0OOO00O00OO0 ="报告编码"#line:602
        OOO00000OOOO0OOO0 =O000O00OO0OO0000O .groupby ([OOOO0O000OO0O0OO0 ]).agg (总数量 =(O0O0O0OOO00O00OO0 ,"nunique"),).reset_index ()#line:605
        OOOOOOOO00O0OO000 =[OOOO0O000OO0O0OO0 ,O00OOO0OO00O0O0OO ]#line:607
        O00O00OOO0000OOOO =O000O00OO0OO0000O .groupby (OOOOOOOO00O0OO000 ).agg (该元素总数量 =(OOOO0O000OO0O0OO0 ,"count"),).reset_index ()#line:611
        OOO000OOO0OOO0O00 =[]#line:613
        O0OO0OOO0O0O0OO0O =0 #line:617
        O0O000000O0OOOO00 =int (len (OOO00000OOOO0OOO0 ))#line:618
        for O0O0O0O0O0O00O0O0 ,O00O00OO0O0OOO0O0 in zip (OOO00000OOOO0OOO0 [OOOO0O000OO0O0OO0 ].values ,OOO00000OOOO0OOO0 ["总数量"].values ):#line:619
            O0OO0OOO0O0O0OO0O +=1 #line:620
            O00OOO000O0OOO0OO =O000O00OO0OO0000O [(O000O00OO0OO0000O [OOOO0O000OO0O0OO0 ]==O0O0O0O0O0O00O0O0 )].copy ()#line:621
            for O0OOO00OO0O0O00OO ,O00OO0OOO0OOO0000 ,O0O0OOO00O0OO00O0 in zip (O0O0O0O0OOO000OO0 ["值"].values ,O0O0O0O0OOO000OO0 ["查找位置"].values ,O0O0O0O0OOO000OO0 ["排除值"].values ):#line:623
                    O0O0OOO00OO0OOOOO =O00OOO000O0OOO0OO .copy ()#line:624
                    O00O0OOOO000OO0O0 =TOOLS_get_list (O0OOO00OO0O0O00OO )[0 ]#line:625
                    O0O0OOO00OO0OOOOO ["关键字查找列"]=""#line:627
                    for OOOO00OOOOO0OOO0O in TOOLS_get_list (O00OO0OOO0OOO0000 ):#line:628
                        O0O0OOO00OO0OOOOO ["关键字查找列"]=O0O0OOO00OO0OOOOO ["关键字查找列"]+O0O0OOO00OO0OOOOO [OOOO00OOOOO0OOO0O ].astype ("str")#line:629
                    O0O0OOO00OO0OOOOO .loc [O0O0OOO00OO0OOOOO ["关键字查找列"].str .contains (O0OOO00OO0O0O00OO ,na =False ),"关键字"]=O00O0OOOO000OO0O0 #line:631
                    if str (O0O0OOO00O0OO00O0 )!="nan":#line:636
                        O0O0OOO00OO0OOOOO =O0O0OOO00OO0OOOOO .loc [~O0O0OOO00OO0OOOOO ["关键字查找列"].str .contains (O0O0OOO00O0OO00O0 ,na =False )].copy ()#line:637
                    if (len (O0O0OOO00OO0OOOOO ))<1 :#line:639
                        continue #line:641
                    O00000O00O00OOOO0 =STAT_find_keyword_risk (O0O0OOO00OO0OOOOO ,[OOOO0O000OO0O0OO0 ,"关键字"],"关键字",O00OOO0OO00O0O0OO ,int (O00O00OO0O0OOO0O0 ))#line:643
                    if len (O00000O00O00OOOO0 )>0 :#line:644
                        O00000O00O00OOOO0 ["关键字组合"]=O0OOO00OO0O0O00OO #line:645
                        O00000O00O00OOOO0 ["排除值"]=O0O0OOO00O0OO00O0 #line:646
                        O00000O00O00OOOO0 ["关键字查找列"]=O00OO0OOO0OOO0000 #line:647
                        OOO000OOO0OOO0O00 .append (O00000O00O00OOOO0 )#line:648
        if len (OOO000OOO0OOO0O00 )<1 :#line:651
            showinfo (title ="错误信息",message ="该注册证号未检索到任何关键字，规则制定存在缺陷。")#line:652
            return 0 #line:653
        OOO00000O0000OOOO =pd .concat (OOO000OOO0OOO0O00 )#line:654
        OOO00000O0000OOOO =pd .merge (OOO00000O0000OOOO ,O00O00OOO0000OOOO ,on =OOOOOOOO00O0OO000 ,how ="left")#line:657
        OOO00000O0000OOOO ["关键字数量比例"]=round (OOO00000O0000OOOO ["计数"]/OOO00000O0000OOOO ["该元素总数量"],2 )#line:658
        OOO00000O0000OOOO =OOO00000O0000OOOO .reset_index (drop =True )#line:660
        if len (OOO00000O0000OOOO )>0 :#line:663
            OOO00000O0000OOOO ["风险评分"]=0 #line:664
            OOO00000O0000OOOO ["报表类型"]="keyword_findrisk"+O00OOO0OO00O0O0OO #line:665
            OOO00000O0000OOOO .loc [(OOO00000O0000OOOO ["计数"]>=3 ),"风险评分"]=OOO00000O0000OOOO ["风险评分"]+3 #line:666
            OOO00000O0000OOOO .loc [(OOO00000O0000OOOO ["计数"]>=(OOO00000O0000OOOO ["数量均值"]+OOO00000O0000OOOO ["数量标准差"])),"风险评分"]=OOO00000O0000OOOO ["风险评分"]+1 #line:667
            OOO00000O0000OOOO .loc [(OOO00000O0000OOOO ["计数"]>=OOO00000O0000OOOO ["数量CI"]),"风险评分"]=OOO00000O0000OOOO ["风险评分"]+1 #line:668
            OOO00000O0000OOOO .loc [(OOO00000O0000OOOO ["关键字数量比例"]>0.5 )&(OOO00000O0000OOOO ["计数"]>=3 ),"风险评分"]=OOO00000O0000OOOO ["风险评分"]+1 #line:669
            OOO00000O0000OOOO =OOO00000O0000OOOO .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:671
        O00O0O0OOOO00O0O0 =OOO00000O0000OOOO .columns .to_list ()#line:681
        O00O0OOOO000OOOO0 =O00O0O0OOOO00O0O0 [O00O0O0OOOO00O0O0 .index ("关键字")+1 ]#line:682
        OOO0000OO0O0000O0 =pd .pivot_table (OOO00000O0000OOOO ,index =O00O0OOOO000OOOO0 ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:693
        OOO0000OO0O0000O0 .columns =OOO0000OO0O0000O0 .columns .droplevel (0 )#line:694
        OOO0000OO0O0000O0 =pd .merge (OOO0000OO0O0000O0 ,OOO00000O0000OOOO [[O00O0OOOO000OOOO0 ,"该元素总数量"]].drop_duplicates (O00O0OOOO000OOOO0 ),on =[O00O0OOOO000OOOO0 ],how ="left")#line:697
        del OOO0000OO0O0000O0 ["All"]#line:699
        OOO0000OO0O0000O0 .iloc [-1 ,-1 ]=OOO0000OO0O0000O0 ["该元素总数量"].sum (axis =0 )#line:700
        print ("耗时：",(time .time ()-OOOOO000OOO0OO000 ))#line:702
        return OOO0000OO0O0000O0 #line:705
def Tread_TOOLS_bar (OO0O000O0O000OOO0 ):#line:713
         ""#line:714
         OOO000000O000OO00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:715
         O0O0OOO00OO0O0OO0 =[pd .read_excel (OOOOOO0OO0O0O0000 ,header =0 ,sheet_name =0 )for OOOOOO0OO0O0O0000 in OOO000000O000OO00 ]#line:716
         O0000O0OO00O00O00 =pd .concat (O0O0OOO00OO0O0OO0 ,ignore_index =True )#line:717
         O000O000O0O000000 =pd .pivot_table (O0000O0OO00O00O00 ,index ="对象",columns ="关键词",values =OO0O000O0O000OOO0 ,aggfunc ="sum",fill_value ="0",margins =True ,dropna =False ,).reset_index ()#line:727
         del O000O000O0O000000 ["All"]#line:729
         O000O000O0O000000 =O000O000O0O000000 [:-1 ]#line:730
         Tread_TOOLS_tree_Level_2 (O000O000O0O000000 ,0 ,0 )#line:732
def Tread_TOOLS_analysis (OO000OO00OO0O0O00 ):#line:737
    ""#line:738
    import datetime #line:739
    global TT_ori #line:740
    global TT_biaozhun #line:741
    if len (TT_ori )==0 :#line:743
       showinfo (title ="提示",message ="您尚未导入原始数据。")#line:744
       return 0 #line:745
    if len (TT_biaozhun )==0 :#line:746
       showinfo (title ="提示",message ="您尚未导入规则。")#line:747
       return 0 #line:748
    OOO0OO0O0OO000OO0 =TT_biaozhun ["设置"]#line:750
    TT_ori ["作用对象"]=""#line:751
    for OO00000O00O0000O0 in TOOLS_get_list (OOO0OO0O0OO000OO0 .loc [0 ,"值"]):#line:752
        TT_ori ["作用对象"]=TT_ori ["作用对象"]+"-"+TT_ori [OO00000O00O0000O0 ].fillna ("未填写").astype ("str")#line:753
    O00OO00OOO0000O00 =Toplevel ()#line:756
    O00OO00OOO0000O00 .title ("单品分析")#line:757
    O00OO0O0000OO000O =O00OO00OOO0000O00 .winfo_screenwidth ()#line:758
    O0O00000OOOO0OO00 =O00OO00OOO0000O00 .winfo_screenheight ()#line:760
    OOO00O00O00O000OO =580 #line:762
    OOO0OOOOO0OO0O0O0 =80 #line:763
    OO0O0000OOO0OOO0O =(O00OO0O0000OO000O -OOO00O00O00O000OO )/1.7 #line:765
    OOO0O00OOO000O0O0 =(O0O00000OOOO0OO00 -OOO0OOOOO0OO0O0O0 )/2 #line:766
    O00OO00OOO0000O00 .geometry ("%dx%d+%d+%d"%(OOO00O00O00O000OO ,OOO0OOOOO0OO0O0O0 ,OO0O0000OOO0OOO0O ,OOO0O00OOO000O0O0 ))#line:767
    OOO00O0O000OOO000 =Label (O00OO00OOO0000O00 ,text ="作用对象：")#line:770
    OOO00O0O000OOO000 .grid (row =1 ,column =0 ,sticky ="w")#line:771
    O000OOO00O000O0O0 =StringVar ()#line:772
    O000OO00O000O00O0 =ttk .Combobox (O00OO00OOO0000O00 ,width =25 ,height =10 ,state ="readonly",textvariable =O000OOO00O000O0O0 )#line:775
    O000OO00O000O00O0 ["values"]=list (set (TT_ori ["作用对象"].to_list ()))#line:776
    O000OO00O000O00O0 .current (0 )#line:777
    O000OO00O000O00O0 .grid (row =1 ,column =1 )#line:778
    O00O0OOOOOOOO000O =Label (O00OO00OOO0000O00 ,text ="分析对象：")#line:780
    O00O0OOOOOOOO000O .grid (row =1 ,column =2 ,sticky ="w")#line:781
    OO0O00OOO0OO0OOO0 =StringVar ()#line:784
    OO00OOOOOO0OOO0OO =ttk .Combobox (O00OO00OOO0000O00 ,width =15 ,height =10 ,state ="readonly",textvariable =OO0O00OOO0OO0OOO0 )#line:787
    OO00OOOOOO0OOO0OO ["values"]=["事件发生月份","事件发生季度","产品批号","型号","规格"]#line:788
    OO00OOOOOO0OOO0OO .current (0 )#line:790
    OO00OOOOOO0OOO0OO .grid (row =1 ,column =3 )#line:791
    O0OO00O0O0OOO0OO0 =Label (O00OO00OOO0000O00 ,text ="事件发生起止时间：")#line:796
    O0OO00O0O0OOO0OO0 .grid (row =2 ,column =0 ,sticky ="w")#line:797
    OO0O0O00O0O0OOO0O =Entry (O00OO00OOO0000O00 ,width =10 )#line:799
    OO0O0O00O0O0OOO0O .insert (0 ,min (TT_ori ["事件发生日期"].dt .date ))#line:800
    OO0O0O00O0O0OOO0O .grid (row =2 ,column =1 ,sticky ="w")#line:801
    O00O0OO0OO00OOO00 =Entry (O00OO00OOO0000O00 ,width =10 )#line:803
    O00O0OO0OO00OOO00 .insert (0 ,max (TT_ori ["事件发生日期"].dt .date ))#line:804
    O00O0OO0OO00OOO00 .grid (row =2 ,column =2 ,sticky ="w")#line:805
    O0O00OO0O00OOOOO0 =Button (O00OO00OOO0000O00 ,text ="原始查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O000OO00O000O00O0 .get (),OO00OOOOOO0OOO0OO .get (),OO0O0O00O0O0OOO0O .get (),O00O0OO0OO00OOO00 .get (),1 ))#line:815
    O0O00OO0O00OOOOO0 .grid (row =3 ,column =2 ,sticky ="w")#line:816
    O0O00OO0O00OOOOO0 =Button (O00OO00OOO0000O00 ,text ="分类查看",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O000OO00O000O00O0 .get (),OO00OOOOOO0OOO0OO .get (),OO0O0O00O0O0OOO0O .get (),O00O0OO0OO00OOO00 .get (),0 ))#line:826
    O0O00OO0O00OOOOO0 .grid (row =3 ,column =3 ,sticky ="w")#line:827
    O0O00OO0O00OOOOO0 =Button (O00OO00OOO0000O00 ,text ="趋势分析",width =10 ,bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :thread_it (Tread_TOOLS_doing ,TT_ori ,O000OO00O000O00O0 .get (),OO00OOOOOO0OOO0OO .get (),OO0O0O00O0O0OOO0O .get (),O00O0OO0OO00OOO00 .get (),2 ))#line:837
    O0O00OO0O00OOOOO0 .grid (row =3 ,column =1 ,sticky ="w")#line:838
def Tread_TOOLS_doing (OOOO0OO000OOOO000 ,OOOO0O00O0OOOOO0O ,OOO00000000O0OOOO ,OO00000OOOO0O000O ,O000OOO0OO0OO00OO ,OO00O0OOO0O0000O0 ):#line:840
    ""#line:841
    global TT_biaozhun #line:842
    OOOO0OO000OOOO000 =OOOO0OO000OOOO000 [(OOOO0OO000OOOO000 ["作用对象"]==OOOO0O00O0OOOOO0O )].copy ()#line:843
    OO00000OOOO0O000O =pd .to_datetime (OO00000OOOO0O000O )#line:845
    O000OOO0OO0OO00OO =pd .to_datetime (O000OOO0OO0OO00OO )#line:846
    OOOO0OO000OOOO000 =OOOO0OO000OOOO000 [((OOOO0OO000OOOO000 ["事件发生日期"]>=OO00000OOOO0O000O )&(OOOO0OO000OOOO000 ["事件发生日期"]<=O000OOO0OO0OO00OO ))]#line:847
    text .insert (END ,"\n数据数量："+str (len (OOOO0OO000OOOO000 )))#line:848
    text .see (END )#line:849
    if OO00O0OOO0O0000O0 ==0 :#line:851
        Tread_TOOLS_check (OOOO0OO000OOOO000 ,TT_biaozhun ["关键字表"],0 )#line:852
        return 0 #line:853
    if OO00O0OOO0O0000O0 ==1 :#line:854
        Tread_TOOLS_tree_Level_2 (OOOO0OO000OOOO000 ,1 ,OOOO0OO000OOOO000 )#line:855
        return 0 #line:856
    if len (OOOO0OO000OOOO000 )<1 :#line:857
        showinfo (title ="错误信息",message ="没有符合筛选条件的报告。")#line:858
        return 0 #line:859
    Tread_TOOLS_check (OOOO0OO000OOOO000 ,TT_biaozhun ["关键字表"],1 )#line:860
    Tread_TOOLS_tree_Level_2 (Tread_TOOLS_Countall (OOOO0OO000OOOO000 ).df_find_all_keword_risk (OOO00000000O0OOOO ),1 ,0 ,OOO00000000O0OOOO )#line:863
def STAT_countx (OOOO0O00OO00OOOO0 ):#line:873
    ""#line:874
    return OOOO0O00OO00OOOO0 .value_counts ().to_dict ()#line:875
def STAT_countpx (OOO0000OO000OO000 ,OO0OOOOO0000000O0 ):#line:877
    ""#line:878
    return len (OOO0000OO000OO000 [(OOO0000OO000OO000 ==OO0OOOOO0000000O0 )])#line:879
def STAT_countnpx (O0O0OOOO000OO000O ,OOO0000OO00O00000 ):#line:881
    ""#line:882
    return len (O0O0OOOO000OO000O [(O0O0OOOO000OO000O not in OOO0000OO00O00000 )])#line:883
def STAT_get_max (OOO0OO0O0OO0OOOO0 ):#line:885
    ""#line:886
    return OOO0OO0O0OO0OOOO0 .value_counts ().max ()#line:887
def STAT_get_mean (O00OOOO0OOO0000OO ):#line:889
    ""#line:890
    return round (O00OOOO0OOO0000OO .value_counts ().mean (),2 )#line:891
def STAT_get_std (O0O00000O0OO0OO00 ):#line:893
    ""#line:894
    return round (O0O00000O0OO0OO00 .value_counts ().std (ddof =1 ),2 )#line:895
def STAT_get_95ci (O0O0OO00O00000OOO ):#line:897
    ""#line:898
    return round (np .percentile (O0O0OO00O00000OOO .value_counts (),97.5 ),2 )#line:899
def STAT_get_mean_std_ci (OO0O0O0OOOOO0OO0O ,OO00O0000OO00OO00 ):#line:901
    ""#line:902
    warnings .filterwarnings ("ignore")#line:903
    O000000OO0OO0O0O0 =TOOLS_strdict_to_pd (str (OO0O0O0OOOOO0OO0O ))["content"].values /OO00O0000OO00OO00 #line:904
    O0OOOOOOOOOOOOOO0 =round (O000000OO0OO0O0O0 .mean (),2 )#line:905
    OOOOO000OO0O00000 =round (O000000OO0OO0O0O0 .std (ddof =1 ),2 )#line:906
    O0000000O00OO00O0 =round (np .percentile (O000000OO0OO0O0O0 ,97.5 ),2 )#line:907
    return pd .Series ((O0OOOOOOOOOOOOOO0 ,OOOOO000OO0O00000 ,O0000000O00OO00O0 ))#line:908
def STAT_findx_value (O000OO0O0OOO0O0O0 ,OO000OO0O00OOO00O ):#line:910
    ""#line:911
    warnings .filterwarnings ("ignore")#line:912
    OOO0OO00OO00OO00O =TOOLS_strdict_to_pd (str (O000OO0O0OOO0O0O0 ))#line:913
    OO0000OOOOOO0OOOO =OOO0OO00OO00OO00O .where (OOO0OO00OO00OO00O ["index"]==str (OO000OO0O00OOO00O ))#line:915
    print (OO0000OOOOOO0OOOO )#line:916
    return OO0000OOOOOO0OOOO #line:917
def STAT_judge_x (OOOOOOO0OO0OOOO0O ,O0O0O0000OO0OOOO0 ):#line:919
    ""#line:920
    for O0OO0000OO0OOOO00 in O0O0O0000OO0OOOO0 :#line:921
        if OOOOOOO0OO0OOOO0O .find (O0OO0000OO0OOOO00 )>-1 :#line:922
            return 1 #line:923
def STAT_basic_risk (OO00OOOO000O000O0 ,OOO0O0O0OOO0000O0 ,OO00OO0OOOO0O0O00 ,OO0OO0O00OOO00000 ,O0O0OO0000000O000 ):#line:926
    ""#line:927
    OO00OOOO000O000O0 ["风险评分"]=0 #line:928
    OO00OOOO000O000O0 .loc [((OO00OOOO000O000O0 [OOO0O0O0OOO0000O0 ]>=3 )&(OO00OOOO000O000O0 [OO00OO0OOOO0O0O00 ]>=1 ))|(OO00OOOO000O000O0 [OOO0O0O0OOO0000O0 ]>=5 ),"风险评分"]=OO00OOOO000O000O0 ["风险评分"]+5 #line:929
    OO00OOOO000O000O0 .loc [(OO00OOOO000O000O0 [OO00OO0OOOO0O0O00 ]>=3 ),"风险评分"]=OO00OOOO000O000O0 ["风险评分"]+1 #line:930
    OO00OOOO000O000O0 .loc [(OO00OOOO000O000O0 [OO0OO0O00OOO00000 ]>=1 ),"风险评分"]=OO00OOOO000O000O0 ["风险评分"]+10 #line:931
    OO00OOOO000O000O0 ["风险评分"]=OO00OOOO000O000O0 ["风险评分"]+OO00OOOO000O000O0 [O0O0OO0000000O000 ]/100 #line:932
    return OO00OOOO000O000O0 #line:933
def STAT_find_keyword_risk (OO0O000O00OOO0OOO ,O0O000000OOOO00O0 ,OO000000OO0O0O0O0 ,O0O0OO000OOOO00OO ,OOO0OO00O00O00OOO ):#line:937
        ""#line:938
        O0OO0O00O000O000O =OO0O000O00OOO0OOO .groupby (O0O000000OOOO00O0 ).agg (证号关键字总数量 =(OO000000OO0O0O0O0 ,"count"),包含元素个数 =(O0O0OO000OOOO00OO ,"nunique"),包含元素 =(O0O0OO000OOOO00OO ,STAT_countx ),).reset_index ()#line:943
        OO0O00OO00O0000O0 =O0O000000OOOO00O0 .copy ()#line:945
        OO0O00OO00O0000O0 .append (O0O0OO000OOOO00OO )#line:946
        O0000OOO000O0O00O =OO0O000O00OOO0OOO .groupby (OO0O00OO00O0000O0 ).agg (计数 =(O0O0OO000OOOO00OO ,"count"),).reset_index ()#line:949
        OO0O0OOO00OO0OOO0 =OO0O00OO00O0000O0 .copy ()#line:952
        OO0O0OOO00OO0OOO0 .remove ("关键字")#line:953
        OOO0OOO00OOO00O00 =OO0O000O00OOO0OOO .groupby (OO0O0OOO00OO0OOO0 ).agg (该元素总数 =(O0O0OO000OOOO00OO ,"count"),).reset_index ()#line:956
        O0000OOO000O0O00O ["证号总数"]=OOO0OO00O00O00OOO #line:958
        O0OOO0O0O000O0O00 =pd .merge (O0000OOO000O0O00O ,O0OO0O00O000O000O ,on =O0O000000OOOO00O0 ,how ="left")#line:959
        if len (O0OOO0O0O000O0O00 )>0 :#line:961
            O0OOO0O0O000O0O00 [['数量均值','数量标准差','数量CI']]=O0OOO0O0O000O0O00 .包含元素 .apply (lambda OO000O00O00O0OOOO :STAT_get_mean_std_ci (OO000O00O00O0OOOO ,1 ))#line:962
        return O0OOO0O0O000O0O00 #line:963
def STAT_find_risk (OO00O00O0O0OOO000 ,OO0O000OO0OOOOO0O ,O00OO00O0O0OO00O0 ,O0OOOO0000O000O00 ):#line:969
        ""#line:970
        O00000OOOOOO00O0O =OO00O00O0O0OOO000 .groupby (OO0O000OO0OOOOO0O ).agg (证号总数量 =(O00OO00O0O0OO00O0 ,"count"),包含元素个数 =(O0OOOO0000O000O00 ,"nunique"),包含元素 =(O0OOOO0000O000O00 ,STAT_countx ),均值 =(O0OOOO0000O000O00 ,STAT_get_mean ),标准差 =(O0OOOO0000O000O00 ,STAT_get_std ),CI上限 =(O0OOOO0000O000O00 ,STAT_get_95ci ),).reset_index ()#line:978
        OO00000OO0OOO00O0 =OO0O000OO0OOOOO0O .copy ()#line:980
        OO00000OO0OOO00O0 .append (O0OOOO0000O000O00 )#line:981
        O00O00O000OOO00O0 =OO00O00O0O0OOO000 .groupby (OO00000OO0OOO00O0 ).agg (计数 =(O0OOOO0000O000O00 ,"count"),严重伤害数 =("伤害",lambda OOOOO000000000O00 :STAT_countpx (OOOOO000000000O00 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0OO000OO0O0OOO00 :STAT_countpx (O0OO000OO0O0OOO00 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:988
        O00O00O0O00O00O00 =pd .merge (O00O00O000OOO00O0 ,O00000OOOOOO00O0O ,on =OO0O000OO0OOOOO0O ,how ="left")#line:990
        O00O00O0O00O00O00 ["风险评分"]=0 #line:992
        O00O00O0O00O00O00 ["报表类型"]="dfx_findrisk"+O0OOOO0000O000O00 #line:993
        O00O00O0O00O00O00 .loc [((O00O00O0O00O00O00 ["计数"]>=3 )&(O00O00O0O00O00O00 ["严重伤害数"]>=1 )|(O00O00O0O00O00O00 ["计数"]>=5 )),"风险评分"]=O00O00O0O00O00O00 ["风险评分"]+5 #line:994
        O00O00O0O00O00O00 .loc [(O00O00O0O00O00O00 ["计数"]>=(O00O00O0O00O00O00 ["均值"]+O00O00O0O00O00O00 ["标准差"])),"风险评分"]=O00O00O0O00O00O00 ["风险评分"]+1 #line:995
        O00O00O0O00O00O00 .loc [(O00O00O0O00O00O00 ["计数"]>=O00O00O0O00O00O00 ["CI上限"]),"风险评分"]=O00O00O0O00O00O00 ["风险评分"]+1 #line:996
        O00O00O0O00O00O00 .loc [(O00O00O0O00O00O00 ["严重伤害数"]>=3 )&(O00O00O0O00O00O00 ["风险评分"]>=7 ),"风险评分"]=O00O00O0O00O00O00 ["风险评分"]+1 #line:997
        O00O00O0O00O00O00 .loc [(O00O00O0O00O00O00 ["死亡数量"]>=1 ),"风险评分"]=O00O00O0O00O00O00 ["风险评分"]+10 #line:998
        O00O00O0O00O00O00 ["风险评分"]=O00O00O0O00O00O00 ["风险评分"]+O00O00O0O00O00O00 ["单位个数"]/100 #line:999
        O00O00O0O00O00O00 =O00O00O0O00O00O00 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:1000
        return O00O00O0O00O00O00 #line:1002
def TOOLS_get_list (O00000OO000O0O0O0 ):#line:1004
    ""#line:1005
    O00000OO000O0O0O0 =str (O00000OO000O0O0O0 )#line:1006
    O0OO00OO00OOOOO00 =[]#line:1007
    O0OO00OO00OOOOO00 .append (O00000OO000O0O0O0 )#line:1008
    O0OO00OO00OOOOO00 =",".join (O0OO00OO00OOOOO00 )#line:1009
    O0OO00OO00OOOOO00 =O0OO00OO00OOOOO00 .split ("|")#line:1010
    O0O0OOO0O0O000O00 =O0OO00OO00OOOOO00 [:]#line:1011
    O0OO00OO00OOOOO00 =list (set (O0OO00OO00OOOOO00 ))#line:1012
    O0OO00OO00OOOOO00 .sort (key =O0O0OOO0O0O000O00 .index )#line:1013
    return O0OO00OO00OOOOO00 #line:1014
def TOOLS_get_list0 (OOO000O000O000O0O ,O00O0O00OO00OO000 ,*O0000O00O00OOOOO0 ):#line:1016
    ""#line:1017
    OOO000O000O000O0O =str (OOO000O000O000O0O )#line:1018
    if pd .notnull (OOO000O000O000O0O ):#line:1020
        try :#line:1021
            if "use("in str (OOO000O000O000O0O ):#line:1022
                O000O0OO00O0OOO0O =OOO000O000O000O0O #line:1023
                O0O0OOOO00OO0O0O0 =re .compile (r"[(](.*?)[)]",re .S )#line:1024
                OOOO0000OOOO0000O =re .findall (O0O0OOOO00OO0O0O0 ,O000O0OO00O0OOO0O )#line:1025
                OOOOO0O000000OO00 =[]#line:1026
                if ").list"in OOO000O000O000O0O :#line:1027
                    OO000OO000O0O0OO0 ="配置表/"+str (OOOO0000OOOO0000O [0 ])+".xls"#line:1028
                    O00O000OOO000OOOO =pd .read_excel (OO000OO000O0O0OO0 ,sheet_name =OOOO0000OOOO0000O [0 ],header =0 ,index_col =0 ).reset_index ()#line:1031
                    O00O000OOO000OOOO ["检索关键字"]=O00O000OOO000OOOO ["检索关键字"].astype (str )#line:1032
                    OOOOO0O000000OO00 =O00O000OOO000OOOO ["检索关键字"].tolist ()+OOOOO0O000000OO00 #line:1033
                if ").file"in OOO000O000O000O0O :#line:1034
                    OOOOO0O000000OO00 =O00O0O00OO00OO000 [OOOO0000OOOO0000O [0 ]].astype (str ).tolist ()+OOOOO0O000000OO00 #line:1036
                try :#line:1039
                    if "报告类型-新的"in O00O0O00OO00OO000 .columns :#line:1040
                        OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1041
                        OOOOO0O000000OO00 =OOOOO0O000000OO00 .split (";")#line:1042
                        OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1043
                        OOOOO0O000000OO00 =OOOOO0O000000OO00 .split ("；")#line:1044
                        OOOOO0O000000OO00 =[O0O0OOO00O0000OO0 .replace ("（严重）","")for O0O0OOO00O0000OO0 in OOOOO0O000000OO00 ]#line:1045
                        OOOOO0O000000OO00 =[OO00OOOO000OO00O0 .replace ("（一般）","")for OO00OOOO000OO00O0 in OOOOO0O000000OO00 ]#line:1046
                except :#line:1047
                    pass #line:1048
                OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1051
                OOOOO0O000000OO00 =OOOOO0O000000OO00 .split ("、")#line:1052
                OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1053
                OOOOO0O000000OO00 =OOOOO0O000000OO00 .split ("，")#line:1054
                OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1055
                OOOOO0O000000OO00 =OOOOO0O000000OO00 .split (",")#line:1056
                OO000OOOO0O00000O =OOOOO0O000000OO00 [:]#line:1058
                try :#line:1059
                    if O0000O00O00OOOOO0 [0 ]==1000 :#line:1060
                      pass #line:1061
                except :#line:1062
                      OOOOO0O000000OO00 =list (set (OOOOO0O000000OO00 ))#line:1063
                OOOOO0O000000OO00 .sort (key =OO000OOOO0O00000O .index )#line:1064
            else :#line:1066
                OOO000O000O000O0O =str (OOO000O000O000O0O )#line:1067
                OOOOO0O000000OO00 =[]#line:1068
                OOOOO0O000000OO00 .append (OOO000O000O000O0O )#line:1069
                OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1070
                OOOOO0O000000OO00 =OOOOO0O000000OO00 .split ("、")#line:1071
                OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1072
                OOOOO0O000000OO00 =OOOOO0O000000OO00 .split ("，")#line:1073
                OOOOO0O000000OO00 =",".join (OOOOO0O000000OO00 )#line:1074
                OOOOO0O000000OO00 =OOOOO0O000000OO00 .split (",")#line:1075
                OO000OOOO0O00000O =OOOOO0O000000OO00 [:]#line:1077
                try :#line:1078
                    if O0000O00O00OOOOO0 [0 ]==1000 :#line:1079
                      OOOOO0O000000OO00 =list (set (OOOOO0O000000OO00 ))#line:1080
                except :#line:1081
                      pass #line:1082
                OOOOO0O000000OO00 .sort (key =OO000OOOO0O00000O .index )#line:1083
                OOOOO0O000000OO00 .sort (key =OO000OOOO0O00000O .index )#line:1084
        except ValueError2 :#line:1086
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:1087
            return False #line:1088
    return OOOOO0O000000OO00 #line:1090
def TOOLS_strdict_to_pd (OO0OOOOOOO0O000O0 ):#line:1091
    ""#line:1092
    return pd .DataFrame .from_dict (eval (OO0OOOOOOO0O000O0 ),orient ="index",columns =["content"]).reset_index ()#line:1093
def Tread_TOOLS_view_dict (OOOO0O00OO0000OOO ,OOO0OOO00OOOO0OO0 ):#line:1095
    ""#line:1096
    OOOOO0OOOOO0OO00O =Toplevel ()#line:1097
    OOOOO0OOOOO0OO00O .title ("查看数据")#line:1098
    OOOOO0OOOOO0OO00O .geometry ("700x500")#line:1099
    O00OOOO0OOO0O0OO0 =Scrollbar (OOOOO0OOOOO0OO00O )#line:1101
    O00OO0OO0O00O000O =Text (OOOOO0OOOOO0OO00O ,height =100 ,width =150 )#line:1102
    O00OOOO0OOO0O0OO0 .pack (side =RIGHT ,fill =Y )#line:1103
    O00OO0OO0O00O000O .pack ()#line:1104
    O00OOOO0OOO0O0OO0 .config (command =O00OO0OO0O00O000O .yview )#line:1105
    O00OO0OO0O00O000O .config (yscrollcommand =O00OOOO0OOO0O0OO0 .set )#line:1106
    if OOO0OOO00OOOO0OO0 ==1 :#line:1107
        O00OO0OO0O00O000O .insert (END ,OOOO0O00OO0000OOO )#line:1109
        O00OO0OO0O00O000O .insert (END ,"\n\n")#line:1110
        return 0 #line:1111
    for O00O0O0OOOOO000O0 in range (len (OOOO0O00OO0000OOO )):#line:1112
        O00OO0OO0O00O000O .insert (END ,OOOO0O00OO0000OOO .iloc [O00O0O0OOOOO000O0 ,0 ])#line:1113
        O00OO0OO0O00O000O .insert (END ,":")#line:1114
        O00OO0OO0O00O000O .insert (END ,OOOO0O00OO0000OOO .iloc [O00O0O0OOOOO000O0 ,1 ])#line:1115
        O00OO0OO0O00O000O .insert (END ,"\n\n")#line:1116
def Tread_TOOLS_fashenglv (O000OO00O0O00O00O ,OOO00O0OO0O0O0OOO ):#line:1119
    global TT_biaozhun #line:1120
    O000OO00O0O00O00O =pd .merge (O000OO00O0O00O00O ,TT_biaozhun [OOO00O0OO0O0O0OOO ],on =[OOO00O0OO0O0O0OOO ],how ="left").reset_index (drop =True )#line:1121
    O000O0O00O0OOO000 =O000OO00O0O00O00O ["使用次数"].mean ()#line:1123
    O000OO00O0O00O00O ["使用次数"]=O000OO00O0O00O00O ["使用次数"].fillna (int (O000O0O00O0OOO000 ))#line:1124
    O0OO000OO0O0OO0OO =O000OO00O0O00O00O ["使用次数"][:-1 ].sum ()#line:1125
    O000OO00O0O00O00O .iloc [-1 ,-1 ]=O0OO000OO0O0OO0OO #line:1126
    O00O00OO00000O0OO =[O0O0OO0O0OO00000O for O0O0OO0O0OO00000O in O000OO00O0O00O00O .columns if (O0O0OO0O0OO00000O not in ["使用次数",OOO00O0OO0O0O0OOO ])]#line:1127
    for O0OO00O0OOOO00OO0 ,O0OOOO00O00O0OO00 in O000OO00O0O00O00O .iterrows ():#line:1128
        for OO000O0O0O0000OO0 in O00O00OO00000O0OO :#line:1129
            O000OO00O0O00O00O .loc [O0OO00O0OOOO00OO0 ,OO000O0O0O0000OO0 ]=int (O0OOOO00O00O0OO00 [OO000O0O0O0000OO0 ])/int (O0OOOO00O00O0OO00 ["使用次数"])#line:1130
    del O000OO00O0O00O00O ["使用次数"]#line:1131
    Tread_TOOLS_tree_Level_2 (O000OO00O0O00O00O ,1 ,1 ,OOO00O0OO0O0O0OOO )#line:1132
def TOOLS_save_dict (O000O0OOOOOOOO00O ):#line:1134
    ""#line:1135
    OO000OOO0O00OO0O0 =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="【排序后的原始数据】",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1141
    try :#line:1142
        O000O0OOOOOOOO00O ["详细描述T"]=O000O0OOOOOOOO00O ["详细描述T"].astype (str )#line:1143
    except :#line:1144
        pass #line:1145
    try :#line:1146
        O000O0OOOOOOOO00O ["报告编码"]=O000O0OOOOOOOO00O ["报告编码"].astype (str )#line:1147
    except :#line:1148
        pass #line:1149
    try :#line:1150
        OO0OOOOO0000O000O =re .search ("\【(.*?)\】",OO000OOO0O00OO0O0 )#line:1151
        O000O0OOOOOOOO00O ["对象"]=OO0OOOOO0000O000O .group (1 )#line:1152
    except :#line:1153
        pass #line:1154
    OO0OOO0O00OOOOO00 =pd .ExcelWriter (OO000OOO0O00OO0O0 ,engine ="xlsxwriter")#line:1155
    O000O0OOOOOOOO00O .to_excel (OO0OOO0O00OOOOO00 ,sheet_name ="字典数据")#line:1156
    OO0OOO0O00OOOOO00 .close ()#line:1157
    showinfo (title ="提示",message ="文件写入成功。")#line:1158
def Tread_TOOLS_DRAW_histbar (O0OO0OOOO0O000OO0 ):#line:1162
    ""#line:1163
    OOOO00O00OO000OO0 =Toplevel ()#line:1166
    OOOO00O00OO000OO0 .title ("直方图")#line:1167
    OOO0OOOOOO0O0OO00 =ttk .Frame (OOOO00O00OO000OO0 ,height =20 )#line:1168
    OOO0OOOOOO0O0OO00 .pack (side =TOP )#line:1169
    OO0O0OOOOO0O00OO0 =Figure (figsize =(12 ,6 ),dpi =100 )#line:1171
    OO00O0000000000OO =FigureCanvasTkAgg (OO0O0OOOOO0O00OO0 ,master =OOOO00O00OO000OO0 )#line:1172
    OO00O0000000000OO .draw ()#line:1173
    OO00O0000000000OO .get_tk_widget ().pack (expand =1 )#line:1174
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1176
    plt .rcParams ['axes.unicode_minus']=False #line:1177
    OO0OO000O0OOO000O =NavigationToolbar2Tk (OO00O0000000000OO ,OOOO00O00OO000OO0 )#line:1179
    OO0OO000O0OOO000O .update ()#line:1180
    OO00O0000000000OO .get_tk_widget ().pack ()#line:1181
    OO00OOO0OO0O0OOO0 =OO0O0OOOOO0O00OO0 .add_subplot (111 )#line:1183
    OO00OOO0OO0O0OOO0 .set_title ("直方图")#line:1185
    O0O00O00OO0OO000O =O0OO0OOOO0O000OO0 .columns .to_list ()#line:1187
    O0O00O00OO0OO000O .remove ("对象")#line:1188
    OOOO0OOO0O000O00O =np .arange (len (O0O00O00OO0OO000O ))#line:1189
    for O0000O00O0O00000O in O0O00O00OO0OO000O :#line:1193
        O0OO0OOOO0O000OO0 [O0000O00O0O00000O ]=O0OO0OOOO0O000OO0 [O0000O00O0O00000O ].astype (float )#line:1194
    O0OO0OOOO0O000OO0 ['数据']=O0OO0OOOO0O000OO0 [O0O00O00OO0OO000O ].values .tolist ()#line:1196
    OOO0OO00O0000OO0O =0 #line:1197
    for OOO0OOO00OOOO0000 ,OO0O0OOO0000OOOO0 in O0OO0OOOO0O000OO0 .iterrows ():#line:1198
        OO00OOO0OO0O0OOO0 .bar ([OO0O000O0OO000O00 +OOO0OO00O0000OO0O for OO0O000O0OO000O00 in OOOO0OOO0O000O00O ],O0OO0OOOO0O000OO0 .loc [OOO0OOO00OOOO0000 ,'数据'],label =O0O00O00OO0OO000O ,width =0.1 )#line:1199
        for OOOOO00OOO000OO00 ,O0OO000OO0O00OO00 in zip ([O0OO000O00O000OOO +OOO0OO00O0000OO0O for O0OO000O00O000OOO in OOOO0OOO0O000O00O ],O0OO0OOOO0O000OO0 .loc [OOO0OOO00OOOO0000 ,'数据']):#line:1202
           OO00OOO0OO0O0OOO0 .text (OOOOO00OOO000OO00 -0.015 ,O0OO000OO0O00OO00 +0.07 ,str (int (O0OO000OO0O00OO00 )),color ='black',size =8 )#line:1203
        OOO0OO00O0000OO0O =OOO0OO00O0000OO0O +0.1 #line:1205
    OO00OOO0OO0O0OOO0 .set_xticklabels (O0OO0OOOO0O000OO0 .columns .to_list (),rotation =-90 ,fontsize =8 )#line:1207
    OO00OOO0OO0O0OOO0 .legend (O0OO0OOOO0O000OO0 ["对象"])#line:1211
    OO00O0000000000OO .draw ()#line:1214
def Tread_TOOLS_DRAW_make_risk_plot (O00O000OO0O0OOO00 ,OOOOOOO0OOO0O0000 ,O0000OOOO00O0O0OO ,O0O0O0OOOO000000O ,OOOO0OO0OOO000000 ):#line:1216
    ""#line:1217
    OO0O000O0O0OO0OOO =Toplevel ()#line:1220
    OO0O000O0O0OO0OOO .title (O0O0O0OOOO000000O )#line:1221
    O00OO00O0000O0000 =ttk .Frame (OO0O000O0O0OO0OOO ,height =20 )#line:1222
    O00OO00O0000O0000 .pack (side =TOP )#line:1223
    OOO0OOOO0OO0O00OO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1225
    OOO000OOOOO0OOO0O =FigureCanvasTkAgg (OOO0OOOO0OO0O00OO ,master =OO0O000O0O0OO0OOO )#line:1226
    OOO000OOOOO0OOO0O .draw ()#line:1227
    OOO000OOOOO0OOO0O .get_tk_widget ().pack (expand =1 )#line:1228
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1230
    plt .rcParams ['axes.unicode_minus']=False #line:1231
    OOO0OOO00O0O0000O =NavigationToolbar2Tk (OOO000OOOOO0OOO0O ,OO0O000O0O0OO0OOO )#line:1233
    OOO0OOO00O0O0000O .update ()#line:1234
    OOO000OOOOO0OOO0O .get_tk_widget ().pack ()#line:1235
    O0OOOO0O00O0O00O0 =OOO0OOOO0OO0O00OO .add_subplot (111 )#line:1237
    O0OOOO0O00O0O00O0 .set_title (O0O0O0OOOO000000O )#line:1239
    OO000OOO0O0O0O000 =O00O000OO0O0OOO00 [OOOOOOO0OOO0O0000 ]#line:1240
    if OOOO0OO0OOO000000 !=999 :#line:1243
        O0OOOO0O00O0O00O0 .set_xticklabels (OO000OOO0O0O0O000 ,rotation =-90 ,fontsize =8 )#line:1244
    O00O0OO0OOOOOOOOO =range (0 ,len (OO000OOO0O0O0O000 ),1 )#line:1247
    for OOOOOO00O00OOOOO0 in O0000OOOO00O0O0OO :#line:1252
        O0O0000000O0OOOOO =O00O000OO0O0OOO00 [OOOOOO00O00OOOOO0 ].astype (float )#line:1253
        if OOOOOO00O00OOOOO0 =="关注区域":#line:1255
            O0OOOO0O00O0O00O0 .plot (list (OO000OOO0O0O0O000 ),list (O0O0000000O0OOOOO ),label =str (OOOOOO00O00OOOOO0 ),color ="red")#line:1256
        else :#line:1257
            O0OOOO0O00O0O00O0 .plot (list (OO000OOO0O0O0O000 ),list (O0O0000000O0OOOOO ),label =str (OOOOOO00O00OOOOO0 ))#line:1258
        if OOOO0OO0OOO000000 ==100 :#line:1261
            for O000OOOOO0OOOO0OO ,O0O0O0OOO00O0OO0O in zip (OO000OOO0O0O0O000 ,O0O0000000O0OOOOO ):#line:1262
                if O0O0O0OOO00O0OO0O ==max (O0O0000000O0OOOOO )and O0O0O0OOO00O0OO0O >=3 and len (O0000OOOO00O0O0OO )!=1 :#line:1263
                     O0OOOO0O00O0O00O0 .text (O000OOOOO0OOOO0OO ,O0O0O0OOO00O0OO0O ,(str (OOOOOO00O00OOOOO0 )+":"+str (int (O0O0O0OOO00O0OO0O ))),color ='black',size =8 )#line:1264
                if len (O0000OOOO00O0O0OO )==1 and O0O0O0OOO00O0OO0O >=0.01 :#line:1265
                     O0OOOO0O00O0O00O0 .text (O000OOOOO0OOOO0OO ,O0O0O0OOO00O0OO0O ,str (int (O0O0O0OOO00O0OO0O )),color ='black',size =8 )#line:1266
    if len (O0000OOOO00O0O0OO )==1 :#line:1276
        O000OO000O0OO0O00 =O00O000OO0O0OOO00 [O0000OOOO00O0O0OO ].astype (float ).values #line:1277
        OO0OO00OOO00O0000 =O000OO000O0OO0O00 .mean ()#line:1278
        OOO0O0OO0OOOOOOO0 =O000OO000O0OO0O00 .std ()#line:1279
        OO000O000OOOOO0OO =OO0OO00OOO00O0000 +3 *OOO0O0OO0OOOOOOO0 #line:1280
        OO0O0OOO000O00O0O =OOO0O0OO0OOOOOOO0 -3 *OOO0O0OO0OOOOOOO0 #line:1281
        O0OOOO0O00O0O00O0 .axhline (OO0OO00OOO00O0000 ,color ='r',linestyle ='--',label ='Mean')#line:1283
        O0OOOO0O00O0O00O0 .axhline (OO000O000OOOOO0OO ,color ='g',linestyle ='--',label ='UCL(μ+3σ)')#line:1284
        O0OOOO0O00O0O00O0 .axhline (OO0O0OOO000O00O0O ,color ='g',linestyle ='--',label ='LCL(μ-3σ)')#line:1285
    O0OOOO0O00O0O00O0 .set_title ("控制图")#line:1287
    O0OOOO0O00O0O00O0 .set_xlabel ("项")#line:1288
    OOO0OOOO0OO0O00OO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1289
    O000OOO000OOOOOO0 =O0OOOO0O00O0O00O0 .get_position ()#line:1290
    O0OOOO0O00O0O00O0 .set_position ([O000OOO000OOOOOO0 .x0 ,O000OOO000OOOOOO0 .y0 ,O000OOO000OOOOOO0 .width *0.7 ,O000OOO000OOOOOO0 .height ])#line:1291
    O0OOOO0O00O0O00O0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1292
    OOOOOO00O0OO00O0O =StringVar ()#line:1295
    OO00OOOOO0O00OOO0 =ttk .Combobox (O00OO00O0000O0000 ,width =15 ,textvariable =OOOOOO00O0OO00O0O ,state ='readonly')#line:1296
    OO00OOOOO0O00OOO0 ['values']=O0000OOOO00O0O0OO #line:1297
    OO00OOOOO0O00OOO0 .pack (side =LEFT )#line:1298
    OO00OOOOO0O00OOO0 .current (0 )#line:1299
    OOO000000O0000OO0 =Button (O00OO00O0000O0000 ,text ="控制图（单项）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O00O000OO0O0OOO00 ,OOOOOOO0OOO0O0000 ,[O0O0OOOOO0OO0OOOO for O0O0OOOOO0OO0OOOO in O0000OOOO00O0O0OO if OOOOOO00O0OO00O0O .get ()in O0O0OOOOO0OO0OOOO ],O0O0O0OOOO000000O ,OOOO0OO0OOO000000 ))#line:1309
    OOO000000O0000OO0 .pack (side =LEFT ,anchor ="ne")#line:1310
    OO000OOOO00OO0O0O =Button (O00OO00O0000O0000 ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :Tread_TOOLS_DRAW_make_risk_plot (O00O000OO0O0OOO00 ,OOOOOOO0OOO0O0000 ,O0000OOOO00O0O0OO ,O0O0O0OOOO000000O ,0 ))#line:1318
    OO000OOOO00OO0O0O .pack (side =LEFT ,anchor ="ne")#line:1320
    OOO000OOOOO0OOO0O .draw ()#line:1321
def Tread_TOOLS_draw (O00O0000OO0O0O0O0 ,O00OO0OO0OO00O00O ,OOOO00O00000OO000 ,OO0OOO0OOOOOOO0OO ,O0O000OO0O0OO0OOO ):#line:1323
    ""#line:1324
    warnings .filterwarnings ("ignore")#line:1325
    O0O000O000O000O00 =Toplevel ()#line:1326
    O0O000O000O000O00 .title (O00OO0OO0OO00O00O )#line:1327
    OO0OOO0OO0000OOO0 =ttk .Frame (O0O000O000O000O00 ,height =20 )#line:1328
    OO0OOO0OO0000OOO0 .pack (side =TOP )#line:1329
    O000OO00O00OO0000 =Figure (figsize =(12 ,6 ),dpi =100 )#line:1331
    O00OO0OO0OO0O000O =FigureCanvasTkAgg (O000OO00O00OO0000 ,master =O0O000O000O000O00 )#line:1332
    O00OO0OO0OO0O000O .draw ()#line:1333
    O00OO0OO0OO0O000O .get_tk_widget ().pack (expand =1 )#line:1334
    OOOOO0OOOOO0O00O0 =O000OO00O00OO0000 .add_subplot (111 )#line:1335
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1337
    plt .rcParams ['axes.unicode_minus']=False #line:1338
    OOO0OO00OOO0OOOOO =NavigationToolbar2Tk (O00OO0OO0OO0O000O ,O0O000O000O000O00 )#line:1340
    OOO0OO00OOO0OOOOO .update ()#line:1341
    O00OO0OO0OO0O000O .get_tk_widget ().pack ()#line:1343
    try :#line:1346
        O0OO000O0O0O0OOO0 =O00O0000OO0O0O0O0 .columns #line:1347
        O00O0000OO0O0O0O0 =O00O0000OO0O0O0O0 .sort_values (by =OO0OOO0OOOOOOO0OO ,ascending =[False ],na_position ="last")#line:1348
    except :#line:1349
        OO0O0O0O0OO0O0O00 =eval (O00O0000OO0O0O0O0 )#line:1350
        OO0O0O0O0OO0O0O00 =pd .DataFrame .from_dict (OO0O0O0O0OO0O0O00 ,TT_orient =OOOO00O00000OO000 ,columns =[OO0OOO0OOOOOOO0OO ]).reset_index ()#line:1353
        O00O0000OO0O0O0O0 =OO0O0O0O0OO0O0O00 .sort_values (by =OO0OOO0OOOOOOO0OO ,ascending =[False ],na_position ="last")#line:1354
    if ("日期"in O00OO0OO0OO00O00O or "时间"in O00OO0OO0OO00O00O or "季度"in O00OO0OO0OO00O00O )and "饼图"not in O0O000OO0O0OO0OOO :#line:1358
        O00O0000OO0O0O0O0 [OOOO00O00000OO000 ]=pd .to_datetime (O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],format ="%Y/%m/%d").dt .date #line:1359
        O00O0000OO0O0O0O0 =O00O0000OO0O0O0O0 .sort_values (by =OOOO00O00000OO000 ,ascending =[True ],na_position ="last")#line:1360
    elif "批号"in O00OO0OO0OO00O00O :#line:1361
        O00O0000OO0O0O0O0 [OOOO00O00000OO000 ]=O00O0000OO0O0O0O0 [OOOO00O00000OO000 ].astype (str )#line:1362
        O00O0000OO0O0O0O0 =O00O0000OO0O0O0O0 .sort_values (by =OOOO00O00000OO000 ,ascending =[True ],na_position ="last")#line:1363
        OOOOO0OOOOO0O00O0 .set_xticklabels (O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],rotation =-90 ,fontsize =8 )#line:1364
    else :#line:1365
        O00O0000OO0O0O0O0 [OOOO00O00000OO000 ]=O00O0000OO0O0O0O0 [OOOO00O00000OO000 ].astype (str )#line:1366
        OOOOO0OOOOO0O00O0 .set_xticklabels (O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],rotation =-90 ,fontsize =8 )#line:1367
    OOO0O0OOO0OO0000O =O00O0000OO0O0O0O0 [OO0OOO0OOOOOOO0OO ]#line:1369
    O0O000O0O0OO0OO00 =range (0 ,len (OOO0O0OOO0OO0000O ),1 )#line:1370
    OOOOO0OOOOO0O00O0 .set_title (O00OO0OO0OO00O00O )#line:1372
    if O0O000OO0O0OO0OOO =="柱状图":#line:1376
        OOOOO0OOOOO0O00O0 .bar (x =O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],height =OOO0O0OOO0OO0000O ,width =0.2 ,color ="#87CEFA")#line:1377
    elif O0O000OO0O0OO0OOO =="饼图":#line:1378
        OOOOO0OOOOO0O00O0 .pie (x =OOO0O0OOO0OO0000O ,labels =O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],autopct ="%0.2f%%")#line:1379
    elif O0O000OO0O0OO0OOO =="折线图":#line:1380
        OOOOO0OOOOO0O00O0 .plot (O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],OOO0O0OOO0OO0000O ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:1381
    elif "帕累托图"in str (O0O000OO0O0OO0OOO ):#line:1383
        OOOO00O000O0OO00O =O00O0000OO0O0O0O0 [OO0OOO0OOOOOOO0OO ].fillna (0 )#line:1384
        O0O00OOO00OO000O0 =OOOO00O000O0OO00O .cumsum ()/OOOO00O000O0OO00O .sum ()*100 #line:1388
        O00O0000OO0O0O0O0 ["百分比"]=round (O00O0000OO0O0O0O0 ["数量"]/OOOO00O000O0OO00O .sum ()*100 ,2 )#line:1389
        O00O0000OO0O0O0O0 ["累计百分比"]=round (O0O00OOO00OO000O0 ,2 )#line:1390
        OOO000OO00O0OO00O =O0O00OOO00OO000O0 [O0O00OOO00OO000O0 >0.8 ].index [0 ]#line:1391
        O0OO000OOO000O000 =OOOO00O000O0OO00O .index .tolist ().index (OOO000OO00O0OO00O )#line:1392
        OOOOO0OOOOO0O00O0 .bar (x =O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],height =OOOO00O000O0OO00O ,color ="C0",label =OO0OOO0OOOOOOO0OO )#line:1396
        OOOOOOOO000OOOOOO =OOOOO0OOOOO0O00O0 .twinx ()#line:1397
        OOOOOOOO000OOOOOO .plot (O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],O0O00OOO00OO000O0 ,color ="C1",alpha =0.6 ,label ="累计比例")#line:1398
        OOOOOOOO000OOOOOO .yaxis .set_major_formatter (PercentFormatter ())#line:1399
        OOOOO0OOOOO0O00O0 .tick_params (axis ="y",colors ="C0")#line:1404
        OOOOOOOO000OOOOOO .tick_params (axis ="y",colors ="C1")#line:1405
        for O00000OO00OO000O0 ,OO0OO0O0OOO000OO0 ,OO000OO0000OOOO0O ,O00O00O00O000O00O in zip (O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],OOOO00O000O0OO00O ,O00O0000OO0O0O0O0 ["百分比"],O00O0000OO0O0O0O0 ["累计百分比"]):#line:1407
            OOOOO0OOOOO0O00O0 .text (O00000OO00OO000O0 ,OO0OO0O0OOO000OO0 +0.1 ,str (int (OO0OO0O0OOO000OO0 ))+", "+str (int (OO000OO0000OOOO0O ))+"%,"+str (int (O00O00O00O000O00O ))+"%",color ='black',size =8 )#line:1408
        if "超级帕累托图"in str (O0O000OO0O0OO0OOO ):#line:1411
            O0OO0000OO00O0000 =re .compile (r'[(](.*?)[)]',re .S )#line:1412
            O00O00OO0O0OO0O0O =re .findall (O0OO0000OO00O0000 ,O0O000OO0O0OO0OOO )[0 ]#line:1413
            OOOOO0OOOOO0O00O0 .bar (x =O00O0000OO0O0O0O0 [OOOO00O00000OO000 ],height =O00O0000OO0O0O0O0 [O00O00OO0O0OO0O0O ],color ="orangered",label =O00O00OO0O0OO0O0O )#line:1414
    O000OO00O00OO0000 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1419
    O00OOO0O0OO0OO0OO =OOOOO0OOOOO0O00O0 .get_position ()#line:1420
    OOOOO0OOOOO0O00O0 .set_position ([O00OOO0O0OO0OO0OO .x0 ,O00OOO0O0OO0OO0OO .y0 ,O00OOO0O0OO0OO0OO .width *0.7 ,O00OOO0O0OO0OO0OO .height ])#line:1421
    OOOOO0OOOOO0O00O0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1422
    O00OO0OO0OO0O000O .draw ()#line:1425
    if len (OOO0O0OOO0OO0000O )<=20 and O0O000OO0O0OO0OOO !="饼图"and O0O000OO0O0OO0OOO !="帕累托图":#line:1428
        for O0OOOOO0O00OOO00O ,OO0000000OOO00O0O in zip (O0O000O0O0OO0OO00 ,OOO0O0OOO0OO0000O ):#line:1429
            OO0OO0OO0000OO0OO =str (OO0000000OOO00O0O )#line:1430
            OO0000OOOOO000O00 =(O0OOOOO0O00OOO00O ,OO0000000OOO00O0O +0.3 )#line:1431
            OOOOO0OOOOO0O00O0 .annotate (OO0OO0OO0000OO0OO ,xy =OO0000OOOOO000O00 ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:1432
    O0O0O0O0OOOOOOOOO =Button (OO0OOO0OO0000OOO0 ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (O00O0000OO0O0O0O0 ),)#line:1442
    O0O0O0O0OOOOOOOOO .pack (side =RIGHT )#line:1443
    O00O00O000O0O0OOO =Button (OO0OOO0OO0000OOO0 ,relief =GROOVE ,text ="查看原始数据",command =lambda :Tread_TOOLS_view_dict (O00O0000OO0O0O0O0 ,1 ))#line:1447
    O00O00O000O0O0OOO .pack (side =RIGHT )#line:1448
    O0O00O0OOO0OOO0OO =Button (OO0OOO0OO0000OOO0 ,relief =GROOVE ,text ="饼图",command =lambda :Tread_TOOLS_draw (O00O0000OO0O0O0O0 ,O00OO0OO0OO00O00O ,OOOO00O00000OO000 ,OO0OOO0OOOOOOO0OO ,"饼图"),)#line:1456
    O0O00O0OOO0OOO0OO .pack (side =LEFT )#line:1457
    O0O00O0OOO0OOO0OO =Button (OO0OOO0OO0000OOO0 ,relief =GROOVE ,text ="柱状图",command =lambda :Tread_TOOLS_draw (O00O0000OO0O0O0O0 ,O00OO0OO0OO00O00O ,OOOO00O00000OO000 ,OO0OOO0OOOOOOO0OO ,"柱状图"),)#line:1464
    O0O00O0OOO0OOO0OO .pack (side =LEFT )#line:1465
    O0O00O0OOO0OOO0OO =Button (OO0OOO0OO0000OOO0 ,relief =GROOVE ,text ="折线图",command =lambda :Tread_TOOLS_draw (O00O0000OO0O0O0O0 ,O00OO0OO0OO00O00O ,OOOO00O00000OO000 ,OO0OOO0OOOOOOO0OO ,"折线图"),)#line:1471
    O0O00O0OOO0OOO0OO .pack (side =LEFT )#line:1472
    O0O00O0OOO0OOO0OO =Button (OO0OOO0OO0000OOO0 ,relief =GROOVE ,text ="帕累托图",command =lambda :Tread_TOOLS_draw (O00O0000OO0O0O0O0 ,O00OO0OO0OO00O00O ,OOOO00O00000OO000 ,OO0OOO0OOOOOOO0OO ,"帕累托图"),)#line:1479
    O0O00O0OOO0OOO0OO .pack (side =LEFT )#line:1480
def helper ():#line:1486
    ""#line:1487
    OO000OOOO00OOOO00 =Toplevel ()#line:1488
    OO000OOOO00OOOO00 .title ("程序使用帮助")#line:1489
    OO000OOOO00OOOO00 .geometry ("700x500")#line:1490
    OO00OOO0OOO000000 =Scrollbar (OO000OOOO00OOOO00 )#line:1492
    OO0O00O00O0OO0000 =Text (OO000OOOO00OOOO00 ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1493
    OO00OOO0OOO000000 .pack (side =RIGHT ,fill =Y )#line:1494
    OO0O00O00O0OO0000 .pack ()#line:1495
    OO00OOO0OOO000000 .config (command =OO0O00O00O0OO0000 .yview )#line:1496
    OO0O00O00O0OO0000 .config (yscrollcommand =OO00OOO0OOO000000 .set )#line:1497
    OO0O00O00O0OO0000 .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1502
    OO0O00O00O0OO0000 .config (state =DISABLED )#line:1503
def Tread_TOOLS_CLEAN (O0O00OOOOOOOO0O0O ):#line:1507
        ""#line:1508
        O0O00OOOOOOOO0O0O ["报告编码"]=O0O00OOOOOOOO0O0O ["报告编码"].astype ("str")#line:1510
        O0O00OOOOOOOO0O0O ["产品批号"]=O0O00OOOOOOOO0O0O ["产品批号"].astype ("str")#line:1512
        O0O00OOOOOOOO0O0O ["型号"]=O0O00OOOOOOOO0O0O ["型号"].astype ("str")#line:1513
        O0O00OOOOOOOO0O0O ["规格"]=O0O00OOOOOOOO0O0O ["规格"].astype ("str")#line:1514
        O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"]=O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1516
        O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"]=O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1517
        O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"]=O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1518
        O0O00OOOOOOOO0O0O ["产品名称"]=O0O00OOOOOOOO0O0O ["产品名称"].str .replace ("*","※",regex =False )#line:1520
        O0O00OOOOOOOO0O0O ["产品批号"]=O0O00OOOOOOOO0O0O ["产品批号"].str .replace ("(","（",regex =False )#line:1522
        O0O00OOOOOOOO0O0O ["产品批号"]=O0O00OOOOOOOO0O0O ["产品批号"].str .replace (")","）",regex =False )#line:1523
        O0O00OOOOOOOO0O0O ["产品批号"]=O0O00OOOOOOOO0O0O ["产品批号"].str .replace ("*","※",regex =False )#line:1524
        O0O00OOOOOOOO0O0O ['事件发生日期']=pd .to_datetime (O0O00OOOOOOOO0O0O ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1527
        O0O00OOOOOOOO0O0O ["事件发生月份"]=O0O00OOOOOOOO0O0O ["事件发生日期"].dt .to_period ("M").astype (str )#line:1531
        O0O00OOOOOOOO0O0O ["事件发生季度"]=O0O00OOOOOOOO0O0O ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1532
        O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"]=O0O00OOOOOOOO0O0O ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1536
        O0O00OOOOOOOO0O0O ["产品批号"]=O0O00OOOOOOOO0O0O ["产品批号"].fillna ("未填写")#line:1537
        O0O00OOOOOOOO0O0O ["型号"]=O0O00OOOOOOOO0O0O ["型号"].fillna ("未填写")#line:1538
        O0O00OOOOOOOO0O0O ["规格"]=O0O00OOOOOOOO0O0O ["规格"].fillna ("未填写")#line:1539
        return O0O00OOOOOOOO0O0O #line:1541
def thread_it (O0O0OO0O0OOO0OOO0 ,*O0OO0OOO00O000O0O ):#line:1545
    ""#line:1546
    O00OO000OOOO0OO0O =threading .Thread (target =O0O0OO0O0OOO0OOO0 ,args =O0OO0OOO00O000O0O )#line:1548
    O00OO000OOOO0OO0O .setDaemon (True )#line:1550
    O00OO000OOOO0OO0O .start ()#line:1552
def showWelcome ():#line:1555
    ""#line:1556
    O0OO0O00O0OO00O00 =roox .winfo_screenwidth ()#line:1557
    O0O0OO00O0O000000 =roox .winfo_screenheight ()#line:1559
    roox .overrideredirect (True )#line:1561
    roox .attributes ("-alpha",1 )#line:1562
    OO00OOO0OO000OO00 =(O0OO0O00O0OO00O00 -475 )/2 #line:1563
    OO000O000000000O0 =(O0O0OO00O0O000000 -200 )/2 #line:1564
    roox .geometry ("675x140+%d+%d"%(OO00OOO0OO000OO00 ,OO000O000000000O0 ))#line:1566
    roox ["bg"]="royalblue"#line:1567
    OOOO0000O0OO00O00 =Label (roox ,text ="医疗器械警戒趋势分析工具",fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:1570
    OOOO0000O0OO00O00 .place (x =0 ,y =15 ,width =675 ,height =90 )#line:1571
    OO0O0OOOO0O00O000 =Label (roox ,text ="Trend Analysis Tools V"+str (version_now ),fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ),)#line:1578
    OO0O0OOOO0O00O000 .place (x =0 ,y =90 ,width =675 ,height =50 )#line:1579
def closeWelcome ():#line:1582
    ""#line:1583
    for O0OO0OO0O0O000OOO in range (2 ):#line:1584
        root .attributes ("-alpha",0 )#line:1585
        time .sleep (1 )#line:1586
    root .attributes ("-alpha",1 )#line:1587
    roox .destroy ()#line:1588
if __name__ =='__main__':#line:1592
    pass #line:1593
root =Tk ()#line:1594
root .title ("医疗器械警戒趋势分析工具Trend Analysis Tools V"+str (version_now ))#line:1595
sw_root =root .winfo_screenwidth ()#line:1596
sh_root =root .winfo_screenheight ()#line:1598
ww_root =700 #line:1600
wh_root =620 #line:1601
x_root =(sw_root -ww_root )/2 #line:1603
y_root =(sh_root -wh_root )/2 #line:1604
root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:1605
root .configure (bg ="steelblue")#line:1606
try :#line:1609
    frame0 =ttk .Frame (root ,width =100 ,height =20 )#line:1610
    frame0 .pack (side =LEFT )#line:1611
    B_open_files1 =Button (frame0 ,text ="导入原始数据",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,0 ),)#line:1624
    B_open_files1 .pack ()#line:1625
    B_open_files3 =Button (frame0 ,text ="导入分析规则",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_fileopen ,1 ),)#line:1638
    B_open_files3 .pack ()#line:1639
    B_open_files3 =Button (frame0 ,text ="趋势统计分析",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_analysis ,0 ),)#line:1654
    B_open_files3 .pack ()#line:1655
    B_open_files3 =Button (frame0 ,text ="直方图（数量）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"数量"))#line:1668
    B_open_files3 .pack ()#line:1669
    B_open_files3 =Button (frame0 ,text ="直方图（占比）",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tread_TOOLS_bar ,"百分比"))#line:1680
    B_open_files3 .pack ()#line:1681
    B_open_files3 =Button (frame0 ,text ="查看帮助文件",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (helper ))#line:1692
    B_open_files3 .pack ()#line:1693
    B_open_files3 =Button (frame0 ,text ="变更注册状态",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (display_random_number ))#line:1704
    B_open_files3 .pack ()#line:1705
except :#line:1706
    pass #line:1707
text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF",font ="微软雅黑")#line:1711
text .pack ()#line:1712
text .insert (END ,"\n  本程序用于趋势分析,供广东省内参与医疗器械警戒试点的企业免费使用。如您有相关问题或改进建议，请联系以下人员：\n\n    佛山市药品不良反应监测中心\n    蔡权周 \n    微信：18575757461 \n    邮箱：411703730@qq.com")#line:1717
text .insert (END ,"\n\n")#line:1718
def A000 ():#line:1720
    pass #line:1721
setting_cfg =read_setting_cfg ()#line:1725
generate_random_file ()#line:1726
setting_cfg =open_setting_cfg ()#line:1727
if setting_cfg ["settingdir"]==0 :#line:1728
    showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:1729
    filepathu =filedialog .askdirectory ()#line:1730
    path =get_directory_path (filepathu )#line:1731
    update_setting_cfg ("settingdir",path )#line:1732
setting_cfg =open_setting_cfg ()#line:1733
random_number =int (setting_cfg ["sidori"])#line:1734
input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:1735
day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:1736
sid =random_number *2 +183576 #line:1737
if input_number ==sid and day_end =="未过期":#line:1738
    usergroup ="用户组=1"#line:1739
    text .insert (END ,usergroup +"   有效期至：")#line:1740
    text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:1741
text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:1742
roox =Toplevel ()#line:1747
tMain =threading .Thread (target =showWelcome )#line:1748
tMain .start ()#line:1749
t1 =threading .Thread (target =closeWelcome )#line:1750
t1 .start ()#line:1751
root .lift ()#line:1752
root .attributes ("-topmost",True )#line:1753
root .attributes ("-topmost",False )#line:1754
root .mainloop ()#line:1756
