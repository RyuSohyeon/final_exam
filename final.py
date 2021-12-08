from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#센서에 연결한 Trig와 Echo 핀의 핀 번호 설정 
TRIG = 23
ECHO = 24
btn_pin = 15
open = 0
print("Distance measurement in progress")

#Trig와 Echo 핀의 출력/입력 설정 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# 버튼 핀의 입력설정 , PULL DOWN 설정 
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

#Trig핀의 신호를 0으로 출력 
GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

while True: 			     
    GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
    time.sleep(0.00001)       # 10µs 딜레이 
    GPIO.output(TRIG, False)
        
    while GPIO.input(ECHO)==0:
        start = time.time()	 # Echo 핀 상승 시간 
    while GPIO.input(ECHO)==1:
        stop= time.time()	 # Echo 핀 하강 시간 
            
    check_time = stop - start
    distance = check_time * 34300 / 2
    
@app.route("/")
def home():
    return render_template('final.html')

@app.route("distance/")
def button_callback(channel):
    print("!")
    global open   # Global 변수선언 
    open = open + 1
    if open == 1: 
        #print("Distance : %.1f cm" % distance)
        print("!")
    time.sleep(0.4)	# 0.4초 간격으로 센서 측정 
    return 0

if __name__ == "__main__":
    app.run(host="0.0.0.0")