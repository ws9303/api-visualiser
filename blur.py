import os
import argparse
import sys

import cv2
import mediapipe as mp

output_dir = './uploads/blur'

def process_img(img, face_detection):

    H, W, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x1 = int(x1 * W)
            y1 = int(y1 * H)
            w = int(w * W)
            h = int(h * H)

            # print(x1, y1, w, h)

            # blur faces
            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w, :], (30, 30))

    return img

# detect faces

def blur_video(filePath):
    mp_face_detection = mp.solutions.face_detection
    filename = os.path.basename(filePath)

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:

        cap = cv2.VideoCapture(filePath)
        ret, frame = cap.read()

        output_video = cv2.VideoWriter(os.path.join(output_dir, filename),
                                        cv2.VideoWriter_fourcc(*'MP4V'),
                                        25,
                                        (frame.shape[1], frame.shape[0]))

        while ret:

            frame = process_img(frame, face_detection)

            output_video.write(frame)

            ret, frame = cap.read()

        cap.release()
        output_video.release()
        
if __name__ == "__main__":
    argument = sys.argv
    blur_video(argument[1])