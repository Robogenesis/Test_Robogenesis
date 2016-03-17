import urllib
import urllib2
import requests
import time
import webbrowser
import serial
import time
import RPi.GPIO as GPIO

ser = serial.Serial("/dev/ttyUSB0",9600)
ser.timeout = 3
if ser.isOpen():
    print(ser.name + ' is open...')
#gps = "$GPGGA,32,153404.000,A,1912.827725,N,7250.504141,E,0.00,0.00,060316,,E,A"
#the above string is split into a list with ',' as the delimiter
#['$GPGGA', '32', '153404.000', 'A', '1912.827725', 'N', '7250.504141', 'E', '0.00', '0.00', '060316', '', 'E', 'A']
# Location 3 tells us if data is valid or not
# Location 4 Gives us latitude data in deg and minutes
# Location 6 Gives us Longitue data in deg and minutes

#'http://my-demo.in/PotholeDetection/InsertData.aspx?lat=19.2258&lon=72.335'
#####################################################################
def data_tx(one, two):
    url = 'http://my-demo.in/PotholeDetection/InsertData.aspx'#lat=19.2258&lon=72.335'
    data = {}
    data['lat'] = one
    data['lon'] = two

    url_values = urllib.urlencode(data)

    get_url = url + '?' + url_values

    print get_url

    response = urllib2.urlopen(get_url)

    html = response.read()

   # print html
######################################################################
# Get the GPS string from serial port. Extract Latitude data in loc[4]
# Convert the Deg minutes to Deg decimal
# Example 1912.827725    12827725/60 = 21462
# Finally Lat in Deg = 19.21462
######################################################################    
def GetLat( gps):   

    LatLong = gps.split(',')
    #print LatLong[3]

    Lat = LatLong[3].split('.')

    if len (Lat[0]) == 4:
        LatDeg = (Lat[0][2]+Lat[0][3]+Lat[1])
        LatDeg = int (LatDeg)/60
        #print LatDeg
        TrueLat = Lat[0][0]+Lat[0][1]+'.'+str(LatDeg)
        #print TrueLat
    elif len (Lat[0]) == 5:
        LatDeg = (Lat[0][3]+Lat[0][4]+Lat[1])
        LatDeg = int (LatDeg)/60
        #print LatDeg
        TrueLat = Lat[0][0]+Lat[0][1]+Lat[0][2]+'.'+ str(LatDeg)
        #print TrueLat
    return TrueLat

    
######################################################################
# Get the GPS string from serial port.Extract Longitude data in loc[4]
# Convert the Deg minutes to Deg decimal
# Example 7250.504141    50504141/60 = 841735
# Finally Long in Deg = 72.841735
###################################################################### 
def GetLong ( gps):

    LatLong = gps.split(',')
    #print LatLong[5]

    Long = LatLong[5].split('.')
    if len (Long[0]) ==4:
        LongDeg = (Long[0][2]+Long[0][3]+Long[1])
        LongDeg = int (LongDeg) / 60
        #print LongDeg
        TrueLong = Long[0][0]+Long[0][1]+'.'+str(LongDeg)
        #print TrueLong
    elif len (Long[0]) == 5:
        LongDeg = (Long[0][3]+Long[0][4]+Long[1])
        LongDeg = int (LongDeg) / 60
        #print LongDeg
        TrueLong = Long[0][0]+Long[0][1]+Long[0][2]+'.'+ str(LongDeg)
        #print TrueLong
    return TrueLong

######################################################################
#Read Data from Serial and get Lat and Long data
#This function is called only when pothole is detected.
#Keep reading until the GPS data is valid.
#Upload the Valid GPS data
######################################################################
def gps_validata(gps):
    StatusActive = gps.split(',')
    #print StatusActive[2]
    if StatusActive[2] == 'A':
        Latitude = GetLat(gps)
        print Latitude
        Longitude = GetLong(gps)
        print Longitude
        data_tx(Latitude,Longitude)
       # webbrowser.open_new("https://www.google.co.in/maps/@{0},{1},24z".format(Latitude, Longitude))
    
#######################################################################
#s=raw_input("Pothole detected. Answer with Y or N\n");

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25,GPIO.OUT)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

#print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

 
while True:

    time.sleep(3)
 
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    #start = time.time()

    for x in xrange (1,40000,1): # while GPIO.input(GPIO_ECHO)==0:
      time.sleep(0.000001)
      if GPIO.input(GPIO_ECHO)==1:
          break
    for x in xrange (1,60000,1): # while GPIO.input(GPIO_ECHO)==0:
      time.sleep(0.000001)
      if GPIO.input(GPIO_ECHO)==0:
          elapsed = x
          break

   #while GPIO.input(GPIO_ECHO)==1:
      #stop = time.time()

    # Calculate pulse length
    # elapsed = x

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = x*2#elapsed * 34300/1000000

    # That was the distance there and back so halve the value
    # distance = distance / 2

    print "Distance : %.1f" % distance

    # Reset GPIO settings
    #  GPIO.cleanup()

    if distance > 20:
        print"pothhole is detected"
        GPIO.output(25,1)
        

    #if(s=='Y'):
       # print "The location of the pothhole is"
        #webbrowser.open_new("https://www.google.co.in/maps/@{0},{1},24z".format(Latitude, Longitude))
		condition = 1
        while condition == 1
            ReadSerial =  ser.readline()     
			if len(ReadSerial) > 4:
				ReadMode =  ReadSerial.split(',')
			   # print ReadMode
				if ReadMode[0] == '$GNRMC':
					condition = 0
					print ReadSerial
                
            
        gps_validata(ReadSerial)

    else :
        print"pothhole is not detected"
        GPIO.output(25,0)
time.sleep(2)
