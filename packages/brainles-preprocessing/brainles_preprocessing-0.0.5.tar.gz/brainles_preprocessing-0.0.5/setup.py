# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brainles_preprocessing',
 'brainles_preprocessing.brain_extraction',
 'brainles_preprocessing.brats',
 'brainles_preprocessing.normalization',
 'brainles_preprocessing.registration']

package_data = \
{'': ['*'],
 'brainles_preprocessing.brain_extraction': ['hdbet_scripts/*'],
 'brainles_preprocessing.registration': ['atlas/*',
                                         'niftyreg_scripts/*',
                                         'niftyreg_scripts/niftyreg_1.5.68/bin/*',
                                         'niftyreg_scripts/niftyreg_1.5.68/include/*']}

install_requires = \
['BrainLes-HD-BET>=0.0.5',
 'auxiliary>=0.0.35',
 'nibabel>=3.2.1',
 'numpy>=1.23.0',
 'path>=16.2.0',
 'pathlib>=1.0.1',
 'tqdm>=4.64.1',
 'ttictoc>=0.5.6']

setup_kwargs = {
    'name': 'brainles-preprocessing',
    'version': '0.0.5',
    'description': 'TODO.',
    'long_description': None,
    'author': 'Florian Kofler',
    'author_email': 'florian.kofler@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
