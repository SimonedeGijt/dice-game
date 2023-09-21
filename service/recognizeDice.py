import os

import cv2
import numpy as np
from sklearn.cluster import DBSCAN

env = os.getenv('ENV', 'dev')
print("Environement is: " + env)
if env != 'dev':
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


def find_dice_values(img, blur, min_contour):
    # Convert the image to grayscale
    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (blur, blur), 0)

    # cv2.imshow("show blurred",blurred)
    # cv2.waitKey()
    # Use Canny edge detection to detect edges
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize an empty list to store results
    dice_dot_contours = []
    displayImg = img.copy()
    for contour in contours:

        #cv2.putText(img, cv2.contourArea(contour), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1)

        # Filter out small contours
        if (cv2.contourArea(contour) > min_contour):
            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)


            if (w > 100 or  h > 100): #filter out big images
                cv2.rectangle(displayImg, (x, y), (x + w, y + h), (0, 255, 255), 2)
                continue

            if(w/h < 0.9 or h/w <0.9): #filter out non-square parts
                cv2.rectangle(displayImg, (x, y), (x + w, y + h), (255, 255, 255), 2)
                continue

            # roi = gray[y:y+h, x:x+w]
            cv2.rectangle(displayImg, (x, y), (x + w, y + h), (255, 0, 0), 2)

            dice_dot_contours.append(contour)
        else:
            #print(cv2.contourArea(contour))
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(displayImg, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cv2.imshow(f"show contours with blur:{blur}" ,displayImg)
    #cv2.waitKey()

    result = []

    cluster_var = 100
    if len(dice_dot_contours) > 0:
        diceValues = find_contour_clusters(dice_dot_contours, cluster_var, 1)
        for list in diceValues:
            result.append(len(list))

    if(len(result) != 5):

        cluster_var = 90
        while len(result) != 5 and cluster_var < 120:
            result = []
            if len(dice_dot_contours) > 0:
                diceValues = find_contour_clusters(dice_dot_contours, cluster_var, 1)
                for list in diceValues:
                    result.append(len(list))
            cluster_var = cluster_var + 5

    return result


def recognize_dice_in_image(file_name=''):
    if env == 'dev':
        img = cv2.imread(file_name)
    else:
        img = pictureService.take_picture()

    blur = 9
    min_contour = 250
    dice_values = find_dice_values(img, blur, min_contour)
    blur = 3
    while(len(dice_values) != 5 and blur<21):
        blur = blur + 2

        if(blur >=17):
            min_contour = 12
        new_result = find_dice_values(img, blur, min_contour)
        #cv2.imshow("show contours",img)

        #cv2.waitKey()
        if(len(new_result) == 5 or abs(len(new_result) - 5) < abs(len(dice_values)-5)):
            dice_values = new_result

    print(dice_values)

    return dice_values


if __name__ == "__main__":
    recognize_dice_in_image("/Users/weijs01/Techdays/dice-game/tests/resources/pictures2/test18.jpg")
