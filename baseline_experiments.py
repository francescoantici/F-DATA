from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVR, SVC
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier, XGBRegressor
from sklearn.linear_model import SGDClassifier, SGDRegressor
from sklearn.metrics import classification_report, mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
from train_model import train_predict
import os 
from tqdm import tqdm
import pandas as pd
import numpy as np 

if __name__ == "__main__":
    
    # Result path
    result_path = "baseline_results"
    
    # Data folder  
    data_folder = "F-DATA"
    
    # ML model to use
    ml_model = KNeighborsClassifier
    
    regression_metric = lambda y_true, y_pred: str(mean_absolute_error(y_true, y_pred))
        
    # Definition of the task specifics
    tasks = {
        "ec":
            {
                "model": ml_model,
                "metric": classification_report,
                "target" : lambda j: j["exit state"] 
            },
        "pclass":
            {
                "model": ml_model,
                "metric": classification_report,
                "target" :  lambda j: j.pclass 
            },
        "avgpcon":
            {
                "model": ml_model,
                "metric" : regression_metric, 
                "target" : lambda j: int(j.avgpcon/j.nnuma) 
            },
        "duration":
            {
                "model": ml_model,
                "metric" : regression_metric, 
                "target" : lambda j: int(j.duration/60)
            }
    }
    
    # Months of data to use for the testing phase
    test_yms = ["23_06", "23_07", "23_08", "23_09", "23_10", "23_11", "23_12", "24_01", "24_02", "24_03", "24_04"]
    
    # Definition of the input encoding
    features = {
        "int_anon" : lambda df: df[["jnam", "usr", "jobenv_req"]].apply(lambda c: c.apply(lambda j:j.split("_")[-1])).values, 
        "sb_anon" : lambda df: df["embedding_anon"].values,
        "sb" : lambda df: df["embedding"].values
    }
    
    results = {t:[] for t in tasks} 
    
    x_train = {f:[] for f in features}
    y_train = {t:[] for t in tasks}
    
    x_test = {f:[] for f in features}
    y_test = {t:[] for t in tasks}   
    
    for data_path in tqdm([os.path.join(or_data_folder, f) for f in os.listdir(or_data_folder) if os.path.isfile(os.path.join(or_data_folder, f)) and f.endswith(".parquet")]):
                    
        # Load dataset 
        df = pd.read_parquet(data_path)
                        
        ym = data_path.split(".parquet")[0]
        
        for feat in features:
                        
            x_values = list(features[feat](df))
            
            if ym in test_yms:
                x_test[feat] += x_values
                    
            else:
                x_train[feat] += x_values
            
        for task in tasks:
            
            y_values = df.apply(tasks[task]["target"], axis = 1).to_list()
                        
            if ym in test_yms:
                y_test[task] += y_values
            else:
                y_train[task] += y_values
    
    for feat in features:
        for task in tqdm(tasks):
            
            # Training and testing of the models 
            model_instance = tasks[task]["model"](n_jobs = -1).fit(x_train[feat], y_train[task])
            print(f"Trained model {feat} for the task {task}")
            y_pred = model_instance.predict(x_test[feat])
            
            with open(os.path.join(result_path, f"{str(ml_model)}_{feat}_{task}.txt"), "w") as f:
                f.write(tasks[task]["metric"](y_test[task], y_pred))
            
            
        
            
                
                
                
                
            
        
                
            
            
            
            
            
            
    
    

