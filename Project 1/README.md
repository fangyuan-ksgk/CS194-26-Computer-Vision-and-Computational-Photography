Images of the Russian Empire: Colorizing the Prokudin-Gorskii photo collection
In the 1900s, Prokudin-Gorskii gained permission by the tzar to take pictures throughout the vast Russian empire. He recorded three exposures of every scene on glass panes using red, green, and blue filters. This project seeks to reproduce the true color images using image alignment techniques.

For more description, see project website:
https://inst.eecs.berkeley.edu/~cs194-26/fa21/hw/proj1/

The aviable orginal images can also be found in the proj website, I included two smaller images for quick testing. Those larger .tif file (>60MB) takes less than a minute to run as well.

Examples of original images (emir), containing three missaligned channels:
![image](https://user-images.githubusercontent.com/66006349/147544981-fac4a231-dada-4ba5-993f-0198e136140e.png)

Without any maneuver, the combined color image with the RGB channels given looks like:
![image](https://user-images.githubusercontent.com/66006349/147545262-b6d25e52-a8a7-4a8c-a9a6-ca5bed169513.png)

This project notebook implement image alignment with pyramids methods which produces aligned image:
![image](https://user-images.githubusercontent.com/66006349/147545357-9c294b40-8479-4e33-b9e9-b96a75d6b9c9.png)


