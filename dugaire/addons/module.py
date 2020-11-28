import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")

from azurecli import azurecli
from kubectl import kubectl
from velero import velero
