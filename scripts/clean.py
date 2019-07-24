#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x = 0
y = 0
yaw = 0

def poseCallback(pose_message):
    global x
    global y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def move(speed, distance, isForward):
    vel_msg = Twist()
    pose = Pose()

    global x,y
    x0 = x
    y0 = y
    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10)
    velocity_publsher = rospy.Publisher("turtle1/cmd_vel/", Twist, queue_size = 10)

    while True:
        rospy.loginfo("Turtle is moving forward")
        velocity_publsher.publish(vel_msg)

        loop_rate.sleep()

        distance_moved = abs(math.sqrt(math.pow((x-x0), 2) + math.pow((y-y0), 2)))
        print distance_moved

        if not (distance_moved<distance):
            rospy.loginfo("Reached")
            break

    vel_msg.linear.x = 0
    velocity_publsher.publish(vel_msg)


def rotate(angular_speed_degree, relative_angle_degree, clockwise):
    global yaw

    vel_msg = Twist()

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0

    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    theta0 = yaw

    angular_speed = math.radians(abs(angular_speed_degree))

    if(clockwise):
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)

    angle_moved = 0.0
    loop_rate = rospy.Rate(10)
    velocity_publsher = rospy.Publisher("turtle1/cmd_vel/", Twist, queue_size = 10)

    t0 = rospy.Time.now().to_sec()

    while True:
        rospy.loginfo("Turtle rotates")
        velocity_publsher.publish(vel_msg)

        t1 = rospy.Time.now().to_sec()

        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()

        if(current_angle_degree>relative_angle_degree):
            rospy.loginfo("Reached")
            break

    vel_msg.angular.z = 0
    velocity_publsher.publish(vel_msg)

def moveGoal(x_goal, y_goal):
    global x
    global y, yaw

    vel_msg = Twist()
    pose = Pose()
    loop_rate = rospy.Rate(10)
    velocity_publsher = rospy.Publisher("turtle1/cmd_vel/", Twist, queue_size = 10)

    while (True):
        distance = abs(math.sqrt(math.pow((x_goal-x), 2) + math.pow((y_goal-y), 2)))
        speed = 1.2*distance

        desired_angle = (math.atan2(y_goal-y, x_goal-x) - pose.theta)
        angular_speed = 4*desired_angle

        vel_msg.linear.x = speed
        vel_msg.angular.z = angular_speed

        velocity_publsher.publish(vel_msg)

        print "x = ", x, "y = ", y

        if(distance<0.01):
            break

def setDesiredOrientation(desired_angle_radians):
    relative_angle_radians = desired_angle_radians - yaw
    if relative_angle_radians < 0:
        clockwise = 1
    else:
        clockwise = 0
    print relative_angle_radians
    print desired_angle_radians

    rotate(30, math.degrees(abs(relative_angle_radians)), clockwise)

def gridClean():
    pose = Pose()

    loop = rospy.Rate(10)

    pose.x = 1
    pose.y = 1
    pose.theta = 0

    moveGoal(pose.x, pose.y)

    setDesiredOrientation(0)

    move(2.0, 9.0, True)
    rotate(math.radians(20), math.radians(90), False)
    move(2.0, 9.0, True)
    rotate(math.radians(20), math.radians(90), False)
    move(2.0, 1.0, True)
    rotate(math.radians(20), math.radians(90), False)
    move(2.0, 9.0, True)
    rotate(math.radians(30), math.radians(90), True)
    move(2.0, 1.0, True)
    rotate(math.radians(30), math.radians(90), True)
    move(2.0, 9.0, True)
    pass

def spiralClean():
    vel_msg = Twist()
    pose = Pose()

    loop = rospy.Rate(1)
    velocity_publsher = rospy.Publisher("turtle1/cmd_vel/", Twist, queue_size = 10)
    wk = 4
    rk = 0
 
    while((pose.x<10.5) and (pose.y<10.5)):
        rk=rk+1
        vel_msg.linear.x =rk
        vel_msg.linear.y =0
        vel_msg.linear.z =0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z =wk
        
        velocity_publsher.publish(vel_msg)
        loop.sleep()

    vel_msg.linear.x = 0 
    vel_msg.angular.z = 0

    velocity_publsher.publish(vel_msg)






if __name__=="__main__":

    try:
        rospy.init_node("turtlesim_cleaner", anonymous=True)
    
        velocity_publsher = rospy.Publisher("turtle1/cmd_vel/", Twist, queue_size = 10)
        pose_subcriber = rospy.Subscriber("/turtle1/pose", Pose, poseCallback)
    
        time.sleep(2)

        #setDesiredOrientation(math.radians(90))
        #gridClean()
        #moveGoal(2,9)
        spiralClean()

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")


    
    

    
