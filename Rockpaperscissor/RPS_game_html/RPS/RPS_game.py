import cv2
from ultralytics import YOLO
import time

# Laad het model met logging uitgeschakeld
model = YOLO('best.pt', verbose=False)

# Open de webcam
cap = cv2.VideoCapture(0)  # Pas de camerabron aan indien nodig

if not cap.isOpened():
    print("Kan de webcam niet openen!")
    exit()

# Functie om de schuifbalk te gebruiken
def nothing(x):
    pass

# Maak een venster en schuifbalken voor parameters
cv2.namedWindow("Parameters")
cv2.createTrackbar("Brightness", "Parameters", 50, 100, nothing)
cv2.createTrackbar("Contrast", "Parameters", 50, 100, nothing)
cv2.createTrackbar("Confidence", "Parameters", 25, 100, nothing)  # In % (0-100)
cv2.createTrackbar("Blur", "Parameters", 0, 20, nothing)  # Gauss-blur kern (0=geen blur)
cv2.createTrackbar("Color Mode", "Parameters", 0, 2, nothing)  # 0=BGR, 1=HSV, 2=Grayscale
cv2.createTrackbar("Min Size", "Parameters", 0, 200, nothing)  # Minimale boxgrootte
cv2.createTrackbar("Rotation", "Parameters", 0, 360, nothing)  # Rotatiehoek

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kon geen frame ophalen. Exiting...")
        break

    # Haal schuifbalkwaarden op
    brightness = cv2.getTrackbarPos("Brightness", "Parameters") - 50
    contrast = cv2.getTrackbarPos("Contrast", "Parameters") - 50
    conf_threshold = cv2.getTrackbarPos("Confidence", "Parameters") / 100.0
    blur_level = cv2.getTrackbarPos("Blur", "Parameters")
    color_mode = cv2.getTrackbarPos("Color Mode", "Parameters")
    min_size = cv2.getTrackbarPos("Min Size", "Parameters")
    rotation_angle = cv2.getTrackbarPos("Rotation", "Parameters")

    # Pas helderheid en contrast aan
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=1 + contrast / 50.0, beta=brightness)

    # Pas blur toe
    if blur_level > 0:
        ksize = blur_level if blur_level % 2 == 1 else blur_level + 1  # Kern moet oneven zijn
        adjusted_frame = cv2.GaussianBlur(adjusted_frame, (ksize, ksize), 0)

    # Verander kleurmodus
    if color_mode == 1:
        adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2HSV)
    elif color_mode == 2:
        gray_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2GRAY)
        adjusted_frame = cv2.merge([gray_frame, gray_frame, gray_frame])

    # Draai het frame
    h, w = adjusted_frame.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1)
    adjusted_frame = cv2.warpAffine(adjusted_frame, rotation_matrix, (w, h))

    # Voorspellingen uitvoeren met YOLO
    results = model.predict(source=adjusted_frame, conf=conf_threshold, save=False, show=False)

    # Zoek het object met de hoogste confidence
    best_box = None
    best_conf = 0
    resultaat = None  # Variabele om het resultaat bij te houden

    for result in results:
        for box in result.boxes:
            conf = box.conf[0]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            box_size = (x2 - x1) * (y2 - y1)

            # Controleer op minimale grootte en hoogste confidence
            if conf > best_conf and box_size > min_size:
                best_conf = conf
                best_box = (x1, y1, x2, y2, box.cls[0])

    # Teken alleen de beste box en geef de output als er detecties zijn
    if best_box is not None:
        x1, y1, x2, y2, cls = best_box
        label = f"{model.names[int(cls)]} {best_conf:.2f}"
        cv2.rectangle(adjusted_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(adjusted_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Detected: {model.names[int(cls)]} with confidence {best_conf:.2f}")

        # Koppel resultaat aan variabele
        if model.names[int(cls)] == "Rock":
            resultaat = 'rock'
        elif model.names[int(cls)] == "Paper":
            resultaat = 'paper'
        elif model.names[int(cls)] == "Scissors":
            resultaat = 'scissors'

    # Print resultaat in de terminal
    if resultaat is not None:
        print(f"Resultaat: {resultaat}")
        

    # Toon het frame
    cv2.imshow("YOLOv8 Webcam", adjusted_frame)

    # Verlaat met 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Resources vrijgeven
cap.release()
cv2.destroyAllWindows()
