import numpy as np
from sklearn.cluster import DBSCAN
import cv2

import os
env = os.getenv('ENV')
print("Environement is: " + env)
if(env != 'dev'):
    import pictureService

def find_contour_clusters(contours, epsilon, min_samples):
    # Extract centroid coordinates from contours
    centroids = []

    for contour in contours:
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centroids.append([cX, cY])

    centroids = np.array(centroids)

    # Apply DBSCAN clustering
    clustering = DBSCAN(eps=epsilon, min_samples=min_samples).fit(centroids)

    # Get labels assigned to each centroid
    labels = clustering.labels_

    # Create a dictionary to store clusters
    clusters = {}
    for i, label in enumerate(labels):
        if label != -1:  # Ignore noise points (label -1)
            if label not in clusters:
                clusters[label] = []

            clusters[label].append(contours[i])

    return list(clusters.values())
def find_dice_values(img, blur):

    # Convert the image to grayscale
    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (blur, blur), 0)

    #cv2.imshow("show blurred",blurred)
    #cv2.waitKey()
    # Use Canny edge detection to detect edges
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize an empty list to store results
    dice_dot_contours = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Filter out small contours
        if cv2.contourArea(contour) > 1500:
            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)

            if(w > 100):
                continue

            # Crop the region of interest
            # roi = gray[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            dice_dot_contours.append(contour)


    diceValues = find_contour_clusters(dice_dot_contours, 200, 1)

    #cv2.imshow("show contours",img)
    #cv2.waitKey()

    result = []

    for list in diceValues:
        result.append(len(list))

    return result

def recognizeDiceInImage(fileName):
    if(env == 'dev'):
        img = cv2.imread(fileName)
    else:
        img = pictureService.takePicture()
    dicevalues = find_dice_values(img,9) #blur = 9 is a magic number that seems to work for most
    if(len(dicevalues) != 5) : #if we did not detect 5 dice add more blur
        dicevalues = find_dice_values(img, 15) #blur = 15 seems to work for most other cases.

    print(dicevalues)
    return dicevalues

if __name__ == "__main__":
    recognizeDiceInImage("")
