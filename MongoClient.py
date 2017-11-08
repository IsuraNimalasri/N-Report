from time import strftime, gmtime
import pandas as pd
from pymongo import MongoClient
import dataSheet as dsheet


# Set MongoDb

try:
    client = MongoClient('localhost',27017)
    db = client.blzdb
    print ('MongoDB is Up & Running .blzdb database is connected')
    # set Collection
    plan = db.plan
    print ('Plan collction is ready')
except:
    print "Please make sure localhost:27017 is up and runnning at that moment"

def today():
    today_ = str(strftime("%Y-%m-%d", gmtime()))
    xdate = today_.split('-')
    day1 = int(xdate[2])+1
    day2 = int(xdate[2])+2
    day3 = int(xdate[2])+3
    today_1 =''
    today_2 ='',
    today_3 = '',
    if day1 < 10:
        day11 = '0'+str(day1)
        today_1 = [xdate[0],xdate[1],day11]
        today_1 = '-'.join(today_1)
    else:
        today_1 = [xdate[0],xdate[1],str(day1)]
        today_1 = '-'.join(today_1)
    if day2 < 10:
        day22 = '0'+str(day2)
        today_2 = [xdate[0],xdate[1],day22]
        today_2 = '-'.join(today_2)
    else:
        today_2 = [xdate[0],xdate[1],str(day2)]
        today_2 = '-'.join(today_2)
    if day3 < 10:
        day33 = '0'+str(day3)
        today_3 = [xdate[0],xdate[1],day33]
        today_3 = '-'.join(today_3)
    else:
        today_3 = [xdate[0],xdate[1],str(day3)]
        today_3 = '-'.join(today_3)

    return today_,today_1,today_2,today_3

report = []

for jf in dsheet.job_function:
    planJobs = {"planname":jf['src'],jf['planned']:today()[jf['gap']]}
    planJobs = dict(planJobs)
    # print planJobs
    numOfplanJobs = plan.find(planJobs).count()
    completedJobs = {"planname":jf['src'],jf['compeleted']:today()[jf['gap']]}
    numOfCompeletJobs = plan.find(completedJobs).count()
    SystemUse = {
        "Job Station":jf['name'],
        "Num planned Jobs":numOfplanJobs,
        'Num Completed Jobs':numOfCompeletJobs
    }
    report.append(SystemUse)

#
fn = "SystemUsage/[SystemUsage]4_" + today()[0] + '.csv'
print fn
df = pd.DataFrame(report)
print df

df.to_csv(fn)