import argparse
from roboflow import Roboflow


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='download_dataset.py')
    parser.add_argument('--api', type=str, help='the api key to access roboflow')
    opt = parser.parse_args()

    rf = Roboflow(api_key=opt.api)
    project = rf.workspace("object-detection-8kjqa").project("anpr_iran-car")
    dataset = project.version(1).download("yolov7")
