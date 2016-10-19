# Summary
The goal of this project was to try to predict time to adoption for shelter dogs.  I used data from the Austin Animal Center (inspired by this [Kaggle competition](https://www.kaggle.com/c/shelter-animal-outcomes)).

The analysis is split into three notebooks:
- data cleaning
- EDA
- model building and analysis

To accompany the findings, I put together a basic Flask app to generate predictions for a given dog.  The app is running on an AWS EC-2 instance [here](http://ec2-54-175-179-135.compute-1.amazonaws.com/myapp/).  Since some of the app is a little computationally intensive, and I'm using a small box, it may need a little patience and page refreshes to work!  

If you put in the information for a given dog in the form on the left, the app will show you whether that dog is predicted to be adopted within 8 days, and show its adoption probability curve versus the rest of the population.

A version that runs locally can be found in the Flask-app folder.
