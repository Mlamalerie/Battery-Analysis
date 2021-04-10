# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 18:17:48 2021

Github: https://www.github.com/Mlamalerie

"""
import time,datetime
import pandas as pd
import os
import psutil
nomEmplacementSauvegarde = "G:\\Mon Drive\\Zone de Code Python\\• Mes logiciels Hack\\• Battery Stat\\"




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
  
    print(percent+'% | '+plugged[0]+' | '+now,end=' | ')
    return int(percent),plugged[1]

def DiffTime(a,b):
    time1 = datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S')
    time2 = datetime.datetime.strptime(b,'%Y-%m-%d %H:%M:%S')
    time_delta = (time2 - time1)
    
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds/60
    heures = minutes/60
    return int(heures),int(minutes) #○return en heure
    


def Run(dureeMax,delaySec,n=2000):
    print()
    tabTime = []
    tabPourcentage = []
    tabBoolPlug = []
    distanceH, distanceM = 0,0
    i = 0
    try:
        while i < n and distanceH < dureeMax:
            Hprec = distanceH # pour voir si lheure change
            tabTime.append( returnTime())
            b = returnBattery(tabTime[-1])
            tabPourcentage.append( b[0] )
            tabBoolPlug.append( b[1] )
            i += 1
            distanceH, distanceM = DiffTime(tabTime[0],tabTime[-1])
            
            if distanceH != Hprec: # heure a changé
                Hprec = distanceH
                print("heure a changé")
                data = pd.DataFrame(data={'datetime' : tabTime, '%' : tabPourcentage,'plugged' : tabBoolPlug})
                SaveCSV(data, tabTime[0],tabTime[-1],distanceM)
                
            
            if(distanceM < 120):            
                print(f"minutes={distanceM}")
            else:
                print(f"heures={distanceH}")
            #time.sleep(delaySec*60)
            time.sleep(delaySec*60)
    except:
        data = pd.DataFrame(data={'datetime' : tabTime, '%' : tabPourcentage,'plugged' : tabBoolPlug})
        return data, tabTime[0],tabTime[-1],distanceM
    else:
        data = pd.DataFrame(data={'t' : tabTime, '%' : tabPourcentage,'plugged' : tabBoolPlug})
        return data,tabTime[0],tabTime[-1],distanceM

def recupVar(nomFich):
    try:
        with open(nomFich,"r",encoding="utf-8") as f:
            text = f.read().strip()
            #q = input("???***")
            var = []
            for tex in text.split("\n"):
                var.append([t.strip() for t in tex.split("#")][0][1:-1].strip())
            #q = input("???****")
            res = {}
            for v in var:
                res[v.split(":")[0].strip()[1:-1]] = v.split(":")[1].strip()
                
          
            #q = input("???")
            return int(res['dureeMax']),int(res['delay'])
    except Exception as e:
        print(e)
        print("erreur dans la recupérations des variables..." )
        input()

def SaveCSV(df,a,b,tempsExc):
    
    global nomEmplacementSauvegarde 
    nomEmplacementSauvegarde += "backups"
    if not os.path.exists(nomEmplacementSauvegarde):
    	os.makedirs(nomEmplacementSauvegarde)

    try:
        df.to_csv(r'backups/export_battery ['+returnNameTime(a)+"+"+returnNameTime(b)+ '] (' + str(tempsExc) + ').csv', index = False, header=True)
    except Exception as e:
        print(e)
        print("la création du fichier csv a eu un pb... " )
        input()
    
def main():
    
    dureeMax,delay = recupVar( nomEmplacementSauvegarde+'var.txt')
    #nbPoint = int(input(" # NB DE POINT : "))
    #dureeMax = int(input(" # DUREE MAX (HOUR) : "))
    #delay =  int(input(" # DELAY (MIN) : "))
    print(f"# DUREE MAX (HOUR) : {dureeMax} ")
    print(f"# DELAY (MIN) :  {delay} ")
    
    df,a,b,tempsExc = Run(dureeMax,delay)
    SaveCSV(df,a,b,tempsExc)
 
   
        
if __name__ == "__main__":

    main()


