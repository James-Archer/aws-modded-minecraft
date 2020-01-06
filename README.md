# aws-modded-minecraft
Code and instructions for setting up a modded Minecraft server on AWS, and some tools for server maintenance. This takes advantage of some of the AWS free-tier features, but the EC2 instance will not be free because of the RAM requirements.

# Introduction

The guide here will cover things in as much detail as I will need to repeat this in the future. Hopefully it'll be pretty thorough, and I’ll try to explain things here as necessary.

The features of this project are:
* A Forge modded Minecraft server.
* Automatic backups as regular as you would like.
* Automatic server shutdown and backup when no players are online.
* A (scalable) website where players can boot the server (or any number of servers) up (password protected) when they want to play.
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
###Verify it all works
### Optional: static IP
### A note about copying an existing world in
## Lambda functions
### Permissions and inputs
### Getting current server status
### Activating servers
## Website 
### Setting up
### Changes for single/multi server
### Host on S3
