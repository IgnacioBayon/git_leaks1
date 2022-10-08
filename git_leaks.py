import pandas as pd, re, signal, sys, time, pdb
from git import Repo

leaks = ['key','password','credentials']

REPO_DIR = "AD/1.1gitleaks/skale/skale-manager"


def extract(url):
    repo = Repo(url)
    return repo

def transform(repo:Repo,leaks):
    commit_list, message_list = [], []
    repo_list = list(repo.iter_commits())
    print(repo.iter_commits())
    for commit in repo_list:
        for leak in leaks:
            if re.search(leak,commit.message,re.I):
                commit_list.append(commit.hexsha)
                message_list.append(commit.message)
                
    return commit_list,message_list
    
def load(commit_list,message_list): 
    
    df_leaks = pd.DataFrame({'Commit':commit_list,'Message':message_list})
    print(df_leaks)
    df_leaks.to_csv(r'AD/1.1gitleaks/leaks.csv')
    


if __name__ == "__main__":
    repo = extract(REPO_DIR)
    commit_list,message_list = transform(repo,leaks)
    load(commit_list,message_list)
