## Developers connected API
A REST API of a simple social network of software developers.

Features:
 - Retrieve whether two “developers” are fully connected or not. Given a pair of developer handles they are considered connected if:
   - They follow each other on Twitter.
   - They have at least a GitHub organization in common.
	
# Setup before running:
Set the Twitter and GitHub secrets using one of the following methods:

* *Environment variables:*
   ```
   export TWITTER_API_CONSUMER_KEY=<TWITTER_API_CONSUMER_KEY>
   export TWITTER_API_CONSUMER_SECRET=<TWITTER_API_CONSUMER_SECRET>
   export TWITTER_API_ACCESS_TOKEN=<TWITTER_API_ACCESS_TOKEN>
   export TWITTER_API_ACCESS_TOKEN_SECRET=<TWITTER_API_ACCESS_TOKEN_SECRET>
   export GITHUB_API_TOKEN=<GITHUB_API_TOKEN>
   ```

* *Specifying them into the `app.env` file at root:* 

   `app.env:`
   ```
   TWITTER_API_CONSUMER_KEY=<TWITTER_API_CONSUMER_KEY>
   TWITTER_API_CONSUMER_SECRET=<TWITTER_API_CONSUMER_SECRET>
   TWITTER_API_ACCESS_TOKEN=<TWITTER_API_ACCESS_TOKEN>
   TWITTER_API_ACCESS_TOKEN_SECRET=<TWITTER_API_ACCESS_TOKEN_SECRET>
   GITHUB_API_TOKEN=<GITHUB_API_TOKEN>
   ```

You will see the following message when trying to launch the app if the secrets are not properly configured:
```
ValueError: The environment variable TWITTER_API_CONSUMER_KEY is not set.
```

# To run (docker-compose):
```
docker-compose build
docker-compose up --abort-on-container-exit
```
# To run (locally):
```
pip install -r requirements.txt
python runserver.py
```
# API:
Usually the host is:

HOST http://localhost:8080

Swagger page: http://localhost:8080


## Realtime endpoint
GET /connected/realtime/:dev1/:dev2

```
curl -X 'GET' \
  'http://localhost:8080/connected/realtime/dev1/dev2' \
  -H 'accept: application/json'
```
### Response 200 OK:
```
{
    "connected": false
}
```

### Response404 NOT FOUND:
```
{
    "errors": [
        ":dev1 is no a valid user in github",
        ":dev2 is no a valid user in twitter"
    ]
}
```

## Register endpoint
GET /connected/register/:dev1/:dev2

```
curl -X 'GET' \
  'http://localhost:8080/connected/register/dev1/dev2' \
  -H 'accept: application/json'
```

### Response 200 OK:
```
[
    {
        "connected": false,
        "registered_at": "2014-07-06T16:00:17Z"
    }
]
```
### Response 404 NOT FOUND:
```
{
    "errors": [
        "No connection registers found for ':dev1' and ':dev2'"
    ]
}
```

# To mention:
 - For this project I have followed a Behaviour Driven Development. A more functional and maybe the original idea from the TDD movement. That means that there is a lot of effort put into the entities and their behaviour. Not many unittests that can fall into testing the implementation rather than the functionality. You can see there is a lot of code on the models and classes that are agnostic of the implementation. They can be use for a backend service that is not an API, an application, a message worker, etc.
 - The service is easy to scale to add a new social network.
 - This project has been developed using clean code style for reusability and easy for testing. Since it is highly plausible that a new external API has to be added into the mix, or that other applications might re-use the entities like "Developer".
 - Right now the coverage is pretty high: ~93%. This is to be use internally in the dev team. Better not to show to management or decision makers.

# Improvements to be considered:
 - Compatibility: I have added versioning 'v1' to the API endpoints for backward compatibility. The endpoints without the version path, like the request endpoint in the exercise, access the latest version resources.
 - Compatibility: the docker servers and database must be in UTC timezone, not local. For the TZ to UTC. All times in logs and apps should be UTC.
 - Security: the response from the register endpoint is a json list. This is has a security flaw called "Top-level Array" that can be exploited by a malicious attacker. Better to use a key-value pair for top-level node of the json. Something like {"results": [...]}.
 - Security: better to implement a authentication method like with a token to access the endpoints.
 - Security: better to retrieve the Twitter, GitHub keys and secrects and database credentials from a secure service, like KeyVault from Azure or AWS.
 - Security: to apply rate limiting for the different API resources. Must be limiting, by ip for i.e.
 - Performance: to implement async calls to the different externals APIs (Twitter, GitHub...)
 - Performance: to apply pagination on the register endpoint results. Git a token for future queries to the client.
 - Performance: to implement async handling to the endpoint. Flask 2.0 allows the routes to be async, or to use another framework like RestAPI. But this latter is a project to infant to rely for long term maintainability.
 - Scalability: scalability should be in Kubernetes, with the asynchronous approach described in this section.
 - Scalability: the organisations entities shoud be stored in a separate table, along with a many-to-many relationship table for dbhistory-organisations. So the table "organisations" field of the dbhistory database should be removed.
 - Scalability: the database should not be deployed on a microservice like in this exercise. It should be in another service. 
 - Monitoring: To include a tracking db-telemetry for every request. Generate a UUID for every request and use it to track down issues in logs. In case of a failure, consider saving more telemetry information. In very tiny cases is good to save the request send by the client into database request and response. This might be detrimental for the storage and the performance.

# To add a new social network, like HackerNews for i.e.:
 - Add the module to `devsocial` dir.
 - Add your class name into the `FULLY_CONNECTED_CONTROLLERS` in `config.py`
 - Just implement the abstract method `connected()` in your controller.

#Inspiration references:
 - **"The Pragmatic Programmer"**, *by David Thomas, Andrew Hunt*. Addison-Wesley, Boston etc., (2000).
 - **"Clean Code: A Handbook of Agile Software Craftsmanship"**, *by Robert C. Martin*. Pearson (2008).