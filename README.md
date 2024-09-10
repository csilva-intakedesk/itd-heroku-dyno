# ITD EPA GIS Lambda Layer

## Requires

The output data from: https://github.com/USEPA/ORD_SAB_Model 

## Deploy

Deploy using Heroku Git
Use git in the command line or a GUI tool to deploy this app.

```bash
Install the Heroku CLI
Download and install the Heroku CLI.
```

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```bash
$ heroku login
```

Clone the repository
Use Git to clone itd-sf's source code to your local machine.

```bash
$ heroku git:clone -a itd-sf
$ cd itd-sf
```

Deploy your changes
Make some changes to the code you just cloned and deploy them to Heroku using Git.
Make sure that you remove the condition for the `EPA_CWS_V1` files if any were updated.

```bash
$ git add .
$ git commit -am "make it better"
$ git push heroku main
```

## Lambda

This is using Heroku Dyno which is the equivalent of AWS Lambda. The main difference is how the app is
instantiated during a request. Refer to `lambda_fuction.py` for more details.

## Python Libraries

To add or remove any library required by the Python scripts, refer to `requirements.txt`
