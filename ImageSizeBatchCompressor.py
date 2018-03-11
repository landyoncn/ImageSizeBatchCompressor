# -*- coding: utf-8 -*-
"""ISBC (ImageSizeBatchCompress) 高质量图片尺寸批量压缩程序 BY LANDY LASTDATE:2018.03.08"""

from PIL import Image
import os
import sys
import datetime
import time

VERSION = "0.4.1"

# 定义可以识别的图片文件类型，可以自行扩充
valid_file_type = ['.JPG', '.jpg', '.JPEG', '.jpeg', '.PNG', '.png', '.GIF', '.gif', '.BMP', '.bmp']
#valid_file_type = ['.JPG', '.jpg', '.JPEG', '.jpeg']
subDir = 0
isCover = 0
allfile = []
img_list = []
inDir = ''
outDir = ''
    
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
            img_list.append(filepath)
        else:
            pass
    return img_list

# 屏幕显示同步写入日志LOG.TXT
def print_writelog(str_line):
    print (str_line)
    f = open('log.txt','a+') # r只读，w可写，a追加
    f.write(str_line+'\n')
    f.close()    

# 图片压缩
def ImgCompress(ComMod, opt_1):
    prompt = '\n【确认压缩？】确认马上进行压缩【直接回车】，输入【 EXIT 回车】放弃压缩并退出本程序！ '
    isOK = input(prompt)
    if isOK.upper() == 'EXIT':
        sys.exit()
    os.system("cls") # windows清屏
    print_writelog ('\n      ============================  图片尺寸批量压缩程序ISBC，版本号：{}  =========================== '.format(VERSION))
    print_writelog (time.strftime("\nStar Time: %Y-%m-%d %H:%M:%S", time.localtime()))
    starttime = datetime.datetime.now() 
    print_writelog ('\n----- 进度 ------ 原尺寸 ---- 原文件大小 ---- 新尺寸 ---- 新文件大小 --- 压缩情况 --- 文件名(后12位) ---')
    img_count = 0
    cf_count = 0
    for img_name in img_list:
        img_count += 1
    for pfe in img_list:
        lable_jpg = 0
        sImg = Image.open(pfe)
        f, e = os.path.splitext(pfe)
        if e in ('.JPG', '.jpg', '.JPEG', '.jpeg'):  # 判断是JPG图片时就读取和保留EXIF信息
            try:    # 部分JPEG没有EXIF信息时略过
                sexif = sImg.info['exif']
                lable_jpg = 1
            except KeyError:
                pass
        cf_count += 1
        sfsize = round(os.path.getsize(pfe)/1024)
        srcW, srcH = sImg.size
        # 图片宽高缩小方式判断
        if ComMod == '2':    #按比例压缩图片宽高，（压缩算法，img.thumbnail对图片进行压缩，还可以改变宽高数值进行压缩）
            perc = int(opt_1)
            desW = round(srcW * (perc/100))
            desH = round(srcH * (perc/100))
        else:               #按指定宽高压缩图片
            if srcW >= srcH :
                desW = int(opt_1)
                desH = round(srcH*(desW/srcW))
            else:
                desH = int(opt_1)
                desW = round(srcW * (desH/srcH))
        #压缩语句
        dImg = sImg.resize((desW, desH), Image.ANTIALIAS)
        desw, desh = dImg.size
        p, fe = os.path.split(pfe)
        if isCover:
            dpfe = os.path.join(p,fe)
        else:
            dpfe = os.path.join(outDir,fe)
        if lable_jpg :
            dImg.save(dpfe, exif = sexif) # 保存EXIF信息
        else:
            dImg.save(dpfe)
        dfsize = round(os.path.getsize(dpfe)/1024)
        #print_writelog ('({}/{})   {}   {} x {}    {}     {} x {}    {}   成功 '.format(cf_count, img_count, fn, srcW, srcH, sfsize, desW, desH, dfsize))
        print_writelog (' (%5d/%d ) %6d x %-6d  %5d kb  %6d x %-6d  %5d kb         成功   %15s ' %(cf_count, img_count, srcW, srcH, sfsize, desW, desH, dfsize, dpfe[-12:]))
        
    endtime = datetime.datetime.now()
    print_writelog (time.strftime("\n-End Time: %Y-%m-%d %H:%M:%S", time.localtime()))
    print_writelog (time.strftime("\nUsed Time: %M:%S",time.localtime((endtime - starttime).seconds)))
    print ('\n\n所有图片批量压缩完成！【按任意键后程序退出】，压缩日志可查看程序目录下的LOG.TXT。')
    input ()
    sys.exit()

# 图片压缩选项_1
def ImgComOpt_1(ComMod):
    while True:
        prompt = '\n请输入进行图片尺寸压缩后长边的像素值：【范围100~3200（推荐值 1600）“BACK”回车返回上一选项】'   
        DesImgW = input(prompt)
        if DesImgW.upper() == 'BACK':
            ImgComOpt()
        else:
            if CheckDigitRange(DesImgW, 100, 3200):
                ImgCompress(ComMod, DesImgW)
                break
            else:
                print ('\n你的输入的值有误，请按回车后重新输入正确的值！！！')
                input ()

# 图片压缩选项_2
def ImgComOpt_2(ComMod):
    while True:    
        ComPer = 50
        prompt = '\n请输入进行图片尺寸压缩的百分比数值 【范围5~100（推荐值 50）“BACK”回车返回上一选项】 '
        ComPer = input(prompt)
        if ComPer.upper() == 'BACK':
            ImgComOpt()
        else:
            if CheckDigitRange(ComPer, 5, 100):
                ImgCompress(ComMod, ComPer)
                break
            else:
                print ('\n你的输入的值有误，请按回车后重新输入正确的值！！！')
                input ()

# 图片压缩选项
def ImgComOpt():
    while True:    
        print ('\n\n > > > > >  2、图片压缩选项  < < < < <')
        prompt = '''\n压缩方式: \n  1、指定图片高与宽的像素值进行压缩。
                                \n  2、指定图片高与宽的百分数值进行压缩。\n\n(选择方式 1 或 2 ，默认方式 1 ): '''
        ComMod = input(prompt)
        if ComMod != '2':
            ComMod = '1'
            ImgComOpt_1(ComMod)
            break
        else:
            ComMod = '2'
            ImgComOpt_2(ComMod)
            break
           
# 主程序
if __name__ == "__main__":
    os.system("cls") # windows清屏
    print('''\n      ============================  图片尺寸批量压缩程序ISBC，版本号：{}  =========================== 
             \n                            （所支持图片的格式包括：JPG、JPEG、PNG、GIF、BMP）
             \n\n > > > > >  1、图片目录信息  < < < < <'''.format(VERSION))
    prompt = '\n压缩图片的【输入目录】(可复制粘贴录入): '
    inDir = input(prompt)
    prompt = '\n压缩后的图片【是否覆盖原文件】！）？【是覆盖输入 True 回车，其它则不覆盖】: '
    isCover = input(prompt)
    if isCover.upper() == 'TRUE':
        outDir = inDir
        isCover = 1
    else:
        isCover = 0
        prompt = '\n压缩图片的【输出目录】(可复制粘贴录入): '
        outDir = input(prompt)
    prompt = '\n是/否包含输入目录下【所有子目录】中的图片文件？【是 输入 True 回车，其它则 否】: '
    subDir = input(prompt)
    if subDir.upper() == 'TRUE':
        subDir = 1
    else:
        subDir = 0
    #列出准备进行压缩的图片数量
    img_count = 0
    if directory_exists(inDir):
        if not directory_exists(outDir):
            make_directory(outDir)        
        img_list = list_img_file(inDir)
        for img_name in img_list:
            img_count += 1
        if img_list:
            print ("\n目录中找到将要进行压缩的图片文件共有：  {}  个！".format(img_count))
            ImgComOpt()
        else:
            print ("\n目录中没有支持图片文件！ 程序自动退出，请确认无误后再运行本程序。")
    else:
        print ("\n你输入的输入目录不存在！ 程序自动退出，请确认无误后再运行本程序。")
        
