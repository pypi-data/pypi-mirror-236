git init
git add .
git commit -m "init creating new project"
git branch -M master
git remote add origin https://git.zoominfo.com/dozi/{name-your-service}
git push --set-upstream origin master
git pull --set-upstream origin master --allow-unrelated-histories --no-edit


