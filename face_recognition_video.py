import face_recognition
import cv2
import pyttsx3;

#text to speech
engine = pyttsx3.init();

def speakText(textToSpeak):
	engine.say(textToSpeak);
	engine.runAndWait() ;
video_show=True
# SET FALSE IF RUNNING IN RASPBERRY PI


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
if (video_capture.isOpened() == False): 
  print("Unable to read camera feed")
else:
    print("Passed video capture initialization")

image_size = 128
# Load a sample picture and learn how to recognize it.
william_image = face_recognition.load_image_file("known_people/William.jpg")
x_scale = y_scale = 128/william_image.shape[0]
william_image = cv2.resize(william_image, (0,0), fx=x_scale, fy=y_scale)
william_face_encoding = face_recognition.face_encodings(william_image)[0]

# Load a second sample picture and learn how to recognize it.
kout_image = face_recognition.load_image_file("known_people/Kout.jpg")
x_scale = y_scale = 128/kout_image.shape[0]
kout_image = cv2.resize(kout_image, (0,0), fx=x_scale, fy=y_scale)
kout_face_encoding = face_recognition.face_encodings(kout_image)[0]


# Load a third sample picture and learn how to recognize it.
leandra_image = face_recognition.load_image_file("known_people/Leandra.jpg")
x_scale = y_scale = 128/leandra_image.shape[0]
leandra_image = cv2.resize(leandra_image, (0,0), fx=x_scale, fy=y_scale)
leandra_face_encoding = face_recognition.face_encodings(leandra_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    william_face_encoding,
    kout_face_encoding,
    leandra_face_encoding
]
known_face_names = [
    "William",
    "Dimitrios",
    "Leandra"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


lastMatchedPerson = None
frame_counter = 0
people_found = []
video_scale = 0.2
while True:
    if frame_counter >= 50:
        frame_counter=0
        people_found = []
    frame_counter+=1
    print(frame_counter)
    #print("Entered while loop")
    # Grab a single frame of video
    ret, frame = video_capture.read()

    #apply frame rotation
    frame=cv2.transpose(frame)
    frame=cv2.flip(frame,flipCode=0)




    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0,0), fx=video_scale, fy=video_scale)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            print("found face")
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                #if reading first everytime, how does it go on to 2nd, and 3rd person in frame?
                # print("Face locations: ",face_locations)
                face_names.append(name)
                if name not in people_found:
                    center_x=0.5*(face_locations[face_names.index(name)][3]+face_locations[face_names.index(name)][1])
                    frame_third = rgb_small_frame.shape[1]/3
                    if center_x < frame_third:
                        relative_location = " to the left"
                    elif center_x > frame_third and center_x < 2*frame_third:
                        relative_location = "ahead"
                    elif center_x > 2*frame_third:
                        relative_location = "to the right"

                    speakText(name + " is " + relative_location + " of you")
                    print("This is "+name)
                    people_found.append(name)

    process_this_frame = frame_counter%2==1


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= int(1/video_scale)
        right *= int(1/video_scale)
        bottom *= int(1/video_scale)
        left *= int(1/video_scale)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    if video_show == True:
        cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
#cv2.destroyAllWindows()