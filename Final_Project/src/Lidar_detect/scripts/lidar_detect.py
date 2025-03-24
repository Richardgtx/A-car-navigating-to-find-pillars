#!/usr/bin/env python3
# coding=utf-8
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

def callback(data):
    move=Twist()
    ranges=data.ranges
    ranges=np.array(data.ranges)
    length=len(ranges)
    pillar=0
    pillar_indices=[]
    for i in range(1,length-1):
        mut=ranges[i+1]-ranges[i-1]
        
        if mut>0.5 and mut<1:
            pillar_indices.append(i)
            pillar=pillar+ranges[i]

    pillar=pillar/len(pillar_indices)
    count=sum(pillar_indices)/len(pillar_indices)
    
    #---
    # valid_ranges=[num for num in ranges if num!=0]
    # pillar=min(valid_ranges)
    # count=ranges.index(pillar)
    ang=data.angle_min+data.angle_increment*count
    rospy.logwarn(f"Pillar dis is {pillar} ang is {ang}")
    #---
    if pillar<0.2:
        pillar=0
        rospy.loginfo("Reach Pillar")   
        return
    move.linear.x=1*np.cos(ang)
    move.linear.y=1*np.sin(ang)
    rospy.loginfo(f"cos(ang)={np.cos(ang)}, sin(ang)={np.sin(ang)}")
    rospy.loginfo(f"linear.x is {move.linear.x} linear.y={move.linear.y}")
    # if min(data.ranges)<0.5:
    #     move.linear.x=x
    #     move.angular.z=0.5
    # else:
    #     move.linear.x=0.2
    #     move.angular.z=0.0
    pub.publish(move)

rospy.init_node('obstacle_avoidance')
pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
rospy.Subscriber('/scan',LaserScan,callback)
rospy.loginfo("Lidar detecting")
rospy.spin()