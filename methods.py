import cv2
import numpy as np
import face_recognition
from ast import literal_eval
import pickle
from array import array
import json
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/attendancePage', methods = ['GET', 'POST'])
def land_attendance():
    return render_template("attend.html")

@app.route('/register', methods=['POST'])
def register():
    try:
        roll = request.form['inputRoll']
        name = request.form['inputName']
        
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Hit Spacebar to click a picture")
        img_person = f"{str(roll)}_{str(name)}"

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Hit Spacebar to click a picture", frame)
            
            k = cv2.waitKey(1)
            if k % 256 == 27:
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = "static/{}.jpg".format(img_person)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                break  
        cam.release()
        cv2.destroyAllWindows()

        subject_image = face_recognition.load_image_file(f"static/{img_person}.jpg")
        subject_face_encoding = face_recognition.face_encodings(subject_image)[0]
        
        known_face_encodings = []
        known_face_names = []
        
        try:
            # with open('known_face_encodings.txt', 'r') as file:
            #     known_face_encodings = literal_eval(file.read())
            # with open('known_face_names.txt', 'r') as file:
            #     known_face_names = literal_eval(file.read())
            file = open('known_face_encodings.p', 'rb')
            known_face_encodings = pickle.load(file)
            file.close()
            
            file = open('known_face_names.p', 'rb')
            known_face_names = pickle.load(file)
            file.close()
            
        except:
            pass
        
        known_face_encodings.append(subject_face_encoding)
        known_face_names.append(img_person)
        # print(known_face_encodings)
        # print(known_face_names)
        
        # with open('known_face_encodings.txt', 'w') as file:
        #     file.write(str(known_face_encodings))
        # with open('known_face_names.txt', 'w') as file:
        #     file.write(str(known_face_names))
        
        file = open('known_face_encodings.p', 'wb')
        pickle.dump(known_face_encodings, file)
        file.close()
        
        file = open('known_face_names.p', 'wb')
        pickle.dump(known_face_names, file)
        file.close()
        
        confirm_str = ""
        with open('templates/confirm.html', 'r') as file:
            confirm_str = file.read()
        confirm_str = confirm_str.replace("{person_image}", f"static/{img_person}.jpg")
        confirm_str = confirm_str.replace("{roll_number}", roll)
        confirm_str = confirm_str.replace("{name}", name)
        
        with open('templates/confirm_final.html', 'w') as file:
            file.write(confirm_str)
        
        return render_template("confirm_final.html")
    except:
        ver_str = ""
        with open('templates/verified.html', 'r') as file:
            ver_str = file.read()
            
        ver_str = ver_str.replace("Hi{name}, <br>Your attendance {ver_status}.", "Face not clearly visible. Please retake the picture.")
            
        with open('templates/verified_final.html', 'w') as file:
            file.write(ver_str)
        return render_template("verified_final.html")
    

@app.route('/attend', methods=['POST'])
def attend():
    try:
        roll = request.form['inputRoll']
        
        known_face_encodings = []
        known_face_names = []
        
        # with open('known_face_encodings.txt', 'r') as file:
        #     known_face_encodings = literal_eval(file.read())
        # with open('known_face_names.txt', 'r') as file:
        #     known_face_names = literal_eval(file.read())
        file = open('known_face_encodings.p', 'rb')
        known_face_encodings = pickle.load(file)
        file.close()
            
        file = open('known_face_names.p', 'rb')
        known_face_names = pickle.load(file)
        file.close()
            
        video_capture = cv2.VideoCapture(0)
        
        final_name = ""
            
        while True:
            ret, frame = video_capture.read()

            rgb_frame = frame

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "Unknown"
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if str(roll) == str(name.split("_")[0]):
                        # print("Attendance Done!")
                        final_name = name
                    
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
            cv2.imshow('Press q to mark attendance', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        video_capture.release()
        cv2.destroyAllWindows()
        
        if final_name == "":
            ver_str = ""
            with open('templates/verified.html', 'r') as file:
                ver_str = file.read()
            
            ver_str = ver_str.replace("{name}", "")
            ver_str = ver_str.replace("{ver_status}", "could not be verified")
            
            with open('templates/verified_final.html', 'w') as file:
                file.write(ver_str)
            return render_template("verified_final.html")
        else:
            ver_str = ""
            with open('templates/verified.html', 'r') as file:
                ver_str = file.read()
            
            name = name.replace("_", " - ")
            ver_str = ver_str.replace("{name}", " " + final_name.split("_")[1])
            ver_str = ver_str.replace("{ver_status}", "has been successsfuly verified")
            
            with open('templates/verified_final.html', 'w') as file:
                file.write(ver_str)
            return render_template("verified_final.html")
        
    except:
        ver_str = ""
        with open('templates/verified.html', 'r') as file:
            ver_str = file.read()
            
        ver_str = ver_str.replace("Hi{name}, <br>Your attendance {ver_status}.", "Sorry, no faces registered in database.")
            
        with open('templates/verified_final.html', 'w') as file:
            file.write(ver_str)
        return render_template("verified_final.html")

if __name__ == "__main__":
    app.run(debug=True)