from setuptools import setup, find_packages

VERSION = '25.2'
DESCRIPTION = 'Package for time domain system identification. LTI and LTV systems, bilinear systems and nonlinear systems.'
LONG_DESCRIPTION = 'Package for time domain system identification. Supports linear time-invariant (LTI) and linear time-varying (LTV) dynamics, bilinear dynamics and nonlinear dynamics.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="systemID_light",
    version=VERSION,
    author="Damien Gueho",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=[
        "systemID_light",
        "systemID_light.core",
        "systemID_light.model"
    ],
    install_requires=['numpy', 'scipy'],
    keywords=['python', 'system identification'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
