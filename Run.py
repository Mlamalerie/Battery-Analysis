# -*- coding: utf-8 -*-


import time,datetime
import pandas as pd
import os,sys
import psutil

from plyer import notification

def intro():
    print('''BATTERRY BACKUPS - Created by Mlamali SAID SALIMO
    github:- https://github.com/Mlamalerie
    Email:- nassim.saidsalimo@gmail.com\n''')

def exit(code):
    print('\nExiting....')
    print('\nPasse une excellente journée bogosse.')
    sys.exit(code)


#LEDOSSIER = os.getcwd()
LEDOSSIER = "G:/Mon Drive/Zone de Code Python/• Mes logiciels Hack/• Battery Stat"



def CreerDossierSauvegarde(ou,doss):
    nomEmplacementSauvegarde = ou + "/" + doss
    if not os.path.exists(nomEmplacementSauvegarde):
        os.mkdir(nomEmplacementSauvegarde)
        return nomEmplacementSauvegarde
    else:
        return nomEmplacementSauvegarde


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
    #notify()
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
                notify(tabPourcentage[-1],tabBoolPlug[-1])
            
                
            
            if(distanceM < 120):            
                print(f"minutes={distanceM}")
            else:
                print(f"heures={distanceH}")
                
            notify(tabPourcentage[-1],tabBoolPlug[-1],True) # notifier si le chargeur est branché
            
            data = pd.DataFrame(data={'datetime' : tabTime, '%' : tabPourcentage,'plugged' : tabBoolPlug})
            SaveCSV(data, tabTime[0],tabTime[-1],delaySec)
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

def SaveCSV(df,a,b,delai):

    try:
        filename = LEDOSSIER + r'/backups/export_battery ['+returnNameTime(a)+'] (' + str(delai) + ').csv'
        df.to_csv(filename, index = False, header=True,sep =";")
        print("saved.")
    except Exception as e:
        print(e)
        print(f"la création du fichier {filename} a eu un pb... " )


def notify(p=None,plug=None,OkCTrop = None):
    image = LEDOSSIER + "/img/icon.ico"
    if(OkCTrop):
        if int(p) > 95 and plug == 1:
             notification.notify(title = "Débranche le chargeur !",message="Eh la batterie ! " +str(p) + "% ..",timeout=10,app_icon=image)
    elif p or plug:
        notification.notify(title = "Rappel : Battery Stat en cours d'execution... ",message=str(p) + "% Battery remaining",timeout=10,app_icon=image)
    else:
         notification.notify(title = "Battery Stat",message="Go.. !",timeout=10,app_icon=image)
        
def main():
    intro()
    dureeMax,delay = recupVar( LEDOSSIER +'/var.txt')

    CreerDossierSauvegarde(LEDOSSIER,"backups")
    #nbPoint = int(input(" # NB DE POINT : "))
    #dureeMax = int(input(" # DUREE MAX (HOUR) : "))
    #delay =  int(input(" # DELAY (MIN) : "))
    print(f"# DUREE MAX (HOUR) : {dureeMax} ")
    print(f"# DELAY (MIN) :  {delay} ")
    
    df,a,b,tempsExc = Run(dureeMax,delay)
    
    #SaveCSV(df,a,b,delay)
    exit(0)
 
   
        
if __name__ == "__main__":

    main()


