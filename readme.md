# Job title to job function prediction 
the project builds a model that predicts the job functions based on its job title 
to use it
1. please download the model and the vectors using the colab note 
2. run the api and send it a post request in the way specified in the api section 
the project has two sections 
## jupyter notebook
the jupyter notebook was a colab note [found here](https://colab.research.google.com/drive/1QSs6-38jayz8g1DAI33FY7YC2niLZ5CH)
it has 5 sections :
- downloading files from drive 
- preprocessing and embedding the data 
- editing the arabic text in the job titles
- model defenition and related functions  
- function calling and model training and testing 
- uploading files to drive 
## api.py
is the flask api that loads the model and predicts job functions when givien a job title 
to use it run the api and send a request to the url in the variable URLs_job_function_predictor in the same file :
(your host) /predictor/(job title)
