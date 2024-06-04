import pandas as pd 
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

def convert_to_str(job):
    return ",".join([f"{job[k]}" for k in job.index if (job[k] and not(pd.isna(job[k])))])
    
if __name__ == "__main__":
        
    # Fugkau system specifications 
    top_perf = 537000000 #GFLOPs 
    mem_bandwidth =  163000000 #Gib/s 
    ridge_point = top_perf/mem_bandwidth 
    
    JOB_FEATURES = ["usr_or", "jnam_or", "jobenv_req_or"]
    
    # Encoder
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    
    or_data_folder = "anon_data_splits"
    
    for data_path in tqdm([os.path.join(or_data_folder, f) for f in os.listdir(or_data_folder) if os.path.isfile(os.path.join(or_data_folder, f)) and f.endswith(".parquet")]):
        
        # Load dataset 
        df = pd.read_parquet(data_path)
        
        # Create number of floating point operations per second features in Flop/second             
        df["flops"] = df.apply(lambda j: (j.perf2 + (j.perf3 * 4))/(j.elp - j.idle_time_ave), axis = 1) 
        
        # Create memory bandwidth feature in Byte/second     
        df["mbwidth"] = df.apply(lambda j: (((j.perf4+j.perf5)/12)*256)/(j.elp - j.idle_time_ave), axis = 1)
        
        # Compute operational intensity in Flop/Byte
        df["opint"] = df.apply(lambda j: j.flops/j.mbwidth, axis=1)
        
        # Create the performance class label -> memory-bound or compute-bound
        df["pclass"] = df.apply(lambda j: "compute-bound" if j.opint >= ridge_point else "memory-bound", axis = 1)
        
        # Generate embeddings    
        encoded_str = encoder.encode(df[JOB_FEATURES].apply(convert_to_str, axis = 1).values)
        
        # Create embedding feature
        df["embedding"] = [encoded_str[i] for i in range(len(df))]
        
        # Create exit state feature 
        df["exit state"] = df.ec.apply(lambda ec: "completed" if int(ec) == 0 else "failed")
        
        # Create duration feature
        df["duration"] = df.elp.values
        
        # Drop original features
        df.drop(JOB_FEATURES + ["jid_or", "elp"], axis = 1, inplace=True)
        
        # Save the newly generated data          
        df.to_parquet(data_path, index=False)
        
        
    
    
    