#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 00:31:14 2022

@author: valentinsauvage
"""
#%% 
def density(temperature, pressure):
    """
    ========== DESCRIPTION ==========
    
    This function return the density of pure helium 4

    ========== VALIDITY ==========
    
    <temperature> : [273.15->1800]
    <pressure> : [0->100e5]

    ========== FROM ==========
    
    KPetersen, H. (1970). The properties of helium: Density, specific heats, 
    viscosity, and thermal conductivity at pressures from 1 to 100 bar and 
    from room temperature to about 1800 K. Risø National Laboratory. Denmark. 
    Forskningscenter Risoe. Risoe-R No. 224

    ========== INPUT ==========

    <temperature>
        -- float --
        The temperature of Helium 4
        [K]
        
    <pressure>
        -- float --
        The pressure of Helium 4
        [Pa]
        
    ========== OUTPUT ==========
    
    <density>
        -- float --
        The density of Helium 4
        [kg].[m]**3
    
    ========== STATUS ==========     
    
    Status : Checked

    """

    ################## CONDITIONS #############################################

    assert 1800 >= temperature >= 273.15, 'The function Helium4.density is not defined for T = ' + str(temperature) + ' K'
    assert 100e5 >= pressure >= 0, 'The function Helium4.density is not defined for P = ' + str(temperature) + ' Pa'

    ################## INITIALISATION #########################################

    # convert [Pa] to [Bar]
    pressure = pressure * 1e-5

    ################## FUNCTION ###############################################

    return 48.18 * pressure / temperature * (1 + 0.4446 * pressure / (temperature ** 1.2)) ** (-1)

#%%
def dynamic_viscosity(temperature):
    """
    ========== DESCRIPTION ==========
    
    This function return the dynamic viscosity of pure helium 4

    ========== VALIDITY ==========
    
    <temperature> : [273.15->1800]

    ========== FROM ==========
    
    KPetersen, H. (1970). The properties of helium: Density, specific heats, 
    viscosity, and thermal conductivity at pressures from 1 to 100 bar and 
    from room temperature to about 1800 K. Risø National Laboratory. Denmark. 
    Forskningscenter Risoe. Risoe-R No. 224

    ========== INPUT ==========

    <temperature>
        -- float --
        The temperature of Helium 4
        [K]
        
    ========== OUTPUT ==========
    
    <dynamic_viscosity>
        -- float --
        The dynamic viscosity of Helium 4
        [Pa].[s]
    
    ========== STATUS ==========     
    
    Status : Checked

    """

    ################## CONDITIONS #############################################

    assert 1800 >= temperature >= 273.15, 'The function Helium4.dynamic_viscosity is not defined for T = ' + str(temperature) + ' K'

    ################## FUNCTION ###############################################

    return 3.674e-7 * temperature ** 0.7

