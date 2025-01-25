from datetime import datetime
import time

import cv2
import yt_dlp

# 4 Corners Camera - downtown Coldwater, MI, USA
url = "https://www.youtube.com/watch?v=ByED80IKdIU"

# Extract video information using yt-dlp
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    # Select the best video format
    formats = info['formats']
    best_format = max(formats, key=lambda f: f.get('height', 0))
    stream_url = best_format['url']
    # Get the YouTube stream FPS (usually fixed)
    youtube_fps = best_format['fps']

# Open video stream with OpenCV
cap = cv2.VideoCapture(stream_url)

frame_count = 0
start_time = time.time()

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Calculate current FPS (frames per second)
    current_fps = frame_count / (time.time() - start_time)

    # Get current time in local time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # TODO get youtube camera's time

    # Text lines to display
    text_lines = [
        f"Frame Count: {frame_count}",
        f"Script FPS: {current_fps:.2f}",
        f"YouTube FPS: {int(youtube_fps)}",
        f"Time: {current_time}"
    ]

    # Position for text
    y_offset = 30

    # Add each line of text
    for line in text_lines:
        cv2.putText(frame, line, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        y_offset += 30

    # Example: Display the frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
