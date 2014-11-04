# -*- coding: utf-8 -*-
"""
    hdnet
    ~~~~~

    Tests for Sampling class

    :copyright: Copyright 2014 the authors, see AUTHORS.
    :license: GPLv3, see LICENSE for details.
"""

import os
import unittest
import shutil
import numpy as np

from hdnet.sampling import sample_from_prob_vector, sample_from_Bernoulli, sample_from_ising


class TestSampling(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        if os.path.exists("sampling"):
            shutil.rmtree("sampling")
        os.mkdir("sampling")

    def tearDown(self):
        if os.path.exists("sampling"):
            shutil.rmtree("sampling")

    def test_basic(self):
        
        p = [.1, .4, .5]
        self.assertTrue(sample_from_prob_vector(p) > -1)
        self.assertTrue(sample_from_prob_vector(p, 100).mean() > 1)
        sample_from_Bernoulli(p, 10)

        p = [.8, .05, .05, .05, .05]
        sample_from_Bernoulli(p, 10)
        sample_from_Bernoulli(p)

        p = [.5, .4, .1]
        self.assertTrue(sample_from_prob_vector(p, 100).mean() < 1)

        p = np.random.random(100)
        p /= p.sum()

        a = np.arange(0, len(p))
        exp_state = np.dot(a, p)

        self.assertTrue(np.abs(sample_from_prob_vector(p, 1000).mean() - exp_state) < 5)

        J = np.random.random((6, 6)) - np.random.random((6, 6))
        J -= np.diag(J.diagonal())
        J += J.T
        theta = np.zeros(6)

        self.assertTrue((J.sum(axis=1).argsort() == sample_from_ising(J,
                            theta, num_samples=10000).mean(axis=1).argsort()).sum() >= 2)

        
