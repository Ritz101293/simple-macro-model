# -*- coding: utf-8 -*-
'''  
Simple no-growth Agent Based Macroeconomic Model (in Python)
Copyright (C) 2018 Ritesh Kakade

'''

import matplotlib.pyplot as plt
#import matplotlib
import numpy as np


def plotAndSaveGraphs(myWorld, t, T):
    if t is None:    
        # Philips curve
        plt.clf()
        plt.scatter(myWorld.unemp_rate[:-2], myWorld.wage_inflation[:-2])
        plt.xlabel("Unemployment Rate")
        plt.ylabel("Wage Inflation")
        plt.savefig('philips.png')
        
        # Log output
        plt.clf()
        plt.plot(np.log(myWorld.production[:-2]))
        plt.xlabel("Time")
        plt.ylabel("Output")
        plt.savefig("LogOutput.png")
        
        #Unemployment growth vs Output growth
        plt.clf()
        Q_growth = (myWorld.production[1:-1] - myWorld.production[:-2])*100/myWorld.production[:-2]
        plt.plot(Q_growth[:-1])
        plt.xlabel("Time")
        plt.ylabel("Output Growth")
        plt.savefig("OutputGrowth.png")
        
        # Unemployment
        plt.clf()
        plt.plot(myWorld.unemp_rate[:-2])
        plt.xlabel("Time")
        plt.ylabel("Unemployment rate")
        plt.savefig("unempRate.png")
        
        # Firm size distribution
        plt.clf()
        plt.hist(myWorld.f_data[T-1,:,9])
        plt.xlabel("Firm Size ddistribution by labor")
        plt.savefig("FirmSizeDistAt"+str(T-1))
        
        # Excess Demand Over Time
        plt.clf()
        plt.plot((1-myWorld.unemp_rate[:-2])*myWorld.H)
        plt.xlabel("Household EMployed vs Time")
        plt.savefig("EmployedHousehold.png")
        
        #Household
        plt.clf()
        plt.plot(np.log(myWorld.hh_income[:-2]), label="Income(In log)")
        plt.plot(np.log(myWorld.hh_savings[:-2]), label="Savings(In log)")
        plt.plot(np.log(myWorld.hh_consumption[:-2]), label="Consumption(In log)")
        plt.legend()
        plt.ylabel("Income/Savings/Consumption")
        plt.savefig("Households.png")
        
    else:
        plt.clf()
        plt.hist(myWorld.f_data[t,:,9])
        plt.xlabel("Firm Size ddistribution by labor")
        plt.savefig("FirmSizeDistAt"+str(t))