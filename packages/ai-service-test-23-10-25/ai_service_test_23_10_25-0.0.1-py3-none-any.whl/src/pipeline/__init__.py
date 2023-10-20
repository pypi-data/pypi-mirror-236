from .DRAEM import *
from .inceptionNet import *
from .prepare import *

import numpy as np
import logging.config
import threading, traceback, logging, pickle, torch, json, time, os


processClassDic = {
    "Input000001" : Input000001,
    "PrePro000001" : PrePro000001,
    "PrePro000002" : PrePro000002,
    "PrePro000011" : PrePro000011,
    "PostPro000001" : PostPro000001,
    "PostPro000002" : PostPro000002,
    "Output000001" : Output000001,
    "ClipMaker000001" : ClipMaker000001,
    "ClipSumm000001" : ClipSumm000001,
    "InferDRAEM" : InferDRAEM,
    "InferInceptionNet" : InferInceptionNet,
    "Over000001" : Over000001
}

class ModelPipeline:

    def __init__(self, volLimit=1*1024**3, pathConf="config/logger_engine.json"):
        self.volLimit = volLimit
        self.pathConf = pathConf
        self.specDic = {}
        self.moduleLoadDic = {}
        self.modelLoaded = {}

        self.initLogger()
        self.initQueue()
        self.initThreadInference()

    def initLogger(self):
        logDic = json.load(open(self.pathConf))
        self.pathLogDir = ""
        for path in logDic["handlers"]["file"]["filename"].split('/')[:-1]:
            self.pathLogDir = os.path.join(self.pathLogDir, path)
            if not os.path.isdir(self.pathLogDir):
                os.mkdir(self.pathLogDir)
        logging.config.dictConfig(logDic)
        self.logger = logging.getLogger("engine_logger")

    def initQueue(self):
        self.deltaTime = 1/60
        self.queueData = []
        self.queueCode = []
        self.queueSpec = []
        self.outputList = []
        self.volTotal = 0

    def initThreadInference(self):
        self.numInitBatch = 32
        self.isRun = False

        self.mainThread = threading.Thread(target=self.master, args=[self])
        self.mainThread.start()

    def writeLog(self, specID, nameModule, packList):
        if "code" in packList:
            for code in packList["code"]:
                strLog = "spec:%s|module:%s|id:%s"%(specID, nameModule, code["image_id"])
                if "clipXYWH-global" in code:
                    strLog += "|clip:" + str(code["clipXYWH-global"])
                self.logger.info(strLog)

    def SetRun(self, isRun):
        self.isRun = isRun
        return self.isRun

    def Put(self, pack, specID):
        if self.HasSpec(specID):
            vol = pack["data"].__sizeof__()
            if self.volTotal+vol < self.volLimit:
                self.queueData.append(pack["data"])
                self.queueCode.append(pack["code"])
                self.queueSpec.append(specID)
                self.volTotal += vol
                isPut = True
                return {"image_id" : pack["code"]["image_id"], "input" : isPut, "remain" : self.volLimit - self.volTotal}
            else:
                isPut = False
                self.logger.error(str({"input" : isPut, "error" : "queue volume limit"}))
                return {"image_id" : pack["code"]["image_id"], "input" : isPut, "error" : "queue volume limit"}
        else:
            isPut = False
            self.logger.error(str({"input" : isPut, "error" : "spec not found"}))
            return {"image_id" : pack["code"]["image_id"], "input" : isPut, "error" : "spec not found"}

    def allot(self, num):
        length = len(self.queueSpec)
        specID = self.queueSpec[0]
        queueSpec = np.array(self.queueSpec[:length])
        idxList = np.where(queueSpec == specID)[0][:num]
        datas = []
        codes = []
        for idx in idxList:
            datas.append(self.queueData[idx])
            codes.append(self.queueCode[idx])
        return {"data" : datas, "code" : np.array(codes)}, specID, idxList

    def remove(self, idxList):
        for i, idx in enumerate(idxList):
            self.volTotal -= self.queueData.pop(idx-i).__sizeof__()
            self.queueCode.pop(idx-i)
            self.queueSpec.pop(idx-i)

    def master(self, _):
        while True:
            if self.isRun:
                if len(self.queueSpec) != 0:
                    packInput = self.allot(self.numInitBatch)
                    pack, specID, idxList = packInput
                    self.outputList += self.inference([pack], specID)
                    self.remove(idxList)
            time.sleep(self.deltaTime)

    def Get(self):
        if len(self.outputList) == 0:
            return None
        else:
            return self.outputList.pop(0)

    def ImportModules(self, specID, parameters):
        errorList = []
        if not self.HasSpec(specID):
            self.specDic[specID] = parameters
            self.moduleLoadDic[specID] = {}
            for processID, processDic in parameters.items():
                try:
                    processName = processDic["name"]
                    processPara = processDic["para"]
                    self.moduleLoadDic[specID][processID] = processClassDic[processName](processPara)
                    if "model" in self.moduleLoadDic[specID][processID].tag:
                        pathModel = self.moduleLoadDic[specID][processID].pathModel
                        if pathModel in self.modelLoaded:
                            self.moduleLoadDic[specID][processID].model = self.modelLoaded[pathModel]
                        elif os.path.isfile(pathModel):
                            self.modelLoaded[pathModel] = self.moduleLoadDic[specID][processID].LoadModel(pathModel)
                            self.moduleLoadDic[specID][processID].SetModel(self.modelLoaded[pathModel])
                        else:
                            self.logger.error(str({"specID" : specID, "processID" : processID, "error" : "model file not found"}))
                            errorList.append({"specID" : specID, "processID" : processID, "error" : "model file not found"})
                except:
                    self.logger.error(str({"specID" : specID, "processID" : processID, "error" : "process not found"}))
                    errorList.append({"specID" : specID, "processID" : processID, "error" : "process not found"})
            if len(errorList) > 0:
                del self.moduleLoadDic[specID], self.specDic[specID]
        return errorList

    def PreLoadModels(self, parameters):
        errorList = []
        for processID, processDic in parameters.items():
            try:
                processName = processDic["name"]
                processPara = processDic["para"]
                moduleLoad = processClassDic[processName](processPara)
                if "model" in moduleLoad.tag:
                    pathModel = processPara["pathModel"]
                    if os.path.isfile(pathModel):
                        if pathModel not in self.modelLoaded:
                            self.modelLoaded[pathModel] = moduleLoad.LoadModel(pathModel)
                    else:
                        self.logger.error(str({"processID" : processID, "error" : "model file not found"}))
                        errorList.append({"processID" : processID, "error" : "model file not found"})
            except:
                self.logger.error(str({"processID" : processID, "error" : "process not found"}))
                errorList.append({"processID" : processID, "error" : "process not found"})
        return errorList

    def HasSpec(self, specID):
        return specID in self.moduleLoadDic

    def makeOutSummary(self, linkList):
        return ["%s|%s"%(src, cnt) for src, cnt in zip(*np.unique(linkList, return_counts=True))]

    def merge(self, packList):
        typeKey = {}
        packNew = {}
        for idx, pack in enumerate(packList):
            if idx == 0:
                keyList = list(pack.keys())
                for key in keyList:
                    typeKey[key] = type(pack[key])
                    packNew[key] = []
            for key in keyList:
                packNew[key].extend(pack[key])
        for key in packNew:
            if typeKey[key] == np.ndarray:
                packNew[key] = np.array(packNew[key])
            elif typeKey[key] == torch.Tensor:
                if len(packNew[key]) > 0:
                    packNew[key] = torch.stack(packNew[key])
                else:
                    packNew[key] = torch.Tensor([])
        return packNew

    def inference(self, packList, specID):
        if self.HasSpec(specID):
            packStorage = []
            for idx, pack in enumerate(packList):
                packStorage.append({"pack" : pack, "out" : "start%d"%idx})
            outputFreeze = {}
            outputFreeze["init"] = packStorage

            outList = self.makeOutSummary([packDic["out"] for packDic in packStorage])
            outListPre = []

            try:
                while outListPre != outList:
                    outListPre = outList
                    for module in self.moduleLoadDic[specID].values():
                        inList = self.makeOutSummary(np.hstack(module.connection["in"]))
                        inoutList = np.intersect1d(outList, inList).tolist()
                        if (inoutList == inList):
                            args = []
                            idxDel = []
                            for inList in module.connection["in"]:
                                packList = []
                                for idx, packOut in enumerate(packStorage):
                                    if packOut["out"] in inList:
                                        packList.append(packOut["pack"])
                                        idxDel.append(idx)
                                packList = self.merge(packList)
                                self.writeLog(specID, module.name, packList)
                                args.append(packList)

                            packStorageNew = []
                            for idx in range(len(packStorage)):
                                if idx not in idxDel:
                                    packStorageNew.append(packStorage[idx])
                            packStorage = packStorageNew
                            del packStorageNew

                            outputFreeze["during"] = [module.name, args]
                            packStorage.extend(module(*args))
                            outList = self.makeOutSummary([packDic["out"] for packDic in packStorage])
                output = []
                for packDic in packStorage:
                    if packDic["out"] == "end":
                        output += packDic["pack"]["output"]
                return output
            except Exception as e:
                pickle.dump(outputFreeze, open("%s/freeze|%s.dump"%(self.pathLogDir, time.strftime("%Y-%m-%d|%H:%M:%S")), "wb"))
                output = []
                for packOut in outputFreeze["init"]:
                    for code in packOut["pack"]["code"]:
                        err = {"image_id" : code["image_id"], "specID" : specID, "processID" : outputFreeze["during"][0], "error" : "process error"}
                        self.logger.error(str(err))
                        output.append(err)
                self.logger.error(traceback.format_exc())
                return output
        else:
            output = []
            for pack in packList:
                err = {"image_id" : pack["code"]["image_id"], "specID" : specID, "processID" : "None", "error" : "spec not found"}
                self.logger.error(str(err))
                output.append(err)
            return output
