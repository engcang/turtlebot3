# Turtlebot3 Simple Lane Keeping using OpenCV
+ ROS version and OpenCV version codes are available to get image in different ways
+ Please attach github URL when you use my code! 코드를 사용시 링크를 첨부해주세요!
+ Each folders and branches has its own README.md which is A to Z explanation in detail 
+ 각각의 폴더와 브런치들에 자세한 README.md(설명)이 별도로 있습니다.
</br></br><br>

## Necessary
+ [HSV convert and Line Detect](https://github.com/engcang/Opencv_tutorial_Matlab_and_python/blob/master/HSD_cvt_LSD_Python)
<br><br>

## Robot - Turtlebot3 from ROBOTIS
+ [Turtlebot3](http://emanual.robotis.com/docs/en/platform/turtlebot3/overview/) </br>
<br>

## Code explanation 
***

### ● After image HSV converted and masked, Line detect
  ~~~python
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
  ~~~
  <br>
  
  1.Used [HSV convert and Line Detect](https://github.com/engcang/Opencv_tutorial_Matlab_and_python/blob/master/HSD_cvt_LSD_Python) as it is <br>
<br>

### ● Turn or Straight
  ~~~python
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
  ~~~
  <br>
  
  2.If **LSD.detect** returned line doesn't exist, turn to that side<br><br>
  3.Else, go straight <br><br>
  4.That's it <br><br>

### ● Result clip, I also used this code at '[R-BIZ Challenge Turtlebot3 Autorace](http://emanual.robotis.com/docs/en/platform/turtlebot3/autonomous_driving/#autonomous-driving)'
<p align="">
<img src="https://github.com/engcang/image-files/blob/master/opencv/Turtlebot3_LaneKeeping.gif" />
</p>
