from torchvision import transforms
from torch import nn
import torch

__all__ = ["SSIMLoss", "FocalLoss"]


class SSIMLoss(nn.Module):

    def __init__(self, max_val=255, window_size=11):
        super(SSIMLoss, self).__init__()
        
        self.max_val = max_val
        self.gauBlur = transforms.GaussianBlur(window_size, sigma=1.5)

    def forward(self, img1, img2):
        mu1 = self.gauBlur(img1)
        mu2 = self.gauBlur(img2)

        mu1_sq = mu1.pow(2)
        mu2_sq = mu2.pow(2)
        mu1_mu2 = mu1 * mu2

        sigma1_sq = self.gauBlur(img1 * img1) - mu1_sq
        sigma2_sq = self.gauBlur(img2 * img2) - mu2_sq
        sigma12 = self.gauBlur(img1 * img2) - mu1_mu2

        c1 = (0.01 * self.max_val) ** 2
        c2 = (0.03 * self.max_val) ** 2

        v1 = 2.0 * sigma12 + c2
        v2 = sigma1_sq + sigma2_sq + c2
        #cs = (v1 / v2).mean() # Full size

        ssim_map = ((2 * mu1_mu2 + c1) * v1) / ((mu1_sq + mu2_sq + c1) * v2)
        return 1 - ssim_map.mean()

class FocalLoss(nn.Module):
    
    def __init__(self, alpha=None, gamma=2, smooth=1e-5, size_average=True):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.smooth = smooth
        self.size_average = size_average
        
    def forward(self, logit, target):
        target = torch.clamp(target, self.smooth, 1-self.smooth)
        BCE = nn.BCELoss(reduction='none')(logit, target)
        p_t = torch.exp(-BCE)
        loss = (1 - p_t)**self.gamma * BCE
        
        if self.alpha != None:
            weight = target * self.alpha + (1 - target) * (1 - self.alpha)
            loss = weight * loss
        
        if self.size_average:
            loss = loss.mean()
        return loss
