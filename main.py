import screeninfo
import numpy
from Modules import optcheck, highgui, imgproc


def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.openImage(imagePath)

    monitor = screeninfo.get_monitors()[0]
    image = highgui.resizeImage(image, (monitor.width >> 1, monitor.height >> 1)) # adjust width and height to base screen
    
    image = imgproc.detectLines(image, 50, 200, rho = 1, theta = numpy.pi / 180)
    highgui.showImage(image, "WindowName")

if __name__ == '__main__':
    main()