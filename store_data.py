
# import necessary libraries
import pandas as pd
import numpy as np
from sims import Ts,wl
from app.constants import Sizes
import matplotlib.pyplot as plt
# create a dummy array
trans_data = Ts
wvln=wl
td=[]
ww=[]

for i in range (80,200):
    if trans_data[i]>1:
        pass
    else:
        td.append(trans_data[i])
        ww.append(wvln[i])
percentage= 0
for i in range(len(td)):
    percentage = percentage+td[i]
percentage =  percentage/len(td)


# display the array
plt.figure()
plt.plot(ww,td,'ro-',label='transmitance')
#plt.plot(wl,1-Ds-Ts,'go-',label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.savefig('_'+str(Sizes.block_x)+'_rnm.png')
plt.show()

# convert array into dataframe
DF = pd.DataFrame([[str(Ts),str(td),Sizes.block_x,Sizes.alpha,percentage]], columns=['Transmitance data','Transmitance used data', 'l_o','Alpha','%'])
DF_easy_to_read = pd.DataFrame([[Sizes.block_x,Sizes.alpha,percentage]], columns=['l_o','Alpha','Transmitance %'])

with open('arrays&trans.csv', 'a') as f:
    DF.to_csv(f,index=False, header=f.tell()==0)
with open('transmitance.csv', 'a') as f:
    DF_easy_to_read.to_csv(f, index=False,header=f.tell()==0)
