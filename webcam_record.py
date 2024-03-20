import cv2
import os
from datetime import datetime,time

# Parameters to change
output_dir = r'E:\jorbanicus\Werk9.0 - Webcam Record and Save'
start_time = time(7, 00)  
end_time = time(8, 00)  
# Parameters to change

output_filename = 'output.mp4'
output_path = os.path.join(output_dir, output_filename)

if not os.path.isdir(output_dir):
    print(f"Output directory {output_dir} does not exist.")
    exit(1)

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
height, width = frame.shape[:2]
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# Check if camera opened successfully
if not cap.isOpened(): 
    print("Unable to read camera feed")
    exit(1)

# Define the codec using VideoWriter_fourcc and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(f'{output_dir}/output_{timestamp}.mp4', fourcc, 20.0, (height, width))

# Create a named window
cv2.namedWindow('Camera Input', cv2.WINDOW_NORMAL)

# Resize the window to specific width and height
cv2.resizeWindow('Camera Input', 352, 640)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Get the current time and draw it on the frame
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Draw a white rectangle
        cv2.rectangle(frame, (0, frame.shape[0] - 20), (200, frame.shape[0]), (255, 255, 255), -1)
        
        # Draw black text on the white rectangle
        cv2.putText(frame, timestamp, (10, frame.shape[0] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Check if the current time is within the desired range
        current_time = datetime.now().time()
        if start_time <= current_time <= end_time:
            # Write the frame into the file
            out.write(frame)

        # Display the resulting frame
        cv2.imshow('Camera Input', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the capture, writer and destroy the window
cap.release()
out.release()
cv2.destroyAllWindows()