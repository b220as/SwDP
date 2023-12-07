# 認識した輪郭を28*28にしてMNISTできるようにする

import cv2
import numpy as np
from sklearn import svm
import pickle

# 学習済モデルの読み込み
clf = svm.SVC(gamma=0.001)
with open('trained_model.pkl', 'rb') as f:
    clf = pickle.load(f)

THRESH_MIN_AREA = 25
THRESH_MAX_AREA = 80

img = cv2.imread('page_1.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, img_obj = cv2.threshold(cv2.bitwise_not(gray), 0, 255, cv2.THRESH_OTSU)

contours, _ = cv2.findContours(img_obj, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    area = cv2.contourArea(contour)
    if THRESH_MIN_AREA < area < THRESH_MAX_AREA:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect

        # 対象領域を切り取り
        cropped_img = img[y:y + h, x:x + w]

        # 1チャンネルに変換
        cropped_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

        # 28x28にリサイズ
        max_dim = max(cropped_gray.shape[0], cropped_gray.shape[1])
        resized_img = np.zeros((max_dim, max_dim), dtype=np.uint8)
        start_x = (max_dim - cropped_gray.shape[1]) // 2
        start_y = (max_dim - cropped_gray.shape[0]) // 2
        resized_img[start_y:start_y + cropped_gray.shape[0], start_x:start_x + cropped_gray.shape[1]] = cropped_gray

        resized_img = cv2.resize(resized_img, (28, 28))

        # 識別の実行（SVCを使って予測）
        predicted = clf.predict(resized_img.reshape(1, -1))

        print("Prediction:", predicted)

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 10)

# save
cv2.imwrite('digits_boundingbox.jpg', img)
