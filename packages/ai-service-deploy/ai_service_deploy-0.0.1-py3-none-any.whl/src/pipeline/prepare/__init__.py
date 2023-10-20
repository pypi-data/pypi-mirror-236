from torchvision import transforms

import numpy as np
import torch, copy, cv2

__all__ = [
    "Input000001",
    "PrePro000001",
    "PrePro000002",
    "PrePro000011",
    "PostPro000001",
    "PostPro000002",
    "Output000001",
    "ClipMaker000001",
    "ClipSumm000001",
    "Over000001"
]


def RecordStep(dic, name):
    if "step" not in dic:
        dic["step"] = []
    dic["step"].append(name)
    return dic

class Input000001:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["input"]
        self.connection = paraDic["connection"]

    def __call__(self, pack):
        codes = pack["code"]
        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)

        packNewList = []
        for pack, out in zip([pack], self.connection["out"]):
            packNewList.append(pack)

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class PreProNorm:

    def Normalize(self, img):
        dst = img - img.mean()
        dst = dst * self.std / img.std() + self.mean
        dst[dst <= 0] = 0
        dst[dst > 255] = 255
        return dst

class PreProCrop:

    def Crop(self, src):
        _, _, stats, _ = cv2.connectedComponentsWithStats(cv2.inRange(src, self.threshold, 255))
        if len(stats) > 1:
            idx = (stats[:,2] * stats[:,3]).argsort()[-2]
            x, y, w, h, _ = stats[idx]
            img = src[y-self.padd:y+h+self.padd,x-self.padd:x+w+self.padd]
            return img, np.array((x-self.padd, y-self.padd))
        else:
            return src, np.array((0, 0))

class Classic:

    def crop(self, src:cv2.Mat):
        src_h, src_w = src.shape
        _, bsrc = cv2.threshold(src, thresh=self.threshold, maxval=255, type=cv2.THRESH_BINARY)
        _, _, stats, _ = cv2.connectedComponentsWithStats(bsrc)
        idx = 0
        min_crop_size = 100
        max_crop_size = 9999
        roi = (0,0,0,0)
        for x, y, w, h, _ in stats:
            if x < self.padd or x + w > src_w - self.padd or y < self.padd or y + h > src_h - self.padd:
                idx += 1
                continue
            if w < min_crop_size or w > max_crop_size or h < min_crop_size or h > max_crop_size:
                idx += 1
                continue
            roi = (x - self.padd, y - self.padd, w + (2*self.padd), h + (2*self.padd))
            break
        dst = src[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
        return dst, np.array((x-self.padd, y-self.padd))

    def bright_correction(self, src):
        t_mean = self.mean
        t_stddev = self.std
        s_mean = np.mean(src)
        s_stddev = np.std(src)
        
        if s_stddev == 0:
            rate = t_stddev
        else:
            rate = t_stddev / s_stddev
        
        s_avr = int(s_mean)
        dst = cv2.Mat(src)
        cv2.subtract(src, s_avr, dst)
        buf = cv2.Mat(-src)
        cv2.add(buf, s_avr, buf)
        buf[buf > s_avr] = 0

        cv2.multiply(dst, rate, dst)
        cv2.add(dst, int(t_mean), dst)
        cv2.multiply(buf, rate, buf)
        cv2.subtract(dst, buf, dst)
        return dst

    def pp(self, src):
        img = self.bright_correction(src)
        img, xy = self.crop(img)
        return img, xy

class PrePro000001(PreProCrop, PreProNorm):

    def __init__(self, paraDic):
        super().__init__()
        self.name = type(self).__name__
        self.tag = ["preprocess"]
        self.connection = paraDic["connection"]
        self.sizeImg = paraDic["sizeImg"]
        self.threshold = paraDic["threshold"]
        self.padd = paraDic["padd"]
        self.mean = paraDic["mean"]
        self.std = paraDic["std"]
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize(self.sizeImg[::-1])
        ])

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]

        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)

        for idx in range(len(imgs)):
            size = imgs[idx].shape[:2][::-1]
            imgPP, coordinate = self.Crop(imgs[idx])
            imgPP = self.Normalize(imgPP)
            if imgPP.shape[0] * imgPP.shape[1] >= 100:
                imgs[idx] = imgPP
                size = imgPP.shape[:2][::-1]
            imgs[idx] = self.transform(imgs[idx]/255).type(torch.float32)

            codes[idx]["imageSize"] = size
            codes[idx]["resize"] = self.sizeImg
            codes[idx]["cropXY"] = coordinate.tolist()

        if len(imgs) != 0:
            pack = {"data" : torch.stack(imgs), "code" : codes}
        else:
            pack = {"data" : torch.Tensor([]), "code" : codes}

        packNewList = [pack]

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class PrePro000011(Classic):

    def __init__(self, paraDic):
        super().__init__()
        self.name = type(self).__name__
        self.tag = ["preprocess"]
        self.connection = paraDic["connection"]
        self.sizeImg = paraDic["sizeImg"]
        self.threshold = paraDic["threshold"]
        self.padd = paraDic["padd"]
        self.mean = paraDic["mean"]
        self.std = paraDic["std"]
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize(self.sizeImg[::-1])
        ])

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]

        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)

        for idx in range(len(imgs)):
            size = imgs[idx].shape[:2][::-1]
            img = imgs[idx]
            imgPP, coordinate = self.pp(img)
            if imgPP.shape[0] * imgPP.shape[1] >= 100:
                img = imgPP
                size = img.shape[:2][::-1]
            imgs[idx] = self.transform(img/255).type(torch.float32)

            codes[idx]["imageSize"] = size
            codes[idx]["resize"] = self.sizeImg
            codes[idx]["cropXY"] = coordinate.tolist()

        if len(imgs) != 0:
            pack = {"data" : torch.stack(imgs), "code" : codes}
        else:
            pack = {"data" : torch.Tensor([]), "code" : codes}

        packNewList = [pack]

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class PostPro000001:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["postprocess"]
        self.connection = paraDic["connection"]
        self.threshold = paraDic["threshold"]

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]
        scores = pack["score"]
        masks = pack["mask"]

        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)

        if len(codes) > 0:
            labelList = (scores >= self.threshold).astype(int)
            for idx in range(len(codes)):
                codes[idx]["score"] = [scores[idx].item()]
                codes[idx]["label"] = labelList[idx]
            
            packNewList = []
            for label in [0, 1]:
                packNew = {}
                boolList = labelList == label
                packNew["data"] = imgs[boolList]
                packNew["code"] = codes[boolList]
                packNew["mask"] = masks[boolList]
                for out in self.connection["out"][label]:
                    packNewList.append(packNew)
        else:
            pack = {"data" : torch.Tensor([]), "code" : codes, "mask" : torch.Tensor([])}
            packNewList = [pack, pack]

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class Output000001:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["output"]
        self.connection = paraDic["connection"]
        self.needs = paraDic["needs"]
        self.mapping = paraDic["mapping"]
        self.result = paraDic["result"]

    def __call__(self, pack):
        codes = pack["code"]

        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)
        
        outputList = []
        for idx in range(len(codes)):
            output = {}
            for name in self.needs:
                if name == "label":
                    output[name] = self.mapping[str(codes[idx][name])]
                elif name == "score":
                    output[name] = max(codes[idx][name])
                else:
                    output[name] = codes[idx][name]

            output["result"] = {}
            for name in self.result:
                output["result"][name] = codes[idx][name]

            outputList.append(output)

        packNewList = [{"output" : outputList}]

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class ClipMaker000001:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["additional"]
        self.connection = paraDic["connection"]
        self.threshold = paraDic["threshold"]

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]
        masks = pack["mask"]

        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)

        output = []
        codesNew = []
        for idx in range(len(imgs)):
            img = imgs[idx]
            mask = masks[idx]
            region = img.shape[-1] * img.shape[-2] * 0.9
            mask = mask.numpy() > self.threshold

            _, _, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
            for x, y, w, h, _ in stats:
                if w*h > 8 and w*h < region:
                    output.append(img[0,y:y+h,x:x+w].numpy())

                    code = copy.deepcopy(codes[idx])
                    clipXYWH = np.array((x, y, w, h))
                    code["clipXYWH"] = clipXYWH.tolist()
                    ratio = np.array(code["imageSize"]) / np.array(code["resize"])
                    xyList = code["cropXY"] + clipXYWH[:2] * ratio
                    whList = clipXYWH[-2:] * ratio
                    code["clipXYWH-global"] = np.append(xyList, whList).astype(int).tolist()
                    codesNew.append(code)

        if len(output) != 0:
            pack = {"data" : output, "code" : np.array(codesNew)}
        else:
            pack = {"data" : torch.Tensor([]), "code" : np.array(codesNew)}

        packNewList = [pack]

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class PrePro000002:

    def __init__(self, paraDic):
        super().__init__()
        self.name = type(self).__name__
        self.tag = ["preprocess"]
        self.connection = paraDic["connection"]
        self.sizeImg = paraDic["sizeImg"]
        self.meanList = paraDic["meanList"]
        self.stdList = paraDic["stdList"]
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(self.meanList, self.stdList)
        ])

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]

        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)

        for idx in range(len(imgs)):
            size = imgs[idx].shape[:2][::-1]
            img = cv2.resize(imgs[idx], self.sizeImg[::-1], interpolation=cv2.INTER_AREA)
            if len(img.shape) == 2:
                img = np.stack((img, img, img), 2)
            imgs[idx] = self.transform(img).type(torch.float32)

            codes[idx]["imageSize"] = size
            codes[idx]["resize"] = self.sizeImg

        if len(imgs) != 0:
            pack = {"data" : torch.stack(imgs), "code" : codes}
        else:
            pack = {"data" : torch.Tensor([]), "code" : codes}

        packNewList = [pack]

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class PostPro000002:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["postprocess"]
        self.connection = paraDic["connection"]
        self.threshold = paraDic["threshold"]

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]
        scores = pack["score"]

        for idx in range(len(codes)):
            codes[idx] = RecordStep(codes[idx], self.name)

        if len(codes) > 0:
            scoreMat = torch.softmax(scores, 1)
            scoreSM = scoreMat.clone().detach()
            boolMat = scoreMat > torch.Tensor(self.threshold)
            scoreMat[boolMat == False] = -1
            scoreMaxList, labelList = scoreMat.max(1)
            labelList[scoreMaxList == -1] = -1

            packNewList = []
            for label in range(-1, len(self.threshold)):
                pack = {}
                boolList = (labelList == label).numpy()
                pack["data"] = imgs[boolList]
                pack["code"] = codes[boolList]

                scoresNew = scoreSM[boolList]
                labelsNew = labelList[boolList]
                for idx2 in range(len(pack["code"])):
                    pack["code"][idx2]["score"] = scoresNew[idx2].numpy().tolist()
                    pack["code"][idx2]["label"] = labelsNew[idx2].item()
                packNewList.append(pack)
        else:
            pack = {"data" : torch.Tensor([]), "code" : codes, "extra" : {}}
            packNewList = []
            for label in range(-1, len(self.threshold)):
                packNewList.append(pack)

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class ClipSumm000001:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["additional"]
        self.connection = paraDic["connection"]
        self.targetLabelList = paraDic["targetLabelList"]

    def __call__(self, pack):

        codesNew = {}
        codes = pack["code"]

        for idx in range(len(codes)):
            code = codes[idx]
            label = code["label"]
            score = code["score"]
            imgID = code["image_id"]
            if imgID not in codesNew:
                codesNew[imgID] = copy.deepcopy(code)
                codesNew[imgID]["label"] = []
                codesNew[imgID]["score"] = []
                codesNew[imgID]["clip_list"] = []

            codesNew[imgID]["label"].append(label)
            codesNew[imgID]["score"].append(score)
            clip_list = {}
            clip_list["label"] = label
            clip_list["score"] = np.array(score).round(4).astype(np.float16).tolist()
            clip_list["xywh"] = code["clipXYWH-global"]
            codesNew[imgID]["clip_list"].append(clip_list)
        codesNew = np.array(list(codesNew.values()))

        for idx in range(len(codesNew)):
            codesNew[idx] = RecordStep(codesNew[idx], self.name)
            if len(np.intersect1d(self.targetLabelList, codesNew[idx]["label"])) > 0:
                codesNew[idx]["label"] = 1
                codesNew[idx]["score"] = [1]
            else:
                codesNew[idx]["label"] = 0
                codesNew[idx]["score"] = [0]

        packNewList = [{"code" : codesNew}]

        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList

class Over000001:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["output"]
        self.connection = paraDic["connection"]

    def __call__(self, *packList):
        packNew = {}
        for pack in packList:
            for packEach in pack["output"]:
                ID = packEach["image_id"]
                if ID not in packNew:
                    packNew[ID] = {}
                for key in packEach.keys():
                    packNew[ID][key] = packEach[key]

        packNewList = []
        for packEach in packNew.values():
            packNewList.append(packEach)

        return [{"pack" : {"output" : packNewList}, "out" : "end"}]

