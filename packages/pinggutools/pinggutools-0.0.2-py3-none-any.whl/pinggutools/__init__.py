#!/usr/bin/env python
import warnings #line:10
import traceback #line:11
import re #line:12
import xlrd #line:13
import xlwt #line:14
import openpyxl #line:15
import pandas as pd #line:16
import numpy as np #line:17
import math #line:18
import tkinter as Tk #line:19
from tkinter import ttk #line:20
from tkinter import *#line:21
import tkinter .font as tkFont #line:22
from tkinter import filedialog ,dialog ,PhotoImage #line:23
from tkinter .messagebox import showinfo #line:24
from tkinter .scrolledtext import ScrolledText #line:25
import collections #line:26
from collections import Counter #line:27
import datetime #line:28
from datetime import datetime ,timedelta #line:29
from tkinter import END #line:30
import xlsxwriter #line:31
import os #line:32
import time #line:33
import threading #line:34
import matplotlib as plt #line:35
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:36
from matplotlib .figure import Figure #line:37
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:38
global ori #line:41
global biaozhun #line:42
global dishi #line:43
biaozhun =""#line:44
dishi =""#line:45
ori =0 #line:46
global modex #line:47
modex =""#line:48
import random #line:50
import requests #line:51
global version_now #line:52
global usergroup #line:53
global setting_cfg #line:54
global csdir #line:55
global peizhidir #line:56
version_now ="0.0.2"#line:57
usergroup ="用户组=0"#line:58
setting_cfg =""#line:59
csdir =str (os .path .dirname (__file__ ))#line:60
csdir =csdir +csdir .split ("pinggutools")[0 ][-1 ]#line:61
print (csdir )#line:62
def extract_zip_file (O0OOO0OOO0O000000 ,OOO0OO00O0OOO0OO0 ):#line:70
    import zipfile #line:72
    if OOO0OO00O0OOO0OO0 =="":#line:73
        return 0 #line:74
    with zipfile .ZipFile (O0OOO0OOO0O000000 ,'r')as OO0OO0000O00O0O0O :#line:75
        for OO000O0OOOO0O00O0 in OO0OO0000O00O0O0O .infolist ():#line:76
            OO000O0OOOO0O00O0 .filename =OO000O0OOOO0O00O0 .filename .encode ('cp437').decode ('gbk')#line:78
            OO0OO0000O00O0O0O .extract (OO000O0OOOO0O00O0 ,OOO0OO00O0OOO0OO0 )#line:79
def get_directory_path (OOO0000OO0OO00000 ):#line:85
    global csdir #line:87
    if not (os .path .isfile (os .path .join (OOO0000OO0OO00000 ,'0（范例）质量评估.xls'))):#line:89
        extract_zip_file (csdir +"def.py",OOO0000OO0OO00000 )#line:94
    if OOO0000OO0OO00000 =="":#line:96
        quit ()#line:97
    return OOO0000OO0OO00000 #line:98
def convert_and_compare_dates (O0OOO00OOO00O00O0 ):#line:102
    import datetime #line:103
    OO0OOOO000OO00OOO =datetime .datetime .now ()#line:104
    try :#line:106
       OO0OOO0OO0OOOO0O0 =datetime .datetime .strptime (str (int (int (O0OOO00OOO00O00O0 )/4 )),"%Y%m%d")#line:107
    except :#line:108
        print ("fail")#line:109
        return "已过期"#line:110
    if OO0OOO0OO0OOOO0O0 >OO0OOOO000OO00OOO :#line:112
        return "未过期"#line:114
    else :#line:115
        return "已过期"#line:116
def read_setting_cfg ():#line:118
    global csdir #line:119
    if os .path .exists (csdir +'setting.cfg'):#line:121
        text .insert (END ,"已完成初始化\n")#line:122
        with open (csdir +'setting.cfg','r')as OO0O0000O00OO0000 :#line:123
            O00O0O00OO00O00O0 =eval (OO0O0000O00OO0000 .read ())#line:124
    else :#line:125
        O0000OOO0OO0000O0 =csdir +'setting.cfg'#line:127
        with open (O0000OOO0OO0000O0 ,'w')as OO0O0000O00OO0000 :#line:128
            OO0O0000O00OO0000 .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:129
        text .insert (END ,"未初始化，正在初始化...\n")#line:130
        O00O0O00OO00O00O0 =read_setting_cfg ()#line:131
    return O00O0O00OO00O00O0 #line:132
def open_setting_cfg ():#line:135
    global csdir #line:136
    with open (csdir +"setting.cfg","r")as O00OOO00OOO0OO0O0 :#line:138
        OO0OOO0O000O0O00O =eval (O00OOO00OOO0OO0O0 .read ())#line:140
    return OO0OOO0O000O0O00O #line:141
def update_setting_cfg (O0OO000OOO0OOO0OO ,OO000O0O0O0O0O000 ):#line:143
    global csdir #line:144
    with open (csdir +"setting.cfg","r")as OOOOOO0OO00OOO00O :#line:146
        O0O00O000OOOO0000 =eval (OOOOOO0OO00OOO00O .read ())#line:148
    if O0O00O000OOOO0000 [O0OO000OOO0OOO0OO ]==0 or O0O00O000OOOO0000 [O0OO000OOO0OOO0OO ]=="11111180000808":#line:150
        O0O00O000OOOO0000 [O0OO000OOO0OOO0OO ]=OO000O0O0O0O0O000 #line:151
        with open (csdir +"setting.cfg","w")as OOOOOO0OO00OOO00O :#line:153
            OOOOOO0OO00OOO00O .write (str (O0O00O000OOOO0000 ))#line:154
def generate_random_file ():#line:157
    O0O0000000OOO000O =random .randint (200000 ,299999 )#line:159
    update_setting_cfg ("sidori",O0O0000000OOO000O )#line:161
def display_random_number ():#line:163
    global csdir #line:164
    OO0O0OO0O0O0OO000 =Toplevel ()#line:165
    OO0O0OO0O0O0OO000 .title ("ID")#line:166
    OOO0OOO0O00OO00O0 =OO0O0OO0O0O0OO000 .winfo_screenwidth ()#line:168
    O00000000OO000000 =OO0O0OO0O0O0OO000 .winfo_screenheight ()#line:169
    O0O000000000O0OOO =80 #line:171
    OOO0OO00OO0000OOO =70 #line:172
    O00OO0O0O000O0OO0 =(OOO0OOO0O00OO00O0 -O0O000000000O0OOO )/2 #line:174
    OOO0OO00O0OO0OO0O =(O00000000OO000000 -OOO0OO00OO0000OOO )/2 #line:175
    OO0O0OO0O0O0OO000 .geometry ("%dx%d+%d+%d"%(O0O000000000O0OOO ,OOO0OO00OO0000OOO ,O00OO0O0O000O0OO0 ,OOO0OO00O0OO0OO0O ))#line:176
    with open (csdir +"setting.cfg","r")as O0OOO0O0000O0O00O :#line:179
        O0OOO0O00O0OOO0O0 =eval (O0OOO0O0000O0O00O .read ())#line:181
    OOOOOO0O00OOOO0O0 =int (O0OOO0O00O0OOO0O0 ["sidori"])#line:182
    O000OO00OO0OO0O0O =OOOOOO0O00OOOO0O0 *2 +183576 #line:183
    print (O000OO00OO0OO0O0O )#line:185
    OOOO00OOOO0O00O00 =ttk .Label (OO0O0OO0O0O0OO000 ,text =f"机器码: {OOOOOO0O00OOOO0O0}")#line:187
    OOOO0OOO00O0O0OO0 =ttk .Entry (OO0O0OO0O0O0OO000 )#line:188
    OOOO00OOOO0O00O00 .pack ()#line:191
    OOOO0OOO00O0O0OO0 .pack ()#line:192
    ttk .Button (OO0O0OO0O0O0OO000 ,text ="验证",command =lambda :check_input (OOOO0OOO00O0O0OO0 .get (),O000OO00OO0OO0O0O )).pack ()#line:196
def check_input (O00O0O0OO0OOO0O00 ,O00OOOO0OOOO0O000 ):#line:198
    try :#line:202
        O0000OOO00O0O0OO0 =int (str (O00O0O0OO0OOO0O00 )[0 :6 ])#line:203
        O0000000O0O00OO00 =convert_and_compare_dates (str (O00O0O0OO0OOO0O00 )[6 :14 ])#line:204
    except :#line:205
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:206
        return 0 #line:207
    if O0000OOO00O0O0OO0 ==O00OOOO0OOOO0O000 and O0000000O0O00OO00 =="未过期":#line:209
        update_setting_cfg ("sidfinal",O00O0O0OO0OOO0O00 )#line:210
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:211
        quit ()#line:212
    else :#line:213
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:214
def update_software (OO0OO0O00000000O0 ):#line:218
    global version_now #line:220
    O00OO000OOO0O0OO0 =requests .get (f"https://pypi.org/pypi/{OO0OO0O00000000O0}/json").json ()["info"]["version"]#line:221
    text .insert (END ,"当前版本为："+version_now )#line:222
    if O00OO000OOO0O0OO0 >version_now :#line:223
        text .insert (END ,"\n最新版本为："+O00OO000OOO0O0OO0 +",正在尝试自动更新....")#line:224
        pip .main (['install',OO0OO0O00000000O0 ,'--upgrade'])#line:226
        text .insert (END ,"\n您可以开展工作。")#line:227
def Topentable (O0OO00O00OOOO00OO ):#line:230
    ""#line:231
    global ori #line:232
    global biaozhun #line:233
    global dishi #line:234
    OO0OOO0000O0O0O0O =[]#line:235
    OO0O000000OOO00OO =[]#line:236
    O0OOO000000OOO000 =1 #line:237
    if O0OO00O00OOOO00OO ==123 :#line:240
        try :#line:241
            OOO00O0O0000OO000 =filedialog .askopenfilename (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:244
            biaozhun =pd .read_excel (OOO00O0O0000OO000 ,sheet_name =0 ,header =0 ,index_col =0 ).reset_index ()#line:247
        except :#line:248
            showinfo (title ="提示",message ="配置表文件有误或您没有选择。")#line:249
            return 0 #line:250
        try :#line:251
            dishi =pd .read_excel (OOO00O0O0000OO000 ,sheet_name ="地市清单",header =0 ,index_col =0 ).reset_index ()#line:254
        except :#line:255
            showinfo (title ="提示",message ="您选择的配置文件没有地市列表或您没有选择。")#line:256
            return 0 #line:257
        if ("评分项"in biaozhun .columns and "打分标准"in biaozhun .columns and "专家序号"not in biaozhun .columns ):#line:262
            text .insert (END ,"\n您使用自定义的配置表。")#line:263
            text .see (END )#line:264
            showinfo (title ="提示",message ="您将使用自定义的配置表。")#line:265
            return 0 #line:266
        else :#line:267
            showinfo (title ="提示",message ="配置表文件有误，请正确选择。")#line:268
            biaozhun =""#line:269
            return 0 #line:270
    try :#line:273
        if O0OO00O00OOOO00OO !=1 :#line:274
            O00O00O0OOO0O00OO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:277
        if O0OO00O00OOOO00OO ==1 :#line:278
            O00O00O0OOO0O00OO =filedialog .askopenfilenames (filetypes =[("XLSX",".xlsx"),("XLS",".xls")])#line:281
            for O000O0O00OOO0OOOO in O00O00O0OOO0O00OO :#line:282
                if ("●专家评分表"in O000O0O00OOO0OOOO )and ("●(最终评分需导入)被抽出的所有数据.xls"not in O000O0O00OOO0OOOO ):#line:283
                    OO0OOO0000O0O0O0O .append (O000O0O00OOO0OOOO )#line:284
                elif "●(最终评分需导入)被抽出的所有数据.xls"in O000O0O00OOO0OOOO :#line:285
                    OO0O000000OOO00OO .append (O000O0O00OOO0OOOO )#line:286
                    OOOO000OO0000O000 =O000O0O00OOO0OOOO .replace ("●(最终评分需导入)被抽出的所有数据","分数错误信息")#line:287
                    O0OOO000000OOO000 =0 #line:288
            if O0OOO000000OOO000 ==1 :#line:289
                showinfo (title ="提示",message ="请一并导入以下文件：●(最终评分需导入)被抽出的所有数据.xls")#line:291
                return 0 #line:292
            O00O00O0OOO0O00OO =OO0OOO0000O0O0O0O #line:293
        OO000OOOO0OOO0000 =[pd .read_excel (OO0OO0O0OO000OOOO ,header =0 ,sheet_name =0 )for OO0OO0O0OO000OOOO in O00O00O0OOO0O00OO ]#line:296
        ori =pd .concat (OO000OOOO0OOO0000 ,ignore_index =True ).drop_duplicates ().reset_index (drop =True )#line:297
        if "报告编码"in ori .columns or "报告表编码"in ori .columns :#line:299
            ori =ori .fillna ("-未填写-")#line:300
        if "报告类型-新的"in ori .columns :#line:303
            biaozhun =pd .read_excel (peizhidir +"0（范例）质量评估.xls",sheet_name ="药品",header =0 ,index_col =0 ).reset_index ()#line:306
            ori ["报告编码"]=ori ["报告表编码"]#line:307
            text .insert (END ,"检测到导入的文件为药品报告，正在进行兼容性数据规整，请稍后...")#line:308
            ori =ori .rename (columns ={"医院名称":"单位名称"})#line:309
            ori =ori .rename (columns ={"报告地区名称":"使用单位、经营企业所属监测机构"})#line:310
            ori =ori .rename (columns ={"报告类型-严重程度":"伤害"})#line:311
            ori ["伤害"]=ori ["伤害"].str .replace ("一般","其他",regex =False )#line:312
            ori ["伤害"]=ori ["伤害"].str .replace ("严重","严重伤害",regex =False )#line:313
            ori .loc [(ori ["不良反应结果"]=="死亡"),"伤害"]="死亡"#line:314
            ori ["上报单位所属地区"]=ori ["使用单位、经营企业所属监测机构"]#line:315
            try :#line:316
                ori ["报告编码"]=ori ["唯一标识"]#line:317
            except :#line:318
                pass #line:319
            ori ["药品信息"]=""#line:323
            O0OOO0O0OOO0O0OO0 =0 #line:324
            O0O0O00O0OO0OO00O =len (ori ["报告编码"].drop_duplicates ())#line:325
            for OOOOOOOOO0OOOO0O0 in ori ["报告编码"].drop_duplicates ():#line:326
                O0OOO0O0OOO0O0OO0 =O0OOO0O0OOO0O0OO0 +1 #line:327
                OO00OOO0O00O00OOO =round (O0OOO0O0OOO0O0OO0 /O0O0O00O0OO0OO00O ,2 )#line:328
                try :#line:329
                    change_schedule (O0OOO0O0OOO0O0OO0 ,O0O0O00O0OO0OO00O )#line:330
                except :#line:331
                    if OO00OOO0O00O00OOO in [0.10 ,0.20 ,0.30 ,0.40 ,0.50 ,0.60 ,0.70 ,0.80 ,0.90 ,0.99 ]:#line:332
                        text .insert (END ,OO00OOO0O00O00OOO )#line:333
                        text .insert (END ,"...")#line:334
                O0OOO000000OO0000 =ori [(ori ["报告编码"]==OOOOOOOOO0OOOO0O0 )].sort_values (by =["药品序号"]).reset_index ()#line:336
                for OOO0OOOO0O00OO0O0 ,O0OOO0OO0OOOOOO00 in O0OOO000000OO0000 .iterrows ():#line:337
                    ori .loc [(ori ["报告编码"]==O0OOO0OO0OOOOOO00 ["报告编码"]),"药品信息"]=ori ["药品信息"]+"●药品序号："+str (O0OOO0OO0OOOOOO00 ["药品序号"])+" 性质："+str (O0OOO0OO0OOOOOO00 ["怀疑/并用"])+"\n批准文号:"+str (O0OOO0OO0OOOOOO00 ["批准文号"])+"\n商品名称："+str (O0OOO0OO0OOOOOO00 ["商品名称"])+"\n通用名称："+str (O0OOO0OO0OOOOOO00 ["通用名称"])+"\n剂型："+str (O0OOO0OO0OOOOOO00 ["剂型"])+"\n生产厂家："+str (O0OOO0OO0OOOOOO00 ["生产厂家"])+"\n生产批号："+str (O0OOO0OO0OOOOOO00 ["生产批号"])+"\n用量："+str (O0OOO0OO0OOOOOO00 ["用量"])+str (O0OOO0OO0OOOOOO00 ["用量单位"])+"，"+str (O0OOO0OO0OOOOOO00 ["用法-日"])+"日"+str (O0OOO0OO0OOOOOO00 ["用法-次"])+"次\n给药途径:"+str (O0OOO0OO0OOOOOO00 ["给药途径"])+"\n用药开始时间："+str (O0OOO0OO0OOOOOO00 ["用药开始时间"])+"\n用药终止时间："+str (O0OOO0OO0OOOOOO00 ["用药终止时间"])+"\n用药原因："+str (O0OOO0OO0OOOOOO00 ["用药原因"])+"\n"#line:338
            ori =ori .drop_duplicates ("报告编码")#line:339
        if "皮损部位"in ori .columns :#line:346
            biaozhun =pd .read_excel (peizhidir +"0（范例）质量评估.xls",sheet_name ="化妆品",header =0 ,index_col =0 ).reset_index ()#line:349
            ori ["报告编码"]=ori ["报告表编号"]#line:350
            text .insert (END ,"检测到导入的文件为化妆品报告，正在进行兼容性数据规整，请稍后...")#line:351
            ori ["报告地区名称"]=ori ["报告单位名称"].astype (str )#line:353
            ori ["单位名称"]=ori ["报告单位名称"].astype (str )#line:355
            ori ["伤害"]=ori ["报告类型"].astype (str )#line:356
            ori ["伤害"]=ori ["伤害"].str .replace ("一般","其他",regex =False )#line:357
            ori ["伤害"]=ori ["伤害"].str .replace ("严重","严重伤害",regex =False )#line:358
            ori ["上报单位所属地区"]=ori ["报告地区名称"]#line:360
            try :#line:361
                ori ["报告编码"]=ori ["唯一标识"]#line:362
            except :#line:363
                pass #line:364
            text .insert (END ,"\n正在开展化妆品注册单位规整...")#line:365
            OOO00O0OO0O0OO0OO =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="机构列表",header =0 ,index_col =0 ,).reset_index ()#line:366
            for OOO0OOOO0O00OO0O0 ,O0OOO0OO0OOOOOO00 in OOO00O0OO0O0OO0OO .iterrows ():#line:368
                ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["中文全称"]),"监测机构"]=O0OOO0OO0OOOOOO00 ["归属地区"]#line:369
                ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["中文全称"]),"市级监测机构"]=O0OOO0OO0OOOOOO00 ["地市"]#line:370
            ori ["监测机构"]=ori ["监测机构"].fillna ("未规整")#line:371
            ori ["市级监测机构"]=ori ["市级监测机构"].fillna ("未规整")#line:372
        try :#line:375
                text .insert (END ,"\n开展报告单位和监测机构名称规整...")#line:376
                O0OO000OOO0000O00 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:377
                OOO00O0OO0O0OO0OO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:378
                O0OOOO0000OOO0O00 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="地市清单",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:379
                for OOO0OOOO0O00OO0O0 ,O0OOO0OO0OOOOOO00 in O0OO000OOO0000O00 .iterrows ():#line:380
                        ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["曾用名1"]),"单位名称"]=O0OOO0OO0OOOOOO00 ["单位名称"]#line:381
                        ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["曾用名2"]),"单位名称"]=O0OOO0OO0OOOOOO00 ["单位名称"]#line:382
                        ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["曾用名3"]),"单位名称"]=O0OOO0OO0OOOOOO00 ["单位名称"]#line:383
                        ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["曾用名4"]),"单位名称"]=O0OOO0OO0OOOOOO00 ["单位名称"]#line:384
                        ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["曾用名5"]),"单位名称"]=O0OOO0OO0OOOOOO00 ["单位名称"]#line:385
                        ori .loc [(ori ["单位名称"]==O0OOO0OO0OOOOOO00 ["单位名称"]),"使用单位、经营企业所属监测机构"]=O0OOO0OO0OOOOOO00 ["监测机构"]#line:388
                for OOO0OOOO0O00OO0O0 ,O0OOO0OO0OOOOOO00 in OOO00O0OO0O0OO0OO .iterrows ():#line:390
                        ori .loc [(ori ["使用单位、经营企业所属监测机构"]==O0OOO0OO0OOOOOO00 ["曾用名1"]),"使用单位、经营企业所属监测机构"]=O0OOO0OO0OOOOOO00 ["监测机构"]#line:391
                        ori .loc [(ori ["使用单位、经营企业所属监测机构"]==O0OOO0OO0OOOOOO00 ["曾用名2"]),"使用单位、经营企业所属监测机构"]=O0OOO0OO0OOOOOO00 ["监测机构"]#line:392
                        ori .loc [(ori ["使用单位、经营企业所属监测机构"]==O0OOO0OO0OOOOOO00 ["曾用名3"]),"使用单位、经营企业所属监测机构"]=O0OOO0OO0OOOOOO00 ["监测机构"]#line:393
                for OO00OO0000O00O000 in O0OOOO0000OOO0O00 ["地市列表"]:#line:395
                        ori .loc [(ori ["上报单位所属地区"].str .contains (OO00OO0000O00O000 ,na =False )),"市级监测机构"]=OO00OO0000O00O000 #line:396
                ori .loc [(ori ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构"]="佛山"#line:397
        except :#line:399
                text .insert (END ,"\n报告单位和监测机构名称规整失败.")#line:400
    except :#line:402
        showinfo (title ="提示",message ="导入文件错误,请重试。")#line:403
        return 0 #line:404
    try :#line:407
        ori =ori .loc [:,~ori .columns .str .contains ("Unnamed")]#line:408
    except :#line:409
        pass #line:410
    try :#line:411
        ori ["报告编码"]=ori ["报告编码"].astype (str )#line:412
    except :#line:413
        pass #line:414
    ori =ori .sample (frac =1 ).copy ()#line:417
    ori .reset_index (inplace =True )#line:418
    text .insert (END ,"\n数据读取成功，行数："+str (len (ori )))#line:419
    text .see (END )#line:420
    if O0OO00O00OOOO00OO ==0 :#line:423
        if "报告编码"not in ori .columns :#line:424
            showinfo (title ="提示信息",message ="\n在校验过程中，发现您导入的并非原始报告数据，请重新导入。")#line:425
        else :#line:426
            showinfo (title ="提示信息",message ="\n数据读取成功。")#line:427
        return 0 #line:428
    O0O00OOOOO000OO00 =ori .copy ()#line:431
    O0000OOO00O0O0000 ={}#line:432
    O0000O0OOO0OOOOO0 =0 #line:433
    if "专家序号"not in O0O00OOOOO000OO00 .columns :#line:434
        showinfo (title ="提示信息",message ="您导入的并非专家评分文件，请重新导入。")#line:435
        return 0 #line:436
    for OOO0OOOO0O00OO0O0 ,O0OOO0OO0OOOOOO00 in O0O00OOOOO000OO00 .iterrows ():#line:437
        OO0O0O0O0OO000000 ="专家打分-"+str (O0OOO0OO0OOOOOO00 ["条目"])#line:438
        try :#line:439
            float (O0OOO0OO0OOOOOO00 ["评分"])#line:440
            float (O0OOO0OO0OOOOOO00 ["满分"])#line:441
        except :#line:442
            showinfo (title ="错误提示",message ="因专家评分或满分值输入的不是数字，导致了程序中止，请修正："+"专家序号："+str (int (O0OOO0OO0OOOOOO00 ["专家序号"]))+"，报告序号："+str (int (O0OOO0OO0OOOOOO00 ["序号"]))+O0OOO0OO0OOOOOO00 ["条目"],)#line:451
            ori =0 #line:452
        if float (O0OOO0OO0OOOOOO00 ["评分"])>float (O0OOO0OO0OOOOOO00 ["满分"])or float (O0OOO0OO0OOOOOO00 ["评分"])<0 :#line:453
            O0000OOO00O0O0000 [str (OOO0OOOO0O00OO0O0 )]=("专家序号："+str (int (O0OOO0OO0OOOOOO00 ["专家序号"]))+"；  报告序号："+str (int (O0OOO0OO0OOOOOO00 ["序号"]))+O0OOO0OO0OOOOOO00 ["条目"])#line:460
            O0000O0OOO0OOOOO0 =1 #line:461
    if O0000O0OOO0OOOOO0 ==1 :#line:463
        OOO0OO00O0O000OO0 =pd .DataFrame (list (O0000OOO00O0O0000 .items ()),columns =["错误编号","错误信息"])#line:464
        del OOO0OO00O0O000OO0 ["错误编号"]#line:465
        O00O000OO0O00O00O =OOOO000OO0000O000 #line:466
        OOO0OO00O0O000OO0 =OOO0OO00O0O000OO0 .sort_values (by =["错误信息"],ascending =True ,na_position ="last")#line:467
        OOOOOOOO000O0O0OO =pd .ExcelWriter (O00O000OO0O00O00O )#line:468
        OOO0OO00O0O000OO0 .to_excel (OOOOOOOO000O0O0OO ,sheet_name ="字典数据")#line:469
        OOOOOOOO000O0O0OO .close ()#line:470
        showinfo (title ="警告",message ="经检查，部分专家的打分存在错误。请您修正错误的打分文件再重新导入全部的专家打分文件。详见:分数错误信息.xls",)#line:474
        text .insert (END ,"\n经检查，部分专家的打分存在错误。详见:分数错误信息.xls。请您修正错误的打分文件再重新导入全部的专家打分文件。")#line:475
        text .insert (END ,"\n以下是错误信息概况：\n")#line:476
        text .insert (END ,OOO0OO00O0O000OO0 )#line:477
        text .see (END )#line:478
        return 0 #line:479
    if O0OO00O00OOOO00OO ==1 :#line:482
        return ori ,OO0O000000OOO00OO #line:483
def Tchouyang (O000OO00OO0000OOO ):#line:486
    ""#line:487
    try :#line:489
        if O000OO00OO0000OOO ==0 :#line:490
            showinfo (title ="提示",message ="您尚未导入原始数据。")#line:491
            return 0 #line:492
    except :#line:493
        pass #line:494
    if "详细描述"in O000OO00OO0000OOO .columns :#line:495
        showinfo (title ="提示",message ="目前工作文件为专家评分文件，请导入原始数据进行抽样。")#line:496
        return 0 #line:497
    OO000OOO0O00O00OO =Toplevel ()#line:500
    OO000OOO0O00O00OO .title ("随机抽样及随机分组")#line:501
    O0O0O00OO00OOO00O =OO000OOO0O00O00OO .winfo_screenwidth ()#line:502
    OOO0OO00O0O00OOOO =OO000OOO0O00O00OO .winfo_screenheight ()#line:504
    O00OOO0OO0O0O0000 =300 #line:506
    OO0OOO00O00000OOO =220 #line:507
    O00000OO0000O0000 =(O0O0O00OO00OOO00O -O00OOO0OO0O0O0000 )/1.7 #line:509
    O000O0O0OO0OOO000 =(OOO0OO00O0O00OOOO -OO0OOO00O00000OOO )/2 #line:510
    OO000OOO0O00O00OO .geometry ("%dx%d+%d+%d"%(O00OOO0OO0O0O0000 ,OO0OOO00O00000OOO ,O00000OO0000O0000 ,O000O0O0OO0OOO000 ))#line:511
    OO0OOOO0OOO00OO00 =Label (OO000OOO0O00O00OO ,text ="评估对象：")#line:513
    OO0OOOO0OOO00OO00 .grid (row =1 ,column =0 ,sticky ="w")#line:514
    O00O000000OOOOO0O =StringVar ()#line:515
    O00O0O00OO00OO0O0 =ttk .Combobox (OO000OOO0O00O00OO ,width =25 ,height =10 ,state ="readonly",textvariable =O00O000000OOOOO0O )#line:518
    O00O0O00OO00OO0O0 ["values"]=["上报单位","县区","地市","省级审核人","上市许可持有人"]#line:519
    O00O0O00OO00OO0O0 .current (0 )#line:520
    O00O0O00OO00OO0O0 .grid (row =2 ,column =0 )#line:521
    OO000000OO0O0O00O =Label (OO000OOO0O00O00OO ,text ="-----------------------------------------")#line:523
    OO000000OO0O0O00O .grid (row =3 ,column =0 ,sticky ="w")#line:524
    O0O0000000O0OO0OO =Label (OO000OOO0O00O00OO ,text ="死亡报告抽样数量（>1)或比例(<=1)：")#line:526
    O0O0000000O0OO0OO .grid (row =4 ,column =0 ,sticky ="w")#line:527
    OO0OO0OO000O00000 =Entry (OO000OOO0O00O00OO ,width =10 )#line:528
    OO0OO0OO000O00000 .grid (row =4 ,column =1 ,sticky ="w")#line:529
    O0OOO0O00O0OOO0OO =Label (OO000OOO0O00O00OO ,text ="严重报告抽样数量（>1)或比例(<=1)：")#line:531
    O0OOO0O00O0OOO0OO .grid (row =6 ,column =0 ,sticky ="w")#line:532
    OO0O0000O00O000OO =Entry (OO000OOO0O00O00OO ,width =10 )#line:533
    OO0O0000O00O000OO .grid (row =6 ,column =1 ,sticky ="w")#line:534
    OO00OOO0O00OOOO00 =Label (OO000OOO0O00O00OO ,text ="一般报告抽样数量（>1)或比例(<=1)：")#line:536
    OO00OOO0O00OOOO00 .grid (row =8 ,column =0 ,sticky ="w")#line:537
    OOO0OOOOO0OOOO0OO =Entry (OO000OOO0O00O00OO ,width =10 )#line:538
    OOO0OOOOO0OOOO0OO .grid (row =8 ,column =1 ,sticky ="w")#line:539
    OO000000OO0O0O00O =Label (OO000OOO0O00O00OO ,text ="-----------------------------------------")#line:541
    OO000000OO0O0O00O .grid (row =9 ,column =0 ,sticky ="w")#line:542
    OOOO0O0O00OOOOOO0 =Label (OO000OOO0O00O00OO ,text ="抽样后随机分组数（专家数量）：")#line:544
    OOOOOO0O0OOOO0OOO =Entry (OO000OOO0O00O00OO ,width =10 )#line:545
    OOOO0O0O00OOOOOO0 .grid (row =10 ,column =0 ,sticky ="w")#line:546
    OOOOOO0O0OOOO0OOO .grid (row =10 ,column =1 ,sticky ="w")#line:547
    O0OOOO00OO0O00O0O =Button (OO000OOO0O00O00OO ,text ="最大覆盖",width =12 ,command =lambda :thread_it (Tdoing0 ,O000OO00OO0000OOO ,OOO0OOOOO0OOOO0OO .get (),OO0O0000O00O000OO .get (),OO0OO0OO000O00000 .get (),OOOOOO0O0OOOO0OOO .get (),O00O0O00OO00OO0O0 .get (),"最大覆盖",1 ,),)#line:564
    O0OOOO00OO0O00O0O .grid (row =13 ,column =1 ,sticky ="w")#line:565
    O000O0O00000OO0OO =Button (OO000OOO0O00O00OO ,text ="总体随机",width =12 ,command =lambda :thread_it (Tdoing0 ,O000OO00OO0000OOO ,OOO0OOOOO0OOOO0OO .get (),OO0O0000O00O000OO .get (),OO0OO0OO000O00000 .get (),OOOOOO0O0OOOO0OOO .get (),O00O0O00OO00OO0O0 .get (),"总体随机",1 ))#line:566
    O000O0O00000OO0OO .grid (row =13 ,column =0 ,sticky ='w')#line:567
def Tdoing0 (O0OO0OO00O0O0OO0O ,OOOO0OO000O0000O0 ,OO0OO0O0O0OOOO000 ,OOOOOO0OOOO0000OO ,O0O0OOOOO00O0O0OO ,OO00000O0OOO00O0O ,O0O0O00000O0O0O0O ,O0OO0OO0OO0O00O0O ):#line:573
    ""#line:574
    global dishi #line:575
    global biaozhun #line:576
    if (OOOO0OO000O0000O0 ==""or OO0OO0O0O0OOOO000 ==""or OOOOOO0OOOO0000OO ==""or O0O0OOOOO00O0O0OO ==""or OO00000O0OOO00O0O ==""or O0O0O00000O0O0O0O ==""):#line:586
        showinfo (title ="提示信息",message ="参数设置不完整。")#line:587
        return 0 #line:588
    if OO00000O0OOO00O0O =="上报单位":#line:589
        OO00000O0OOO00O0O ="单位名称"#line:590
    if OO00000O0OOO00O0O =="县区":#line:591
        OO00000O0OOO00O0O ="使用单位、经营企业所属监测机构"#line:592
    if OO00000O0OOO00O0O =="地市":#line:593
        OO00000O0OOO00O0O ="市级监测机构"#line:594
    if OO00000O0OOO00O0O =="省级审核人":#line:595
        OO00000O0OOO00O0O ="审核人.1"#line:596
        O0OO0OO00O0O0OO0O ["modex"]=1 #line:597
        O0OO0OO00O0O0OO0O ["审核人.1"]=O0OO0OO00O0O0OO0O ["审核人.1"].fillna ("未填写")#line:598
    if OO00000O0OOO00O0O =="上市许可持有人":#line:599
        OO00000O0OOO00O0O ="上市许可持有人名称"#line:600
        O0OO0OO00O0O0OO0O ["modex"]=1 #line:601
        O0OO0OO00O0O0OO0O ["上市许可持有人名称"]=O0OO0OO00O0O0OO0O ["上市许可持有人名称"].fillna ("未填写")#line:602
    if O0OO0OO0OO0O00O0O ==1 :#line:604
        if len (biaozhun )==0 :#line:605
            OOOO0O0O0OOOOOO00 =peizhidir +"0（范例）质量评估.xls"#line:606
            try :#line:607
                if "modex"in O0OO0OO00O0O0OO0O .columns :#line:608
                    O00O0O0O00O0O0000 =pd .read_excel (OOOO0O0O0OOOOOO00 ,sheet_name ="器械持有人",header =0 ,index_col =0 ).reset_index ()#line:609
                else :#line:610
                    O00O0O0O00O0O0000 =pd .read_excel (OOOO0O0O0OOOOOO00 ,sheet_name =0 ,header =0 ,index_col =0 ).reset_index ()#line:611
                text .insert (END ,"\n您使用配置表文件夹中的“0（范例）质量评估.xls“作为评分标准。")#line:612
                text .see (END )#line:613
            except :#line:616
                O00O0O0O00O0O0000 =pd .DataFrame ({"评分项":{0 :"识别代码",1 :"报告人",2 :"联系人",3 :"联系电话",4 :"注册证编号/曾用注册证编号",5 :"产品名称",6 :"型号和规格",7 :"产品批号和产品编号",8 :"生产日期",9 :"有效期至",10 :"事件发生日期",11 :"发现或获知日期",12 :"伤害",13 :"伤害表现",14 :"器械故障表现",15 :"年龄和年龄类型",16 :"性别",17 :"预期治疗疾病或作用",18 :"器械使用日期",19 :"使用场所和场所名称",20 :"使用过程",21 :"合并用药/械情况说明",22 :"事件原因分析和事件原因分析描述",23 :"初步处置情况",},"打分标准":{0 :"",1 :"填写人名或XX科室，得1分",2 :"填写报告填报人员姓名或XX科X医生，得1分",3 :"填写报告填报人员移动电话或所在科室固定电话，得1分",4 :"可利用国家局数据库检索，注册证号与产品名称及事件描述相匹配的，得8分",5 :"可利用国家局数据库检索，注册证号与产品名称及事件描述相匹配的，得4分",6 :"规格和型号任填其一，且内容正确，得4分",7 :"产品批号和编号任填其一，且内容正确，,得4分。\n注意：（1）如果该器械使用年限久远，或在院外用械，批号或编号无法查询追溯的，报告表“使用过程”中给予说明的，得4分；（2）出现YZB格式、YY格式、GB格式等产品标准格式，或“XX生产许XX”等许可证号，得0分；（3）出现和注册证号一样的数字，得0分。",8 :"确保“生产日期”和“有效期至”逻辑正确，“有效期至”晚于“生产日期”，且两者时间间隔应为整月或整年，得2分。",9 :"确保生产日期和有效期逻辑正确。\n注意：如果该器械是使用年限久远的（2014年之前生产产品），或在院外用械，生产日期和有效期无法查询追溯的，并在报告表“使用过程”中给予说明的，该项得4分",10 :"指发生医疗器械不良事件的日期，应与使用过程描述一致，如仅知道事件发生年份，填写当年的1月1日；如仅知道年份和月份，填写当月的第1日；如年月日均未知，填写事件获知日期，并在“使用过程”给予说明。填写正确得2分。\n注意：“事件发生日期”早于“器械使用日期”的，得0分。",11 :"指报告单位发现或知悉该不良事件的日期，填写正确得5分。\n注意：“发现或获知日期”早于“事件发生日期”的，或者早于使用日期的，得0分。",12 :"分为“死亡”、“严重伤害”“其他”，判断正确，得8分。",13 :"描述准确且简明，或者勾选的术语贴切的，得6分；描述较为准确且简明，或选择术语较为贴切，或描述准确但不够简洁，得3分；描述冗长、填成器械故障表现的，得0分。\n注意：对于“严重伤害”事件，需写明实际导致的严重伤害，填写不恰当的或填写“无”的，得0分。伤害表现描述与使用过程中关于伤害的描述不一致的，得0分。对于“其他”未对患者造成伤害的，该项可填“无”或未填写，默认得6分。",14 :"描述准确而简明，或者勾选的术语贴切的，得6分；描述较为准确，或选择术语较为贴切，或描述准确但不够简洁，得3分；描述冗长、填成伤害表现的，得0分。故障表现与使用过程中关于器械故障的描述不一致的，得0分。\n注意：对于不存在器械故障但仍然对患者造成了伤害的，在伤害表现处填写了对应伤害，该项填“无”，默认得6分。",15 :"医疗器械若未用于患者或者未造成患者伤害的，患者信息非必填项，默认得1分。",16 :"医疗器械若未用于患者或者未造成患者伤害的，患者信息非必填项，默认得1分。",17 :"指涉及医疗器械的用途或适用范围，如治疗类医疗器械的预期治疗疾病，检验检查类、辅助治疗类医疗器械的预期作用等。填写完整准确，得4分；未填写、填写不完整或填写错误，得0分。",18 :"需与使用过程描述的日期一致，若器械使用日期和不良事件发生日期不是同一天，填成“不良事件发生日期”的，得0分；填成“有源设备启用日期”的，得0分。如仅知道事件使用年份，填写当年的1月1日；如仅知道年份和月份，填写当月的第1日；如年月日均未知，填写事件获知日期，并在“使用过程”给予说明。",19 :"使用场所为“医疗机构”的，场所名称可以为空，默认得2分；使用场所为“家庭”或“其他”，但勾选为医疗机构的，得0分；如使用场所为“其他”，没有填写实际使用场所或填写错误的，得0分。",20 :"按照以下四个要素进行评分：\n（1）具体操作使用情况（5分）\n详细描述具体操作人员资质、操作使用过程等信息，对于体外诊断医疗器械应填写患者诊疗信息（如疾病情况、用药情况）、样品检测过程与结果等信息。该要素描述准确完整的，得5分；较完整准确的，得2.5分；要素缺失的，得0分。\n（2）不良事件情况（5分）\n详细描述使用过程中出现的非预期结果等信息，对于体外诊断医疗器械应填写发现的异常检测情况，该要素描述完整准确的，得5分；较完整准确的，得2.5分；要素缺失的，得0分。\n（3）对受害者的影响（4分）\n详细描述该事件（可能）对患者造成的伤害，（可能）对临床诊疗造成的影响。有实际伤害的事件，需写明对受害者的伤害情况，包括必要的体征（如体温、脉搏、血压、皮损程度、失血情况等）和相关检查结果（如血小板检查结果）；对于可能造成严重伤害的事件，需写明可能对患者或其他人员造成的伤害。该要素描述完整准确的，得4分；较完整准确的，得2分；要素缺失的，得0分。\n（4）采取的治疗措施及结果（4分）\n有实际伤害的情况，须写明对伤者采取的治疗措施（包括用药、用械、或手术治疗等，及采取各个治疗的时间），以及采取治疗措施后的转归情况。该要素描述完整准确得4分，较完整准确得2分，描述过于笼统简单，如描述为“对症治疗”、“报告医生”、“转院”等，或者要素缺失的，得0分；无实际伤害的，该要素默认得4分。",21 :"有合并用药/械情况但没有填写此项的，得0分；填写不完整的，得2分；评估认为该不良事件过程中不存在合并用药/械情况的，该项不填写可得4分。\n如：输液泵泵速不准，合并用药/械情况应写明输注的药液、并用的输液器信息等。",22 :"原因分析不正确，如对于产品原因（包括说明书等）、操作原因 、患者自身原因 、无法确定的勾选与原因分析的描述的内容不匹配的，得0分，例如勾选了产品原因，但描述中说明该事件可能是未按照说明书要求进行操作导致（操作原因）；原因分析正确，但原因分析描述填成使用过程或者处置方式的，得2分。",23 :"包含产品的初步处置措施和对患者的救治措施等，填写完整得2分，部分完整得1分，填写过于简单得0分。",},"满分分值":{0 :0 ,1 :1 ,2 :1 ,3 :1 ,4 :8 ,5 :4 ,6 :4 ,7 :4 ,8 :2 ,9 :2 ,10 :2 ,11 :5 ,12 :8 ,13 :6 ,14 :6 ,15 :1 ,16 :1 ,17 :4 ,18 :2 ,19 :2 ,20 :18 ,21 :4 ,22 :4 ,23 :2 ,},})#line:698
                text .insert (END ,"\n您使用软件内置的评分标准。")#line:699
                text .see (END )#line:700
            try :#line:702
                dishi =pd .read_excel (OOOO0O0O0OOOOOO00 ,sheet_name ="地市清单",header =0 ,index_col =0 ).reset_index ()#line:705
                text .insert (END ,"\n找到地市清单，将规整地市名称。")#line:706
                for OOOO0O0O00OO000O0 in dishi ["地市列表"]:#line:707
                    O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["上报单位所属地区"].str .contains (OOOO0O0O00OO000O0 ,na =False )),"市级监测机构",]=OOOO0O0O00OO000O0 #line:711
                    O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构",]="佛山"#line:715
                    O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["市级监测机构"].str .contains ("北海",na =False )),"市级监测机构",]="北海"#line:722
                    O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["联系地址"].str .contains ("北海市",na =False )),"市级监测机构",]="北海"#line:726
                text .see (END )#line:727
            except :#line:728
                text .insert (END ,"\n未找到地市清单或清单有误，不对地市名称进行规整，未维护产品的报表的地市名称将以“未填写”的形式展现。")#line:729
                text .see (END )#line:730
        else :#line:731
            O00O0O0O00O0O0000 =biaozhun .copy ()#line:732
            if len (dishi )!=0 :#line:733
                try :#line:734
                    text .insert (END ,"\n找到自定义的地市清单，将规整地市名称。")#line:735
                    for OOOO0O0O00OO000O0 in dishi ["地市列表"]:#line:736
                        O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["使用单位、经营企业所属监测机构"].str .contains (OOOO0O0O00OO000O0 ,na =False )),"市级监测机构",]=OOOO0O0O00OO000O0 #line:740
                    O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构",]="佛山"#line:744
                    text .see (END )#line:745
                except TRD :#line:746
                    text .insert (END ,"\n导入的自定义配置表中，未找到地市清单或清单有误，不对地市名称进行规整，未维护产品的报表的地市名称将以“未填写”的形式展现。",)#line:750
                    text .see (END )#line:751
            text .insert (END ,"\n您使用了自己导入的配置表作为评分标准。")#line:752
            text .see (END )#line:753
    text .insert (END ,"\n正在抽样，请稍候...已完成30%")#line:754
    O0OO0OO00O0O0OO0O =O0OO0OO00O0O0OO0O .reset_index (drop =True )#line:755
    O0OO0OO00O0O0OO0O ["质量评估模式"]=O0OO0OO00O0O0OO0O [OO00000O0OOO00O0O ]#line:758
    O0OO0OO00O0O0OO0O ["报告时限"]=""#line:759
    O0OO0OO00O0O0OO0O ["报告时限情况"]="超时报告"#line:760
    O0OO0OO00O0O0OO0O ["识别代码"]=range (0 ,len (O0OO0OO00O0O0OO0O ))#line:761
    try :#line:762
        O0OO0OO00O0O0OO0O ["报告时限"]=pd .to_datetime (O0OO0OO00O0O0OO0O ["报告日期"])-pd .to_datetime (O0OO0OO00O0O0OO0O ["发现或获知日期"])#line:765
        O0OO0OO00O0O0OO0O ["报告时限"]=O0OO0OO00O0O0OO0O ["报告时限"].dt .days #line:766
        O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["伤害"]=="死亡")&(O0OO0OO00O0O0OO0O ["报告时限"]<=7 ),"报告时限情况"]="死亡未超时，报告时限："+O0OO0OO00O0O0OO0O ["报告时限"].astype (str )#line:769
        O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["伤害"]=="严重伤害")&(O0OO0OO00O0O0OO0O ["报告时限"]<=20 ),"报告时限情况"]="严重伤害未超时，报告时限："+O0OO0OO00O0O0OO0O ["报告时限"].astype (str )#line:772
        O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["伤害"]=="其他")&(O0OO0OO00O0O0OO0O ["报告时限"]<=30 ),"报告时限情况"]="其他未超时，报告时限："+O0OO0OO00O0O0OO0O ["报告时限"].astype (str )#line:775
        O0OO0OO00O0O0OO0O .loc [(O0OO0OO00O0O0OO0O ["报告时限情况"]=="超时报告"),"报告时限情况"]="！疑似超时报告，报告时限："+O0OO0OO00O0O0OO0O ["报告时限"].astype (str )#line:778
        O0OO0OO00O0O0OO0O ["型号和规格"]=("型号："+O0OO0OO00O0O0OO0O ["型号"].astype (str )+"   \n规格："+O0OO0OO00O0O0OO0O ["规格"].astype (str ))#line:781
        O0OO0OO00O0O0OO0O ["产品批号和产品编号"]=("产品批号："+O0OO0OO00O0O0OO0O ["产品批号"].astype (str )+"   \n产品编号："+O0OO0OO00O0O0OO0O ["产品编号"].astype (str ))#line:787
        O0OO0OO00O0O0OO0O ["使用场所和场所名称"]=("使用场所："+O0OO0OO00O0O0OO0O ["使用场所"].astype (str )+"   \n场所名称："+O0OO0OO00O0O0OO0O ["场所名称"].astype (str ))#line:793
        O0OO0OO00O0O0OO0O ["年龄和年龄类型"]=("年龄："+O0OO0OO00O0O0OO0O ["年龄"].astype (str )+"   \n年龄类型："+O0OO0OO00O0O0OO0O ["年龄类型"].astype (str ))#line:799
        O0OO0OO00O0O0OO0O ["事件原因分析和事件原因分析描述"]=("事件原因分析："+O0OO0OO00O0O0OO0O ["事件原因分析"].astype (str )+"   \n事件原因分析描述："+O0OO0OO00O0O0OO0O ["事件原因分析描述"].astype (str ))#line:805
        O0OO0OO00O0O0OO0O ["是否开展了调查及调查情况"]=("是否开展了调查："+O0OO0OO00O0O0OO0O ["是否开展了调查"].astype (str )+"   \n调查情况："+O0OO0OO00O0O0OO0O ["调查情况"].astype (str ))#line:814
        O0OO0OO00O0O0OO0O ["控制措施情况"]=("是否已采取控制措施："+O0OO0OO00O0O0OO0O ["是否已采取控制措施"].astype (str )+"   \n具体控制措施："+O0OO0OO00O0O0OO0O ["具体控制措施"].astype (str )+"   \n未采取控制措施原因："+O0OO0OO00O0O0OO0O ["未采取控制措施原因"].astype (str ))#line:823
        O0OO0OO00O0O0OO0O ["是否为错报误报报告及错报误报说明"]=("是否为错报误报报告："+O0OO0OO00O0O0OO0O ["是否为错报误报报告"].astype (str )+"   \n错报误报说明："+O0OO0OO00O0O0OO0O ["错报误报说明"].astype (str ))#line:830
        O0OO0OO00O0O0OO0O ["是否合并报告及合并报告编码"]=("是否合并报告："+O0OO0OO00O0O0OO0O ["是否合并报告"].astype (str )+"   \n合并报告编码："+O0OO0OO00O0O0OO0O ["合并报告编码"].astype (str ))#line:837
    except :#line:838
        pass #line:839
    if "报告类型-新的"in O0OO0OO00O0O0OO0O .columns :#line:840
        O0OO0OO00O0O0OO0O ["报告时限"]=pd .to_datetime (O0OO0OO00O0O0OO0O ["报告日期"].astype (str ))-pd .to_datetime (O0OO0OO00O0O0OO0O ["不良反应发生时间"].astype (str ))#line:842
        O0OO0OO00O0O0OO0O ["报告类型"]=O0OO0OO00O0O0OO0O ["报告类型-新的"].astype (str )+O0OO0OO00O0O0OO0O ["伤害"].astype (str )+"    "+O0OO0OO00O0O0OO0O ["严重药品不良反应"].astype (str )#line:843
        O0OO0OO00O0O0OO0O ["报告类型"]=O0OO0OO00O0O0OO0O ["报告类型"].str .replace ("-未填写-","",regex =False )#line:844
        O0OO0OO00O0O0OO0O ["报告类型"]=O0OO0OO00O0O0OO0O ["报告类型"].str .replace ("其他","一般",regex =False )#line:845
        O0OO0OO00O0O0OO0O ["报告类型"]=O0OO0OO00O0O0OO0O ["报告类型"].str .replace ("严重伤害","严重",regex =False )#line:846
        O0OO0OO00O0O0OO0O ["关联性评价和ADR分析"]="停药减药后反应是否减轻或消失："+O0OO0OO00O0O0OO0O ["停药减药后反应是否减轻或消失"].astype (str )+"\n再次使用可疑药是否出现同样反应："+O0OO0OO00O0O0OO0O ["再次使用可疑药是否出现同样反应"].astype (str )+"\n报告人评价："+O0OO0OO00O0O0OO0O ["报告人评价"].astype (str )#line:847
        O0OO0OO00O0O0OO0O ["ADR过程描述以及处理情况"]="不良反应发生时间："+O0OO0OO00O0O0OO0O ["不良反应发生时间"].astype (str )+"\n不良反应过程描述："+O0OO0OO00O0O0OO0O ["不良反应过程描述"].astype (str )+"\n不良反应结果:"+O0OO0OO00O0O0OO0O ["不良反应结果"].astype (str )+"\n对原患疾病影响:"+O0OO0OO00O0O0OO0O ["对原患疾病影响"].astype (str )+"\n后遗症表现："+O0OO0OO00O0O0OO0O ["后遗症表现"].astype (str )+"\n死亡时间:"+O0OO0OO00O0O0OO0O ["死亡时间"].astype (str )+"\n直接死因:"+O0OO0OO00O0O0OO0O ["直接死因"].astype (str )#line:848
        O0OO0OO00O0O0OO0O ["报告者及患者有关情况"]="患者姓名："+O0OO0OO00O0O0OO0O ["患者姓名"].astype (str )+"\n性别："+O0OO0OO00O0O0OO0O ["性别"].astype (str )+"\n出生日期:"+O0OO0OO00O0O0OO0O ["出生日期"].astype (str )+"\n年龄:"+O0OO0OO00O0O0OO0O ["年龄"].astype (str )+O0OO0OO00O0O0OO0O ["年龄单位"].astype (str )+"\n民族："+O0OO0OO00O0O0OO0O ["民族"].astype (str )+"\n体重:"+O0OO0OO00O0O0OO0O ["体重"].astype (str )+"\n原患疾病:"+O0OO0OO00O0O0OO0O ["原患疾病"].astype (str )+"\n病历号/门诊号:"+O0OO0OO00O0O0OO0O ["病历号/门诊号"].astype (str )+"\n既往药品不良反应/事件:"+O0OO0OO00O0O0OO0O ["既往药品不良反应/事件"].astype (str )+"\n家族药品不良反应/事件:"+O0OO0OO00O0O0OO0O ["家族药品不良反应/事件"].astype (str )#line:849
    OO0O0O0000OO00OOO =filedialog .askdirectory ()#!!!!!!!#line:853
    O0O000O0OO00OO0OO =1 #line:856
    for O000OOO0OO000000O in O0OO0OO00O0O0OO0O ["伤害"].drop_duplicates ():#line:857
        if O000OOO0OO000000O =="其他":#line:858
            O0OO00O00O0O00OOO =1 #line:859
            O00O0O00OOO0OO000 =O0OO0OO00O0O0OO0O [(O0OO0OO00O0O0OO0O ["伤害"]=="其他")]#line:860
            OOO0O0OO00O0OOO00 =Tdoing (O00O0O00OOO0OO000 ,OOOO0OO000O0000O0 ,O0O0OOOOO00O0O0OO ,OO00000O0OOO00O0O ,O0O0O00000O0O0O0O ,O0OO0OO0OO0O00O0O )#line:861
            if O0O000O0OO00OO0OO ==1 :#line:862
                O0O0OO00O00O00O00 =OOO0O0OO00O0OOO00 [0 ]#line:863
                O0O000O0OO00OO0OO =O0O000O0OO00OO0OO +1 #line:864
            else :#line:865
                O0O0OO00O00O00O00 =pd .concat ([O0O0OO00O00O00O00 ,OOO0O0OO00O0OOO00 [0 ]],axis =0 )#line:866
        if O000OOO0OO000000O =="严重伤害":#line:868
            OOO00OOOOO000O000 =1 #line:869
            O0OO00O0O000O0O00 =O0OO0OO00O0O0OO0O [(O0OO0OO00O0O0OO0O ["伤害"]=="严重伤害")]#line:870
            OO000O00O0O0O0OOO =Tdoing (O0OO00O0O000O0O00 ,OO0OO0O0O0OOOO000 ,O0O0OOOOO00O0O0OO ,OO00000O0OOO00O0O ,O0O0O00000O0O0O0O ,O0OO0OO0OO0O00O0O )#line:871
            if O0O000O0OO00OO0OO ==1 :#line:872
                O0O0OO00O00O00O00 =OO000O00O0O0O0OOO [0 ]#line:873
                O0O000O0OO00OO0OO =O0O000O0OO00OO0OO +1 #line:874
            else :#line:875
                O0O0OO00O00O00O00 =pd .concat ([O0O0OO00O00O00O00 ,OO000O00O0O0O0OOO [0 ]],axis =0 )#line:876
        if O000OOO0OO000000O =="死亡":#line:878
            O00OO0000000OO000 =1 #line:879
            O00OOOO0OOOO0O00O =O0OO0OO00O0O0OO0O [(O0OO0OO00O0O0OO0O ["伤害"]=="死亡")]#line:880
            O00O0OO0O0OO0OO00 =Tdoing (O00OOOO0OOOO0O00O ,OOOOOO0OOOO0000OO ,O0O0OOOOO00O0O0OO ,OO00000O0OOO00O0O ,O0O0O00000O0O0O0O ,O0OO0OO0OO0O00O0O )#line:881
            if O0O000O0OO00OO0OO ==1 :#line:882
                O0O0OO00O00O00O00 =O00O0OO0O0OO0OO00 [0 ]#line:883
                O0O000O0OO00OO0OO =O0O000O0OO00OO0OO +1 #line:884
            else :#line:885
                O0O0OO00O00O00O00 =pd .concat ([O0O0OO00O00O00O00 ,O00O0OO0O0OO0OO00 [0 ]],axis =0 )#line:886
    text .insert (END ,"\n正在抽样，请稍候...已完成50%")#line:890
    O000O00O000O0OO00 =pd .ExcelWriter (str (OO0O0O0000OO00OOO )+"/●(最终评分需导入)被抽出的所有数据"+".xlsx")#line:891
    O0O0OO00O00O00O00 .to_excel (O000O00O000O0OO00 ,sheet_name ="被抽出的所有数据")#line:892
    O000O00O000O0OO00 .close ()#line:893
    if O0OO0OO0OO0O00O0O ==1 :#line:896
        OO000O00O0OOO0O0O =O0OO0OO00O0O0OO0O .copy ()#line:897
        OO000O00O0OOO0O0O ["原始数量"]=1 #line:898
        O00O0OOO00OOOOO0O =O0O0OO00O00O00O00 .copy ()#line:899
        O00O0OOO00OOOOO0O ["抽取数量"]=1 #line:900
        O0000O0OO0OO000OO =OO000O00O0OOO0O0O .groupby ([OO00000O0OOO00O0O ]).aggregate ({"原始数量":"count"})#line:903
        O0000O0OO0OO000OO =O0000O0OO0OO000OO .sort_values (by =["原始数量"],ascending =False ,na_position ="last")#line:906
        O0000O0OO0OO000OO =O0000O0OO0OO000OO .reset_index ()#line:907
        O0OO00O0OO000O000 =pd .pivot_table (O00O0OOO00OOOOO0O ,values =["抽取数量"],index =OO00000O0OOO00O0O ,columns ="伤害",aggfunc ={"抽取数量":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:918
        O0OO00O0OO000O000 .columns =O0OO00O0OO000O000 .columns .droplevel (0 )#line:919
        O0OO00O0OO000O000 =O0OO00O0OO000O000 .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:922
        O0OO00O0OO000O000 =O0OO00O0OO000O000 .reset_index ()#line:923
        O0OO00O0OO000O000 =O0OO00O0OO000O000 .rename (columns ={"All":"抽取总数量"})#line:924
        try :#line:925
            O0OO00O0OO000O000 =O0OO00O0OO000O000 .rename (columns ={"一般":"抽取数量(一般)"})#line:926
        except :#line:927
            pass #line:928
        try :#line:929
            O0OO00O0OO000O000 =O0OO00O0OO000O000 .rename (columns ={"严重伤害":"抽取数量(严重)"})#line:930
        except :#line:931
            pass #line:932
        try :#line:933
            O0OO00O0OO000O000 =O0OO00O0OO000O000 .rename (columns ={"死亡":"抽取数量-死亡"})#line:934
        except :#line:935
            pass #line:936
        OO00O0OO0OOOOOO0O =pd .merge (O0000O0OO0OO000OO ,O0OO00O0OO000O000 ,on =[OO00000O0OOO00O0O ],how ="left")#line:937
        OO00O0OO0OOOOOO0O ["抽取比例"]=round (OO00O0OO0OOOOOO0O ["抽取总数量"]/OO00O0OO0OOOOOO0O ["原始数量"],2 )#line:938
        O0O0000OO00OOO00O =pd .ExcelWriter (str (OO0O0O0000OO00OOO )+"/抽样情况分布"+".xlsx")#line:939
        OO00O0OO0OOOOOO0O .to_excel (O0O0000OO00OOO00O ,sheet_name ="抽样情况分布")#line:940
        O0O0000OO00OOO00O .close ()#line:941
    O0O0OO00O00O00O00 =O0O0OO00O00O00O00 [O00O0O0O00O0O0000 ["评分项"].tolist ()]#line:947
    OOOOO0OOO00O0OOOO =int (O0O0OOOOO00O0O0OO )#line:949
    text .insert (END ,"\n正在抽样，请稍候...已完成70%")#line:951
    for O000OOO0OO000000O in range (OOOOO0OOO00O0OOOO ):#line:952
        if O000OOO0OO000000O ==0 :#line:953
            OO0OOO0O0O00O00O0 =O0O0OO00O00O00O00 [(O0O0OO00O00O00O00 ["伤害"]=="其他")].sample (frac =1 /(OOOOO0OOO00O0OOOO -O000OOO0OO000000O ),replace =False )#line:957
            OO00OO0O000O000O0 =O0O0OO00O00O00O00 [(O0O0OO00O00O00O00 ["伤害"]=="严重伤害")].sample (frac =1 /(OOOOO0OOO00O0OOOO -O000OOO0OO000000O ),replace =False )#line:960
            OO0OOO0O0OOOOO0O0 =O0O0OO00O00O00O00 [(O0O0OO00O00O00O00 ["伤害"]=="死亡")].sample (frac =1 /(OOOOO0OOO00O0OOOO -O000OOO0OO000000O ),replace =False )#line:963
            O0O0O0OO0O0OO0O0O =pd .concat ([OO0OOO0O0O00O00O0 ,OO00OO0O000O000O0 ,OO0OOO0O0OOOOO0O0 ],axis =0 )#line:965
        else :#line:967
            O0O0OO00O00O00O00 =pd .concat ([O0O0OO00O00O00O00 ,O0O0O0OO0O0OO0O0O ],axis =0 )#line:968
            O0O0OO00O00O00O00 .drop_duplicates (subset =["识别代码"],keep =False ,inplace =True )#line:969
            OO0OOO0O0O00O00O0 =O0O0OO00O00O00O00 [(O0O0OO00O00O00O00 ["伤害"]=="其他")].sample (frac =1 /(OOOOO0OOO00O0OOOO -O000OOO0OO000000O ),replace =False )#line:972
            OO00OO0O000O000O0 =O0O0OO00O00O00O00 [(O0O0OO00O00O00O00 ["伤害"]=="严重伤害")].sample (frac =1 /(OOOOO0OOO00O0OOOO -O000OOO0OO000000O ),replace =False )#line:975
            OO0OOO0O0OOOOO0O0 =O0O0OO00O00O00O00 [(O0O0OO00O00O00O00 ["伤害"]=="死亡")].sample (frac =1 /(OOOOO0OOO00O0OOOO -O000OOO0OO000000O ),replace =False )#line:978
            O0O0O0OO0O0OO0O0O =pd .concat ([OO0OOO0O0O00O00O0 ,OO00OO0O000O000O0 ,OO0OOO0O0OOOOO0O0 ],axis =0 )#line:979
        try :#line:980
            O0O0O0OO0O0OO0O0O ["报告编码"]=O0O0O0OO0O0OO0O0O ["报告编码"].astype (str )#line:981
        except :#line:982
            pass #line:983
        OO0OOOO0O00O0OOOO =str (OO0O0O0000OO00OOO )+"/"+str (O000OOO0OO000000O +1 )+".xlsx"#line:984
        if O0OO0OO0OO0O00O0O ==1 :#line:987
            O0OOO0OOOOO0O0OO0 =TeasyreadT (O0O0O0OO0O0OO0O0O .copy ())#line:988
            del O0OOO0OOOOO0O0OO0 ["逐条查看"]#line:989
            O0OOO0OOOOO0O0OO0 ["评分"]=""#line:990
            if len (O0OOO0OOOOO0O0OO0 )>0 :#line:991
                for OO000OOOOO00OOO00 ,OOOOO0OOOOOO000OO in O00O0O0O00O0O0000 .iterrows ():#line:992
                    O0OOO0OOOOO0O0OO0 .loc [(O0OOO0OOOOO0O0OO0 ["条目"]==OOOOO0OOOOOO000OO ["评分项"]),"满分"]=OOOOO0OOOOOO000OO ["满分分值"]#line:993
                    O0OOO0OOOOO0O0OO0 .loc [(O0OOO0OOOOO0O0OO0 ["条目"]==OOOOO0OOOOOO000OO ["评分项"]),"打分标准"]=OOOOO0OOOOOO000OO ["打分标准"]#line:996
            O0OOO0OOOOO0O0OO0 ["专家序号"]=O000OOO0OO000000O +1 #line:998
            O0OO000OO0000OOOO =str (OO0O0O0000OO00OOO )+"/"+"●专家评分表"+str (O000OOO0OO000000O +1 )+".xlsx"#line:999
            OO00O00OO000O000O =pd .ExcelWriter (O0OO000OO0000OOOO )#line:1000
            O0OOO0OOOOO0O0OO0 .to_excel (OO00O00OO000O000O ,sheet_name ="字典数据")#line:1001
            OO00O00OO000O000O .close ()#line:1002
    text .insert (END ,"\n正在抽样，请稍候...已完成100%")#line:1005
    showinfo (title ="提示信息",message ="抽样和分组成功，请查看以下文件夹："+str (OO0O0O0000OO00OOO ))#line:1006
    text .insert (END ,"\n抽样和分组成功，请查看以下文件夹："+str (OO0O0O0000OO00OOO ))#line:1007
    text .insert (END ,"\n抽样概况:\n")#line:1008
    text .insert (END ,OO00O0OO0OOOOOO0O [[OO00000O0OOO00O0O ,"原始数量","抽取总数量"]])#line:1009
    text .see (END )#line:1010
def Tdoing (OO00O000OOO00O0OO ,O0000O0OOO0O00O0O ,O00O0OOO00O0000O0 ,O0O00O0OOO000O0OO ,OO00OO000OOOOO000 ,O0OOO00000000OO00 ):#line:1013
    ""#line:1014
    def O000OOO00OO0OO000 (O00O0OOOO000O0OO0 ,O0OO0O00OO00OO0O0 ,O00OO000O0000O000 ):#line:1016
        if float (O0OO0O00OO00OO0O0 )>1 :#line:1017
            try :#line:1018
                O0OOOOO0O0OO000OO =O00O0OOOO000O0OO0 .sample (int (O0OO0O00OO00OO0O0 ),replace =False )#line:1019
            except ValueError :#line:1021
                O0OOOOO0O0OO000OO =O00O0OOOO000O0OO0 #line:1023
        else :#line:1024
            O0OOOOO0O0OO000OO =O00O0OOOO000O0OO0 .sample (frac =float (O0OO0O00OO00OO0O0 ),replace =False )#line:1025
            if len (O00O0OOOO000O0OO0 )*float (O0OO0O00OO00OO0O0 )>len (O0OOOOO0O0OO000OO )and O00OO000O0000O000 =="最大覆盖":#line:1027
                O000000OO00O00O0O =pd .concat ([O00O0OOOO000O0OO0 ,O0OOOOO0O0OO000OO ],axis =0 )#line:1028
                O000000OO00O00O0O .drop_duplicates (subset =["识别代码"],keep =False ,inplace =True )#line:1029
                OO00O0OO0O000O0OO =O000000OO00O00O0O .sample (1 ,replace =False )#line:1030
                O0OOOOO0O0OO000OO =pd .concat ([O0OOOOO0O0OO000OO ,OO00O0OO0O000O0OO ],axis =0 )#line:1031
        return O0OOOOO0O0OO000OO #line:1032
    if OO00OO000OOOOO000 =="总体随机":#line:1035
        O00O00O00O0O000OO =O000OOO00OO0OO000 (OO00O000OOO00O0OO ,O0000O0OOO0O00O0O ,OO00OO000OOOOO000 )#line:1036
    else :#line:1038
        O00OO0O0OOOO000OO =1 #line:1039
        for OO00O000OO0OOOO0O in OO00O000OOO00O0OO [O0O00O0OOO000O0OO ].drop_duplicates ():#line:1040
            O0O0000OOO0O000OO =OO00O000OOO00O0OO [(OO00O000OOO00O0OO [O0O00O0OOO000O0OO ]==OO00O000OO0OOOO0O )].copy ()#line:1041
            if O00OO0O0OOOO000OO ==1 :#line:1042
                O00O00O00O0O000OO =O000OOO00OO0OO000 (O0O0000OOO0O000OO ,O0000O0OOO0O00O0O ,OO00OO000OOOOO000 )#line:1043
                O00OO0O0OOOO000OO =O00OO0O0OOOO000OO +1 #line:1044
            else :#line:1045
                OO0OOOOO000O0O0OO =O000OOO00OO0OO000 (O0O0000OOO0O000OO ,O0000O0OOO0O00O0O ,OO00OO000OOOOO000 )#line:1046
                O00O00O00O0O000OO =pd .concat ([O00O00O00O0O000OO ,OO0OOOOO000O0O0OO ])#line:1047
    O00O00O00O0O000OO =O00O00O00O0O000OO .drop_duplicates ()#line:1048
    return O00O00O00O0O000OO ,1 #line:1049
def Tpinggu ():#line:1052
    ""#line:1053
    OOOOO0OOOO0OO0O00 =Topentable (1 )#line:1054
    OOOOOO0O00OO0O0OO =OOOOO0OOOO0OO0O00 [0 ]#line:1055
    O00OO00O0OOOOOO0O =OOOOO0OOOO0OO0O00 [1 ]#line:1056
    try :#line:1059
        OOOO0O00000000O0O =[pd .read_excel (O0O0O0000O0OOO00O ,header =0 ,sheet_name =0 )for O0O0O0000O0OOO00O in O00OO00O0OOOOOO0O ]#line:1063
        O00OOO000OOO000O0 =pd .concat (OOOO0O00000000O0O ,ignore_index =True ).drop_duplicates ()#line:1064
        try :#line:1065
            O00OOO000OOO000O0 =O00OOO000OOO000O0 .loc [:,~O00OOO000OOO000O0 .columns .str .contains ("^Unnamed")]#line:1066
        except :#line:1067
            pass #line:1068
    except :#line:1069
        showinfo (title ="提示信息",message ="载入文件出错，任务终止。")#line:1070
        return 0 #line:1071
    try :#line:1074
        OOOOOO0O00OO0O0OO =OOOOOO0O00OO0O0OO .reset_index ()#line:1075
    except :#line:1076
        showinfo (title ="提示信息",message ="专家评分文件存在错误，程序中止。")#line:1077
        return 0 #line:1078
    O00OOO000OOO000O0 ["质量评估专用表"]=""#line:1080
    text .insert (END ,"\n打分表导入成功，正在统计，请耐心等待...")#line:1083
    text .insert (END ,"\n正在计算总分，请稍候，已完成20%")#line:1084
    text .see (END )#line:1085
    OOO0O00O00O0OO00O =OOOOOO0O00OO0O0OO [["序号","条目","详细描述","评分","满分","打分标准","专家序号"]].copy ()#line:1088
    OO0O0O000O0O000O0 =O00OOO000OOO000O0 [["质量评估模式","识别代码"]].copy ()#line:1089
    OOO0O00O00O0OO00O .reset_index (inplace =True )#line:1090
    OO0O0O000O0O000O0 .reset_index (inplace =True )#line:1091
    OO0O0O000O0O000O0 =OO0O0O000O0O000O0 .rename (columns ={"识别代码":"序号"})#line:1092
    OOO0O00O00O0OO00O =pd .merge (OOO0O00O00O0OO00O ,OO0O0O000O0O000O0 ,on =["序号"])#line:1093
    OOO0O00O00O0OO00O =OOO0O00O00O0OO00O .sort_values (by =["序号","条目"],ascending =True ,na_position ="last")#line:1094
    OOO0O00O00O0OO00O =OOO0O00O00O0OO00O [["质量评估模式","序号","条目","详细描述","评分","满分","打分标准","专家序号"]]#line:1095
    for O0O0000OOO0OOO000 ,OO0OOO0O00O0OOOO0 in OOOOOO0O00OO0O0OO .iterrows ():#line:1097
        OO0O00O000OO0OOOO ="专家打分-"+str (OO0OOO0O00O0OOOO0 ["条目"])#line:1098
        O00OOO000OOO000O0 .loc [(O00OOO000OOO000O0 ["识别代码"]==OO0OOO0O00O0OOOO0 ["序号"]),OO0O00O000OO0OOOO ]=OO0OOO0O00O0OOOO0 ["评分"]#line:1099
    del O00OOO000OOO000O0 ["专家打分-识别代码"]#line:1100
    del O00OOO000OOO000O0 ["专家打分-#####分隔符#########"]#line:1101
    try :#line:1102
        O00OOO000OOO000O0 =O00OOO000OOO000O0 .loc [:,~O00OOO000OOO000O0 .columns .str .contains ("^Unnamed")]#line:1103
    except :#line:1104
        pass #line:1105
    text .insert (END ,"\n正在计算总分，请稍候，已完成60%")#line:1106
    text .see (END )#line:1107
    OO0OO0OOOOO00OOOO =O00OO00O0OOOOOO0O [0 ]#line:1110
    try :#line:1111
        OOOO000000000000O =str (OO0OO0OOOOO00OOOO ).replace ("●(最终评分需导入)被抽出的所有数据.xls","")#line:1112
    except :#line:1113
        OOOO000000000000O =str (OO0OO0OOOOO00OOOO )#line:1114
    OO0O00OOOOOOOO0O0 =pd .ExcelWriter (str (OOOO000000000000O )+"各评估对象打分核对文件"+".xlsx")#line:1122
    OOO0O00O00O0OO00O .to_excel (OO0O00OOOOOOOO0O0 ,sheet_name ="原始打分")#line:1123
    OO0O00OOOOOOOO0O0 .close ()#line:1124
    O00O0O0OOOOO00OOO =Tpinggu2 (O00OOO000OOO000O0 )#line:1128
    text .insert (END ,"\n正在计算总分，请稍候，已完成100%")#line:1130
    text .see (END )#line:1131
    showinfo (title ="提示信息",message ="打分计算成功，请查看文件："+str (OOOO000000000000O )+"最终打分"+".xlsx")#line:1132
    text .insert (END ,"\n打分计算成功，请查看文件："+str (OO0OO0OOOOO00OOOO )+"最终打分"+".xls\n")#line:1133
    O00O0O0OOOOO00OOO .reset_index (inplace =True )#line:1134
    text .insert (END ,"\n以下是结果概况：\n")#line:1135
    text .insert (END ,O00O0O0OOOOO00OOO [["评估对象","总分"]])#line:1136
    text .see (END )#line:1137
    O0OO0OOO000OOO0OO =["评估对象","总分"]#line:1141
    for O00OOOOO0OO00000O in O00O0O0OOOOO00OOO .columns :#line:1142
        if "专家打分"in O00OOOOO0OO00000O :#line:1143
            O0OO0OOO000OOO0OO .append (O00OOOOO0OO00000O )#line:1144
    O000O000OOOOO00OO =O00O0O0OOOOO00OOO [O0OO0OOO000OOO0OO ]#line:1145
    OOO0000OO0OOO0OOO =pd .read_excel (peizhidir +"0（范例）质量评估.xls",sheet_name =0 ,header =0 ,index_col =0 ).reset_index ()#line:1149
    if "专家打分-不良反应名称"in O0OO0OOO000OOO0OO :#line:1151
        OOO0000OO0OOO0OOO =pd .read_excel (peizhidir +"0（范例）质量评估.xls",sheet_name ="药品",header =0 ,index_col =0 ).reset_index ()#line:1152
    if "专家打分-化妆品名称"in O0OO0OOO000OOO0OO :#line:1154
        OOO0000OO0OOO0OOO =pd .read_excel (peizhidir +"0（范例）质量评估.xls",sheet_name ="化妆品",header =0 ,index_col =0 ).reset_index ()#line:1155
    if "专家打分-是否需要开展产品风险评价"in O0OO0OOO000OOO0OO :#line:1156
        OOO0000OO0OOO0OOO =pd .read_excel (peizhidir +"0（范例）质量评估.xls",sheet_name ="器械持有人",header =0 ,index_col =0 ).reset_index ()#line:1157
    for O0O0000OOO0OOO000 ,OO0OOO0O00O0OOOO0 in OOO0000OO0OOO0OOO .iterrows ():#line:1158
        O0OOO0000OOO0O000 ="专家打分-"+str (OO0OOO0O00O0OOOO0 ["评分项"])#line:1159
        try :#line:1160
            warnings .filterwarnings ('ignore')#line:1161
            O000O000OOOOO00OO .loc [-1 ,O0OOO0000OOO0O000 ]=OO0OOO0O00O0OOOO0 ["满分分值"]#line:1162
        except :#line:1163
            pass #line:1164
    del O000O000OOOOO00OO ["专家打分-识别代码"]#line:1165
    O000O000OOOOO00OO .iloc [-1 ,0 ]="满分分值"#line:1166
    O000O000OOOOO00OO .loc [-1 ,"总分"]=100 #line:1167
    if "专家打分-事件原因分析.1"not in O0OO0OOO000OOO0OO :#line:1169
        O000O000OOOOO00OO .loc [-1 ,"专家打分-报告时限"]=5 #line:1170
    if "专家打分-事件原因分析.1"in O0OO0OOO000OOO0OO :#line:1172
        O000O000OOOOO00OO .loc [-1 ,"专家打分-报告时限"]=10 #line:1173
    O000O000OOOOO00OO .columns =O000O000OOOOO00OO .columns .str .replace ("专家打分-","",regex =False )#line:1176
    if ("专家打分-器械故障表现"in O0OO0OOO000OOO0OO )and ("modex"not in O00OOO000OOO000O0 .columns ):#line:1178
        O000O000OOOOO00OO .loc [-1 ,"姓名和既往病史"]=2 #line:1179
        O000O000OOOOO00OO .loc [-1 ,"报告日期"]=1 #line:1180
    else :#line:1181
        del O000O000OOOOO00OO ["伤害"]#line:1182
    if "专家打分-化妆品名称"in O0OO0OOO000OOO0OO :#line:1184
        del O000O000OOOOO00OO ["报告时限"]#line:1185
    try :#line:1188
        O000O000OOOOO00OO =O000O000OOOOO00OO [["评估对象","总分","伤害.1","是否开展了调查及调查情况","关联性评价","事件原因分析.1","是否需要开展产品风险评价","控制措施情况","是否为错报误报报告及错报误报说明","是否合并报告及合并报告编码","报告时限"]]#line:1189
    except :#line:1190
        pass #line:1191
    try :#line:1192
        O000O000OOOOO00OO =O000O000OOOOO00OO [["评估对象","总分","报告日期","报告人","联系人","联系电话","注册证编号/曾用注册证编号","产品名称","型号和规格","产品批号和产品编号","生产日期","有效期至","事件发生日期","发现或获知日期","伤害","伤害表现","器械故障表现","姓名和既往病史","年龄和年龄类型","性别","预期治疗疾病或作用","器械使用日期","使用场所和场所名称","使用过程","合并用药/械情况说明","事件原因分析和事件原因分析描述","初步处置情况","报告时限"]]#line:1193
    except :#line:1194
        pass #line:1195
    try :#line:1196
        O000O000OOOOO00OO =O000O000OOOOO00OO [["评估对象","总分","报告类型","报告时限","报告者及患者有关情况","原患疾病","药品信息","不良反应名称","ADR过程描述以及处理情况","关联性评价和ADR分析"]]#line:1197
    except :#line:1198
        pass #line:1199
    OO0OO0O0OOOOOO000 =pd .ExcelWriter (str (OOOO000000000000O )+"最终打分"+".xlsx")#line:1201
    O000O000OOOOO00OO .to_excel (OO0OO0O0OOOOOO000 ,sheet_name ="最终打分")#line:1202
    OO0OO0O0OOOOOO000 .close ()#line:1203
    Ttree_Level_2 (O000O000OOOOO00OO ,0 ,O00O0O0OOOOO00OOO )#line:1205
def Tpinggu2 (O0OOOOO0000O0000O ):#line:1208
    ""#line:1209
    O0OOOOO0000O0000O ["报告数量小计"]=1 #line:1210
    if ("器械故障表现"in O0OOOOO0000O0000O .columns )and ("modex"not in O0OOOOO0000O0000O .columns ):#line:1213
        O0OOOOO0000O0000O ["专家打分-姓名和既往病史"]=2 #line:1214
        O0OOOOO0000O0000O ["专家打分-报告日期"]=1 #line:1215
        if "专家打分-报告时限情况"not in O0OOOOO0000O0000O .columns :#line:1216
            O0OOOOO0000O0000O ["报告时限"]=O0OOOOO0000O0000O ["报告时限"].astype (float )#line:1217
            O0OOOOO0000O0000O ["专家打分-报告时限"]=0 #line:1218
            O0OOOOO0000O0000O .loc [(O0OOOOO0000O0000O ["伤害"]=="死亡")&(O0OOOOO0000O0000O ["报告时限"]<=7 ),"专家打分-报告时限"]=5 #line:1219
            O0OOOOO0000O0000O .loc [(O0OOOOO0000O0000O ["伤害"]=="严重伤害")&(O0OOOOO0000O0000O ["报告时限"]<=20 ),"专家打分-报告时限"]=5 #line:1220
            O0OOOOO0000O0000O .loc [(O0OOOOO0000O0000O ["伤害"]=="其他")&(O0OOOOO0000O0000O ["报告时限"]<=30 ),"专家打分-报告时限"]=5 #line:1221
    if "专家打分-事件原因分析.1"in O0OOOOO0000O0000O .columns :#line:1225
       O0OOOOO0000O0000O ["专家打分-报告时限"]=10 #line:1226
    OOOO00O0OO0OOO0OO =[]#line:1229
    for O00OO0O0000OO0OOO in O0OOOOO0000O0000O .columns :#line:1230
        if "专家打分-"in O00OO0O0000OO0OOO :#line:1231
            OOOO00O0OO0OOO0OO .append (O00OO0O0000OO0OOO )#line:1232
    O0000OOO00O00OOO0 =1 #line:1236
    for O00OO0O0000OO0OOO in OOOO00O0OO0OOO0OO :#line:1237
        OOOOO0000O0O0O000 =O0OOOOO0000O0000O .groupby (["质量评估模式"]).aggregate ({O00OO0O0000OO0OOO :"sum"}).reset_index ()#line:1238
        if O0000OOO00O00OOO0 ==1 :#line:1239
            O0OOO0O00000O0O0O =OOOOO0000O0O0O000 #line:1240
            O0000OOO00O00OOO0 =O0000OOO00O00OOO0 +1 #line:1241
        else :#line:1242
            O0OOO0O00000O0O0O =pd .merge (O0OOO0O00000O0O0O ,OOOOO0000O0O0O000 ,on ="质量评估模式",how ="left")#line:1243
    O000O0000OO0O0O00 =O0OOOOO0000O0000O .groupby (["质量评估模式"]).aggregate ({"报告数量小计":"sum"}).reset_index ()#line:1245
    O0OOO0O00000O0O0O =pd .merge (O0OOO0O00000O0O0O ,O000O0000OO0O0O00 ,on ="质量评估模式",how ="left")#line:1246
    for O00OO0O0000OO0OOO in OOOO00O0OO0OOO0OO :#line:1249
        O0OOO0O00000O0O0O [O00OO0O0000OO0OOO ]=round (O0OOO0O00000O0O0O [O00OO0O0000OO0OOO ]/O0OOO0O00000O0O0O ["报告数量小计"],2 )#line:1250
    O0OOO0O00000O0O0O ["总分"]=round (O0OOO0O00000O0O0O [OOOO00O0OO0OOO0OO ].sum (axis =1 ),2 )#line:1251
    O0OOO0O00000O0O0O =O0OOO0O00000O0O0O .sort_values (by =["总分"],ascending =False ,na_position ="last")#line:1252
    warnings .filterwarnings ('ignore')#line:1253
    O0OOO0O00000O0O0O .loc ["平均分(非加权)"]=round (O0OOO0O00000O0O0O .mean (axis =0 ),2 )#line:1254
    O0OOO0O00000O0O0O .loc ["标准差(非加权)"]=round (O0OOO0O00000O0O0O .std (axis =0 ),2 )#line:1255
    O0OOO0O00000O0O0O =O0OOO0O00000O0O0O .rename (columns ={"质量评估模式":"评估对象"})#line:1256
    O0OOO0O00000O0O0O .iloc [-2 ,0 ]="平均分(非加权)"#line:1257
    O0OOO0O00000O0O0O .iloc [-1 ,0 ]="标准差(非加权)"#line:1258
    return O0OOO0O00000O0O0O #line:1260
def Ttree_Level_2 (OOOOOO000OOO0O0OO ,OO0O00OO0O00O0000 ,OO00O0OOOOO000O00 ,*O00O0OO00OO000O00 ):#line:1263
    ""#line:1264
    OO00O000O00O0O000 =OOOOOO000OOO0O0OO .columns .values .tolist ()#line:1266
    OO0O00OO0O00O0000 =0 #line:1267
    O000000OO000O0OOO =OOOOOO000OOO0O0OO .loc [:]#line:1268
    O00OOOO0OOO00O00O =Toplevel ()#line:1271
    O00OOOO0OOO00O00O .title ("报表查看器")#line:1272
    OO0000OOOO00OOOOO =O00OOOO0OOO00O00O .winfo_screenwidth ()#line:1273
    O0O0OO0O00OOOOOOO =O00OOOO0OOO00O00O .winfo_screenheight ()#line:1275
    OOOOOOOOO000OO0O0 =1300 #line:1277
    OOO000O0O00OO000O =600 #line:1278
    O0OO00000OO000O0O =(OO0000OOOO00OOOOO -OOOOOOOOO000OO0O0 )/2 #line:1280
    O0O0O00O00O0000OO =(O0O0OO0O00OOOOOOO -OOO000O0O00OO000O )/2 #line:1281
    O00OOOO0OOO00O00O .geometry ("%dx%d+%d+%d"%(OOOOOOOOO000OO0O0 ,OOO000O0O00OO000O ,O0OO00000OO000O0O ,O0O0O00O00O0000OO ))#line:1282
    O0O000O0O0O0OOOO0 =ttk .Frame (O00OOOO0OOO00O00O ,width =1300 ,height =20 )#line:1283
    O0O000O0O0O0OOOO0 .pack (side =TOP )#line:1284
    O00OO000O000O0OO0 =O000000OO000O0OOO .values .tolist ()#line:1287
    O000OOOOOO000OOOO =O000000OO000O0OOO .columns .values .tolist ()#line:1288
    OO00O0OO0O00O0000 =ttk .Treeview (O0O000O0O0O0OOOO0 ,columns =O000OOOOOO000OOOO ,show ="headings",height =45 )#line:1289
    for O0O0OOOO00O0OOOOO in O000OOOOOO000OOOO :#line:1291
        OO00O0OO0O00O0000 .heading (O0O0OOOO00O0OOOOO ,text =O0O0OOOO00O0OOOOO )#line:1292
    for OO00000000OO00O00 in O00OO000O000O0OO0 :#line:1293
        OO00O0OO0O00O0000 .insert ("","end",values =OO00000000OO00O00 )#line:1294
    for O0OOO0O0O000OOO00 in O000OOOOOO000OOOO :#line:1295
        OO00O0OO0O00O0000 .column (O0OOO0O0O000OOO00 ,minwidth =0 ,width =120 ,stretch =NO )#line:1296
    OOOOO00O0000OO000 =Scrollbar (O0O000O0O0O0OOOO0 ,orient ="vertical")#line:1298
    OOOOO00O0000OO000 .pack (side =RIGHT ,fill =Y )#line:1299
    OOOOO00O0000OO000 .config (command =OO00O0OO0O00O0000 .yview )#line:1300
    OO00O0OO0O00O0000 .config (yscrollcommand =OOOOO00O0000OO000 .set )#line:1301
    OO0000OOO0O0OO0OO =Scrollbar (O0O000O0O0O0OOOO0 ,orient ="horizontal")#line:1303
    OO0000OOO0O0OO0OO .pack (side =BOTTOM ,fill =X )#line:1304
    OO0000OOO0O0OO0OO .config (command =OO00O0OO0O00O0000 .xview )#line:1305
    OO00O0OO0O00O0000 .config (yscrollcommand =OOOOO00O0000OO000 .set )#line:1306
    def O0000O00OO0O0000O (O0OO00OOO0O0O00OO ,OO0000OOOOO00O0OO ,O0O0O0OO0O0O00OOO ):#line:1308
        for O00000OOOO0O0000O in OO00O0OO0O00O0000 .selection ():#line:1311
            O0O0OOOOOO00000O0 =OO00O0OO0O00O0000 .item (O00000OOOO0O0000O ,"values")#line:1312
        O0OO00O00OO000OO0 =O0O0OOOOOO00000O0 [2 :]#line:1314
        OO00O0OO00OOOO000 =O0O0O0OO0O0O00OOO .iloc [-1 ,:][2 :]#line:1317
        O0OOOO00O000OOOOO =O0O0O0OO0O0O00OOO .columns #line:1318
        O0OOOO00O000OOOOO =O0OOOO00O000OOOOO [2 :]#line:1319
        Tpo (OO00O0OO00OOOO000 ,O0OO00O00OO000OO0 ,O0OOOO00O000OOOOO ,"失分","得分",O0O0OOOOOO00000O0 [0 ])#line:1321
        return 0 #line:1322
    OO00O0OO0O00O0000 .bind ("<Double-1>",lambda O000OO00000OOOO0O :O0000O00OO0O0000O (O000OO00000OOOO0O ,O000OOOOOO000OOOO ,O000000OO000O0OOO ),)#line:1328
    def OO0O0OOO00OO0O00O (O00O0000O00O0000O ,OO00OOOO0O00O00OO ,O0O0O0OO000OOOOO0 ):#line:1330
        OO0OO0OO000O0000O =[(O00O0000O00O0000O .set (OO000000OOOOOO0O0 ,OO00OOOO0O00O00OO ),OO000000OOOOOO0O0 )for OO000000OOOOOO0O0 in O00O0000O00O0000O .get_children ("")]#line:1331
        OO0OO0OO000O0000O .sort (reverse =O0O0O0OO000OOOOO0 )#line:1332
        for O00O0OO0OOO000OO0 ,(OOOOOOOO0O0000OOO ,O0OOO0O0000000OOO )in enumerate (OO0OO0OO000O0000O ):#line:1334
            O00O0000O00O0000O .move (O0OOO0O0000000OOO ,"",O00O0OO0OOO000OO0 )#line:1335
        O00O0000O00O0000O .heading (OO00OOOO0O00O00OO ,command =lambda :OO0O0OOO00OO0O00O (O00O0000O00O0000O ,OO00OOOO0O00O00OO ,not O0O0O0OO000OOOOO0 ))#line:1338
    for O000O0O0O0OO0O0OO in O000OOOOOO000OOOO :#line:1340
        OO00O0OO0O00O0000 .heading (O000O0O0O0OO0O0OO ,text =O000O0O0O0OO0O0OO ,command =lambda _col =O000O0O0O0OO0O0OO :OO0O0OOO00OO0O00O (OO00O0OO0O00O0000 ,_col ,False ),)#line:1345
    OO00O0OO0O00O0000 .pack ()#line:1347
def Txuanze ():#line:1349
    ""#line:1350
    global ori #line:1351
    O0OO0OOOOO0OO0OO0 =pd .read_excel (peizhidir +"0（范例）批量筛选.xls",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1352
    text .insert (END ,"\n正在执行内部数据规整...\n")#line:1353
    text .insert (END ,O0OO0OOOOO0OO0OO0 )#line:1354
    ori ["temppr"]=""#line:1355
    for O0O0O000000O0O00O in O0OO0OOOOO0OO0OO0 .columns .tolist ():#line:1356
        ori ["temppr"]=ori ["temppr"]+"----"+ori [O0O0O000000O0O00O ]#line:1357
    O00O0OOOOOO00OOOO ="测试字段MMMMM"#line:1358
    for O0O0O000000O0O00O in O0OO0OOOOO0OO0OO0 .columns .tolist ():#line:1359
        for O000O00OO0O00O0OO in O0OO0OOOOO0OO0OO0 [O0O0O000000O0O00O ].drop_duplicates ():#line:1360
            if O000O00OO0O00O0OO :#line:1361
                O00O0OOOOOO00OOOO =O00O0OOOOOO00OOOO +"|"+str (O000O00OO0O00O0OO )#line:1362
    ori =ori .loc [ori ["temppr"].str .contains (O00O0OOOOOO00OOOO ,na =False )].copy ()#line:1363
    del ori ["temppr"]#line:1364
    ori =ori .reset_index (drop =True )#line:1366
    text .insert (END ,"\n内部数据规整完毕。\n")#line:1367
def Tpo (OO0000O0OO000000O ,OOO00OOOOOO000O0O ,OO0OO0OO000O0OOO0 ,OOO000OO0000OOOOO ,OO0000OOOO0OOOOOO ,OOOO0O0O0000OO0O0 ):#line:1370
    ""#line:1371
    OO0000O0OO000000O =OO0000O0OO000000O .astype (float )#line:1372
    OOO00OOOOOO000O0O =tuple (float (O00OO00OO0OO0OO00 )for O00OO00OO0OO0OO00 in OOO00OOOOOO000O0O )#line:1373
    OOOO0OOOOOO0O0O0O =Toplevel ()#line:1374
    OOOO0OOOOOO0O0O0O .title (OOOO0O0O0000OO0O0 )#line:1375
    OO00OOOOOO0O0O0OO =ttk .Frame (OOOO0OOOOOO0O0O0O ,height =20 )#line:1376
    OO00OOOOOO0O0O0OO .pack (side =TOP )#line:1377
    OO0O000000O000O0O =0.2 #line:1379
    O0OOOOO0O000OOOOO =Figure (figsize =(12 ,6 ),dpi =100 )#line:1380
    OOO00OO00OOO0OO0O =FigureCanvasTkAgg (O0OOOOO0O000OOOOO ,master =OOOO0OOOOOO0O0O0O )#line:1381
    OOO00OO00OOO0OO0O .draw ()#line:1382
    OOO00OO00OOO0OO0O .get_tk_widget ().pack (expand =1 )#line:1383
    O000OO00O00OOO0O0 =O0OOOOO0O000OOOOO .add_subplot (111 )#line:1384
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:1386
    O000OO000O00O00OO =NavigationToolbar2Tk (OOO00OO00OOO0OO0O ,OOOO0OOOOOO0O0O0O )#line:1388
    O000OO000O00O00OO .update ()#line:1389
    OOO00OO00OOO0OO0O .get_tk_widget ().pack ()#line:1391
    O00O0O0OO00OOO0O0 =range (0 ,len (OO0OO0OO000O0OOO0 ),1 )#line:1392
    O000OO00O00OOO0O0 .set_xticklabels (OO0OO0OO000O0OOO0 ,rotation =-90 ,fontsize =8 )#line:1395
    O000OO00O00OOO0O0 .bar (O00O0O0OO00OOO0O0 ,OO0000O0OO000000O ,align ="center",tick_label =OO0OO0OO000O0OOO0 ,label =OOO000OO0000OOOOO )#line:1399
    O000OO00O00OOO0O0 .bar (O00O0O0OO00OOO0O0 ,OOO00OOOOOO000O0O ,align ="center",label =OO0000OOOO0OOOOOO )#line:1400
    O000OO00O00OOO0O0 .set_title (OOOO0O0O0000OO0O0 )#line:1401
    O000OO00O00OOO0O0 .set_xlabel ("项")#line:1402
    O000OO00O00OOO0O0 .set_ylabel ("数量")#line:1403
    O0OOOOO0O000OOOOO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:1406
    OOO00000000O0OOOO =O000OO00O00OOO0O0 .get_position ()#line:1407
    O000OO00O00OOO0O0 .set_position ([OOO00000000O0OOOO .x0 ,OOO00000000O0OOOO .y0 ,OOO00000000O0OOOO .width *0.7 ,OOO00000000O0OOOO .height ])#line:1408
    O000OO00O00OOO0O0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:1409
    OOO00OO00OOO0OO0O .draw ()#line:1411
def helper ():#line:1414
    ""#line:1415
    OOOOOOO0OOOO0OO0O =Toplevel ()#line:1416
    OOOOOOO0OOOO0OO0O .title ("程序使用帮助")#line:1417
    OOOOOOO0OOOO0OO0O .geometry ("700x500")#line:1418
    OO0000000OOO0OO0O =Scrollbar (OOOOOOO0OOOO0OO0O )#line:1420
    OO0O00OOO00O0O000 =Text (OOOOOOO0OOOO0OO0O ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1421
    OO0000000OOO0OO0O .pack (side =RIGHT ,fill =Y )#line:1422
    OO0O00OOO00O0O000 .pack ()#line:1423
    OO0000000OOO0OO0O .config (command =OO0O00OOO00O0O000 .yview )#line:1424
    OO0O00OOO00O0O000 .config (yscrollcommand =OO0000000OOO0OO0O .set )#line:1425
    OO0O00OOO00O0O000 .insert (END ,"\n                                             帮助文件\n\n\n为帮助用户快速熟悉“阅易评”使用方法，现以医疗器械不良事件报告表为例，对使用步骤作以下说明：\n\n第一步：原始数据准备\n用户登录国家医疗器械不良事件监测信息系统（https://maers.adrs.org.cn/），在“个例不良事件管理—报告浏览”页面，选择本次评估的报告范围（时间、报告状态、事发地监测机构等）后进行查询和导出。\n●注意：国家医疗器械不良事件监测信息系统设置每次导出数据上限为5000份报告，如查询发现需导出报告数量超限，需分次导出；如导出数据为压缩包，需先行解压。如原始数据在多个文件夹内，需先行整理到统一文件夹中，方便下一步操作。\n\n第二步：原始数据导入\n用户点击“导入原始数据”按钮，在弹出数据导入框中找到原始数据存储位置，本程序支持导入多个原始数据文件，可在长按键盘“Ctrl”按键的同时分别点击相关文件，选择完毕后点击“打开”按钮，程序会提示“数据读取成功”或“导入文件错误”。\n●注意：基于当前评估工作需要，仅针对使用单位报告进行评估，故导入数据时仅选择“使用单位、经营企业医疗器械不良事件报告”，不支持与“上市许可持有人医疗器械不良事件报告”混选。如提示“导入文件错误，请重试”，请重启程序并重新操作，如仍提示错误可与开发者联系（联系方式见文末）。\n\n第三步：报告抽样分组\n用户点击“随机抽样分组”按钮，在“随机抽样及随机分组”弹窗中：\n1、根据评估目的，在“评估对象”处勾选相应选项，可根据选项对上报单位（医疗机构）、县（区）、地市实施评估。注意：如果您是省级用户，被评估对象是各地市，您要关闭本软件，修改好配置表文件夹“0（范例）质量评估.xls”中的“地市列表”单元表，将本省地市参照范例填好再运行本软件。如果被评估对象不是选择“地市”，则无需该项操作。\n2、根据报告伤害类型依次输入需抽取的比例或报告数量。程序默认此处输入数值小于1（含1）为抽取比例，输入数值大于1为抽取报告数量，用户根据实际情况任选一种方式即可。本程序支持不同伤害类型报告选用不同抽样方式。\n3、根据参与评估专家数量，在“抽样后随机分组数”输入对应数字。\n4、抽样方法有2种，一种是最大覆盖，即对每个评估对象按抽样数量/比例进行单独抽样，如遇到不足则多抽（所以总体实际抽样数量可能会比设置的多一点），每个评估对象都会被抽到；另外一种是总体随机，即按照设定的参数从总体中随机抽取（有可能部分评估对象没有被抽到）。\n用户在确定抽样分组内容全部正确录入后，点击“最大覆盖”或者“总体随机”按钮，根据程序提示选择保存地址。程序将按照专家数量将抽取的报告进行随即分配，生成对应份数的“专家评分表”，专家评分表包含评分项、详细描述、评分、满分、打分标准等。专家评分表自动隐藏报告单位等信息，用户可随机将评分表派发给专家进行评分。\n●注意：为保护数据同时便于专家查看，需对专家评分表进行格式设置，具体操作如下（或者直接使用格式刷一键完成，模板详见配置表-专家模板）：全选表格，右键-设置单元格格式-对齐，勾选自动换行，之后设置好列间距。此外，请勿修改“专家评分表“和“（最终评分需导入）被抽出的所有数据”两类工作文件的文件名。\n\n第四步：评估得分统计\n用户在全部专家完成评分后，将所有专家评分表放置在同一文件夹中，点击“评估得分统计”按钮，全选所有专家评分表和“（最终评分需导入）被抽出的所有数据”这个文件，后点击“打开”，程序将首先进行评分内容校验，对于打分错误报告给与提示并生成错误定位文件，需根据提示修正错误再全部导入。如打分项无误，程序将提示“打分表导入成功，正在统计请耐心等待”，并生成最终的评分结果。\n\n本程序由广东省药品不良反应监测中心和佛山市药品不良反应监测中心共同制作，其他贡献单位包括广州市药品不良反应监测中心、深圳市药物警戒和风险管理研究院等。如有疑问，请联系我们：\n评估标准相关问题：广东省药品不良反应监测中心 张博涵 020-37886057\n程序运行相关问题：佛山市药品不良反应监测中心 蔡权周 0757-82580815 \n\n",)#line:1429
    OO0O00OOO00O0O000 .config (state =DISABLED )#line:1431
def TeasyreadT (O0OOOO000OOOOO000 ):#line:1434
    ""#line:1435
    O0OOOO000OOOOO000 ["#####分隔符#########"]="######################################################################"#line:1438
    O00OOOOO0O0O0O00O =O0OOOO000OOOOO000 .stack (dropna =False )#line:1439
    O00OOOOO0O0O0O00O =pd .DataFrame (O00OOOOO0O0O0O00O ).reset_index ()#line:1440
    O00OOOOO0O0O0O00O .columns =["序号","条目","详细描述"]#line:1441
    O00OOOOO0O0O0O00O ["逐条查看"]="逐条查看"#line:1442
    return O00OOOOO0O0O0O00O #line:1443
def Tget_list (OO0O0O0OO0O0OOO00 ):#line:1448
    ""#line:1449
    OO0O0O0OO0O0OOO00 =str (OO0O0O0OO0O0OOO00 )#line:1450
    OOOOOO0O0OO0O0000 =[]#line:1451
    OOOOOO0O0OO0O0000 .append (OO0O0O0OO0O0OOO00 )#line:1452
    OOOOOO0O0OO0O0000 =",".join (OOOOOO0O0OO0O0000 )#line:1453
    OOOOOO0O0OO0O0000 =OOOOOO0O0OO0O0000 .split (",")#line:1454
    OOOOOO0O0OO0O0000 =",".join (OOOOOO0O0OO0O0000 )#line:1455
    OOOOOO0O0OO0O0000 =OOOOOO0O0OO0O0000 .split ("，")#line:1456
    OO0OO0O0O0OOOOO0O =OOOOOO0O0OO0O0000 [:]#line:1457
    OOOOOO0O0OO0O0000 =list (set (OOOOOO0O0OO0O0000 ))#line:1458
    OOOOOO0O0OO0O0000 .sort (key =OO0OO0O0O0OOOOO0O .index )#line:1459
    return OOOOOO0O0OO0O0000 #line:1460
def thread_it (O00O0O0O0000OOO00 ,*OO0O0O0000OO0OOO0 ):#line:1463
    ""#line:1464
    O00OO00OOOO0O0O00 =threading .Thread (target =O00O0O0O0000OOO00 ,args =OO0O0O0000OO0OOO0 )#line:1466
    O00OO00OOOO0O0O00 .setDaemon (True )#line:1468
    O00OO00OOOO0O0O00 .start ()#line:1470
def showWelcome ():#line:1473
    ""#line:1474
    OOO00OO0OO0000OOO =roox .winfo_screenwidth ()#line:1475
    O0O000000O000O000 =roox .winfo_screenheight ()#line:1477
    roox .overrideredirect (True )#line:1479
    roox .attributes ("-alpha",1 )#line:1480
    OOO0O0OO0O0OOO0O0 =(OOO00OO0OO0000OOO -475 )/2 #line:1481
    O0OOO000O00OO00OO =(O0O000000O000O000 -200 )/2 #line:1482
    roox .geometry ("675x140+%d+%d"%(OOO0O0OO0O0OOO0O0 ,O0OOO000O00OO00OO ))#line:1484
    roox ["bg"]="royalblue"#line:1485
    OO0O0000000O00OO0 =Label (roox ,text ="阅易评",fg ="white",bg ="royalblue",font =("微软雅黑",35 ))#line:1488
    OO0O0000000O00OO0 .place (x =0 ,y =15 ,width =675 ,height =90 )#line:1489
    OO0OOOOOOOO00000O =Label (roox ,text ="                                 广东省药品不良反应监测中心                         V1.7",fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ),)#line:1496
    OO0OOOOOOOO00000O .place (x =0 ,y =90 ,width =675 ,height =50 )#line:1497
def closeWelcome ():#line:1500
    ""#line:1501
    for OOO0OO00OOO0000OO in range (2 ):#line:1502
        root .attributes ("-alpha",0 )#line:1503
        time .sleep (1 )#line:1504
    root .attributes ("-alpha",1 )#line:1505
    roox .destroy ()#line:1506
root =Tk ()#line:1510
root .title ("阅易评 V1.7 20230609")#line:1511
try :#line:1512
    root .iconphoto (True ,PhotoImage (file =peizhidir +"0（范例）ico.png"))#line:1513
except :#line:1514
    pass #line:1515
sw_root =root .winfo_screenwidth ()#line:1516
sh_root =root .winfo_screenheight ()#line:1518
ww_root =700 #line:1520
wh_root =620 #line:1521
x_root =(sw_root -ww_root )/2 #line:1523
y_root =(sh_root -wh_root )/2 #line:1524
root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:1525
root .configure (bg ="steelblue")#line:1526
try :#line:1529
    frame0 =ttk .Frame (root ,width =100 ,height =20 )#line:1530
    frame0 .pack (side =LEFT )#line:1531
    B_open_files1 =Button (frame0 ,text ="导入原始数据",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Topentable ,0 ),)#line:1544
    B_open_files1 .pack ()#line:1545
    B_open_files3 =Button (frame0 ,text ="随机抽样分组",bg ="steelblue",height =2 ,fg ="snow",width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tchouyang ,ori ),)#line:1558
    B_open_files3 .pack ()#line:1559
    B_open_files3 =Button (frame0 ,text ="评估得分统计",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Tpinggu ),)#line:1572
    B_open_files3 .pack ()#line:1573
    B_open_files3 =Button (frame0 ,text ="查看帮助文件",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (helper ),)#line:1586
    B_open_files3 .pack ()#line:1587
    B_open_files1 =Button (frame0 ,text ="更改评分标准",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Topentable ,123 ),)#line:1599
    B_open_files1 =Button (frame0 ,text ="内置数据清洗",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (Txuanze ),)#line:1613
    if usergroup =="用户组=1":#line:1614
        B_open_files1 .pack ()#line:1615
    B_open_files1 =Button (frame0 ,text ="更改用户分组",bg ="steelblue",fg ="snow",height =2 ,width =12 ,font =("微软雅黑",12 ),relief =GROOVE ,activebackground ="lightsteelblue",command =lambda :thread_it (display_random_number ))#line:1627
    if usergroup =="用户组=0":#line:1628
        B_open_files1 .pack ()#line:1629
except :#line:1631
    pass #line:1632
text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF",font ="微软雅黑")#line:1636
text .pack ()#line:1637
text .insert (END ,"\n    欢迎使用“阅易评”，本程序由广东省药品不良反应监测中心联合佛山市药品不良反应监测中心开发，主要功能包括：\n    1、根据报告伤害类型和用户自定义抽样比例对报告表随机抽样；\n    2、根据评估专家数量对抽出报告表随机分组，生成专家评分表；\n    3、根据专家最终评分实现自动汇总统计。\n    本程序供各监测机构免费使用，使用前请先查看帮助文件。\n  \n版本功能更新日志：\n2022年6月1日  支持医疗器械不良事件报告表质量评估(上报部分)。\n2022年10月31日  支持药品不良反应报告表质量评估。  \n2023年4月6日  支持化妆品不良反应报告表质量评估。\n2023年6月9日  支持医疗器械不良事件报告表质量评估(调查评价部分)。\n\n缺陷修正：20230609 修正结果列排序（按评分项目排序）。\n\n注：化妆品质量评估仅支持第一怀疑化妆品。",)#line:1642
text .insert (END ,"\n\n")#line:1643
setting_cfg =read_setting_cfg ()#line:1649
generate_random_file ()#line:1650
setting_cfg =open_setting_cfg ()#line:1651
if setting_cfg ["settingdir"]==0 :#line:1652
    showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:1653
    filepathu =filedialog .askdirectory ()#line:1654
    path =get_directory_path (filepathu )#line:1655
    update_setting_cfg ("settingdir",path )#line:1656
setting_cfg =open_setting_cfg ()#line:1657
random_number =int (setting_cfg ["sidori"])#line:1658
input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:1659
day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:1660
sid =random_number *2 +183576 #line:1661
if input_number ==sid and day_end =="未过期":#line:1662
    usergroup ="用户组=1"#line:1663
    text .insert (END ,usergroup +"   有效期至：")#line:1664
    text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:1665
else :#line:1666
    text .insert (END ,usergroup )#line:1667
text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:1668
peizhidir =str (setting_cfg ["settingdir"])+csdir .split ("pinggutools")[0 ][-1 ]#line:1669
try :#line:1670
    update_software ("pinggutools")#line:1671
except :#line:1672
    pass #line:1673
roox =Toplevel ()#line:1676
tMain =threading .Thread (target =showWelcome )#line:1677
tMain .start ()#line:1678
t1 =threading .Thread (target =closeWelcome )#line:1679
t1 .start ()#line:1680
root .lift ()#line:1681
root .attributes ("-topmost",True )#line:1682
root .attributes ("-topmost",False )#line:1683
root .mainloop ()#line:1684
