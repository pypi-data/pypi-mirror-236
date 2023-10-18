#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:08:46 2023

@author: alexis
"""

from openwind.continuous import NetlistConnector

class Tonehole(NetlistConnector):
    """Models a complete tonehole as the combination of a junction,
    a chimney pipe and a radiation.

    Used for temporal simulation with locally implicit schemes"""

    def __init__(self, junct, pipe, rad,
                 label, scaling, convention='PH1'):
        super().__init__(label, scaling, convention)
        self.junct = junct
        self.pipe = pipe
        self.rad = rad

