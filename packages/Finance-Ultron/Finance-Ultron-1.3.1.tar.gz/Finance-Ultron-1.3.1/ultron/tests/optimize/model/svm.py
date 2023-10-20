# -*- coding: utf-8 -*-
import unittest, pdb
import numpy as np
import pandas as pd
from sklearn.svm import NuSVR as NuSVR2
from ultron.optimize.model.svm import NvSVRModel
from ultron.optimize.model.loader import load_model


class SVMModel(unittest.TestCase):

    def setUp(self):
        self.n = 3
        self.features = ['a', 'b', 'c']
        self.train_x = pd.DataFrame(np.random.randn(1000, self.n),
                                    columns=self.features)
        self.train_y = np.random.randn(1000)
        self.train_y_label = np.where(self.train_y > 0., 1, 0)
        self.predict_x = pd.DataFrame(np.random.randn(10, self.n),
                                      columns=self.features)

    def test_nvsvr_model(self):
        model = NvSVRModel(kernel='linear', features=self.features)
        model.fit(self.train_x, self.train_y)
        calculated_y = model.predict(self.predict_x)

        expected_model = NuSVR2(kernel='linear')
        expected_model.fit(self.train_x, self.train_y)
        expected_y = expected_model.predict(self.predict_x)

        np.testing.assert_array_equal(calculated_y, expected_y)
        np.testing.assert_array_almost_equal(expected_model.coef_,
                                             model.weights)

    def test_nvsvr_model_presistence(self):
        model = NvSVRModel(kernel='linear', features=self.features)
        model.fit(self.train_x, self.train_y)

        desc = model.save()
        new_model = load_model(desc)

        calculated_y = model.predict(self.predict_x)
        expected_y = new_model.predict(self.predict_x)

        np.testing.assert_array_almost_equal(calculated_y, expected_y)
        np.testing.assert_array_almost_equal(new_model.weights, model.weights)
