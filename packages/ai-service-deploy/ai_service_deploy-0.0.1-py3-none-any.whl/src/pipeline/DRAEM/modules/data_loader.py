from torch.utils.data import Dataset
from torchvision import transforms
from math import pi, sqrt
from PIL.Image import open
import numpy as np
import torch, cv2, os

__all__ = ["CSV2DIC", "TrainDataset", "ValidDataset", "TestDataset"]


def Crop(src, threshold=50, padd=5):
    _, _, stats, _ = cv2.connectedComponentsWithStats(cv2.inRange(src, threshold, 255))
    if len(stats) > 1:
        idx = (stats[:,2] * stats[:,3]).argsort()[-2]
        x, y, w, h, _ = stats[idx]
        img = src[y-padd:y+h+padd,x-padd:x+w+padd]
        return img, np.array((x-padd, y-padd))
    else:
        return np.zeros((0, 0), dtype=np.uint8), np.array((0, 0))

def Normalization(img, mean=128, std=48):
    dst = img - img.mean()
    dst = dst * std / img.std() + mean
    dst[dst <= 0] = 0
    dst[dst > 255] = 255
    return dst

def f(t):
    return 6*t**5 - 15*t**4 + 10*t**3

def generate_perlin_noise_2d(size, res):

    size = torch.tensor(size).type(torch.int32)
    res = torch.Tensor(res).type(torch.int32)
    d = torch.Tensor((torch.ceil(size / res[0]), torch.ceil(size / res[1]))).type(torch.int64)
    delta = 1/d
    grid = torch.stack(torch.meshgrid(torch.arange(0, res[0], delta[0]), torch.arange(0, res[1], delta[1])), dim = -1) % 1

    angles = 2*pi*torch.rand(res[0]+1, res[1]+1)
    gradients = torch.stack((torch.cos(angles), torch.sin(angles)), dim = -1)
    g00 = gradients[0:-1,0:-1].repeat_interleave(d[0], 0).repeat_interleave(d[1], 1)[:size,:size]
    g10 = gradients[1:,0:-1].repeat_interleave(d[0], 0).repeat_interleave(d[1], 1)[:size,:size]
    g01 = gradients[0:-1,1:].repeat_interleave(d[0], 0).repeat_interleave(d[1], 1)[:size,:size]
    g11 = gradients[1:,1:].repeat_interleave(d[0], 0).repeat_interleave(d[1], 1)[:size,:size]
    grid = grid[:size,:size]

    n00 = (grid * g00).sum(2)
    n10 = (torch.dstack((grid[:,:,0]-1, grid[:,:,1])) * g10).sum(2)
    n01 = (torch.dstack((grid[:,:,0], grid[:,:,1]-1)) * g01).sum(2)
    n11 = (torch.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11).sum(2)

    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11

    return sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

def CSV2DIC(path):
    csv = np.loadtxt(path, delimiter=",", dtype=str)
    dic = {}
    if len(csv.shape) > 1:
        for idx, col in enumerate(csv[0]):
            dic[col] = csv[1:,idx].tolist()
    else:
        dic[csv[0]] = csv[1:].tolist()
    return dic

def Normalization(img, mean=128, std=48):
    img.mean()
    img.std()

    dst = img - img.mean()
    dst = dst * std / img.std() + mean
    dst[dst <= 0] = 0
    dst[dst > 255] = 255
    return dst

def Crop(src, threshold=50, padd=5):
    if src.mean() > 32:
        _, _, stats, _ = cv2.connectedComponentsWithStats(cv2.inRange(src, threshold, 255))
        idx = (stats[:,2] * stats[:,3]).argsort()[-2]
        x, y, w, h, _ = stats[idx]
        img = src[y-padd:y+h+padd,x-padd:x+w+padd]
    else:
        img = src
    return img

class TrainDataset(Dataset):

    def __init__(self, pathPack, resize=(256, 256)):

        self.resize = resize[::-1]
        self.resizeTensor = torch.Tensor(resize[::-1]).type(torch.int32)
        self.sizeExpaded = int(self.resizeTensor.numpy().max()*1.5)
        self.pathImgsList = pathPack["image"]
        self.pathSourList = pathPack["source"]
        self.length = len(self.pathImgsList)

        self.InitRandoms()
        self.InitTransforms()

    def InitRandoms(self):
        self.idxListSour = torch.randint(len(self.pathSourList), size=(self.length,)).type(torch.int32).numpy().tolist()
        self.randListAnor = torch.randint(2, size=(self.length,)).type(torch.bool).numpy().tolist()
        self.randListRotI = torch.rand(self.length) > 0.7
        self.randListPerl = torch.randint(1, 7, size=(self.length, 2))
        self.randListBeta = torch.rand(self.length) * 0.8

    def InitTransforms(self):
        self.importTF = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize(self.resize)
        ])
        self.randAugmenter = transforms.Compose([
            transforms.RandomSolarize(32, p=0.5),
            transforms.RandomInvert(),
            transforms.RandomAutocontrast(),
            transforms.RandomEqualize(),
            transforms.ToTensor(),
            transforms.Resize((self.sizeExpaded, self.sizeExpaded)),
        ])

        interpol = transforms.InterpolationMode.BILINEAR
        self.rotSmallTF = transforms.RandomRotation((-2, 2), interpol)
        self.rotLargeTF = transforms.RandomRotation((-45, 45), interpol)

    def __getitem__(self, idx):
        # Load original image
        img = Normalization(np.array(open(self.pathImgsList[idx]).convert("L")))
        img = self.importTF(img/255).type(torch.float32)
        # Randomly image rotate
        if self.randListRotI[idx]:
            img = self.rotSmallTF(img)
        
        # Anormal to normal or Normal to normal
        if self.randListAnor[idx]:
            # Load overlay source image
            source = self.randAugmenter(open(self.pathSourList[self.idxListSour[idx]]).convert("L"))

            # Make rotated perlin noise mask
            sizeSta = ((self.sizeExpaded - self.resizeTensor)/2).type(torch.int32)
            sizeEnd = ((self.sizeExpaded + self.resizeTensor)/2).type(torch.int32)
            idxRes = self.randListPerl[idx]
            mask = generate_perlin_noise_2d(self.sizeExpaded, (2**idxRes[0], 2**idxRes[1]))
            maskRot = self.rotLargeTF(mask.unsqueeze(0))
            maskRot = maskRot[:,sizeSta[0]:sizeEnd[0],sizeSta[1]:sizeEnd[1]]
            source = source[:,sizeSta[0]:sizeEnd[0],sizeSta[1]:sizeEnd[1]]

            # Make overlay image
            beta = self.randListBeta[idx]
            maskTF = maskRot >= 0.5
            imgAnor = img.type(torch.float32)
            imgAnor[maskTF] *= beta
            imgAnor[maskTF] += source[maskTF] * (1-beta)
            maskTF = maskTF.type(torch.float32)
        else:
            # Normal to normal case
            maskTF = torch.zeros_like(img, dtype=torch.float32)
            imgAnor = img
        
        # Set label
        if torch.sum(maskTF) == 0:
            label = [0.0]
        else:
            label = [1.0]

        sample = {"image" : img, "anomaly_mask" : torch.cat([1-maskTF, maskTF]),
                  "augmented_image" : imgAnor, "label" : label}
        return sample

    def __len__(self):
        return self.length

class ValidDataset(Dataset):

    def __init__(self, pathPack, resize=(256, 256), full=False):

        self.resize = resize[::-1]
        self.pathImgsList = pathPack["image"]
        self.pathTrueList = pathPack["ground_truth"]
        self.length = len(self.pathImgsList)
        self.full = full

        self.importTF = transforms.Compose([transforms.ToTensor(),
                                            transforms.Resize(self.resize)])

        self.InitIndexList()

    def InitIndexList(self):
        idxList = torch.arange(self.length)

        isGT = torch.tensor([os.path.isfile(value) for value in self.pathTrueList], dtype=torch.bool)
        idxListPosi = idxList[isGT]
        idxListNega = idxList[isGT == False]

        nums = (sum(isGT), sum(isGT == False))
        numMin = min(nums)
        idxListPosi = idxListPosi[torch.randperm(nums[0])]
        idxListNega = idxListNega[torch.randperm(nums[1])]

        idxShuffle = torch.cat((idxListPosi[:numMin], idxListNega[:numMin]))
        self.idxList = torch.cat((idxShuffle[torch.randperm(numMin*2)], idxListPosi[numMin:], idxListNega[numMin:]))

        if len(self.idxList) > 1000 and self.full == False:
            self.idxList = self.idxList[:1000]

    def __getitem__(self, idx):
        idx = self.idxList[idx]

        # Load original image
        img = Normalization(np.array(open(self.pathImgsList[idx]).convert("L")))
        img = self.importTF(img/255).type(torch.float32)

        if os.path.isfile(self.pathTrueList[idx]):
            mask = self.importTF(open(self.pathTrueList[idx]).convert("L")).round()
            label = [1.0]
        else:
            mask = torch.zeros_like(img, dtype=torch.float32)
            label = [0.0]

        sample = {"path" : self.pathImgsList[idx], "image" : img,
                  "mask" : torch.cat([1-mask, mask]), "label" : label}

        return sample

    def __len__(self):
        return len(self.idxList)

class TestDataset(Dataset):

    def __init__(self, pathPack, resize=(256, 256)):

        self.resize = resize[::-1]
        self.pathImgsList = pathPack["image"]
        self.pathTrueList = pathPack["ground_truth"]
        self.length = len(self.pathImgsList)

        self.importTF = transforms.Compose([transforms.ToTensor(),
                                            transforms.Resize(self.resize)])

        self.idxList = torch.arange(self.length)

    def __getitem__(self, idx):
        idx = self.idxList[idx]

        # Load original image
        img = np.array(open(self.pathImgsList[idx]).convert("L"))
        imgPP = Crop(img)
        if imgPP.shape[0] * imgPP.shape[1] >= 100:
            imgPP = Normalization(imgPP)
            img = imgPP
        img = self.importTF(imgPP)

        if os.path.isfile(self.pathTrueList[idx]):
            mask = self.importTF(open(self.pathTrueList[idx]).convert("L")).round()
            label = [1.0]
        else:
            mask = torch.zeros_like(img, dtype=torch.float32)
            label = [0.0]

        sample = {"path" : self.pathImgsList[idx], "image" : img,
                  "mask" : torch.cat([1-mask, mask]), "label" : label}

        return sample

    def __len__(self):
        return len(self.idxList)
