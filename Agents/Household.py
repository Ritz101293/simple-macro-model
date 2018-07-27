# -*- coding: utf-8 -*-
import numpy as np

class Household:
    #firm_ids = None
    Z = 3
    M = 4
    beta = 4
    
    def __init__(self, Y0, MPC, h):
        self.id = h
        
        self.Y = Y0
        self.S = 0
        self.C = 0
        self.C_d = MPC*Y0
        self.MPC = 0
        
        self.w = 0
        self.w_r = 0
        self.unemp_benefit = 0
        self.div = 0
        self.w_flag = 0
        self.div_flag = 0
        
        self.is_employed = False
        self.d_employed=0
        self.d_unemployed=0
        self.firm_id = 0
        self.prev_firm_id = 0
        self.firms_applied = []
        self.job_offers = []
        self.prev_F = 0

    
    def getId(self):
        return self.id
    
    def resetSomeVariables(self):
        self.firms_applied = []
        self.job_offers = []
        self.w_flag = 0
        self.div_flag = 0
        self.div=0
    
    def updateIncome(self):
        self.Y = np.around(self.getSavings() + self.getWage() + self.getUnempBenefits()+ self.getDividends(),decimals=2)
    
    def getIncome(self):
        return self.Y
    
    def calcMPC(self, S_avg):
        self.MPC = np.around(1/(1 + (np.tanh(self.S/S_avg))**self.beta),decimals=2)

    def getMPC(self):
        return self.MPC
    
    def setDesiredCons(self, S_avg):
#        if S_avg ==0:
#            self.C_d = self.C_d/p_lvl
#        else:
        self.calcMPC(S_avg)
        self.C_d = np.around((self.getIncome())*self.getMPC(),decimals=2)
        
    def getDesiredCons(self):
        return self.C_d
    
    def setActualCons(self, c):
        self.C = np.around(c,decimals=2)
        
    def getActualCons(self):
        return self.C
    
    def updateSavings(self):
        self.S = np.around(self.Y - self.C,decimals=2)
    
    def getSavings(self):
        return self.S
    
    def setPrevCFirm(self, f):
        self.prev_F = f
    
    def getPrevCFirm(self):
        return self.prev_F
        
    def setEmployedFirmId(self, f_id):
        self.firm_id = f_id
    
    def getEmployedFirmId(self):
        return self.firm_id
    
    def updatePrevEmployer(self, fid):
        self.prev_firm_id = fid
    
    def setWage(self, w):
        self.w = np.around(w,decimals=2)
    
    def getWage(self):
        return self.w
    
    def setUnempBenefits(self,u):
        self.unemp_benefit = np.around(u,decimals=2)
    
    def getUnempBenefits(self):
        return self.unemp_benefit
    
    def setWageFlag(self):
        self.w_flag = 1
    
    def unsetWageFlag(self):
        self.w_flag = 0
    
    def setDividends(self, d):
        self.div = self.div + np.around(d,decimals=2)
        
    def getDividends(self):
        return self.div
    
    def setDivFlag(self):
        self.div_flag = 1
    
    def unsetDivFlag(self):
        self.div_flag = 0
    
    def getPrevEmployer(self):
        return self.prev_firm_id
    
    def incrementEdays(self):
        self.d_employed = self.d_employed + 1
    
    def incrementUdays(self):
        self.d_unemployed = self.d_unemployed + 1
    
    def resetEdays(self):
        self.d_employed = 0
    
    def resetUdays(self):
        self.d_unemployed = 0
    
    def getDaysEmployed(self):
        return self.d_employed
    
    def getDaysUnemployed(self):
        return self.d_unemployed
    
    def updateEmploymentStatus(self):
        self.is_employed = not self.is_employed
    
    def getEmploymentStatus(self):
        return self.is_employed
    
    def applyToFirm(self, fid):
        self.firms_applied.append(fid)
    
    def setAppliedFirms(self, fa):
        self.firms_applied = fa
    
    def getFirmsApplied(self):
        return self.firms_applied
    
    def updateJobOffers(self, fid):
        self.job_offers.append(fid)
    
    def getJobOffers(self):
        return self.job_offers
    
    
        
        
        
        
        
        
        
        
        