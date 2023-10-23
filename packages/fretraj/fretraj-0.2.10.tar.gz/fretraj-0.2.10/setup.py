# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fretraj']

package_data = \
{'': ['*'], 'fretraj': ['UI/*', 'examples/*', 'skripts/*']}

install_requires = \
['importlib-metadata>=6.8.0,<7.0.0',
 'jsonschema>=4.9.1,<5.0.0',
 'mdtraj>=1.9.7,<2.0.0',
 'numba>=0.57.0',
 'pandas>=1.2',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['fretraj = fretraj.console:main',
                     'fretraj_gui = fretraj.fretraj_gui:main',
                     'pymol_vis = fretraj.console:pymol_vis',
                     'vmd_vis = fretraj.console:vmd_vis']}

setup_kwargs = {
    'name': 'fretraj',
    'version': '0.2.10',
    'description': 'Predicting FRET with accessible-contact volumes',
    'long_description': '<img src="https://raw.githubusercontent.com/fdsteffen/fretraj/master/docs/images/fretraj_logo_readme.png">\n\n[![Build Status](https://github.com/fdsteffen/fretraj/workflows/FRETraj%20test/badge.svg)](https://github.com/fdsteffen/fretraj/actions)\n[![Docs Status](https://github.com/fdsteffen/fretraj/workflows/FRETraj%20docs/badge.svg)](https://github.com/fdsteffen/fretraj/actions)\n[![PyPI](https://img.shields.io/pypi/v/fretraj)](https://pypi.org/project/fretraj/)\n[![Conda Version](https://img.shields.io/conda/vn/conda-forge/fretraj.svg)](https://anaconda.org/conda-forge/fretraj)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n*FRETraj* is a Python module for **predicting FRET efficiencies** by calculating multiple accessible-contact volumes (multi-ACV) to estimate donor and acceptor dye dynamics. The package features a user-friendly **PyMOL plugin**<sup>[1](#pymol)</sup> for for FRET-assisted, integrative structural modeling. It interfaces with the [*LabelLib*](https://github.com/Fluorescence-Tools/LabelLib) library for fast computation of ACVs. \nSpecifically, *FRETraj* is designed to:\n- plan (single-molecule) FRET experiments by optimizing **labeling positions**\n- interpret FRET-based **distance measurements** on a biomolecule\n- integrate FRET experiments with **molecular dynamics** simulations\n\n<img src="https://raw.githubusercontent.com/fdsteffen/fretraj/master/docs/images/graphical_abstract.png">\n\n## Installation and Documentation\nFollow the instructions for your platform [here](https://rna-fretools.github.io/fretraj/getting_started/installation)\n\n## References\nIf you use **FRETraj** in your work please refer to the following paper:\n\n- F.D. Steffen, R.K.O. Sigel, R. Börner, *Bioinformatics* **2021**. [![](https://img.shields.io/badge/DOI-10.1093/bioinformatics/btab615-blue.svg)](https://doi.org/10.1093/bioinformatics/btab615)\n\n### Additional readings\n- F.D. Steffen, R.K.O. Sigel, R. Börner, *Phys. Chem. Chem. Phys.* **2016**, *18*, 29045-29055.\n- S. Kalinin, T. Peulen, C.A.M. Seidel et al. *Nat. Methods*, **2012**, *9*, 1218-1225.\n- T. Eilert, M. Beckers, F. Drechsler, J. Michaelis, *Comput. Phys. Commun.*, **2017**, *219*, 377–389.\n- M. Dimura, T. Peulen, C.A.M. Seidel et al. *Curr. Opin. Struct. Biol.* **2016**, *40*, 163-185.\n- M. Dimura, T. Peulen, C.A.M Seidel et al. *Nat. Commun.* **2020**, *11*, 5394.\n\n---\n\n<sup><a name="pymol">1</a></sup> PyMOL was developed by WarrenDeLano and is maintained by Schrödinger, LLC.\n',
    'author': 'Fabio Steffen',
    'author_email': 'fabio.steffen@chem.uzh.ch',
    'maintainer': 'Fabio Steffen',
    'maintainer_email': 'fabio.steffen@chem.uzh.ch',
    'url': 'https://rna-fretools.github.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
