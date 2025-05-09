from datetime import datetime
import time

import cv2
import pytz
import yt_dlp

from car_detector import CarDetector


def get_youtube_stream_url(url):
    """Extract the best stream URL from the YouTube video.
    TODO separate the rest of the code
        from this youtube function."""
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info["formats"]
        best_format = max(formats, key=lambda f: f.get("height", 0))
        stream_url = best_format["url"]
        fps = best_format["fps"]
        res = best_format["resolution"]
        print(f"YouTube FPS: {fps}, resolution: {res}")
        return stream_url


def add_text_to_frame(frame, text_lines):
    """Add lines of text to the frame.
    TODO move to some utils functions."""
    y_offset = 30
    for line in text_lines:
        cv2.putText(
            frame,
            line,
            (10, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )
        y_offset += 30


def main():
    # TODO refactor the main function
    detector = CarDetector()

    # 4 Corners Camera - downtown Coldwater, MI, USA
    url = "https://www.youtube.com/watch?v=ByED80IKdIU"
    camera_tz = pytz.timezone('America/Detroit')

    stream_url = get_youtube_stream_url(url)

    # Open video stream with OpenCV
    cap = cv2.VideoCapture(stream_url)

    frame_count = 0
    start_time = time.time()

    # Process each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detected_frame = detector.detect_cars(frame)
        cv2.imshow("Car Detection", detected_frame)

        # TODO the whole frame counting and editing block may be extracted as a function
        frame_count += 1
        # Calculate current FPS (frames per second)
        current_fps = frame_count / (time.time() - start_time)
        current_time = datetime.now(camera_tz).strftime("%Y-%m-%d %H:%M:%S")
        text_lines = [
            f"{current_time}",
            f"Frame Count: {frame_count}",
            f"Script FPS: {current_fps:.2f}"
        ]
        add_text_to_frame(detected_frame, text_lines)

        cv2.imshow("Frame", detected_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
