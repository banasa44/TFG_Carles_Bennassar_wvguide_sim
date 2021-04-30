
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
plt.title('Transmitance within our laser range wv, for size block:'+str(Sizes.block_x))
plt.plot(ww,td,'ro-',label='transmitance')
#plt.plot(wl,1-Ds-Ts,'go-',label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.savefig('1350_1450_w_'+str(Sizes.block_x)+'_nm.png')
plt.show()

# convert array into dataframe
DF = pd.DataFrame([[str(Ts),str(td),Sizes.block_x,Sizes.alpha,percentage, str(Sizes.version)]], columns=['Transmitance data','Transmitance used data', 'Block size_0','Alpha','%','Version',])
DF_easy_to_read = pd.DataFrame([[Sizes.block_x,Sizes.alpha,percentage, str(Sizes.version)]], columns=['Block size_0','Alpha','Transmitance %','Version',])

with open('arrays&trans.csv', 'a') as f:
    DF.to_csv(f,index=False, header=f.tell()==0)
with open('transmitance.csv', 'a') as f:
    DF_easy_to_read.to_csv(f, index=False,header=f.tell()==0)
