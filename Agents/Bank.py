# -*- coding: utf-8 -*-
import numpy as np

class Bank:
    
    h_phi = 0.1
    mu = 0.11
    r_bar = 0.04
    
    def __init__(self, NB0, b, aNB,factor):
        self.id = b
        
        self.E = 0
        
        self.phi = 0
        self.tCr = (NB0/aNB)*10*factor
        self.Cr = 0
        self.Cr_a = 0
        self.Cr_rem = 0
        self.Cr_d = []
        self.r_d = []
        self.r =[]
        self.firms_appl = []
        self.firms_loaned = []
        
        self.Cr_p = 0
    
    def getId(self):
        return self.id
    
    def resetSomeVariables(self):
        self.Cr_p = 0
        self.firms_appl = []
        self.firms_loaned = []
        self.Cr_a = 0
        self.Cr_rem = 0
    
    def updateEquity(self):
        self.E = self.E + self.getLoanPaid()
    
    def getEquity(self):
        return self.E
    
    def updateFirmsAppl(self, fid):
        self.firms_appl.append(fid)
    
    def getFirmsAppl(self):
        return self.firms_appl
    
    def calcPhi(self):
        self.phi = np.random.uniform(low=0,high=self.h_phi)
        
    def calcIntRate(self, lev):
        self.calcPhi()
        rt = self.r_bar*(1 + self.phi*np.sqrt(lev))
        return rt

    def updateIntRates(self, r):
        self.r.append(r)
    
    def getIntRates(self):
        return self.r
    
    def setCreditSupply(self):
        if self.E == 0:
            self.Cr = self.tCr
        else:
            self.Cr = self.E/0.11
    
    def setActualCreditSupplied(self, c):
        self.Cr_a = self.Cr_a + c
    
    def getActualCreditSupplied(self):
        return self.Cr_a
    
    def setRemainingCredit(self):
        self.Cr_rem = self.Cr - self.Cr_a
    
    def getRemainingCredit(self):
        return self.Cr_rem
    
    def getCreditSupply(self):
        return self.Cr
    
    def addFirmsRatesCredits(self, fid, cr, rt):
        self.firms_loaned.append(fid)
        self.Cr_d.append(cr)
        self.r_d.append(rt)
    
    def getFirms(self):
        return self.firms_loaned
    
    def getCreditDisbursed(self):
        return self.Cr_d
    
    def getRatesDisbursed(self):
        return self.r_d
    
    def setLoanPaid(self, p):
        self.Cr_p = self.Cr_p + p
    
    def getLoanPaid(self):
        return self.Cr_p
    