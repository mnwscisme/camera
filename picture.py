# version:1.0.1905.9051
import gxipy as gx
from PIL import Image
import numpy
import cv2


def main():
	# 打开设备
	# 枚举设备
	device_manager = gx.DeviceManager() 
	dev_num, dev_info_list = device_manager.update_device_list()
	if dev_num == 0:
		sys.exit(1)
	# 获取设备基本信息列表
	str_sn = dev_info_list[0].get("sn")
	# 通过序列号打开设备
	cam = device_manager.open_device_by_sn(str_sn)
	# 导入配置信息
	# cam.import_config_file("./import_config_file.txt")
	# 开始采集
	cam.stream_on()
	
	# 帧率
	fps = cam.AcquisitionFrameRate.get()  
	# 视频的宽高
	size = (int(cam.Width.get()),int(cam.Height.get()))

	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('2.avi',fourcc,fps,size)
	#cv2.namedWindow('origin', flags = cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)

	while (1):
    cap = cam.data_stream[0].get_image()
		cap = cap.convert("RGB")
		frame = cap.get_numpy_array()
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		
		if cap is None:
			continue
		#frame = cv2.flip(frame,1)		
		out.write(frame)
		cv2.imshow('origin', frame)

		if cv2.waitKey(1) == ord('q'):
			break
	cv2.destroyWindow('origin')
	
	# 停止采集
	cam.stream_off()
        #释放
	out.release()
	# close device
	cam.close_device()
	cv2.destroyAllWindows()  

if __name__ == "__main__":
    main()
