#!/usr/bin/env python3
# coding=utf-8

import rospy
from std_msgs.msg import String
i=0
des=('1','2','3')
def NavResultCallback(msg):
    rospy.logwarn("Navigation Result=%s",msg.data)
    global i
    
    if msg.data=="done":
        i=(i+1)%3
        rospy.logwarn("Destination=%s",i+1)
        navi_msg=String()
        navi_msg.data=des[i]
        navi_pub.publish(navi_msg)


if __name__=="__main__":
    rospy.init_node("wp_node")

    navi_pub=rospy.Publisher("/waterplus/navi_waypoint",String,queue_size=10)
    res_sub=rospy.Subscriber("/waterplus/navi_result",String,NavResultCallback,queue_size=10)
    navi_msg=String()
    navi_msg.data=des[i]
    navi_pub.publish(navi_msg)
    
    rospy.spin()