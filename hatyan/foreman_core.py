# -*- coding: utf-8 -*-
"""
foreman.py contains all foreman definitions now embedded in hatyan. The dataset is derived from "M.G.G. Foreman (2004), Manual for Tidal Heights Analysis and Prediction, Institute of Ocean Sciences (Patricia Bay, Sidney B.C. Canada)"

hatyan is a Python program for tidal analysis and prediction, based on the FORTRAN version. 
Copyright (C) 2019-2021 Rijkswaterstaat.  Maintained by Deltares, contact: Jelmer Veenstra (jelmer.veenstra@deltares.nl). 
Source code available at: https://github.com/Deltares/hatyan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

#################################################
################# FILECONTENTS ##################
#################################################


def get_foreman_content():
    import pandas as pd
    import numpy as np
    import os
    
    file_path = os.path.realpath(__file__)
    foreman_file = os.path.join(os.path.dirname(file_path),'data_components_foreman.txt')
    content_pd = pd.read_csv(foreman_file, comment='#', names=[0], skip_blank_lines=False)
    content_pd[0] = content_pd[0].str.replace('-0.',' -0.',regex=False) #add spaces where needed
    content_pd[0] = content_pd[0].str.replace('LDA2','LABDA2',regex=False)
    content_pd[0] = content_pd[0].str.replace('Z0','A0',regex=False)
    splitlines = np.where(content_pd[0].isnull())[0]
    if len(splitlines) != 2:
        print( 'WARNING: foreman file has less or more than 2 blank lines, fix corrupted file and run again' )
    
    #foreman_freqs_harmonic_raw = content_pd.loc[:splitlines[0]-1,0] #derived with doodson table for harmonic components and shallowrelations
    #foreman_harmonic_head = content_pd.loc[splitlines[0]+1:splitlines[0]+2,0] #not used
    foreman_harmonic_raw = content_pd.loc[splitlines[0]+3:splitlines[1]-1,0]
    foreman_shallowrelations_raw = content_pd.loc[splitlines[1]+1:,0]

    return foreman_harmonic_raw, foreman_shallowrelations_raw


def get_foreman_doodson_nodal_harmonic(lat_deg=51.45):
    """
    Omzetten van het tweede deel van de foremantabel in een pandas DataFrame met harmonische (+satellite) componenten.

    Parameters
    ----------
    const_list : TYPE
        DESCRIPTION.
    lat_deg : TYPE, optional
         0 in degrees from equator (pos N, neg S). For R1 and R2, maar variatie heeft niet erg veel invloed op A en phi. The default is 51.45.

    Returns
    -------
    foreman_harmonic_doodson_all : TYPE
        DESCRIPTION.
    foreman_harmonic_nodal_all : TYPE
        DESCRIPTION.
    foreman_harmonic_doodson : TYPE
        DESCRIPTION.
    foreman_harmonic_nodal : TYPE
        DESCRIPTION.

    """
    import numpy as np
    import pandas as pd
    
    foreman_harmonic_raw, foreman_shallowrelations_raw = get_foreman_content()
    
    lat_rad = np.deg2rad(lat_deg)
    
    R1 = 0.36309*(1.-5.*np.sin(lat_rad)*np.sin(lat_rad))/np.sin(lat_rad) #-1 #for lat=50N
    R2 = 2.59808*np.sin(lat_rad) #2 #for lat=50N

    foreman_harmonic_new = foreman_harmonic_raw.str.split(' ', expand=True)
    foreman_harmonic_new = foreman_harmonic_new.set_index(0, drop=True)
    foreman_harmonic_new.index.name = None
    foreman_harmonic_list_new = list(set(foreman_harmonic_new.index.tolist()))

    #get all foreman harmonic doodson and nodal values
    foreman_harmonic_doodson_all_new = pd.DataFrame()
    foreman_harmonic_nodal_all_new = pd.DataFrame()
    for iC, const in enumerate(foreman_harmonic_list_new):
        foreman_harmonic_sel = foreman_harmonic_new.loc[[const]]
        
        row1 = foreman_harmonic_sel.iloc[0,:]
        row1 = row1[~row1.isnull()] #remove nans
        if not len(row1) == 8:
            raise Exception('ERROR: first row of component %s does not have length 8, so corrupt foreman file, line:\n%s'%(const,row1))
        foreman_harmonic_doodson_all_new[const] = row1
        
        if len(foreman_harmonic_sel.index) > 1:
            row_other_raw = foreman_harmonic_sel.iloc[1:,:]
            row_other = row_other_raw.stack(dropna=True)
            row_otherlen = len(row_other)
            if (row_otherlen%5)!=0:
                raise Exception('ERROR: length of list of nodal values should be a multiple of 5, corrupt foreman file for %s'%(const))
            row_other_reshape = row_other.values.reshape(row_otherlen//5,5)
            row_other_reshape_pd = pd.DataFrame(row_other_reshape,index=[const]*(row_otherlen//5))
            foreman_harmonic_nodal_all_new = foreman_harmonic_nodal_all_new.append(row_other_reshape_pd)
    foreman_doodson_harmonic = foreman_harmonic_doodson_all_new.astype(float).T
    
    bool_R1 = foreman_harmonic_nodal_all_new[4].str.contains('R1')
    bool_R2 = foreman_harmonic_nodal_all_new[4].str.contains('R2')
    foreman_harmonic_nodal_all_new.loc[bool_R1,4] = foreman_harmonic_nodal_all_new.loc[bool_R1,4].str.replace('R1','').astype(float)*R1
    foreman_harmonic_nodal_all_new.loc[bool_R2,4] = foreman_harmonic_nodal_all_new.loc[bool_R2,4].str.replace('R2','').astype(float)*R2
    foreman_nodal_harmonic = foreman_harmonic_nodal_all_new.astype(float)

    return foreman_doodson_harmonic, foreman_nodal_harmonic


def get_foreman_shallowrelations():
    """
    Omzetten van het derde deel van de foremantabel in een pandas DataFrame met shallow water relations.

    Returns
    -------
    foreman_shallowrelations : TYPE
        DESCRIPTION.

    """
    
    foreman_harmonic_raw, foreman_shallowrelations_raw = get_foreman_content()
    
    foreman_shallowrelations = foreman_shallowrelations_raw.str.split(' ', expand=True)
    foreman_shallowrelations = foreman_shallowrelations.set_index(0, drop=True)
    foreman_shallowrelations.index.name = None
    
    return foreman_shallowrelations


#################################################
#################### FREQ V0 ####################
#################################################

def get_foreman_v0freq_fromfromharmonicdood(dood_date=None, mode=None):
    """
    Zoekt de frequentie of v0 voor alle harmonische componenten, in geval van v0 op de gegeven datum (dood_date). Hiervoor zijn de harmonische doodson getallen
    (foreman_harmonic_doodson_all) nodig, afkomstig uit get_foreman_harmonic uit foreman.py 
    """
    
    import numpy as np
    import pandas as pd
    import datetime as dt
    
    from hatyan.hatyan_core import get_doodson_eqvals
    
    if dood_date is None: #in case of frequency
        dood_date = pd.DatetimeIndex([dt.datetime(1900,1,1)]) #dummy value
    foreman_doodson_harmonic, foreman_nodal_harmonic = get_foreman_doodson_nodal_harmonic()
    dood_T_rad, dood_S_rad, dood_H_rad, dood_P_rad, dood_N_rad, dood_P1_rad = get_doodson_eqvals(dood_date=dood_date, mode=mode)
    const_list = foreman_doodson_harmonic.index
    t_const_doodson_lun = np.concatenate([np.zeros((len(const_list),1)),foreman_doodson_harmonic.loc[:,:7].values],axis=1)
    omega1 = t_const_doodson_lun[:,1:2]
    corr_array = np.concatenate([omega1,np.zeros((len(const_list),1)),-omega1,omega1,np.zeros((len(const_list),4))],axis=1)
    t_const_doodson_sol = t_const_doodson_lun+corr_array
    t_const_doodson_sol[:,1] = 0
    if mode=='freq':
        dood_rad_array = np.stack([dood_T_rad,np.zeros((dood_T_rad.shape)),dood_S_rad,dood_H_rad,dood_P_rad,np.zeros((dood_N_rad.shape)),dood_P1_rad,np.zeros((dood_T_rad.shape))])
        t_const_freq_dood = np.dot(t_const_doodson_sol,dood_rad_array)/(2*np.pi)
        t_const_freqv0_dood_pd = pd.DataFrame({'freq':t_const_freq_dood[:,0]},index=const_list)
        freqv0_dood_pd = t_const_freqv0_dood_pd
    else:
        dood_rad_array = np.stack([dood_T_rad,np.zeros((dood_T_rad.shape)),dood_S_rad,dood_H_rad,dood_P_rad,dood_N_rad,dood_P1_rad,np.zeros((dood_T_rad.shape))+2*np.pi])
        v_0i_rad = np.dot(t_const_doodson_sol,dood_rad_array)
        v_0i_rad_pd = pd.DataFrame(v_0i_rad,index=const_list)
        freqv0_dood_pd = v_0i_rad_pd
    
    return freqv0_dood_pd


def get_foreman_v0_freq(const_list, dood_date):
    """
    Zoekt voor iedere component uit de lijst de v op basis van harmonische doodson getallen en de frequentie rechtstreeks uit de foreman tabel.
    Shallow water componenten worden afgeleid met de relaties beschreven in de foreman tabel.
    """
    import numpy as np
    import pandas as pd
    
    foreman_freqs = get_foreman_v0freq_fromfromharmonicdood(dood_date=None, mode='freq') #list with only harmonic components with more precision than file
    v_0i_rad_harmonic_pd = get_foreman_v0freq_fromfromharmonicdood(dood_date=dood_date, mode=None)
    
    foreman_shallowrelations = get_foreman_shallowrelations()
    foreman_harmonic_list = v_0i_rad_harmonic_pd.index.tolist()
    foreman_shallowrelations_list = foreman_shallowrelations.index.tolist()
    
    v_0i_rad = np.zeros((len(const_list),len(dood_date)))
    t_const_freq = np.zeros((len(const_list)))
    
    #v and freq for harmonic and shallow constituents
    for iC,const in enumerate(const_list):
        if const in foreman_harmonic_list:
            v_0i_rad[iC,:] = v_0i_rad_harmonic_pd.loc[const]
            t_const_freq[iC] = foreman_freqs.loc[const,'freq']
        elif const in foreman_shallowrelations_list: #or is not in foreman_harmonic_doodson_all_list
            v_0i_rad_temp = 0
            t_const_freq_temp = 0
            foreman_shallow_const = foreman_shallowrelations.loc[const].tolist()
            num_dependencies = int(foreman_shallow_const[0])
            for iD in range(num_dependencies):
                id_factor = iD*2+1
                id_constname = iD*2+2
                harm_factor = float(foreman_shallow_const[id_factor])
                harm_const = foreman_shallow_const[id_constname]
                v_dependency = v_0i_rad_harmonic_pd.loc[harm_const].values
                v_0i_rad_temp = v_0i_rad_temp + harm_factor*v_dependency
                
                freq_dependency = foreman_freqs.loc[harm_const,'freq'] #should be dependent on harmonic doodson numbers (make foreman_freqs_dood_all variable in foreman.py, in freq or harmonic definition)
                t_const_freq_temp = t_const_freq_temp + harm_factor*freq_dependency
            v_0i_rad[iC,:] = v_0i_rad_temp
            t_const_freq[iC] = t_const_freq_temp
        else:
            raise Exception('ERROR: constituent %s is not in foreman_harmonic_doodson_all_list and foreman_shallow_all_list, this is invalid.'%(const))
    v_0i_rad_pd = pd.DataFrame(v_0i_rad,index=const_list)
    t_const_freq_pd = pd.DataFrame({'freq':t_const_freq},index=const_list)
    
    return v_0i_rad_pd, t_const_freq_pd


#################################################
################# NODALFACTORS ##################
#################################################
def get_foreman_nodalfactors_fromharmonic_oneconst(foreman_harmonic_nodal_const, dood_date):
    import numpy as np
        
    from hatyan.hatyan_core import get_doodson_eqvals
    dood_T_rad, dood_S_rad, dood_H_rad, dood_P_rad, dood_N_rad, dood_P1_rad = get_doodson_eqvals(dood_date)
    
    fore_delta_jk_rad_all = np.dot(foreman_harmonic_nodal_const.loc[:,0:2],np.stack([dood_P_rad, dood_N_rad, dood_P1_rad]))
    fore_alpha_jk_all = foreman_harmonic_nodal_const.loc[:,3:3].values * 2*np.pi #phase correction satellite. 0.5=90 voor M2 en N2, 0=0 voor S2
    fore_r_jk_all = foreman_harmonic_nodal_const.loc[:,4:4].values #amplitude ratio for satellite. 0.0373 voor M2 en N2, 0.0022 voor S2
    fore_A_jk = 1
    fore_fj_left_all = fore_A_jk * fore_r_jk_all * np.cos(fore_delta_jk_rad_all + fore_alpha_jk_all) #should be sum for n sattelites
    fore_fj_right_all = fore_A_jk * fore_r_jk_all * np.sin(fore_delta_jk_rad_all + fore_alpha_jk_all) #should be sum for n sattelites
    fore_fj_left = fore_fj_left_all.sum(axis=0)
    fore_fj_right = fore_fj_right_all.sum(axis=0)
    
    f_i_FOR = ( (1+ fore_fj_left)**2 + (fore_fj_right)**2)**(1/2.)
    u_i_rad_FOR = -np.arctan2(fore_fj_right,1+fore_fj_left) #added minus to get sign comparable to hatyan

    return f_i_FOR, u_i_rad_FOR


def get_foreman_nodalfactors(const_list, dood_date):
    """
    Zoekt voor iedere component uit de lijst de u en f (nodal factors) op basis van satellite doodson getallen uit de foreman tabel.
    Shallow water componenten worden afgeleid met de relaties beschreven in de foreman tabel.
    """
    import numpy as np
    import pandas as pd
    
    foreman_shallowrelations = get_foreman_shallowrelations()
    foreman_doodson_harmonic, foreman_nodal_harmonic = get_foreman_doodson_nodal_harmonic()
    
    foreman_harmonic_doodson_all_list = foreman_doodson_harmonic.index.tolist()
    foreman_harmonic_nodal_all_list = foreman_nodal_harmonic.index.unique().tolist()
    foreman_shallow_all_list = foreman_shallowrelations.index.tolist()
    
    f_i_FOR = np.ones((len(const_list),len(dood_date)))
    u_i_rad_FOR = np.zeros((len(const_list),len(dood_date)))
    
    #f and u for harmonic constituents
    for iC,const in enumerate(const_list):
        if const in foreman_harmonic_doodson_all_list:
            if const in foreman_harmonic_nodal_all_list:
                foreman_harmonic_nodal_const = foreman_nodal_harmonic.loc[[const]]
                f_i_FOR[iC,:], u_i_rad_FOR[iC,:] = get_foreman_nodalfactors_fromharmonic_oneconst(foreman_harmonic_nodal_const, dood_date)
        elif const in foreman_shallow_all_list: # component has satellites based on shallow water relations
            f_i_FOR_temp = 1.0
            u_i_rad_FOR_temp = 0.0
            foreman_shallow_const = foreman_shallowrelations.loc[const].tolist()
            num_dependencies = int(foreman_shallow_const[0])
            for iD in range(num_dependencies):
                id_factor = iD*2+1
                id_constname = iD*2+2
                harm_factor = float(foreman_shallow_const[id_factor])
                harm_const = foreman_shallow_const[id_constname]
                if harm_const in foreman_harmonic_nodal_all_list:
                    foreman_harmonic_nodal_const = foreman_nodal_harmonic.loc[[harm_const]]
                    f_i_dependency, u_i_rad_dependency = get_foreman_nodalfactors_fromharmonic_oneconst(foreman_harmonic_nodal_const, dood_date)#foreman_harmonic_nodal_all[foreman_harmonic_nodal_all_list.index()][iS]
                    f_i_FOR_temp = f_i_FOR_temp * f_i_dependency**abs(harm_factor)
                    u_i_rad_FOR_temp = u_i_rad_FOR_temp + harm_factor*u_i_rad_dependency
                else:
                    raise Exception('ERROR: harmonic component %s for shallow water component %s is not available in the harmonic nodal factors (foreman_nodal_harmonic)'%(harm_const,const))
            f_i_FOR[iC,:] = f_i_FOR_temp
            u_i_rad_FOR[iC,:] = u_i_rad_FOR_temp
        else:
            raise Exception('ERROR: constituent %s is not in foreman_harmonic_doodson_all_list and foreman_shallow_all_list, this is invalid.'%(const))
    
    f_i_FOR_pd = pd.DataFrame(f_i_FOR, index=const_list)
    u_i_rad_FOR_pd = pd.DataFrame(u_i_rad_FOR, index=const_list)
    
    return f_i_FOR_pd, u_i_rad_FOR_pd


