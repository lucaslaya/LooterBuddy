# Summer 2024 CS 3200 Project - Looter Buddy

## Made by: Lucas Laya Marina

## About

An application that allows players, developers, and streamers to interact with each other and data from a hypothetical lootershooter game.
It allows players to manage their inventory/loadout, look at their performance, and engage with community posts. For developers it shows player
performance data, equipment popularity data, and allows for posting and engaging with the community. Lastly streamers can also access
equipment popularity data and post/engage with posts.

## Current Project Components

Currently, there are three major components:
- Streamlit App (in the `./app` directory)
- Flask REST api (in the `./api` directory)
- MySQL setup files (in the `./database-files` directory)

## Getting Started with the repo
1. Clone the repo to your computer. 
1. Set up the `.env` file in the `api` folder based on the `.env.template` file. Just set a password and rename the file to `.env`
1. Start the docker containers with `docker-compose up --build` (make sure to be in the correct directory). 
1. To access the streamlit UI go to `http://localhost:8501` on your pc's browser


 