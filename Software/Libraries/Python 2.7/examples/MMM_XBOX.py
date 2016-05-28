from MMM import MMM
import sys
import time
import pygame
import XboxController

# Create an MMM
mmm = MMM('COM3')

# Setup Xbox controller
xboxCont = XboxController.XboxController(
    controllerCallBack = None,
    joystickNo = 0,
    deadzone = 0.3,
    scale = 1,
    invertYAxis = False)
xboxCont.start()

time.sleep(1.5);

# Continuously respond to Xbox360 Controller Input
while(True):
  
  # Quit when pressing back button
  if(xboxCont.BACK):
    xboxCont.stop()
    mmm.ser.close()
    quit()
  
  # reset pose with start
  if(xboxCont.START):
    mmm.reset()
  
  # Control Wheels with DPAD
  (horizontal,vertical) = xboxCont.DPAD
  mmm.leftWheel = (-horizontal + vertical) * 255
  mmm.rightWheel = (horizontal + vertical) * 255
  
  # Boost with A
  if(xboxCont.A):
    mmm.leftWheel = 255
    mmm.rightWheel = 255
  
  # Left Thumbstick
  if(xboxCont.LEFTTHUMB):
    # Control Arm 
    mmm.leftArm -= xboxCont.LTHUMBY*50
  else:
    # Control Shoulder
    mmm.leftShoulder += xboxCont.LTHUMBX*3
    # Control Elbow
    mmm.leftElbow -= xboxCont.LTHUMBY*3
  
  # Right Thumbstick
  if(xboxCont.RIGHTTHUMB):
    # Control Arm 
    mmm.rightArm -= xboxCont.RTHUMBY*50
  else:
    # Control Shoulder
    mmm.rightShoulder -= xboxCont.RTHUMBX*3
    # Control Elbow
    mmm.rightElbow -= xboxCont.RTHUMBY*3
  
  # Activate Left Gripper
  if(xboxCont.LB):
    mmm.setLeftGrippers(180,180,180,180,180)
  else:
    mmm.setLeftGrippers(0,0,0,0,0)
    
  # Activate Right Gripper
  if(xboxCont.RB):
    mmm.setRightGrippers(180,180,180,180,180)
  else:
    mmm.setRightGrippers(0,0,0,0,0)
  
  # Clamp all values to be safe
  mmm.clampAll()  
    
  #send data to robot
  mmm.update()
  
  # Add a short delay
  time.sleep(0.05)
  
  mmm.parseData()
  
  
  