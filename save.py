# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 18:17:48 2021

Github: https://www.github.com/Mlamalerie

"""
import time,datetime
import pandas as pd
import os
import psutil

def returnTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def returnNameTime(time):
    aaaa = time.split(" ")[0]
    bbbb = time.split(" ")[1]
    
    h = "".join([ x for x in bbbb.split(':')[0:2] ])
    return aaaa + "-" + h

def returnBattery(now):
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
    plugged = ("Plugged In",1) if plugged else ("Not Plugged In",0)
  
    print(percent+'% | '+plugged[0]+' | '+now)
    return int(percent),plugged[1]

def DiffTime(a,b):
    time1 = datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S')
    time2 = datetime.datetime.strptime(b,'%Y-%m-%d %H:%M:%S')
    time_delta = (time2 - time1)
    
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds/60
    heures = minutes/60
    return int(heures) #○return en heure


def Run(dureeMax,delaySec,n=2000):
    print()
    tabTime = []
    tabPourcentage = []
    tabBoolPlug = []
    distance = 0
    i = 0
    try:
        while i < n and distance < dureeMax:
            
            tabTime.append( returnTime())
            b = returnBattery(tabTime[-1])
            tabPourcentage.append( b[0] )
            tabBoolPlug.append( b[1] )
            i += 1
            distance = DiffTime(tabTime[0],tabTime[-1])
            if i % 100 == 0:
                print(f"ça fait plus de {(distance)} heures que le bail tourne..")
            time.sleep(delaySec*60)
    except:
        data = pd.DataFrame(data={'t' : tabTime, '%' : tabPourcentage,'plugged' : tabBoolPlug})
        return data, tabTime[0],tabTime[-1]
    else:
        data = pd.DataFrame(data={'t' : tabTime, '%' : tabPourcentage,'plugged' : tabBoolPlug})
        return data,tabTime[0],tabTime[-1]

def main():
    #nbPoint = int(input(" # NB DE POINT : "))
    duree = int(input(" # DUREE MAX (HOUR) : "))
    delayMin =  int(input(" # DELAY (MIN) : "))
   
    df,a,b = Run(duree,0.5)
    
    nomEmplacementSauvegarde = "backups"
    if not os.path.exists(nomEmplacementSauvegarde):
    	os.makedirs(nomEmplacementSauvegarde)

    
    df.to_csv (r'backups/export_battery ['+returnNameTime(a)+"+"+returnNameTime(b)+ '].csv', index = False, header=True)

if __name__ == "__main__":
   main()