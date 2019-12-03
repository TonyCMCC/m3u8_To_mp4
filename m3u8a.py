# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 22:31:26 2018

@author: XuLp
"""
import sys
import os
import shutil
import re
from glob import glob
from Crypto.Cipher import AES

#获取需要转换的路径
def get_user_path(argv_dir):
	if os.path.isdir(argv_dir):
		return argv_dir
	elif os.path.isabs(argv_dir):
		return argv_dir
	else:
		return False
#对转换的TS文件进行排序		
def get_sorted_ts(user_path):
    ts_list = glob(os.path.join(user_path,'*'))
    #print(ts_list)
    boxer = []
    for ts in ts_list:
        if os.path.exists(ts):
            #print(os.path.splitext(os.path.basename(ts)))
            file,_ = os.path.splitext(os.path.basename(ts))
            if file != 'k0':                
                boxer.append(file)
    boxer.sort(key=lambda x:int(re.findall('^\d+|\d+$',x)[0]))    
    return os.path.basename(user_path), boxer
#文件合并	
def convert_m3u8(boxer,o_file_name):
	#cmd_arg = str(ts0)+"+"+str(ts1)+" "+o_file_name
	tmp = []
	for ts in boxer:
		tmp.append(str(ts)+'.ts')
	cmd_str = '+'.join(tmp)
	exec_str = "copy /b "+cmd_str+' '+o_file_name
	#print("copy /b "+cmd_str+' '+o_file_name)
	os.system(exec_str)

#根据m3u8文件内容，获取目录和文件名		
def get_files( file_name):
    f = open(file_name, mode='r', encoding='utf-8')
    boxer = []
    parentdir = None
    for line in f.read().splitlines():
        if line[0] is not  '#':
           filename = os.path.basename(line)
           boxer.append(filename)
           if parentdir is None :       
              parentdir = os.path.basename(os.path.dirname(line))
    return parentdir, boxer

#根据m3u8文件生成mp4
    
def deal_m3u8(filename):
    
    i_file = os.path.join(os.getcwd(),filename)
    if os.path.exists(i_file) is False:
        print('输入文件不存在，程序停止运行。')
        exit(0)
        
    if os.path.isdir(i_file):
        print('正在准备处理目录:%s' % filename)
        pardir,boxers = get_sorted_ts(i_file)
    else:
        print('正在准备处理m3u8文件:%s' % filename)
        pardir,boxers = get_files(i_file)
        
    out_file = os.path.splitext(os.path.basename(i_file))[0]+'.mp4'
    
    #获取ts文件目录
    pardir =  os.path.join(os.getcwd(),pardir)    
    key = None
    # 如果目录下有k0,说明有加密，进行加密处理
    if os.path.exists(os.path.join(pardir,'k0')):
        print('检测到加密key,准备读取')
        with open(os.path.join(pardir,'k0')) as file:
            key = file.read()
            print("视频已加密，需解密处理,key:"+ key)
            cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, b'0000000000000000')

    with open(os.path.join(os.getcwd(),out_file), mode = 'wb+') as file:
         print('打开输出文件:%s' % filename)
         for f in boxers:
            filename = os.path.join(pardir,str(f))
            #print('正在准备写入:'+ filename, end="")
            sys.stdout.write('正在准备写入:%s \r' % filename)
            sys.stdout.flush()
            with open(filename,mode = 'rb') as in_file:
                 if key is not None:
                     file.write(cryptor.decrypt(in_file.read()))
                 else:
                     file.write(in_file.read())
    print('\n写入完成!!!')
    print('测试如没有问题,可以删除:'+ pardir)
    print('删除目录:'+ pardir)
    shutil.rmtree(pardir)
    if os.path.exists(i_file):
        print('删除m3u8文件:' + i_file)
        os.remove(i_file)
    print('结束')

if __name__=='__main__':
    argv_len = len(sys.argv)
    if argv_len not in (2,3,4):
        print("参数个数非法:输入文件、输出文件、key文件") 
        print("3个参数 m3u8.py 输入.m3u8 输出文件.mp4 加密key")
        print("2个参数 m3u8.py 输入.m3u8 输出文件.mp4")
        print("1个参数 m3u8.py 输入.m3u8")
        exit(0)
    i_file = None
    if argv_len is 2:
      i_file, = sys.argv[1:]  
      o_file = os.path.splitext(os.path.basename(i_file))[0]+'.mp4'
    if argv_len is 3:
      i_file,o_file =sys.argv[1:]  
    if argv_len is 4:
      i_file,o_file,key =sys.argv[1:]
    if i_file is '.':
        m3u8_list = glob(os.path.join(os.getcwd(),'*.m3u8'))
        for i in m3u8_list:
            deal_m3u8(i)
    else:
       deal_m3u8(i_file)

"""
    user_path = get_user_path(o_dir)
    print(user_path)
    if not user_path:
        print("您输入的路径不正确，:-(" + o_dir) 
        exit(0)
    else:
        if os.path.exists(os.path.join(user_path,o_file_name)):
            print('目标文件已存在，程序停止运行。')
            exit(0)
        os.chdir(user_path)
		#convert_m3u8('2.ts','4.ts',o_file_name)
        boxer = get_sorted_ts(user_path)
        print(boxer)
        convert_m3u8(boxer,o_file_name)
        print(os.getcwd())
"""