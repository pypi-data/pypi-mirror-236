This module is about automated data cleaning of datasets for machine learning and deep learning applications. The initial version 

comprises of data cleaning operations with regards to the task of classification. Futher releases will incorporate method for 

regression and other A.I tasks. 

# Features
The module deals with the following errors in the dataset automatically:-

    * Duplicate rows and columns

    * Non-numerical datatypes

    * Missing data

    * Different ranges of data

The module also returns a summary descirption of the operations that are performed on the dataset during the process of data cleaning.

The module is designed in such a way that it handles errors and exceptions. Any errors while performing an operation doesnt affect the 

performance of the other operation.

## Handling duplicates

The module will automatically remove the duplicate rows and columns in the dataset.

## Non-numerical datatypes

The module will automatically convert the non-numerical datatypes to numerical using labelencoder.

## Missing data

The module will remove the rows that have null values, only if the dataset is very large. Or else, it will perform imputation using 

statistical measures or machine learning models. If the method is specified by the user, the particular one will be executed, or else, the 

default imputation method (standard deviation).

## Different ranges of data

The module will deal with this issue based on the type of classification/regression model the user wishes to perform. Generally models

that use gradient descent like linear regression, neural nets and distance based algorithms like

KMeans and KNN require standardisation technique, whereas other algorithms like SVM, naive bayes require normalization technique and 

algorithms like decision tree, random forest, bagging and boosting algorithms require no scaling at all.

# SYNTAX

from AutoDataCleaner import AutoDataClean

data_cleaning = AutoDataClean.DataCleaner(data, algo=None,method=None,target_name='Outcome',imputer='knn',k_neighbors=5)

## To get the data

data=data_cleaning.data

## To get the description of the operations performed

print(data_cleaning.descriptions)


## Options for the argument algo

'SVM', 'ANN', 'KNN', 'Naive Bayes', 'KMeans', 'LDA' ,'QDA', 'Logistic Regression', 'Decision Tree', 'Random Forest', 'xgboost', 'Gradient 

Boosting', 'adaboost'

## Options for the argument method

'bfill', 'ffill', 'mean', 'median', 'mode', 'variance', 'std'

## Options for the argument imputer

'simple', 'knn'
