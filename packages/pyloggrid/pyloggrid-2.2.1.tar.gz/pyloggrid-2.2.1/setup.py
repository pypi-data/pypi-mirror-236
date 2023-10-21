# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyloggrid', 'pyloggrid.Libs', 'pyloggrid.LogGrid']

package_data = \
{'': ['*']}

install_requires = \
['cython>=3.0.4,<4.0.0',
 'h5py>=3.8.0,<4.0.0',
 'imageio-ffmpeg>=0.4.8,<0.5.0',
 'imageio>=2.28.1,<3.0.0',
 'joblib>=1.2.0,<2.0.0',
 'matplotlib>=3.8.0,<4.0.0',
 'numpy>=1.26.1,<2.0.0',
 'orjson>=3.8.11,<4.0.0',
 'pyqt6>=6.5.3,<7.0.0',
 'rkstiff>=0.3.0,<0.4.0',
 'scienceplots>=2.0.1,<3.0.0',
 'scipy>=1.11.2,<2.0.0']

setup_kwargs = {
    'name': 'pyloggrid',
    'version': '2.2.1',
    'description': 'A python library to perform simulations on logarithmic lattices',
    'long_description': 'PyLogGrid is a Python-based framework for running and analyzing numerical simulations on [log-lattices [1]](https://www.doi.org/10.1088/1361-6544/abef73). The log-lattice structure is particularly useful for modeling phenomena that exhibit multi-scale behavior, such as turbulence. PyLogGrid is designed to be flexible, customizable, and easy to use.\n\nThis framework has been used in several scientific papers such as [[2]](https://www.doi.org/10.1017/jfm.2023.204), [[3]](https://www.doi.org/10.1103/PhysRevE.107.065106).\n\nThe framework includes a variety of built-in tools for analyzing simulation results, including visualization tools and post-processing scripts.\n\n### References:\n\n**[1]** Campolina, C. S., & Mailybaev, A. A. (2021). Fluid dynamics on logarithmic lattices. Nonlinearity, 34(7), 4684. doi:10.1088/1361-6544/abef73\n\n**[2]** Barral, A., & Dubrulle, B. (2023). Asymptotic ultimate regime of homogeneous Rayleigh–Bénard convection on logarithmic lattices. Journal of Fluid Mechanics, 962, A2. doi:10.1017/jfm.2023.204\n\n**[3]** Costa, G., Barral, A., & Dubrulle, B. (2023). Reversible Navier-Stokes equation on logarithmic lattices. Physical Review E, 107(6), 065106. doi:10.1103/PhysRevE.107.065106\n',
    'author': 'Amaury Barral',
    'author_email': 'amaury.barral@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://drf-gitlab.cea.fr/amaury.barral/log-grid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
