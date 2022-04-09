import array as arr
class Data:
    def cwgr(stock):
        cwgr_prog=arr.array('f')
        for i in range(0,len(stock),4):
            if i+4 >= len(stock):
                break 
            else:
                growth=stock[i+4]/stock[i]
                num_semanas=4
                cwgr_prog.append(growth**(1/num_semanas)-1)
        return cwgr_prog
    
        
