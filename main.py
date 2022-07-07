from machine import Pin, PWM, ADC    #Klassen für GPIO
from time import sleep               #Klassen für sleep


class myPWM(PWM):                 #eigene Klasse die mich den dutycycle nicht
    def __init__(self, pin: Pin): #von 0..65535 sondern 0...100% einstellen lässt
        super().__init__(pin)     #Objname = myPWM(Pin(Nummer))
    def duty(self,d):             #Objname.freq(Frequenz)
        print(65535*d//100)       #Objname.duty(Prozent)
        super().duty_u16(65535*d//100) 
####################################################################
#Pinverwaltung:
        
pwm14 = myPWM(Pin(14))             #GPIO Pin für PowerLED
pwm14.freq(500)                    #PWM Frequenz = 500 Hz

in0 = Pin(18, Pin.IN,Pin.PULL_DOWN) #GPIO Pin für Input 0
in1 = Pin(19, Pin.IN,Pin.PULL_DOWN) #GPIO Pin für Input 1
in2 = Pin(20, Pin.IN,Pin.PULL_DOWN) #GPIO Pin für Input 2

spg26 = ADC(26)                    #ADC Wert für Spannungsüberwachung

temp27 = ADC(27)                    #ADC Wert für Temperaturüberwachung

gruen0 = Pin(10, Pin.OUT)           #GPIO Pin für grün0
gruen1 = Pin(11, Pin.OUT)           #GPIO Pin für grün1
gelb   = Pin(12, Pin.OUT)           #GPIO Pin für gelb
rot    = Pin(13, Pin.OUT)           #GPIO Pin für rot

####################################################################
#Funktionen:

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
    #print(state)
    
    return 0

def readSpg():               #lese GPIO26 aus
    read = spg26.read_u16()
    #print("Spannung: ", read)
    #sleep(0.01)             #aus irgendwelchen Gründen lies er sonst nur Müll
    return read

def writeBat(read):         #schreibe Batteriezustand
    if read > 30000:
       gruen0.on()
       gruen1.on()
       gelb.on()
       rot.on()
    if read < 22500:
       gruen0.off()
       gruen1.on()
       gelb.on()
       rot.on()
    if read < 15000:
       gruen0.off()
       gruen1.off()
       gelb.on()
       rot.on()
    if read < 7500:
       gruen0.off()
       gruen1.off()
       gelb.off()
       rot.on()
    return 0

def batDown():                     #Notprogramm wenn Batterie leer ist
    rot.off()
    sleep(0.5)
    rot.on()
    sleep(0.5)
    return 0

def readTemp():                   #Platinentemp auslesen
    read = temp27.read_u16()
    print("Temperatur: ", read)
    sleep(0.01)                   #ADC bug
    return read

def toHot():                      #wenn Platinentemp zu hoch wird
    for count in range(10): #Dann sinnvolle Zeit aussitzen. 
        gruen0.off()
        gruen1.off()
        gelb.off()
        rot.off()
        
        sleep(0.5)
        
        gruen0.on()
        gruen1.on()
        gelb.on()
        rot.on()
        
        sleep(0.5)
       
        

####################################################################
#main:
while True:
    #Schleife für alles ok
    while True:
        writeState(getState())        #schreibe den Modus, den das Wahlrad vorgibt
        writeBat(readSpg())            #schreibe den gelesenen Batteriezustand
        
        if readSpg() < 1000:           #fällt die Batteriespannung unter kritischen wert
            pwm14.duty(0)             #dann schalte lampe aus
            break
        
        if readTemp() > 30000:       #wenn Platinentemp zu hoch wird
            pwm14.duty(0)             #dann schalte lampe aus
            toHot()                  #und gib gescheid
        
    #Schleife für Akku leer    
    while True:
        batDown()                    #Akku leer, also rot blinken und licht aus
        if readSpg() > 15000:          #Wenn Akku wieder mind halb voll, dann gehts wieder
            break
        
    
  
    
    
    
    
    
    
