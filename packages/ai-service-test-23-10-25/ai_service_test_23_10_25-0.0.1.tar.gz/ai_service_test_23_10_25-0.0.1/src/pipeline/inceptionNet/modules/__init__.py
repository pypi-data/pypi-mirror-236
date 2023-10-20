from torchvision import models

import numpy as np
import torch, time

__all__ = ["InferInceptionNet"]


class ManagerInceptionNet:

    def __init__(self, pathModel, numLabel, device):
        self.device = device
        self.model = models.inception_v3(pretrained=True)

        fc_in_features = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(fc_in_features, numLabel)

        self.model.load_state_dict(torch.load(pathModel, map_location=device))
        self.model = self.model.to(device)
        self.model.eval()
        self.timeLast = time.time()

    def __call__(self, data):
        self.timeLast = time.time()
        return self.model(data)


class InferInceptionNet:

    def __init__(self, paraDic):
        self.name = type(self).__name__
        self.tag = ["model"]
        self.connection = paraDic["connection"]
        self.pathModel = paraDic["pathModel"]
        self.numLabel = paraDic["numLabel"]
        self.device = paraDic["device"]
        self.batchSize = paraDic["batchSize"]

    def LoadModel(self, pathModel):
        self.pathModel = pathModel
        return ManagerInceptionNet(self.pathModel, self.numLabel, self.device)

    def SetModel(self, manager):
        self.model = manager
        self.device = manager.device

    def __call__(self, pack):
        imgs = pack["data"]
        codes = pack["code"]

        for idx in range(len(codes)):
            codes[idx]["step"].append(self.name)

        outputs = []
        for idx in range(0, imgs.shape[0], self.batchSize):
            img = imgs[idx:idx+self.batchSize].to(self.device)

            outputs.extend(self.model(img).detach().cpu())

        if 'img' in locals():
            del img
            with torch.cuda.device(self.device):
                torch.cuda.empty_cache()

        if len(outputs) != 0:
            pack = {"data" : imgs, "code" : np.array(codes), "score" : torch.stack(outputs)}
        else:
            pack = {"data" : torch.Tensor([]), "code" : np.array([]), "score" : torch.Tensor([])}

        packNewList = [pack]
    
        packOutList = []
        for pack, outList in zip(packNewList, self.connection["out"]):
            for out in outList:
                packOutList.append({"pack" : pack, "out" : out})
        return packOutList