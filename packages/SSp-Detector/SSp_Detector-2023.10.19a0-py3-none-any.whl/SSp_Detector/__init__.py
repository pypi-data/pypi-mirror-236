import logging
from .ssp_detector import *
from outdated import warn_if_outdated

#Define logger
logging.basicConfig(format="%(asctime)s|%(levelname)s|%(message)s",datefmt="%y-%b-%d %H:%M:%S")

__author__="Simon J. Guillot <simon.guillot@inserm.fr>"
__version__= "2023.10.19a0"

#Warn if newer version is available
warn_if_outdated("SSp_Detector",__version__)
