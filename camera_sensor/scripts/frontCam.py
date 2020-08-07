#!/usr/bin/env python3
# license removed for brevity
import rospy
import cv2
from std_msgs.msg import String
import numpy as np

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    car = cv2.imread('/home/calm/Pictures/topCar.jpg')
    carsmall = cv2.resize(car, (80, 200), interpolation = cv2.INTER_NEAREST)
    height = 300
    width  = 400
    blank_image = np.zeros((height,width,3), np.uint8)
    blank_image[:,0:width//2] = (255,0,0)      # (B, G, R)
    blank_image[:,width//2:width] = (0,255,0)

    frontcam = cv2.VideoCapture('/home/calm/Downloads/frontCam2.avi')
    backcam = cv2.VideoCapture('/home/calm/Downloads/backCam2.avi')

    src1 = np.float32([[280,426-106], [350,426-106], [400, 425], [0, 425]])
    dst1 = np.float32([[200,0], [400, 0], [400, 199], [200, 199]])
    M1 = cv2.getPerspectiveTransform(src1,dst1)

    src2 = np.float32([[250,253], [350,253], [620, 425], [70, 425]])
    dst2 = np.float32([[200,0], [400, 0], [400, 199], [200, 199]])
    M2 = cv2.getPerspectiveTransform(src2,dst2)   
    
    while not rospy.is_shutdown():
        hello_str = " hello world %s"  % rospy.get_time()
        rospy.loginfo(hello_str)

        ret1, front = frontcam.read()
        ret2, back = backcam.read()
        if (ret1 == True and ret2 == True):
            cv2.imshow("front image",front)
            cv2.imshow("back image",back)
            print(type(front), front.dtype)

            topFront = cv2.warpPerspective(front, M1,(600,200))
            cv2.imshow(" topfront", topFront)

            topBack = cv2.warpPerspective(back, M2,(600,200))
            cv2.imshow(" topback", topBack)

            birdeye = np.zeros([600,600,3], dtype=np.uint8)
            birdeye[0:200,:,:] = topFront
            birdeye[200:400,260:340,:] = carsmall
            birdeye[400:600,:,:] = np.rot90(topBack,2)
            cv2.imshow(" bird", birdeye)
            cv2.waitKey(1)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
