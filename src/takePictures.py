#!/usr/bin/env python3
# import the opencv library
import cv2
#Ros
import rospy
from sensor_msgs.msg import Image
    #OpenCV
from cv_bridge import CvBridge
    #Time
from datetime import datetime,timedelta
import numpy as np
import os
import time

class takePictures():
    def __init__(self) -> None:

        self.bridge = CvBridge()
        #Node
        rospy.init_node('take_pictures', anonymous=True)
        #Subsriber
        rospy.Subscriber("/camera/color/image_raw", Image, self.takePicture)
        #Get current time
        self.now = datetime.now()
        #Get params
        self.target     = rospy.get_param('~target', 'default_value')
        self.pictures   = int(rospy.get_param('~pictures', '400'))
        self.start      = int(rospy.get_param('~start', '0'))
        self.counter    = 0
        #Make dir
        try:
            self.parent_dir = os.path.join(os.path.dirname(__file__), self.target)
            os.mkdir(self.parent_dir)
        except:
            pass
        #Spind script
        rospy.spin()
    def  takePicture (self,ros_Image):
        frame = self.bridge.imgmsg_to_cv2(ros_Image, desired_encoding='bgr8')
        cv2.imshow('frame', frame)
        cv2.waitKey(3)
        if (((datetime.now()-self.now )>=timedelta(seconds = 1)) ):
            if(self.counter<self.pictures):
                self.counter = self.counter + 1
                self.now  = datetime.now()
                name = self.parent_dir+"/"+"{:04n}".format(int(self.start + self.counter))+".jpg"
                print(name)
                cv2.imwrite(name, frame) 
            else:
                self.__del__()
        
    def __del__(self):

        # Destroy all the windows
        cv2.destroyAllWindows()

if __name__ == '__main__':
    time.sleep(30) 
    takePictures = takePictures()