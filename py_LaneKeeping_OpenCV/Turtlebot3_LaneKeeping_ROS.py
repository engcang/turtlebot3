#!/usr/bin/env python
"""
Created on Fri Nov  9 10:25:22 2018

@author: mason
"""
'''libraries'''
import time
import numpy as np
import rospy
import roslib
import cv2
import sys
import signal

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import CompressedImage
from tf.transformations import euler_from_quaternion, quaternion_from_euler

global LSD
LSD = cv2.createLineSegmentDetector(0)

def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

''' class '''
class robot():
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.pose_subscriber = rospy.Subscriber('/odom', Odometry, self.callback_pose)
        self.img_subscriber = rospy.Subscriber('/raspicam_node/image/compressed',CompressedImage,self.callback_img)

    def callback_img(self,data):
        np_arr = np.fromstring(data.data, np.uint8)
        self.image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV >= 3.0:
        
    def callback_pose(self, data):
        self.pose = data.pose.pose.position
        self.orient = data.pose.pose.orientation
        orientation_list = [self.orient.x, self.orient.y, self.orient.z, self.orient.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        self.theta = yaw
            
    def keeping(self,hsv):
        global LSD
        vel_msg=Twist()
        crop_L=hsv[350:410,40:220]
        crop_R=hsv[350:410,402:582]
        L_mask = cv2.inRange(crop_L,(21,50,100),(36,255,255))
        L2_mask = cv2.inRange(crop_L,(36,0,165),(255,255,255))
        R_mask = cv2.inRange(crop_R,(36,0,165),(255,255,255))
        R2_mask = cv2.inRange(crop_R,(21,50,100),(36,255,255))
      
        yello_line = LSD.detect(L_mask)
        yello_line2 = LSD.detect(L2_mask)
        white_line = LSD.detect(R_mask)
        white_line2 = LSD.detect(R2_mask)
        if yello_line[0] is None and yello_line2[0] is None:
            vel_msg.linear.x = 0.05
            vel_msg.angular.z = 0.6
        elif white_line[0] is None and white_line2[0] is None:
            vel_msg.linear.x = 0.05
            vel_msg.angular.z = -0.6
        else :
            vel_msg.linear.x = 0.2
            vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

    def imageupdate(self):
        image=self.image_np
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        return image,hsv
        
turtle=robot()
time.sleep(1.2)
if __name__=='__main__':
    while 1:
        try:
            img,hsv=turtle.imageupdate()
            turtle.keeping(hsv) 
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
        except :
           print('got error')
