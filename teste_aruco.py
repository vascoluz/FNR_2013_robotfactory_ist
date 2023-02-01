import cv2

VideoCap = False
cap = cv2.VideoCapture(0)

def findAruco(img, markerSize = 5, totalMarkers = 50, draw = True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = cv2.aruco.Dictionary_get(key)
    arucoParam = cv2.aruco.DetectorParameters_create()    
    bbox, ids, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    if ids != None:
        print(ids)
    if draw:
        cv2.aruco.drawDetectedMarkers(img, bbox)
    
    return ids

while True:
    _,img = cap.read()
    ids = findAruco(img)

    if cv2.waitKey(1) == 113: #113 -> letter 'Q' (used for exit)
        break

    cv2.imshow("img", img)