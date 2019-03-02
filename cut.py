import cv2                            # importing Python OpenCV
from datetime import datetime         # importing datetime for naming files w/ timestamp
import os

def diffImg(t0, t1, t2):              # Function to calculate difference between images.
	d1 = cv2.absdiff(t2, t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1, d2)
	
def ms_to_str(millis):
	millis = int(millis)
	seconds=(millis/1000)%60
	seconds = int(seconds)
	minutes=(millis/(1000*60))%60
	minutes = int(minutes)
	hours=(millis/(1000*60*60))%24
	return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
	
def handle_exit(cam, in_motion, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str):
	if in_motion == 1:
		print 'end: ' + ms_to_str(cam.get(cv2.CAP_PROP_POS_MSEC))
		os.system(ff_path + ' -ss ' + start_time + ' -i ' + in_file_path + ' -c copy -t ' +  ms_to_str(cam.get(cv2.CAP_PROP_POS_MSEC) - ms_start_time) + ' ' + out_path + '\\' + str(vid_num) + '.avi')
		mrg_str = mrg_str + 'file \'' +  out_path + '\\' + str(vid_num) + '.avi\'\n'
	cam.release()
	
	with open(out_path + '\\out.txt', "w") as text_file:
		text_file.write(mrg_str)
		
	os.system(ff_path + ' -f concat -safe 0 -i ' + out_path + '\\out.txt -c copy ' + out_path + '\\output.avi')
	
	exit()
	
def skip_10_sec(cam, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str):
	fps = cam.get(cv2.CAP_PROP_FPS)
	frames = fps * 15
	i = 0
	while i < frames:
		(g, dimg) = cam.read()
		if not g:
			handle_exit(cam, 1, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
		i = i + 1
  

in_file_path = 'C:\\videos\\14.avi'
threshold = 81500                     # Threshold for triggering "motion detection"
in_motion = 0
cam = cv2.VideoCapture(in_file_path)             # Lets initialize capture on webcam

ff_path='C:\\Users\\reuvenp\\Downloads\\ffmpeg-3.4.2-win64-static\\bin\\ffmpeg.exe'
out_path='C:\\Users\\reuvenp\\Downloads\\p\\out'
vid_num = 1
start_time = ''
ms_start_time = 0
mrg_str = ''


# Read three images first:
(g1, dimg1) = cam.read()
(g2, dimg2) = cam.read()
(g3, dimg3) = cam.read()
if not g1 or not g2 or not g3:
	handle_exit(cam, in_motion, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
t_minus = cv2.cvtColor(dimg1, cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(dimg2, cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(dimg3, cv2.COLOR_RGB2GRAY)
# Lets use a time check so we only take 1 pic per sec
timeCheck = datetime.now().strftime('%Ss')



while True:
	if in_motion == 0:
		if cv2.countNonZero(diffImg(t_minus, t, t_plus)) > threshold and timeCheck != datetime.now().strftime('%Ss'):
			print 'start: ' + ms_to_str(cam.get(cv2.CAP_PROP_POS_MSEC) - 8000)
			if cam.get(cv2.CAP_PROP_POS_MSEC) <= 8000:
				start_time = '00:00:00'
				ms_start_time = 0
			else:
				start_time = ms_to_str(cam.get(cv2.CAP_PROP_POS_MSEC) - 8000)
				ms_start_time = cam.get(cv2.CAP_PROP_POS_MSEC) - 8000
			in_motion = 1
			skip_10_sec(cam, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
			(g1, dimg1) = cam.read()
			(g2, dimg2) = cam.read()
			(g3, dimg3) = cam.read()
			if not g1 or not g2 or not g3:
				handle_exit(cam, in_motion, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
			t_minus = cv2.cvtColor(dimg1, cv2.COLOR_RGB2GRAY)
			t = cv2.cvtColor(dimg2, cv2.COLOR_RGB2GRAY)
			t_plus = cv2.cvtColor(dimg3, cv2.COLOR_RGB2GRAY)
				
		else:
			t_minus = t
			t = t_plus
			(g, dimg) = cam.read()
			if not g:
				handle_exit(cam, in_motion, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
			t_plus = cv2.cvtColor(dimg, cv2.COLOR_RGB2GRAY)
				
	else:
	
		if cv2.countNonZero(diffImg(t_minus, t, t_plus)) > threshold:
			skip_10_sec(cam, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
		
		else:
			in_motion = 0
			print 'end: ' + ms_to_str(cam.get(cv2.CAP_PROP_POS_MSEC))
			os.system(ff_path + ' -ss ' + start_time + ' -i ' + in_file_path + ' -c copy -t ' +  ms_to_str(cam.get(cv2.CAP_PROP_POS_MSEC) - ms_start_time) + ' ' + out_path + '\\' + str(vid_num) + '.avi')
			mrg_str = mrg_str + 'file \'' +  out_path + '\\' + str(vid_num) + '.avi\'\n'
			vid_num = vid_num + 1
			
		
		(g1, dimg1) = cam.read()
		(g2, dimg2) = cam.read()
		(g3, dimg3) = cam.read()
		if not g1 or not g2 or not g3:
			handle_exit(cam, in_motion, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
		t_minus = cv2.cvtColor(dimg1, cv2.COLOR_RGB2GRAY)
		t = cv2.cvtColor(dimg2, cv2.COLOR_RGB2GRAY)
		t_plus = cv2.cvtColor(dimg3, cv2.COLOR_RGB2GRAY)	
				
	
	timeCheck = datetime.now().strftime('%Ss')

	key = cv2.waitKey(1)
	if key == 27:
		break
handle_exit(cam, in_motion, ff_path, start_time, in_file_path, ms_start_time, out_path, vid_num, mrg_str)
