# version:1.0.1905.9051
import gxipy as gx
from PIL import Image
import numpy
import cv2

# 枚举设备。dev_info_list 是设备信息列表,列表的元素个数为枚举到的设备个数,列表元素是字典,其中包含设备索引(index)、ip 信息(ip)等设备信息
device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()
if dev_num == 0:
	sys.exit(1)
# 打开设备
# 获取设备基本信息列表
strSN = dev_info_list[0].get("sn")
# 通过序列号打开设备
cam = device_manager.open_device_by_sn(strSN)
# 开始采集
cam.stream_on()
# 获取流通道个数
# 如果 int_channel_num == 1,设备只有一个流通道,列表 data_stream 元素个数为 1
# 如果 int_channel_num > 1,设备有多个流通道,列表 data_stream 元素个数大于 1
# 目前千兆网相机、USB3.0、USB2.0 相机均不支持多流通道。
# int_channel_num = cam.get_stream_channel_num()
# 获取数据
# num 为采集图片次数
num = 10
for i in range(num):
	# 从第 0 个流通道获取一幅图像
	raw_image = cam.data_stream[0].get_image()
	# 从彩色原始图像获取 RGB 图像
	rgb_image = raw_image.convert("RGB")
	if rgb_image is None:
		continue
	# 从 RGB 图像数据创建 numpy 数组
	numpy_image = rgb_image.get_numpy_array()
	if numpy_image is None:
		continue
	# 显示并保存获得的 RGB 图片
	image = Image.fromarray(numpy_image, 'RGB')
	image.show()
	image.save(str(i)+"image.jpg")
# 停止采集,关闭设备
cam.stream_off()
cam.close_device()
