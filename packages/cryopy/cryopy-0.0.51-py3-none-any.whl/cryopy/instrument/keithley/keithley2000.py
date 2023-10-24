# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 23:30:35 2022

@author: Administrateur
"""


def query_current(address):
    """
    ========== DESCRIPTION ==========

    This function get the value of the DCI from Keithley 2000

    ========== FROM ==========

    Manual of Keithley 2000

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument (e.g. 'GPIB0::15::INSTR')

    ========== OUTPUT ==========

    <current>
        -- float --
        The measured current
        [A]

    ========== STATUS ==========

    Status : Checked


    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    rm = pyvisa.ResourceManager()
    instru = rm.open_resource(address)
    instru.write(':CONF:CURR:DC')

    ################## FUNCTION ###############################################

    answer = instru.query(':READ?')
    answer = float(answer)

    return answer
