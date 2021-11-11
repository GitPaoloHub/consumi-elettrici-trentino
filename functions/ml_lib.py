import pandas as pd
import numpy as np
import geopandas as gpd


weather = pd.read_pickle("../data/processed/WEATHER.pkl")
grid = pd.read_pickle("../data/processed/GRID.pkl")
consumi = pd.read_pickle("../data/processed/CONSUMI.pkl")


def add_orario(df_in):
    df_out=df_in.astype({"hour": int})
    conditions = [
        (df_out['hour']>=8) & (df_out['hour']<19),
        (df_out['hour']>=19) & (df_out['hour']<=23),
        (df_out['hour']>=0) & (df_out['hour']<8)    
        ]
    values = ['giorno','sera','notte']
    df_out['orario'] = np.select(conditions, values)
    return df_out


def df_regressione():
    consumi_tot = add_orario(consumi)
    consumi_cella = consumi_tot[consumi_tot['cellId']==2737]  # ho scelto una cella di Rovereto (ha la stazione meteo T0147)
    consumi_tot = consumi_tot.groupby(['mounth','day','week','orario']).sum()
    consumi_tot.reset_index(level=[0,1,2,3],inplace=True)
    consumi_cella = consumi_cella.groupby(['mounth','day','week','orario']).sum()
    consumi_cella.reset_index(level=[0,1,2,3],inplace=True)
    consumi_tot.drop(columns=['day','cellId','hour','utenze','mounth'], inplace=True)
    consumi_cella.drop(columns=['day','cellId','hour','utenze','mounth'], inplace=True)
    
    # parte delle temperature
    
    weather_tot = add_orario(weather)
    weather_cella = weather_tot[weather_tot['station']=='T0147']
    weather_tot = weather_tot.groupby(['mounth','day','orario']).mean()
    weather_tot.reset_index(level=[0,1,2],inplace=True)
    weather_cella = weather_cella.groupby(['mounth','day','orario']).mean()
    weather_cella.reset_index(level=[0,1,2],inplace=True)
    weather_tot.drop(columns=['minTemperature','maxTemperature','precip','hour','orario','mounth'], inplace=True)
    weather_cella.drop(columns=['minTemperature','maxTemperature','precip','hour','orario','mounth'], inplace=True)
    
    #accollo la colonna delle temperature alle matrici dei consumi
    consumi_tot['temp'] = weather_tot['temper']
    consumi_cella['temp'] = weather_cella['temper']
    return consumi_tot,consumi_cella


def crea_df_reg(df):
    c_g_3=[]    #consumo giorno -3
    t_g_3=[]    #temperatura giorno -3   
    c_s_3=[]    #consumo sera -3
    t_s_3=[]    #temperatura sera -3 
    c_g_2=[]    #consumo giorno -2
    t_g_2=[]    #temperatura giorno -2
    c_s_2=[]    #consumo sera -1
    t_s_2=[]    #temperatura sera -1 
    c_g_1=[]    #consumo giorno -1
    t_g_1=[]    #temperatura giorno -1
    c_s_1=[]    #consumo sera -1
    t_s_1=[]    #temperatura sera -1 
    week=[]     #giorno della settimana
    target_g=[] #consumi del target della giornata
    target_s=[] #consumi del target della sera
    for i in range(9,183,3):
        c_g_3.append(df['consumi'][i-9])
        t_g_3.append(df['temp'][i-9])
        c_s_3.append(df['consumi'][i-7])
        t_s_3.append(df['temp'][i-7])
        c_g_2.append(df['consumi'][i-6])
        t_g_2.append(df['temp'][i-6])
        c_s_2.append(df['consumi'][i-4])
        t_s_2.append(df['temp'][i-4])
        c_g_1.append(df['consumi'][i-3])
        t_g_1.append(df['temp'][i-3])
        c_s_1.append(df['consumi'][i-1])
        t_s_1.append(df['temp'][i-1])
        week.append(df['week'][i])
        target_g.append(df['consumi'][i])
        target_s.append(df['consumi'][i+2])
    dataframe=pd.DataFrame({'c_g_3':c_g_3,'t_g_3':t_g_3,'c_s_3':c_s_3,'t_s_3':t_s_3,'c_g_2':c_g_2,'t_g_2':t_g_2,'c_s_2':c_s_2,'t_s_2':t_s_2,'c_g_1':c_g_3,'t_g_1':t_g_1,'c_s_1':c_s_1,'t_s_1':t_s_1,'week':week,'target_g':target_g,'target_s':target_s})
    return dataframe  


def crea_df_class():
    # come prima cosa uniamo i dataframe grid e consumi così da selezionare subito le celle 'bc' e usare solo quelle
    trento=consumi.merge(grid.loc[:,['geometry','category','cellId']], how='left', on='cellId')
    trento=trento[trento['category']=='bc']
    # come per la regressione anche qui mi conviene aggiungere la colonna del tipo di orario
    trento = add_orario(trento)
    trento=trento.groupby(['mounth','day','week','cellId','utenze','orario']).sum()
    trento.reset_index(level=[0,1,2,3,4,5],inplace=True)
    trento['C/U']=trento['consumi']/trento['utenze']
    
    
    # creo 4 liste contenenti le celle con più consumi giorno per giorno per giorno e sera
    # con il rispettivo consumo
    consumi_g=trento[trento['orario']=='giorno']
    consumi_g.reset_index(drop=True, inplace=True)
    top_g=[]
    topc_g=[]
    week=[]  # mi serve anche sta colonna ed è il modo più facile per averla
    for i in range(0,1342,22):
        ind=consumi_g.loc[i:i+21]['C/U'].idxmax()
        top_g.append(consumi_g['cellId'][ind])
        topc_g.append(consumi_g['C/U'][ind])
        week.append(consumi_g['week'][ind])
    top_g=list(map(str, top_g))
        
    consumi_s=trento[trento['orario']=='giorno']
    consumi_s.reset_index(drop=True, inplace=True)
    top_s=[]
    topc_s=[]
    for i in range(0,1342,22):
        ind=consumi_s.loc[i:i+21]['C/U'].idxmax()
        top_s.append(consumi_s['cellId'][ind])
        topc_s.append(consumi_s['C/U'][ind])
    top_s=list(map(str, top_s))
    
    data=pd.DataFrame({'consumi_g_3':topc_g[0:58],'consumi_s_3':topc_s[0:58],
                  'consumi_g_2':topc_g[1:59],'consumi_s_2':topc_s[1:59],
                  'consumi_g_1':topc_g[2:60],'consumi_s_1':topc_s[2:60],'week':week[3:61],
                  'target_g':top_g[3:61],'target_s':top_s[3:61] }  )
    return data