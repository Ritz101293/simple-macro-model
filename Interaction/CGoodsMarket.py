# -*- coding: utf-8 -*-
import numpy as np

def searchAndMatchCGoods(myWorld, t, H, Fc):
    f_array = myWorld.f_array
    c_array = myWorld.c_array
    Z = c_array[0].Z
    c_ids = np.array(range(H)) + 1
    f_ids = np.array(range(Fc)) + 1
    savg= myWorld.S_avg[t-1]
    f_id = list(f_ids)
    for f in f_ids:
        if f is not None:
            f_obj = f_array[f-1]
            Qp = f_obj.getActualQty()
            if Qp <= 0:
                f_id.remove(f)                
    print("")
    print("Consumption Goods market OPENS!!!")
    print("")
    np.random.shuffle(c_ids)
    f_out_of_stock = []   

    for ck in c_ids:
        c = c_array[ck-1]
        C_d = 0
        if t == 0:
            C_d = c.getDesiredCons()
        else:
            c.setDesiredCons(savg)
            C_d = c.getDesiredCons()
            
        if len(f_id) > 0:         
            if len(f_id) >= Z:            
                select_f = np.random.choice(f_id, Z, replace = False)
            else:
                select_f = f_id
        else:
            print("No production in the economy!!!")
        
        cs = 0
        c_rem = C_d - cs
        prev_cs = 0
        select_f = [x for x in select_f if x not in f_out_of_stock and f_array[x-1] is not None]
        
        if len(select_f) > 0:
            prices = []
            for f in select_f:
                if f_array[f-1] is not None:                
                    prices.append(f_array[f-1].getPrice())
            
            select_f_np = np.array(select_f)
            prices = np.array(prices)
            
            #print(ck,list(select_f_np),list(prices))
            for i in range(len(select_f_np)):
                i = np.argmin(prices)
                pmin = np.min(prices)
                fi = select_f[i]
                if f_array[fi-1] is not None:
                    Qrf = f_array[fi-1].getQtyRemaining()
                    #print(fi, c_rem, Qrf)
                    if Qrf > 0.001:
                        #print("Firm qty rem:", Qrf*pmin, fi, pmin)
                        Qr = Qrf*pmin
                        Qs = 0
                        
                        if Qr >= c_rem:
                            cs = cs + c_rem
                            Qs = Qs + c_rem
                            c_rem = C_d - cs
                            Qr = Qr -Qs
                            
                        else:
                            cs = cs + Qr
                            c_rem = C_d - cs
                            Qs = Qs + Qr
                            Qr = 0
                        #print(prev_cs, cs)
                        prev_cs = cs - prev_cs
                        f_array[fi-1].setQtySold(Qs/pmin)
                        f_array[fi-1].setQtyRemaining()
                        
#                        print("Household no %d with total demand worth %f purchased goods worth %f from firm %d at price %f" %
#                              (ck, C_d, prev_cs, fi, pmin))
                        prices = np.delete(prices, i)
                        select_f = np.delete(select_f, i)
                    if f_array[fi-1].getQtyRemaining() < 0.001:                    
                        f_out_of_stock.append(fi)
                        #print("Firm %d out of stock!!!!!!" %(fi))
                        #print("")
                if c_rem == 0:
                    break
#        else:
#            print("Selected firm is out of stock!!!")
        #print(select_f)       
        c.setActualCons(cs)
        c.updateSavings()
           
        
    #print("")
    print("Consumption Goods market CLOSED!!!")           
    print("")
    print("Firms calculating Revenues......")
    computeRevenues(f_array)
    print("")
    print("Revenues Calculated!!!")
    print("")
    
                
    myWorld.f_array = f_array
    myWorld.c_array = c_array
            
         
def computeRevenues(f_array):
    for f in f_array:
        if f is not None:
            f.calcRevenues()
            #print("firm %d sold %f of goods at price %f with revenue of %f"%(f.getId(),f.getQtySold(),f.getPrice(),f.getRevenues()))
              
      
    

def doProduction(myWorld, t):
    f_array = myWorld.f_array
    print("")
    print("Firms producing....!")

    for f in f_array:
        if f is not None:                
            #print("desired:",f.getDesiredQty())
            f.setDesiredQty()
            f.resetQtySold()
            f.setActualQty()
            f.setQtyRemaining()
#            print("L:", f.getTotalEmployees())
#            print("alpha:",f.getProductivity())
            if t==0:
                Qp = f.getActualQty()
                if Qp != 0:
                    #L_rp = f.getLoanToBePaid()
                    f.setPriceAtT0(1.5*f.getActualWageBill()/(Qp)) #Code is different inside class file
#            if f.getActualQty() == 0:
#                print("Firm %d produced %f qty of cgoods worth %f with %f employees and productivity of %f" %
#                  (f.getId(), f.getActualQty(), f.getActualQty()*f.getPrice(), f.getTotalEmployees(),
#                   f.getProductivity()))

    print("Production DONE!!!")
    print("")
    myWorld.f_array = f_array

            
    