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
#Variablen:
minBatVoltage = 1000                 #Batteirespannung wenn alles ok ist
maxTemp = 30000                      #maximale Temperatur wenn alles ok ist

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
    pwm14.duty(0)             #dann schalte lampe aus
    
    
    rot.off()                 #blinken
    sleep(0.5)
    rot.on()
    sleep(0.5)
    return 0

def readTemp():                   #Platinentemp auslesen
    read = temp27.read_u16()
    #print("Temperatur: ", read)
    sleep(0.01)                   #ADC bug
    return read

def toHot():                      #wenn Platinentemp zu hoch wird
    pwm14.duty(0)             #dann schalte lampe aus
    for count in range(3): #3x blinken
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
    if readSpg() > minBatVoltage:      #benötige Spannung abfragen um blinken zu verhindern
        writeState(getState())        #schreibe den Modus, den das Wahlrad vorgibt
        
    writeBat(readSpg())            #schreibe den gelesenen Batteriezustand
    
    print("Max temp: ", maxTemp)
    print("akt temp: ", readTemp())
    
    if readSpg() < minBatVoltage:   #fällt die Batteriespannung unter kritischen wert
        minBatVoltage = 15000     #erhöhe mindestspannung
        batDown()                 #rot blinken, kritischen Wert erhöhen und Licht aus
        

    
    if readTemp() > maxTemp:       #wenn Platinentemp zu hoch wird
        maxTemp = 20000           #maximal Temperatur erniedirgen
        toHot()                  #und gib gescheid
    


    
  
    
    
    
    
    
    
