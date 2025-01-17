# -*- coding: utf-8 -*-
"""
numbering_extremes.py
Deze configfile kan gebruikt worden om de dataset data_M2phasediff_perstation.txt bij te werken

"""

import os, sys
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
import hatyan

file_config = os.path.realpath(__file__) #F9 doesnt work, only F5 (F5 also only method to reload external definition scripts)
dir_output, timer_start = hatyan.init_RWS(file_config, sys.argv, interactive_plots=False)
#dir_testdata = 'P:\\1209447-kpp-hydraulicaprogrammatuur\\hatyan\\hatyan_data_acceptancetests'
dir_testdata = 'C:\\DATA\\hatyan_data_acceptancetests'

stats_all = ['ABDN','AMLAHVN','BAALHK','BATH','BERGSDSWT','BORSSLE','BOURNMH','BRESKS','BROUWHVSGT02','BROUWHVSGT08','CADZD','CROMR','CUXHVN','DELFZL','DENHDR','DENOVBTN','DEVPT','DORDT','DOVR','EEMHVN','EEMSHVN','EURPFM','EURPHVN','FELSWE','FISHGD','GEULHVN','GOIDSOD','GOUDBG','HAGSBNDN','HANSWT','HARLGN','HARMSBG','HARTBG','HARTHVN','HARVT10','HEESBN','HELLVSS','HOEKVHLD','HOLWD','HUIBGT','IJMDBTHVN','IJMDSMPL','IMMHM','KATSBTN','KEIZVR','KINLBVE','KORNWDZBTN','KRAMMSZWT','KRIMPADIJSL','KRIMPADLK','K13APFM','LAUWOG','LEITH','LICHTELGRE','LITHDP','LLANDNO','LOWST','MAASMSMPL','MAASSS','MAESLKRZZDE','MARLGT','MOERDK','NES','NEWHVN','NEWLN','NIEUWSTZL','NORTHSS','OOSTSDE04','OOSTSDE11','OOSTSDE14','OUDSD','OVLVHWT','PARKSS','PETTZD','PORTSMH','RAKND','ROOMPBNN','ROOMPBTN','ROTTDM','ROZBSSNZDE','ROZBSSZZDE','SCHAARVDND','SCHEVNGN','SCHIERMNOG','SCHOONHVN','SHEERNS','SINTANLHVSGR','SPIJKNSE','STAVNSE','STELLDBTN','STORNWY','SUURHBNZDE','TENNSHVN','TERNZN','TERSLNZE','TEXNZE','VLAARDGN','VLAKTVDRN','VLIELHVN','VLISSGN','VURN','WALSODN','WERKDBTN','WESTKPLE','WESTTSLG','WEYMH','WHITBY','WICK','WIERMGDN','YERSKE','ZALTBML','A12','AUKFPFM','AWGPFM','D15','F16','F3PFM','J6','K14PFM','L9PFM','NORTHCMRT','Q1']
stats_xfac0 = ['A12','ABDN','AUKFPFM','BOURNMH','CROMR','CUXHVN','D15','DEVPT','DOVR','F16','F3PFM','FELSWE','FISHGD','IMMHM','J6','K13APFM','K14PFM','KINLBVE','LEITH','LLANDNO','LOWST','NEWHVN','NEWLN','NORTHCMRT','NORTHSS','PORTSMH','SHEERNS','STORNWY','WEYMH','WHITBY','WICK']
stats_MSL = ['EURPFM','K13APFM','LICHTELGRE','A12','AUKFPFM','AWGPFM','D15','F16','F3PFM','J6','K14PFM','L9PFM','NORTHCMRT','Q1']

stats_CADZDm2 = ['WICK']
stats_CADZDm1 = ['ABDN','CROMR','DOVR','EURPFM','FELSWE','IMMHM','LEITH','LOWST','NORTHSS','SHEERNS','WHITBY','VLAKTVDRN']
#stats_CADZD0 = ['CADZD','BATH','VLISSGN','ROOMPBTN','HARVT10','HOEKVHLD','ROTTDM','DORDT','SCHEVNGN','IJMDBTHVN','PETTZD','DENHDR','HARLGN','CUXHVN']
stats_CADZDp1 = []
stats_CADZDtoofar = ['NORTHCMRT','FISHGD','LLANDNO','NEWLN','DEVPT','WEYMH','PORTSMH','BOURNMH','NEWHVN','STORNWY','KINLBVE']

#selected_stations = stats_all
selected_stations = ['AUKFPFM']
selected_stations = ['WICK','ABDN','LEITH','WHITBY','IMMHM','CROMR','FELSWE','CADZD','VLISSGN','TERNZN','ROOMPBTN','HARVT10','HOEKVHLD','ROTTDM','DORDT','SCHEVNGN','IJMDBTHVN','PETTZD','DENHDR','DENOVBTN','HARLGN','HOLWD','SCHIERMNOG','LAUWOG','EEMSHVN','DELFZL','CUXHVN']
#selected_stations = ['CROMR','CADZD','HOEKVHLD','DENHDR','CUXHVN']
#selected_stations = ['CADZD','DENHDR']

file_ldb = os.path.join(dir_testdata,'other','wvs_coastline3.ldb') #WGS84 ldb is converted to RD, but does not change anything wrt to matlab converted ldb, which is good
ldb_pd_wgs = pd.read_csv(file_ldb, delim_whitespace=True,skiprows=4,names=['x','y'],na_values=[999.999])
x_out, y_out = hatyan.convertcoordinates(coordx_in=ldb_pd_wgs['x'].values, coordy_in=ldb_pd_wgs['y'].values, epsg_in=4326, epsg_out=28992)
ldb_pd = pd.DataFrame({'RDx':x_out/1000, 'RDy':y_out/1000})

if 0:
    """
    #all stations in NLD, including several from English coast for which it is know how many tidal waves before CADZD they are. ZALTBML excluded because there is no _ana file available
    stats_xfac1_ana4yr_NAP = [x for x in stats_all if x not in stats_xfac0+stats_MSL+['ZALTBML']]
    selected_stations = stats_xfac1_ana4yr_NAP+stats_CADZDm2+stats_CADZDm1+['CUXHVN']
    selected_stations = list(np.unique(selected_stations))
    selected_stations = ['WICK', 'ABDN', 'LEITH', 'WHITBY', 'IMMHM', 'CROMR', 'FELSWE',
           'VLAKTVDRN', 'CADZD', 'WESTKPLE', 'OOSTSDE11', 'BRESKS', 'VLISSGN',
           'BROUWHVSGT02', 'ROOMPBTN', 'OOSTSDE14', 'BORSSLE', 'OOSTSDE04',
           'BROUWHVSGT08', 'TERNZN', 'HARVT10', 'OVLVHWT', 'STELLDBTN', 'HANSWT',
           'WALSODN', 'MAASMSMPL', 'ROOMPBNN', 'TENNSHVN', 'BAALHK', 'HOEKVHLD',
           'EURPHVN', 'HARTHVN', 'ROZBSSNZDE', 'AMLAHVN', 'SCHAARVDND',
           'MAESLKRZZDE', 'SUURHBNZDE', 'BATH', 'STAVNSE', 'KRAMMSZWT', 'KATSBTN',
           'SINTANLHVSGR', 'YERSKE', 'BERGSDSWT', 'SCHEVNGN', 'MARLGT', 'MAASSS',
           'HARMSBG', 'ROZBSSZZDE', 'GEULHVN', 'VLAARDGN', 'HARTBG', 'SPIJKNSE',
           'EEMHVN', 'PARKSS', 'ROTTDM', 'GOIDSOD', 'IJMDSMPL', 'KRIMPADIJSL',
           'IJMDBTHVN', 'KRIMPADLK', 'GOUDBG', 'DORDT', 'PETTZD', 'SCHOONHVN',
           'DENHDR', 'TEXNZE', 'WERKDBTN', 'HAGSBNDN', 'VURN', 'MOERDK', 'OUDSD',
           'RAKND', 'HELLVSS', 'DENOVBTN', 'TERSLNZE', 'KEIZVR', 'VLIELHVN',
           'WESTTSLG', 'KORNWDZBTN', 'WIERMGDN', 'HARLGN', 'HUIBGT', 'NES',
           'HEESBN', 'LAUWOG', 'SCHIERMNOG', 'HOLWD', 'EEMSHVN', 'LITHDP',
           'DELFZL', 'NIEUWSTZL', 'CUXHVN'] #ordered version of above
    """
    #all stations and ones that are too far away (north, south and southwest of UK) removed
    selected_stations = stats_all
    for stat_remove in stats_CADZDtoofar:
        selected_stations.remove(stat_remove)
    selected_stations.remove('LITHDP') #problem station for at least 2018
    selected_stations.remove('ZALTBML') #no ana file available

create_spatialplot = True

yr=2000
yr_HWLWno = 2010
for yr_HWLWno in [2000,2010,2021]: #range(1999,2022):
    stats = pd.DataFrame()
    pd_firstlocalHW_list = pd.DataFrame()

    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(15,8))
    n_colors = len(selected_stations)
    colors = plt.cm.jet(np.linspace(0,1,n_colors))
    for i_stat, current_station in enumerate(selected_stations):
        print('-'*100)
        print('%-45s = %s'%('station_name',current_station))
        print('-'*5)
        
        #START OF STATION SETTINGS
        #xfactor
        if current_station in stats_xfac0:
            xfac=False
        else:
            xfac=True
        #analysis_peryear
        #analysis_peryear=True
        #constituent list
        const_list = hatyan.get_const_list_hatyan('year') #94 const
        #vertical reference
        #vertref='NAP'
        #END OF STATION SETTINGS
        
        file_data_comp0 = os.path.join(dir_testdata,'predictie2019','%s_ana.txt'%(current_station))
    
        #file_data_compvali = os.path.join(dir_testdata,'predictie2019','%s_ana.txt'%(current_station))
        times_ext_pred = [dt.datetime(yr-1,12,31),dt.datetime(yr,1,2,12)]
        times_step_pred = 1
        
        file_data_predvali = os.path.join(dir_testdata,'predictie2019','%s_pre.txt'%(current_station))
        #file_data_predvaliHWLW = os.path.join(dir_testdata,'predictie2019','%s_ext.txt'%(current_station))
    
        #component groups
        COMP_merged = hatyan.read_components(filename=file_data_comp0)
        
        #prediction and validation
        ts_prediction = hatyan.prediction(comp=COMP_merged, nodalfactors=True, xfac=xfac, fu_alltimes=True, times_ext=times_ext_pred, timestep_min=times_step_pred)

        #ts_validation = hatyan.readts_dia(filename=file_data_predvali, station=current_station)
        #ts_ext_validation = hatyan.readts_dia(filename=file_data_predvaliHWLW, station=current_station)
        #hatyan.write_tsdia(ts=ts_prediction, station=current_station, vertref=vertref, filename='prediction_%im_%s.dia'%(times_step_pred,current_station))
        ts_ext_prediction = hatyan.calc_HWLW(ts=ts_prediction)
        
        if i_stat == 0:
            COMP_merged_CADZD = hatyan.read_components(filename=file_data_comp0.replace(current_station,'CADZD'))
            ts_prediction_CADZD = hatyan.prediction(comp=COMP_merged_CADZD, nodalfactors=True, xfac=xfac, fu_alltimes=True, times_ext=times_ext_pred, timestep_min=times_step_pred)
            ts_prediction_CADZD_M2 = hatyan.prediction(comp=COMP_merged_CADZD.loc[['A0','M2']], nodalfactors=True, xfac=xfac, fu_alltimes=True, times_ext=times_ext_pred, timestep_min=times_step_pred)
            ax1.plot(ts_prediction_CADZD_M2.index, ts_prediction_CADZD_M2['values'], label='CADZD_M2', color='k')
            ts_ext_prediction_CADZD = hatyan.calc_HWLW(ts=ts_prediction_CADZD, debug=True)
            bool_newyear = (ts_ext_prediction_CADZD.index>dt.datetime(yr,1,1)) & (ts_ext_prediction_CADZD['HWLWcode']==1)
            firstHWcadz = ts_ext_prediction_CADZD.loc[bool_newyear].index[0].to_pydatetime()
            #firstHWcadz = dt.datetime(2000,1,1,9,45,0)#dt.datetime(2010,1,1,13,40,0)
        
        M2phasediff_raw = (COMP_merged.loc['M2','phi_deg']-COMP_merged_CADZD.loc['M2','phi_deg'])%360
        
        if current_station in stats_CADZDp1:
            bool_wrtHWcadz = (ts_ext_prediction.index >= firstHWcadz) & (ts_ext_prediction['HWLWcode']==1)
            ts_firstlocalHW = ts_ext_prediction.loc[bool_wrtHWcadz].iloc[1] #second HW after HWcadzd
            M2phasediff = M2phasediff_raw+360
        elif current_station in stats_CADZDm1:
            bool_wrtHWcadz = (ts_ext_prediction.index <= firstHWcadz) & (ts_ext_prediction['HWLWcode']==1)
            ts_firstlocalHW = ts_ext_prediction.loc[bool_wrtHWcadz].iloc[-1] #last HW before HWcadzd
            M2phasediff = M2phasediff_raw-360
        elif current_station in stats_CADZDm2:
            bool_wrtHWcadz = (ts_ext_prediction.index <= firstHWcadz) & (ts_ext_prediction['HWLWcode']==1)
            ts_firstlocalHW = ts_ext_prediction.loc[bool_wrtHWcadz].iloc[-2] #second to last HW before HWcadzd
            M2phasediff = M2phasediff_raw-360-360
        else:
            bool_wrtHWcadz = (ts_ext_prediction.index >= firstHWcadz) & (ts_ext_prediction['HWLWcode']==1)
            ts_firstlocalHW = ts_ext_prediction.loc[bool_wrtHWcadz].iloc[0] #first HW after HWcadzd
            M2phasediff = M2phasediff_raw
            
        #print('tdiff %s:'%(current_station), ts_firstlocalHW.index-firstHWcadz)
        pdrow = pd.DataFrame({'time': [ts_firstlocalHW.name], 'HWtdiff_hr': [(ts_firstlocalHW.name-firstHWcadz).total_seconds()/3600], 'M2phase':COMP_merged.loc['M2','phi_deg'], 'M2phasediff':M2phasediff}, index=[current_station])
        if create_spatialplot:
            diablocks_pd_extra = hatyan.get_diablocks(filename=file_data_predvali)
            RDx, RDy = hatyan.convertcoordinates(coordx_in=diablocks_pd_extra.loc[0,'x'], coordy_in=diablocks_pd_extra.loc[0,'y'], epsg_in=diablocks_pd_extra.loc[0,'epsg'], epsg_out=28992)
            pdrow['RDx'] = RDx/1000 #from m to km
            pdrow['RDy'] = RDy/1000 #from m to km
        stats = stats.append(pdrow)
            
        #hatyan.write_tsdia_HWLW(ts_ext=ts_ext_prediction, station=current_station, vertref=vertref, filename='prediction_HWLW_%im_%s.dia'%(times_step_pred, current_station))
        #fig, (ax1,ax2) = hatyan.plot_timeseries(ts=ts_prediction, ts_ext=ts_ext_prediction, ts_ext_validation=ts_ext_validation)
        #fig.savefig('prediction_%im_%s_HWLW'%(times_step_pred, current_station))
        #fig, (ax1,ax2) = hatyan.plot_timeseries(ts=ts_prediction, ts_ext=ts_ext_prediction)
        #fig.savefig('prediction_%im_%s_validation'%(times_step_pred, current_station))
        
        ax1.plot(ts_prediction.index, ts_prediction['values'], label=current_station, color=colors[i_stat])
        ax1.plot([ts_firstlocalHW.name,ts_firstlocalHW.name], [ts_firstlocalHW['values'], 2.5], '--', linewidth=1.5, color=colors[i_stat])
        ax1.plot(ts_firstlocalHW.name,ts_firstlocalHW['values'],'x', color=colors[i_stat])
        
        if 1: #validation case
            #calculate tidal wave number
            times_ext_pred_HWLWno = [dt.datetime(yr_HWLWno-1,12,31),dt.datetime(yr_HWLWno,1,2,12)]
            COMP_merged_temp = COMP_merged.copy()
            #COMP_merged_temp.loc['M2','A']=0.05
            ts_prediction_HWLWno = hatyan.prediction(comp=COMP_merged_temp, nodalfactors=True, xfac=xfac, fu_alltimes=True, times_ext=times_ext_pred_HWLWno, timestep_min=times_step_pred)
            ts_ext_prediction_HWLWno_pre = hatyan.calc_HWLW(ts=ts_prediction_HWLWno)
            #fig,(ax1,ax2) = hatyan.plot_timeseries(ts=ts_prediction_HWLWno, ts_ext=ts_ext_prediction_HWLWno_pre)
            #breakit
            
            print(current_station)
            if 0: #corr_tideperiods instead of txt file, does not give decent results for all stations
                if current_station in stats_CADZDm1:
                    corr_tideperiods = -360
                elif current_station in stats_CADZDm2:
                    corr_tideperiods = -2*360
                else:
                    corr_tideperiods = 0
                ts_ext_prediction_HWLWno = hatyan.calc_HWLWnumbering(ts_ext=ts_ext_prediction_HWLWno_pre, station=None, corr_tideperiods=corr_tideperiods)
            else:
                ts_ext_prediction_HWLWno = hatyan.calc_HWLWnumbering(ts_ext=ts_ext_prediction_HWLWno_pre, station=current_station)
            
            print(ts_ext_prediction_HWLWno)
            for irow, pdrow in ts_ext_prediction_HWLWno.iterrows():
                ax2.text(pdrow.name,pdrow['values'],pdrow['HWLWno'].astype(int), color=colors[i_stat])
            HWLWno_focus = np.int(np.round((dt.datetime(yr_HWLWno,1,1,9,45)-dt.datetime(2000,1,1,9,45)).total_seconds()/3600/12.420601))
            ts_firstlocalHW_fromcalc = ts_ext_prediction_HWLWno[(ts_ext_prediction_HWLWno['HWLWcode']==1) & (ts_ext_prediction_HWLWno['HWLWno']==HWLWno_focus)]
            
            pd_firstlocalHW_list = pd_firstlocalHW_list.append(ts_firstlocalHW_fromcalc)
            
            ax2.plot(ts_prediction_HWLWno.index, ts_prediction_HWLWno['values'], label=current_station, color=colors[i_stat])
            ax2.plot([ts_firstlocalHW_fromcalc.index[0],ts_firstlocalHW_fromcalc.index[0]], [ts_firstlocalHW_fromcalc['values'].iloc[0], 2.5], '--', linewidth=1.5, color=colors[i_stat])
            ax2.plot(ts_firstlocalHW_fromcalc.index,ts_firstlocalHW_fromcalc['values'],'x', color=colors[i_stat])
    
    ax2.plot(pd_firstlocalHW_list.index,pd_firstlocalHW_list['values'],'-ok')
    
    stats['M2phasediff_hr'] = stats['M2phasediff']/360*12.420601
    stats_M2phasediff_out = stats.sort_values('M2phasediff_hr')['M2phasediff']
    #stats_M2phasediff_out.to_csv(r'c:\DATA\hatyan_github\hatyan\data_M2phasediff_perstation_new.txt', sep=' ', header=False, float_format='%.2f')
    
    #hatyan.exit_RWS(timer_start)
    print(stats)    
    print('')
    print(hatyan.get_hatyan_freqs(['M2']))
    
    ax1.set_xlim(times_ext_pred)
    ax2.set_xlim(times_ext_pred_HWLWno)
    ax2.set_xlim([dt.datetime(yr_HWLWno-1,12,31),dt.datetime(yr_HWLWno,1,2,12)])
    ax1_ylim = ax1.get_ylim()
    ax1.plot([dt.datetime(yr,1,1),dt.datetime(yr,1,1)],ax1_ylim,'k--')
    fig.tight_layout()
    for ax in (ax1,ax2):
        ax.legend(loc=2, fontsize=7)#bbox_to_anchor=(1,1))
        ax.set_ylim(ax1_ylim)
        import matplotlib.dates as mdates
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    fig.savefig('tide_numbering_%i.png'%(yr_HWLWno), dpi=250)

if create_spatialplot:
    fig2, (fig2_ax1) = plt.subplots(1,1,figsize=(10,9))
    fig2_ax1.plot(ldb_pd['RDx'],ldb_pd['RDy'],'-k',linewidth=0.4)
    fig2_ax1.plot(stats.loc['CADZD','RDx'], stats.loc['CADZD','RDy'],'xk')
    pc = fig2_ax1.scatter(stats['RDx'], stats['RDy'],10,stats['M2phasediff'], vmin=-360,vmax=360, cmap='hsv')
    fig2.colorbar(pc, ax=fig2_ax1)
    fig2_ax1.set_xlim([-400,360])
    fig2_ax1.set_ylim([200,1200])
    fig2_ax1.set_aspect('equal')
    for irow, pdrow in stats.iterrows():
        fig2_ax1.text(pdrow['RDx'], pdrow['RDy'], '%.1f'%(pdrow['M2phasediff']))
        #fig2_ax1.text(pdrow['RDx'], pdrow['RDy'], '%.1f (%s)'%(pdrow['M2phasediff'],pdrow.name))
    fig2.tight_layout()
    if 0:
        import contextily as ctx
        source_list = [ctx.providers.Stamen.Terrain, #default source
                   ctx.providers.Esri.WorldImagery,
                   ctx.providers.CartoDB.Voyager,
                   #ctx.providers.NASAGIBS.ViirsEarthAtNight2012,
                   ctx.providers.Stamen.Watercolor]
        ctx.add_basemap(fig2_ax1, source=source_list[1], crs="EPSG:28992", attribution_size=5)
    fig2.savefig('tide_numbering_phasediff.png', dpi=250)

hatyan.exit_RWS(timer_start) #provides footer to outputfile when calling this script with python
