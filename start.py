# -*- coding: utf-8 -*-

from Agents.World import World
from Interaction.LabourMarket import searchAndMatchLabor, wagePayments
from Interaction.CreditMarket import searchAndMatchCredit, settleDebts
from Interaction.CGoodsMarket import doProduction, searchAndMatchCGoods
from Interaction.FinancialMarket import payDividends, checkForBankrupcy
from DataCollection.Stats import updateData, calcStatistics
from DataCollection.Plots import plotAndSaveGraphs

import numpy as np
import time

start_time = time.time()

T = 100#int(input("Enter the time period :"))
H = 500#int(input("Enter the number of households:"))
Fc = 100#int(input("Enter the number of C-firms:"))
B = 2#int(input("Enter the number of banks:"))
myWorld = World(H, Fc, B, T)
myWorld.populate()
c_d = np.zeros((T+2, H, 20))
f_d = np.zeros((T+2, Fc, 20))
b_d = np.zeros((T+2, B, 20))



for t in range(T):
    
    
    print("Time Period equals :", t)
    # 1) Firms decide output to be produced and thus labor required(desired), accordingly price or quantity is 
    # updated along with firms expected demand
    #
    # 2) A fully decentr labor market opens. Firms post vacancies with wages. Workers approach subset of 
    # firms (randomly selected) acoording to wage offer. Laborr contract expires after finite period "theta"
    # and worker whose contract has expired applies to most recent firm first. Firm pays wage bills to start.
    #
    searchAndMatchLabor(myWorld, t, H, Fc)
    # 3) If there is a financing gap, firms go to credit market. Go to random chosen bank to get loans starting
    # with one having lowest interest rate. Banks sort borrowers application according financial condition and
    # satisfy untill the exhaustion of credit supply. Interest rate is calc acc to markup on an baseline rate.
    # After credit market closed, if firms are short, they fire workers or dont accept them.
    #
    searchAndMatchCredit(myWorld, t, Fc, B)
    # 4) Production takes one unit of time regardless of the scale of prod/firms
    #
    doProduction(myWorld, t)
    # 5) After production is completed, goods market opens. Firm post their offer price, consumer contact
    # subset of randomly chosen firm acc to price and satisfy their demand. goods with excess supply can't be
    # stored in an inventory and they are dispopsed of with no cost.
    # 
    searchAndMatchCGoods(myWorld, t, H, Fc)
    # 6) Firms collect revenue and calc gross profits. If gross profits are high enough, they pay principal
    # and interest to bank. If net profits is +ve, they pay dividends.
    #        
    # 7) Earnings after interest payments and dividends are retained earnings which are carried forword to 
    # next period to increase net worth. positive net worth, survive otherwise firms/banks go bankrupt.
    #
    wagePayments(myWorld, t, H, Fc)
    settleDebts(myWorld, t, Fc, B)
    payDividends(myWorld, t, H, Fc, B)
            # Function for dividend payments
    # 8) New firms/banks enter the market of size smaller than average size ofthose who got bankrupt.
    updateData(myWorld, t, H, Fc, B)
    calcStatistics(myWorld, t, H, Fc, B)
    checkForBankrupcy(myWorld,t)
    if t in [50, 100, 150, 200, 300, 400, 500, 800, 1000]:
        plotAndSaveGraphs(myWorld, t, T)
    v=raw_input("Press Enter to continue...")
                
c_d = myWorld.c_data
f_d = myWorld.f_data
b_d = myWorld.b_data

plotAndSaveGraphs(myWorld, None, T)



print("Time taken to execute: %s seconds" % (time.time()-start_time))