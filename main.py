from machine import Pin, PWM      #Klassen für Pins und PWM
from time import sleep            #klassen für sleep

class myPWM(PWM):                 #eigene Klasse die mich den dutycycle nicht
    def __init__(self, pin: Pin): #von 0..65535 sondern 0...100% einstellen lässt
        super().__init__(pin)     #Objname = myPWM(Pin(Nummer))
    def duty(self,d):             #Objname.freq(Frequenz)
        print(65535*d//100)       #Objname.duty(Prozent)
        super().duty_u16(65535*d//100) 

pwm14 = myPWM(Pin(14))              #GPIO Pin für myPWM
pwm14.freq(1000)                    #PWM Frequenz = 1kHz



in0 = Pin(18, Pin.IN,Pin.PULL_DOWN) #GPIO Pin für Input 0
in1 = Pin(19, Pin.IN,Pin.PULL_DOWN) #GPIO Pin für Input 1
in2 = Pin(20, Pin.IN,Pin.PULL_DOWN) #GPIO Pin für Input 2



def getState():                     #lese Status des Wahlrades aus
    get = 0
    if in0.value():
        get = 0
    if in1.value():
        get = 1
    if in2.value():
        get = 2
    
    return get

def writeState(state):             #schreibe etnsprechenden Modus
    if state == 0:
        pwm14.duty(0)
    if state == 1:
        pwm14.duty(50)
    if state == 2:
        pwm14.duty(100)
    print(state)
    
    return 0
        


while True:
    writeState(getState())        #schreibe den Modus, den das Wahlrad vorgibt
    
    
    
    
    
