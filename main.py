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
TempHyst = 0                         #Hystereselvl für Temperatur
SpgHyst = 0                          #Hystereselvl für Spannung
minBatVoltage = 10000                 #Batteirespannung wenn alles ok ist
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
    sleep(0.01)             #aus irgendwelchen Gründen lies er sonst nur Müll
    return read

def writeBat(read):         #schreibe Batteriezustand
    print("Schreibe")
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
    pwm14.duty(0)                  #dann schalte lampe aus
    
    gruen0.off()                   #alle leds ausschalten
    gruen1.off()
    gelb.off()
    rot.off()
    
    rot.on()                      #blinken
    sleep(0.5)
    rot.off()
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
    print("gre : ", minBatVoltage)
    print("akt : ", readSpg())
    #sleep(0.5)
#1. Hysteresen
#Temperatur:
    if readTemp() > maxTemp and TempHyst == 0:         #wenn unteres Hystereselevel und maxtemp überschritten wurde:
        maxTemp = 20000                                #neue maxtemp setzten
        TempHyst = 1                                   #neues Hystereselvl setzten
        
    if readTemp() < maxTemp and TempHyst == 1:         #wenn oberes Hysterelevel und maxtemp unterschritten:
        maxTemp = 30000                                #neue maxtemp setzten
        TempHyst = 0                                   #neues Hystereselvl setzten
    
    #Spannung:  
    if readSpg() < minBatVoltage and SpgHyst == 0:    #wenn unteres Hystereselevel und mindest SPG unterschritten wurde:
        minBatVoltage = 15000                         #neue mindest SPG setzten
        SpgHyst = 1                                   #neues Hystereselvl setzten
        
    if readSpg() > minBatVoltage and SpgHyst == 1:    #wenn oberes Hysterelevel und mindest SPG überschritten:
        minBatVoltage = 10000                         #neue mindest SPG setzten
        SpgHyst = 0                                   #neues Hystereselvl setzten

#2. Bedierwarungen ausgeben:       
    if readTemp() > maxTemp:
        toHot()                                        #Temperaturwarnung ausgeben
    
    if readSpg() < minBatVoltage:
        batDown()                                     #Spannungswarung ausgeben

#3. Nur wenn alles ok ist, Licht anschalten und Batteriezustand anzeigen:
    if readSpg() > minBatVoltage and readTemp() < maxTemp:      #benötige Spannung abfragen um blinken zu verhindern
        writeState(getState())        #schreibe den Modus, den das Wahlrad vorgibt
        writeBat(readSpg())            #schreibe den gelesenen Batteriezustand
        #Hier ist noch ein BUG!
        

    
    
    
    
    
