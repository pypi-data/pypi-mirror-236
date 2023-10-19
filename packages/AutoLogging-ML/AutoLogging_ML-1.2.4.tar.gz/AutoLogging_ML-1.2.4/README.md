# Update- 1. Given the option to use classification autologging for both small and large datasets. 
# 2. The module can now work on regression datasets with negative values.
This project is about a python package for automated logging and visualization of metrics of classfication and regression algorithms in machine learning.

Features
* The module covers both regression and classification tasks. 
* The module integrates a wide range of metrics related to classification and regression
* The module can provide a barplot of the specified metrics from the specified subset of data
* The module can provide the confusion matrix for all the different ML algorithms
* The module can save automatically save the best model (highest validation accuracy for classification and lowest validation mse for regression)
* The module can arrange the results table based on the user of the request
* The module can provide the classification reports for all the different ML algorithms


Functions
* Train and log for classification. All the classifiers are trained on the datasets and the results (accuracy, precision, recall, F1) are logged onto a dataframe which is displayed to the user. This function applies around 16 different classification algorithms as mentioned below:-
'svm-linear'

'svm-rbf'

'svm-poly'

'knn'

'naive bayes'

'decision tree'

'random forest'

'adaboost'

'gradient boost'

'xgboost'

'logistic regression'

'bagging classifier'

'extra tree classifier'

'linear discriminant analysis'

'quadratic discriminant analysis'

'cat boost classifier'

returns- best model and result table


* Get confusion matrix. This function helps to get the confusion matrices for all the classification algorithms on the specified set (training/validation)

* Get classification report. This function helps to get the classification reports for all the classification algorithms on the specified set (training/validation)

* Sort table by metric. This function helps to arrange the result table as per the metric requested by the user.

* Display metric plots. This function plots a barplot for the comparative analysis of the classication algorithms on the specified metric and on the specified subset. 

* Train and log for regression. All the regressors are trained on the datasets and the results (mae, mse, msle, median error, mape, max error) are logged onto a dataframe which is displayed to the user. This function applies around 13 different regression algorithms as mentioned below:- 
'linear regression'

'sgd regression'

'ridge regression'

'elastic net'

'decision tree regression'

'random forest regression'

'adaboost regression'

'gradient boost regression'

'xgboost regression'

'bagging regression'

'hist gradient boosting regression'

'extra tree regression'

'cat boost regression'

Syntax

from AutoLogging_ML import AutoLogger

# train_and_log_classification

a= AutoLogger.train_and_log_classification(x_train,x_test,y_train,y_test)
print(a)

a stores the dataframe comprising of all the metric values for the training and validation datasets. 

# get_metric_plots_classification

AutoLogger.get_metric_plots_classification(a,subset='None',metric='None')

returns the barplot of all the algorithms on the mentioned metric and mentioned subset.

subset= 'training' , 'validation'

metric= 'accuracy' , 'precision', 'recall', 'f1', 'msle', 'median absolute error', 'maximum error'

# get_confusion_matrix

AutoLogger.get_confusion_matrix(a,subset='None')

returns the confusion matrix of all the classification algorithms on the specified subset

subset= 'training'. 'validation'

# get_clasification_report

AutoLogger.get_classification_report(a,subset='None')

returns the classification reports of all the classification algorithms on the specified subset

subset= 'training'. 'validation'

# train_and_log_regression

b= AutoLogger.train_and_log_regression(x_train, x_test, y_train, y_test)

print(b)


b stores the dataframe comprising of all the metric values for the training and validation datasets.

# get_metric_plots_regression

AutoLogger.get_metric_plots_regression(b,subset=None,metric=None)


returns the barplot of all the algorithms on the mentioned metric and mentioned subset.

subset= 'training' , 'validation'

metric= 'mae' , 'mse', 'mape', 'r2', 'msle', 'median absolute error', 'maximum error'

# sort_table_by_metric

AutoLogger.sort_table_by_metric