import pandas as pd 
import os

if __name__ == "__main__":
    
    or_data_folder = "anon_data_splits"
    
    # Load dataset 
    df = pd.read_parquet([os.path.join(or_data_folder, f) for f in os.listdir(or_data_folder) if os.path.isfile(os.path.join(or_data_folder, f)) and f.endswith(".parquet")][0])
    
    md_file = "docs/feature_list.md"
    
    anonymized = ["jid", "usr", "jnam", "jobenv_req"]
    
    docstring = "\n".join([f"|{str(f)}|...|{str(df[f].dtype)}|{'true' if f in anonymized else 'false'}|" for f in df.columns])
    
    with open(md_file, "w") as f:
        f.write("# Job feature list\n\n")
        f.write("|Column|Description|Type|Anonymized|\n|------|-----------|----|----------|\n")
        for l in docstring:
            f.write(l)
                    
        