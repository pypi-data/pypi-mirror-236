import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from sklearn.utils import resample

class DataCleaner:

    def __init__(self, data, algo, target_name, method, imputer=None, k_neighbors=None):
        self.data = data
        self.algo = algo
        self.target_name = target_name
        self.method = method
        self.imputer = imputer
        self.k_neighbors = k_neighbors
        self.descriptions = []
        self.method_errors = {}

        try:
            self.data, desc_duplicate = self.treat_duplicate(self.data)
            self.descriptions.append(desc_duplicate)
        except Exception as e:
            self.method_errors['treat_duplicate'] = str(e)

        try:
            self.data, desc_encoding = self.treat_encoding(self.data, self.target_name)
            self.descriptions.append(desc_encoding)
        except Exception as e:
            self.method_errors['treat_encoding'] = str(e)

        try:
            self.data, desc_missing_data = self.treat_missing_data(self.data, self.method, self.imputer, self.k_neighbors)
            self.descriptions.append(desc_missing_data)
        except Exception as e:
            self.method_errors['treat_missing_data'] = str(e)

        try:
            self.data, desc_feature_scaling = self.feature_scaling(self.data, self.algo, self.target_name)
            self.descriptions.append(desc_feature_scaling)
        except Exception as e:
            self.method_errors['feature_scaling'] = str(e)
        self.method_descriptions = ' '.join(self.descriptions)

        if self.method_errors:
            print("Errors occurred in the following methods:")
            for method, error in self.method_errors.items():
                print(f"{method}: {error}")

    def treat_duplicate(self, data):
        data = data.drop_duplicates()
        desc = f'The dataset comprises of {data.duplicated().sum()} duplicate rows, and those rows have been dropped to eliminate redundancy of data.'
        return data, desc

    def treat_encoding(self, data, target_name):
        for col in data.columns:
            if data[col].dtype == 'object' and col != target_name:
                data[col] = LabelEncoder().fit_transform(data[col])
        data[target_name] = LabelEncoder().fit_transform(data[col])
        desc = 'All the samples in the given dataset are converted to numerical data types using label encoding. Also, the target column was encoded using label encoding.'
        return data, desc

    def treat_missing_data(self, data, method, imputer=None, k_neighbors=None):
        desc = ""
        null = data.isnull().sum().sum()
        desc='There are '+str(null)+ ' null values in the dataset.'
        if null != 0:
            if len(data.index) > 10000:
                data = data.dropna()
                desc = 'The null values were dropped off since the dataset size is huge - ' + str(len(data.index))
            else:
                if method == 'forward':
                    data = data.fillna(method='ffill')
                    desc = 'The null values were replaced by next data points.'
                elif method == 'backward':
                    data = data.fillna(method='bfill')
                    desc = 'The null values were replaced by previous data points.'
                elif method == 'mean':
                    for i in data.columns:
                        data[i] = data[i].fillna(data[i].mean())
                    desc = 'The null values were replaced by the mean values.'
                elif method == 'median':
                    for i in data.columns:
                        data[i] = data[i].fillna(data[i].median())
                    desc = 'The null values were replaced by the median values.'
                elif method == 'variance':
                    for i in data.columns:
                        data[i] = data[i].fillna(data[i].var())
                    desc = 'The null values were replaced by the variance values.'
                else:
                    for i in data.columns:
                        data[i] = data[i].fillna(data[i].std())
                    desc = 'The null values were replaced by the standard deviation values.'
                if imputer is not None:
                    if imputer == 'simple':
                        simple_imputer = SimpleImputer(strategy=method)
                        data = pd.DataFrame(simple_imputer.fit_transform(data), columns=data.columns)
                        desc = f'The null values were imputed using SimpleImputer with strategy: {method}.'
                    elif imputer == 'knn':
                        if k_neighbors is not None:
                            knn_imputer = KNNImputer(n_neighbors=k_neighbors)
                            data = pd.DataFrame(knn_imputer.fit_transform(data), columns=data.columns)
                            desc = f'The null values were imputed using KNNImputer with {k_neighbors} neighbors.'
                        else:
                            raise ValueError("k_neighbors must be specified when using KNNImputer.")
        return data, desc
    def feature_scaling(self, data, algo, target_name):
        desc = ""
        if algo is not None:
            if algo in ['ANN', 'KNN', 'KMeans','Logistic Regression']:
                data_without_target = data.drop(target_name, axis=1)
                scaler = Normalizer()
                data_without_target = pd.DataFrame(scaler.fit_transform(data_without_target), columns=data_without_target.columns)
                data = pd.concat([data_without_target, data[target_name]], axis=1)
                desc = 'All the features in the dataset have been undergone normalization feature scaling technique.'
            elif algo in ['SVM', 'LDA', 'QDA','Naive Bayes']:
                data_without_target = data.drop(target_name, axis=1)
                scaler = StandardScaler()
                data_without_target = pd.DataFrame(scaler.fit_transform(data_without_target), columns=data_without_target.columns)
                data = pd.concat([data_without_target, data[target_name]], axis=1)
                desc = 'All the features in the dataset have been undergone standardization feature scaling technique.'
            elif algo in ['Decision Tree', 'Random Forest', 'Gradient Boosting','xgboost','adaboost']:
                desc = 'All the features in the dataset have been undergone no feature scaling technique.'
        else:
            data_without_target = data.drop(target_name, axis=1)
            scaler = StandardScaler()
            data_without_target = pd.DataFrame(scaler.fit_transform(data_without_target), columns=data_without_target.columns)
            data = pd.concat([data_without_target, data[target_name]], axis=1)
            desc = 'All the features in the dataset have been undergone standardization feature scaling technique.'
        return data, desc