import pandas as pd
import re, signal, sys, time
from git import Repo

END = "\033[m"

REPO_DIR = "1.1gitleaks/skale/skale-manager"
leaks = ['key', 'password', 'credentials']


def handler_signal(signal, frame):
    print("\n\n[!] Out .......\n")
    sys.exit(1)


def compile_p(leaks):
    compiled_leaks = []
    for leak in leaks:
        compiled_leaks.append(re.compile(leak))
    return compiled_leaks


def extract(url):
    repo = Repo(url)
    return repo


def transform(repo:Repo, compiled_leaks):
    commit_list, message_list = [], []
    repo_list = list(repo.iter_commits())
    print(repo.iter_commits())
    for commit in repo_list:
        for leak in compiled_leaks:
            if leak.search(commit.message,re.I):
                commit_list.append(commit.hexsha)
                message_list.append(commit.message)
                
    return commit_list, message_list


def load(commit_list, message_list): 
    
    df_leaks = pd.DataFrame({'Commit':commit_list,'Message':message_list})
    df_leaks.to_csv(r'1.1gitleaks/leaks.csv')
    

def progress_bar(iz, de):
    for i in range(iz, 1+de):
        print("\033[1A\033[2K", end="")
        x = i//2
        if i < 67:
            print('╠╣' + '█'*x + '░'*(100-x) +'╠╣ ' + str(i/2) + '% \ EXTRACT' + END)
        elif i <124:
            print('╠╣' + '█'*x + '░'*(100-x) +'╠╣ ' + str(i/2) + '% \ TRANSFORM' + END)
        else:
            print('╠╣' + '█'*x + '░'*(100-x) +'╠╣ ' + str(i/2) + '% \ LOAD' + END)
        time.sleep(0.01)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, handler_signal)

    compiled_leaks = compile_p(leaks)
    repo = extract(REPO_DIR)
    commit_list,message_list = transform(repo, compiled_leaks)
    progress_bar(1, 66)
    progress_bar(67, 124)
    load(commit_list, message_list)
    progress_bar(124, 200)
    exit(0)