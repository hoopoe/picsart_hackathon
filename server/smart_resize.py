import dlib
import cv2

def rect_to_tuple(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def face_pos(im, upsample=1):
    face_detector = dlib.get_frontal_face_detector()
    faces = face_detector(im, upsample)
    return faces[0] if len(faces) > 0 else 0

def resize(im):
    pos = face_pos(im, 1)
    if pos == 0:
        return im
    pos = rect_to_tuple(face_pos(im, 1))
    face_area = (pos[2] - pos[0]) * (pos[1] - pos[3])
    if face_area > 38400:
        im = cv2.resize(im, (0, 0), fx=0.5, fy=0.5)
        pos = rect_to_tuple(face_pos(im, 2))

    face_center = (int((pos[1] + pos[3])/2), int((pos[2] + pos[0])/2))
    crop_coords = (max(face_center[0]-120, 0), max(face_center[1]-160,0))
    im_croped = im[crop_coords[1]:crop_coords[1]+320,crop_coords[0]:crop_coords[0]+240]
    return im_croped
