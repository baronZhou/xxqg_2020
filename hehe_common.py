#!/usr/bin/python3

#pip3 install wget

import wget
import zipfile
import os
import sys
from ftplib import FTP
from datetime import datetime, timedelta
import struct
import shutil
import xlrd
import xlwt
from xlutils.copy import copy
import json  

#================== excel =====================#
# data = xlrd.open_workbook('excel.xls')
# table = data.sheets()[0]          #通过索引顺序获取
#table = data.sheet_by_index(0) #通过索引顺序获取
#table = data.sheet_by_name(u'Sheet1')#通过名称获取
#table.row_values(i)#返回该行的值，为数组
#table.col_values(i)#返回该列的值，为数组
#table.nrows#行数
#table.ncols#列数
#table.cell(0,0).value #获取单元格
#table.cell(2,3).value

table1_invalid_start_x = 3;
table1_invalid_start_y = 2;
'''
	从excel解析出的是一个列表，每个元素是一个字典。示例如下：
	[{'name': '周贺贺', 'mail': 'hehezhou@asrmicro.com', 'title': 'debug for fingerprint', 'gerritID': 'https://source.asrmicro.com/#/c/27980/', 'period': 'once'}, 
	{'name': '周贺贺1', 'mail': 'hehezhou@asrmicro.com', 'title': 'gatekeeper hal debug', 
	'gerritID': 'https://source.asrmicro.com/#/c/26560/\nhttps://source.asrmicro.com/#/c/26563/', 'period': 'merged'}]
'''
def read_excel_to_dict(excel_path,table_name,use_list):
	try:
		data = xlrd.open_workbook(excel_path)
		table = data.sheet_by_name(table_name)
		print(table.nrows)
		print(table.ncols)
		#print(table.row_values(table1_invalid_start_x))
	
		for ncol in range(table1_invalid_start_x - 1,table.nrows):
			line = table.row_values(ncol)
			#print(line)
			row_dict = {}
			row_dict['name'] = line[table1_invalid_start_y -1 + 0]
			row_dict['mail'] = line[table1_invalid_start_y -1 + 1]
			row_dict['title'] = line[table1_invalid_start_y -1 + 2]
			row_dict['gerritID'] = line[table1_invalid_start_y -1 + 3]
			row_dict['period'] = line[table1_invalid_start_y -1 + 4]
			print(row_dict)
			use_list.append(row_dict)
	except Exception as e:
		return 'error';

def create_sheet(f,table_name,try_count):
	if try_count <= 1:
		return
	try:
		sheet1 = f.add_sheet(table_name + '-' + str(11 - try_count),cell_overwrite_ok=True)
		return sheet1
	except Exception as e:
		return create_sheet(f,table_name,try_count-1)
			
		
def write_dict_to_history_excel(excel_path,table_name,use_list):
	if os.path.exists(excel_path):
		rf = xlrd.open_workbook(excel_path)
		f = copy(rf)
	else:
		f = xlwt.Workbook(excel_path) #新建excel

	try:
		sheet1 = f.add_sheet(table_name,cell_overwrite_ok=True)
	except Exception as e:
		sheet1 = create_sheet(f,table_name,10)
	
	colume_name = ['Name', 'mail','title', 'gerrit id','period']

	for item in range(len(colume_name)):
		sheet1.write(1, item+1, colume_name[item])
	
	i = 0
	for line in use_list:
		sheet1.write(table1_invalid_start_y + i, 1, line['name'])
		sheet1.write(table1_invalid_start_y + i, 2, line['mail'])
		sheet1.write(table1_invalid_start_y + i, 3, line['title'])
		sheet1.write(table1_invalid_start_y + i, 4, line['gerritID'])
		sheet1.write(table1_invalid_start_y + i, 5, line['period'])
		i += 1
	
	f.save(excel_path)

def create_a_new_excel(excel_path,table_name,use_list):
	if os.path.exists(excel_path):
		os.remove(excel_path)
	f = xlwt.Workbook(excel_path) #新建excel
	
	font = xlwt.Font()
	font.bold = True
	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER  #水平方向
	alignment.vert = xlwt.Alignment.VERT_TOP
	style1 = xlwt.XFStyle()
	style1.font = font
	#style1.borders = borders
	style1.alignment = alignment
	
	style2 = xlwt.XFStyle()
	style2.alignment.wrap = 1 #自动换行

	try:
		sheet1 = f.add_sheet(table_name,cell_overwrite_ok=True)
	except Exception as e:
		sheet1 = create_sheet(f,table_name,10)
	
	colume_name = ['Name', 'mail','title', 'gerrit id','period']

	for item in range(len(colume_name)):
		sheet1.write(1, item+1, colume_name[item],style=style1)
	
	sheet1.col(2).width = 256 * (25)
	sheet1.col(3).width = 256 * (35)
	sheet1.col(4).width = 256 * (35)
	
	i = 0
	for line in use_list:
		if(int(line['period']) <= 1):
			continue
		line['period'] = str(int(line['period']) - 1)
		sheet1.write(table1_invalid_start_y + i, 1, line['name'])
		sheet1.write(table1_invalid_start_y + i, 2, line['mail'],style2)
		sheet1.write(table1_invalid_start_y + i, 3, line['title'],style2)
		sheet1.write(table1_invalid_start_y + i, 4, line['gerritID'],style2)
		sheet1.write(table1_invalid_start_y + i, 5, line['period'])
		i += 1
	
	f.save(excel_path)

def get_time(): # 20190620-06:30
	return datetime.now().strftime('%Y%m%d-%H:%M')
def get_month(): # 20190620
	return datetime.now().strftime('%Y%m')
	#- datetime.timedelta(days=1)
def get_day(): # 20190620
	return datetime.now().strftime('%Y%m%d')
def get_yestoday_day(): # 20190620
	return (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
def get_tomorrow_day(): # 20190621
	return (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
	
#================ json =========
def common_config():
	with open('config.json', 'r') as f:
		return json.load(f)

#================== wget =====================#
def wgetFile(data_addr,filename):
	wget.download(data_addr,out=filename)

#================== zip =====================#
def unzipFile(filename):
	f = zipfile.ZipFile(filename,'r')
	for file in f.namelist():
		f.extract(file,"./")

#================== hash =====================#
def getMD5(filename):
	s1 = os.popen(("md5sum %s") % (filename))
	s2 = s1.readlines()[0].split(' ')[0].strip()
	return s2

#================== file =====================#
def rm_dir(path):
	if os.path.exists(path):
		if os.path.isdir(path):
			ls = os.listdir(path)
			for i in ls:
				c_path = os.path.join(path, i)
				if os.path.isdir(c_path):
					rm_dir(c_path) #回调函数
					os.rmdir(c_path)
				else:
					os.remove(c_path)
		else:
			os.remove(path)
	os.rmdir(path)

#================== FTP =====================#
global ftp_use

def init_FTP_account_secret():
	global ftp_use
	config = common_config()
	ftp_use['addr'] = config['secret']['FTP_addr']
	ftp_use['user'] = config['secret']['FTP_username']
	ftp_use['passwd'] = config['secret']['9eLtBmea']
	return ftp_use
	

def d_file_from_ftp(remote_path,filename,bufsize):
	ftp_addr = ftp_use['addr']
	ftp_username = ftp_use['user']
	ftp_passwd = ftp_use['passwd']

	ftp1 = FTP()
	ftp1.connect(ftp_addr)
	ftp1.login(ftp_username,ftp_passwd)

	try:
		FP=open(filename,"wb").write
		ftp1.cwd(remote_path)
		ftp1.retrbinary('RETR ' + filename,FP,bufsize)
		ftp1.close()
	except Exception as e:
		print('\tSome error happen. remote_path='+remote_path+", filename="+filename)

def u_file_to_ftp(remote_path,filename,bufsize):
	ftp_addr = ftp_use['addr']
	ftp_username = ftp_use['user']
	ftp_passwd = ftp_use['passwd']

	ftp1 = FTP()
	ftp1.connect(ftp_addr)
	ftp1.login(ftp_username,ftp_passwd)

	try:
		FP = open(filename, 'rb')
		ftp1.storbinary('STOR ' + remote_path + '/' + filename, FP, bufsize)
		ftp1.set_debuglevel(0)
		FP.close()
	except Exception as e:
		print('\tSome error happen. remote_path='+remote_path+", filename="+filename)

def create_remote_dir(remote_path,new_dir):
	ftp_addr = ftp_use['addr']
	ftp_username = ftp_use['user']
	ftp_passwd = ftp_use['passwd']

	ftp1 = FTP()
	ftp1.connect(ftp_addr)
	ftp1.login(ftp_username,ftp_passwd)
		
	ftp1.cwd(remote_path)
	try:
		ftp1.cwd(new_dir)
		print('\tThe ' + new_dir + ' has been exist.')
	except Exception as e:
		print('\tThe ' + new_dir + ' dir is not exist. Mkdir it.')
		ftp1.mkd(new_dir)

def rm_file_in_ftp(remote_path,filename):
	ftp_addr = ftp_use['addr']
	ftp_username = ftp_use['user']
	ftp_passwd = ftp_use['passwd']

	ftp1 = FTP()
	ftp1.connect(ftp_addr)
	ftp1.login(ftp_username,ftp_passwd)
	
	try:
		ftp1.cwd(remote_path)
		slist = ftp1.nlst()
		if filename in str(ftp1.nlst()):
			ftp1.delete(filename)
	except Exception as e:
		print('\tThe ' + remote_path + ' maybe invalid.')

def rm_files_in_ftp(remote_path):
	ftp_addr = ftp_use['addr']
	ftp_username = ftp_use['user']
	ftp_passwd = ftp_use['passwd']

	ftp1 = FTP()
	ftp1.connect(ftp_addr)
	ftp1.login(ftp_username,ftp_passwd)
	
	try:
		ftp1.cwd(remote_path)
		slist = ftp1.nlst()
		for file in slist:
			ftp1.delete(file)
	except Exception as e:
		print('\tThe ' + remote_path + ' maybe invalid.')

if __name__ == '__main__':
	print(str(sys.argv[0]) + " enter")

