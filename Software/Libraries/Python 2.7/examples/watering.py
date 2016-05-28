'''
python "desktop/assemble tasks/watering.py"
'''

'''
This Script performs the "Watering Plants" task for Multipurpose Mobile Manipulator.
A variable amount of plants are arranged around the robot.
Using its ultrasonic rangefinders, the robot goes around in a circle to water the plants.
The robot goes around in a circle and waters them once by one.
'''

# Load Libraries
from MMM import MMM
from MMM_Speaker import Speaker
import sys
import time
import threading
 
#constants
rot90 = 2.25 # time to rotate 90
ft1 = 2.00 # time to move one foot
waitT = 1.00 # time to wait before going to next plant
waterT = 5.00 # time to water plant
headings = 5 # number of headings to search
speakTime = 2 # time to wait to say something

#variables
range = 100
plantHeight = 15
plantsWatered = 0

# Create an MMM
mmm = MMM('COM3');        
speaker = Speaker();

#Helper speak/print function        
def speakPrint(text):
  speaker.speak(text)
  print(text)  
  time.sleep(speakTime);
                
# --- ROTATE AND WATER HELPER FUNCTIONS --- #

#sweep floor once while moving forward for 3 seconds. 
#Stop and return angle with time moved if found.
def sweep():
  speakPrint("Sweeping!")
  
  #move forward
  mmm.setWheelVelocity(.18,.18)
  mmm.extendArms(0,.127)
  mmm.rotateElbows(60,10)  
  
  #Time
  moveTime = 0;  
  
  #scan floor with right arm for 3 sec, return if found something 
  for x in xrange(30):
    angle = 60+x*2
    mmm.rotateShoulders(0,angle) #counter clock wise
    
    mmm.parseData()
    range = mmm.getRightRange()
    if(range < 70-plantHeight and range > 0): #bump in ground, plant found!
      mmm.setWheelVelocity(.0,.0)
      speakPrint("Plant found!")
      return [angle,moveTime]
    moveTime += 0.05
    time.sleep(0.05)
  for x in xrange(30):
    angle = 120-x*2
    mmm.rotateShoulders(0,angle) #clock wise
    mmm.parseData()
    range = mmm.getRightRange()
    if(range < 70-plantHeight and range > 0): #bump in ground, plant found!
      mmm.setWheelVelocity(.0,.0)
      speakPrint("Plant found!")
      return [angle,moveTime]
    moveTime += 0.05
    time.sleep(0.05)
    
  return [-1,moveTime]; # found nothing

# Opens valve and lowers arm for gravity based watering at angle.
def waterPlant(angle):

  # rotate to watering position
  mmm.setWheelVelocity(0,0) 
  speakPrint("Rotating to watering position...")
  rotTime = 0
  if(angle > 90):
    mmm.setWheelVelocity(-.18,.18) 
    rotTime = rot90 * abs(90.0-angle)/180.0
    time.sleep(rotTime)
  elif(angle < 90):
    mmm.setWheelVelocity(-.18,.18)
    rotTime = rot90 * abs(90.0-angle)/30.0
    time.sleep(rotTime)
  
  #move forward 1 foot
  mmm.setWheelVelocity(0.0,0.0)
  speakPrint("Moving forward 1 foot.")
  mmm.setWheelVelocity(.18,.18)
  time.sleep(ft1)
  
  #stop
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)
    
  # perform watering actions:
  speakPrint("Watering Step 1.")
  mmm.setLeftGrippers(0,0,0,0,0)
  mmm.rotateShoulders(120,120)
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)
 
  speakPrint("Watering Step 2.")
  mmm.setLeftGrippers(90,0,0,0,0)
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)

  speakPrint("Watering Step 3.")
  mmm.rotateElbows(-15,60)  
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waterT)
    
  speakPrint("Watering Step 4.")
  mmm.rotateElbows(60,60)  
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)

  speakPrint("Watering Step 5.")
  mmm.setLeftGrippers(0,0,0,0,0)
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)

  speakPrint("Watering Step 6.")
  mmm.rotateShoulders(0,120)
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)

  #return time spent rotating
  speakPrint("Successfully watered plant.")
  return rotTime
  
# --- MAIN SEQUENCE FOR WATERING 4 PLANTS, SPACED 24in APART STRAIGHT LINE --- #

#give some time to connect
time.sleep(5)              

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

# search through 8 rows
for heading in xrange(headings):
  speakPrint("Beginning sweep at " + str(heading*360/headings) + " degrees...")
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)
  
  #rotate to heading 
  if(heading > 0):
    mmm.setWheelVelocity(-.18,.18)
    time.sleep(rot90*4.0/headings)
    mmm.setWheelVelocity(0,0)
    time.sleep(waitT)
  
  #reset move time
  totalMoveTime = 0;
  found = False;
  
  #search front
  for sweepPass in xrange(2):
    result = sweep()
    angle = result[0]
    moveTime = result[1]
    totalMoveTime += moveTime    
    
    #found something!
    if (angle > -1):
      found = True
      rotTime = waterPlant(angle); #water the plant  
      plantsWatered += 1;
      speakPrint("Reverting rotation.")
      mmm.setWheelVelocity(.18,-.18) #revert any rotation while watering
      time.sleep(rotTime)           
      mmm.setWheelVelocity(0,0) #stop
      time.sleep(waitT)
      break;

  # Plant not found in search
  if(found == False):
    mmm.setWheelVelocity(0,0) #stop
    speakPrint("Plant not found.")  
  
  #move back to origin
  speakPrint("Going back.")
  mmm.setWheelVelocity(-.18,-.18)
  time.sleep(totalMoveTime)    
  mmm.setWheelVelocity(0.0,0.0)
  time.sleep(waitT)
      
#Done
speakPrint("Successfully watered " + str(plantsWatered) + " plants.")
mmm.setWheelVelocity(0.0,0.0)
time.sleep(waitT)
mmm.ser.close()
quit() 