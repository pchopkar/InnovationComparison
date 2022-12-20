from fastapi import FastAPI
import logging
import service as s
import csv
import pandas as pd
import io
#import numpy as np
from sklearn.model_selection import train_test_split
#import torch
#from numba import vectorize,jit,njit
#device = torch.device('cuda')
logging.basicConfig(level=logging.INFO)
#app = FastAPI()
# @app.post("/innovationDuplication")
# def root(Brief_Idea_input: str,Concept_and_objective_Input : str,Potential_area_of_applicatioin_Input : str, Sector_Input : str):
# @jit(nopython=True)
# @njit 


def root():
    logging.info("Inside root()")
    #df = dataFetch('InnovationTrainData.csv')
    #df1 = dataFetch('InnovationTrainData.csv')
    #df = df.head(10)
    #df = df1.head(5)
    logging.info("Fetching Approved List")
    df1 = s.dataFetch('Approved_Ideas.csv')
    df1['Status'] = "Approved"
    # print(df1.head(4))

    logging.info("Fetching Not Approved List")
    df2 = s.dataFetch('Not_Approved_Ideas.csv')
    df2['Status'] = "Not Approved"

    logging.info("Concat approve non approved Excel sheet")
    df = pd.concat([df1,df2],ignore_index=True)
    #df = df.head(20)
    #df = pd.concat(df2, ignore_index=True)
    #df.to_excel(df1, index=False)

    #df.app
    model = s.modelFetch()
    logging.info("Data and Model Fetched")
    logging.info("Train Test Data Segration")
    train,test = train_test_split(df, test_size=0.30, random_state=0)
    train.to_csv("Train.csv", sep='\t', encoding='utf-8')
    test.to_csv("Test.csv", sep='\t', encoding='utf-8')
    # myFile = open('train.csv', 'w')
    # writer = csv.writer(myFile)
    # writer.writerow(['Sr No.','Reference No',	'Incubatee Name',	'State',	'District',	'Title of proposed idea/innovation',	
    #                 'Whether the idea involves use of existing intellectual property or not, give brief detail there of',	
    #                 'Briefly explain newness/uniqueness of the innovation',
    #                 'Concept & Objective',
    #                 'Specify the potential areas of application in industry/market in brief'
    #                 'Briefly provide the market data for the potential idea/ innovation',
    #                 'Name and details of Mentors',
    #                 'Experience and Qualification of Mentors',
    #                 'Contact Details of Mentors',
    #                 'Current Development Status of innovation',
    #                 'Expected time of completion of idea',
    #                 'Idea Sector'])
    # i=1                
    # for i in range(len(train)):
    #     writer.writerow(train[i])
    #data = ['India is my country','Hello World','Example','who are you']
    #df = s.dataFetch('InnovationTestData.csv')
    #df = df.head(10)
    fields = ['Briefly explain newness/uniqueness of the innovation', 'Concept & Objective',
              'Specify the potential areas of application in industry/market in brief', 'Idea Sector', 'Old Status','Status']
    rows = []
    #logging.info("Input Size " + len(df))
    filename = "Result.csv"
    for i in range(len(test)):
            logging.info(str(i) + " Input")
            Brief_Idea_input = test['Briefly explain newness/uniqueness of the innovation'].iloc[i]
            Concept_and_objective_Input = test['Concept & Objective'].iloc[i]
            Potential_area_of_applicatioin_Input = test['Specify the potential areas of application in industry/market in brief'].iloc[i]
            Sector_Input = test['Idea Sector'].iloc[i]

            logging.info("Calling InnovationComp")
            status = s.innovationComp(Brief_Idea_input, Concept_and_objective_Input,
                                    Potential_area_of_applicatioin_Input, Sector_Input,train,model)
            logging.info("Returned from InnovationComp with processed input "+ str(i) + " "+str(status))

            rows1 = [Brief_Idea_input, Concept_and_objective_Input,
                    Potential_area_of_applicatioin_Input, Sector_Input, test['Status'].iloc[i], status]
            rows.append(rows1)
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows) 
    logging.info("File Initiated to Prepare")
    logging.info("Returned from root()")
    # return li
# Brief_Idea_input = input("Enter Your Brief_Idea_input")
# Concept_and_objective_Input = input("Enter Your Concept_and_objective_Input")
# Potential_area_of_applicatioin_Input = input("Enter Your Potential_area_of_applicatioin_Input")
# Sector_Input = input("Enter Your Sector_Input")
# print(root(Brief_Idea_input,Concept_and_objective_Input,Potential_area_of_applicatioin_Input,Sector_Input))


root()
