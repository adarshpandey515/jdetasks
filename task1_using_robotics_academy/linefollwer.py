import GUI
import HAL
import numpy as np
import cv2

# Boundaries for detecting red color
boundaries = [
    ([0, 10, 90], [60, 76, 220])  # Red range in BGR
]

# Robot constants
VELOCITY = 6  # Adjust this as needed (linear velocity)
TURN_SPEED = 3 # Angular speed (adjust based on testing)

# Loop to keep reading images and processing
while True:
    image = HAL.getImage()  # Capture the image (BGR8)
    
    # Convert BGR to HSV for more accurate color detection (optional)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    for lower, upper in boundaries:
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        
        # Mask the red colors
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # Find contours to get the center of mass (the red line)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get the center of the contour (centroid)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])  # X coordinate of centroid
                cY = int(M["m01"] / M["m00"])  # Y coordinate of centroid
                
                # Draw a circle at the center of the red line (for debugging)
                cv2.circle(output, (cX, cY), 5, (0, 255, 0), -1)
                
                # Calculate the deviation from the center of the image
                height, width = image.shape[:2]
                center_x = width // 2  # Center of the image
                error = cX - center_x  # Horizontal error
                
                # Adjust angular velocity based on the error (line deviation)
                angular_velocity = -TURN_SPEED * error / center_x  # Normalize the error
                
                # Set linear velocity (constant for line-following)
                HAL.setV(VELOCITY)
                HAL.setW(angular_velocity)
                
                # Show the output
                GUI.showImage(np.hstack([image, output]))

            else:
                # If no contour found (robot is lost), stop or search
                HAL.setV(0)
                HAL.setW(0)
                GUI.showImage(image)
        else:
            # If no red line is detected, stop the robot or search for the line
            HAL.setV(0)
            HAL.setW(0)
            GUI.showImage(image)
