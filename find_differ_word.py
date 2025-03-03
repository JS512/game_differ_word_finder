from google.cloud import vision
import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui


def find_differ(arr) :
    arr2 = [0 for i in range(len(arr))]
    
    if all(item in arr for item in ["단계", "도전", "하기"]) :
        return arr.index("도전"), True
    
    for idx, val in enumerate(arr) :        
        for idx2, val2 in enumerate(arr) :            
            if val != val2 :
                arr2[idx] -= 1
    
                
    return arr2.index(min(arr2)), False
            
def detect_text(img):
    """Detects text in the file."""
    from google.cloud import vision

    # with open(path, "rb") as image_file:
    #     content = image_file.read()

    image = vision.Image(content=img)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")
    rs_texts = []
    vertices = []
    for text in texts:
        print(f'\n"{text.description}"')

        # vertices.append( (text.bounding_poly.vertices[0].x,text.bounding_poly.vertices[0].y))
        # vertices = [
        #     ({vertex.x},{vertex.y}) for vertex in text.bounding_poly.vertices
        # ]
        if text.locale == "" :
            rs_texts.append(text.description)
            vertices.append( (text.bounding_poly.vertices[0].x,text.bounding_poly.vertices[0].y))
        else :
            nlines = len(text.description.splitlines())
            if nlines < 4 :
                return
            
        # print("bounds: {}".format(",".join(vertices)))

    idx, next = find_differ(rs_texts)
    
    
    x = vertices[idx][0]
    y = vertices[idx][1] + 300
    
    pyautogui.click(x, y)
    
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    # if next :
    

def screenshot_to_bytes(sc) :
    # 바이트 데이터로 변환
    img = Image.frombytes("RGB", sc.size, sc.rgb)
    img_bytes_io = io.BytesIO()
    img.save(img_bytes_io, format="PNG")  # PNG, JPEG 등 원하는 포맷 지정 가능
    img_bytes = img_bytes_io.getvalue()  # 바이트 데이터로 변환
    return img_bytes

if __name__ == '__main__':
    import io, time
    client = vision.ImageAnnotatorClient()
    bounding_box = {'top': 300, 'left': 0, 'width': 450, 'height': 650}

    sct = mss()

    # while True:
    while True :
        sct_img = sct.grab(bounding_box)
        
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # 1. 이미지를 흑백으로 변환
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Threshold 적용
        # threshold는 2개의 값을 인자로 받습니다: 임계값, 임계값을 넘은 픽셀은 최대값으로 설정
        # 예를 들어, 임계값 127을 넘는 값은 255(흰색)으로 설정하고, 그 이하 값은 0(검정)으로 설정합니다.
        # ret, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
        # # cv2.imshow('Original Grayscale Image', gray_image)
        # cv2.imshow('Thresholded Image', thresh_image)
        # cv2.waitKey(0)
        # if (cv2.waitKey(1) & 0xFF) == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
        
        # success, encoded_image = cv2.imencode('.png', thresh_image)

        # # 이미지가 성공적으로 인코딩되었으면, bytearray로 변환
        # if success:
        #     byte_data = encoded_image.tobytes()
        detect_text(screenshot_to_bytes(sct_img))
        time.sleep(1)
