# -*- coding: utf-8 -*-
'''  
Simple no-growth Agent Based Macroeconomic Model (in Python)
Copyright (C) 2018 Ritesh Kakade

'''


import numpy as np
from Household import Household
from CFirm import CFirm
from Bank import Bank

class World:
    
    def __init__(self, H, Fc, B, T):
        self.H = H
        self.Fc = Fc
        self.B = B
        self.T = T
        self.c_array = []
        self.f_array = []
        self.b_array = []
        self.c_data = np.zeros((T+2, H, 20))
        self.f_data = np.zeros((T+2, Fc, 20))
        self.b_data = np.zeros((T+2, B, 20))
        self.init_p_lvl= 0
        
        self.unemp_rate = np.zeros(T+2)
        self.S_avg = np.zeros(T+2)
        self.P_lvl = np.zeros(T+2)
        self.avg_prod = np.zeros(T+2)
        self.inflation = np.zeros(T+2)
        self.wage_lvl = np.zeros(T+2)
        self.wage_inflation = np.zeros(T+2)
        self.production = np.zeros(T+2)
        self.production_by_value = np.zeros(T+2)
        self.consumption = np.zeros(T+2)
        self.demand = np.zeros(T+2)
        self.hh_income = np.zeros(T+2)
        self.hh_savings = np.zeros(T+2)
        self.hh_consumption = np.zeros(T+2)
        
    def populate(self):
        Qty = []
        Y0 = np.random.uniform(low=50,high=100,size=self.H)
        for h in range(self.H):
            MPC = np.random.uniform(low=0.6,high=0.9)
            self.c_array.append(Household(Y0[h], MPC, h+1))
            self.c_data[:,h,0] = h+1
            self.c_data[0,h,1] = Y0[h]
            self.c_data[0,h,2] = MPC*Y0[h]
            self.c_data[0,h,5] = MPC*Y0[h]
            self.c_data[0,h,4] = MPC
            
        for f in range(self.Fc):
            self.f_array.append(CFirm(f+1, self.H//self.Fc, np.mean(Y0)))
            self.f_data[:,f,0] = f+1
            Qty.append(self.f_array[f].getDesiredQty())
        
        NB0 = np.random.uniform(low = 3000, high = 6000, size = self.B)
        aNB0 = np.mean(NB0)
        factor = self.H*9
        for b in range(self.B):
            self.b_array.append(Bank(NB0[b], b+1, aNB0, factor))
            self.b_data[:,b,0] = b+1

        
#    def createNetwork(self):
#        
        