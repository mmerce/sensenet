import sensenet.importers
tf = sensenet.importers.import_tensorflow()

from sensenet.constants import NUMERIC, CATEGORICAL, IMAGE_PATH

from sensenet.preprocess.categorical import CategoricalPreprocessor
from sensenet.preprocess.numeric import NumericPreprocessor
from sensenet.preprocess.numeric import BinaryPreprocessor
from sensenet.preprocess.image import ImagePreprocessor

class Preprocessor():
    def __init__(self, model, extras):
        self._preprocessors = []

        if model.get('image_network', None) is not None:
            img_proc = ImagePreprocessor(model['image_network'], extras)
            self._image_preprocessor = img_proc

        for pp in model['preprocess']:
            ptype = pp['type']

            if ptype == NUMERIC:
                if 'mean' in pp:
                    self._preprocessors.append(NumericPreprocessor(pp))
                elif 'zero_value' in pp:
                    self._preprocessors.append(BinaryPreprocessor(pp))
            elif ptype == CATEGORICAL:
                self._preprocessors.append(CategoricalPreprocessor(pp))
            elif ptype == IMAGE_PATH:
                self._preprocessors.append(img_proc)
            else:
                raise ValueError('Cannot make processor with type "%s"' % ptype)


    def __call__(self, inputs):
        str_idx = 0
        processed = []

        try:
            string_inputs = inputs['string']
            numeric_inputs = inputs['numeric']
        except TypeError:
            string_inputs = None
            numeric_inputs = inputs

        for i, pp in enumerate(self._preprocessors):
            if isinstance(pp, (ImagePreprocessor, CategoricalPreprocessor)):
                if string_inputs is not None:
                    ith_string = tf.reshape(string_inputs[:,str_idx], (-1,))
                    str_idx += 1
                    processed.append(pp(ith_string))
                elif isinstance(pp, ImagePreprocessor):
                    processed.append(pp(numeric_inputs))
            else:
                ith_numeric = tf.reshape(numeric_inputs[:, i], (-1,))
                processed.append(pp(ith_numeric))

        if len(processed) > 1:
            return tf.concat(processed, -1)
        else:
            return processed[0]
