import numpy as np
import cv2
import screeninfo

if __name__ == '__main__':
    screen_id = 1

    # get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]
    # screen = screeninfo.get_monitors()
    print(screen)
    width, height = screen.width, screen.height
    data = cv2.imread(filename='testRESULT.png')    

    window_name = 'SLM'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, data)
    cv2.waitKey()
    cv2.destroyAllWindows()