
import logging
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def dataFetch(datFetch:str):
    logging.debug("Inside dataFetch()")
    df = pd.read_csv(datFetch, encoding= 'unicode_escape')
    logging.debug("dataFetch Done")
    return df

def modelFetch():
    logging.debug("Inside modelFetch()")
    model = SentenceTransformer('paraphrase-albert-small-v2')
    logging.debug("Model Fetch Done")
    return model

def innovationComp(Brief_Idea_input: str,Concept_and_objective_Input : str,Potential_area_of_applicatioin_Input : str, Sector_Input : str):
    try:
        logging.debug("Entry of function")
        global df,model
        df = dataFetch('InnovationTrainData.csv')
        #df = df1.head(5)
        model = modelFetch()
        logging.debug("Data and Model Fetched Returned")
        #data = ['India is my country','Hello World','Example','who are you']
        Brief_Idea_data = df['Briefly explain newness/uniqueness of the innovation'].to_list()
        Brief_Idea_data.append(Brief_Idea_input)

        Concept_and_objective_data = df['Concept & Objective'].to_list()
        Concept_and_objective_data.append(Concept_and_objective_Input)

        Potential_area_of_applicatioin_data = df['Specify the potential areas of application in industry/market in brief'].to_list()
        Potential_area_of_applicatioin_data.append(Potential_area_of_applicatioin_Input)

        Sector_data = df['Idea Sector'].to_list()
        Sector_data.append(Sector_Input)

        i = len(Brief_Idea_data)-1

        logging.debug("All Input Fetched")

        Brief_Idea_vec = model.encode(Brief_Idea_data)
        Brief_Idea_compare = cosine_similarity(
                            [Brief_Idea_vec[i]],
                            Brief_Idea_vec[0:i+1])
        logging.debug("Breif Idea vector done")

        Concept_and_objective_vec = model.encode(Concept_and_objective_data)
        Concept_and_objective_compare = cosine_similarity(
                            [Concept_and_objective_vec[i]],
                            Concept_and_objective_vec[0:i+1])          
        logging.debug("Concept and Objective vector done")

        Potential_area_of_applicatioin_vec = model.encode(Potential_area_of_applicatioin_data)
        Potential_area_of_applicatioin_compare = cosine_similarity(
                            [Potential_area_of_applicatioin_vec[i]],
                            Potential_area_of_applicatioin_vec[0:i+1])    
        logging.debug("Potential Area of Application vector done")

        Sector_vec = model.encode(Sector_data)
        Sector_compare = cosine_similarity(
                            [Sector_vec[i]],
                            Sector_vec[0:i+1])   
        logging.debug("Sector vector done")   
        li = []
        
        for k in range(Brief_Idea_compare.size-1) :
            if((not any(Brief_Idea_input)) or (not any(Concept_and_objective_Input)) or (not any(Potential_area_of_applicatioin_Input)) or (not any(Sector_Input))):
                logging.debug("Input is Empty") 
                raise Exception("Input is Empty")
            elif((Brief_Idea_compare[0][k]*100)>85.00 and (Concept_and_objective_compare[0][k]*100)>85.00 and (Potential_area_of_applicatioin_compare[0][k]*100)>85.00 and (Sector_compare[0][k]*100)>85.00):
                        #li.append(k)
                        #outputS = inputS + "\n ::::::::is " + str(compare[0][k]*100) + " similar to :::::::: \n" + " " + data[k]
                        
                        outputS = { "Briefly explain newness/uniqueness of the innovation - Given": Brief_Idea_input,
                                    #"Briefly explain newness/uniqueness of the innovation - Old": Brief_Idea_data[k],
                                    "Briefly explain newness/uniqueness of the innovation - Comparison": Brief_Idea_compare[0][k]*100,

                                    "Concept & Objective - Given " : Concept_and_objective_Input,
                                    #"Concept & Objective - Old " :Concept_and_objective_data[k],
                                    "Concept & Objective": Concept_and_objective_compare[0][k]*100,

                                    "Specify the potential areas of application in industry/market in brief - Given" : Potential_area_of_applicatioin_Input, 
                                    #"Specify the potential areas of application in industry/market in brief - Old" : Potential_area_of_applicatioin_data[k],
                                    "Specify the potential areas of application in industry/market in brief - Comparison": Potential_area_of_applicatioin_compare[0][k]*100,
                                    
                                    "Idea Sector - Given" : Sector_Input,
                                    #"Idea Sector - Old" : Sector_data[k],
                                    "Idea Sector - Comparison" : Sector_compare[0][k]*100,

                                    "Title_Of_Proposed_Idea": df['Title of proposed idea/innovation'][k], 
                                    "Reference No" : df["Reference No"][k],
                                    "Status " : "Duplicate Idea"
                                }
                        li.append(outputS)
                        
        if not li :
            
            outputS = {    "Briefly explain newness/uniqueness of the innovation - Given": Brief_Idea_input,
                                    #"Briefly explain newness/uniqueness of the innovation - Old": "NA",
                                    "Briefly explain newness/uniqueness of the innovation - Comparison": "0%",

                                    "Concept & Objective - Given " : Concept_and_objective_Input,
                                    #"Concept & Objective - Old " :"NA",
                                    "Concept & Objective": "0%",

                                    "Specify the potential areas of application in industry/market in brief - Given" : Potential_area_of_applicatioin_Input, 
                                    #"Specify the potential areas of application in industry/market in brief - Old" : "NA",
                                    "Specify the potential areas of application in industry/market in brief - Comparison": "0%",
                                    
                                    "Idea Sector - Given" : Sector_Input,
                                    #"Idea Sector - Old" : "NA",
                                    "Idea Sector - Comparison" : "0%",

                                    "Title_Of_Proposed_Idea": " ", 
                                    "Reference No" : " ",
                                    "Status " : "Hurray! New Idea"
                        }
            li.append(outputS)
            logging.debug("Idea is Unique") 
    except Exception as e:
        logging.debug("Oops Exception Occured")
        print("Oops!", e.__class__, "occurred.")            
    return li