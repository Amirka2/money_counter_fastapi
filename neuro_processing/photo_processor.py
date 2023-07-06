from ultralytics import YOLO
# result.plot() - нарисовать квадраты
import cv2
from darknetpy.detector import Detector


model = YOLO('detector.pt')
unprocessed_photo_folder = './photos/unprocessed/'
processed_photo_folder = './photos/processed/'

net = Detector('path/to/config.cfg', 'path/to/weights.weights', 0, 'path/to/names.names')


image = cv2.imread('path/to/image.jpg')

results = net.detect(image)

for cat, score, bounds in results:
    x, y, w, h = bounds
    cv2.rectangle(image, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), 2)
    cv2.putText(image, cat.decode(), (int(x - w / 2), int(y - h / 2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)


cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()



def process_photo(photo_name: str):
    summ = 0
    items_path = detect_items(photo_name)
    items = cut_items(items_path)
    for i in items:
        summ += classify_item(i)

    return summ


def detect_items(photo_name: str):
    results = model([f'{unprocessed_photo_folder}{photo_name}'])
    print('!')

    return 0
    # os.system('cmd /k "yolo task=detect mode=predict '
    #           'model=/detector.pt '
    #           f'source={unprocessed_photo_folder}{photo_name} '
    #           'show=True imgsz=640 '
    #           f'name={processed_photo_folder}{photo_name} '
    #           'hide_labels=False"')
    # return processed_photo_folder + photo_name


def cut_items(photo_path: str):
    return '1'


def classify_item(item_path: str):
    pass
