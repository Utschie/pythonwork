import pagetotxt
import pageloop
from multiprocessing import Pool

p = Pool(8)
for i in range(250000,250008):
    p.apply_async(pageloop,args = (i,)) 


p.close()
p.join()
print('All subprocess done')

