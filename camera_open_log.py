########################################################################################
#
#	CopyRight	(C) VIVO,2020		All Rights Reserved!
#
#	Module:		Camera open log save
#
#	File:		camera_open_log.py
#
#	Author:		liuchangjian
#	
#	Date:		2015-10-09
#
#	E-mail:		liuchangjian@vivo.com.cn
#
##########################################################################################

#########################################################################################
#
#	History:
#
#	Name			Date		Ver		Act
#-----------------------------------------------------------------------------------------
#	liuchangjian	2015-10-09	v0.1		create
#	liuchangjian	2015-10-10	v0.1		add platform judge and log switch control
#	liuchangjian	2015-10-12	v0.2		move open log to camera_open_test function. Make sure log must to be open!
#
##########################################################################################

#!/bin/python
import sys,os,string,time
from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage

qcom_hardware='qcom'
sleep_time = 50
loop_count = 1
camera_open_delay = 2
camera_open_time = 2

def Camera_open(device):
	device.shell("am start com.android.camera")
	MonkeyRunner.sleep(1)
	
def Camera_kill_and_start(device):
	MonkeyRunner.sleep(camera_open_time)
	device.shell("am force-stop com.android.camera")
	MonkeyRunner.sleep(camera_open_delay)
	Camera_open(device)

def Camera_back_and_start(device):
	MonkeyRunner.sleep(camera_open_time)
	device.shell("input keyevent KEYCODE_BACK");
	MonkeyRunner.sleep(camera_open_delay)
	Camera_open(device)
	
def Camera_home_and_start(device):
	MonkeyRunner.sleep(camera_open_time)
	device.shell("input keyevent KEYCODE_HOME");
	MonkeyRunner.sleep(camera_open_delay)
	Camera_open(device)

def Camera_kill(device):
	MonkeyRunner.sleep(camera_open_time)
	device.shell("am force-stop com.android.camera")	
	
def clear_log_file(device):
	device.shell("rm -rf /sdcard/mtklog/*")

def qcom_log_close_del(device):
	qcom_log_close(device)
	device.shell("rm -rf /sdcard/bbklog/");
	print "Del bbklog file!!"
	
def mtk_log_close_del(device):
	mtk_log_close(device)
	device.shell("rm -rf /sdcard/mtklog");
	print "Del mtklog file!!"
	
def qcom_log_close(device):
	device.shell("setprop persist.sys.is_bbk_log 0");
	
def mtk_log_close(device):
	device.shell("am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name stop --ei cmd_target 1");

def qcom_log_open(device):
	device.shell("setprop persist.sys.is_bbk_log 2");
	
def mtk_log_open(device):
	device.shell("am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name start --ei cmd_target 1");	
	
def qcom_log_save(device):
	print "Save qcom log!!!"
	os.system("..\\platform-tools\\adb pull /sdcard/bbklog/adb_log/")
	
def mtk_log_save(device):
	print "Save mtk log!!!"
	os.system("..\\platform-tools\\adb pull /sdcard/mtklog/mobilelog/")

def camera_open_test(device):	
	# reboot phone for camera first open	
	print "Phone will reboot!!!"
	device.reboot()
	
	MonkeyRunner.sleep(sleep_time)
	
	# open log
	print "open log:"
	if platform:
		qcom_log_open(device)
	else:
		mtk_log_open(device)

	# first open camera
	print "First open Camera!"
	Camera_open(device)
	
	# open camera
	print "open Camera!"
	Camera_kill_and_start(device)
	
	# back open camera
	print "Back and open Camera!"
	Camera_back_and_start(device)
	
	# home open camera
	print "Home and open Camera!"
	Camera_home_and_start(device)
	
	# close camera
	print "close camera!"
	Camera_kill(device)

if __name__ == '__main__':
	# set cp to dos
	os.system("chcp 437")

	print "Wait for Device Connection..."
	device = MonkeyRunner.waitForConnection()
	
	# judge Platform
	hardware=device.shell("getprop ro.hardware")
	if qcom_hardware in hardware:
		platform=1
		print "Platform is qcom!"
	else:
		platform=0
		print "Platform set to MTK!"
	
	# close camera log ,del log file and reboot
	if platform:
		qcom_log_close_del(device)
	else:
		mtk_log_close_del(device)
	
	cnt=0
	while cnt < loop_count:
		camera_open_test(device)
		cnt = cnt + 1
		
	# close log
	print "close log!"
	if platform:
		qcom_log_close(device)
	else:
		mtk_log_close(device)	
		
	# open log
	print "save camera log:"
	if platform:
		qcom_log_save(device)
	else:
		mtk_log_save(device)	

	