# import cv2
# import numpy as np

# cam = cv2.VideoCapture(0)

# cv2.namedWindow("Hit Spacebar to click a picture")

# img_person = "b"

# while True:
#     ret, frame = cam.read()
#     if not ret:
#         print("failed to grab frame")
#         break
#     cv2.imshow("Hit Spacebar to click a picture", frame)
    
#     k = cv2.waitKey(1)
#     if k%256 == 27:
#         # ESC pressed
#         print("Escape hit, closing...")
#         break
#     elif k%256 == 32:
#         # SPACE pressed
#         img_name = "{}.jpg".format(img_person)
#         cv2.imwrite(img_name, frame)
#         print("{} written!".format(img_name))
#         break
        
# cam.release()
# cv2.destroyAllWindows()
# arr = ""
# with open('known_face_encodings.txt', "r") as file:
#     arr = eval(file.read())

# print(arr)
# print(type(arr))

# arr.append("Snagnik")

# with open('known_face_encodings.txt', "w") as file:
#     file.write(str(arr))
from array import array


print(la)