URI Parser REST API
===================

URI Parser REST API is a simple Serverless-based REST API to parse URIs.

[![Build Status: GitHub Actions](https://github.com/rovellipaolo/serverless-uri-parser-rest-api/actions/workflows/ci.yml/badge.svg)](https://github.com/rovellipaolo/serverless-uri-parser-rest-api/actions)
[![Test Coverage: Coveralls](https://coveralls.io/repos/github/rovellipaolo/serverless-uri-parser-rest-api/badge.svg)](https://coveralls.io/github/rovellipaolo/serverless-uri-parser-rest-api)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


## Overview

URI Parser REST API uses `urllib` (https://docs.python.org/3/library/urllib.html) and `validator` (https://pypi.org/project/validators/) to parse a given URI and extract its parts.

**NOTE: This is just a playground to play with Python/Serverless, nothing serious.**


## Build

The first step is cloning the URI Parser REST API repository, or downloading its source code.

```shell
$ git clone https://github.com/rovellipaolo/serverless-uri-parser-rest-api
$ cd serverless-uri-parser-rest-api
```

Then, to install all the needed Python and Serverless dependencies, launch the following command:

```shell
$ make install-serverless
$ make build
```

For some of the commands described below you will also need to install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

**NOTE:** The local Serverless template can be validated via `make validate` command, while the OpenAPI definition can be generated locally (from the local Serverless template) via `make generate-openapi` command.


## Test

Once you've configured it (see the _"Build"_ section), you can run the tests and checkstyle as follows.

```shell
$ make test
$ make checkstyle
```

You can also run the tests with coverage by launching the following command:
```shell
$ make test-coverage
```

And/or configure the checkstyle to run automatically at every git commit by launching the following command:
```shell
$ make install-githooks
```


### Deploy

To deploy URI Parser REST API in AWS, launch the following commands:

```shell
$ make deploy stage=v1 version=1.0
...
Serverless APIGateway Service Proxy OutPuts
endpoints:
  GET - https://a88mr4js02.execute-api.eu-west-1.amazonaws.com/v1/api
...
```

Where `stage` can be for example _"dev"_ or _"prod"_, _"v1"_ or _"v2"_, etc.

```shell
$ curl --aws-sigv4 "aws:amz:eu-west-1:execute-api" --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" --request GET https://a88mr4js02.execute-api.eu-west-1.amazonaws.com/v1/api/status
{
    "message": "REST API up and running... long live and prosper!"
}

$ curl --aws-sigv4 "aws:amz:eu-west-1:execute-api" --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" --request POST https://a88mr4js02.execute-api.eu-west-1.amazonaws.com/v1/api/parse -d '{"uri": "https://user:password@domain.tld:8080/path?key=value#fragment"}'
{
    "fragment": "fragment",
    "host": "domain.tld",
    "port": 8080,
    "path": "/path",
    "query": "key=value",
    "raw": "https://user:password@domain.tld:8080/path?key=value#fragment",
    "scheme": "https",
    "userinfo": "user:password"
}
```

**NOTE:** The OpenAPI definition can be downloaded (from AWS) via `make download-openapi` command and will be also exposed at `https://a88mr4js02.execute-api.eu-west-1.amazonaws.com/v1/api`.


## Licence

URI Parser REST API is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
