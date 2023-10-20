import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import PIL
from sklearn.cluster import KMeans


# Inspiration from: https://towardsdatascience.com/finding-most-common-colors-in-python-47ea0767a06a

def palette(clusters):
    """
    Creates a palette of colors from the clusters.
    :param clusters:
    :return: A list of center clusters
    """

    width = 200
    color_palette = np.zeros((50, width, 3), np.uint8)
    steps = width / clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_):
        color_palette[:, int(idx * steps):(int((idx + 1) * steps)), :] = centers
    return color_palette


def extract_palette_from_image(image_relative_path, num_colors=10):
    """
    Extracts the main colors from an image and returns them as a list of RGB tuples.
    :param image_relative_path: The absolute path to the image.
    :param num_colors: The number of colors to extract.
    :return: A list of RGB tuples.
    """

    # Read image with open CV
    img = cv.imread(image_relative_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    dim = (200, 200)  # The albums are always a square
    # resize image
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    clt = KMeans(n_clusters=num_colors, n_init='auto')
    clt.fit(img.reshape(-1, 3))

    clt_1 = clt.fit(img.reshape(-1, 3))

    return img, palette(clt_1), rgb_to_hex(clt_1)


def show_image_and_palette(img_reduced, img_palette):
    """
    Shows the image and the palette of colors extracted from it.
    :param img_reduced:
    :param img_palette:
    """
    f, ax = plt.subplots(1, 2, figsize=(10, 10))
    ax[0].imshow(img_reduced)
    ax[1].imshow(img_palette)
    ax[0].axis('off')
    ax[1].axis('off')
    f.tight_layout()
    plt.show()


def rgb_to_hex(color_clusters: KMeans):
    """
    Extract the colors from the image palette and returns them as a hex string.
    :param color_clusters: The color clusters.
    :return: The hex string.
    """
    palette_colors = []

    for _, color in enumerate(color_clusters.cluster_centers_):
        color_rgb = np.array(color, dtype=int)
        color_hex = '#{:02X}{:02X}{:02X}'.format(*color_rgb)
        palette_colors.append(color_hex)

    return palette_colors
