# -*- coding: utf-8 -*-
"""
predictie_2019_allfromdia.py
hatyan master configfile
voor alle stations indien mogelijk:
    - analyse van 4 jaar aan data
    - analyse van 19 jaar aan data
    - combineren
    - predictie maken

"""

import os, sys
import datetime as dt
import pandas as pd
import hatyan

file_config = os.path.realpath(__file__)
dir_output, timer_start = hatyan.init_RWS(file_config, sys.argv, interactive_plots=False)
#dir_testdata = 'P:\\1209447-kpp-hydraulicaprogrammatuur\\hatyan\\hatyan_data_acceptancetests'
dir_testdata = 'C:\\DATA\\hatyan_data_acceptancetests'

stats_all = ['ABDN','AMLAHVN','BAALHK','BATH','BERGSDSWT','BORSSLE','BOURNMH','BRESKS','BROUWHVSGT02','BROUWHVSGT08','CADZD','CROMR','CUXHVN','DELFZL','DENHDR','DENOVBTN','DEVPT','DORDT','DOVR','EEMHVN','EEMSHVN','EURPFM','EURPHVN','FELSWE','FISHGD','GEULHVN','GOIDSOD','GOUDBG','HAGSBNDN','HANSWT','HARLGN','HARMSBG','HARTBG','HARTHVN','HARVT10','HEESBN','HELLVSS','HOEKVHLD','HOLWD','HUIBGT','IJMDBTHVN','IJMDSMPL','IMMHM','KATSBTN','KEIZVR','KINLBVE','KORNWDZBTN','KRAMMSZWT','KRIMPADIJSL','KRIMPADLK','K13APFM','LAUWOG','LEITH','LICHTELGRE','LITHDP','LLANDNO','LOWST','MAASMSMPL','MAASSS','MAESLKRZZDE','MARLGT','MOERDK','NES','NEWHVN','NEWLN','NIEUWSTZL','NORTHSS','OOSTSDE04','OOSTSDE11','OOSTSDE14','OUDSD','OVLVHWT','PARKSS','PETTZD','PORTSMH','RAKND','ROOMPBNN','ROOMPBTN','ROTTDM','ROZBSSNZDE','ROZBSSZZDE','SCHAARVDND','SCHEVNGN','SCHIERMNOG','SCHOONHVN','SHEERNS','SINTANLHVSGR','SPIJKNSE','STAVNSE','STELLDBTN','STORNWY','SUURHBNZDE','TENNSHVN','TERNZN','TERSLNZE','TEXNZE','VLAARDGN','VLAKTVDRN','VLIELHVN','VLISSGN','VURN','WALSODN','WERKDBTN','WESTKPLE','WESTTSLG','WEYMH','WHITBY','WICK','WIERMGDN','YERSKE','ZALTBML','A12','AUKFPFM','AWGPFM','D15','F16','F3PFM','J6','K14PFM','L9PFM','NORTHCMRT','Q1']
stats_xfac0 = ['A12','ABDN','AUKFPFM','BOURNMH','CROMR','CUXHVN','D15','DEVPT','DOVR','F16','F3PFM','FELSWE','FISHGD','IMMHM','J6','K13APFM','K14PFM','KINLBVE','LEITH','LLANDNO','LOWST','NEWHVN','NEWLN','NORTHCMRT','NORTHSS','PORTSMH','SHEERNS','STORNWY','WEYMH','WHITBY','WICK']
stats_MSL = ['EURPFM','K13APFM','LICHTELGRE','A12','AUKFPFM','AWGPFM','D15','F16','F3PFM','J6','K14PFM','L9PFM','NORTHCMRT','Q1']

#selected_stations = stats_all
selected_stations = ['CADZD','DORDT','DEVPT']

file_slotgemiddelden = os.path.join(dir_testdata,'predictie2019','_slotgemiddelden_predictie2019.txt')
stations_slotgem = pd.read_csv(file_slotgemiddelden, names=['slotgemiddelde'], comment='#', delim_whitespace=True)

stats_noana = []
stats_no4Y = []
stats_no19Y = []

for current_station in selected_stations:
    print('-'*100)
    print('%-45s = %s'%('station_name',current_station))
    print('-'*5)
    
    #START OF STATION SETTINGS
    #nodalfactors
    nodalfactors = True
    #xfactor
    if current_station in stats_xfac0:
        xfac=False
    else:
        xfac=True
    #analysis_peryear
    analysis_peryear=True
    #constituent list
    if current_station in ['D15','F3PFM','K14PFM','MAESLKRZZDE','Q1','A12','AWGPFM','F16','J6','L9PFM']:
        const_list = hatyan.get_const_list_hatyan('month') #21 const, potentially extended with component splitting (5 components) and SA+SM
    elif current_station in ['AMLAHVN']:
        const_list = hatyan.get_const_list_hatyan('halfyear') #88 const
    else:
        const_list = hatyan.get_const_list_hatyan('year') #94 const
    #component splitting, not necesary for D15/F3PFM/K14PFM, since there is no 19Y data available
    CS_comps = None
    #vertical reference
    if current_station in stats_MSL:
        vertref='MSL'
    else:
        vertref='NAP'
    #END OF STATION SETTINGS
 
   
    file_data_comp0_raw = [os.path.join(dir_testdata,'predictie2019','%s_obs%i.txt'%(current_station, file_id)) for file_id in [1,2,3,4]]
    file_data_comp0 = [x for x in file_data_comp0_raw if os.path.exists(x)] #slim filename list down to available files/years
        
    file_data_comp1 = os.path.join(dir_testdata,'predictie2019','%s_obs19.txt'%(current_station))
    
    file_data_compvali = os.path.join(dir_testdata,'predictie2019','%s_ana.txt'%(current_station))
    
    times_ext_pred = [dt.datetime(2019,1,1),dt.datetime(2020,1,1)]
    times_step_pred = 10

    file_data_predvali = os.path.join(dir_testdata,'predictie2019','%s_pre.txt'%(current_station))
    file_data_predvaliHWLW = os.path.join(dir_testdata,'predictie2019','%s_ext.txt'%(current_station))
    
    if not os.path.exists(file_data_compvali):
        stats_noana.append(current_station)
        continue

    if file_data_comp0 == []:
        stats_no4Y.append(current_station)
        continue
        
    #component groups
    ts_measurements_group0 = hatyan.readts_dia(filename=file_data_comp0, station=current_station)
    times_ext_comp0 = [ts_measurements_group0.index[0],ts_measurements_group0.index[-1]]
    times_stepcomp0 = (ts_measurements_group0.index[1]-ts_measurements_group0.index[0]).total_seconds()/60

    comp_frommeasurements_avg_group0, comp_frommeasurements_all_group0 = hatyan.get_components_from_ts(ts=ts_measurements_group0, const_list=const_list, nodalfactors=nodalfactors, xfac=xfac, fu_alltimes=False, analysis_peryear=analysis_peryear, return_allyears=True, CS_comps=CS_comps)

    #fig,(ax1,ax2) = hatyan.plot_components(comp_frommeasurements_avg_group0, comp_allyears=comp_frommeasurements_all_group0)
    #fig.savefig('components_%s_4Y.png'%(current_station))
    #comp_metadata = {'station':current_station, 'vertref':vertref, 'times_ext':[x.strftime('%Y%m%d%H%M') for x in times_ext_comp0], 'times_step':times_stepcomp0, 'xfac':xfac}
    #hatyan.write_components(comp_frommeasurements_avg_group0, filename='components_%s_4Y.txt'%(current_station), metadata=comp_metadata)
    if not os.path.exists(file_data_comp1): #check if 19Y file is available
        stats_no19Y.append(current_station)
        continue

    ts_measurements_group1 = hatyan.readts_dia(filename=file_data_comp1, station=current_station)
    comp_fromfile_group1 = hatyan.get_components_from_ts(ts=ts_measurements_group1, const_list=const_list, nodalfactors=nodalfactors, xfac=xfac, fu_alltimes=False, analysis_peryear=False)
    
    #merge component groups (SA/SM from 19Y, rest from 4Y)
    COMP_merged = hatyan.merge_componentgroups(comp_main=comp_frommeasurements_avg_group0, comp_sec=comp_fromfile_group1, comp_sec_list=['SA','SM'])
    #replace A0 amplitude (middenstand) by slotgemiddelde
    if current_station in stations_slotgem.index.tolist():
        COMP_merged.loc['A0','A'] = stations_slotgem.loc[current_station,'slotgemiddelde']

    COMP_validation = hatyan.read_components(filename=file_data_compvali)
    fig, (ax1,ax2) = hatyan.plot_components(COMP_merged, comp_validation=COMP_validation)
    fig.savefig('components_%s_merged.png'%(current_station))
    comp_metadata = {'station':current_station, 'vertref':vertref, 'times_ext':times_ext_comp0, 'times_ext2':'SA and SM imported from analyseresultatenbestand', 'times_step':times_stepcomp0, 'xfac':xfac}
    hatyan.write_components(COMP_merged, filename='components_%s_merged.txt'%(current_station), metadata=comp_metadata)

    #prediction and validation
    ts_prediction = hatyan.prediction(comp=COMP_merged, nodalfactors=nodalfactors, xfac=xfac, fu_alltimes=False, times_ext=times_ext_pred, timestep_min=times_step_pred)
    ts_validation = hatyan.readts_dia(filename=file_data_predvali, station=current_station)
    #ts_ext_validation = hatyan.readts_dia(filename=file_data_predvaliHWLW, station=current_station)
    hatyan.write_tsdia(ts=ts_prediction, station=current_station, vertref=vertref, filename='prediction_%im_%s.dia'%(times_step_pred,current_station))
    #ts_ext_prediction = hatyan.calc_HWLW(ts=ts_prediction)
    #hatyan.write_tsdia_HWLW(ts_ext=ts_ext_prediction, station=current_station, vertref=vertref, filename='prediction_HWLW_%im_%s.dia'%(times_step_pred, current_station))
    #fig, (ax1,ax2) = hatyan.plot_timeseries(ts=ts_prediction, ts_ext=ts_ext_prediction, ts_ext_validation=ts_ext_validation)
    #fig.savefig('prediction_%im_%s_HWLW'%(times_step_pred, current_station))
    fig, (ax1,ax2) = hatyan.plot_timeseries(ts=ts_prediction, ts_validation=ts_validation)
    fig.savefig('prediction_%im_%s_validation'%(times_step_pred, current_station))
    #fig, (ax1,ax2) = hatyan.plot_timeseries(ts=ts_prediction, ts_validation=ts_measurements_group0)
    #fig.savefig('prediction_%im_%s_measurements'%(times_step_pred, current_station))

        
hatyan.exit_RWS(timer_start)
print('\nthese %i stations were requested for processing:\n%s'%(len(selected_stations),selected_stations))
print('\nthese %i stations were not processed because there is no ana/comp dataset available:\n%s'%(len(stats_noana),stats_noana))
print('\nthese %i stations were not processed because there is no 4Y or likewise data available:\n%s'%(len(stats_no4Y),stats_no4Y))
print('\nthese %i stations were not processed because there is no 19Y data available:\n%s'%(len(stats_no19Y),stats_no19Y))


