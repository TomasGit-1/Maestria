import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_blue = np.array([0, 100, 83])
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    res = cv.bitwise_and(frame, frame, mask=mask)

    # Resize images to ensure they have the same dimensions
    frame = cv.resize(frame, (300, 200))  # Resize frame for uniform display
    mask = cv.resize(cv.cvtColor(mask, cv.COLOR_GRAY2BGR), (300, 200))  # Convert mask to BGR and resize
    res = cv.resize(res, (300, 200))  # Resize res for uniform display

    # Stack images horizontally
    combined = np.hstack((frame, mask, res))

    # Display the stacked images
    cv.imshow('Combined', combined)

    # Check for ESC key press to exit
    if cv.waitKey(1) & 0xFF == 27:
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
