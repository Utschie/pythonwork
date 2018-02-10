import gevent
import time

def coroutine(start):
  ge = list()
  for i in range(0,150):
      ge.append(gevent.spawn(print,start))
      start = start+1
  for i in range(0,150):
      ge[i].join()
      time.sleep(0.1)
      gevent.sleep(0)
   


for i in range(250000,250150,150):
    coroutine(i)
    pass