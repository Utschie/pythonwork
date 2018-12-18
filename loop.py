for i in range(250000,672742):
    url = 'file:///D:/lottowebpage/odds.500.com/fenxi/ouzhi-{n}.shtml'
    url = url.format(n=i)
    try:
      pagetotxt(url)
      print(i)
    except Exception as e:
      continue


print('MISSION COMPLETED. I AM THE SPIDERMAN')