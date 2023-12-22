## Cleaning pods in status Evicted 

delete subs in status Failed, for execution frequency we use CronJob

use lib kubernetes 

[off_docs](https://kubernetes.readthedocs.io/en/latest/README.html)

[github_repa_](https://github.com/kubernetes-client/python)

## build docker images 
```sh
docker-compose build 
```
## if use helm 
```
kubectl create ns devops
helm upgrade --install cleaning -n devops ./kube/cleaning/
```


[alternativa](https://github.com/gianlucam76/k8s-cleaner/tree/main)