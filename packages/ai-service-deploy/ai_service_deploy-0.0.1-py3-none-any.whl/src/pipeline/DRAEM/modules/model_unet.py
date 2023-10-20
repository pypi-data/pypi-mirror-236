import torch
import torch.nn as nn

__all__ = ["weights_init", "ReconstructiveSubNetwork", "DiscriminativeSubNetwork"]


def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)

class ReconstructiveSubNetwork(nn.Module):
    
    def __init__(self,in_channels=3, out_channels=3, base_width=128):
        super(ReconstructiveSubNetwork, self).__init__()

        self.encoder = EncoderReconstructive(in_channels, base_width)
        self.decoder = DecoderReconstructive(base_width, out_channels=out_channels)

    def forward(self, x):

        b5 = self.encoder(x)
        output = self.decoder(b5)

        return output

class DiscriminativeSubNetwork(nn.Module):
    
    def __init__(self,in_channels=3, out_channels=3, base_channels=64):
        super(DiscriminativeSubNetwork, self).__init__()

        self.encoder_segment = EncoderDiscriminative(in_channels, base_channels)
        self.decoder_segment = DecoderDiscriminative(base_channels, out_channels=out_channels)

    def forward(self, x):

        bPack = self.encoder_segment(x)
        output_segment = self.decoder_segment(*bPack)

        return output_segment

def MakeConv2DBlock(numInputChannels, numOutputChannels):

    blockList = [
        nn.Conv2d(numInputChannels, numOutputChannels, kernel_size=3, padding=1),
        nn.BatchNorm2d(numOutputChannels),
        nn.ReLU(inplace=True)]

    return blockList

def MakeConv2DSeq(numInputChannels, numCenterChannels, numOutputChannels, numCycles):

    blocks = []
    blocks.extend(MakeConv2DBlock(numInputChannels, numCenterChannels))
    for num in range(1, numCycles-1):
        blocks.extend(MakeConv2DBlock(numCenterChannels, numCenterChannels))
    blocks.extend(MakeConv2DBlock(numCenterChannels, numOutputChannels))

    return nn.Sequential(*blocks)

class EncoderDiscriminative(nn.Module):
    
    def __init__(self, in_channels, base_width):
        super(EncoderDiscriminative, self).__init__()

        _m = 2**0
        self.block1 = MakeConv2DSeq(in_channels, base_width*_m, base_width*_m, 2)
        self.mp1 = nn.Sequential(nn.MaxPool2d(2))
        
        _m = 2**1
        self.block2 = MakeConv2DSeq(base_width*int(_m/2), base_width*_m, base_width*_m, 2)
        self.mp2 = nn.Sequential(nn.MaxPool2d(2))
        
        _m = 2**2
        self.block3 = MakeConv2DSeq(base_width*int(_m/2), base_width*_m, base_width*_m, 2)
        self.mp3 = nn.Sequential(nn.MaxPool2d(2))
        
        _m = 2**3
        self.block4 = MakeConv2DSeq(base_width*int(_m/2), base_width*_m, base_width*_m, 2)
        self.mp4 = nn.Sequential(nn.MaxPool2d(2))
        
        self.block5 = MakeConv2DSeq(base_width*_m, base_width*_m, base_width*_m, 2)
        self.mp5 = nn.Sequential(nn.MaxPool2d(2))
        
        self.block6 = MakeConv2DSeq(base_width*_m, base_width*_m, base_width*_m, 2)

    def forward(self, x):

        b1 = self.block1(x)
        mp1 = self.mp1(b1)

        b2 = self.block2(mp1)
        mp2 = self.mp3(b2)

        b3 = self.block3(mp2)
        mp3 = self.mp3(b3)

        b4 = self.block4(mp3)
        mp4 = self.mp4(b4)

        b5 = self.block5(mp4)
        mp5 = self.mp5(b5)

        b6 = self.block6(mp5)

        return b1, b2, b3, b4, b5, b6

class DecoderDiscriminative(nn.Module):
    
    def __init__(self, base_width, out_channels=1):
        super(DecoderDiscriminative, self).__init__()

        _m = 2**3
        self.up_b = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m, base_width*_m)])
        self.db_b = MakeConv2DSeq(base_width*_m*2, base_width*_m, base_width*_m, 2)

        _m = 2**2
        self.up1 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m*2, base_width*_m)])
        self.db1 = MakeConv2DSeq(base_width*(_m+_m*2), base_width*_m, base_width*_m, 2)

        _m = 2**1
        self.up2 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m*2, base_width*_m)])
        self.db2 = MakeConv2DSeq(base_width*(_m+_m*2), base_width*_m, base_width*_m, 2)

        _m = 2**0
        self.up3 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m*2, base_width*_m)])
        self.db3 = MakeConv2DSeq(base_width*(_m+_m*2), base_width*_m, base_width*_m, 2)

        self.up4 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m, base_width*_m)])
        self.db4 = MakeConv2DSeq(base_width*_m*2, base_width, base_width, 2)

        self.fin_out = nn.Sequential(nn.Conv2d(base_width, out_channels, kernel_size=3, padding=1))

    def forward(self, b1, b2, b3, b4, b5, b6):

        up_b = self.up_b(b6)
        cat_b = torch.cat((up_b,b5),dim=1)
        db_b = self.db_b(cat_b)

        up1 = self.up1(db_b)
        cat1 = torch.cat((up1,b4),dim=1)
        db1 = self.db1(cat1)

        up2 = self.up2(db1)
        cat2 = torch.cat((up2,b3),dim=1)
        db2 = self.db2(cat2)

        up3 = self.up3(db2)
        cat3 = torch.cat((up3,b2),dim=1)
        db3 = self.db3(cat3)

        up4 = self.up4(db3)
        cat4 = torch.cat((up4,b1),dim=1)
        db4 = self.db4(cat4)

        out = self.fin_out(db4)

        return out

class EncoderReconstructive(nn.Module):
    
    def __init__(self, in_channels, base_width):
        super(EncoderReconstructive, self).__init__()

        _m = 2**0
        self.block1 = MakeConv2DSeq(in_channels, base_width*_m, base_width*_m, 2)
        self.mp1 = nn.Sequential(nn.MaxPool2d(2))
        
        _m = 2**1
        self.block2 = MakeConv2DSeq(base_width*int(_m/2), base_width*_m, base_width*_m, 2)
        self.mp2 = nn.Sequential(nn.MaxPool2d(2))
        
        _m = 2**2
        self.block3 = MakeConv2DSeq(base_width*int(_m/2), base_width*_m, base_width*_m, 2)
        self.mp3 = nn.Sequential(nn.MaxPool2d(2))
        
        _m = 2**3
        self.block4 = MakeConv2DSeq(base_width*int(_m/2), base_width*_m, base_width*_m, 2)
        self.mp4 = nn.Sequential(nn.MaxPool2d(2))
        
        self.block5 = MakeConv2DSeq(base_width*_m, base_width*_m, base_width*_m, 2)

    def forward(self, x):

        b1 = self.block1(x)
        mp1 = self.mp1(b1)

        b2 = self.block2(mp1)
        mp2 = self.mp3(b2)

        b3 = self.block3(mp2)
        mp3 = self.mp3(b3)

        b4 = self.block4(mp3)
        mp4 = self.mp4(b4)

        b5 = self.block5(mp4)

        return b5

class DecoderReconstructive(nn.Module):
    
    def __init__(self, base_width, out_channels=1):
        super(DecoderReconstructive, self).__init__()

        _m = 2**3
        self.up1 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m, base_width*_m)])
        self.db1 = MakeConv2DSeq(base_width*_m, base_width*_m, base_width*int(_m/2), 2)

        _m = 2**2
        self.up2 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m, base_width*_m)])
        self.db2 = MakeConv2DSeq(base_width*_m, base_width*_m, base_width*int(_m/2), 2)

        _m = 2**1
        self.up3 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m, base_width*_m)])
        self.db3 = MakeConv2DSeq(base_width*_m, base_width*_m, base_width*int(_m/2), 2)

        _m = 2**0
        self.up4 = nn.Sequential(
            *[nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            *MakeConv2DBlock(base_width*_m, base_width*_m)])
        self.db4 = MakeConv2DSeq(base_width*_m, base_width*_m, base_width, 2)

        self.fin_out = nn.Sequential(nn.Conv2d(base_width, out_channels, kernel_size=3, padding=1))

    def forward(self, b5):

        up1 = self.up1(b5)
        db1 = self.db1(up1)

        up2 = self.up2(db1)
        db2 = self.db2(up2)

        up3 = self.up3(db2)
        db3 = self.db3(up3)

        up4 = self.up4(db3)
        db4 = self.db4(up4)

        out = self.fin_out(db4)

        return out