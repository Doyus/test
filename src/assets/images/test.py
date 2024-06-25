from PIL import Image

# 打开图片,转换模式为RGB
img = Image.open('logo2.png').convert('RGB')

# 获取图片数据
pixels = img.load()

# 定义源颜色和目标颜色
src_color = (51, 51, 51) # 333333
dst_color = (140, 182, 242) # 8CB6F2

# 遍历所有像素,替换颜色
for x in range(img.width):
  for y in range(img.height):
    if pixels[x,y] == src_color:
      pixels[x,y] = dst_color

# 保存结果图片
img.save('logo.png')