from fastapi import FastAPI
import logging
import service as s

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
@app.post("/innovationDuplication")
def root(Brief_Idea_input: str,Concept_and_objective_Input : str,Potential_area_of_applicatioin_Input : str, Sector_Input : str):
    logging.debug("Inside root()")
    df = s.dataFetch('InnovationTestData.csv')
    logging.debug("Input Size " + len(df))
    for i in range(len(df)):
        Brief_Idea_input = df['Briefly explain newness/uniqueness of the innovation'][i]
        Concept_and_objective_Input = df['Concept & Objective'][i]
        Potential_area_of_applicatioin_Input = df['Specify the potential areas of application in industry/market in brief'][i]
        Sector_Input = df['Idea Sector'][i]
        li = s.innovationComp(Brief_Idea_input,Concept_and_objective_Input,Potential_area_of_applicatioin_Input,Sector_Input)
    logging.debug("Returned from root()")
    return li  
# Brief_Idea_input = input("Enter Your Brief_Idea_input")
# Concept_and_objective_Input = input("Enter Your Concept_and_objective_Input")
# Potential_area_of_applicatioin_Input = input("Enter Your Potential_area_of_applicatioin_Input")
# Sector_Input = input("Enter Your Sector_Input")
# print(root(Brief_Idea_input,Concept_and_objective_Input,Potential_area_of_applicatioin_Input,Sector_Input))
