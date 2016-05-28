from MMM import MMM
from MMM_Speaker import Speaker
import sys
import time

# Create an MMM
mmm = MMM('COM3')
speaker = Speaker()

# defined variables
rot90 = 2.25 # time to rotate 90
d12 = 2      # time to move 12 inches

# initial pose
mmm.setWheelVelocity(0,0)
mmm.rotateShoulders(100,100)
mmm.rotateElbows(-60,-60)
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0)
mmm.update();  

#usage info
print("Welcome to the robot commander.\n")
print("To make the robot move, type in commands in this format:\n")
print("[L] rotates left 90 degrees.")
print("[R] rotates right 90 degrees.")
print("[F] moves the robot forward.")
print("[B] moves the robot backward.\n")

#Continuously ask for input
while(True):
  commands = raw_input("Type Commands and press Enter.")

  for i in xrange(len(commands)):
    command = commands[i].upper()
    if(command == 'L'): # rotate left
      speaker.speak("Rotating left.");
      mmm.setWheelVelocity(.18,-.18)
      mmm.update()  
      time.sleep(rot90)
    elif(command == 'R'): # rotate right
      speaker.speak("Rotating right.");
      mmm.setWheelVelocity(-.18,.18)
      mmm.update()
      time.sleep(rot90)
    elif(command == 'F'): # move forward
      speaker.speak("Moving forward.");
      mmm.setWheelVelocity(.18,.18)
      mmm.update()
      time.sleep(rot90)
    elif(command == 'B'): # move backward
      speaker.speak("Moving backward.");
      mmm.setWheelVelocity(-.18,-.18)
      mmm.update()
      time.sleep(rot90)
    elif(command == 'Q'): # quit
      mmm.ser.close()
      quit()  

  #stop the robot when done parsing commands      
  mmm.setWheelVelocity(0,0)
  mmm.update()
  
