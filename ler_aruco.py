import cv2
import numpy as np
import pyrealsense2 as rs

# Configure color stream
pipeline = rs.pipeline()
config = rs.config()

# Function that finds the aruco
def findAruco(img, markerSize = 5, totalMarkers = 50, draw = True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = cv2.aruco.Dictionary_get(key)
    arucoParam = cv2.aruco.DetectorParameters_create()    
    bbox, ids, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    if draw:
        cv2.aruco.drawDetectedMarkers(img, bbox)

    return ids

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent frame: color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        # Convert image to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Reading the aruco
        ids = findAruco(color_image)

        if ids != None:
            print(ids)

        # Show images
        cv2.namedWindow('RealSense Camera', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense Camera', color_image)

        if cv2.waitKey(1) == 113: #113 -> letter 'Q' (used for exit)
            break

finally:
    # Stop streaming
    pipeline.stop()