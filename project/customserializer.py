# -*- coding: utf-8 -*-

import pickle
import json
import time
import pandas
import numpy

def to_json(python_object):
    print("serializing object type : {}".format(type(python_object)))
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': list(python_object)}
    elif isinstance(python_object, pandas.core.series.Series):
        return {'__class__': 'pandas.core.series.Series',
                '__value__': list(python_object)}
    elif isinstance(python_object, numpy.ndarray):
        return {'__class__': 'numpy.ndarray',
                '__value__': python_object.tolist()}
    elif isinstance(python_object, numpy.number):
        return {'__class__': 'numpy.number',
                '__value__': python_object.tolist()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'bytes':
            return bytes(json_object['__value__'])
        elif json_object['__class__'] == 'pandas.core.series.Series':
            return list(json_object['__value__'])
        elif json_object['__class__'] == 'numpy.ndarray':
            return list(json_object['__value__'])
        elif json_object['__class__'] == 'numpy.number':
            return list(json_object['__value__'])
    return json_object