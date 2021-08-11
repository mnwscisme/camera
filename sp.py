#**************************************************************************#
#       __________          _______       _________       _________        #
#      /_______  /\        /__  __/\     /  ______/\     /  ______/\       #
#      \______/ / /        \_/ /\_\/    /  /\_____\/    /  /\_____\/       #
#           / / /     __    / / /      /  /_/___       /  /_/___           #
#         / / /      / /\  / / /      /  ______/\     /  ______/\          #
#       / /_/____    \ \/_/ / /      /  /\_____\/    /  /\_____\/          #
#     /_________/\    \____/ /      /__/ /          /__/ /                 #
#     \_________\/     \___\/       \__\/           \__\/                  #
#                                                                          #
#                       2021  浙江纺织服装职业技术学院 RoboFuture          #
#**************************************************************************#


#-------------------------------------#
#       调用摄像头
#-------------------------------------#

import gxipy as gx
from PIL import Image
import numpy
import cv2
import datetime
import os

device_manager = gx.DeviceManager()
dev_num,dev_info_list = device_manager.update_device_list()
if dev_num == 0:
 sys.exit(1)
str_sn = dev_info_list[0].get("sn")
cam = device_manager.open_device_by_sn(str_sn)
#.....#


# set continuous acquisition
cam.TriggerMode.set(gx.GxSwitchEntry.OFF)

# set exposure 设置曝光时间
cam.ExposureTime.set(5000.0)

# set gain 设置增益
cam.Gain.set(0.0)



# get param of improving image quality
if cam.GammaParam.is_readable():
	gamma_value = cam.GammaParam.get()
	gamma_lut = gx.Utility.get_gamma_lut(gamma_value)
else:
	gamma_lut = None
if cam.ContrastParam.is_readable():
	contrast_value = cam.ContrastParam.get()
	contrast_lut = gx.Utility.get_contrast_lut(contrast_value)
else:
	contrast_lut = None
if cam.ColorCorrectionParam.is_readable():
	color_correction_param = cam.ColorCorrectionParam.get()
else:
	color_correction_param = 0
#.....#


cam.stream_on()
fps = cam.AcquisitionFrameRate.get()

#根据时间命名文件，防止重命名，导致文件覆盖
def getNameDate(nameIn="output.avi"):
	if not nameIn.endswith(".avi"):
		raise 	ValueError("filename must end on .avi")
	filename =  nameIn.replace(".avi","_{0}.avi").format(datetime.datetime.now().strftime("%Y-%m-%d"))
	if os.path.isfile(filename):
		fn2 = filename[0:-4]+'_{0}.avi'
		count = 1
		while os.path.isfile(fn2.format(count)):
			count += 1
		return fn2.format(count)
	else:
		return filename

def whiteBalance(img):
	r,g,b = cv2.split(img)
	r_avg = cv2.mean(r)[0]		
	g_avg = cv2.mean(g)[0]
	b_avg = cv2.mean(b)[0]
	k = (r_avg + g_avg + b_avg)/3
	kr = k / r_avg
	kg = k / g_avg
	kb = k / b_avg
	r = cv2.addWeighted(src1 = r,alpha = kr,src2 = 0,beta = 0, gamma = 0)
	g = cv2.addWeighted(src1 = g,alpha = kg,src2 = 0,beta = 0, gamma = 0)
	b = cv2.addWeighted(src1 = b,alpha = kb,src2 = 0,beta = 0, gamma = 0)
	balance_img = cv2.merge([b,g,r])
	
	return balance_img

size = (int(cam.Width.get()),int(cam.Height.get()))
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#filename = 'output_{0}.avi'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

#out = cv2.VideoWriter(getNameDate("a.avi"),fourcc,fps,size)

while(1):
	cap = cam.data_stream[0].get_image()
	cap = cap.convert("RGB")
	#cap.image_improvement(color_correction_param=0,contrast_lut = None,gamma_lut = None)
	cap.saturation(64) #Saturation 饱和度:0~128
	cap.sharpen(0.1) #sharpen 锐化:0.1~5.0
	
	frame = cap.get_numpy_array()	
	frame = whiteBalance(frame)
	#frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	
	if frame is None:	
		continue
	#out.write(frame)
	cv2.imshow('origin',frame)
	
	if cv2.waitKey(1) == ord('q'):
		break

cv2.destroyWindow('origin')

cam.stream_off()
#out.release()
cam.close_device()
cv2.destroyAllWindows() 
