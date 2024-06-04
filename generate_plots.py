from datetime import datetime
import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
from tqdm import tqdm
import os

if __name__ == "__main__":
    
    sns.set_style("whitegrid")
    
    or_data_folder = "F-DATA"
    
    plot_path = "plots"
    
    stats_tot = {"ym":[], "pclass":[], "navgpcon":[], "nminpcon":[], "nmaxpcon":[], "ec":[], "elp":[], "nnuma":[]}
    
    for data_path in tqdm([os.path.join(or_data_folder, f) for f in os.listdir(or_data_folder) if os.path.isfile(os.path.join(or_data_folder, f)) and f.endswith(".parquet")]):
        
        # Load dataset 
        df = pd.read_parquet(data_path)
        
        ym = data_path.split("/")[-1].replace("data_", "").replace("_anon.parquet", "")[2:]
        
        plot_path_ym = os.path.join(plot_path, ym)
        
        if not os.path.exists(plot_path_ym):
            os.makedirs(plot_path_ym)
        
        # Exit code plots  
        size = 9
        count_ec = df[~df.ec.isna()].value_counts("ec")
        x_v = list(map(lambda t: str(int(t)), count_ec.index.values[:size])) + ["Others"]
        y_v = list(count_ec.values[:size]) + [sum(count_ec.values[size:])]
        
        sns.barplot(x = x_v, y = y_v)
        plt.ylabel("# of jobs")
        plt.xlabel("Exit code of the job")
        plt.yscale("log")
        plt.xticks(rotation = 45)
        plt.tight_layout()
        plt.savefig(os.path.join(plot_path_ym, "ec_distribution.png"))
        plt.savefig(os.path.join(plot_path_ym, "ec_distribution.pdf"), format = "pdf")
        plt.clf()
        
        # Duration plot
        df = df[~df.elp.isna()]
        df["Duration (in minutes)"] = df.elp.apply(lambda e: int(int(e)/60))
        sns.histplot(data = df, x = "Duration (in minutes)")
        plt.ylabel("# of jobs")
        plt.yscale("log")
        plt.tight_layout()
        plt.savefig(os.path.join(plot_path_ym, "dr_distribution.png"))
        plt.savefig(os.path.join(plot_path_ym, "dr_distribution.pdf"), format = "pdf")
        plt.clf()
        
        # Power plot
        df[(df.nnuma != 0) & ~(df.nnuma.isna()) & (df.nnuma != "")]
        
        df["navgpcon"] = df.apply(lambda j: float(j.avgpcon/j.nnuma), axis = 1)
        df["nminpcon"] = df.apply(lambda j: float(j.minpcon/j.nnuma), axis = 1)
        df["nmaxpcon"] = df.apply(lambda j: float(j.maxpcon/j.nnuma), axis = 1)
        
        df = df[(df.nminpcon > 10) & (df.nminpcon < 300)]
        df = df[(df.navgpcon > 10) & (df.navgpcon < 300)]
        df = df[(df.nmaxpcon > 10) & (df.nmaxpcon < 300)]
        
        sns.histplot(data = df, x = "nminpcon", alpha = 0.7, label = "minpcon")
        sns.histplot(data = df, x = "navgpcon", alpha = 0.7, label = "avgpcon")
        sns.histplot(data = df, x = "nmaxpcon", alpha = 0.7, label = "maxpcon")
        plt.legend()
        plt.ylabel("# of jobs")
        plt.xlabel("Power consumption (in Watts)")
        # plt.xscale("log")
        plt.yscale("log")
        plt.tight_layout()
        plt.savefig(os.path.join(plot_path_ym, "pcon.png"))
        plt.savefig(os.path.join(plot_path_ym, "pcon.pdf"), format = "pdf")
        plt.clf()
        
        stats_tot["ym"] += [ym]*len(df)
        stats_tot["pclass"] += df["pclass"].to_list()
        stats_tot["nminpcon"] += df["nminpcon"].to_list()
        stats_tot["navgpcon"] += df["navgpcon"].to_list()
        stats_tot["nmaxpcon"] += df["nmaxpcon"].to_list()
        stats_tot["ec"] += df["ec"].to_list()
        stats_tot["elp"] += df["elp"].to_list()
        stats_tot["nnuma"] += df["nnuma"].to_list()
    
    stats_df = pd.DataFrame.from_dict(stats_tot)
    
    stats_df["ym"] = stats_df.ym.apply(lambda ym: ym.replace("_", "/"))
    stats_df["exit state"] = stats_df["ec"].apply(lambda ec: "completed" if int(ec) == 0 else "failed")
    
    fig = plt.figure(figsize=(21, 13))
    ax1 = fig.add_subplot(2, 3, 1)
    ax2 = fig.add_subplot(2, 3, 2)
    ax3 = fig.add_subplot(2, 3, 3)
    ax4 = fig.add_subplot(2, 3, 4)
    ax5 = fig.add_subplot(2, 3, 5)
    ax6 = fig.add_subplot(2, 3, 6)
            
    # Number of jobs per month plots  
    sns.histplot(data=stats_df.sort_values("ym"), x = "ym", ax = ax1)
    ax1.set_ylabel("# of jobs")
    ax1.set_xlabel("Year month")
    ticks = ax1.get_xticks()
    labels = ax1.get_xticklabels()
    ax1.set_xticks(ticks=ticks, labels =[str(labels[i].get_text()) if i%3==0 else "" for i in range(len(labels))], rotation = 45)
    ax1.set_title('a)', y=-0.175)
    
    # Nnuma plot
    def parse_nnuma(nnuma):
        values = [0, 10, 100, 1000, 10000, 100000, 200000]
        for i in range(len(values) - 1):
            if  values[i] <= int(nnuma) < values[i+1]:
                return f"[{values[i]}, {values[i+1]})"
            
    stats_df["nnuma"] = stats_df.nnuma.apply(parse_nnuma)
    sns.histplot(data = stats_df.sort_values("nnuma"), x = "nnuma", ax = ax2)
    ax2.set_ylabel("# of jobs")
    ax2.set_xlabel("# of nodes allocated")
    ax2.set_yscale("log")
    ticks = ax2.get_xticks()
    labels = ax2.get_xticklabels()
    ax2.set_xticks(ticks, [r"[1, 10)", r"[10, 100)", r"[100, 1K)", r"[1k, 10K)", r"[10K, 100K)", r"[100K, 1M)"])
    ax2.set_title('b)', y=-0.175)
    
    # Duration plot
    stats_df = stats_df[~stats_df.elp.isna()]
    stats_df["Duration (in minutes)"] = stats_df.elp.apply(lambda e: int(int(e)/60))
    print(len(stats_df[stats_df["Duration (in minutes)"] < 60]))
    sns.histplot(data = stats_df, x = "Duration (in minutes)", ax = ax3)
    ax3.set_ylabel("# of jobs")
    ax3.set_yscale("log")
    ax3.set_title('c)', y=-0.175)
    
    # Exit state plots  
    counts_es = {l:len(stats_df[stats_df["exit state"] == l]) for l in stats_df["exit state"].unique()}
    stats_df["exit state"] = stats_df["exit state"].apply(lambda es: f"{es} ({counts_es.get(es)})")
    
    sns.histplot(data=stats_df.sort_values("ym"), x = "ym", hue = "exit state", multiple="stack", ax=ax4)
    ax4.set_ylabel("# of jobs")
    ax4.set_xlabel("Year month")
    ticks = ax4.get_xticks()
    labels = ax4.get_xticklabels()
    ax4.set_xticks(ticks=ticks, labels =[str(labels[i].get_text()) if i%3==0 else "" for i in range(len(labels))], rotation = 45)
    ax4.set_title('d)', y=-0.175)
    
    # Pclass plots  
    counts_pclass = {l:len(stats_df[stats_df.pclass == l]) for l in stats_df.pclass.unique()}
    stats_df["pclass"] = stats_df.pclass.apply(lambda pc: f"{pc} ({counts_pclass.get(pc)})")
    
    sns.histplot(data=stats_df.sort_values("ym"), x = "ym", hue = "pclass", multiple="stack",  ax = ax5)
    ax5.set_ylabel("# of jobs")
    ax5.set_xlabel("Year month")
    ticks = ax5.get_xticks()
    labels = ax5.get_xticklabels()
    ax5.set_xticks(ticks=ticks, labels =[str(labels[i].get_text()) if i%3==0 else "" for i in range(len(labels))], rotation = 45)
    ax5.set_title('e)', y=-0.175)            
    
    # Power plot    
    stats_df = stats_df[stats_df.nminpcon > 10]
    sns.histplot(data = stats_df, x = "nminpcon", alpha = 0.35, label = "minpcon", ax = ax6)
    sns.histplot(data = stats_df, x = "navgpcon", alpha = 0.35, label = "avgpcon", ax = ax6)
    sns.histplot(data = stats_df, x = "nmaxpcon", alpha = 0.35, label = "maxpcon", ax = ax6)
    ax6.set_title('f)', y=-0.175)
    ax6.legend()
    ax6.set_ylabel("# of jobs")
    ax6.set_xlabel("Power consumption (in Watts)")
    ax6.set_yscale("log")
    
    # Total plot    
    plt.tight_layout()
    plt.savefig(os.path.join(plot_path, "pairplot.png"), dpi = 300)
    plt.savefig(os.path.join(plot_path, "pairplot.pdf"), format = "pdf")
    plt.clf()