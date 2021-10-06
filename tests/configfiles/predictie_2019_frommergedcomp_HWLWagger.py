# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 10:33:54 2020

@author: veenstra
"""
import pytest
import os, sys
#sys.path.append(r'c:\DATA\hatyan_github')
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
plt.close('all')

from hatyan import timeseries as Timeseries
from hatyan import components as Components
from hatyan.analysis_prediction import get_components_from_ts, prediction
from hatyan.hatyan_core import get_const_list_hatyan
from hatyan.wrapper_RWS import get_outputfoldername, init_RWS, exit_RWS

file_config = os.path.realpath(__file__)
dir_output, timer_start = init_RWS(file_config, sys.argv, interactive_plots=False)
#dir_testdata = 'P:\\1209447-kpp-hydraulicaprogrammatuur\\hatyan\\hatyan_data_acceptancetests'
dir_testdata = 'C:\\DATA\\hatyan_data_acceptancetests'

file_slotgemiddelden = os.path.join(dir_testdata,'predictie2019','_slotgemiddelden_predictie2019.txt')
stations_slotgem = pd.read_csv(file_slotgemiddelden, names=['slotgemiddelde'], comment='#', delim_whitespace=True)

times_ext_pred_HWLWno = [dt.datetime(2010,1,31,3),dt.datetime(2010,2,17,12)] #longer period with alternating aggers and no aggers, also eerste HW wordt als lokaal ipv primair HW gezien, also extra agger outside of 1stLW/agger/2ndLW sequence
times_step_pred = 1
stat_list = ['HOEKVHLD','DENHDR','PETTZD'] #HOEKVHLD has alternating aggers, DENHDR has double HW's (PETTZD ook)

for current_station in stat_list:

    file_data_comp0 = os.path.join(dir_testdata,'predictie2019','%s_ana.txt'%(current_station))
    COMP_merged = Components.read_components(filename=file_data_comp0)
    COMP_merged_temp = COMP_merged.copy()
    
    ts_prediction_HWLWno = prediction(comp=COMP_merged_temp, nodalfactors=True, xfac=True, fu_alltimes=True, times_ext=times_ext_pred_HWLWno, timestep_min=times_step_pred)
    ts_ext_prediction_main = Timeseries.calc_HWLW(ts=ts_prediction_HWLWno)#, debug=True)
    ts_ext_prediction_all = Timeseries.calc_HWLW(ts=ts_prediction_HWLWno, calc_HWLW345=True, calc_HWLW345_cleanup1122=False)#, debug=True)
    ts_ext_prediction_clean = Timeseries.calc_HWLW(ts=ts_prediction_HWLWno, calc_HWLW345=True, calc_HWLW345_cleanup1122=True) #for numbering, cannot cope with 11/22 HWLWcodes
    
    ts_ext_prediction_HWLWno = Timeseries.calc_HWLWnumbering(ts_ext=ts_ext_prediction_clean, station=current_station)
    
    fig, (ax1,ax2) = Timeseries.plot_timeseries(ts=ts_prediction_HWLWno, ts_ext=ts_ext_prediction_all)
    for irow, pdrow in ts_ext_prediction_HWLWno.iterrows():
        ax1.text(pdrow.name,pdrow['values'],pdrow['HWLWno'].astype(int))
    ax1.set_ylim(-1.2,1.7)
    fig.savefig('prediction_HWLW_%im_%s_main'%(times_step_pred, current_station))

    if 0: #current_station=='HOEKVHLD':
        file_ext_vali = os.path.join(dir_testdata,'other','hoek_har.dia') #file is nonexistent
        ts_ext_vali = Timeseries.readts_dia(filename=file_ext_vali, station=current_station, block_ids='allstation')
        #ts_ext_vali = Timeseries.crop_timeseries(ts_ext_vali, [dt.datetime(1990,1,5),dt.datetime(1990,1,10)])
        ts_ext_vali = Timeseries.calc_HWLWnumbering(ts_ext=ts_ext_vali, station=current_station)
        fig, (ax1,ax2) = Timeseries.plot_timeseries(ts=ts_prediction_HWLWno, ts_ext=ts_ext_prediction_clean, ts_ext_validation=ts_ext_vali)

    Timeseries.write_tsdia_HWLW(ts_ext=ts_ext_prediction_main, station=current_station, vertref='NAP', filename='prediction_HWLW_%im_%s_main.dia'%(times_step_pred, current_station))
    Timeseries.write_tsdia_HWLW(ts_ext=ts_ext_prediction_clean, station=current_station, vertref='NAP', filename='prediction_HWLW_%im_%s_agger345.dia'%(times_step_pred, current_station))
    
    #ts_ext_prediction_HWLWno = Timeseries.calc_HWLWnumbering(ts_ext=ts_ext_prediction_HWLWno_pre, station=current_station)

exit_RWS(timer_start)

