import wiringpi
# import playmusic
import RPi.GPIO as GPIO

class Serial(object):
    def __init__(self):
        

#         self.music = playmusic.MUSIC()

        # default speed
        self.default_speed = 0
        self.speed = self.default_speed

        # motor
        self.STOP = 0
        self.FORWARD = 1
        self.BACKWARD = 2
        self.DIR = 3

        #motor channel
        self.CH1 = 0
        self.CH2 = 1

        #PIN input & output
        self.OUTPUT = 1
        self.INPUT = 0

        #PIN setting
        self.HIGH = 1
        self.LOW = 0

        #Raspberry GPIO setting
        #PWM
        self.ENA = 36 #front wheel
        self.ENB = 33 #rear wheel



        #GPIO PIN
        self.IN1 = 38
        self.IN2 = 40
        self.IN3 = 35
        self.IN4 = 37
        
        GPIO.setmode(GPIO.BOARD)
        
        #SERVO
        self.servoPin = 12
        self.SERVO_MAX_DUTY = 12
        self.SERVO_MIN_DUTY = 3
        self.right = 80
        self.left = 80
        self.center = 80
        

        GPIO.setup(self.servoPin, GPIO.OUT)
        self.servo = GPIO.PWM(self.servoPin, 50)
        self.servo.start(0)
        #wiringpi.wiringPiSetup()

        GPIO.setwarnings(False)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN4, GPIO.OUT)
        self.pwm = GPIO.PWM(self.ENB, 100)
        self.pwm.start(0)
        

    
    #PIN setting function
 #   def setPinConfig(self, EN, INA, INB):
        #wiringpi.pinMode(EN, self.OUTPUT)
        #wiringpi.pinMode(INA, self.OUTPUT)
        #wiringpi.pinMode(INB, self.OUTPUT)
        #wiringpi.softPwmCreate(EN, 0, 255)

        #GPIO.softPwmCreate(EN, 0, 255)



    
  
#    self.pwmA = setPinConfig(ENA, IN1, IN2)
#    self.pwmB = setPinConfig(ENB, IN3, IN4)
    
    #motor control function
    def setMotorControl(self, pwm, INA, INB, speed, stat):
        #motor speed control PWM
        #wiringpi.softPwmWrite(PWM, speed)
        pwm.ChangeDutyCycle(speed)
        
        
        #FORWARD
        if stat == self.FORWARD:
            GPIO.output(INA, self.HIGH)
            GPIO.output(INB, self.LOW)
            #wiringpi.digitalWrite(INA, self.HIGH)
            #wiringpi.digitalWrite(INB, self.LOW)

        #BACKWARD
        elif stat == self.BACKWARD:
            GPIO.output(INA, self.LOW)
            GPIO.output(INB, self.HIGH)
            #wiringpi.digitalWrite(INA, self.LOW)
            #wiringpi.digitalWrite(INB, self.HIGH)

        #STOP
        elif stat == self.STOP:
            GPIO.output(INA, self.LOW)
            GPIO.output(INB, self.LOW)
            #wiringpi.digitalWrite(INA, self.LOW)
            #wiringpi.digitalWrite(INB, self.LOW)

        #elif stat == self.DIR:
            #wiringpi.digitalWrite(INA, self.HIGH)
            #wiringpi.digitalWrite(INB, self.HIGH)
        
    #motor control function_warp
    #ch1 == front
    #ch2 == back
            
        #self.IN1 = 38
        #self.IN2 = 40
        #self.IN3 = 35
        #self.IN4 = 37
            

    def setMotor(self, ch, speed, stat):    
        self.setMotorControl(self.pwm, self.IN3, self.IN4, speed, stat)
            

            
    def setServoPos(self, degree):
        # angle maximum 180
        if degree > 150:
            degree = 150
        
            # angle(degree) -> duty change.
        duty = self.SERVO_MIN_DUTY+(degree*(self.SERVO_MAX_DUTY-self.SERVO_MIN_DUTY)/180.0)
        # angle, duty output
        print("Degree: {} to {}(Duty)".format(degree, duty))

        # change duty output = servo pwm
        self.servo.ChangeDutyCycle(duty)
        
            
            
    def steer(self, data):
        print(data)
#         if data == '60' :
#             print('limit 60')
#             self.speed = 180
#             self.music.play_music('./sounds/limit60.mp3')                
#         elif data == '30' :
#             self.speed = self.default_speed
#             self.music.play_music('./sounds/limit30.mp3')
        if (data == 'w') :
#            self.setMotor(self.CH1, 50, self.DIR)
            self.setMotor(self.CH2, 50, self.FORWARD)
#             if data == 'lw' :
#                 self.music.play_music('./sounds/go.mp3')
        elif data == 'x' :
            self.setMotor(self.CH1, 50, self.DIR)
            self.setMotor(self.CH2, 50, self.BACKWARD)
        elif data == 'a' :
            self.left-=1
            self.setServoPos(self.left)
#             self.setMotor(self.CH1, 255, self.FORWARD)
#             self.setMotor(self.CH2, self.speed, self.FORWARD)
        elif (data == 'd') or (data == 'td') :
            self.right+=1
            self.setServoPos(self.right)
#            if data == 'td' :
#                 self.music.play_music('./sounds/turn_right.mp3')
        elif (data == 's'):
            self.left = 80
            self.right = 80
            self.setMotor(self.CH1, self.speed, self.DIR)
            self.setServoPos(self.center)
            self.setMotor(self.CH2, 0, self.STOP)
#             if data == 's' :
#                 self.music.play_music('./sounds/stop.mp3')
#             elif data == 'us' :
#                 self.music.play_music('./sounds/obs_stop.mp3')
#             elif data == 'ls' :
#                 self.music.play_music('./sounds/light_stop.mp3')
#             elif data == 'ss' :
#                 self.music.play_music('./sounds/wait.mp3')
