from setuptools import setup

import bayesian_changepoint_detection

setup(
    name='bayescd',
    version=bayesian_changepoint_detection.__version__,
    description='Bayesian changepoint detection algorithms',
    author='Johannes Kulick',
    author_email='mail@johanneskulick.net',
    url='http://github.com/hildensia/bayesian_changepoint_detection',
    packages=['bayesian_changepoint_detection'],
    install_requires=['scipy>=1.6.0', 'numpy', 'decorator', 'pytest', 'matplotlib', 'seaborn', 'tqdm'],
)
