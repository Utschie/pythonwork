#用这种方式保存下来的网页是乱码
import urllib.request  

def getHtml(url):  
    html = urllib.request.urlopen(url).read()  
    return html     


def saveHtml(file_name,file_content):  #定义两个函数之间要至少空两行，否则会出错  
    #    注意windows文件命名的禁用符，比如 /    
    with open (file_name.replace('/','_')+".html","wb") as f:  
    #   写文件用bytes而不是str，所以要转码    
        f.write( file_content )    
         


html = getHtml("http://odds.500.com/index_history_2016-03-05.shtml") #调用函数时要与之前定义函数空至少三行，否则会出错 
saveHtml("D:\\lottowebpage\\text1",html) #用此种格式指定保存目录 
      
print ("结束")  