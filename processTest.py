#https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
import psutil
import pandas as pd
def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['name', 'cpu_percent','memory_percent'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return pd.DataFrame.from_dict(listOfProcObjects)

def main():
   
    print('*** Top process with highest memory usage ***')
    data = getListOfProcessSortedByMemory()
    data = data.sort_values(by=['memory_percent'],ascending=False)
    print(data)
    data = data.groupby(['name']).sum()
    data = data.sort_values(by=['memory_percent'],ascending=False)
    select = data.iloc[:5,:]
    print(select,select["memory_percent"].sum())
if __name__ == '__main__':
   main()
   input(">")