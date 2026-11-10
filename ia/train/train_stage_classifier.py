# Dans la première cellule Colab :
from google.colab import drive
drive.mount("/content/drive")
# Puis copie le dataset dans /content/drive/MyDrive/aptos/
# Et lance :
# !python train/train_stage_classifier.py