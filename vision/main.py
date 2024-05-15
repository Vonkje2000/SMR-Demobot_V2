import cv2
from ultralytics import YOLO


def gen_frames(model): 
    webcam = cv2.VideoCapture(0)
    while True:
        success, frame = webcam.read()
        if not success:
            break
        else:
              # Object detection
            try:
                results = model.track(frame, conf=0.65, imgsz=480, classes=0, verbose=False)
                if results:
                    # Assuming results[0] exists and can be plotted
                    frame = results[0].plot()  # Render the first result's plot on the frame
                else:
                    print("No results to render")
                    continue
            except Exception as e:
                print(f"Error during detection or rendering: {e}")
                continue  # Skip this frame

            # Encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            
            # Yield the output frame in byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                  bytearray(encodedImage) + b'\r\n')
    
    webcam.release()

