#更改当前python工作目录，更改后， 所有文件默认保存在新的文件夹下
#不过每次重新打开python时工作目录又会回到原来的那个
import os
os.getcwd() #查看当前工作目录
os.chdir("D:\\lottowebpage") #改变目录，注意双引号和反斜杠