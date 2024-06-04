import pandas as pd 
import pickle
import os 
from tqdm import tqdm
    
if __name__ == "__main__":
    
    or_data_folder = "or_data_splits"
    anon_data_folder = "anon_data_splits"
        
    features = ["jid", "usr", "jnam", "jobenv_req"]
    anonym_maps = {f:{} for f in features}
        
    tot_length = 0
    
    for data_path in tqdm([f for f in os.listdir(or_data_folder) if os.path.isfile(os.path.join(or_data_folder, f)) and f.endswith(".csv")]):
                           
        # Read data
        df = pd.read_csv(os.path.join(or_data_folder, data_path), on_bad_lines="skip")
                
        df["jobenv_req"] = df["cr_jobenv_req"]
        df["freq_req"] = df["cr_freq_req"]
        df["freq_alloc"] = df["cr_freq_alloc"]
    
        # Dropping empty columns
        for column in ["cr_jobenv_req", "cr_freq_req", "cr_freq_alloc", "ermsg", "fjprofiler", "elpl.1"]:
            try:
                df = df.drop(column, axis = 1)
            except Exception as e:
                print(e)
        
        # Dropping empty columns
        for f in df.columns:
            if len(df[~(df[f].isna())]) == 0:
                df = df.drop([f], axis = 1)
        
        # Anonymizing fields
        for feat in features:
            
            # unique values 
            uvl = list(df[feat].unique())
            
            df[f"{feat}_or"] = df[feat]
            
            first_idx = len(anonym_maps[feat])
            new_values = list(filter(lambda v: not(v in anonym_maps[feat]), uvl))
            
            for j in range(len(new_values)):
                anonym_maps[feat][new_values[j]] = f"{feat}_{j+first_idx}"
            
            df[feat] = df[feat].apply(anonym_maps[feat].get)
        
        for fp in ["adt", "sdt", "edt"]:
            df = df[(~(df[fp].isna())) & (df[fp] != "")]
            df = df[(df[fp].apply(lambda d: not(d.startswith("1970"))))]
            # df[fp] = df[fp].apply(pd.to_datetime)
         
        # Features to convert to float
        for fp in ["perf1", "perf2", "perf3", "perf4", "perf5", "perf6", "elpl", "elp", "idle_time_ave", "econ", "avgpcon", "minpcon", "maxpcon", "mmszu", "mszl"]:
            df = df[(~(df[fp].isna())) & (df[fp] != "")]
            df[fp] = df[fp].apply(float)
        
        # Features to convert to int
        for fp in ["cnumr", "cnumat", "cnumut", "nnumr", "nnuma", "nnumu", "freq_req", "freq_alloc", "ec", "pri", "msza"]:
            df = df[(~(df[fp].isna())) & (df[fp] != "")]
            df[fp] = df[fp].apply(int)
        
        mlength = len(df)
        print(mlength)
        tot_length+=mlength
        
        # Save anonymized data
        df.to_parquet(os.path.join(anon_data_folder, data_path.replace(".csv", "_anon.parquet")), index = False)
        
    print(f"Total number of jobs: {tot_length}")
        
    with open(f"anonym_map/map2anon.pickle", "wb") as fa:
        pickle.dump(anonym_maps, fa)
        
    
    
    
    
    