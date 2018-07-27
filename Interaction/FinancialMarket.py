'''  
Simple no-growth Agent Based Macroeconomic Model (in Python)
Copyright (C) 2018 Ritesh Kakade

'''


import numpy as np

def payDividends(myWorld, t, H, Fc, B):
    f_array = myWorld.f_array
    c_array = myWorld.c_array
    n=0
    for f in f_array:
        if f is not None:        
            divs = 0
            f.calcProfits()
            if f.getProfits() > 0:
                f.setDividends()
                divs = f.getDividends()
                #print("Firm: ",f.getId(),divs)
            else:
                n=n+1
                #print("No dividends!!")
            
            if divs > 0:
                for c in c_array:
                    c.setDividends(divs/H)
                    c.setDivFlag()
        
    myWorld.f_array = f_array
    myWorld.c_array = c_array
    print("Out of %d Firms, %d reported profits this period"%(Fc,Fc-n))

def checkForBankrupcy(myWorld, t):
    f_array = myWorld.f_array
    c_array = myWorld.c_array
    f_data = myWorld.f_data
    for f in f_array:
        if f is not None:    
            if f.getNetWorth() < 0:
                f.updateBankrupcyPeriod()
            else:
                f.resetBankrupcyPeriod()
            
            if f.getBankrupcyPeriod() > 4:
                fid= f.getId()
                h_emp = f.getEmployedHousehold()
                print("Firm %d has gone BANKRUPT!!!"%(fid))
                f_array[fid-1] = None
                for i in h_emp:
                    c_array[i-1].updatePrevEmployer(fid)
                    c_array[i-1].updateEmploymentStatus()
                    c_array[i-1].setEmployedFirmId(0)
                    c_array[i-1].setUnempBenefits(0.8*c_array[i-1].getWage())
                    c_array[i-1].setWage(0)
                    c_array[i-1].resetEdays()
                    #print("Household %d layed off from firm %d"%(c_array[i-1].getId(),fid))
                f_data[t+1,fid-1,:] = np.zeros((1,1,20))
    
    myWorld.f_array = f_array
    myWorld.c_array = c_array
    myWorld.f_data = f_data