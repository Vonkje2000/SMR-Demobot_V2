import cv2
from ultralytics import YOLO

webcamera = cv2.VideoCapture(0)
webcamera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
webcamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
def gen_frames(model=None,detector=None): 
    while True:
        success, frame = webcamera.read()
        if not success:
            break
        else:
              # Object detection
            if model is not None:  
                frame = getFramesByModel(model,frame) 
            elif detector is not None:  
                frame =  detect_emotions(detector, frame)
            if frame is not None:
                # Encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                if not flag:
                    continue
                
                # Yield the output frame in byte format
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                    bytearray(encodedImage) + b'\r\n')
            else:
                continue     

    # webcamera.release()

def getFramesByModel(model, frame):
    """
    Processes a frame using the given model to detect objects.
    
    Args:
        model: The detection model used to process the frame.
        frame: A single frame from a video feed or image, as a NumPy array.
        
    Returns:
        The frame with detected objects plotted on it, or None if no results are found.
    """
    # Define constants for model parameters
    confidence_threshold = 0.65  # Confidence threshold for detection
    image_size = 480  # Image size for processing
    # target_class = 0  # Target class for detection
    verbose_mode = False  # Verbose mode for the model

    try:
        # Detect objects in the frame using the model
        results = model.track(frame, conf=confidence_threshold, imgsz=image_size, classes=0,  verbose=verbose_mode)
        if results:
            # Assuming results[0] exists and can be plotted
            return results[0].plot()  # Render the first result's plot on the frame
        else:
            print("No results to render")
            return None
    except Exception as e:
        print(f"Error during detection or rendering: {e}")
        return None


def detect_emotions(detector, frame):
    """
    Detects emotions on faces in a given frame using the provided detector.
    
    Args:
        detector: An emotion detector object with a `detect_emotions` method.
        frame: A single frame from a video feed or image, as a NumPy array.
        
    Returns:
        The frame with detected emotions and annotations drawn on it.
    """
    # Define constants for drawing
    circle_color = (0, 255, 0)  # Green color for the circle
    circle_thickness = 5  # Thickness of the circle border
    font_scale = 1  # Font scale for the text
    text_color = (0, 255, 0)  # Green color for the text
    text_thickness = 4  # Thickness of the text
    text_offset = 20  # Offset for the text position above the face
    circle_y_offset = 10  # Vertical offset for the circle position above the face center
    circle_radius_multiplier = 1.1  # Multiplier to increase the circle radius

    try:
        # Detect emotions in the frame
        result = detector.detect_emotions(frame)
        
        for face in result:
            # Extract face bounding box and emotion data
            (x, y, w, h) = face["box"]
            emotion = max(face["emotions"], key=face["emotions"].get)
            
            # Calculate center coordinates for the circle, slightly above the center
            center_coordinates = (x + w // 2, y + h // 2 - circle_y_offset)
            # Increase the radius by a defined multiplier
            radius = int(w * circle_radius_multiplier)
            
            # Draw a circle around the detected face
            cv2.circle(frame, center_coordinates, radius, circle_color, circle_thickness)
            # Annotate the detected emotion above the face
            cv2.putText(frame, emotion, (x, y - text_offset), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, text_thickness, cv2.LINE_AA)
        
        return frame
    
    except Exception as e:
        print(f"Error during emotion detection: {e}")
        return frame