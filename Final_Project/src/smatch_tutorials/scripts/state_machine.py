#!/usr/bin/env python3

import rospy
import smach
from std_msgs.msg import String

# define state Foo
class Move_to_Waypoint(smach.State):
    def __init__(self):
        
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.order=0
    def execute(self, userdata):
        if self.order < 4:
            rospy.loginfo('Moving to Waypoint %d',self.order)
            self.order += 1
            return 'outcome1'
        else:
            return 'outcome2'
    

# define state Bar
class Scanning(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome2'])

    def execute(self, userdata):
        rospy.loginfo('Scanning')
        return 'outcome2'
        



# main
def main():
    rospy.init_node('smach_example_state_machine')

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


if __name__ == '__main__':
    main()