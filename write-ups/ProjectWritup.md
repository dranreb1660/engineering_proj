# METIS ENGINEERING PROJECT - End To End Fantasy Premier League Data pipeline/App

## FANTASY PREMIER LEAGUE

### Abstract:
Fantasy premier league is increasing in popularity at a tremendous amount year by year. During the 2015/2016 season this online fantasy game registered about 4 million participants (Managers). fast forward 5 years later, the 2020/2021 season saw a total of about 8 million managers and are projected to reach over 10 million when the English Premier League resumes later next month on august 2021 for the next season. 

This comes at no big suprise, however, as the use of data science has found its ways in many sporting activities and are surely here to stay. How joyful is it to use tools we love using (Data Science tool and techneques) to do the things we enjoy doing (Soccer). That is exactly what I want to accomplish in this project - use data science to play "the beautiful game".

That weekly ritual of re- thinking your team you spent hours beuilding a few days/ week before, which player to select out of over 700 players to help you overcome the over 8 million fpl managers or within your friends group. What if there was a model that gives you the possible high point scorers in each gameweek? In this project, I will build an end to end application that will be capable to predict points a player will score in the coming gameweek given his previous week statistics.

### Design
* I will build a pipeline that will collect and update data, and store the data in a SQL database.
* I will use then querry from the database to build a Predictive model, save the model and update the model as new data becomes available in the database.
* The model will then be used to make predictions based on user input.
* I can then deploy the app to be hosted on the cloud to be accesible to others.    

### Data :
* The data we will use is from the [Official Fantasy Premier Leage](https://fantasy.premierleague.com) API
* The data contains all previous week stats for over 700 players for 38 gameweeks. 
* I will use a player's previus weeks' stats to predict the points of the player in the next gameweek?

### Algorithm
* The main algorithm is be a predictive model with Linear Regression that takes an input from a user and spills out. The app currently has two functionalities;
   1.Manual Prediction
   	* Here, user can fill a form of five fields namely was_home, Home Team score, Away Team Score, Minutes, Goals Scored, Assists, Clean sheets, Total Points. The user can then submit this form to get a prediction of  the expected points of the player the following week. 

   2. Semi- Auto Prediction
   	* Here, we present user with 2 drop down menus to select the name of the player and the curent week. this input is used to rach the database to get the players stats needed to make prediction. upon submit, a predicted point is returned to user for the following week. 
 ![](images/cat.jpg)

### Tools:
* Data Acquisition and storage and Modeling
  * Python  
  * pandas
  * SQL
  * Scikit-learn

 * Deployment
   * Flask
   * Docker 



