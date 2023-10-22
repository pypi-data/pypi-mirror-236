import io
import os
from pathlib import Path

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'commutauto'
DESCRIPTION = 'CLI to interact with your car sharing service API. Search for available vehicles, manage your bookings and more...'
URL = 'https://github.com/elbuco1/commutauto'
EMAIL = 'lrtboucaud@gmail.com'
AUTHOR = "Laurent Boucaud"
REQUIRES_PYTHON = '>=3.7'

def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

INSTALL_REQUIRES = list_reqs()

TEST_REQUIRES = [
    'pytest',
    'tox'
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# try:
#     with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#         long_description = '\n' + f.read()
# except FileNotFoundError:
#     long_description = DESCRIPTION

# import version
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / NAME

about = {}
with open(PACKAGE_DIR / 'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    package_data={
        'commutauto': ['VERSION']
    },
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "tests": TEST_REQUIRES
    },
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': [
            'commutauto=commutauto.__main__:main'
        ]
    }
)
