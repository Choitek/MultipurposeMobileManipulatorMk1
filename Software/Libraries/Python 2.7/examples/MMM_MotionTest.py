# Load Libraries
from MMM import MMM
from MMM_Speaker import Speaker
import sys
import time
import threading

# Create an MMM
mmm = MMM('COM3');        
speaker = Speaker();
time.sleep(5) # give some time to connect

# Function to run on another thread
def updateRobot():
  while True:
    mmm.clampAll();  
    mmm.update();
    time.sleep(0.1);
    mmm.parseData();
 
#begin thread
thread = threading.Thread(target=updateRobot, args=())
thread.daemon = True            
thread.start()

# initial pose
speaker.speak("I am a robot.")
mmm.setWheelVelocity(0,0)
mmm.rotateShoulders(100,100)
mmm.rotateElbows(-60,-60)
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0)

# Action 0
raw_input("Press Enter.") 
speaker.speak("I am moving.")
mmm.setWheelVelocity(.18,-.18)
time.sleep(5)
mmm.setWheelVelocity(0,0)

# Action 1
raw_input("Press Enter.") 
speaker.speak("Life is wonderful.")
mmm.rotateElbows(60,-60)
mmm.extendArms(.027,0)
  
# Action 2
raw_input("Press Enter.") 
speaker.speak("Bye bye now.")
mmm.ser.close()
quit()