import cv2
import numpy as np


def color_check(color: str, image) -> bool:
    """
    function to that takes a given color and image and determines whethere that color present to a certain level
     in the image using opencv filters
    :param color: the string of the color
    :param image: the image
    :return: True or False, or an error message if a precondition is not met

    :examples:

    >>> color_check("red",  "apple.jpg")
    True

    >>> color_check("green", "limes.jpg")
    True

    >>> color_check("orange", "orange.jpg")
    True

    >>> color_check("yellow", "banana.jpeg")
    True

    >>> color_check("blue", "blue_strawberry.jpg")
    True

    >>> color_check("purple", "plum.jpg")
    True

    """

    # a dictionary for the HSV ranges for each color
    dict_boundaries = {
        "red": [np.array([0, 175, 20]), np.array([10, 255, 255]),
                np.array([160, 100, 20]), np.array([179, 255, 255])],
        "green": [np.array([36, 25, 25]), np.array([70, 255, 255])],
        "orange": [np.array([10, 100, 20]), np.array([25, 255, 255])],
        "yellow": [np.array([21, 39, 64]), np.array([40, 255, 255])],
        "blue": [np.array([60, 35, 140]), np.array([180, 255, 255])],
        "purple": [np.array([155, 5, 5]), np.array([280, 255, 255])],
        "gray": [np.array([0, 0, 70]), np.array([180, 20, 255])],
        "black": [np.array([0, 0, 0]), np.array([180, 255, 70])],
        "white": [np.array([0, 0, 205]), np.array([180, 35, 255])],
        "brown": [np.array([10, 100, 20]), np.array([20, 255, 200])],
    }

    # print(image)
    # the image will be a str name for testing and a numpy array when the function is running with the webcam
    if type(image) is str:
        image = cv2.imread(image)
    elif type(image) is not np.ndarray:
        return TypeError

    cv2.imshow("Picture", image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # converts the image to HSV
    # cv2.imshow("HSV", image)

    boundary = dict_boundaries[color]

    if len(boundary) == 4:  # red has two boundaries because it spans across either end of the HSV specturm

        lower1 = boundary[0]
        upper1 = boundary[1]
        lower2 = boundary[2]
        upper2 = boundary[3]

        lower_mask = cv2.inRange(image, lower1,
                                 upper1)  # cv2.inRange checks for any pixels that fall in the HSV range I set
        upper_mask = cv2.inRange(image, lower2, upper2)

        full_mask = lower_mask + upper_mask  # creates one mask from the two masks
    else:

        lower1 = boundary[0]
        upper1 = boundary[1]

        full_mask = cv2.inRange(image, lower1, upper1)

    # print(lower1)
    # print(upper1)

    white_pixels = np.sum(
        full_mask == 255)  # the mask creates a black and white image where white pixels are pixels that fall in the range
    black_pixels = np.sum(full_mask == 0)  # and black piexels are pixels are pixels that don't fall in the range

    # print(white_pixels)

    # cv2.imshow('mask', full_mask)

    cv2.waitKey(0)
    cv2.destroyWindow('Picture')# closes the windows once a key is pressed
    # print(white_pixels)
    # print(black_pixels)

    if white_pixels > black_pixels / 9:  # if 10% of the image is white that counts as a True case
        return True
    else:
        return False


def camera(source: int) -> None:
    """
    a function that creates a live camera window,
    when the space bar is pressed it takes a picture and that image is returned
    :param source: the source of the camera usually 0, 1, or -1 depending on the device
    :return: the numpy array of the image taken
    """
    vid = cv2.VideoCapture(source)  # capture video from the source
    while True:
        ret, frame = vid.read()
        frame = cv2.flip(frame, 1)  # horizantally inverts the image
        cv2.imshow('frame', frame)  # shows a livefeed of the image

        if cv2.waitKey(1) & 0xFF == ord(' '):  # if space bar is pressed
            image = frame  # takes a picture of the frame
            break

    vid.release()
    cv2.destroyWindow('frame')  # closes the window
    return image  # returns the picture as a numpy array


if __name__ == "__main__":
    print(color_check('brown', camera(0)))
