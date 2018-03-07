# Tutorial Build Your Develop Environment and Contribute



## Pipeline in Shifu

![Shifu Pipeline](../images/pipline/pipline.png)

This picture shows Shifu's whole pipeline and just do some json configurations, whole pipeline will be executed and later you can get your first ML model.

## How to Install pyshifu

The easiest way to install pyshifu is using pip:     
```bazaar
pip install pyshifu
```
or use conda:         
```bazaar
conda install pyshifu
```

or login into horton:
```bazaar
ssh phxbastion2.phx.paypal.com
su website
```

## How to Run Shifu Pipeline

Shifu will parse your Hadoop platform settings and set all Hadoop conf for Shifu runtime. 

* import shifu
    ```
    from pyshifu import shifu
    ```

* shifu new    
API: shifu.new(model_name, work_directory)
    ```
    >>> shifu.new("new_model", "/Users/haifwu/Model")
    ```
    shifu.new(model_name, work_directory)
    parameters: 
        model_name: the name of the new model
        work_directory: the new model will be created under this work directory
    This command will create a new dataset folder for training, in the new folder, You will find some auto-created files:
    1. ModelConfig.json: Some input and model pipeline configurations and which will be discussed more later.
       
       ```json
         "basic" : {
            "name" : "turorial",
            "author" : "shifu",
            "description" : "Created at 2016-11-28 20:08:31",
            "version" : "0.2.0",
            "runMode" : "DIST",
            "postTrainOn" : false,
            "customPaths" : { }
         },
         "dataSet" : {
            "source" : "HDFS",
            "dataPath" : "hdfs:/user/shifu/DataSet1",
            "dataDelimiter" : "|",
            "headerPath" : "hdfs:/user/shifu/DataSet1/.pig_header",
            "headerDelimiter" : "|",
            "filterExpressions" : "",
            "weightColumnName" : "",
            "targetColumnName" : "diagnosis",
            "posTags" : [ "M" ],
            "negTags" : [ "B" ],
            "missingOrInvalidValues" : [ "", "*", "#", "?", "null", "~" ],
            "metaColumnNameFile" : "columns/meta.column.names",
            "categoricalColumnNameFile" : "columns/categorical.column.names"
          },
          ...
       ```
       
       * basic::name is the name of your data set and is the same as data set folder
       * basic::runMode can be 'local' or 'mapred'/'dist', by default is local which means run jobs on local machine; 'mapred'/'dist' means jobs are running in Hadoop platform
       * dataSet::source has two types: 'local' or 'hdfs' which means data in local or hadoop file system.
       * dataSet::dataPath is the data path for model training. If 'hdfs' source, dataPath should be files or folders in HDFS; Regex expression is supported here, for example: you can use such dataPath: hdfs:/user/shifu/{2016/01,2016/02}/trainingdata; you can take our example data in ${SHIFU_HOME}/example/cancer-judgement/ and push it into your HDFS for testing.
       * dataSet::headerPath: which is a file for data header, if it is null, first line of your dataPath will be parsed as headers.
       * dataSet::dataDelimiter & dataSet::headerDelimiter: how to parse headerPath and dataPath files
       * dataSet::filterExpressions: User-specified expressions like ' columnA == '2' ' are supported to filter data in stats and training
       * dataSet::weightColumnName: if your training or stats are based on weighted columns. For example in our risk training, it should be dollar columns which means our target is to save dollar-wise loss. If not set, it is unit-wised.
       * dataSet::targetColumnName: which column is your target column, please make sure it is successfully configured.
       * dataSet::posTags: elements in such list will be treated as positive like 1 in binary classification.
       * dataSet::negTags: elements in such list will be treated as negative like 0 in binary classification.
       * dataSet::missingOrInvalidValues: values in such list will be treated as invalid.
       * dataSet::metaColumnNameFile: meta column config file which is by default and created well in columns folder
       * dataSet::categoricalColumnNameFile: categorical column config files which list all categorical features and will be set in init step

    2. columns/categorical.column.names: Empty file which specifies categorical columns
    3. columns/Eval1score.meta.column.names: Empty file which specifies evaluation meta columns
    4. columns/forceremove.column.names: Empty file which specifies columns which will be forced to remove in model training
    5. columns/forceselect.column.names: Empty file which specifies columns which will be forced to selected in model training
    6. columns/meta.column.names: Empty file which specifies columns like ID column

    Mostly in this part, user should config basic and dataSet path well, then in next steps all running are based on successful data paths and modes.    
   
* shifu init
    ```
    >>> shifu.init()
    ```

     All next steps from init should be run in <data set folder>, this design is to make sure your running in different data sets are doable. 

     Init step will create another important file which is ColumnConfig.json near ModelConfig.json. ColumnConfig.json is a json file includes all statistic info and mostly info will be filled later in 'stats' step.
     
     So far numerical or categorical columns must be specified by users in columns/categorical.column.names. This is very important to do the right column stats and transform. Please do make sure you configure categorical columns here well.

* shifu stats
    ```
    >>> shifu.stats()
    ```

     Stats step is used to collect statistics like mean, stddev, ks and other info by using MapReduce/Pig/Spark jobs.

     ```json
           "stats" : {
              "maxNumBin" : 10,
              "binningMethod" : "EqualPositive",
              "sampleRate" : 0.8,
              "sampleNegOnly" : false,
              "binningAlgorithm" : "SPDTI"
           },
     ```
     
     * stats::maxNumBin: how many bins (buckets) in each numerical columns will be computed. The more the better results but more computations. Better in 10-50. For categorical features
     * stats::binningMethod: What kind of binning method: 'EqualPositive' in each bin the same positive number of records, others like 'EqualNegative', 'EqualTotal' and 'EqualInterval' ...
     * stats::sampleRate: usually you can do sampling for stats to accelerate this steps
     * stats::sampleNegOnly: If only sample negative records, this is useful for some cases negative are much more that positive records. 
     * stats::binningAlgorithm: By default it is 'SPDTI' which is histogram-based statistics. 

     After stats running, you can find ColumnConfig.json updated in data set folder with mean, ks, binning and other stats info which can be used in next steps.

* shifu norm
    ```
    >>> shifu.norm()
    ```
     
     For logistic regression or neural network models, training input data should be normalized like z-score normalization or maxmin normalization. Such normalization methods are both supported in this step.
     
     For tree ensemble models like Random Forest or Gradient Boosted Trees, no need norm step after shifu 0.10.x. while in shifu 0.9.x, norm is still needed, actually norm is just to cleaning data for further training.

     ```json
        "normalize" : {
           "stdDevCutOff" : 4.0,
           "sampleRate" : 1.0,
           "sampleNegOnly" : false,
           "normType" : "ZSCALE"
        },
     ```
     
     * normalize::stdDevCutOff: stddev cut off for zscore, if abs value after zscore are still larger than this value, will be cut off to this value.
     * normalize::sampleRate: samplining data for next step training.
     * normalize::sampleNegOnly: If only sample negative records, this is useful for some cases negative are much more that positive records. 
     * normalize::normType: can be 'zscale'/'zscore', 'maxmin', 'woe'.

     'woe' norm type is very important, it leverages binning information to transform numerical values into discrete values. This norm type improves model stability very well.
     
* shifu varsel
    ```
    >>> shifu.varsel()
    ```

  After stats and norm, varsel step is used for feature selection according to some statistic information like KS or IV value. 

  ```json
  "varSelect" : {
    "forceEnable" : true,
    "forceSelectColumnNameFile" : "columns/forceselect.column.names",
    "forceRemoveColumnNameFile" : "columns/forceremove.column.names",
    "filterEnable" : true,
    "filterNum" : 100,
    "filterOutRatio" : 0.05,
    "filterBy" : "FI",
    "missingRateThreshold" : 0.98,
    "params" : null
  }
  ```
     * varSelect::forceEnable: If enable force remove and force selection features
     * varSelect::filterEnable: If enable filter in variable selection
     * varSelect::filterNum: The number of variables need to be selected for model training, filterNum has higher priority than filterOutRatio, in another word, once filterNum is set filterOutRatio is ignored.
     * varSelect::filterOutRatio: ratio of variables should be filtered out after running **shifu varselect**
     * varSelect::filterBy: type of variable selection type, like 'KS', 'IV', 'SE', 'FI'

   For any detailed information, please check [https://github.com/ShifuML/shifu/wiki/Variable-Selection-in-Shifu](Variable Selection in Shifu)


* shifu train
    ```
    >>> shifu.train()
    ```
    
     One of Shifu's pros is that training in Shifu is very powerful:
     
     * Distributed Logistic Regression / Neural Network / Tree Ensemble training are supported if runMode is 'dist'
     * Bagging and validation are native supported with just a configuration
     * All distributed training are fault tolerance and tested well in busy shared cluster. Straggler issue is solved well to make sure training running smoothly in Hadoop cluster.

     ```json
        "train" : {
           "baggingNum" : 5,
           "baggingWithReplacement" : true,
           "baggingSampleRate" : 1.0,
           "validSetRate" : 0.2,
           "numTrainEpochs" : 200,
           "isContinuous" : false,
           "workerThreadCount" : 4,
           "algorithm" : "NN",
           "params" : {
              "NumHiddenLayers" : 1,
              "ActivationFunc" : [ "tanh" ],
              "NumHiddenNodes" : [ 50 ],
              "RegularizedConstant" : 0.0,
              "LearningRate" : 0.1,
              "Propagation" : "R"
            },
        },
     ```

     * train::baggingNum: How many models will be trained.
     * train::baggingWithReplacement: If bagging is combined with replacement sampling like Random Forest.
     * train::baggingSampleRate: How many training data will be used in training and validation, by default it is 1.
     * train::validSetRate: How many data are for validation data, others are for training
     * train::numTrainEpochs: How many iterations are used to train NN/LR models
     * train::isContinuous: If existing models in models folder and such one is set to true, training will start from existing NN/LR/GBT models. Such feature is not supported in Random forest. 
     * train::workerThreadCount: Data are distributed in each Hadoop task, in each task, how many threads are used to training model in parallel. This can accelerate training. By default it is 4. In a shared cluster better set to 4-8. Set it higher sometimes may have CPU issues in a shared cluster without set CPU isolation well.
     * train::algorithm: 'NN', 'LR', 'GBT', 'RF' are supported so far in Shifu. For different algorithm, different train::params should be set well.
     * train::params::NumHiddenLayers: How many hidden layers in Neural network
     * train::params::ActivationFunc: Activation functions in each hidden laryer. 
     * train::params::NumHiddenNodes: Hidden nodes in each layer.
     * train::params::LearningRate: Learning rate for neural network building
     * train::params::Propagation: 'R', 'Q', 'B' are supported well, here 'B' is BackPropagation, 'Q' is QuickPropagation. 'R' is ResilentPropagation. By default it is 'Q'. 

     After training is finished, you can find models trained in local folder <data set>/models/. Which can be used in production or evaluation step.

* shifu eval
    ```
    >>> shifu.eval()
    ```

     Evaluation step is to evaluate models you just trained. If multiple models are found in models folder. all will be evaluated and 'mean' model score is used to do final performance report.

     ```json
      "evals" : [ {
          "name" : "Eval1",
          "dataSet" : {
            "source" : "HDFS",
            "dataPath" : "hdfs:/user/shifu/EvalSet1",
            "validationDataPath" : null,
            "dataDelimiter" : "|",
            "headerPath" : "hdfs:/user/shifu/EvalSet1/.pig_header",
            "headerDelimiter" : "|",
            "filterExpressions" : "",
            "weightColumnName" : "",
            "targetColumnName" : "diagnosis",
            "posTags" : [ "M" ],
            "negTags" : [ "B" ],
            "missingOrInvalidValues" : [ "", "*", "#", "?", "null", "~" ],
            "metaColumnNameFile" : "columns/meta.column.names",
            "categoricalColumnNameFile" : "columns/categorical.column.names"
         },
       "performanceBucketNum" : 10,
       "performanceScoreSelector" : "mean",
       "scoreMetaColumnNameFile" : "columns/Eval1score.meta.column.names",
     }
     ```
     
     * Evaluation supports multiple evaluation data set setting.
     * evals::dataSet: most time are the same as the ones in dataSet part
     * evals::performanceBucketNum: Bucket number to check points in final report.
     * evals::performanceScoreSelector: By default it is mean value for all bagging models.

     Evaluation results can be found in console like AUC or Gain Chart, Precision-Recal chart, and html format report can be found in evaluation local folder. Then you can get your models and model performance.
 
     