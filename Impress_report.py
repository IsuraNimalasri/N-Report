import pandas as pd
import Queries as esq
from elasticsearch import Elasticsearch
import time
# ===================  Config Panel ====================

# Code
current_date = "2018-01-17"
Tenant = 'mas'
factory_id = 'xxxxo'
es_prot  = 9200
ops_index = ["ncs-xxx-zzzz-2018.01.17"]
ana_index = "ncs-xxx-zvxbxkl"
qc_good =["ftt","rwtogood"]
eff_analysis  = 'rhgrh',
MZone = 19800  #machine time Zone
FZone = 21600  # Factory Time Zone

# Files
MIS_report_Name = "kkkk23-01-2018.xlsx"
kubakuba_Report = factory_id+"_"+current_date+"_Analysis"+".xlsx"
path = 'Data/'+MIS_report_Name



es = Elasticsearch([{"host":"localhost","port":es_prot}])
# ==================================================================

# MIS reading
mis_report  = pd.read_excel(path, sheet_name='MIS Report')
columns = mis_report.columns


data = {}
#  if you need to read new column from MIS file use --->mis_report[columns["pls enter column number"]]
# For example If you need add "smv" value in to your data set  . Key name can be use as "smv" and The value should be
# .Please follow the for commented line in the for loop

def epochCon(MachineZone = 19800,t = time.time(),factoryZone = 19800):
    t = t - (MachineZone*1000)
    t = t + (factoryZone * 1000)
    k = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(t/1000))
    return k

for i in xrange(5,25):
    # data["line" + str(mis_report[columns[1]][i])]['smv'] =mis_report[columns[2]][i]
    data["line" + str(mis_report[columns[1]][i])] = {}
    data["line" + str(mis_report[columns[1]][i])]['MIS'] = mis_report[columns[42]][i]
    if mis_report[columns[1]][i] < 10:
        data["line" + str(mis_report[columns[1]][i])]['Line'] ="line0"+str(mis_report[columns[1]][i])
    else:
        data["line" + str(mis_report[columns[1]][i])]['Line'] = "line" + str(mis_report[columns[1]][i])
    data["line" + str(mis_report[columns[1]][i])]["Date"] =current_date
    data["line" + str(mis_report[columns[1]][i])]['Analytic'] = 0
    data["line" + str(mis_report[columns[1]][i])]['QC'] = 0
    data["line" + str(mis_report[columns[1]][i])]['QC_time'] = 0
    data["line" + str(mis_report[columns[1]][i])]['Analytics_time'] = 0
    data["line" + str(mis_report[columns[1]][i])]["Sessplan_Name"] = ""
    # data["line"+str(mis_report[columns[1]][i])] = mis_report_d

# ===========  Elasticsearch =========================================================

# Get the analytic-(efficiency_analysis) last record  from the database for a particular date for all the lines.

esq.analytic_good_qty['query']['filtered']["filter"]['bool']['must'][0]['term']['factory_id'] = factory_id
esq.analytic_good_qty['query']['filtered']["filter"]['bool']['must'][1]['term']['currentdate'] = current_date
analytic_qty = es.search(index=ana_index,doc_type=eff_analysis,body=esq.analytic_good_qty)

for r1 in analytic_qty['aggregations']['0']['buckets']:
    data[r1['key']]['Analytic'] = r1['1']['buckets'][0]['key']
    # print data[r['key']]


# Get the ops and rwtogood count for the day for all the lines

esq.ops_good_qty['query']['filtered']["filter"]['term']['factory_id'] = factory_id
ops_goods_qty = es.search(index=ops_index,doc_type=qc_good,body=esq.ops_good_qty)

for r2 in ops_goods_qty['aggregations']['0']['buckets']:
    data[r2['key']]['QC'] = r2['1']['value']
    # print data[r2['key']]

#  ============ Get the Last good item hit time From QC ==============================
esq.qc_last_good_item_time['query']['filtered']["filter"]['term']['factory_id'] = factory_id
qc_time = es.search(index=ops_index,doc_type=qc_good,body=esq.qc_last_good_item_time)

for r3 in qc_time['aggregations']['0']['buckets']:
    data[r3['key']]['QC_time'] = epochCon(MZone,r3['1']['buckets'][0]['key'],FZone)
    # print data[r3['key']]

# ============= Get the Last good item hit time From Analytic ==========================
esq.qc_last_good_item_time['query']['filtered']["filter"]['term']['factory_id'] = factory_id
ana_time = es.search(index=ana_index,doc_type=eff_analysis,body=esq.ana_last_good_item_time)

for r4 in ana_time['aggregations']['0']['buckets']:
    data[r4['key']]['Analytics_time'] = epochCon(MZone,r4['1']['buckets'][0]['key'],FZone)
    # print data[r4['key']]

# ========================# Selected session plan ======================

esq.Seesplan['query']['filtered']["filter"]['term']['factory_id'] = factory_id
sessplan = es.search(index=ops_index,doc_type="operations",body=esq.Seesplan)

for r5 in sessplan['aggregations']['0']['buckets']:
    data[r5['key']]['Sessplan_Name'] = r5['1']['buckets'][0]['key']

#====================  Make Data Frame ===================================

df = []
for row in data:
    df.append(data[row])

Final_report  =  pd.DataFrame(df)

Final_report['Diffrence Analytic-QC'] = Final_report["Analytic"] - Final_report['QC']
Final_report['Diffrence Analytic-MIS'] = Final_report["Analytic"] - Final_report['MIS']

Final_report['Reason']  = "No issues "
Final_report = Final_report.sort_values(by=["Line"],ascending=True)

print Final_report
# ===============================END ========================================================

writer = pd.ExcelWriter('Data/'+kubakuba_Report)
Final_report.to_excel(writer,'Report')
writer.save()
