import json
from time import process_time
from pathlib import Path

def main():
    time_start = process_time()
    
    #Iterate through every JSON, do stuff.
    for file in Path('./JSON/Raw JSON/').rglob('*.json'):
        with file.open() as log:
            data = json.load(log)
        
        print('\n', file.name)

        #Build a library with the time the reds occured as a key, and a list of players who baited them
        redBaits = {}
        for mechanics in data['mechanics']:
            if mechanics['name'] == 'Red.B':
                for actor in mechanics['mechanicsData']:
                    if actor['time'] in redBaits:
                        redBaits[actor['time']].append(actor['actor'])
                    else:
                        redBaits[actor['time']] = [actor['actor']]  

        for time in redBaits.keys():
            ellieDied = ellieDead(data, time)
            covertDied = covertDead(data, time)

            #Both HAMS got their reds
            if 'Silas Alder' in redBaits[time] and 'Covertpz' in redBaits[time]:
                print(redBaits[time], 'got their reds at', time/1000, 'seconds.')
            #Covert died, ellie's alive and got her red
            elif 'Silas Alder' in redBaits[time] and covertDied:
                print(redBaits[time], '(Covert died) got reds at', time/1000, 'seconds.')
            #Ellie died, covert's alive and got his red
            elif 'Covertpz' in redBaits[time] and ellieDied:
                print(redBaits[time], '(Ellie died) got reds at', time/1000, 'seconds.')
            #Covert got his red, ellie didn't and didn't die so hers was stolen
            elif 'Covertpz' in redBaits[time] and not ellieDied:
                print(redBaits[time], '(Ellie\'s stolen) got reds at', time/1000, 'seconds.')
            #Ellie got her red, Covert didn't and didn't die so his was stolen
            elif 'Silas Alder' in redBaits[time] and not covertDied:
                print(redBaits[time], '(Covert\'s stolen) got reds at', time/1000, 'seconds.')
            #Neither HAM got their reds, this is if Ellie is alive and covert is dead
            elif not 'Silas Alder' in redBaits[time] and not ellieDied and not 'Covertpz' in redBaits[time] and covertDied:
                print(redBaits[time], '(Covert died, Ellie\'s stolen) got the reds at', time/1000, 'seconds.')
            #Neither HAM got their reds, this is if Covert is alive and ellie is dead
            elif not 'Covertpz' in redBaits[time] and not covertDied and not 'Silas Alder' in redBaits[time] and ellieDied:
                print(redBaits[time], '(Ellie died, Covert\'s stolen) got the reds at', time/1000, 'seconds.')
            elif ellieDead and covertDead:
                print(redBaits[time], '(Ellie and Covert both dead) got reds at', time/1000, 'seconds.')
            #Hopefully that's all the cases, otherwise both the reds were stolen
            else:
                print(redBaits[time][0], 'and', redBaits[time][1], 'both reds stolen at', time/1000, 'seconds.')

    time_stop = process_time()

def covertDead(data, eventTime):
    covertDead = False
    for mechanics in data['mechanics']:
        if mechanics['name'] == 'Dead':
            for actor in mechanics['mechanicsData']:
                if actor['actor'] == 'Covertpz':
                    if actor['time'] < eventTime:
                        covertDead = True
    return covertDead

def ellieDead(data, eventTime):
    ellieDead = False
    for mechanics in data['mechanics']:
        if mechanics['name'] == 'Dead':
            for actor in mechanics['mechanicsData']:
                if actor['actor'] == 'Silas Alder':
                    if actor['time'] < eventTime:
                        ellieDead = True
    return ellieDead

main()