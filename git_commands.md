## Git Commands 


### Basic Commands -- Local Repository


1. git config --global user.name "Your Name"  
   Set your name for all repositories.
2. git config --global user.email "your.email@example.com"  
    Set your email for all repositories.

3. git init  
   Initialize a new Git repository in the current directory.
   creates a new .git subdirectory in the current directory.

4. git status  
   Show the working tree status, including staged, unstaged, and untracked files.
   options: 
    - `-s` or `--short`: Show a short summary of the status.
    - `-b` or `--branch`: Show the branch information.
    - `-u` or `--untracked-files`: Show untracked files.

5. git add <file> 
   Add a file to the staging area for the next commit.
   stages changes to be committed.
   options:
    - `.`: Add all changes in the current directory and subdirectories.
    - `-A`: Add all changes, including deletions.
    - `-u`: Add only tracked files. 

6. git commit -m "Commit message"  
   Commit the staged changes to the repository with a descriptive message.
   it uses the Files, User Name, and User Email to create a new commit object in the repository.
   create commitid (SHA-1 hash)
   options:
    - `-a`: Automatically stage files that have been modified and deleted, but new files you have not told Git about are not affected.
    - `--amend`: Modify the most recent commit.
  
7. git log  
   Show the commit history for the current branch.
   options:
    - `--oneline`: Show each commit on a single line.
    - `--graph`: Show a graphical representation of the commit history.
    - `--all`: Show all branches. 

8. git diff  
   Show the differences between the working directory and the staging area or between commits.
   options:
    - `--staged`: Show changes between the staging area and the last commit.
    - `--name-only`: Show only the names of changed files.
    - `--color`: Show colored output for easier reading.

9. git push <remote> <branch>  
   Push the local branch to the specified remote repository.
   connect and upload the local branch to the remote repository.
   .git folder contains the configuration for the remote repository and the branch to push to.
   options:
    - `-u` or `--set-upstream`: Set the upstream branch for the current branch.
    - `--force`: Force push to overwrite the remote branch.

10. git remote add <name> <url>  
    Add a new remote repository with the specified name and URL.
    connects with a remote repository and allows you to fetch and push changes.
    options:
     - `-f` or `--fetch`: Fetch the remote repository after adding it.
     - `-t` or `--tags`: Fetch all tags from the remote repository.


11. git pull <remote> <branch>
    Fetch and merge changes from the specified remote branch into the current branch.
    options:
     - `--rebase`: Rebase the current branch on top of the upstream branch after fetching.
     - `--no-commit`: Do not create a merge commit after pulling.

## Remote repository first

12. git clone <url>
   Clone a remote repository to the local machine.
   .git folder contains the configuration for the remote repository and the branch to clone.
   options:
    - `--depth <depth>`: Create a shallow clone with a history truncated to the specified number of commits.
    - `--branch <branch>`: Clone a specific branch.

13. git fetch <remote>
    Fetch changes from the specified remote repository without merging them.
    options:
     - `--all`: Fetch all remotes.
     - `--prune`: Remove any remote-tracking references that no longer exist on the remote.

14. git pull <remote> <branch>
    Fetch and merge changes from the specified remote branch into the current branch.
    options:
     - `--rebase`: Rebase the current branch on top of the upstream branch after fetching.
     - `--no-commit`: Do not create a merge commit after pulling.

15. git merge --abort / git merge --continue
    Handle merge conflicts that occur when changes from different branches cannot be automatically merged.
    Occur when changes from different branches cannot be automatically merged.
    options:
     - `--abort`: Abort the merge and return to the previous state.
     - `--continue`: Continue the merge after resolving conflicts.

16. git push <remote> <branch>
    Push the local branch to the specified remote repository.
    options:
     - `-u` or `--set-upstream`: Set the upstream branch for the current branch.
     - `--force`: Force push to overwrite the remote branch.

## Dangerous Commands

17. git reset --hard <commit>
    Reset the current branch to the specified commit, discarding all changes in the working directory and staging area.
    options:
     - `--soft`: Reset only the HEAD to the specified commit, keeping changes in the working directory and staging area.
     - `--mixed`: Reset the HEAD and index to the specified commit, keeping changes in the working directory.
     - `--hard`: Reset the HEAD, index, and working directory to the specified commit, discarding all changes.

18. git clean -f
    Remove untracked files from the working directory.
    options:
     - `-d`: Remove untracked directories in addition to untracked files.
     - `-x`: Remove all untracked files, including those ignored by .gitignore.
     - `-n` or `--dry-run`: Show what would be removed without actually removing anything.

19. git rebase <branch>
    Reapply commits on top of another base tip.
    options:
     - `--interactive`: Interactively rebase the current branch onto the specified branch.
     - `--onto <newbase>`: Rebase the current branch onto a new base commit.



## Branching Commands

20. git branch <branch-name>
    Create a new branch with the specified name.
    Dev, QA, Production, Staging, Hotfix, Feature, Release, etc.
    Main / Master -> The primary branch of the repository.
    options:
     - `-d` or `--delete`: Delete the specified branch.
     - `-D`: Force delete the specified branch, even if it has unmerged changes.
     - `-m` or `--move`: Rename the specified branch.

