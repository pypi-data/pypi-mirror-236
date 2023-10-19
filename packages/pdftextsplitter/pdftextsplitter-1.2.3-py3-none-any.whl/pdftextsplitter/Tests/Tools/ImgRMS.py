from PIL import Image, ImageChops 
import math, operator
import matplotlib.pyplot as plt

def ImgRMS(picturename1: str, pciturename2: str) -> list[float]:
    """
    # Calculates mu and sigma of the difference between two images.
    
    # Parameters
    # picturename1 (str): full filename of the first  picture to compare, including the full path and file extension.
    # picturename2 (str): full filename of the second picture to compare, including the full path and file extension.
    
    # Returns:
    list[float]: [mu, sigma] of the difference between the pictures.
    """
    
    # ------------------------------------------------------------

    # begin by opening the two pictures:
    im1 = Image.open(picturename1)
    im2 = Image.open(pciturename2)
    
    # Compute the datapoints of the difference:
    data = ImageChops.difference(im1, im2).histogram()
    
    # Close the pictures:
    im1.close()
    im2.close()
  
    # Calculate mu and sigma:
    n = len(data)
    mu = 0.0
    sigma = 0.0
    
    for k in range(0,n):
        mu = mu + data[k]
        sigma = sigma + (data[k]*data[k])
    
    mu = mu/n
    sigma = sigma/n
    sigma = sigma - mu*mu
    sigma = math.sqrt(sigma)
    
    # Returns the answer:
    return [mu, sigma]
