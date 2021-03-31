from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
import PIL
from PIL import Image
import numpy as np

file = 'Capital Markets.txt'

with open (file, 'r', encoding='latin1') as fin:
    data = fin.read()

stopwords = set(STOPWORDS)

image_mask = np.array(Image.open("bunny.jpg"))

cloud = WordCloud(font_path= None, stopwords = STOPWORDS, mask = image_mask, background_color= 'white', width=1200,height=1000,colormap='plasma').generate(data)

cloud.to_file("Capital_markets_cloud.jpeg")
plt.imshow(cloud)
plt.axis('off')
plt.show()
