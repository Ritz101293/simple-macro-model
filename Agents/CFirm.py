# -*- coding: utf-8 -*-
'''  
Simple no-growth Agent Based Macroeconomic Model (in Python)
Copyright (C) 2018 Ritesh Kakade

'''

import numpy as np

class CFirm:
    
    H = 2 # Number of banks a firm select randomly to search for credit.
    h_eta = 0.1 # max value of price update parameter
    h_pho = 0.1 # max value of qty update parameter
    r_bar = 0.4 # Base interest rate set by central bank(absent in this model)
    theta = 8 # Duration of contract
    h_zeta = 0.01 # Wage increase parameter
    delta = 0.5 # Dividend payments parameter
    
    def __init__(self, f, fc, NWa):
        self.id = f # Firm id
        self.hbyf= fc
        self.aa = NWa*0.6
        self.Qd = 0 # Desired qty production
        self.Qp = 0 # Actual Qty produced
        self.Qs = 0 # Qty sold
        self.Qr = self.Qp - self.Qs # Qty Remaining
        self.eta = np.random.uniform(low=0,high=self.h_eta) # Price update parameter
        self.p = 0 # Price
        self.pho = np.random.uniform(low=0,high=self.h_pho) # Qty update parameter
        self.bankrupcy_period = 0
        
        self.alpha = np.random.uniform(low=5,high=6) # Labor Productivity
        self.Ld = 0  # Desired Labor to be employed
        self.Lhat = 0 # Labor whose contracts are expiring
        self.L = 0 # Actual Labor Employed
        self.Wb_d = 0 # Desired Wage bills
        self.Wb_a = 0 # Actual Wage bills
        self.Wp = 0 # Wage level
        self.vac = 0
        self.W_pay = 0 # Wage updated when paying
        self.job_applicants = [] # Ids of Job applicants
        self.job_offered = [] # Ids of selected candidates
        self.last_wage_t = 0 # Previous wage offered
        self.w_emp = [] # Ids of workers/household employed
        self.is_hiring = False # Flag to be activated when firm enters labor market to hire

        self.P = 0 # Profits
        self.p_low = 0 # Min price below which a firm cannot charge
        self.NW = NWa*200 # Net-Worth of a firm
        self.Rev = 0 # Revenues of a firm
        self.Total_Rev = 0
        self.RE = 0 # Retained Earnings
        self.divs = 0 # Dividend payments to the households
        
        self.B = 0 # amount of credit (total)
        self.banks = [] # banks from where the firm got the loans
        self.Bi = [] # Amount of credit taken by banks
        self.r = [] # rate of Interest on credit by banks
        self.loan_paid = 0
        self.pay_loan = False # Flag to be activated when firm takes credit
        self.credit_appl = []
        self.loan_to_be_paid = 0
        
    def getId(self):
        return self.id
    
    def resetSomeVariables(self):
        self.job_applicants = []
        self.job_offered = []
        self.credit_appl = []
        self.Lhat = 0
        self.loan_paid = 0
        self.Ld = 0
        self.banks = []
        self.Bi = []
        self.r = []
        self.Rev = 0
        self.divs = 0
        self.loan_to_be_paid = 0
        self.P = 0
        self.RE = 0
        self.B = 0
        self.Wb_d = 0
        self.Wb_a = 0
        self.vac = 0
        
    ####################################### LABOR MARKET FUNCTION #######################################
    
    def setWage(self, zeta):
        w_min = self.aa
        if self.calcVacancies() > 0:
            self.Wp = np.around(max(w_min, min(w_min*(np.random.uniform(low=1.01,high=1.10)),self.Wp*(1+zeta/2))),decimals=2)
            self.is_hiring = True
        else:
            self.Wp = np.around(max(w_min, self.Wp),decimals=2)
            self.is_hiring = False

    def getWage(self):
        return self.Wp
    
    def setDesiredWageBill(self):
        self.Wb_d = self.getWage()*self.getRequiredLabor()
    
    def getDesiredWageBill(self):
        return self.Wb_d

    def setActualWageBill(self):
        self.Wb_a = self.getWage()*self.getTotalEmployees()
    
    def getActualWageBill(self):
        return self.Wb_a
    
    def isHiring(self):
        return self.is_hiring
    
    def employHousehold(self, h_id):
        self.w_emp.append(h_id)
    
    def updateEmployedHousehold(self, a):
        self.w_emp = a
    
    def removeHousehold(self, a):
        self.w_emp.remove(a)
    
    def getEmployedHousehold(self):
        return self.w_emp
    
    def getTotalEmployees(self):
        return self.L
    
    def updateTotalEmployees(self):
        self.L = len(self.w_emp)
    
    def updateNumberOfExpiredContract(self, n):
        self.Lhat = self.Lhat + n
    
    def getNumberOfExpiredContract(self):
        return self.Lhat
    
    def updateApplicant(self, cid):
        self.job_applicants.append(cid)
    
    def getJobApplicants(self):
        return self.job_applicants
    
    def updateJobOffered(self, a):
        self.job_offered = a
    
    def getJobOffered(self):
        return self.job_offered
    
    def calcVacancies(self):
        V = int((self.Ld - self.L + self.Lhat)*1)
        self.vac = V
        if V > 0:
            return V
        else:
            return 1
    
    def calcVacRate(self):
        self.vac = self.vac - self.getTotalEmployees()
    
    def getVacRate(self):
        return self.vac
    
    def setRequiredLabor(self, flag):
        #print(self.Qd,self.alpha)
        if flag:
            self.Ld = self.hbyf
        else:
            self.Ld = int(self.Qd//self.alpha)
    
    def getRequiredLabor(self):
        return self.Ld

    #################################### CONSUMTION GOODS RELATED FUNCTIONS ##############################
        
    def setPriceAtT0(self, p):
        self.p = p
    
    def getPrice(self):
        return self.p
    
    def setMinPrice(self):
        if self.getQtySold() != 0:           
            self.p_low = 0#(self.getLoanToBePaid())/(self.getQtySold())
        else:
            self.p_low = 0
        
    def decideProduction(self, prev_Inv, prev_APrice, prev_FPrice, prev_FQty, desQty):
        p_d = prev_FPrice - prev_APrice
        #print(prev_Inv, prev_APrice, prev_FPrice, prev_FQty)
        if p_d >= 0:
            if prev_Inv > 0:
                #Reduce only Price until lower bound is reached
                self.p = np.around(max(prev_FPrice*(1-self.eta), prev_APrice),decimals=2)
                self.Qd = np.around(prev_FQty,decimals=2) if prev_FQty > 0 else max(1.01*desQty,10)
            else:
                #Increase quantity - firm expect higher demand
                self.Qd = np.around(prev_FQty*(1+self.pho),decimals=2) if prev_FQty > 0 else max(1.01*desQty,10)
                self.p = np.around(prev_FPrice,decimals=2)
        else:
            if prev_Inv > 0:
                #Reduce quantity - firm expect lower demand
                self.Qd = np.around(prev_FQty*(1-self.pho),decimals=2) if prev_FQty > 0 else max(1.01*desQty,10)
                self.p = np.around(prev_FPrice,decimals=2)
            else:
                #Increase only price
                self.p = np.around(max(prev_FPrice*(1+self.eta), prev_APrice),decimals=2)
                self.Qd = np.around(prev_FQty,decimals=2) if prev_FQty > 0 else max(1.01*desQty,10)
#        if prev_FQty ==0:
#            print("Firm %d decides to produce %f amount at %f price with des Qty %f and prev Qty %f"%
#                  (self.getId(),self.Qd,self.p, desQty, prev_FQty))
    
    def getDesiredQty(self):
        return self.Qd
    
    def setDesiredQty(self):
        self.Qd = np.around(self.Qd,decimals=2)
    
    def setProductivity(self):
        self.alpha = np.around(np.random.uniform(low=5,high=6),decimals=2)
    
    def getProductivity(self):
        return self.alpha
    
    def setActualQty(self):
        self.setProductivity()
        qp = self.getProductivity()*self.getTotalEmployees()
        self.Qp = np.around(qp,decimals=2)
    
    def getActualQty(self):
        return self.Qp
    
    def resetQtySold(self):
        self.Qs = 0
    
    def setQtySold(self, qs):
        self.Qs = self.Qs + np.around(qs,decimals=2)
        
    def getQtySold(self):
        return self.Qs
    
    def setQtyRemaining(self):
        self.Qr = self.Qp - self.Qs
    
    def getQtyRemaining(self):
        return self.Qr
    
    ######################################## FINANCIAL MARKET FUNCTION #####################################
    
    def resetBankrupcyPeriod(self):
        self.bankrupcy_period = 0
    
    def getBankrupcyPeriod(self):
        return self.bankrupcy_period
    
    def updateBankrupcyPeriod(self):
        self.bankrupcy_period = self.bankrupcy_period + 1
    
    def resetTotalRevenue(self):
        self.Total_Rev = 0
    
    def calcTotalRevenues(self, r):
        self.Total_Rev = self.Total_Rev + r
        
    def getTotalRevenues(self):
        return self.Total_Rev
    
    def calcRevenues(self):
        self.Rev = np.around(self.getQtySold()*self.getPrice(),decimals=2)
        self.calcTotalRevenues(self.Rev)
    
    def getRevenues(self):
        return self.Rev
    
    def wagePaid(self):
        self.W_pay = self.Wp
    
    def getWagePaid(self):
        return self.W_pay
    
    def calcProfits(self):
        #self.calcRevenues()
        #print("total revenues:", self.getTotalRevenues())
        self.P = np.around(self.getTotalRevenues() -self.getActualWageBill() - np.sum((np.array(self.Bi))*(np.array(self.r))),decimals=2)
        self.resetTotalRevenue()
    
    def getProfits(self):
        return self.P
    
    def setDividends(self):
        if self.getProfits():
            self.divs = np.around(self.getProfits()*self.delta,decimals=2)
        else:
            self.divs = 0
        
    def getDividends(self):
        return self.divs
    
    def calcRetainedEarnings(self):
        self.RE = np.around(self.getProfits() - self.getDividends(),decimals=2)
    
    def getRetainedEarnings(self):
        return self.RE
    
    def updateNetWorth(self):
        self.calcRetainedEarnings()
        self.NW = self.NW + self.getRetainedEarnings()
    
    def getNetWorth(self):
        return self.NW
    
    def isBankrupt(self):
        if (self.NW+self.P) < 0:
            return True
        else:
            return False
        
    ######################################### CREDIT MARKET FUNCTION ####################################
    
    def updateLoanPaymentStatus(self):
        self.pay_loan = not self.pay_loan
    
    def payLoan(self):
        self.loan_paid = np.around(self.getLoanToBePaid(),decimals=2)
    
    def loanRequired(self):
        if self.Wb_a > self.NW:
            self.B = self.Wb_a - self.NW
            return True
        else:
            self.B = 0
            return False

    def getLoanAmount(self):
        return self.B
    
    def setCreditAppl(self, c_a):
        self.credit_appl = c_a
    
    def getCreditAppl(self):
        return self.credit_appl
    
    def addBanksAndRates(self, bid, bi, rt):
        self.banks.append(bid)
        self.Bi.append(bi)
        self.r.append(rt)
    
    def getBanks(self):
        return self.banks
    
    def getCredits(self):
        return self.Bi
    
    def getRates(self):
        return self.r
    
    def setLoanToBePaid(self):
        self.loan_to_be_paid = np.around(np.sum((np.array(self.Bi))*(1 + np.array(self.r))),decimals=2)
    
    def getLoanToBePaid(self):
        return self.loan_to_be_paid
    
    def getLeverageRatio(self):
        if self.NW <= 0:
            return np.random.uniform(low=1.5,high=2.0)
        else:    
            return self.B/self.NW
        

        
        