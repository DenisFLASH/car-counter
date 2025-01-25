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

# Open video stream with OpenCV
cap = cv2.VideoCapture(stream_url)

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Example: Display the frame
    cv2.imshow('Frame', frame)

    # Perform video analytics (replace this with your logic)
    # For example, converting frame to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Show the processed frame
    # cv2.imshow('Processed Frame', gray)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
