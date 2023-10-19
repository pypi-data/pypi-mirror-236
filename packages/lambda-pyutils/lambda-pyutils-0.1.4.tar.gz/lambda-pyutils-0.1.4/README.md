# Python utility library for machine learning

## Opencv

### Dnn based face detector:  

Example usage:
```
from pyutils.cvfacedetector.facedetector import FaceDetector
faceDetector = FaceDetector(confidence=0.6) # pass optional confidence

results = faceDetector.detectFaces(img) # returns list of (face, box) for each detected face
for face, box, confidence in results:
    print('face', face.shape)
    print('box', box)
    print('confidence', confidence)

> face (235, 235, 3)
> box [73, 105, 235, 235]
> confidence 0.9877282
```  

## Building and publishing the build
```
# create virtual environment
python -m virtualenv venv
./venv/scripts/activate.ps1 (or source in linux)
pip install -r requirements.txt
python -m build

# upload to test.pypi.org   
python -m twine upload --repository testpypi dist/*

# upload to pypi.org
python -m twine upload dist/*

```


## Installing the package
From test.pypi.org:  
`pip install -i https://test.pypi.org/simple/ lambda-pyutils`    

From pypi.org:  
`pip install lambda-pyutils`