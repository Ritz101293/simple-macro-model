# -*- coding: utf-8 -*-
'''  
Simple no-growth Agent Based Macroeconomic Model (in Python)
Copyright (C) 2018 Ritesh Kakade

'''


import numpy as np
import math as m
import utils as utils


def searchAndMatchCredit(myWorld, t, Fc, B):
    f_array = myWorld.f_array
    c_array = myWorld.c_array
    b_array = myWorld.b_array    

    for f in f_array:
        if f is not None:
            H = f.H       
            break
    
    b_ids = np.array(range(B)) + 1 # b_d[:,0]
#    n_b = len(b_ids)
    f_ids = np.array(range(Fc)) + 1 # f_d[:,0]
#    n_f = len(f_ids)
    f_cr = []
    # Firms apply for Credit
    np.random.shuffle(f_ids)
    print("")
    print("Credit MArket OPENS!!!!")
    print("")
    for f in f_ids:
        f= int(f)
        if f_array[f-1] is not None:
            if f_array[f-1].loanRequired():
                f_cr.append(f)
                b_apply = np.random.choice(b_ids, H, replace=False)
                #print("Banks:", b_apply)
    
                f_array[f-1].setCreditAppl(b_apply)
                for bb in b_apply:
                    bb = int(bb)
                    b_array[bb-1].updateFirmsAppl(f)
                
    if len(f_cr) > 0:
        #print("Firms needs Credit!")
        # Banks decides on the interest rates
        np.random.shuffle(b_ids)
        for b in b_ids:
            b = int(b)
            b_obj = b_array[b-1]
            b_obj.setCreditSupply()
            b_obj.setActualCreditSupplied(0)
            b_obj.setRemainingCredit()
            print("Bank %d has a credit supply of %f" %(b, b_obj.getCreditSupply()))
            #b_d[b-1, 3] = b_obj.getCreditSupply()
            #b_d[b-1, 6] = b_obj.getCreditSupply()
            f_appl = b_obj.getFirmsAppl()
            for f_a in f_appl:
                if f_a is not None:
                    lv = f_array[f_a-1].getLeverageRatio()
                    b_obj.updateIntRates(b_obj.calcIntRate(lv))
        
        # Firms chose the bank having lowest int rate and go to second bank if its credit req are not satisfied
        for f_c in f_cr:
            f_c = int(f_c)
            r = []
            b_a = f_array[f_c-1].getCreditAppl()
            b_a_np = np.array(b_a)
            for b in b_a:
                b = int(b)
                f_b = b_array[b-1].getFirmsAppl()
                r_b = b_array[b-1].getIntRates()
                r.append(r_b[f_b.index(f_c)])
            r_np = np.array(r)
            Cr_req = f_array[f_c-1].getLoanAmount()
            cr = 0
            rem = Cr_req - cr
            #print(b_a_np)
            #b_a = list(b_a)
            for bk in b_a_np:
                i = np.argmin(r_np)
                C_s = 0
                C_r = b_array[int(b_a[i])-1].getRemainingCredit()
                if C_r >= rem:
                    C_s = C_s + rem
                    cr = cr + rem
                    rem = Cr_req -cr
                    C_r = C_r - C_s
                    f_array[f_c-1].addBanksAndRates(int(b_a[i]), cr, r_np[i])
                    b_array[int(b_a[i])-1].addFirmsRatesCredits(f_c, cr, r_np[i])
                else:
                    cr  = cr + C_r
                    rem = Cr_req - cr
                    C_s = C_s + C_r
                    C_r = 0
                    f_array[f_c-1].addBanksAndRates(int(b_a[i]), cr, r_np[i])
                    b_array[int(b_a[i])-1].addFirmsRatesCredits(f_c, cr, r_np[i])
                    
                b_array[int(b_a[i])-1].setActualCreditSupplied(C_s)
                b_array[int(b_a[i])-1].setRemainingCredit()
                
#                print("Firm %d got loan of %f at Bank %d at %f rate of interest with total demand of %f"
#                          %(f_c,cr,int(b_a[i]),r_np[i], Cr_req))
                
                
                #del b_a[i]
                b_a = np.delete(b_a, i)
                r_np = np.delete(r_np, i)
                if rem == 0:
                    break
                
                if len(b_a) == 0:
                    break
            f_array[f_c-1].setLoanToBePaid()
            print(f_array[f_c-1].getLoanToBePaid())
    else:
        print("No credit requirement in the economy")
    print("")            
    print("Credit Market CLOSED!!!!")
    print("")
    hh_layed_off = []
    updateProductionDecisions(f_array, hh_layed_off)
    updateHouseholdEmpStatus(hh_layed_off, c_array)
    
    myWorld.f_array = f_array
    myWorld.c_array = c_array
    myWorld.b_array = b_array
                    
                
             
def updateProductionDecisions(f_array, hh_layed_off):
    print("")
    print("Firms updating hiring decision.....")
    for f in f_array:
        if f is not None:
            if f.getLoanAmount() > 0:
                unsatisfied_cr = f.getLoanAmount() - sum(f.getCredits())
                Lb = int(m.floor(unsatisfied_cr/f.getWage()))
                if Lb > 0:
                    h = f.getEmployedHousehold()
                    if len(h) >= Lb:
                        #print(h, Lb)
                        h_lo = np.random.choice(h, Lb, replace = False)
                        h = [x for x in h if x not in h_lo]
                    else:
                        h_lo = h
                        h = []
                    f.updateEmployedHousehold(h)
                    f.updateTotalEmployees()
                    hh_layed_off = utils.appendArrays(hh_layed_off, h_lo)
    print("Firms succesfully updated hiring decisions")
    print("")
    print("")
                
def updateHouseholdEmpStatus(hh_layed_off, c_array):
    for h in hh_layed_off:
        c_array[h-1].updatePrevEmployer(c_array[h-1].getEmployedFirmId())
        c_array[h-1].setEmployedFirmId(0)
        c_array[h-1].updateEmploymentStatus()
 

def settleDebts(myWorld, t, Fc, B):
    f_array = myWorld.f_array
    b_array = myWorld.b_array
    print("Firms settling DEBTS......")
    for f in f_array:
        if f is not None:    
            f.payLoan()
            banks = f.getBanks()
            credit = f.getCredits()
            rates = f.getRates()
            #print(banks, credit, rates)
            for i in range(len(banks)):
                b_array[int(banks[i])-1].setLoanPaid(credit[i]*(rates[i]+1))
    
    
    myWorld.f_array = f_array
    myWorld.b_array = b_array
    
    print("DEBTS settled!!!!!!!")
    print("")
                
       
        
         
            