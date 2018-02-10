import pagetotxt
def pageloop(x):
  url = 'file:///D:/lottowebpage/odds.500.com/fenxi/ouzhi-{n}.shtml'
  url = url.format(n=x)
  pagetotxt(url)
  print(x)


