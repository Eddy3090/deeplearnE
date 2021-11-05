from keras.engine import Layer
import keras.backend as K
class CAM(Layer):
    def __init__(self):
        Layer.__init__(self)

    def call(self, inputs, class_weights=None):
        cam = inputs*class_weights
        
        cam = K.sum(cam, axis=4)
#         print ('cam',K.int_shape(cam))
        cam = K.expand_dims(cam, axis=-1)

        return cam
    
    def compute_output_shape(self,input_shape):
        return tuple(list(input_shape[:-1])+list([1]))
    
    
    
from keras.engine import Layer
import keras.backend as K

class GtMask(Layer):
    def call(self, inputs, gt_mask=None):
        back_mask = 1-gt_mask
        outputs = inputs*back_mask
        return outputs
