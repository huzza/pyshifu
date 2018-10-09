from __future__ import absolute_import, division, print_function, unicode_literals
from pyshifu.core.shell import Shell


from pyshifu.core.exception.base_exception import ShifuException


class Shifu(Shell):
    def __init__(self):
        super(Shifu, self).__init__()

    def use(self, model_name, work_dir):
        self._use_existing_model(work_dir, model_name)
        print('Enter to model workspace %s, execute commands for %s' % (self._model_dir, model_name))

    def new(self, name, work_dir=None):
        try:
            self._init_working_directory(work_dir, name)
        except ShifuException as exception:
            print (exception.get_message())
        self._run_command_new(name)


    def init(self, run_mode=None, source=None, dataPath=None, validationDataPath=None, dataDelimiter=None,
             headerPath=None, headerDelimiter=None, filterExpressions=None, weightColumnName=None,
             targetColumnName=None, posTags=None, negTags=None, missingOrInvalidValues=None, metaColumnNameFile=None,
             categoricalColumnNameFile=None):
        if run_mode:
            self._update_config("basic", {"runMode": run_mode})
        config_map = {}
        if source:
            config_map["source"] = source
        if dataPath:
            config_map["dataPath"] = dataPath
        if validationDataPath:
            config_map["validationDataPath"] = validationDataPath
        if dataDelimiter:
            config_map["dataDelimiter"] = dataDelimiter
        if headerPath:
            config_map["headerPath"] = headerPath
        if headerDelimiter:
            config_map["headerDelimiter"] = headerDelimiter
        if filterExpressions:
            config_map["filterExpressions"] = filterExpressions
        if weightColumnName:
            config_map["weightColumnName"] = weightColumnName
        if targetColumnName:
            config_map["targetColumnName"] = targetColumnName
        if posTags:
            config_map["posTags"] = posTags
        if negTags:
            config_map["negTags"] = negTags
        if missingOrInvalidValues:
            config_map["missingOrInvalidValues"] = missingOrInvalidValues
        if metaColumnNameFile:
            config_map["metaColumnNameFile"] = metaColumnNameFile
        if categoricalColumnNameFile:
            config_map["categoricalColumnNameFile"] = categoricalColumnNameFile
        self._update_config("dataSet", config_map)
        self._run_command("init", "stats")

    def stats(self, maxNumBin=None, cateMaxNumBin=None, binningMethod=None, sampleRate=None, sampleNegOnly=None,
              binningAlgorithm=None, psiColumnName=None):
        config_map = {}
        if maxNumBin:
            config_map["maxNumBin"] = maxNumBin
        if cateMaxNumBin:
            config_map["cateMaxNumBin"] = cateMaxNumBin
        if binningMethod:
            config_map["binningMethod"] = binningMethod
        if sampleRate:
            config_map["sampleRate"] = sampleRate
        if sampleNegOnly:
            config_map["sampleNegOnly"] = sampleNegOnly
        if binningAlgorithm:
            config_map["binningAlgorithm"] = binningAlgorithm
        if psiColumnName:
            config_map["psiColumnName"] = psiColumnName
        self._update_config("stats", config_map)
        self._run_command("stats", "norm")

    def norm(self, stdDevCutOff=None, sampleRate=None, sampleNegOnly=None, normType=None):
        config_map = {}
        if sampleRate:
            config_map["sampleRate"] = sampleRate
        if sampleNegOnly:
            config_map["sampleNegOnly"] = sampleNegOnly
        if normType:
            config_map["normType"] = normType
        self._update_config("normalize", config_map)
        self._run_command("norm", "varsel")

    def varsel(self, forceEnable=None, candidateColumnNameFile=None, forceSelectColumnNameFile=None,
               forceRemoveColumnNameFile=None, filterEnable=None, filterNum=None, filterBy=None, filterOutRatio=None,
               autoFilterEnable=None, missingRateThreshold=None, correlationThreshold=None, minIvThreshold=None,
               minKsThreshold=None, postCorrelationMetric=None, params=None):
        config_map = {}
        if forceEnable:
            config_map["forceEnable"] = forceEnable
        if candidateColumnNameFile:
            config_map["candidateColumnNameFile"] = candidateColumnNameFile
        if forceSelectColumnNameFile:
            config_map["forceSelectColumnNameFile"] = forceSelectColumnNameFile
        if forceRemoveColumnNameFile:
            config_map["forceRemoveColumnNameFile"] = forceRemoveColumnNameFile
        if filterEnable:
            config_map["filterEnable"] = filterEnable
        if filterNum:
            config_map["filterNum"] = filterNum
        if filterBy:
            config_map["filterBy"] = filterBy
        if filterOutRatio:
            config_map["filterOutRatio"] = filterOutRatio
        if autoFilterEnable:
            config_map["autoFilterEnable"] = autoFilterEnable
        if missingRateThreshold:
            config_map["missingRateThreshold"] = missingRateThreshold
        if correlationThreshold:
            config_map["correlationThreshold"] = correlationThreshold
        if minIvThreshold:
            config_map["minIvThreshold"] = minIvThreshold
        if minKsThreshold:
            config_map["minKsThreshold"] = minKsThreshold
        if postCorrelationMetric:
            config_map["postCorrelationMetric"] = postCorrelationMetric
        if params:
            config_map["params"] = params
        self._update_config("varSelect", config_map)
        self._run_command("varsel", "train")

    def train(self, baggingNum=None, baggingWithReplacement=None, baggingSampleRate=None, validSetRate=None,
              numTrainEpochs=None, isContinuous=None, workerThreadCount=None, algorithm=None, params=None,
              customPaths=None):
        config_map = {}
        if baggingNum:
            config_map["baggingNum"] = baggingNum
        if baggingWithReplacement:
            config_map["baggingWithReplacement"] = baggingWithReplacement
        if baggingSampleRate:
            config_map["baggingSampleRate"] = baggingSampleRate
        if validSetRate:
            config_map["validSetRate"] = validSetRate
        if numTrainEpochs:
            config_map["numTrainEpochs"] = numTrainEpochs
        if isContinuous:
            config_map["isContinuous"] = isContinuous
        if workerThreadCount:
            config_map["workerThreadCount"] = workerThreadCount
        if algorithm:
            config_map["algorithm"] = algorithm
        if params:
            config_map["params"] = params
        if customPaths:
            config_map["customPaths"] = customPaths
        self._update_config("train", config_map)
        self._run_command("train", "eval")

    def eval(self, name=None, dataSet=None, performanceBucketNum=None, performanceScoreSelector=None,
             scoreMetaColumnNameFile=None, customPaths=None):
        config_map = {}
        if name:
            config_map["name"] = name
        if dataSet:
            config_map["dataSet"] = dataSet
        if performanceBucketNum:
            config_map["performanceBucketNum"] = performanceBucketNum
        if performanceScoreSelector:
            config_map["performanceScoreSelector"] = performanceScoreSelector
        if scoreMetaColumnNameFile:
            config_map["scoreMetaColumnNameFile"] = scoreMetaColumnNameFile
        if customPaths:
            config_map["customPaths"] = customPaths
        self._update_config_eval(config_map)
        self._run_command("eval")





