
import RPi.GPIO as GPIO
import time

import paho.mqtt.publish as publish



GPIO.setmode(GPIO.BCM)
#end push button
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#reset push button
GPIO.setup(14,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#brake input
GPIO.setup(12,GPIO.IN)
# for buzzer
GPIO.setup(21,GPIO.OUT)

while True:
    input_state=GPIO.input(14)
    if input_state==False:
		#starting time
        time1=time.time()
        time.sleep(0.2)
        flag=True
		#initialized score
        score=5000
        while score>0:
            state=GPIO.input(12)
            #if brake pressed we decrease score for every .1 sec as long as the brake is pressed
            if state:
                score=score-10
                time.sleep(0.1)
			# when game ends we break from loop
            end=GPIO.input(10)
            if end==False:
                flag=False
                time.sleep(0.2)
                break
		# final sleep		
        time2=time.time()
        GPIO.output(21,GPIO.HIGH)
		#buzzing for 1 second
        time.sleep(1)
        GPIO.output(21,GPIO.LOW)
		#ip address of the pi
        if flag:
            ans=(int)(time2-time1)
            publish.single("test_channel",
                           "Game Lost: Time Taken: "+str(ans), hostname="192.168.0.102")
        else :
            publish.single("test_channel","Game Won: Score= "+str(score), hostname="192.168.0.102")
            
      

    
    
