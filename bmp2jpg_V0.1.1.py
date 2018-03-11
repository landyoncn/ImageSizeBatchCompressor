# -*- coding: utf-8 -*-
""" bmp2jpg BMP图片批量转换JPEG图片程序 BY LANDY LASTDATE:2018.03.09

    通常320*240*24b的225k的BMP转成JPG后大约15.6K,压缩比15:1

"""

from PIL import Image
import os
import sys
import datetime
import time

VERSION = "0.1.1"

# 定义可以识别的图片文件类型，可以自行扩充
valid_file_type = ['.BMP', '.bmp']
subDir = 0
isCover = 0
allfile = []
bmp_list = []
inDir = ''
    
# 创建目录
def make_directory(directory):
    os.makedirs(directory)
    
# 判断目录是否存在
def directory_exists(directory):
    if os.path.exists(directory):
        return True
    else:
        return False

# 判断输入是否在指定范围内的正整数            
def CheckDigitRange(idg, min_d, max_d):
    if idg.isdigit():
        if (int(idg) >= min_d) and (int(idg) <= max_d):
            return True
        else:
            return False
    else:
        return False

# 遍历列出目录及子目录下所有文件和目录
def list_all_file(path):
    allfilelist=os.listdir(path)
    for file in allfilelist:
        filepath=os.path.join(path,file)
        if subDir:  # 判断是否包含目录                
            if os.path.isdir(filepath): # 判断是否目录，是则递归
                list_all_file(filepath)
        allfile.append(filepath)
    return allfile

# 筛选出图片文件列表返回
def list_img_file(directory):
    all_list = list_all_file(directory) 
    for filepath in all_list:
        f, e = os.path.splitext(filepath)
        if e in valid_file_type:
            bmp_list.append(filepath)
        else:
            pass
    return bmp_list

# 屏幕显示同步写入日志LOG.TXT
def print_writelog(str_line):
    print (str_line)
    f = open('log.txt','a+') # r只读，w可写，a追加
    f.write(str_line+'\n')
    f.close()    

# bmp转jpeg程序
def bmp2jpg_convert():
    prompt = '\n【确认开始？】确认马上进行转换【直接回车】，输入【 EXIT 回车】放弃压缩并退出本程序！ '
    isOK = input(prompt)
    if isOK.upper() == 'EXIT':
        sys.exit()
    os.system("cls") # windows清屏
    print_writelog ('\n      ============================  BMP图片批量转换JPEG图片程序bmp2jpg，版本号：{}  =========================== '.format(VERSION))
    print_writelog (time.strftime("\nStar Time: %Y-%m-%d %H:%M:%S", time.localtime()))
    starttime = datetime.datetime.now() 
    print_writelog ('\n---- 进度 ---- BMP文件大小 --- JPEG文件大小 --- 转换情况 --- 文件名（后12位） ---')
    bmp_count = 0
    cf_count = 0
    for bmp_name in bmp_list:
        bmp_count += 1
    for s_pfe in bmp_list:
        cf_count += 1
        sfsize = round(os.path.getsize(s_pfe)/1024)
        pf, e = os.path.splitext(s_pfe)
        d_pfe = pf+'.jpg'
        #转换语句
        Image.open(s_pfe).save(d_pfe)
        dfsize = round(os.path.getsize(d_pfe)/1024)
        if isCover: #如果是就删除BMP文件
            os.remove(s_pfe)
        p,fe = os.path.split(d_pfe)
        f,e = os.path.splitext(fe)
        #dpfe = os.path.join(p,fe)        
        print_writelog (' (%5d/%d ) %8d kb   %8d kb           成功    %15s ' %(cf_count, bmp_count, sfsize, dfsize,  f[-12:]))
        
    endtime = datetime.datetime.now()
    print_writelog (time.strftime("\n-End Time: %Y-%m-%d %H:%M:%S", time.localtime()))
    print_writelog (time.strftime("\nUsed Time: %M:%S",time.localtime((endtime - starttime).seconds)))
    print ('\n\n所有BMP图片批量转换完成！【按任意键后程序退出】，转换日志可查看程序目录下的LOG.TXT。')
    input ()
    sys.exit()

           
# 主程序
if __name__ == "__main__":
    os.system("cls") # windows清屏
    print ('\n      ============================  图片批量转换程序（BMP转JPEG）版本号：{}  =========================== '.format(VERSION))
    print ('\n\n > > > > >  1、图片目录信息  < < < < <')
    prompt = '\nBMP图片【输入目录】(可复制粘贴录入): '
    inDir = input(prompt)
    prompt = '\n转换JPEG图片后【确认删除原BMP图片】！）？【删除输入 True 回车，其它则不覆盖】: '
    isCover = input(prompt)
    if isCover.upper() == 'TRUE':
        isCover = 1
    else:
        isCover = 0
    prompt = '\n是/否包含目录下所有【子目录】中的BMP图片文件？【是 输入 True 回车，其它则 否】: '
    subDir = input(prompt)
    if subDir.upper() == 'TRUE':
        subDir = 1
    else:
        subDir = 0
    #列出准备找到的BMP图片数量
    bmp_count = 0
    if directory_exists(inDir):      
        bmp_list = list_img_file(inDir)
        for img_name in bmp_list:
            bmp_count += 1
        if bmp_list:
            print ("\n目录中找到准备进行转换的图片文件共有：  {}  个！".format(bmp_count))
            bmp2jpg_convert()
        else:
            print ("\n目录中没有支持图片文件！ 程序自动退出，请确认无误后再运行本程序。")
    else:
        print ("\n你输入的来源目录不存在！ 程序自动退出，请确认无误后再运行本程序。")
        
