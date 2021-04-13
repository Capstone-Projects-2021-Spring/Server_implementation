Photo Tag - Server
===
This is the Python web service designed to process and tag images coming from iOS and Android mobile devices. 

## Project Overview
PhotoTag is a mobile application designed in both Android and iOS which is designed to eliminate time spent by the user searching in their gallery for a specific image. With PhotoTag, users will be able to attach keywords to their existing photos with suggested tags from an image processing API, or choose to add their own custom keywords. These keywords will be used to search through the image collection for a smaller subset, for less total time spent searching for the user.

## Related Repositories
[iOS Application Repository](https://github.com/Capstone-Projects-2021-Spring/project-phototag-iOS)
[Android Application Repository](https://github.com/Capstone-Projects-2021-Spring/project-phototag-android)

## Instructions
### Prerequisites 
1. Run a Redis database instance on the local machine
2. Set the `firebase_api_key` environmental variable to the appropriate value

### Instructions
Clone the repository
```
$ git clone https://github.com/Capstone-Projects-2021-Spring/project_phototag_server_implementation.git  
```
Install all required libraries 
```
$ pip3 install requirements.txt 
```
Run the Flask web service
```
$ python3 server.py
```
Start up a worker
```
$ python3 worker.py
```
Access the web service for testing
```
FORM - http://localhost:5000/uploadImage
```

## Application Contributors
-   Alex J St.Clair (Cross-platform, project leader)
-   James Coolen (Android)
-   Matthew Day (Android)
-   Sebastian Tota (iOS, Git)
-   Reed Ceniviva (Android)
-   Ryan O' Connor (iOS)
-   Tadeusz J Rzepka (Android, Git, Scrum-master)
