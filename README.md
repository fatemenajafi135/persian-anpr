# Automatic Number Plate Recognizition for Iranian(Persian) plates 


## **License plate detection**

**Install requirements**

``` shell
pip install -r requirements.txt (--use-feature=2020-resolver)
```

**dataset**

I used two datasets ([car plate dataset](https://www.kaggle.com/datasets/andrewmvd/car-plate-detection) and [Iranian car number plate](https://www.kaggle.com/datasets/skhalili/iraniancarnumberplate)) for transfer learning the YOLOv7 to detect car license plates. As I wantet better performance on Iranian license plates, during spliting the whole dataset, I set splits *ratio for train/validation/test* of the Iranian dataset to 70/15/15 and the other dataset to 75/25/0. I used flip horizontal, rotation (-10° to +10°), shear (±10° to ±10°), and noise(5%) for *augmentation*.  

Add the [new dataset](https://universe.roboflow.com/object-detection-8kjqa/anpr_iran-car/dataset/1) from roboflow for training or fune-tuning using your specific API key. The car license plate dataset will be placed at ```./ANPR_Iran-car-1```. 

``` shell
run download_dataset.py --api [YOUR SPECIFIC API KEY]
```


**download the base model weights of YOLOv7**

``` shell
wget -P ./weights https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt
```

**transfer learning for license plate detection**

 train model:

``` shell
python train.py --epochs 50 --workers 8 --device 0 --batch-size 16 --data ANPR_Iran-car-1/data.yaml --img 640 640 --cfg cfg/training/yolov7.yaml --weights 'yolov7.pt' --name yolov7-license --hyp data/hyp.scratch.custom.yaml
```

or download the best model I have trained for car lisense plate detection:

``` shell
cd weights
gdown 1fsf3T_u3wvPJQJDTMi8LfVdCxIUUA34S
cd ..
``` 

detect license plates for the testset using model:
‍‍‍‍‍‍
``` shell
python detect.py --weights [PATH TO WEIGHTS (.pt file)] --conf 0.1 --source [PATH TO A DIRECTORY OR A SINGLE IMAGE TO DETECT]
# example using my model 
python detect.py --weights weights/best.pt --conf 0.2 --source ./ANPR_Iran-car-1/test/images
```

Results will be placed on ```runs/detect/exp*```.


## **ocr**

[More on OCR ...](https://github.com/fatemenajafi135/persian-anpr/tree/main/ocr)


## **Wrap up for license plate recognition**

**using easyocr**

change ```[...]``` in line *78* on file ```utils/plots.py``` to the *direct* path of ```Yekan.ttf``` on your system.

``` shell
python anpr.py --path2detect [PATH OF FILES] --detecttype [FILE TYPE] --imagename [IMAGE NAME] --videoname [VIDEO NAME] --weights weights/best.pt --savepath runs/recognize  --device cpu --imagesize 640
#Example
python anpr.py --path2detect ./to_detect --detecttype image --imagename plate.jpg
```



## **YOLOv7**

More about [YOLO7](https://github.com/WongKinYiu/yolov7/blob/main/README.md) 
