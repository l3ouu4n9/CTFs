from PIL import Image, ImageChops
image1 = Image.open('image1.png')
image2 = Image.open('image2.png')
diff = ImageChops.difference(image1, image2)
diff.save('diff.png')