#!/usr/bin/env python

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import cv2

'''
http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
http://atagan-memo.blogspot.jp/2012/11/opencvai-ballwifi.html
http://venuschjp.blogspot.jp/2015/02/pythonopencvweb.html
'''

DEBUG = True
DEFAULT_IP_ADDRESS = '192.168.2.1'
DEFAULT_NODE_NAME = 'web_cam'
DEFAULT_TOPIC_NAME = 'web_cam_img'


class WebCamManager:
    def __init__(self, _ipaddress, _topicname):
        self.cvbridge = CvBridge()
        self.capture = cv2.VideoCapture('http://' + _ipaddress + '/?action=stream.mjpeg')
        self.topicname = _topicname

    def open(self):
        return self.capture.isOpened()

    def init_publisher(self):
        self.pub_image = rospy.Publisher(self.topicname, Image)

    def publish_img(self):
        has_image, cv_image = self.capture.read()
        if has_image == False:
            print('fail to grub image')
        try:
            self.pub_image.publish(self.cvbridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError, e:
            print e

# --------------------------------------------
if __name__ == '__main__':
    rospy.init_node(DEFAULT_NODE_NAME, anonymous=True)
    rate_mgr = rospy.Rate(30)  # Hz
    web_cam_ip = rospy.get_param('~ip_address', DEFAULT_IP_ADDRESS)

    if (DEBUG): print('initializing...')
    web_cam = WebCamManager(web_cam_ip, DEFAULT_TOPIC_NAME)
    if (DEBUG): print('initialized!')

    if not web_cam.open():
        print('fail to open!')
    else:
        if (DEBUG): print('run!')
        while not rospy.is_shutdown():
            web_cam.publish_img()
            rate_mgr.sleep()



