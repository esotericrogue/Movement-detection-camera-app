import cv2
import time
from datetime import datetime
from emailing import send_email
import glob

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count= 1

while True:
    now = str(datetime.now().strftime("%A %d/%m/%y %H:%M:%S"))

    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    cv2.putText(img=frame, text=now, org= (50, 50),
                fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                color=(20, 110, 220), thickness=2, lineType=cv2.LINE_AA)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 60,255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", thresh_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email()

    cv2.imshow("video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()