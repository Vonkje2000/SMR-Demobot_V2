import cv2
from ultralytics import YOLO

# 1. Laad het YOLOv8-model
model = YOLO('best.pt')  # Vervang door het pad naar je YOLOv8-model

# 2. Open de webcam
cap = cv2.VideoCapture(0)  # Gebruik 0 voor de standaard webcam. Pas aan voor andere camera's.

if not cap.isOpened():
    print("Kan de webcam niet openen!")
    exit()

# 3. Real-time voorspellingen uitvoeren
while True:
    ret, frame = cap.read()
    if not ret:
        print("Kon geen frame ophalen. Exiting...")
        break

    # Gebruik YOLOv8 om voorspellingen te maken op het frame
    results = model.predict(source=frame, conf=0.25, save=False, show=False)

    # Zoek de hoogste confidence box
    best_box = None
    best_conf = 0

    for result in results:
        for box in result.boxes:
            conf = box.conf[0]  # Confidence score
            if conf > best_conf:  # Update als deze box beter is
                best_conf = conf
                best_box = box

    # Als er een geldige box is, teken deze
    if best_box is not None and best_conf >= 0.5:  # Alleen als confidence >= 0.5
        x1, y1, x2, y2 = map(int, best_box.xyxy[0])  # Coördinaten van de box
        cls = best_box.cls[0]                        # Class label index
        label = f"{model.names[int(cls)]} {best_conf:.2f}"  # Label met klasse en confidence
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Groene box
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Print alleen de class label naar de terminal
        print(f"Detected: {model.names[int(cls)]}")

    # Toon het frame in een venster
    cv2.imshow("YOLOv8 Webcam", frame)

    # Sluit het venster met 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 4. Webcam en vensters afsluiten
cap.release()
cv2.destroyAllWindows()
