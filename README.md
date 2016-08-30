## Reddit History

A simple suite of services that monitors a given list of subreddits on [reddit API](https://www.reddit.com/dev/api/), fetches all submissions and comments related to it, stores them in a Mongo database and exposes the data over a HTTP API. Uses [Docker](https://www.docker.com/) with [Docker Compose](https://docs.docker.com/compose/).

### Usage

```sh
$ docker-compose up
```

The API is accessible at `localhost:5000/items` with the following params:
 - __from, to__ (required) - the time interval (in UNIX timestamp).
 - __subreddit__ (required).
 - __keyword__ (optional) - it will return only the items containing the `keyword` in the title/body.

So, a call might look like `http://localhost:5000/items?from=1472546520&to=1472546534&subreddit=python&keyword=interactions`

#### Config

The monitored subreddits can be changed in `reddit_worker/config.yml`. Another configurable option is `polling_interval`(in seconds) in the same file. Note that after any change, the docker containers must be rebuilt, so a next run would be:

```sh
$ docker-compose --build up
```

### Tests

```sh
$ bash run_tests.sh

$ EXTERNAL_TEST=1 bash run_tests.sh
```
This script sets-up the docker containers, and run all tests. It can also run external tests (to check the Reddit API) if the environment variable is set like above.
