# Visual Question answering

Check out official webiste of [VisualQA](https://visualqa.org/)

Download the weight matrix of the 16 layer CNN model.
[vgg16_weights.h5](https://drive.google.com/file/d/0Bz7KyqmuGsilT0J5dmRCM0ROVHc/view)
 and put in src/model/dataset folder. Unable to put it here because of huge size :P


## Demo GIF

![Demo video](https://github.com/jai-singhal/visualqa/blob/master/demo.gif)

## Installation guide

1. Clone repository 

    `
    git clone https://github.com/jai-singhal/visualqa
    `
2. cd to repository.

3. Create a virtualenv by following command

    ` virtualenv -p python3 .
    `

4. Activate virtualenv 

    `
    source bin/activate
    `

5. Install required packages 

    `
    pip3 install -r requirements.txt
    `
    
    Note that you may find difficulty while installing spacy, this guide is for linux/mac only.
    For windows users, please download cpp build tools.

    And spacy models.
    `
    python3 -m spacy download en-core-web-sm==2.0.0
    `

    `
    python3 -m spacy download en-vectors-web-lg==2.1.0
    `

6. cd to src and run the server 

    `
    python3 manage.py runserver
    `
