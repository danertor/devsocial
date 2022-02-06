## Developers connected API
A REST API of a simple social network of software developers.

Features:
 - Retrieve whether two “developers” are fully connected or not. Given a pair of developer handles they are considered connected if:
   - They follow each other on Twitter.
   - They have at least a GitHub organization in common.
	
# Setup before running:
Set the following environment variables with your own keys:
```
export TWITTER_API_CONSUMER_KEY=<TWITTER_API_CONSUMER_KEY>
export TWITTER_API_CONSUMER_SECRET=<TWITTER_API_CONSUMER_SECRET>
export TWITTER_API_ACCESS_TOKEN=<TWITTER_API_ACCESS_TOKEN>
export TWITTER_API_ACCESS_TOKEN_SECRET=<TWITTER_API_ACCESS_TOKEN_SECRET>
export GITHUB_API_TOKEN=<GITHUB_API_TOKEN>
```

# To run (docker-compose):
```
docker-compose build
docker-compose up
```
# To run (locally):
```
pip install -r requirements.txt
python runserver.py
```
# API:
## Realtime endpoint
GET /connected/realtime/:dev1/:dev2

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
 - Right now the coverage is pretty high, > 90%. This is to be use internally in the dev team. Better not to show to management or decision makers.

# Improvements to be considered:
 - Compatibility: I have added versioning 'v1' to the API endpoints for backward compatibility. The endpoints without the version path, like the request endpoint in the exercise, access the latest version resources.
 - Compatibility: the docker servers and database must be in UTC timezone, not local. For the TZ to UTC. All times in logs and apps should be UTC.
 - Security: the response from the register endpoint is a json list. This is has a security flaw called "Top-level Array" that can be exploited by a malicious attacker. Better to use a key-value pair for top-level node of the json. Something like {"results": [...]}.
 - Security: better to implement a authentication method like with a token to access the endpoints.
 - Security: better to retrieve the Twitter, GitHub keys and secrets and database credentials from a secure service, like KeyVault from Azure or AWS.
 - Security: to apply rate limiting for the different API resources. Must be limiting, by ip for i.e.
 - Performance: to implement async calls to the different externals APIs (Twitter, GitHub...)
 - Performance: to apply pagination on the register endpoint results. Git a token for future queries to the client.
 - Performance: to implement async handling to the endpoint. Flask 2.0 allows the routes to be async, or to use another framework like RestAPI. But this latter is a project to infant to rely for long term maintainability.
 - Scalability: scalability should be in Kubernetes, with the asynchronous approach described in this section.
 - Scalability: the organisations entities should be stored in a separate table, along with a many-to-many relationship table for dbhistory-organisations. So the table "organisations" field of the dbhistory database should be removed.
 - Monitoring: To include a tracking db-telemetry for every request. Generate an UUID for every request and use it to track down issues in logs. In case of a failure, consider saving more telemetry information. In very tiny cases is good to save the request send by the client into database request and response. This might be detrimental for the storage and the performance.

# To add a new social network, like HackerNews for i.e.:
 - Add the module to `devsocial` dir.
 - Add your class name into the `FULLY_CONNECTED_CONTROLLERS` in `config.py`
 - Just implement the abstract method `connected()` in your controller.
