
import numpy as np
import torch
from PIL import Image

import sys
import os
# 丑陋至极
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Siamese_pytorch')))

from Siamese_pytorch.nets.siamese import Siamese as siamese
from Siamese_pytorch.utils.utils import letterbox_image, preprocess_input, cvtColor

class Siamese(object):

    def __init__(self, **kwargs):
        
        device  = torch.device('cpu')
        model   = siamese([105, 105])
        model.load_state_dict(torch.load("models/siamese.pth", map_location=device))
        self.net = model.eval()

    
    def letterbox_image(self, image, size):

        image   = image.convert("RGB")
        iw, ih  = image.size
        w, h    = size
        scale   = min(w/iw, h/ih)
        nw      = int(iw*scale)
        nh      = int(ih*scale)

        image       = image.resize((nw,nh), Image.BICUBIC)
        new_image   = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
        return new_image


    def detect_image(self, image_1, image_2):

        image_1 = letterbox_image(cvtColor(image_1), [105, 105], False)
        image_2 = letterbox_image(cvtColor(image_2), [105, 105], False)
        
        photo_1  = preprocess_input(np.array(image_1, np.float32))
        photo_2  = preprocess_input(np.array(image_2, np.float32))

        with torch.no_grad():
            photo_1 = torch.from_numpy(np.expand_dims(np.transpose(photo_1, (2, 0, 1)), 0)).type(torch.FloatTensor)
            photo_2 = torch.from_numpy(np.expand_dims(np.transpose(photo_2, (2, 0, 1)), 0)).type(torch.FloatTensor)

            output = self.net([photo_1, photo_2])[0]
            output = torch.nn.Sigmoid()(output)

        return output

