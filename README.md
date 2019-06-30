# webcrawler
Use scrapy to crawl title, url, image-url, ingredients and text of german recipe pages:

|| Domain | total number of recipes    |
|-|-------------------|-------:|
|1| www.chefkoch.de | 330.000 |
|2| www.ichkoche.at | 150.000|
|3| www.daskochrezept.de| 87.000|
|4| www.eatsmarter.de | 83.000 |
|5| www.lecker.de | 60.000 |
|6| www.essen-und-trinken.de | 30.000 |
|7| www.womenshealth.de| 2.000 |
|8| www.rapunzel.de | ??? |
|9| www.springlane.de|???|
|10| www.proveg.com|???|
|11| www.eat-this.org|???|
|12| www.veganheaven.de|???|
|13| www.youtube.de|???|

# Deployment of docker container to OpenShift

1) Build image from local docker file
```
docker build .
```

2) Test-run docker image (ID) with crawler **name** (not class name, but "name" variable) as environment variable
```
docker run --env SPIDER_NAME=chefkoch image
```
3) Login to OpenShift CLI
```
oc login
```

4) Use washeuteessen-test project
``` 
oc project washeuteessen-test
```

5) Deploy crawler to openshift
```
oc start-build washeuteessen-crawler --from-dir=. --follow
```