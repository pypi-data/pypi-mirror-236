from torch.autograd import Variable

import torch, time, os
import matplotlib.pyplot as plt
import numpy as np

__all__ = ["MakeFolderTree", "Tensor2Image", "DrawPreview", "DrawLossGraph", "StepTrain", "StepTest"]


def MakeFolderTree(filePath, last=-1):
    accuPath = ""
    for subPath in filePath.split('/')[:last]:
        accuPath = os.path.join(accuPath, subPath)
        if bool(subPath) and not os.path.isdir(accuPath):
            os.mkdir(accuPath)
    return None

def Tensor2Image(mat):
    mat = mat.detach().cpu().numpy()
    mat = np.transpose(mat, (0, 2, 3, 1))
    if mat.shape[3] == 1:
        return (mat*255).astype(np.uint8)
    else:
        return mat[:,:,:,1]

def DrawPreview(matList, pathSave):
    plt.figure(figsize=(4*len(matList), 4))

    for idx, mat in enumerate(matList):
        # Set plot position
        plt.subplot(1, len(matList), idx+1)
        plt.imshow(mat, "gray")
        plt.axis("off")

    plt.savefig(pathSave, bbox_inches='tight')
    plt.close()
    return None

def DrawLossGraph(lossPack, pathSave):
    plt.figure(figsize=(15, 4))

    plt.subplot(1,3,1)
    plt.title("Train")
    plt.plot(lossPack["train"]["L2"], label="L2", color="blue")
    plt.plot(lossPack["train"]["SSIM"], label="SSIM", color="red")
    plt.plot(lossPack["train"]["Focal"], label="Focal", color="black")
    plt.legend()

    plt.subplot(1,3,2)
    plt.title("Test")
    plt.plot(lossPack["test"]["Focal"], label="Focal", color="black")
    plt.legend()

    plt.subplot(1,3,3)
    plt.title("FPR")
    plt.plot(lossPack["test"]["FPR"], label="1-Specificity", color="red")
    plt.legend()

    plt.savefig(pathSave)
    plt.close()
    return None

def StepTrain(epoch, modelDic, lossFuncDic, dataLoader, optimizer, device, termSave, pathPreV):
    state = "Train"
    modelRe = modelDic["recon"]
    modelDi = modelDic["discr"]
    lossFuncL2 = lossFuncDic["L2"]
    lossFuncSSIM = lossFuncDic["SSIM"]
    lossFuncFocal = lossFuncDic["Focal"]

    modelRe.train()
    modelDi.train()

    lossRecordDic = {"L2" : 0, "SSIM" : 0, "Focal" : 0}
    current = 0
    numTotal = len(dataLoader.dataset)
    numTest = 0

    # Start
    timeSta = time.time()
    for pack in dataLoader:
        imgNor = Variable(pack["image"]).to(device)
        imgAnor = Variable(pack["augmented_image"]).to(device)
        mskAnor = Variable(pack["anomaly_mask"]).to(device)

        optimizer.zero_grad()

        imgReC = modelDic["recon"](imgAnor)
        mskExp = modelDic["discr"](torch.cat([imgReC, imgAnor], 1))

        lossL2 = lossFuncL2(imgNor, imgReC)
        lossSSIM = lossFuncSSIM(imgNor, imgReC) / 8
        lossFocal = lossFuncFocal(torch.softmax(mskExp, 1), mskAnor)
        loss = lossL2 + lossSSIM + lossFocal

        loss.backward()
        optimizer.step()

        current += len(imgAnor)
        lossRecordDic["L2"] += lossL2.detach().cpu().numpy()
        lossRecordDic["SSIM"] += lossSSIM.detach().cpu().numpy()
        lossRecordDic["Focal"] += lossFocal.detach().cpu().numpy()

        # Record sample images
        if epoch % termSave == 0:
            MakeFolderTree(pathPreV)
            matBatchList = (imgAnor, mskAnor, imgReC, mskExp)
            for matList in zip(*list(map(Tensor2Image, matBatchList))):
                if numTest < 8 :
                    numTest += 1
                    DrawPreview(matList, "%s%s_%.3d.jpg"%(pathPreV, state, numTest))

        print("%s %d/%d (%.2f%%) : %.1fs"%(state, current, numTotal, 100*current/numTotal, time.time()-timeSta), end="\r")
    print()

    lossRecordDic["L2"] /= current
    lossRecordDic["SSIM"] /= current
    lossRecordDic["Focal"] /= current

    return lossRecordDic

def StepTest(epoch, modelDic, lossFuncDic, dataLoader, device, termSave, pathPreV, threshold=-1):
    state = "Test"
    modelRe = modelDic["recon"]
    modelDi = modelDic["discr"]
    lossFuncFocal = lossFuncDic["Focal"]

    modelRe.eval()
    modelDi.eval()

    getScore = torch.nn.Sequential(torch.nn.Softmax(dim=1),
                                   torch.nn.AvgPool2d(21, stride=1, padding=21//2),
                                   torch.nn.AdaptiveMaxPool2d(1))

    lossRecordDic = {"Focal" : 0}
    current = 0
    numTotal = len(dataLoader.dataset)
    numTest = 0
    results = {"path" : {"P" : [], "N" : []}, "score" : {"P" : [], "N" : []}}

    # Start
    timeSta = time.time()
    for pack in dataLoader:
        with torch.no_grad():
            imgAnor = pack["image"].to(device)
            mskAnor = pack["mask"].to(device)
        labelList = pack["label"][0].numpy()
        pathList = np.array(pack["path"])

        imgReC = modelRe(imgAnor)
        mskExp = modelDi(torch.cat([imgReC, imgAnor], 1))

        lossFocal = lossFuncFocal(torch.softmax(mskExp, 1), mskAnor)
        
        current += len(imgAnor)
        scores = getScore(mskExp[:,1].detach().cpu()).flatten().numpy()
        results["path"]["P"].extend(pathList[labelList == 1])
        results["path"]["N"].extend(pathList[labelList == 0])
        results["score"]["P"].extend(scores[labelList == 1])
        results["score"]["N"].extend(scores[labelList == 0])
        lossRecordDic["Focal"] += lossFocal.detach().cpu().numpy()

        # Record sample images
        if termSave == -1:
            matBatchList = (imgAnor, mskAnor, imgReC, mskExp)
            for matList in zip(*list(map(Tensor2Image, matBatchList))):
                if numTest < 16:
                    numTest += 1
                    DrawPreview(matList, "%s%s_%.3d.jpg"%(pathPreV, state, numTest))
        elif epoch % termSave == 0:
            matBatchList = (imgAnor, mskAnor, imgReC, mskExp)
            for matList in zip(*list(map(Tensor2Image, matBatchList))):
                if numTest < 8:
                    numTest += 1
                    DrawPreview(matList, "%s%s_%.3d.jpg"%(pathPreV, state, numTest))

        if threshold == -1:
            if len(results["score"]["P"]) == 0:
                FPR = np.nan
            else:
                threshold = np.min(results["score"]["P"])
                FPR = (np.array(results["score"]["N"]) >= threshold).sum()/len(results["score"]["N"])*100
        else:
            FPR = (np.array(results["score"]["N"]) >= threshold).sum()/len(results["score"]["N"])*100
        print("%s %d/%d (%.2f%%) | FPR %.2f%% : %.1fs"
              %(state, current, numTotal, 100*current/numTotal, FPR, time.time()-timeSta), end="\r")
    print()
    del imgAnor, mskAnor, imgReC, mskExp, lossFocal

    lossRecordDic["Focal"] /= current
    lossRecordDic["FPR"] = FPR

    return lossRecordDic, results