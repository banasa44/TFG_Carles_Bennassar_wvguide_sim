
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
plt.title('Transmitance within our laser range wv, for w='+str(Sizes.block_x)+', alpha='+str(Sizes.alpha)+'μm')
plt.plot(ww,td,'ro-',label='transmitance')
#plt.plot(wl,1-Ds-Ts,'go-',label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.ylabel("transmitance")
plt.legend(loc="best")
plt.savefig('app/static/images/graph/1350_1450_w_'+str(Sizes.block_x)+'alph_'+str(Sizes.alpha)+'μm.png')
#plt.show()

# convert array into dataframe
DF_Ts = pd.DataFrame(np.transpose(Ts))
DF_td = pd.DataFrame(np.transpose(td))
DF_easy_to_read = pd.DataFrame([[Sizes.block_x,Sizes.alpha,percentage, str(Sizes.version)]], columns=['Block size_0','Alpha','Transmitance %','Version',])

with open('app/static/csv/trans_full_range_11_arrays.csv', 'a') as f:
    DF_Ts.to_csv(f,index=True, header=f.tell()==0)
with open('app/static/csv/trans_optim_range_11_arrays.csv', 'a') as f:
    DF_td.to_csv(f,index=True, header=f.tell()==0)
with open('app/static/csv/transmitance.csv', 'a') as f:
    DF_easy_to_read.to_csv(f, index=False,header=f.tell()==0)
