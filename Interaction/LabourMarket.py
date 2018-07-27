# -*- coding: utf-8 -*-

import numpy as np
import utils as utils

def searchAndMatchLabor(myWorld, t, H, Fc):
    hired = 0
    f_data = myWorld.f_data
    f_array = myWorld.f_array
    c_array = myWorld.c_array

    c_ids = np.array(range(H)) + 1 # c_d[:,0]
    #n_f = len(f_d[:,0])
    for f in f_array:
        if f is not None:    
            theta = f.theta
            h_zeta = f.h_zeta
            break

    M = c_array[0].M
    f_empl = [] # List of Firms who are going to post vacancies
    
    # Here will come function to get aggregate statistics about the economy.
    prev_avg_p = myWorld.P_lvl[t-1]
    print("")
    print("Labor Market OPENS!")
    #print("")
    # Firms posting Vacancies and Wages
    for i in range(Fc):
        f = f_array[i]
        if f == None:
            continue
        else:
            if t==0:
                f.setRequiredLabor(True)
            else:
                f.decideProduction(f_data[t-1,f.getId()-1, 4], prev_avg_p,
                                          f_data[t-1,f.getId()-1, 5],f_data[t-1,f.getId()-1, 3],
                                          f_data[t-1,f.getId()-1, 1])
                f.setRequiredLabor(False)
            if f.getTotalEmployees() >= 0:
                c_f = f.getEmployedHousehold()
                v = getVacancies(f, c_f, c_array, theta)
                #print(v, f.getDesiredQty())
                if v > 0:
                    f_empl.append(f.getId())
            zeta = np.random.uniform(low=0,high=h_zeta)
            if f_data[t-1,f.getId()-1,3] == 0:
                f.setWage(2*zeta)
            else:
                f.setWage(zeta)
            f.setDesiredWageBill()
            #print(f.getWage())
   #  print("Firms posted Vacancies and Wage offers")
    
    if len(f_empl) > 0:
        # Unemployed Households applying for the vacancies
        c_ids = [x for x in c_ids if not c_array[int(x)-1].getEmploymentStatus()] # Household who are unemployed
        print("%d Households are participating in the labor market"%len(c_ids))
        np.random.shuffle(c_ids)
        for k in c_ids:
            k = int(k)
            c = c_array[k-1]
            appl = None # To store firms applied by this household
            prev_emp = c.getPrevEmployer() # Households always apply to previous employer where the contact has expired
            # print(prev_emp)
            f_empl_c = [x for x in f_empl if x != prev_emp]
            if len(f_empl_c) > M - 1:
                appl = np.random.choice(f_empl_c, M-1, replace = False)
                np.append(appl, prev_emp)
            else:
                appl = f_empl_c
                np.append(appl, prev_emp)
            # print(k)
            c.setAppliedFirms(appl)
            # print(c.getFirmsApplied())
            for a in appl:
                f_array[a-1].updateApplicant(c.getId())
        # print("Houshold applied for the vacancies")
        
        # Firms offer Jobs to randomly selected applicants
        for f in f_empl:
            vac = f_array[f-1].calcVacancies()
            applicants = f_array[f-1].getJobApplicants()
            n_applicants = len(applicants)
            #print("applicants:", n_applicants, vac)
            if vac >= n_applicants:
                f_array[f-1].updateJobOffered(utils.appendArrays(f_array[f-1].getJobOffered(),
                       applicants))
                updateHouseholdJobOffers(f, applicants, c_array)
                # print("labor Shortage!!!")
            else:
                applicants = np.random.choice(applicants, vac, replace=False)
                #print(applicants)
                f_array[f-1].updateJobOffered(utils.appendArrays(f_array[f-1].getJobOffered(),
                       applicants))
                updateHouseholdJobOffers(f, applicants, c_array)
                # print("Labor Excess!!")
            #print("job offered:", f_array[f-1].getJobOffered(), vac)
        # print("Firms offer the Jobs to the household")
        
        # Household accepts if job offered is of highest wage
        for l in c_ids:
            l = int(l)
            c = c_array[l-1]
            f_applied_ids = [x-1 for x in c.getFirmsApplied()]
            f_job_offers = [x-1 for x in c.getJobOffers()]
            f_e = np.empty(len(f_applied_ids))
            offer_wage = []
            #print(l,f_applied_ids, f_job_offers)
            if len(f_applied_ids) != 0:
                ind = 0
                for ii in f_applied_ids:
                    f_e[ind] = f_array[ii].getWage()
                    ind += 1
                for of in f_job_offers:
                    offer_wage.append(np.around(f_array[of].getWage(),decimals=2))
                #print(f_e)
                w_max = max(f_e)
                #print(f_e,offer_wage)
                if w_max in offer_wage:
                    #print("hired!!!")
                    f_max_id = f_job_offers[offer_wage.index(w_max)]
                    c.updateEmploymentStatus()
                    c.setEmployedFirmId(f_max_id+1)
                    c.setWage(w_max)
                    hired = hired + 1
                    f = f_array[f_max_id]
                    f.employHousehold(l)
                    f.updateTotalEmployees()
                elif t > 0 and len(offer_wage) > 0:
                    mm = max(np.array(offer_wage))
                    if mm > myWorld.wage_lvl[t-1]:
                        f_max_id = f_job_offers[offer_wage.index(mm)]
                        c.updateEmploymentStatus()
                        c.setEmployedFirmId(f_max_id+1)
                        c.setWage(w_max)
                        hired = hired + 1
                        f = f_array[f_max_id]
                        f.employHousehold(l)
                        f.updateTotalEmployees()
                    #print("Household no: %d has got employed in Firm no: %d at wage %f"% (l, f_max_id+1, w_max))
    else:
        print("No Labor Requirements in the economy")
            
    print("")   
    print("Labor Market CLOSED!!!! with %d household hired!!"%(hired))
    print("")
    for fa in f_array:
        if fa is not None:
            fa.setActualWageBill()
    print("Firms calculated Wage bills!!")
    print("")

    myWorld.f_data = f_data
    myWorld.f_array = f_array
    myWorld.c_array = c_array

            
def updateHouseholdJobOffers(f, applicants, c_array):
    for a in applicants:
        c = c_array[a-1]
        c.updateJobOffers(f)

def getVacancies(f, c_f, c_array, theta):
    n = 0
    rv_array = np.random.binomial(1,0.5,size=len(c_f))
    for j in (c_f):
        c = c_array[j-1]
        #print(c.getDaysEmployed(), theta, " firm ", f.getId())
        if c.getDaysEmployed()+1 > theta:
            rv = rv_array[c_f.index(j)]
            if rv == 1:
                f.removeHousehold(c.getId())
                c.updatePrevEmployer(f.getId())
                c.updateEmploymentStatus()
                #print("employment contract expired: ", c.getId()," at ",f.getId(), c.getEmploymentStatus())
                c.setEmployedFirmId(0)
                c.setWage(0)
                c.resetEdays()
                n = n + 1

    f.updateNumberOfExpiredContract(n)
    f.updateTotalEmployees()
    #print(f.getId(), f.getTotalEmployees(), f.getRequiredLabor(), f.getNumberOfExpiredContract())
    v = f.calcVacancies()
    #f_d[f.getId()-1, 16] = f.getNumberOfExpiredContract()
    return v
   
            

def wagePayments(myWorld, t, H, Fc):
    f_array = myWorld.f_array
    c_array = myWorld.c_array
    min_w = myWorld.wage_lvl[t-1]
    mw=0
    for f in f_array:
        if f is not None:
            emp = f.getEmployedHousehold()
            for e in emp:
                c = c_array[e-1]
                c.setWageFlag()
                mw = max(mw,c.getWage())
            f.wagePaid()
            
    for c in c_array:
        if c.getEmploymentStatus():
            c.setUnempBenefits(0)
        else:
            if t == 0:
                min_w = 0.5*mw
            c.setUnempBenefits(0.5*min_w)
            
            
            
            
    
    
    
    
    