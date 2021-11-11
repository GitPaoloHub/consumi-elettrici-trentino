import pandas as pd
import numpy as np
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot  as plt

weather = pd.read_pickle("../data/processed/WEATHER.pkl")
precip = pd.read_pickle("../data/processed/PRECIP.pkl")
grid = pd.read_pickle("../data/processed/GRID.pkl")
consumi = pd.read_pickle("../data/processed/CONSUMI.pkl")
appa = pd.read_pickle("../data/processed/APPA.pkl")

precip=precip.astype({'cellId': int})

def consumi_giornalieri(cons,cons_tot):
    consumi_hour=cons.groupby(['hour','category']).sum().drop(columns=['utenze','cellId'])
    consumi_hour=consumi_hour.reset_index(level=[1])
    with plt.style.context('seaborn'):
        for cat in ['f','p','c','i']:
            df=consumi_hour[consumi_hour['category']==cat]
            plt.plot(df.index, df['consumi']/cons_tot['consumi'][cat])
        plt.legend(['f','p','c','i'])
        plt.xticks([1,4,7,10,13,16,19,22],['1:00','4:00','7:00','10:00','13:00','16:00','19:00','22:00'])
        plt.title('Consumi giornalieri')
    plt.show()
    
 
def consumi_settimanali(cons,cons_tot):
    consumi_week=cons.groupby(['week','category']).sum().drop(columns=['utenze','cellId'])
    consumi_week=consumi_week.reset_index(level=[1])
    with plt.style.context('seaborn'):
        for cat in ['f','p','c','i']:
            df=consumi_week[consumi_week['category']==cat]
            df=df.reindex(['mon','tue','wed','thu','fri','sat','sun'])
            plt.plot(df.index, df['consumi']/cons_tot['consumi'][cat])
        plt.legend(['f','p','c','i'])
        plt.title('Consumi settimanali')
    plt.show()
    
def consumi_bimestrali(cons,cons_tot):   
    consumi_day=cons.groupby(['mounth','day','category']).sum().drop(columns=['utenze','cellId'])
    consumi_day=consumi_day.reset_index(level=[2])
    with plt.style.context('seaborn'):
        for cat in ['f','p','c','i']:
            df=consumi_day[consumi_day['category']==cat]
            data=[]
            for day in df.index:
                data.append(day[1]+'-'+day[0])
            plt.plot(data,df['consumi']/cons_tot['consumi'][cat])
        plt.legend(['f','p','c','i']) 
        plt.xticks([0,7,14,21,28,35,42,49,56])
        plt.title('Consumi bimestrali')
    plt.show()
    
    
def consumi_temp(category):
    pw=consumi.merge(grid.loc[:,['cellId','station','category']], how='left', on='cellId')
    pw=pw.astype({'hour': int})
    pw=pw.groupby(['station','mounth','day','hour','category']).sum()
    pw=pw.reset_index(level=[0,1,2,3,4])
    pw=pw.merge(weather, how='left', on=['station','mounth','day','hour'])
    pw=pw.drop(columns=['geometry','year','minTemperature','maxTemperature','mounth','day','hour','utenze','cellId','station','precip'])
    pw['temper']=round(pw['temper'])
    
    if category=='tot':
        countw=pw.groupby(['temper']).count()
        totw=pw.groupby(['temper']).sum()        
    else:
        countw=pw[pw['category']==category].groupby(['temper']).count()
        totw=pw[pw['category']==category].groupby(['temper']).sum()
    totw['consumi']=totw['consumi']/countw['consumi']
    totw['count']=countw['consumi']
    totw=totw.reset_index(level=[0])
    
    with plt.style.context('seaborn'):
        sns.barplot(x='temper',y='consumi' ,data=totw,palette="icefire")
        #sns.lineplot(x='temper',y='count',data=tot)
        #plt.xticks([0,3,6,9,12,15,18,21,24,27,30,33],[-15,-12,-9,-6,-3,0,3,6,9,12,15,18])
        plt.xticks(rotation='vertical')
    plt.show()
  
def dataframe_weather():
    #dataframe che contiene informazioni sulle precipitazioni/temperature per ogini cella
    #per aggiungere la temperatura
    pt=consumi.merge(grid.loc[:,['cellId','station']], how='left', on='cellId')
    pt.drop(columns=['year','consumi','utenze','week','hour'],inplace=True)
    pt2=weather.groupby(['mounth','day','station']).mean()
    pt2=pt2.reset_index(level=[0,1,2]).drop(columns=['maxTemperature','minTemperature','precip','hour'])
    pt=pt.merge(pt2, how='left', on=['station','day','mounth'])
    
    # precip registra le precipitazioni anche su celle che non hanno consumi, fondendola con il DF dei consumi ci assicuriamo 
    # di ignorare tali celle
    pp=consumi.groupby(['cellId', 'mounth','day']).sum()
    pp=pp.reset_index(level=[0,1,2])
    pp=pp.merge(precip, how='left', on=['cellId','mounth','day'])
    pp=pp.merge(pt, how='left', on=['cellId','mounth','day'])
    pp=pp.merge(grid.loc[:,['cellId','category']], how='left', on=['cellId'])
    pp.drop(columns=['utenze','year','mounth','day'],inplace=True)
    #pp.fillna(0, inplace=True)
    pp['precip']=pp['precip']//10
    return pp
    
def consumi_precip(category):
    pp=dataframe_weather()
    # raggruppo per contare e poi per sommare i consumi
    if category=='tot':
        tempp=pp.groupby(['precip']).mean()
        countp=pp.groupby(['precip']).count()
        totp=pp.groupby(['precip']).sum()
    else:
        tempp=pp[pp['category']==category].groupby(['precip']).mean()
        countp=pp[pp['category']==category].groupby(['precip']).count()
        totp=pp[pp['category']==category].groupby(['precip']).sum()
    totp['consumi']=totp['consumi']/countp['consumi']
    totp['count']=countp['consumi']
    totp['temp']=tempp['temper']
    totp=totp.reset_index(level=[0])
    
    
    with plt.style.context('seaborn'):
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        sns.barplot(x='precip',y='consumi' ,data=totp,palette="Blues_d", ax=ax1)
        sns.scatterplot(x='precip',y='temp',data=totp, ax=ax2)
        #plt.xticks([0,3,6,9,12,15,18,21,24,27,30,33],[-15,-12,-9,-6,-3,0,3,6,9,12,15,18])
        plt.xticks([])
    plt.show()
    

def top_correlation(corr_matrix,N):
    coeff=[]
    row=[]
    column=[]
    for i in range(14):
        for j in range(5):
            if i>j:
                coeff.append(abs(corr_matrix).iloc[i, j])
                row.append(i)
                column.append(j)
                
    df=pd.DataFrame({'row':row,'column':column,'coeff':coeff})
    df.sort_values(by=['coeff'], ascending = [0], inplace = True,ignore_index=True)
    for i in range(N):
        print(corr_matrix.columns[df['column'][i]],':',corr_matrix.index[df['row'][i]], '\t=',corr_matrix.iloc[df['row'][i], df['column'][i]])
               