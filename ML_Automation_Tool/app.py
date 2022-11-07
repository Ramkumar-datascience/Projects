from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import pandas as pd
import io
from scipy import stats
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler, QuantileTransformer, PowerTransformer, Normalizer, LabelEncoder
from sklearn.linear_model import LinearRegression, BayesianRidge, Lasso, Ridge, RidgeClassifier, LogisticRegression, SGDClassifier
import sklearn.metrics as metrics
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, OPTICS, Birch

app = Flask(__name__)

df = pd.DataFrame()
categorical_columns = list()
numerical_columns = list()
other_columns = list()
X_train = pd.DataFrame()
X_test = pd.DataFrame()
y_train = pd.DataFrame()
y_test = pd.DataFrame()
target = ''
test = ''

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/description',methods=['GET','POST'])
def upload_file():
   global df
   if request.method == 'POST':
      f = request.files['filename']
      f.save(secure_filename(f.filename))
      fn = f.filename
      if fn[-3:]=='csv':
          df = pd.read_csv(f.filename)
      elif fn[-4:]=='xlsx':
          df = pd.read_excel(f.filename)
      return render_template('description.html')
   else:
      return 'Not Secure'
        
   
@app.route('/describe')
def description():
   global df
   df = df.copy()
   result1, result2, result3 = '','',''
   input_name = request.args.get('desc')
   if input_name == 'Info':
       buffer = io.StringIO()
       df.info(buf=buffer)
       s=buffer.getvalue()
       result1 = s.splitlines()
       return render_template('description.html', result1 = result1)
   elif input_name == 'Shape':
       result2 = df.shape
       return render_template('description.html', result2 = result2)
   elif input_name == 'Columns':
       result3 = df.columns
       return render_template('description.html', result3 = result3)
   #return render_template('description.html', result1 = result1, result2 = result2, result3 = result3)

@app.route('/start')
def starteda():
    return render_template('eda.html')
   
@app.route('/eda')
def eda():
    global df
    global target
    global test
    df = df.copy()
    global categorical_columns
    global numerical_columns 
    global other_columns 
    global X_train
    global X_test
    global y_train
    global y_test

    df.columns = df.columns.str.strip()
    for c,t in zip(df.dtypes.index.to_list(),df.dtypes.to_list()):
        if t=="object":
            categorical_columns.append(c)
        elif t=="int64" or t=="float64":
            numerical_columns.append(c)
        else:
            other_columns.append(c)
    
    result = ''
    input_name = request.args.get('eda')
    train = request.args.get('train')
    test = request.args.get('test')
    target = request.args.get('target')
   
    features = df[numerical_columns]
    if input_name == 'irm':
        for i in df.describe().columns:
            Q1=df.describe().at['25%',i]
            Q3=df.describe().at['75%',i]
            IQR=Q3 - Q1
            LTV=Q1 - 1.5 * IQR
            UTV=Q3 + 1.5 * IQR
            x=np.array(df[i])
            p=[]
            count = 0
            for j in x:
                if j < LTV or j>UTV:
                    p.append(df[i].median())
                    count = count + 1
                else:
                    p.append(j)
            df[i]=p
        result1 = 'Number of outliers: ' + str(count)
        if count == 0:
            result = 'No outliers found'
        else:
            result = result1 + '\n' + 'Outliers treated successfully' + '\n' + str(df.shape)
        return render_template('eda.html', result = result)
    
    elif input_name == 'sdm':
        for i in df.describe().columns:
            q1 = df.describe().at['25%',i]
            q3 = df.describe().at['75%',i]
            IQR = q3-q1
            lwr_bound = q1-(1.5*IQR)
            upr_bound = q3+(1.5*IQR)
            index=df[i][(df[i]>upr_bound)|(df[i]<lwr_bound)].index
            df.drop(index,inplace=True)
            result = 'Outliers treated successfully' + '\n' + str(df.shape)
        return render_template('eda.html', result = result)
    
    elif input_name == 'mvrm':
        count =  df.isnull().sum().sum()
        if count == 0:
            result = 'No missing values found'
        else:
            df = df.dropna(axis=0)
            result = 'Number of missing values detected: '+str(count)+'\n'+'Missing value rows dropped successfully'+'\n'+str(df.shape)
        return render_template('eda.html', result = result)
    
    elif input_name == 'mvcm':
        count =  df.isnull().sum().sum()
        if count == 0:
            result = 'No missing values found'
        else:
            df = df.dropna(axis=1)
            result = 'Number of missing values detected: '+str(count)+'\n'+'Missing value columns dropped successfully'+'\n'+str(df.shape)
        return render_template('eda.html', result = result)
    
    elif input_name == 'meanm':
        count = df.isnull().sum().sum()
        if count == 0:
            result = 'No missing values found'
        else:
            for i in numerical_columns:
                df.fillna({i : df[i].mean()}, inplace=True)
            for i in categorical_columns:
                df.fillna({i : df[i].mode()[0]}, inplace=True)
            for i in other_columns:
                df.fillna({i : df[i].mode()[0]}, inplace=True)
            result = 'Number of missing values detected: '+str(count)+'\n'+'Missing values are imputed with mean successfully'+'\n'+str(df.shape)
        return render_template('eda.html', result = result)
    
    elif input_name == 'medianm':
        count = df.isnull().sum().sum()
        if count == 0:
            result = 'No missing values found'
        else:
            for i in numerical_columns:
                df.fillna({i : df[i].median()}, inplace=True)
            for i in categorical_columns:
                df.fillna({i : df[i].mode()[0]}, inplace=True)
            for i in other_columns:
                df.fillna({i : df[i].mode()[0]}, inplace=True)
            result = 'Number of missing values detected: '+str(count)+'\n'+'Missing values are imputed with median successfully'+'\n'+str(df.shape)
        return render_template('eda.html', result = result)

    elif input_name == 'minmax':
        scaler = MinMaxScaler()
        df[numerical_columns] = scaler.fit_transform(features.values)
        result = 'MinMax Scaling Successful'
        return render_template('eda.html',result = result)

    elif input_name == 'standard':
        scaler = StandardScaler()
        df[numerical_columns] = scaler.fit_transform(features.values)
        result = 'Standard Scaling Successful'
        return render_template('eda.html',result = result)

    elif input_name == 'maxabs':
        scaler = MaxAbsScaler()
        df[numerical_columns] = scaler.fit_transform(features.values)
        result = 'MaxAbs Scaling Successful'
        return render_template('eda.html',result = result)

    elif input_name == 'robust':
        scaler = RobustScaler()
        df[numerical_columns] = scaler.fit_transform(features.values)
        result = 'Robust Scaling Successful'
        return render_template('eda.html',result = result)
    
    elif input_name == 'quantile':
        scaler = QuantileTransformer()
        df[numerical_columns] = scaler.fit_transform(features.values)
        result = 'Quantile Transformation Successful'
        return render_template('eda.html',result = result)

    elif input_name == 'log':
        for i in numerical_columns:
            df[i] = np.log(df[i])
        result = 'Log Transformation Successful'
        return render_template('eda.html',result = result)

    elif input_name == 'power':
        scaler = PowerTransformer(method = 'yeo-johnson')
        df[numerical_columns] = scaler.fit_transform(features.values)
        result = 'Power Transformation Successful'
        return render_template('eda.html',result = result)
    
    elif input_name == 'unitvector':
        scaler = Normalizer(norm = 'l2')
        df[numerical_columns] = scaler.fit_transform(features.values)
        result = 'Unit Vector Scaling Successful'
        return render_template('eda.html',result = result)

    elif input_name == 'label':
        label_encoder = LabelEncoder()
        for i in categorical_columns:
            df[i] = label_encoder.fit_transform(df[i])
        result = 'Label Encoding Successful'
        return render_template('eda.html',result = result)

    elif input_name == 'onehot':
        df = pd.get_dummies(df, columns = categorical_columns)
        result = 'One Hot Encoding Successful' + '\n' + 'Shape: ' + str(df.shape)
        result1 = ''
        result1 = df.columns
        return render_template('eda.html', result = result, result1 = result1)

    elif input_name == 'tc':
        result1 = ''
        df = df.convert_dtypes()
        buffer = io.StringIO()
        df.info(buf=buffer)
        s=buffer.getvalue()
        result1 = s.splitlines()
        return render_template('eda.html', result1 = result1)
        
    else:
        if test == '':
            result = 'Please give train-test split values and submit the form \n to split the dataset.'
            return render_template('eda.html',result = result)
        else:
            X = df.drop(target, axis=1)
            y = df[target]
            X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=int(test)/100, random_state=0)
            result = 'Split Successful' + '\n' + 'Training data shape: ' + str(X_train.shape) + '\n'+ 'Training labels shape: ' + str(y_train.shape) + '\n'+ 'Test data shape: ' + str(X_test.shape) + '\n'+ 'Test labels shape: ' + str(y_test.shape)
            return render_template('eda.html', result = result)

@app.route('/startmb')
def startmb():
    global test
    if test == '':
        result = 'Please give train-test split values and submit the form \n to split the dataset.'
        return render_template('eda.html',result = result)
    else:
        return render_template('ml.html')

@app.route('/mb')
def mb():
    global df
    global categorical_columns
    global numerical_columns 
    global other_columns 
    global X_train
    global X_test
    global y_train
    global y_test
    global target

    result = ''

    input_model1 = request.args.get('ml1')
    input_model2 = request.args.get('ml2')
    input_model3 = request.args.get('ml3')
   
    if input_model1 == "linearregression":
        if target not in numerical_columns:
            result = 'Target column '+target+' is not a numerical column'+'\n'+'Please choose a classification technique'
            return render_template('ml.html',result=result)
        else:
            model = LinearRegression()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            train_score=model.score(X_train,y_train)
            test_score=model.score(X_test,y_test)
            explained_variance=metrics.explained_variance_score(y_test, y_pred)
            mean_absolute_error=metrics.mean_absolute_error(y_test, y_pred) 
            mse=metrics.mean_squared_error(y_test, y_pred) 
            median_absolute_error=metrics.median_absolute_error(y_test, y_pred)
            r2=metrics.r2_score(y_test, y_pred)
            result = 'Evaluation Metrics'+'\n'+'Train Score: '+str(train_score)+'\n'+'Test Score: '+str(test_score)+'\n'+'Explained Variance: '+str(round(explained_variance,4))+'\n'+'R2: '+str(round(r2,4))+'\n'+'MAE: '+str(round(mean_absolute_error,4))+'\n'+'MSE: '+str(round(mse,4))+'\n'+'RMSE: '+str(round(np.sqrt(mse),4))
            return render_template('ml.html',result=result)
        
    elif input_model1 == "bridgeregression":
        if target not in numerical_columns:
            result = 'Target column '+target+' is not a numerical column'+'\n'+'Please choose a classification technique'
            return render_template('ml.html',result=result)
        else:
            niterations = int(request.args.get('niter1'))
            model = BayesianRidge(n_iter = niterations)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            train_score=model.score(X_train,y_train)
            test_score=model.score(X_test,y_test)
            explained_variance=metrics.explained_variance_score(y_test, y_pred)
            mean_absolute_error=metrics.mean_absolute_error(y_test, y_pred) 
            mse=metrics.mean_squared_error(y_test, y_pred) 
            median_absolute_error=metrics.median_absolute_error(y_test, y_pred)
            r2=metrics.r2_score(y_test, y_pred)
            result = 'Evaluation Metrics'+'\n'+'Train Score: '+str(train_score)+'\n'+'Test Score: '+str(test_score)+'\n'+'Explained Variance: '+str(round(explained_variance,4))+'\n'+'R2: '+str(round(r2,4))+'\n'+'MAE: '+str(round(mean_absolute_error,4))+'\n'+'MSE: '+str(round(mse,4))+'\n'+'RMSE: '+str(round(np.sqrt(mse),4))
            return render_template('ml.html',result=result)
        
    elif input_model1 == "randomforestregression":
        if target not in numerical_columns:
            result = 'Target column '+target+' is not a numerical column'+'\n'+'Please choose a classification technique'
            return render_template('ml.html',result=result)
        else:
            nestimators = int(request.args.get('nestim1'))
            model = RandomForestRegressor(n_estimators = nestimators)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            train_score=model.score(X_train,y_train)
            test_score=model.score(X_test,y_test)
            explained_variance=metrics.explained_variance_score(y_test, y_pred)
            mean_absolute_error=metrics.mean_absolute_error(y_test, y_pred) 
            mse=metrics.mean_squared_error(y_test, y_pred) 
            median_absolute_error=metrics.median_absolute_error(y_test, y_pred)
            r2=metrics.r2_score(y_test, y_pred)
            result = 'Evaluation Metrics'+'\n'+'Train Score: '+str(train_score)+'\n'+'Test Score: '+str(test_score)+'\n'+'Explained Variance: '+str(round(explained_variance,4))+'\n'+'R2: '+str(round(r2,4))+'\n'+'MAE: '+str(round(mean_absolute_error,4))+'\n'+'MSE: '+str(round(mse,4))+'\n'+'RMSE: '+str(round(np.sqrt(mse),4))
            return render_template('ml.html',result=result)
        
    elif input_model1 == "lassoregression":
        if target not in numerical_columns:
            result = 'Target column '+target+' is not a numerical column'+'\n'+'Please choose a classification technique'
            return render_template('ml.html',result=result)
        else:
            alpha = float(request.args.get('alpha'))
            model = Lasso(alpha = alpha)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            train_score=model.score(X_train,y_train)
            test_score=model.score(X_test,y_test)
            explained_variance=metrics.explained_variance_score(y_test, y_pred)
            mean_absolute_error=metrics.mean_absolute_error(y_test, y_pred) 
            mse=metrics.mean_squared_error(y_test, y_pred) 
            median_absolute_error=metrics.median_absolute_error(y_test, y_pred)
            r2=metrics.r2_score(y_test, y_pred)
            result = 'Evaluation Metrics'+'\n'+'Train Score: '+str(train_score)+'\n'+'Test Score: '+str(test_score)+'\n'+'Explained Variance: '+str(round(explained_variance,4))+'\n'+'R2: '+str(round(r2,4))+'\n'+'MAE: '+str(round(mean_absolute_error,4))+'\n'+'MSE: '+str(round(mse,4))+'\n'+'RMSE: '+str(round(np.sqrt(mse),4))
            return render_template('ml.html',result=result)

    elif input_model1 == "ridgeregression":
        if target not in numerical_columns:
            result = 'Target column '+target+' is not a numerical column'+'\n'+'Please choose a classification technique'
            return render_template('ml.html',result=result)
        else:
            alpha = float(request.args.get('alpha'))
            model = Ridge(alpha = alpha)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            train_score=model.score(X_train,y_train)
            test_score=model.score(X_test,y_test)
            explained_variance=metrics.explained_variance_score(y_test, y_pred)
            mean_absolute_error=metrics.mean_absolute_error(y_test, y_pred) 
            mse=metrics.mean_squared_error(y_test, y_pred) 
            median_absolute_error=metrics.median_absolute_error(y_test, y_pred)
            r2=metrics.r2_score(y_test, y_pred)
            result = 'Evaluation Metrics'+'\n'+'Train Score: '+str(train_score)+'\n'+'Test Score: '+str(test_score)+'\n'+'Explained Variance: '+str(round(explained_variance,4))+'\n'+'R2: '+str(round(r2,4))+'\n'+'MAE: '+str(round(mean_absolute_error,4))+'\n'+'MSE: '+str(round(mse,4))+'\n'+'RMSE: '+str(round(np.sqrt(mse),4))
            return render_template('ml.html',result=result)

    
    elif input_model2 == "ridgeclassifier":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            alpha = float(request.args.get('alpha'))
            model = RidgeClassifier(alpha = alpha)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model2 == "logisticregression":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            solver = request.args.get('solver')
            penalty = request.args.get('penalty1')
            cparam = float(request.args.get('cparam1'))
            model = LogisticRegression(solver = solver, penalty = penalty, C = cparam)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model2 == "sgradientboosting":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            loss = request.args.get('loss')
            penalty = request.args.get('penalty2')
            model = SGDClassifier(loss = loss, penalty = penalty)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model2 == "knnclassification":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            nneighbours = int(request.args.get('nneighbours'))
            algorithm = request.args.get('algorithm')
            model = KNeighborsClassifier(n_neighbors = nneighbours, algorithm = algorithm)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model2 == "decisiontrees":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            criterion = request.args.get('criterion')
            model = DecisionTreeClassifier(criterion = criterion)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model2 == "randomforest":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            nestimators = int(request.args.get('nestim2'))
            model = RandomForestClassifier(n_estimators = nestimators)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model2 == "naivebayes":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            model = GaussianNB()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model2 == "supportvectormachines":
        if target not in categorical_columns:
            result = 'Target column '+target+' is not a categorical column'+'\n'+'Please choose a regression technique'
            return render_template('ml.html',result=result)
        else:
            cparam = float(request.args.get('cparam2'))
            gamma = request.args.get('gamma')
            kernel = request.args.get('kernel')
            model = SVC(C = cparam, gamma = gamma, kernel = kernel)
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            cv = metrics.classification_report(y_test, y_pred)
            result = cv
            return render_template('ml.html',result = result)

    elif input_model3 == "kmeansclustering":
        nclusters = int(request.args.get('nclusters1'))
        algorithm = request.args.get('algo')
        model = KMeans(n_clusters = nclusters, algorithm = algorithm).fit(df)
        cluster_labels = model.labels_
        silhouettescore = metrics.silhouette_score(df, cluster_labels)
        chscore = metrics.calinski_harabasz_score(df, cluster_labels)
        dbscore = metrics.davies_bouldin_score(df, cluster_labels)
        result = 'Label Names: ' + str(np.unique(model.labels_))+'\n'+'Silhouette Score: '+str(silhouettescore)+'\n'+'Calinski Harabasz Score: '+str(chscore)+'\n'+'Davies Bouldin Score: '+str(dbscore)
        return render_template('ml.html',result = result)

    elif input_model3 == "ahc":
        nclusters = int(request.args.get('nclusters2'))
        affinity = request.args.get('affinity')
        linkage = request.args.get('linkage')
        model = AgglomerativeClustering(n_clusters = nclusters, affinity = affinity, linkage = linkage).fit(df)
        cluster_labels = model.labels_
        silhouettescore = metrics.silhouette_score(df, cluster_labels)
        chscore = metrics.calinski_harabasz_score(df, cluster_labels)
        dbscore = metrics.davies_bouldin_score(df, cluster_labels)
        result = 'Label Names: ' + str(np.unique(model.labels_))+'\n'+'Silhouette Score: '+str(silhouettescore)+'\n'+'Calinski Harabasz Score: '+str(chscore)+'\n'+'Davies Bouldin Score: '+str(dbscore)
        return render_template('ml.html',result = result)

    elif input_model3 == "dbscan":
        eps = float(request.args.get('eps'))
        minsamples = int(request.args.get('minsamples'))
        algorithm = request.args.get('alg')
        model = DBSCAN(eps = eps, min_samples = minsamples, algorithm = algorithm).fit(df)
        cluster_labels = model.labels_
        chscore = metrics.calinski_harabasz_score(df, cluster_labels)
        dbscore = metrics.davies_bouldin_score(df, cluster_labels)
        result = 'Label Names: ' + str(np.unique(model.labels_))+'\n'+'Calinski Harabasz Score: '+str(chscore)+'\n'+'Davies Bouldin Score: '+str(dbscore)
        return render_template('ml.html',result = result)

    elif input_model3 == "optics":
        minsamples = int(request.args.get('minsamples'))
        algorithm = request.args.get('alg')
        model = OPTICS(min_samples = minsamples, algorithm = algorithm).fit(df)
        cluster_labels = model.labels_
        chscore = metrics.calinski_harabasz_score(df, cluster_labels)
        dbscore = metrics.davies_bouldin_score(df, cluster_labels)
        result = 'Label Names: ' + str(np.unique(model.labels_))+'\n'+'Calinski Harabasz Score: '+str(chscore)+'\n'+'Davies Bouldin Score: '+str(dbscore)
        return render_template('ml.html',result = result)

    elif input_model3 == "birch":
        threshold = float(request.args.get('threshold'))
        branchingfactor = int(request.args.get('branchingfactor'))
        clusters = int(request.args.get('clusters'))
        model = Birch(threshold = threshold, branching_factor = branchingfactor, n_clusters = clusters).fit(df)
        cluster_labels = model.labels_
        silhouettescore = metrics.silhouette_score(df, cluster_labels)
        chscore = metrics.calinski_harabasz_score(df, cluster_labels)
        dbscore = metrics.davies_bouldin_score(df, cluster_labels)
        result = 'Label Names: ' + str(np.unique(model.labels_))+'\n'+'Silhouette Score: '+str(silhouettescore)+'\n'+'Calinski Harabasz Score: '+str(chscore)+'\n'+'Davies Bouldin Score: '+str(dbscore)
        return render_template('ml.html',result = result)


    else:
        return render_template('ml.html')

    
if __name__ == '__main__':
    app.run(debug = True)
