# About the project
This is a chatbot project that I made using Rasa which is an open-source framework for developing AI powered, industrial grade chatbots. For this project, I developed a banking system consisting of 3 components:
* Node Backend
* Rasa Backend
* Frontend

## Node Backend
This comprises of a Node.js application where user can signup to the bank by opening an account and perform basic operations. These operation include queries like *Account Balance*, *Transaction History* & *Account Details*. User can also *Transfer Money* to other account in the same bank.

## Rasa Backend
This comprises of rasa rasa chatbot that is trained and configured to understand all the types of queries a user can ask. It then classify user query using *NLU (Natural Language Understanding)* to get the *Intent* of the query & perform a certain *Action* based on that. I have also made some *Custom Actions* according to the needs of our project.

## Frontend
This comprises of a basic HTML, CSS & Javascript frontend through which the user can access and interact with the backend. The wesite includes *Sign-In / Sign-Up page*, *Homepage* & *Transfer Money page*. The chatbot can be accessed from the homepage itself.

## Clone
Firstly clone this repo using git:

```git clone https://github.com/uchiha-satyam/Chatbot.git```

For cloning this project you require the following:

* **python 3.8.\*** (Install from website)
* **Node.js** (Install from website)
* **nodemon** (Install using ```npm install -g nodemon```)
* Activate virutal environment using: ```.\myenv\Scripts\activate```
* **rasa[spacy]** (Install using ```pip install rasa[spacy]```)
* **rasa-sdk** (Install using ```pip install rasa-sdk```)
* You will need access to a MongoDB Atlas database for storing user data. Fill appropriate details in the **./application/backend/sample.env** file and then rename it to **.env**

To install dependencies & train rasa model follow the given steps:

* From **./application/backend/** directory run: ```npm ci```
* From **./application/frontend/** directory run: ```npm ci```
* From **./** directory run: ```rasa train```

## Run
To run the project follow the steps given below:

* From **./application/backend/** directory run: ```node app.js```
* From **./** run: ```rasa run actions```
* From **./** run: ```rasa run --enable-api --cors "*"```
* From **./application/frontend/** run a live server using **Live Server(extention)** in VsCode. This live server should be started for **./application/frontend/chatbot.html**

Now your project is up and running.