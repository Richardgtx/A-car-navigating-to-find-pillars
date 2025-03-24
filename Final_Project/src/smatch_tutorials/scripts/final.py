#!/usr/bin/env python3

import rospy
import smach
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np




# define state Foo
def NavResultCallback(msg):
      
      rospy.loginfo("Navigation Result=%s",msg.data)
    
        
        
class Move_to_Waypoint(smach.State):
    
    def __init__(self):
        self.des=('1','2','3')
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.i=0
        self.navi_pub=rospy.Publisher("/waterplus/navi_waypoint",String,queue_size=10)
        self.res_sub=rospy.Subscriber("/waterplus/navi_result",String,self.NavResultCallback,queue_size=10)
        rospy.loginfo("Move to Waypoint Ready")
        self.recieve_mess=False
        
    def NavResultCallback(self,msg):
        rospy.logwarn("Navigation Result=%s",msg.data)
        if msg.data=="done":
            self.recieve_mess=True

       
            
 
    def execute(self, userdata):
        rospy.loginfo("Move to Waypoint")
        
        if self.i>=3:
            return 'outcome2'
        rospy.logwarn("Destination=%s",self.i+1)
        while not self.recieve_mess:
            self.navi_msg=String()
            self.navi_msg.data=self.des[self.i]
            self.navi_pub.publish(self.navi_msg)
            rospy.logwarn("Navigating")
            rospy.sleep(3)

        rospy.loginfo("Navigation Success")
        if self.i< 3:
            self.i=(self.i+1)
            self.recieve_mess=False
            return 'outcome1'
        
        
    

# define state Barrro
class Scanning(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome2'])
        self.pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.res=rospy.Subscriber('/scan',LaserScan,self.callback)
        self.mess=False
        self.move=Twist()
    def callback(self,data):
        self.laserdata=data
        #---
                
    def execute(self, userdata):
        rospy.loginfo('Scanning')
        while self.mess==False:
            ranges=self.laserdata.ranges
            valid_ranges=[num for num in ranges if num!=0]
            pillar=min(valid_ranges)
            count=ranges.index(pillar)
            ang=self.laserdata.angle_min+self.laserdata.angle_increment*count
            rospy.logwarn(f"Pillar dis is {pillar} ang is {ang}")
            #---
            if pillar<0.3:
                pillar=0
                rospy.loginfo("Reach Pillar")
                rospy.sleep(5)
                rospy.loginfo("Restart")
                self.mess=True
                rospy.logwarn("Scanning Success")
                self.mess=False
                return 'outcome2'
            self.move.linear.x=np.exp(-pillar)*np.cos(ang)
            self.move.linear.y=np.exp(-pillar)*np.sin(ang)
            rospy.loginfo(f"cos(ang)={np.cos(ang)}, sin(ang)={np.sin(ang)}")
            rospy.loginfo(f"linear.x is {self.move.linear.x} linear.y={self.move.linear.y}")

            self.pub.publish(self.move)
            rospy.logwarn("Finding Pillar")
            

        
        

# main
def main():
    rospy.init_node('smach_example_state_machine')
    #<------>
        # rospy.sleep(1)
    #<------>
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['Finished'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('Move_to_Waypoint', Move_to_Waypoint(), 
                               transitions={'outcome1':'Scanning', 
                                            'outcome2':'Finished'})
        smach.StateMachine.add('Scanning', Scanning(), 
                               transitions={'outcome2':'Move_to_Waypoint'})

    # Execute SMACH plan
    outcome = sm.execute()
    rospy.spin()


if __name__ == '__main__':
    main()