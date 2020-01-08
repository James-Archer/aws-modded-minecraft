# aws-modded-minecraft (Under construction)
Code and instructions for setting up a modded Minecraft server on AWS, and some tools for server maintenance. This takes advantage of some of the AWS free-tier features, but the EC2 instance will not be free because of the RAM requirements.

# Introduction

The guide here will cover things in as much detail as I will need to repeat this in the future. Hopefully it'll be pretty thorough, and I’ll try to explain things here as necessary. I put this together because I couldn't find anything that was both complete in the features I wanted, and didn't have a whole lot of assumed knowledge. *Disclaimer*: most of the stuff here I learned as I did it so I'm sure there are better ways to do things, and there's all sorts of nonsense in here, but this works for me and that's my standard for this.

The features of this project are:
* A Forge modded Minecraft server.
* Automatic backups as regular as you would like.
* Automatic server shutdown and backup when no players are online.
* A (scalable) website where players can boot the server (or any number of servers) up (password protected) when they want to play. [The code for this is hosted here!](https://github.com/James-Archer/mc-server-manager-website-template)
This is all to minimise the costs of leaving the server running 24/7, and reduce the maintenance required by the server maintainer.

## AWS services used
* S3 for the setup files, backup location, and hosting the website.
* EC2 for hosting the Minecraft server.
* Lambda for letting the website talk to the EC2 instances. 
* IAM for enabling them all to talk to each other

## Other tools used
* A few bash scripts
* Crontabs for scheduling
* Python code to run on Lambda, and to perform the automatic shutdown checks.
* React.js for the website.
# Setting up
## Getting the server running
For the AWS side of things, *most* of this is taken from the video/accompanying Medium post from Andrew Brown: https://dev.to/exampro/how-to-run-a-modded-minecraft-server-on-aws-4hlk 

I’ll summarise it here, and include any changes I made and why.
### Set up S3 bucket
### Create IAM roles
### Create EC2 instance
The assumed name of the EC2 instance is Minecraft-server-\<SERVER-NAME\>, so that the Lambda functions can identify it by the name. I could use the InstanceID but if I have to create a new instance for whatever reason, this way is easier.
### Verify it all works
### Optional: static IP
### A note about copying an existing world in
## Lambda functions
I have two separate Lambda functions here, but you could put them into the same one and set up the API a bit better. Both Lambdas are running the default Python 3.8 runtime. It'll probably work with others (except 2.7 because c'mon it's 2020, people) but I haven't verified it.

You simply need to copy in code in [the Lambda folder]( https://github.com/James-Archer/aws-modded-minecraft/tree/master/Lambda) into each function, and they should work. Test code is left as an exercise for the reader.
### Permissions and inputs
CloudWatch is enabled, and it also needs access to EC2 so I used the *AmazonEC2FullAccess* policy. I could make one with only the permissions it needs, but if there's a security issue someone can exploit by getting into my EC2 instance via these Lambda functions, I'll take that as a learning experience when it happens. 

Both will also need API gateways. Go to "Add Trigger", select "API Gateway". I used the HTTP API Beta, and enabled CORS from the additional settings. I have no idea if any of those choices mattered, but it works so ¯\\_(ツ)_/¯. Both Lambdas can use the same API gateway template so add the same one to both functions. 

### Getting current server status (status-minecraft-server)
You will need to add the server name in the `servers` list. This takes a simple GET request, and checks the EC2 instances for the desired server, and determines if it is on or off. “Running” and “Pending” both count for the “on” state. It then returns the state of the server to the website.
### Activating servers (start-minecraft-server)
The activation request is a POST request containing the server name and the password. You will need to add the server name **(Note that the server name here does NOT include the “Minecraft-server-“ part. i.e. if your EC2 instance name is “Minecraft-server-HelloWorld“ then you need to put just “HelloWorld” here)** and the password you want here. Hardcoded in plain text because this is a Minecraft server not a bank.

The function will decode the JSON data from base64 and check against the password above. If it is correct, it will attempt to activate the EC2 instance. Appropriate success and failure codes are sent back to  the website.
## Website 
The React.js code is available [here]( https://github.com/James-Archer/mc-server-manager-website-template). Make sure you have npm installed to test and build the site.
### Setting up
Clone the repo above, and install the packages:
~~~~
git clone https://github.com/James-Archer/mc-server-manager-website-template
cd mc-server-manager-website-template/web-app
npm install
~~~~
While the packages install, add your own stuff to the website. Edit /web-app/src/App.js and change the following:
* 7: Your Lambda API endpoint here\*.
* 8: Your other Lambda endpoint here\*.
* 41: The name of the server that matches the format above under [Activating servers](https://github.com/James-Archer/aws-modded-minecraft/blob/master/README.md#activating-servers-start-minecraft-server). 
* 52: As above.
* 146: The name of your server to be displayed. Doesn’t have to match above. Purely flavour.
* 162: Can add whatever text you want here. 

\*To get the API endpoint address, find them in your Lambda functions: click on the “API Gateway” in the Designer section, and copy the “API Endpoint” address.

If you want to change and style stuff, go to town in App.css, and if you don’t like the egg then swap out logo.svg. Might work with non-SVG images, might not. That’s your problem.

Test the website by running `yarn start` and once it’s to your liking, build the server with `yarn build`. This will create a “build” directory in the web-app folder and compile the website and all required files into it.
### Host on S3
I followed this guide for [deploying a react app to S3](https://www.newline.co/fullstack-react/articles/deploying-a-react-app-to-s3/) so I recommend you do too. If you want your own domain name for the website, there’s specific instructions for that, otherwise the URL will be of the form \<bucket-name\>.s3-website.\<bucket-region\>.amazonaws.com. Not super memorable but free so just bookmark it and you’ll be fine.
### Changes for single/multi server
To run multiple servers, repeat the process for creating the S3 buckets and EC2 instances for each server, making sure the names (EC2 instance Tag: Name) follow the template “Minecraft-server-\<UNIQUE-NAME\>”. Simply add the server name to the `servers` list in the `status-minecraft-server` function and adding the name and password to `start-minecraft-server` function. This way you can have a unique password for each server if you wish. The former is a Python `list` and the latter is a `dictionary` so look those up if you don’t know how they work.

To change the server, see [my website code here with two servers running.]( https://github.com/James-Archer/mc-server-manager-website/tree/bbed935b533e3c4601fbd2e48c6fc92848110cdd) Note that the commit linked here is what the template in this tutorial uses. Feel free to check the latest version but I have no idea what it’ll look like. 

My implementation for two servers is to copy  a bunch of functions and hard code it all in. I’m sure there’s a better way of scaling it but it took me half an hour and it works for me so if you have a better, scalable solution feel free to make a PR. 

