# -*- coding: utf-8 -*-
'''  
Simple no-growth Agent Based Macroeconomic Model (in Python)
Copyright (C) 2018 Ritesh Kakade

'''

import numpy as np
#import matplotlib.pyplot
    
def updateData(myWorld, t, H, Fc, B):
    f_array = myWorld.f_array
    c_array = myWorld.c_array
    b_array = myWorld.b_array
    f_data = myWorld.f_data
    c_data = myWorld.c_data
    b_data = myWorld.b_data
    n=0
    for c in c_array:
        if c.getEmploymentStatus():
            c.incrementEdays()
        else:
            c.incrementUdays()
        #print(c_array[h].getId(),c_array[h].getIncome(), c_array[h].getActualCons(), c_array[h].getSavings())
        c_data[t, c.getId()-1, 2] = c.getActualCons()
        if c.getActualCons() > 0:
            n=n+1
        c_data[t, c.getId()-1, 3] = c.getSavings()
        if t !=0:
            c_data[t, c.getId()-1, 4] = c.getMPC() 
        c_data[t, c.getId()-1, 5] = c.getDesiredCons()
        c_data[t, c.getId()-1, 6] = c.getWage()         
        c_data[t, c.getId()-1, 7] = c.getUnempBenefits()  # Code for the reservation Wages
        c_data[t, c.getId()-1, 8] = c.getPrevEmployer()
        c_data[t, c.getId()-1, 9] = c.getEmployedFirmId()
        c_data[t, c.getId()-1, 10] = 1 if c.getEmploymentStatus() else 0
        c_data[t, c.getId()-1, 11] = c.getPrevCFirm()
        c_data[t, c.getId()-1, 12] = c.getDividends()
        c_data[t, c.getId()-1, 13] = c.getDaysEmployed()
        c_data[t, c.getId()-1, 14] = c.getDaysUnemployed()
        
        c.updateIncome()
        c_data[t+1, c.getId()-1, 1] = c.getIncome()
        
        c.resetSomeVariables()
    
    print("Out of total %d Household, %d did consume"%(H,n))
    
    for f in f_array:
        if f is not None:
            f.setMinPrice()
            f_data[t,f.getId()-1,1] = f.getDesiredQty()
            f_data[t,f.getId()-1,2] = f.getActualQty()
            f_data[t,f.getId()-1,3] = f.getQtySold()
            f_data[t,f.getId()-1,4] = f.getQtyRemaining()
            f_data[t,f.getId()-1,5] = f.getPrice()
            f_data[t,f.getId()-1,6] = f.getProductivity()
            f_data[t,f.getId()-1,7] = f.getRequiredLabor()
            f_data[t,f.getId()-1,8] = f.getNumberOfExpiredContract()
            f_data[t,f.getId()-1,9] = f.getTotalEmployees()
            f_data[t,f.getId()-1,10] = f.getWage()
            f_data[t,f.getId()-1,13] = f.getRevenues()
            f_data[t,f.getId()-1,18] = f.getNetWorth()
            #print(len(f_data[:,0,0]))
            f.calcVacRate()
            f_data[t, f.getId()-1,19] = f.getVacRate()
            f_data[t,f.getId()-1,14] = f.getLoanToBePaid()            
            f_data[t,f.getId()-1,11] = f.getDesiredWageBill()
            f_data[t,f.getId()-1,12] = f.getActualWageBill()            
            f.updateNetWorth()
            f_data[t,f.getId()-1,15] = f.getProfits()
            f_data[t,f.getId()-1,16] = f.getDividends()
            f_data[t,f.getId()-1,17] = f.getRetainedEarnings()
            f_data[t+1,f.getId()-1,18] = f.getNetWorth()
            #print(f.getRevenues(),f.getProfits(),f.getNetWorth())
            
            f.resetSomeVariables()
    
    for b in b_array:
        b_data[t, b.getId()-1, 1] = b.getEquity()
        b_data[t, b.getId()-1, 2] = b.getCreditSupply()
        b_data[t, b.getId()-1, 3] = b.getActualCreditSupplied()
        b_data[t, b.getId()-1, 4] = b.getRemainingCredit()
        #print(np.array(b.getRatesDisbursed())*np.array(b.getRatesDisbursed()))
        b_data[t, b.getId()-1, 5] = np.sum(np.array(b.getCreditDisbursed())*np.array(b.getRatesDisbursed()))/np.sum(np.array(b.getCreditDisbursed())) if len(b.getCreditDisbursed()) > 0 else 0
        b_data[t, b.getId()-1, 7] = b.getLoanPaid()
        #b_data[t, b.getId()-1, 6] = b_data[t, b.getId()-1, 5] - b_data[t, b.getId()-1, 7]
        b.updateEquity()
        b_data[t+1,b.getId()-1,1] = b.getEquity()
        
        
        b.resetSomeVariables()
        
        
    myWorld.f_array = f_array
    myWorld.c_array = c_array
    myWorld.b_array = b_array
    myWorld.f_data = f_data
    myWorld.c_data = c_data
    myWorld.b_data = b_data


def calcStatistics(myWorld, t, H, Fc, B):
    f_data = myWorld.f_data
    c_data = myWorld.c_data
    b_data = myWorld.b_data
    f_d = f_data[t,:,:]
    c_d = c_data[t,:,:]
    b_d = b_data[t,:,:]
    #print(np.sum(c_d[:,10]), H)
    plvl = 0
    for f in range(Fc):
        plvl = plvl + np.mean(f_data[:t+1,f-1, 5])*np.sum(f_data[:t+1,f-1,3])
    
    plvl = plvl/np.sum(f_data[:t+1,:,3])
    
    myWorld.S_avg[t] = np.mean(c_d[:,3])
    myWorld.unemp_rate[t] = 1 - (np.sum(c_d[:,10])/H)
    myWorld.P_lvl[t] = plvl
    print("total produced:",np.sum(f_d[:,2]*f_d[:,5]), "total consumed:", np.sum(c_d[:,2]))
    myWorld.avg_prod[t] = np.sum(f_d[:,6]*f_d[:,9])/np.sum(f_d[:,9])

    myWorld.inflation[t] = myWorld.P_lvl[t]-myWorld.P_lvl[t-1] if t!=0 else 0
    myWorld.inflation[t] = myWorld.inflation[t]*100
    
    myWorld.wage_lvl[t] = np.sum(f_d[:,10]*f_d[:,9])/np.sum(f_d[:,9])
    myWorld.wage_inflation[t] = (myWorld.wage_lvl[t]-myWorld.wage_lvl[t-1])/np.sum(myWorld.wage_lvl[t-1]) if t!=0 else 0
    myWorld.wage_inflation[t] = myWorld.wage_inflation[t]*100
    
    myWorld.production[t] = np.sum(f_d[:,2])
    myWorld.production_by_value[t] = np.sum(f_d[:,2]*f_d[:,5])
    myWorld.consumption[t] = np.sum(c_d[:,2])
    myWorld.demand[t] = np.sum(c_d[:,5])
    myWorld.hh_income[t] = np.sum(c_d[:,1])
    myWorld.hh_savings[t] = np.sum(c_d[:3])
    myWorld.hh_consumption[t] = np.sum(c_d[:,2])
    print("total demand:", myWorld.demand[t], "avg Price and Wage lvl:",myWorld.P_lvl[t],myWorld.wage_lvl[t])
    

    
    