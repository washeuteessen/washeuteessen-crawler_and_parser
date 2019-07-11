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
|7| www.rewe.de | 4.000 |
|8| www.rapunzel.de | ??? |
|9| www.springlane.de|???|
|10| www.proveg.com|???|
|11| www.eat-this.org|???|
|12| www.veganheaven.de|???|
|13| www.youtube.de|???|
|14| www.brigitte.de/rezepte|???|
|15| www.angebrannt.de|???|
|16| www.frag-mutti.de|???|
|17| www.livingathome.de/kochen-feiern/rezepte/archiv|???|
|18| www.kochbar.de|???|
|19| www.cocktails.de|???|
|20| www.backenmachtgluecklich.de|???|
|21| www.womenshealth.de| 2.000 |


## Local run

1. build image from local docker file
    ```bash
    docker build .
    ```
    
2. run image 
    ```bash
    docker run --env SPIDER_NAME=chefkoch image
    ```

## Deploy to Openshift

1. verify your logged in and select the correct namespace
    ```bash
    $ oc projects
    $ oc project *namespace*
    ```
    
2. start build with
    ```bash
    $ oc start-build washeuteessen-crawler --from-dir=. --follow
    ```

3. verify result
    ```bash 
    $ oc describe dc/washeuteessen-crawler
    
    ...
    Deployment #3 (latest):
    	Name:		washeuteessen-crawler-X
    	Created:	2 minutes ago
    	Status:		Active
    ...
    
    ```
## Run cronjob on OpenShift

1. Get all jobs
```
oc get jobs
```
2. Abort pod
```
oc delete pod <name>
```