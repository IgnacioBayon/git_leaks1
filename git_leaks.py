import pandas as pd, re, signal, sys, time, pdb
from git import Repo

REPO_DIR = "1.1gitleaks/skale/skale-manager"
leaks = ['key','password','credentials']

def compilar_patrones(leaks):
    compiled_leaks = []
    for leak in leaks:
        compiled_leaks.append(re.compile(leak))
    return compiled_leaks

def extract(url):
    repo = Repo(url)
    return repo

def transform(repo:Repo,compiled_leaks):
    commit_list, message_list = [], []
    repo_list = list(repo.iter_commits())
    print(repo.iter_commits())
    for commit in repo_list:
        for leak in compiled_leaks:
            if leak.search(commit.message,re.I):
                commit_list.append(commit.hexsha)
                message_list.append(commit.message)
                
    return commit_list,message_list
    
def load(commit_list,message_list): 
    
    df_leaks = pd.DataFrame({'Commit':commit_list,'Message':message_list})
    print(df_leaks)
    df_leaks.to_csv(r'1.1gitleaks/leaks.csv')
    


if __name__ == "__main__":
    
    compiled_leaks = compilar_patrones(leaks)

    repo = extract(REPO_DIR)
    commit_list,message_list = transform(repo,compiled_leaks)
    load(commit_list,message_list)
