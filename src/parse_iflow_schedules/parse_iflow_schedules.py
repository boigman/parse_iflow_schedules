'''
Created on Mar 30, 2020

@author: 08925
File derived from PowerGREP search "schedule" on H:\HCI\Integration_flows, look inside .zip files, include files="*.iflw"
Copy output text to Notepad++, save as iflow_schedules.txt  
'''
import os,sys
import re
from bs4 import BeautifulSoup as bs 
num_args = len(sys.argv)
filename = sys.argv[1]
outfname = filename.replace("txt","xml")
csvfname = filename.replace("txt","csv")
f = open(filename, 'r+')
fo = open(outfname, 'w+')
my_file_data = f.read().replace("&lt;","<").replace("&gt;",">")
#print(my_file_data)
#regex = r"^\d match.*\s.*Integration_flows\\(.*)\.zip.*\n\s+(<key>.*\n\s+<value.*<\/value>)"
regex = r"^\d match.*\s.*Integration_flows\\(.*)\.zip.*(\s+<bpmn)?.*\s+(<key>.*\n\s+<value.*<\/value>)"
regex = r"^\d match.*\s.*Integration_flows\\(.*)\.zip.*(\s+<bpmn)?.*\s+(<key>.*\n\s+<value.*<\/value>)"
matches = re.finditer(regex, my_file_data, re.MULTILINE)

fo.write('<?xml version="1.0"?>')
#print("<iflows>")
fo.write("<iflows>")
for matchNum, match in enumerate(matches, start=1):
    
#    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
#    x = 2
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        if groupNum ==1:
#            print("<iflow>")
            fo.write("<iflow>")
#            print("<name>"+match.group(groupNum)+"</name>")
            fo.write("<name>"+match.group(groupNum)+"</name>")
#        else:
        elif groupNum ==3:
            
            wongo = match.group(groupNum).replace("                        ","").replace("                    ","").replace("value","xvalue")
#            print(wongo)
            fo.write(wongo)
#            print ("{group}".format(group = match.group(groupNum)))
 #           if groupNum ==2:
#                print("</iflow>")
            fo.write("</iflow>")
#print("</iflows>")
fo.write("</iflows>")
fo.close()
fcsv = open(csvfname, 'w+')
f = open(outfname, 'r+')
my_file_data = f.read()
#print(my_file_data)
f.close()
fcsv.write("name,triggerType,dateType,timeType,onWeekly,hourValue,minutesValue,timeZone,secondValue,fromInterval,toInterval,OnEverySecond,Schedule1\n")

bs_content = bs(my_file_data, "lxml")
for iflow in bs_content.find_all("iflow"):
    xname = ""
    dateType = ""
    onWeekly = ""
    timeType = ""
    hourValue = ""
    minutesValue = ""
    timeZone = ""
    triggerType = ""
    secondValue = ""
    fromInterval = ""
    toInterval = ""
    OnEverySecond = ""
    Schedule1 = ""
    
    result = []
    for name in iflow.find_next("name"):
        print(name)
        xname = name
    for val in iflow.find_all("xvalue"):
        for row in val.find_all("row"):
            result=row.find_all("cell")
            if(result[0].text=='dateType'):
                dateType = result[1].text
            if(result[0].text=='timeType'):
                timeType = result[1].text
            if(result[0].text=='triggerType'):
                triggerType = result[1].text
            if(result[0].text=='onWeekly'):
                onWeekly = result[1].text
            if(result[0].text=='hourValue'):
                hourValue = result[1].text
            if(result[0].text=='minutesValue'):
                minutesValue = result[1].text
            if(result[0].text=='secondValue'):
                secondValue = result[1].text
            if(result[0].text=='timeZone'):
                timeZone = result[1].text
            if(result[0].text=='fromInterval'):
                fromInterval = result[1].text
            if(result[0].text=='toInterval'):
                toInterval = result[1].text
            if(result[0].text=='OnEverySecond'):
                OnEverySecond = result[1].text
            if(result[0].text=='schedule1' and timeType=="TIME_HOUR_INTERVAL"):
                Schedule1 = result[1].text
                indx=Schedule1.find('+?')
                if indx > -1:
                    Schedule1 = Schedule1[:indx]
                while Schedule1.find('0+')>-1:
                    indx=Schedule1.find('0+')
                    Schedule1=Schedule1[indx+2:]
                Schedule1 = '"'+Schedule1+'"'
    fcsv.write(xname+','+triggerType+','+dateType+','+timeType+',"'+onWeekly+'",'+hourValue+','+minutesValue+','+timeZone+','+secondValue+','+fromInterval+','+toInterval+','+OnEverySecond+','+Schedule1+'\n')
fcsv.close()    
                
