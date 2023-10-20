from .data_loader import *
from .loss import *
from .model_unet import *
from .process import *

import numpy as np
import torch, time

__all__ = data_loader.__all__.copy()
__all__ += loss.__all__.copy()
__all__ += model_unet.__all__.copy()
__all__ += process.__all__.copy()
__all__ += ["InferDRAEM"]


class ManagerDRAEM:

    def __init__(self, pathModel, device):
        self.device = device
        self.modelDic = {}
        self.modelDic["recon"] = ReconstructiveSubNetwork(in_channels=1, out_channels=1).to(device)
        self.modelDic["discr"] = DiscriminativeSubNetwork(in_channels=2, out_channels=2).to(device)

        ckp = torch.load(pathModel, map_location=device)
        self.modelDic["recon"].load_state_dict(ckp["modelRe_state_dict"])
        self.modelDic["discr"].load_state_dict(ckp["modelDi_state_dict"])
        self.modelDic["recon"].eval()
        self.modelDic["discr"].eval()

    def __call__(self, data):
        self.timeLast = time.time()
        imgReC = self.modelDic["recon"](data)
        mskExp = self.modelDic["discr"](torch.cat([imgReC, data], 1))
        return mskExp

class InferDRAEM:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["model"]
        self.connection = paraDic["connection"]
        self.pathModel = paraDic["pathModel"]
        self.device = paraDic["device"]
        self.batchSize = paraDic["batchSize"]

        self.getScore = torch.nn.Sequential(
            torch.nn.Softmax(dim=1),
            torch.nn.AvgPool2d(21, stride=1, padding=21//2),
            torch.nn.AdaptiveMaxPool2d(1)
            )

    def LoadModel(self, pathModel):
        self.pathModel = pathModel
        return ManagerDRAEM(self.pathModel, self.device)

    def SetModel(self, manager):
        self.model = manager
        self.device = manager.device

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]

        for idx in range(len(codes)):
            codes[idx]["step"].append(self.name)

        masks = []
        scores = []
        for idx in range(0, imgs.shape[0], self.batchSize):
            img = imgs[idx:idx+self.batchSize].to(self.device)
            mskExp = self.model(img).detach().cpu()
            scores.extend(self.getScore(mskExp[:,1]).flatten().numpy())
            mskExp = torch.softmax(mskExp, 1)[:,1]
            masks.extend(mskExp)

        if 'img' in locals():
            del img, mskExp
            with torch.cuda.device(self.device):
                torch.cuda.empty_cache()

        if len(imgs) != 0:
            pack = {"data" : imgs, "code" : np.array(codes), "score" : np.array(scores), "mask" : torch.stack(masks)}
        else:
            pack = {"data" : imgs, "code" : np.array([]), "score" : np.array([]), "mask" : torch.Tensor([])}

        packNewList = [pack]
    
        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList
