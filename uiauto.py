import sys
import os
import uiautomator2 as u2
import json
import random
import schedule
import threading
import time
from datetime import datetime, timedelta
import hehe_common

# sudo python3 -m uiautomator2 init   #设备上会多一个uiautomator的应用
# sudo python3 -m weditor

global today_time
global yestoday_time
FLAT_EXIT = False


schedule_task=0 # 0-单次执行该脚本, 1-每天定时执行该脚本,定时时间在main函数中写死01:01
excute_every_time="01:01" #每天的定时执行该脚本的时间

############## 视频配置 ###############
skip_shipin_cache_list=["第一频道","学习视频","联播频道","看电视","看理论","看党史","看慕课","看人物","看文艺","看科学","看自然","看影视","看法治","看军事","网络视听",
"强国通","百灵","电视台","电台","我的"]
shipin_title_list=["第一频道","学习视频","联播频道","看电视","看理论","看党史","看慕课","看人物","看文艺","看科学","看自然","看影视","看法治","看军事","网络视听",]

numbers_of_one_shipin_title=5 #每一个标题栏目下翻页的次数,建议为5
shipin_count_max=10 # 阅读文章上限6分(1篇1分)，需要完整阅读6篇文章+, 建议10
shipin_period_max=24 # 阅读文章时长上限6分(累计3分钟赚取1分), 需要阅读18分钟+, 建议24
shipin_count=0
shipin_starttime = datetime.now()

############## 阅读配置 ###############
skip_cache_list=["综合","推荐","要闻","新思想","北京","上海","直播中国","快闪","发布","实践","订阅","经济","志愿者","教育","体育","人物","大自然",
"科技","技能","理论","文化","读书","党史","电影","传播中国","健康","人事","法纪","国际","十九大时间","纪实","用典","时评","军事","旅游","学习之家",
"强国通","百灵","电视台","电台","我的"]
wenzhang_title_list=["推荐","要闻","新思想","综合","直播中国","快闪","发布","实践","订阅","经济","志愿者","教育","体育","人物","大自然",
"科技","技能","理论","文化","读书","党史","电影","传播中国","健康","人事","法纪","国际","十九大时间","纪实","用典","时评","军事","旅游","学习之家"]

numbers_of_one_wz_title=10  #每一个标题栏目下翻页的次数,建议为10
yuedu_count_max=12 # 阅读文章上限6分(1篇1分)，需要完整阅读6篇文章+, 建议12
yuedu_period_max=18 # 阅读文章时长上限6分(累计2分钟赚取1分), 需要阅读12分钟+, 建议18
yuedu_count=0
yuedu_starttime = datetime.now()

def delay_random(x):
	tempTime = x /10 * random.uniform(1, 10)
	#print(("delay %s s...") % (tempTime))
	time.sleep(tempTime)

def wait_xpath_element_click(d,str_path,wait_period):
	i = 0.0
	step = 0.2
	while True:
		time.sleep(step)
		if d.xpath(str_path).exists:
			d.xpath(str_path).click()
			break
		i += step
		if i > wait_period:
			print("[ERROR] wait too time for : " + str_path)
			break;

def wait_xpath_element_appear(d,str_path,wait_period):
	i = 0.0
	step = 0.2
	while True:
		time.sleep(step)
		if d.xpath(str_path).exists:
			break
		i += step
		if i > wait_period:
			print("[ERROR] wait too time for : " + str_path)
			break;

cache_list=["default","default","default"]
def cache_init(cache_list):
	cache_list[0]="default"
	cache_list[1]="default"
	cache_list[2]="default"
def cache_append(cache_list,buf):
	cache_list[0]=cache_list[1]
	cache_list[1]=cache_list[2]
	cache_list[2]=buf

def is_yuedu_end():
	global yuedu_count
	global yuedu_starttime
	print(("已经阅读了%s s, 阅读篇数：%s") % (str((datetime.now() - yuedu_starttime).seconds),yuedu_count))
	if int((datetime.now() - yuedu_starttime).seconds) >= yuedu_period_max*60 and yuedu_count >=yuedu_count_max:
		print(("阅读时长超过了%s分钟，阅读文章个数也超过了%s个. 退出阅读!!") % (yuedu_period_max,yuedu_count_max))
		return 1
	return 0

def back_xuexi_home(d):
	if d.xpath("//*[@text='我的']").exists and d.xpath("//*[@text='强国通']").exists:
		print("不需要press back")
	else:
		d.press("back")

def yuedu_a_wenzhang(d):
	global yuedu_count
	global yuedu_starttime
	while True:
		time.sleep(4);delay_random(4)
		d.swipe(0.474, 0.8, 0.502, 0.198, 0.3)
		time.sleep(1);delay_random(1)
		if d.xpath("//*[@text='已显示全部观点']").exists or d.xpath("//*[@text='观点']").exists or d.xpath("//*[@text='暂无观点 快来发表观点']").exists:
			print("已经滑动到最底部了")
			yuedu_count +=1
			back_xuexi_home(d)
			break;

def scroll_click_wenzhang_view(d):	

	for scrool_num in range(1,numbers_of_one_wz_title):
		for elem in d.xpath("//android.widget.TextView").all():
			if elem.text not in skip_cache_list:
				cache_append(cache_list,elem.text)
			else:
				continue
			if (elem.text == today_time or elem.text == yestoday_time):
				#elem.click()
				print(cache_list)
				print(("点击 : %s") % (cache_list[0]))
				xpath_buf="//*[@text=\'" + cache_list[0] + "\']"
				
				try:
					d.xpath(xpath_buf).click()
				except:
					xpath_buf="//*[@text=\'" + cache_list[2] + "\']" #如果文章被滑动上方看不见了，则点击时间
					d.xpath(xpath_buf).click()
				time.sleep(0.5);delay_random(0.5)
				
				######## 开始阅读文章 ###########
				
				if d.xpath("//*[@text='欢迎发表你的观点']").exists:
					yuedu_a_wenzhang(d)
				
				######## 阅读结束 ###########
				back_xuexi_home(d)
				if(is_yuedu_end() == 1): #阅读结束
					return
		time.sleep(0.7);delay_random(0.7)
		d(scrollable=True).scroll.vert.forward(steps=100)
		time.sleep(0.7);delay_random(0.7)

	print("=============scroll_click_wenzhang_view exit=================")

def watch_all_wenzhang_title(d):
	global yuedu_starttime
	global yuedu_count
	yuedu_starttime = datetime.now()
	yuedu_count=0
	for title in wenzhang_title_list:
		xpath_buf="//*[@text=\'" + title +"\']"
		print("点击 ： " + xpath_buf)
		d.click(0.94, 0.135) #点击三个横岗
		time.sleep(0.7);delay_random(0.7)
		try:
			d.xpath(xpath_buf).click()
		except:
			d.press("back")
			pass
		time.sleep(0.7);delay_random(0.7)
		
		scroll_click_wenzhang_view(d)
		if(is_yuedu_end() == 1): #阅读结束
			return

############## 视频函数 ###############
def is_shipin_end():
	global shipin_count
	global shipin_starttime
	print(("总共观看了%s s，观看视频篇数：%s") % (str((datetime.now() - shipin_starttime).seconds),shipin_count))
	if int((datetime.now() - shipin_starttime).seconds) >= shipin_period_max*60 and shipin_count >=shipin_count_max:
		print(("观看视频时长超过了%s分钟，观看视频个数也超过了%s个. 退出视频!!") % (shipin_period_max,shipin_count_max))
		return 1
	return 0

def yuedu_a_shipin(d,buf):
	global shipin_count
	global shipin_starttime
	while True:
		time.sleep(2)
		if d.xpath("//*[@text='重新播放']").exists:
			print("(视频播放完成 : %s)" % (buf))
			shipin_count +=1
			back_xuexi_home(d)
			break;

def scroll_click_shipin_view(d):	
	cache_init(cache_list)
	for scrool_num in range(1,numbers_of_one_shipin_title):
		for elem in d.xpath("//android.widget.TextView").all():
			xpath_buf=elem.text
			if len(xpath_buf) == 5:
				if xpath_buf[2] == ":":
					continue
			if elem.text not in skip_shipin_cache_list:
				cache_append(cache_list,elem.text)
			else:
				continue
			if (elem.text == today_time or elem.text == yestoday_time):
				#elem.click()
				print(cache_list)
				print(("点击 : %s") % (cache_list[0]))
				xpath_buf="//*[@text=\'" + cache_list[0] + "\']"
				
				try:
					d.xpath(xpath_buf).click()
				except:
					xpath_buf="//*[@text=\'" + cache_list[2] + "\']" #如果视频被滑动上方看不见了，则点击时间
					d.xpath(xpath_buf).click()
				time.sleep(0.2);delay_random(0.2)
				
				######## 开始观看视频 ###########
				
				if d.xpath("//*[@text='欢迎发表你的观点']").exists:
					yuedu_a_shipin(d, cache_list[0])
				
				######## 阅读结束 ###########
				back_xuexi_home(d)
				if(is_shipin_end() == 1): #阅读结束
					return
		time.sleep(0.7);delay_random(0.7)
		d(scrollable=True).scroll.vert.forward(steps=100)
		time.sleep(0.7);delay_random(0.7)

	print("=============scroll_click_shipin_view exit=================")

def watch_all_shipin_title(d):
	global shipin_starttime
	global shipin_count
	shipin_starttime = datetime.now()
	shipin_count=0

	print(shipin_title_list)
	for title in shipin_title_list:
		xpath_buf="//*[@text=\'" + title +"\']"
		print("点击 ： " + xpath_buf)
		try:
			d.xpath(xpath_buf).click()
		except:
			d.press("back")
			pass
		time.sleep(0.7);delay_random(0.7)
		
		scroll_click_shipin_view(d)
		if(is_shipin_end() == 1): #观看结束
			return

def xuexiqiangguo(username,passwd,name):
	config = hehe_common.common_config()
	d = u2.connect()

	d.app_stop("cn.xuexi.android") 
	d.app_clear('cn.xuexi.android')
	d.app_start("cn.xuexi.android")
	delay_random(5)

	d.implicitly_wait(25)
	print("Try to LogIn...")
	d(resourceId="cn.xuexi.android:id/et_phone_input").send_keys(username);print("Enter your username");delay_random(2) #输入用户名
	d(resourceId="cn.xuexi.android:id/et_pwd_login").send_keys(passwd);print("Enter your secret");delay_random(2) #输入密码
	d(resourceId="cn.xuexi.android:id/btn_next").click();print("Click the LogIn Button");delay_random(2) #点击登录
	
	time.sleep(8);delay_random(4)
	wait_xpath_element_click(d,"//*[@text='我的']",30);delay_random(2)
	wait_xpath_element_click(d,"//*[@text='学习积分']",10);delay_random(2) #点击学习积分

	wait_xpath_element_appear(d,"//*[@text='积分明细']",10);delay_random(2)
	d.press("back");delay_random(2)
	wait_xpath_element_appear(d,"//*[@text='学习积分']",10);delay_random(2)
	d.press("back");delay_random(2)
	
	watch_all_wenzhang_title(d)
	wait_xpath_element_click(d,"//*[@text='电视台']",30);delay_random(2)
	watch_all_shipin_title(d)
	
	d.implicitly_wait(25)
	time.sleep(5)
	d.app_stop("cn.xuexi.android") 
	d.app_clear('cn.xuexi.android')
	d.screen_off()

class usb_install_thread(threading.Thread): # 安装确认
	def init(self):
		threading.Thread.init(self)

	def run(self): # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
		d = u2.connect()
		while True:
			if(FLAT_EXIT == True):
				break
			time.sleep(0.2)
				
			try:
				#if d.exists(text="允许"):
				#	d(resourceId="com.android.packageinstaller:id/permission_allow_button").click() #允许
				if d.exists(text="我知道了"):
					d(resourceId="cn.xuexi.android:id/btn_right_text").click() #我知道了
				if d(description=u"同意").exists:
					d(description=u"同意").click()
				if d.xpath("//*[@text='学习强国隐私权政策']").exists:
					print("消灭弹窗：学习强国隐私政策")
					d.click(0.834, 0.897)
				if d.xpath("//*[@text='立即开启']").exists:
					d.xpath("//*[@text='立即开启']").click()
				if d.xpath("//*[@text='要允许 学习强国 访问以下权限吗？']").exists:  #红米note
					d.xpath("//*[@text='允许']").click()
				if d.xpath("//*[@text='温馨提示']").exists and d.xpath("//*[@text='关闭']").exists:
					d.xpath("//*[@text='关闭']").click()
				
			except:
				pass

def every_day_operation():
	print(("================= (%s) enter =================") % (hehe_common.get_time()))
	delay_random(6)
	config = hehe_common.common_config()
	for dict in config['userlist']:
		print(("######(%s)#######") % (dict['name']))
		try:
			xuexiqiangguo(dict['username'],dict['passwd'],dict['name'])
			delay_random(120)
		except:
			pass

def test():	
	config = hehe_common.common_config()
	d = u2.connect()
	time.sleep(10000)
	
if __name__ == '__main__':
	print(str(sys.argv[0]) + " enter")
	today_time=datetime.now().strftime('%Y-%m-%d')
	yestoday_time=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
	print(yestoday_time)
	
	thread1 = usb_install_thread() #这是点击弹窗的线程
	thread1.start()

	if(str(sys.argv[1]) == "debug"):
		print("===========debug=======")
		test()
	else:
		if schedule_task == 0:
			every_day_operation()
		else:
			schedule.every().day.at(excute_every_time).do(every_day_operation)
			while True:
				schedule.run_pending()
				time.sleep(10)
	FLAT_EXIT = True
