# **Optical Character Recognition (OCR)**

I tried some techniques for OCR. (None of them have made me satisfied yet.)

## Using Python Packages for OCR 

There are many packages for OCR like "*easyocr*", "*pytesseract*", and "*paddleocr*". Although all of them support Persian, none of them performs well on Persian texts and license plates even after croping the plate part. 

<br/>

## Training simple OCR

Considering text recognition as an image classification task (because place of each character is pre-defined), I train a simple Neural Networkk for classify each letter on the plate. The train set has about 8.3k instances. This model doesn't perform well on plates either. 
- **Dataset**: A dataset of Persian letters and digits is needed (Like mnist dataset). It can be accessed [here](https://universe.roboflow.com/object-detection-yolov5/plate_ocr_ir/dataset/2).
- **Model**: A simple model with an architecture of one flatten and two dense layers trained on the dataset. You can train model:
``` shell 
cd ocr
python simple_model.py
```
or use the best I've trained [here](https://drive.google.com/drive/folders/1xymW4gxmImUNHEwbei2flIKO8nH66L9k).

<br/>

## Training OCR using CRNN algorithm and PaddlePaddle

[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) is an awesome multilingual OCR toolkits based on [PaddlePaddle](https://github.com/PaddlePaddle) (practical ultra lightweight OCR system, support 80+ languages recognition, provide data annotation and synthesis tools, support training and deployment among server, mobile, embedded and IoT devices). I will implement the *text recognition* part using [PaddleOCR's doc for text recognition](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/recognition_en.md).


- **Dataset**:
 I generate artificial number plates using [this repository](https://github.com/amirmgh1375/iranian-license-plate-recognition). It generated with a "simple dataset" format, defined in paddleocr repo. You can download it [here](https://drive.google.com/drive/folders/1Euiupm8Fk8YCt0gQCwfzIQmI9UPuZ8mw). 

- **Model**: In process...
