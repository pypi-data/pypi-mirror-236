from pathpretrain.train_model import train_model
import pandas as pd, pickle
from torchvision.ops import nms
import matplotlib.pyplot as plt, numpy as np
from skimage import measure
import warnings
from pathpretrain.train_model import train_model, generate_transformers, generate_kornia_transforms
from torch.utils.data import Dataset
import torch, pandas as pd, numpy as np
from PIL import Image
import seaborn as sns, matplotlib
from scipy.special import softmax
from sklearn.preprocessing import RobustScaler
import tqdm
import fire
warnings.filterwarnings("ignore")

def clean_instance(instances,remove_non_uro=True):
    instances=instances.to("cpu")
    instance_idx=np.arange(len(instances))
    if len(instance_idx):
        keep=nms(boxes = instances.pred_boxes.tensor[instances.pred_classes!=2], scores = instances.scores[instances.pred_classes!=2], iou_threshold=0.1).numpy()
        idx_keep=np.hstack([instance_idx[(instances.pred_classes!=2).numpy()][keep],instance_idx[(instances.pred_classes==2).numpy()]])
        if remove_non_uro: idx_keep=idx_keep[np.isin((instances.pred_classes).numpy()[idx_keep],[0,1,4])]
#         if sum(instances.pred_classes==2): else: idx_keep=instance_idx[(instances.pred_classes!=2).numpy()][keep]
        idx_keep=idx_keep[(instances.scores[idx_keep]>=0.2).numpy()]
        return instances[idx_keep]
    else: return instances

def clean_instance_v2(instances,remove_non_uro=True,prioritize_uro=False,iou_threshold=0.1,aty_reassign=0.2,uro_iou=0.7,keep_class=-1):
    instances=instances.to("cpu")
    instance_idx=np.arange(len(instances))
    if len(instance_idx):
        # keep uro over atypical
        if prioritize_uro:
            uro_class=torch.tensor([0,4])
            tmp_scores=instances.scores[torch.isin(instances.pred_classes,uro_class)]
            tmp_scores[instances.pred_classes[torch.isin(instances.pred_classes,uro_class)]==0]=aty_reassign
            keep=nms(boxes = instances.pred_boxes.tensor[torch.isin(instances.pred_classes,uro_class)], scores = tmp_scores, iou_threshold=uro_iou).numpy()
    #         print(keep)
            keep=np.union1d(keep,np.where(instances.pred_classes[torch.isin(instances.pred_classes,uro_class)]==4)[0])
            idx_keep=np.hstack([instance_idx[torch.isin(instances.pred_classes,uro_class).numpy()][keep],instance_idx[~torch.isin(instances.pred_classes,uro_class)]])
            instances=instances[idx_keep]
            instance_idx=np.arange(len(instances))

        keep=nms(boxes = instances.pred_boxes.tensor[instances.pred_classes!=keep_class], scores = instances.scores[instances.pred_classes!=keep_class], iou_threshold=iou_threshold).numpy()
        idx_keep=np.hstack([instance_idx[(instances.pred_classes!=keep_class).numpy()][keep],instance_idx[(instances.pred_classes==keep_class).numpy()]])
        if remove_non_uro: idx_keep=idx_keep[np.isin((instances.pred_classes).numpy()[idx_keep],[0,1,4])]
#         if sum(instances.pred_classes==2): else: idx_keep=instance_idx[(instances.pred_classes!=2).numpy()][keep]
        idx_keep=idx_keep[(instances.scores[idx_keep]>=0.2).numpy()]
        return instances[idx_keep]
    else: return instances
