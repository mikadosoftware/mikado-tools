### CLean out local dir compared to origin
git checkout master
git pull
git fetch --prune ## kill off local branches that are not in origin
git branch -vv | awk '/: gone]/{print $1}' | xargs git branch -d

#### show people who need to delete branches from the repo



### journal/ todo

git for-each-ref --format '%(committerdate) %q %(authorname)' | sort -k5n -k2m -k3n -k4n n | grep remote | grep -v $IGNORE
