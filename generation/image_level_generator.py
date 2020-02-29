from skimage.transform import resize
from dungeon_level.dungeon_tiles import Tiles
from skimage import feature, color, io
import numpy as np

class ImageLevelGenerator:
    @staticmethod
    def generate(level, size):
        image = ImageLevelGenerator.get_level_image()
        image_size = np.array(image.shape)[:2]
        resized_size = (image_size * min(size / image_size)).astype(int) # Resize such that the bigger dimension is the same size as the dimension in size and the smaller dimension is smaller than it's corresponding dimension in size
        resized_image = resize(image, resized_size, anti_aliasing=True)

        if len(resized_image.shape) != 1:
            resized_image = color.rgb2gray(resized_image)

        edges_image = feature.canny(resized_image)
        
        level.upper_layer = np.full(resized_size, Tiles.empty)
        level.lower_layer = np.full(resized_size, Tiles.empty)

        level.upper_layer[edges_image] = Tiles.wall


    @staticmethod
    def get_level_image():
        # https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSb0bBaPlJF-VWMQ3NCFNzDq1JbPSA-1EYOtMva-IiNVYFNIe9-
        # https://image.shutterstock.com/image-illustration/cute-insect-snail-260nw-789321244.jpg
        # https://www.pinclipart.com/picdir/middle/192-1925693_there-is-a-side-view-of-a-dog.png
        # https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12234558/Chinook-On-White-03.jpg
        url = "https://www.pinclipart.com/picdir/middle/192-1925693_there-is-a-side-view-of-a-dog.png"
        image = io.imread(url)
        return image
        