import header
####################################################################
#main:
while True:
    #print("gre : ", minBatVoltage)
    #print("akt : ", readSpg())
    #sleep(0.5)
#1. Hysteresen
#Temperatur:
    if header.readTemp() > header.maxTemp and header.TempHyst == 0:         #wenn unteres Hystereselevel und maxtemp überschritten wurde:
        header.maxTemp = 20000                                #neue maxtemp setzten
        header.TempHyst = 1                                   #neues Hystereselvl setzten
        
    if header.readTemp() < header.maxTemp and header.TempHyst == 1:         #wenn oberes Hysterelevel und maxtemp unterschritten:
        header.maxTemp = 30000                                #neue maxtemp setzten
        header.TempHyst = 0                                   #neues Hystereselvl setzten
    
    #Spannung:  
    if header.readSpg() < header.minBatVoltage and header.SpgHyst == 0:    #wenn unteres Hystereselevel und mindest SPG unterschritten wurde:
        header.minBatVoltage = 15000                         #neue mindest SPG setzten
        header.SpgHyst = 1                                   #neues Hystereselvl setzten
        
    if header.readSpg() > header.minBatVoltage and header.SpgHyst == 1:    #wenn oberes Hysterelevel und mindest SPG überschritten:
        header.minBatVoltage = 10000                         #neue mindest SPG setzten
        header.SpgHyst = 0                                   #neues Hystereselvl setzten

#2. Bedierwarungen ausgeben:       
    if header.readTemp() > header.maxTemp:
        header.toHot()                                        #Temperaturwarnung ausgeben
    
    if header.readSpg() < header.minBatVoltage:
        header.batDown()                                     #Spannungswarung ausgeben

#3. Nur wenn alles ok ist, Licht anschalten und Batteriezustand anzeigen:
    if header.readSpg() > header.minBatVoltage and header.readTemp() < header.maxTemp:      #benötige Spannung abfragen um blinken zu verhindern
        header.writeState(header.readState())        #schreibe den Modus, den das Wahlrad vorgibt
        header.writeSpg(header.readSpg())            #schreibe den gelesenen Batteriezustand
        #Hier ist noch ein BUG!
        

    
    
    
    
    
