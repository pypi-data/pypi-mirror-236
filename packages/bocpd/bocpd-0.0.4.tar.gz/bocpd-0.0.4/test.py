from functools import partial

import numpy as np
from scipy.stats import multivariate_normal, norm

from bocpd.bayesian_models import online_changepoint_detection
from bocpd.hazard_functions import constant_hazard
from bocpd.online_likelihoods import StudentT, MultivariateT

def test_multivariate():
    np.random.seed(seed=34)
    # 10-dimensional multivariate normal, that shifts its mean at t=50, 100, and 150
    dataset = np.vstack((
        multivariate_normal.rvs([0] * 10, size=50),
        multivariate_normal.rvs([4] * 10, size=50),
        multivariate_normal.rvs([0] * 10, size=50),
        multivariate_normal.rvs([-4] * 10, size=50)
    ))
    r, maxes = online_changepoint_detection(
        dataset,
        partial(constant_hazard, 50),
        MultivariateT(dims=10)
    )

    # Assert that we detected the mean shifts
    for brkpt in [50, 100, 150]:
        assert maxes[brkpt + 1] < maxes[brkpt - 1]


def test_univariate():
    np.random.seed(seed=34)
    # 10-dimensional univariate normal
    dataset = np.hstack((norm.rvs(0, size=50), norm.rvs(2, size=50)))
    r, maxes = online_changepoint_detection(
        dataset,
        partial(constant_hazard, 20),
        StudentT(0.1, .01, 1, 0)
    )
    assert maxes[50] - maxes[51] > 40
