from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse



import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
# from appscript import app, k
# from mactypes import Alias
from pathlib import Path
from datetime import datetime,timedelta

import pandas as pd
pd.set_option('display.precision',3)

from datetime import datetime
import numpy as np
from datetime import timedelta

from IPython.display import display,Javascript,Markdown
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import FileLink, FileLinks , HTML

from pandas.api.types import CategoricalDtype

import matplotlib.pyplot as plt
#%matplotlib inline
# display(HTML("<style>.container {width:100% !important;}</style>"))
import warnings
warnings.simplefilter("ignore")
import pdb;

import seaborn as sns

from tabulate import tabulate

import pymysql as MySQLdb
import pandas as pd
import json
import pandas as pd
import requests
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime,timedelta
import calendar

def convertDataFramesToJson(inputSet):
    newJsonSet = {}
    for key,value in inputSet.items():
        newJsonSet[key] = value.to_json(orient = "split")
        
    return newJsonSet

def get_meter_list(request):
    site_name=request.GET.get('site_name', None)
    meter_list=get_meter_names(site_name)
    print(meter_list)
    return JsonResponse(meter_list,safe=False)

def get_summary_table_report(request):
    site_name=request.GET.get('site_name', None)
    #return JsonResponse({"site": site_name},safe=False)
    summary_report=get_summary_table(site_name)
    print(summary_report)
    return JsonResponse(convertDataFramesToJson(summary_report),safe=False)

def get_alert_report(request):

    alert_analyse=request.GET.get('alert_analyse', None)
    phase=request.GET.get('phase', None)
    site_name=request.GET.get('site_name', None)

    start_date=pd.to_datetime(request.GET.get('start_date', None))
    end_date=pd.to_datetime(request.GET.get('end_date', None))
    threshold=float(request.GET.get('threshold', None))

    # first graph 
    mainOutput=main(alert_analyse,phase,start_date,end_date,threshold,site_name)
    jsonOutput = convertDataFramesToJson(mainOutput)
    return JsonResponse(jsonOutput)

def get_deep_dive_report(request):
    # alert_analyse="Abnormal Change in Energy Consumption"
    alert_analyse=request.GET.get('alert_analyse', None)
    # phase='Main 1 L1 ( kWh )'
    phase=request.GET.get('phase', None)
    site_name=request.GET.get('site_name', None)

    start_date=pd.to_datetime(request.GET.get('start_date', None))
    end_date=pd.to_datetime(request.GET.get('end_date', None))
    threshold=float(request.GET.get('threshold', None))
    alert_no=int(request.GET.get('alert_no', None))
    main_deep_dive_output=main_deep_dive(alert_analyse,phase,site_name,start_date,end_date,alert_no,threshold)
    jsonOutput = convertDataFramesToJson(main_deep_dive_output)
    return JsonResponse(jsonOutput)


def api_main(request):
    alert_analyse=request.GET.get('alert_analyse', None)
    phase=request.GET.get('phase', None)
    #ans=request.GET.get('ans', None) # Deep Dive Yes/No
    #alert_no=int(request.GET.get('alert_no', None))
    threshold=int(request.GET.get('threshold', None))
    site_name=request.GET.get('site_name', None)
    start_date=pd.to_datetime(request.GET.get('start_date', None))
    end_date=pd.to_datetime(request.GET.get('end_date', None))
    
    read_data(alert_analyse,site_name,start_date,end_date)

    

    mainOutput=main(alert_analyse,phase,start_date,end_date,threshold)
    print(mainOutput)
    jsonOutput = convertDataFramesToJson(mainOutput)
    #print(jsonOutput)
    return JsonResponse(jsonOutput)

def api_main_deep_dive_output(request):
    alert_analyse=request.GET.get('alert_analyse', None)
    phase=request.GET.get('phase', None)
    ans="YES" # Deep Dive Yes/No
    alert_no=1
    threshold=int(request.GET.get('threshold', None))
    site_name=request.GET.get('site_name', None)
    start_date=pd.to_datetime(request.GET.get('start_date', None))
    end_date=pd.to_datetime(request.GET.get('end_date', None))
    
    read_data(alert_analyse,site_name,start_date,end_date)
    mainOutput=main(alert_analyse,phase,start_date,end_date,threshold)
    main_deep_dive_output=main_deep_dive(alert_analyse,ans,alert_no,threshold)
    print(main_deep_dive_output)
    jsonOutput = convertDataFramesToJson(main_deep_dive_output)
    #print(jsonOutput)

    return JsonResponse(jsonOutput)

def index(request):
    print(request.GET)    
    alert_analyse="Abnormal Change in Energy Consumption"
    phase='Main 1 L1 ( kWh )'


    # alert_analyse="Voltage Imbalance"
    site_name='site-lcc-oxford-circus-65297'
    start_date=pd.to_datetime("2021-08-01 00:00:00")
    end_date=pd.to_datetime("2021-08-31 23:59:59")

    read_data(alert_analyse,site_name,start_date,end_date)

    threshold=0

    mainOutput=main(alert_analyse,phase,start_date,end_date,threshold)
    print(mainOutput)
    jsonOutput = convertDataFramesToJson(mainOutput)


    return JsonResponse(jsonOutput)
    return JsonResponse({"username":request.GET.get('end_date', None)})
    alert_analyse=request.GET.get('alert_analyse', None)
    phase=request.GET.get('phase', None)
    ans=request.GET.get('ans', None) # Deep Dive Yes/No
    alert_no=int(request.GET.get('alert_no', None))
    threshold=float(request.GET.get('threshold', None))

    # thresholds
    # voltage =2
    # pf=0.9
    # current=10

    # alert_analyse="Voltage Imbalance"
    site_name=request.GET.get('site_name', None)
    start_date=pd.to_datetime(request.GET.get('start_date', None))
    end_date=pd.to_datetime(request.GET.get('end_date', None))



    # alert_analyse="Abnormal Change in Energy Consumption"
    # phase='Main 1 L1 ( kWh )'
    # ans="YES" # Deep Dive Yes/No
    # alert_no=1
    # threshold=0

    # # thresholds
    # # voltage =2
    # # pf=0.9
    # # current=10

    # # alert_analyse="Voltage Imbalance"
    # site_name='site-lcc-oxford-circus-65297'
    # start_date=pd.to_datetime("2021-08-01 00:00:00")
    # end_date=pd.to_datetime("2021-08-31 23:59:59")
    read_data(alert_analyse,site_name,start_date,end_date)
    output = main(alert_analyse,phase,start_date,end_date,ans,alert_no,threshold)
    
    jsonOutput = convertDataFramesToJson(output)
        
    return JsonResponse(jsonOutput)





# Alerts Generation

def generate_alert_report(df,variable,threshold,name_of_the_variable,case,obs_count):
    start=datetime.datetime.now()

    df['Flag']=0
    if case=="greater":
        df.loc[df[variable]>threshold,'Flag']=1  
    else:
        df.loc[df[variable]<threshold,'Flag']=1  
    df['Alert Log']="No Alert"
    count=0
    add=[]
    z=0
    
    for i in range(obs_count,df['Flag'].shape[0]):
        j=i-obs_count
        while j< i:
            if df['Flag'][i]>=df['Flag'][j] & df['Flag'][i]!=0:
                count+=1
                if count>obs_count and ((df['Alert Log'][i-1]!="Alert") and (df['Alert Log'][i-2]!="Alert")):
                    z+=1
                    add.append(df['Time stamp'][i])
                    df['Alert Log'].iloc[i]="Alert"
                    if z==1:
                        abc=1
                    break
                    count=6
            else:
                break
            j+=1


    add=list(set(add))
    len(add)

    df['color_marker']=np.where(df['Alert Log']=="Alert", 'red', '#00FE35')
    df['Threshold']=threshold

    df['alert text']=np.where(df['Alert Log']=="Alert","Alert","")
    
    return df

def generate_alert_report(df,variable,threshold,name_of_the_variable,case,obs_count):
    start=datetime.now()

    df=df.sort_values("Time stamp")
    df.reset_index(drop=True,inplace=True)
    df['Flag']=0
    if case=="greater":
        df.loc[df[variable]>threshold,'Flag']=1  
    else:
        df.loc[df[variable]<threshold,'Flag']=1  

    df['Alert Log']="No Alert"
    
    count=0
    add=[]
    z=0
    
    for i in range(obs_count,df['Flag'].shape[0]):
        count=0
        j=i-obs_count
        if df['Flag'][i]==1:
            while j<i:
                if (df['Flag'][j]==1):
                    count+=1
                    if count>obs_count-1 and ((df['Flag'][i-1]==1) and (df['Alert Log'][i-1]!="Alert"))                         and ((df['Alert Log'][i-2]!="Alert") and (df['Flag'][i-2]==1))                            and ((df['Alert Log'][i-3]!="Alert") and (df['Flag'][i-3]==1)):
                        z+=1
                        add.append(df['Time stamp'][i])
                        df['Alert Log'].iloc[i]="Alert"
                        if z==1:
                            abc=1
                    j+=1
                else:
                    break
        else:
            pass
            


    add=list(set(add))

    df['color_marker']='#00FE35'
    df.loc[df['Alert Log']=="Alert",'color_marker']="red"
    df['Threshold']=threshold

    df['alert text']=np.where(df['Alert Log']=="Alert","Alert","")
    
    return df

def generate_alert_report_energy(temp,variable,threshold,name_of_the_variable,case,obs_count):
    start=datetime.now()
    temp=temp.sort_values("Time stamp")
    temp.reset_index(drop=True,inplace=True)
    temp['Flag']=0
    if case=="greater":
        temp.loc[temp[variable]>temp['threshold'],'Flag']=1  
    else:
        temp.loc[temp[variable]<temp['threshold'],'Flag']=1  

    temp['Alert Log']="No Alert"
    
    count=0
    add=[]
    z=0
    
    for i in range(obs_count,temp['Flag'].shape[0]):
        count=0
        j=i-obs_count
        if temp['Flag'][i]==1:
            while j<i:
                if (temp['Flag'][j]==1):
                    count+=1
                    if count>obs_count-1 and ((temp['Flag'][i-1]==1) and (temp['Alert Log'][i-1]!="Alert")):#((temp['Alert Log'][i-1]!="Alert") and (temp['Alert Log'][i-2]!="Alert")):
                        z+=1
                        add.append(temp['Time stamp'][i])
                        temp['Alert Log'].iloc[i]="Alert"
                        if z==1:
                            abc=1
                    j+=1

                else:
                    break
        else:
            pass
            


    add=list(set(add))
    
    temp['color_marker']='#00FE35'
    temp.loc[temp['Alert Log']=="Alert",'color_marker']="red"
    temp['Threshold']=temp['threshold']

    temp['alert text']=np.where(temp['Alert Log']=="Alert","Alert","")
    alert_temp=temp.copy()
    return alert_temp

def get_threshold(date_range,col,trad_cat):
    std=df[(df['Time stamp']<date_range.replace(hour=0)) &
           (df['Time stamp']>date_range-timedelta(days=30)) &
           (df['weekday']==date_range.day_name()) & 
           (df['trading_cat']==trad_cat)][col].std()
    mean=df[(df['Time stamp']<date_range.replace(hour=0)) & 
            (df['Time stamp']>date_range-timedelta(days=30)) &
            (df['weekday']==date_range.day_name()) &
            (df['trading_cat']==trad_cat)][col].mean()
    threshold=mean+std*2
    return threshold


def deep_dive_graph(alert_no):
    
    dttime=alert_df['Time stamp'].iloc[alert_no]
    thrshld=alert_df['threshold'].iloc[alert_no]
    
    temp['Time stamp']=pd.to_datetime(temp['Time stamp'])

    plot=temp[(temp['Time stamp']>dttime-timedelta(days=1)) & (temp['Time stamp']<=dttime+timedelta(hours=1))]
    plot1=temp[(temp['Time stamp']>dttime-timedelta(days=7, hours=12)) & (temp['Time stamp']<dttime)]
    
    tab=flt_df[(flt_df['Time stamp']>=dttime-timedelta(days=7, hours=12)) & (flt_df['Time stamp']<=dttime) ]
    tab1=tab.groupby(['weekday','trading_cat']).aggregate({para:['mean','std','max','min']}).reset_index()
    
    cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cat_type = CategoricalDtype(categories=cats, ordered=True)
    tab1['weekday'] = tab1['weekday'].astype(cat_type)
    tab1.sort_values("weekday",inplace=True)
    tab1.reset_index(drop=True,inplace=True)
    
    return plot,plot1,tab1

def deep_dive(ans,alert_no):
    global alert_df
    if ans=="YES":
        alert_df=temp_[temp_['Alert Log']=="Alert"].iloc[:,:5].reset_index(drop=True).round(2)
        alert_df=alert_df[['Time stamp', 'weekday', 'trading_cat', 'threshold','Energy']]
        alert_df['Actual Vs Threshold(in %)']=round((alert_df['Energy']-alert_df['threshold'])/alert_df['threshold']*100,2)
        style = {'description_width': 'initial','handle_color': 'red'} 
        plot,plot1,tab1=deep_dive_graph(alert_no)
        return plot,plot1,tab1
    else:
        return 

def selection(col,start_date,end_date):
    
    start_date=datetime.combine(start_date, datetime.min.time())
    end_date=datetime.combine(end_date, datetime.min.time())
    
    global para
    global temp_
    global temp
    
    para=col
    final_energy_alert=pd.DataFrame()
    temp=flt_df[['Time stamp',col,'weekday','trading_cat']]
    temp['threshold']=temp.apply(lambda x: get_threshold(x['Time stamp'],para,x['trading_cat']),axis=1)
    temp.rename(columns={col:"Energy"},inplace=True)
    temp['variable']=col
    case='greater'
    variable="Energy"
    name_of_the_variable="Energy"
    temp=temp.sort_values("Time stamp",ascending=0)
    threshold="check"

    temp=temp[(temp['Time stamp']>=start_date) & (temp['Time stamp']<=end_date)]
    
    temp_=generate_alert_report_energy(temp,variable,threshold,name_of_the_variable,case,2)

    return temp_

def deep_dive_energy_analysis(col,start_date,end_date,ans,alert_no):
    global temp_
    temp_=selection(col,start_date,end_date)
    plot,plot1,tab1=deep_dive(ans,alert_no)
    return plot,plot1,tab1

def deep_dive_voltage_graph(alert_no):
    
    alert_df['Time stamp']=pd.to_datetime(alert_df['Time stamp'])
    dttime=alert_df['Time stamp'].iloc[alert_no]
    thrshld=alert_df['Threshold'].iloc[alert_no]
    
    temp_['Time stamp']=pd.to_datetime(temp_['Time stamp'])
    
    display(temp_)
    
    plot=temp_[(temp_['Time stamp']>dttime-timedelta(days=1)) & (temp_['Time stamp']<=dttime+timedelta(hours=1))]
    plot1=temp_[(temp_['Time stamp']>dttime-timedelta(days=7, hours=12)) & (temp_['Time stamp']<dttime)]
    
    tab=temp_[(temp_['Time stamp']>dttime-timedelta(days=7, hours=12)) & (temp_['Time stamp']<dttime) ]
    tab['weekday']=tab['Time stamp'].apply(lambda x: x.strftime("%A"))
    tab1=tab.groupby(['weekday']).aggregate({"Voltage %":['mean','std','max','min']}).reset_index()
    
    cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cat_type = CategoricalDtype(categories=cats, ordered=True)
    tab1['weekday'] = tab1['weekday'].astype(cat_type)
    tab1.sort_values("weekday",inplace=True)
    tab1.reset_index(drop=True,inplace=True)
    
    return plot,plot1,tab1

def deep_dive_voltage(ans,alert_no):
    global alert_df
    if ans=="YES":
        alert_df=temp_[temp_['Alert Log']=="Alert"].reset_index(drop=True).round(2)
        alert_df=alert_df[['Time stamp', 'Voltage', 'Mean_Voltage', 'Voltage %','Threshold']]
        alert_df['Actual Vs Threshold(in %)']=round((alert_df['Voltage %']-alert_df['Threshold'])/alert_df['Threshold']*100,2)
        plot,plot1,tab1=deep_dive_voltage_graph(alert_no)
        return plot,plot1,tab1
    else:
        return 

def selection_voltage(col,threshold,start_date,end_date):
    start_date=datetime.combine(start_date, datetime.min.time())
    end_date=datetime.combine(end_date, datetime.min.time())
    
    global para
    global temp_
    global temp_
    
    
    para=col
    final_voltage[col+" %"]=round(abs(final_voltage[col]-final_voltage['Mean_Voltage'])*100/final_voltage['Mean_Voltage'],2)
    variable=col+" %"
    Threshold=threshold
    name_of_the_variable="Voltage"
    
    case='greater'
    check=final_voltage[['Time stamp',col,"Mean_Voltage",variable]]
    check.rename(columns={col:"Voltage",variable:'Voltage %'},inplace=True)
    check['variable']=col
    check['Time stamp']=pd.to_datetime(check['Time stamp'])
    check1=check[(check['Time stamp']>=start_date) & (check['Time stamp']<=end_date)]
    temp_=generate_alert_report(check,"Voltage %",Threshold,name_of_the_variable,case,6)
    return temp_

def deep_dive_voltage_analysis(col,threshold,start_date,end_date,ans,alert_no):
    global temp_
    temp_=selection_voltage(col,threshold,start_date,end_date)
    plot,plot1,tab1=deep_dive_voltage(ans,alert_no)
    return plot,plot1,tab1

def deep_dive_current_graph(alert_no):
    alert_df['Time stamp']=pd.to_datetime(alert_df['Time stamp'])
    dttime=alert_df['Time stamp'].iloc[alert_no]
    thrshld=alert_df['Threshold'].iloc[alert_no]
    
    temp_['Time stamp']=pd.to_datetime(temp_['Time stamp'])
    
    plot=temp_[(temp_['Time stamp']>dttime-timedelta(days=1)) & (temp_['Time stamp']<=dttime+timedelta(hours=1))]
    plot1=temp_[(temp_['Time stamp']>dttime-timedelta(days=7, hours=12)) & (temp_['Time stamp']<dttime)]
    
    tab=temp_[(temp_['Time stamp']>dttime-timedelta(days=7, hours=12)) & (temp_['Time stamp']<dttime) ]
    tab['weekday']=tab['Time stamp'].apply(lambda x: x.strftime("%A"))
    tab1=tab.groupby('weekday').aggregate({"Current %":['mean','std','max','min']}).reset_index()
    
    cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cat_type = CategoricalDtype(categories=cats, ordered=True)
    tab1['weekday'] = tab1['weekday'].astype(cat_type)
    tab1.sort_values("weekday",inplace=True)
    tab1.reset_index(drop=True,inplace=True)
    
    return plot,plot1,tab1

def deep_dive_current(ans,alert_no):
    global alert_df
    if ans=="YES":
        alert_df=temp_[temp_['Alert Log']=="Alert"].reset_index(drop=True).round(2)
        alert_df=alert_df[['Time stamp', 'Current', 'mains_mean_Current', 'Current %','Threshold']]
        alert_df['Actual Vs Threshold(in %)']=round((alert_df['Current %']-alert_df['Threshold'])/alert_df['Threshold']*100,2)
        plot,plot1,tab1=deep_dive_current_graph(alert_no)
        return plot,plot1,tab1
    else:
        return 

def selection_current(col,threshold,start_date,end_date):
    start_date=datetime.combine(start_date, datetime.min.time())
    end_date=datetime.combine(end_date, datetime.min.time())
    global para
    global temp
    global temp_
    para=col
    final_current[col+" %"]=round(abs(final_current[col]-final_current['mains_mean_Current'])*100/final_current['mains_mean_Current'],2)
    variable=col+" %"
    threshold=threshold
    name_of_the_variable="Current"
    case='greater'
    check=final_current[['Time stamp',col,"mains_mean_Current",variable]]
    check.rename(columns={col:"Current",variable:'Current %'},inplace=True)
    check['variable']=col
    check['Time stamp']=pd.to_datetime(check['Time stamp'])
    check1=check[(check['Time stamp']>=start_date) & (check['Time stamp']<=end_date)]
    temp_=generate_alert_report(check,"Current %",threshold,name_of_the_variable,case,6)
    return temp_

def deep_dive_current_analysis(col,threshold,start_date,end_date,ans,alert_no):
    global temp_
    temp_=selection_current(col,threshold,start_date,end_date)
    plot,plot1,tab1=deep_dive_current(ans,alert_no)
    return plot,plot1,tab1

def deep_dive_power_factor_graph(alert_no):
    alert_df['Time stamp']=pd.to_datetime(alert_df['Time stamp'])
    dttime=alert_df['Time stamp'].iloc[alert_no]
    thrshld=alert_df['Threshold'].iloc[alert_no]
    
    temp_['Time stamp']=pd.to_datetime(temp_['Time stamp'])
    
    plot=temp_[(temp_['Time stamp']>dttime-timedelta(days=1)) & (temp_['Time stamp']<=dttime+timedelta(hours=1))]
    plot1=temp_[(temp_['Time stamp']>dttime-timedelta(days=7, hours=12)) & (temp_['Time stamp']<dttime)]
    
    tab=temp_[(temp_['Time stamp']>dttime-timedelta(days=7, hours=12)) & (temp_['Time stamp']<dttime) ]
    tab['weekday']=tab['Time stamp'].apply(lambda x: x.strftime("%A"))
    tab1=tab.groupby('weekday').aggregate({"PF":['mean','std','max','min']}).reset_index()
    
    cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cat_type = CategoricalDtype(categories=cats, ordered=True)
    tab1['weekday'] = tab1['weekday'].astype(cat_type)
    tab1.sort_values("weekday",inplace=True)
    tab1.reset_index(drop=True,inplace=True)
    
    return plot,plot1,tab1

def deep_dive_power_factor(ans,alert_no):
    global alert_df
    if ans=="YES":
        alert_df=temp_[temp_['Alert Log']=="Alert"].reset_index(drop=True).round(2)
        alert_df=alert_df[['Time stamp', 'PF','Threshold']]
        alert_df['Actual Vs Threshold(in %)']=round((alert_df['PF']-alert_df['Threshold'])/alert_df['Threshold']*100,2)
        style = {'description_width': 'initial','handle_color': 'red'} 
        plot,plot1,tab1=deep_dive_power_factor_graph(alert_no)
        return plot,plot1,tab1
    else:
        return 

def deep_dive_pf_analysis(col,threshold,start_date,end_date,ans,alert_no):
    global temp_
    temp_=selection_power_factor(col,threshold,start_date,end_date)
    plot,plot1,tab1=deep_dive_power_factor(ans,alert_no)
    return plot,plot1,tab1

def selection_power_factor(col,threshold,start_date,end_date):
    start_date=datetime.combine(start_date, datetime.min.time())
    end_date=datetime.combine(end_date, datetime.min.time())
    global para
    global temp
    global temp_
    para=col
    variable="PF"
    threshold=threshold
    name_of_the_variable="Power Factor"
    case='lesser'
    check=final_pf[['Time stamp',col]]
    check.rename(columns={col:"PF"},inplace=True)
    check['variable']=col
    check['Time stamp']=pd.to_datetime(check['Time stamp'])
#     check['Time stamp']=check['Time stamp'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M'))
    check1=check[(check['Time stamp']>=start_date) & (check['Time stamp']<=end_date)]
    temp_=generate_alert_report(check,variable,threshold,name_of_the_variable,case,6)
    return temp_


def main(alert_analyse,phase,start_date,end_date,threshold,site_name):
    variable=get_variable(alert_analyse)
    unit=get_unit(variable)
    phase=phase+" ( "+unit+" )"
    
    read_data(alert_analyse,site_name,start_date,end_date)
    
    totalData = {}
    if alert_analyse=="Voltage Imbalance":
        temp_=selection_voltage(phase,threshold,start_date,end_date)
        display(temp_.head())
        graph1_table1=temp_[['Time stamp','Voltage']]
        graph1_table2=temp_[['Time stamp','Threshold']]
        graph1_table3=temp_[['Time stamp','Alert Log']]
        graph1_table4=temp_[['Time stamp','Voltage %']]
     
        alert_table=temp_[temp_['Alert Log']=="Alert"][['Time stamp','Voltage %','Threshold']]
        alert_table['Actual Vs Threshold(in %)']=round((alert_table['Voltage %']/alert_table['Threshold']-1)*100,2)

        totalData["graph1_table1"] = graph1_table1
        totalData["graph1_table2"] = graph1_table2
        totalData["graph1_table3"] = graph1_table3
        totalData["alert_table"] = alert_table

        return totalData

    elif alert_analyse=="Load Imbalance":
        temp_=selection_current(phase,threshold,start_date,end_date)
        graph1_table1=temp_[['Time stamp','Current']]
        graph1_table2=temp_[['Time stamp','Threshold']]
        graph1_table3=temp_[['Time stamp','Alert Log']]
        alert_table=temp_[temp_['Alert Log']=="Alert"][['Time stamp','Current %','Threshold']]
        alert_table['Actual Vs Threshold(in %)']=round((alert_table['Current %']/alert_table['Threshold']-1)*100,2)

        totalData["graph1_table1"] = graph1_table1
        totalData["graph1_table2"] = graph1_table2
        totalData["graph1_table3"] = graph1_table3
        totalData["alert_table"] = alert_table

        return totalData

    elif alert_analyse=="Low Power Factor":
        temp_=selection_power_factor(phase,threshold,start_date,end_date)

        graph1_table1=temp_[['Time stamp','PF']]
        graph1_table2=temp_[['Time stamp','Threshold']]
        graph1_table3=temp_[['Time stamp','Alert Log']]
        alert_table=temp_[temp_['Alert Log']=="Alert"][['Time stamp','PF','Threshold']]
        alert_table['Actual Vs Threshold(in %)']=round((alert_table['PF']/alert_table['Threshold']-1)*100,2)

        totalData["graph1_table1"] = graph1_table1
        totalData["graph1_table2"] = graph1_table2
        totalData["graph1_table3"] = graph1_table3
        totalData["alert_table"] = alert_table

        return totalData

    elif alert_analyse=="Abnormal Change in Energy Consumption":

        temp_=selection(phase,start_date,end_date)
        graph1_table1=temp_[['Time stamp','Energy']]
        graph1_table2=temp_[['Time stamp','threshold']]
        graph1_table3=temp_[['Time stamp','Alert Log']]
        alert_table=temp_[temp_['Alert Log']=="Alert"][['Time stamp','Energy','weekday','trading_cat','threshold']]
        alert_table['Actual Vs Threshold(in %)']=round((alert_table['Energy']/alert_table['threshold']-1)*100,2)
        
        totalData["graph1_table1"] = graph1_table1
        totalData["graph1_table2"] = graph1_table2
        totalData["graph1_table3"] = graph1_table3
        totalData["alert_table"] = alert_table

        return totalData

    else:
        pass
    return

def main_deep_dive(alert_analyse,phase,site_name,start_date,end_date,alert_no,threshold):
    
    variable=get_variable(alert_analyse)
    unit=get_unit(variable)
    phase=phase+" ( "+unit+" )"
    
    read_data(alert_analyse,site_name,start_date,end_date)
    
    totalData={}
    
    ans="YES"
    
    if ans=="NO":
        return 
    else:
        if alert_analyse=="Voltage Imbalance":

            plot,plot1,tab1=deep_dive_voltage_analysis(phase,threshold,start_date,end_date,ans,alert_no)

            graph2_table1=plot[['Time stamp','Voltage']]
            graph2_table2=plot[['Time stamp','Threshold']]
            graph2_table3=plot[['Time stamp','Voltage %']]
            
            plot1_transformed=np.histogram(plot['Voltage %'].values)
            y=plot1_transformed[0]
            X=plot1_transformed[1]
            
            plot1_transformed1=pd.DataFrame(y,columns=['Voltage Imbalance'])

            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))

            plot1_transformed1['X']=X_
            plot1_transformed1=plot1_transformed1.set_index("X")

            graph3_table1=plot1[['Time stamp','Voltage']]
            graph3_table2=plot1[['Time stamp','Threshold']]
            graph3_table3=plot[['Time stamp','Voltage %']]
            
            plot3_transformed=np.histogram(plot1['Voltage %'].values)
            y=plot3_transformed[0]
            X=plot3_transformed[1]
            
            plot3_transformed1=pd.DataFrame(y,columns=['Voltage Imbalance'])
            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))
            plot3_transformed1['X']=X_
            plot3_transformed1=plot3_transformed1.set_index("X")
            table1=tab1.copy()

            totalData["graph2_table1"]=graph2_table1
            totalData["graph2_table2"]=graph2_table2
            totalData["graph2_table3"]=graph2_table3
            totalData["graph3_table1"]=graph3_table1
            totalData["graph3_table2"]=graph3_table2
            totalData["graph3_table3"]=graph3_table3
            totalData["histogram_1"]=plot1_transformed1
            totalData["histogram_2"]=plot3_transformed1
            totalData["Mix_Max_Table"]=table1

            return totalData
        elif alert_analyse=="Load Imbalance":
            
            plot,plot1,tab1=deep_dive_current_analysis(phase,threshold,start_date,end_date,ans,alert_no)

            graph2_table1=plot[['Time stamp','Current']]
            graph2_table2=plot[['Time stamp','Threshold']]
            graph2_table3=plot[['Time stamp','Current %']]
            
            plot1_transformed=np.histogram(plot['Current %'].values)
            y=plot1_transformed[0]
            X=plot1_transformed[1]
            
            plot1_transformed1=pd.DataFrame(y,columns=['Load Imbalance'])

            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))

            plot1_transformed1['X']=X_
            plot1_transformed1=plot1_transformed1.set_index("X")            

            graph3_table1=plot1[['Time stamp','Current']]
            graph3_table2=plot1[['Time stamp','Threshold']]
            graph3_table3=plot[['Time stamp','Current %']]
            
            plot3_transformed=np.histogram(plot1['Current %'].values)
            y=plot3_transformed[0]
            X=plot3_transformed[1]
            
            plot3_transformed1=pd.DataFrame(y,columns=['Load Imbalance'])
            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))
            plot3_transformed1['X']=X_
            plot3_transformed1=plot3_transformed1.set_index("X")
            
            table1=tab1.copy()

            totalData["graph2_table1"]=graph2_table1
            totalData["graph2_table2"]=graph2_table2
            totalData["graph2_table3"]=graph2_table3
            totalData["graph3_table1"]=graph3_table1
            totalData["graph3_table2"]=graph3_table2
            totalData["graph3_table3"]=graph3_table3
            totalData["histogram_1"]=plot1_transformed1
            totalData["histogram_2"]=plot3_transformed1
            totalData["Mix_Max_Table"]=table1

            return totalData

        elif alert_analyse=="Low Power Factor":

            plot,plot1,tab1=deep_dive_pf_analysis(phase,threshold,start_date,end_date,ans,alert_no)

            graph2_table1=plot[['Time stamp','PF']]
            graph2_table2=plot[['Time stamp','Threshold']]
            
            plot1_transformed=np.histogram(plot['PF'].values)
            y=plot1_transformed[0]
            X=plot1_transformed[1]
            
            plot1_transformed1=pd.DataFrame(y,columns=['y'])
            #display(plot1_transformed1)

            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))
    
            plot1_transformed1['X']=X_
            plot1_transformed1=plot1_transformed1.set_index("X")

            graph3_table1=plot1[['Time stamp','PF']]
            graph3_table2=plot1[['Time stamp','Threshold']]
            
            plot3_transformed=np.histogram(plot1['PF'].values)
            y=plot3_transformed[0]
            X=plot3_transformed[1]
            
            plot3_transformed1=pd.DataFrame(y,columns=['y'])
            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))
            plot3_transformed1['X']=X_
            plot3_transformed1=plot3_transformed1.set_index("X")

            table1=tab1.copy()

            totalData["graph2_table1"]=graph2_table1
            totalData["graph2_table2"]=graph2_table2
            totalData["graph3_table1"]=graph3_table1
            totalData["graph3_table2"]=graph3_table2
            totalData["histogram_1"]=plot1_transformed1
            totalData["histogram_2"]=plot3_transformed1
            totalData["Mix_Max_Table"]=table1
            return totalData
        elif alert_analyse=="Abnormal Change in Energy Consumption":

            plot,plot1,tab1=deep_dive_energy_analysis(phase,start_date,end_date,ans,alert_no)

            graph2_table1=plot[['Time stamp','Energy']]
            graph2_table2=plot[['Time stamp','threshold']]
            
            plot1_transformed=np.histogram(plot['Energy'].values)
            y=plot1_transformed[0]
            X=plot1_transformed[1]
            
            plot1_transformed1=pd.DataFrame(y,columns=['Abnormal Change in Energy Consumption'])
            #display(plot1_transformed1)

            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))

            plot1_transformed1['X']=X_
            plot1_transformed1=plot1_transformed1.set_index("X")

            graph3_table1=plot1[['Time stamp','Energy']]
            graph3_table2=plot1[['Time stamp','threshold']]
            
            plot3_transformed=np.histogram(plot1['Energy'].values)
            y=plot3_transformed[0]
            X=plot3_transformed[1]
            
            plot3_transformed1=pd.DataFrame(y,columns=['Abnormal Change in Energy Consumption'])
            X_=[]
            for i in range(0,len(X)-1):
                X_.append(str(round(X[i],2))+"-"+str(round(X[i+1],2)))
            plot3_transformed1['X']=X_
            plot3_transformed1=plot3_transformed1.set_index("X")

            table1=tab1.copy()

            totalData["graph2_table1"]=graph2_table1
            totalData["graph2_table2"]=graph2_table2
            totalData["graph3_table1"]=graph3_table1
            totalData["graph3_table2"]=graph3_table2
            totalData["histogram_1"]=plot1_transformed1
            totalData["histogram_2"]=plot3_transformed1
            totalData["Mix_Max_Table"]=table1

            return totalData

        else:
            pass
        return

def main_table(phase,start_date,end_date,site_name):
    phase_=phase
    totalData = {}
    final_table=pd.DataFrame()
    for alert_analyse in ["Voltage Imbalance","Load Imbalance","Low Power Factor"]:#,"Abnormal Change in Energy Consumption"]:
        read_data(alert_analyse,site_name,start_date,end_date)
        variable=get_variable(alert_analyse)
        unit=get_unit(variable)
        phase=phase_+" ( "+unit+" )"
        print(phase)
        if alert_analyse=="Voltage Imbalance":
            temp_=selection_voltage(phase,2,start_date,end_date)
            tempp=pd.DataFrame([alert_analyse],columns=['Alert Type'])
            tempp['Count']=temp_[temp_['Alert Log']=="Alert"].shape[0]
            final_table=pd.concat([final_table,tempp],axis=0)
        elif alert_analyse=="Load Imbalance":
            temp_=selection_current(phase,15,start_date,end_date)
            tempp=pd.DataFrame([alert_analyse],columns=['Alert Type'])
            tempp['Count']=temp_[temp_['Alert Log']=="Alert"].shape[0]
            final_table=pd.concat([final_table,tempp],axis=0)
        elif alert_analyse=="Low Power Factor":
            temp_=selection_power_factor(phase,0.95,start_date,end_date)
            tempp=pd.DataFrame([alert_analyse],columns=['Alert Type'])
            tempp['Count']=temp_[temp_['Alert Log']=="Alert"].shape[0]
            final_table=pd.concat([final_table,tempp],axis=0)
        elif alert_analyse=="Abnormal Change in Energy Consumption":
            temp_=selection(phase,start_date,end_date)
            tempp=pd.DataFrame([alert_analyse],columns=['Alert Type'])
            tempp['Count']=temp_[temp_['Alert Log']=="Alert"].shape[0]
            final_table=pd.concat([final_table,tempp],axis=0)
        else:
            pass

    return final_table

def get_summary_table(site_name):
    meter_lists=get_meter_names(site_name)
    

    now=datetime.now()
 
    if now.month==1:
        start_date=now.replace(month=now.month-1,year=now.year-1,day=1,hour = 0, minute = 0, second = 0, microsecond = 0)
        end_date=now.replace(month=now.month-1,year=now.year-1,day=31, hour = 0, minute = 0, second = 0, microsecond = 0)
    else:
        start_date=now.replace(month=now.month-1,day=1, hour = 0, minute = 0, second = 0, microsecond = 0)
        end_date=now.replace(month=now.month-1,day=calendar.monthrange(2021, now.month-1)[1], hour = 0, minute = 0, second = 0, microsecond = 0)

    final_data=pd.DataFrame()
    for phase in meter_lists[:1]:
        temp_data=main_table(phase,start_date,end_date,site_name)
        temp_data['Phase']=phase
        final_data=pd.concat([final_data,temp_data],axis=0)

    pivot_table=pd.pivot_table(final_data,index='Alert Type',columns='Phase',values='Phase',aggfunc='sum')

    return pivot_table


def get_variable(alert_analyse):
    if alert_analyse=="Voltage Imbalance":
        variable ="voltage"
    elif alert_analyse=="Load Imbalance":
        variable="power"
    elif alert_analyse=="Low Power Factor":
        variable="power_factor"
    elif alert_analyse=="Abnormal Change in Energy Consumption":
        variable="energy"
    else:
        pass
    return variable

def get_unit(variable):
    if variable =="energy":
        unit='kWh'
    elif variable == "voltage":
        unit="V"
    elif variable =="power":
        unit="kW"
    elif variable =="power_factor":
        unit=""
    return unit

def get_final_columns(data,unit):
    final_columns=[]
    for col in data.columns:
        if (col.find("_R")!=-1) :
            final_columns.append(col.replace("_R"," L1 ( "+unit+" )"))
        elif (col.find("_S")!=-1) :
            final_columns.append(col.replace("_S"," L2 ( "+unit+" )"))
        elif (col.find("_T")!=-1) :
            final_columns.append(col.replace("_T"," L3 ( "+unit+" )"))
        else:
            final_columns.append(col.replace("_"," ( "+unit+" )"))
    return final_columns

def get_transformed_data(alert_analyse,site_name,start_date,end_date):
    
    variable=get_variable(alert_analyse)
    
    unit=get_unit(variable)
    
    static_url='https://api.oak-insights.com/consumption/five?site_id='
    url=static_url+site_name+"&start="+start_date+"&end="+end_date

    r = requests.get(url)
    files = r.json()

    df_mysql1=pd.DataFrame(files['data'])

    df_mysql1[variable]=df_mysql1[variable].astype(float)
    df_mysql1['Meter_Name']=df_mysql1['name']+"_"
    
    mains_df=pd.pivot_table(df_mysql1,index='measurement_time',columns='Meter_Name',values=variable) ## transforming data
    
    final_columns=get_final_columns(mains_df,unit) 
    mains_df.columns=final_columns 
    
    static_url='https://api.oak-insights.com/phase/five?site_id='
    url=static_url+site_name+"&start="+start_date+"&end="+end_date
    r = requests.get(url)
    files = r.json()
    df_mysql1=pd.DataFrame(files['data'])
    df_mysql1[variable]=df_mysql1[variable].astype(float)
    df_mysql1['Meter_Name']=df_mysql1['name']+"_"+df_mysql1['phase']

    mains_phase_df=pd.pivot_table(df_mysql1,index='measurement_time',columns='Meter_Name',values=variable)
    final_columns=get_final_columns(mains_phase_df,unit) 
    mains_phase_df.columns=final_columns ## change the column name as per csv
    
    mains_df=mains_df.reset_index()
    mains_phase_df=mains_phase_df.reset_index()
    combined_df=mains_df.merge(mains_phase_df,on='measurement_time',how='left')
    combined_df=combined_df.set_index('measurement_time')
    
    final_columns=get_final_columns(combined_df,unit) 
    combined_df.columns=final_columns

    return combined_df

def get_opr_hours(site_name):
    host='oak-api.ceedji5fvimj.eu-west-2.rds.amazonaws.com'
    port=3306
    username='oak-api-micro'
    password='ThOak@Ap!M!cr012'
    database='customer'

    mysql_cn= MySQLdb.connect(host=host, 
                    port=port,user=username, passwd=password, 
                    db=database)

    opr_hours_sql = 'select * from customer.operating_hours where site_id = "{}";'.format(site_name)
    opr_hours = pd.read_sql(opr_hours_sql, con=mysql_cn)
    opr_hours=opr_hours.dropna(subset=['start'])
    
    opr_hours['start'] = pd.DataFrame(opr_hours['start'].apply(lambda x: str(x)[-8:-3]))
    opr_hours['start']=opr_hours['start'].apply(lambda x: datetime.strptime(x,"%H:%M"))
    opr_hours['end'] = pd.DataFrame(opr_hours['end'].apply(lambda x: str(x)[-8:-3]))
    opr_hours['end']=opr_hours['end'].apply(lambda x: datetime.strptime(x,"%H:%M"))

    opr_hours['end']=opr_hours['end'].apply(lambda x: x.replace(minute=59) if x.minute==0 else x)

#     site_opr_hour=opr_hours[opr_hours['site_id']==site_name]
    site_opr_hour=opr_hours
    
    def split_hours(x,y):
        if x<y:
            return x,y
        else:
            return [(x,23),(0,y)]

    def get_hours(x):
        start=x['start'].hour
        end=x['end'].hour
        if start>end:
            splitted_hour=split_hours(start,end)
            return_list=[]
            for each in splitted_hour:
                start=each[0]
                end=each[1]
                i=start
                while i<end+1:
                    if i==24:
                        return_list.append(0)
                    else:
                        return_list.append(i)
                    i+=1
            return return_list
        else:
            if end==0:
                end=24
            i=start
            return_list=[]
            while i<end+1:
                if i==24:
                    return_list.append(0)
                else:
                    return_list.append(i)
                i+=1
            return return_list
    site_opr_hour['hour']=site_opr_hour.apply(lambda x: get_hours(x) , axis=1)
    site_opr_hour['type']=site_opr_hour['type'].apply(lambda x: "Prep" if x=="Preparatory" else x) 
    site_opr_hour['type']=site_opr_hour['type'].apply(lambda x: "Non Operating" if pd.isnull(x) else x)
    site_opr_hour['type']=site_opr_hour['type'].apply(lambda x: "Non Operating" if x == 'Closed' else x)
    site_opr_hour=site_opr_hour.explode('hour')
    site_opr_hour.rename(columns={'day':'weekday'},inplace=True)
    
    return site_opr_hour


def read_data(alert_analyse,site_name,start_date,end_date):
    
    global final_voltage
    global final_pf
    global final_current
    global flt_df
    
    if alert_analyse=="Voltage Imbalance":
        
        start_date=start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date=end_date.strftime("%Y-%m-%d %H:%M:%S")
        data_df=get_transformed_data(alert_analyse,site_name,start_date,end_date)
        data_df=data_df.reset_index().rename(columns={'measurement_time':'Time stamp'})
        data_df=data_df.fillna(0)
        
        global final_voltage
        
        voltage_file=data_df.copy()
        only_col=['Time stamp']
        for each in voltage_file.columns:
            if each.find("Main 1")!=-1:
                only_col.append(each)
        final_voltage=voltage_file[only_col]
        final_voltage.drop_duplicates(inplace=True)
        final_voltage.reset_index(drop=True,inplace=True)
        
        final_voltage.sort_values("Time stamp",inplace=True)
        mains_voltage=final_voltage.columns[2:].tolist()
        final_voltage['Mean_Voltage']=final_voltage[mains_voltage].mean(axis=1)
        
    if alert_analyse=="Load Imbalance":
        start_date=start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date=end_date.strftime("%Y-%m-%d %H:%M:%S")
        data_df=get_transformed_data(alert_analyse,site_name,start_date,end_date)
        data_df=data_df.reset_index().rename(columns={'measurement_time':'Time stamp'})
        data_df=data_df.fillna(0)

        global final_current
        
        current_file=data_df.copy()
        only_col=['Time stamp']
        for each in current_file.columns:
            if each.find("Main 1")!=-1:
                only_col.append(each)
        final_current=current_file[only_col]

        final_current.drop_duplicates(inplace=True)
        final_current.reset_index(drop=True,inplace=True)
        final_current.sort_values("Time stamp",inplace=True)
        mains_current=final_current.columns[2:]
        final_current['mains_mean_Current']=final_current[mains_current].mean(axis=1)
        
    if alert_analyse=="Low Power Factor":
        start_date=start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date=end_date.strftime("%Y-%m-%d %H:%M:%S")
        data_df=get_transformed_data(alert_analyse,site_name,start_date,end_date)
        data_df=data_df.reset_index().rename(columns={'measurement_time':'Time stamp'})
        data_df=data_df.fillna(0)
        global final_pf
        final_pf=data_df
        final_pf.drop_duplicates(inplace=True)
        final_pf.reset_index(drop=True,inplace=True)
        final_pf.sort_values("Time stamp",inplace=True)

    if alert_analyse=="Abnormal Change in Energy Consumption":
        global energy
        start_date=start_date-timedelta(days=30)
        start_date=start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date=end_date.strftime("%Y-%m-%d %H:%M:%S")
        data_df=get_transformed_data(alert_analyse,site_name,start_date,end_date)
        data_df=data_df.reset_index().rename(columns={'measurement_time':'Time stamp'})
        energy=data_df.copy()
        energy.drop_duplicates(inplace=True)
        energy.reset_index(drop=True,inplace=True)
        energy.sort_values("Time stamp",inplace=True)
        energy=energy.fillna(0)
        global df
        df=energy.copy()
        from datetime import datetime
        
        df['Time stamp']=df['Time stamp'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
        df = df.sort_values('Time stamp')
        df['hour']=df['Time stamp'].dt.hour
        df['weekday'] = df['Time stamp'].dt.day_name()
        
        site_opr_hour=get_opr_hours(site_name)
        df=df.merge(site_opr_hour[['weekday','hour','type']],on=['weekday','hour'],how='left')
        df.rename(columns={'type':'trading_cat'},inplace=True)
        
        flt_df=df[df['Time stamp']>start_date]
        
    return

def get_meter_names(site_name):
    start_date=datetime.now()-timedelta(hours=280)
    start_date=start_date.replace(minute=0,second=0,microsecond=0)
    end_date=datetime.now()-timedelta(hours=240,minutes=10)
    end_date=end_date.replace(minute=0,second=0,microsecond=0)
    data=get_data_for_meter_list(site_name,start_date,end_date)
    return data

def change_phase_name(col):
    if (col.find("_R")!=-1) :
        return(col.replace("_R"," L1"))
    elif (col.find("_S")!=-1) :
        return(col.replace("_S"," L2"))
    elif (col.find("_T")!=-1) :
        return(col.replace("_T"," L3"))
    else:
        return(final_columns.append(col))

def get_data_for_meter_list(site_name,start_date,end_date):
    
    start_date=start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_date=end_date.strftime("%Y-%m-%d %H:%M:%S")
    
    static_url='https://api.oak-insights.com/consumption/five?site_id='
    url=static_url+site_name+"&start="+start_date+"&end="+end_date
    r = requests.get(url)
    files = r.json()#!/usr/bin/env python

    df_mysql1=pd.DataFrame(files['data'])
    df_mysql1['Meter_Name']=df_mysql1['name']
    
    static_url='https://api.oak-insights.com/phase/five?site_id='
    url=static_url+site_name+"&start="+start_date+"&end="+end_date
    r = requests.get(url)
    files = r.json()
    df_mysql2=pd.DataFrame(files['data'])
    df_mysql2['Meter_Name']=df_mysql2['name']+"_"+df_mysql2['phase']
    df_mysql2['Meter_Name']=df_mysql2['Meter_Name'].apply(lambda x: change_phase_name(x))
    
    final_df=pd.concat([df_mysql1,df_mysql2],axis=0)
    phase_name_list=final_df['Meter_Name'].unique().tolist()

    return phase_name_list