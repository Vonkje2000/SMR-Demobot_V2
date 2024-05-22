import os
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # هذا يخفي الرسائل الإعلامية والتحذيرات
logging.getLogger('tensorflow').setLevel(logging.FATAL)  # ضبط مستوى تسجيل TensorFlow على الأخطاء الفادحة فقط

from deepface import DeepFace
import cv2

# استخدام كاميرا الويب
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # قراءة الإطار من كاميرا الويب
    ret, frame = cap.read()
    if not ret:
        break
    
    # تحويل الصورة إلى تدرجات الرمادي
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # كشف الوجوه في الصورة
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # تحليل الصورة باستخدام DeepFace
    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    
    for (x, y, w, h) in faces:
        # استخراج المشاعر
        emotion = result[0]['dominant_emotion']
        
        # رسم دائرة حول الوجه
        center_coordinates = (x + w//2, y + h//2)
        radius = int(w / 1)
        color = (0, 255, 0)  # لون الدائرة أخضر
        thickness = 2
        cv2.circle(frame, center_coordinates, radius, color, thickness)
        
        # عرض الشعور المكتشف
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # عرض الإطار
    cv2.imshow('Emotion Detection', frame)
    
    # إنهاء التشغيل عند الضغط على المفتاح 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
