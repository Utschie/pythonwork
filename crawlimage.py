#爬取图片下载到本地文件夹
import requests
imageurl = 'https://www.celebjihad.com/celeb-jihad/harlots/emily_ratajkowski16/main2.jpg'#通过源码找到图片的地址
image = requests.get(imageurl).content#得到图片文件的代码形式
address = 'D:\\emily_ratajkowski.jpg'#规定出图片的写入文件和图片的命名
with open(address,"wb") as f:
  f.write(image)

print(address + '已写入')









