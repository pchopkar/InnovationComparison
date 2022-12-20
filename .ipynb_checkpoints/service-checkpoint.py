
import logging
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import gc
#import numpy as np
#from numba import jit, njit
# import torch
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#@njit 
def dataFetch(datFetch:str):
    logging.info("Inside dataFetch()")
    df = pd.read_csv(datFetch, encoding= 'unicode_escape')
    logging.info("dataFetch Done")
    return df

#@njit
def modelFetch():
    logging.info("Inside modelFetch()")
    model = SentenceTransformer('paraphrase-albert-small-v2')
    logging.info("Model Fetch Done")
    return model
#@njit
def innovationComp(Brief_Idea_input: str,
                    Concept_and_objective_Input : str,
                    Potential_area_of_applicatioin_Input : str, 
                    Sector_Input : str,
                    df,model):
    status = False
    try:
        logging.info("Entry of innovationComp() function")
        #data = ['India is my country','Hello World','Example','who are you']
        Brief_Idea_data = df['Briefly explain newness/uniqueness of the innovation'].to_list()
        Concept_and_objective_data = df['Concept & Objective'].to_list()
        Potential_area_of_applicatioin_data = df['Specify the potential areas of application in industry/market in brief'].to_list()
        Sector_data = df['Idea Sector'].to_list()
        
        Brief_Idea_data.append(Brief_Idea_input)
        Concept_and_objective_data.append(Concept_and_objective_Input)
        Potential_area_of_applicatioin_data.append(Potential_area_of_applicatioin_Input)
        Sector_data.append(Sector_Input)

        i = len(Brief_Idea_data)-1

        logging.info("All Input Fetched")

        Brief_Idea_vec = model.encode(Brief_Idea_data)
        Brief_Idea_compare = cosine_similarity(
                            [Brief_Idea_vec[i]],
                            Brief_Idea_vec[0:i+1])
        logging.info("Brief Idea vector done")

        Concept_and_objective_vec = model.encode(Concept_and_objective_data)
        Concept_and_objective_compare = cosine_similarity(
                            [Concept_and_objective_vec[i]],
                            Concept_and_objective_vec[0:i+1])          
        logging.info("Concept and Objective vector done")

        Potential_area_of_applicatioin_vec = model.encode(Potential_area_of_applicatioin_data)
        Potential_area_of_applicatioin_compare = cosine_similarity(
                            [Potential_area_of_applicatioin_vec[i]],
                            Potential_area_of_applicatioin_vec[0:i+1])    
        logging.info("Potential Area of Application vector done")

        Sector_vec = model.encode(Sector_data)
        Sector_compare = cosine_similarity(
                            [Sector_vec[i]],
                            Sector_vec[0:i+1])   
        logging.info("Sector vector done")   
        li = []
        for k in range(Brief_Idea_compare.size-1) :
            if((not any(Brief_Idea_input)) or (not any(Concept_and_objective_Input)) or (not any(Potential_area_of_applicatioin_Input)) or (not any(Sector_Input))):
                logging.info("Input is Empty") 
                raise Exception("Input is Empty")
            elif((Brief_Idea_compare[0][k]*100)>85.00 and (Concept_and_objective_compare[0][k]*100)>85.00 and (Potential_area_of_applicatioin_compare[0][k]*100)>85.00 and (Sector_compare[0][k]*100)>85.00):
                        #li.append(k)
                        #outputS = inputS + "\n ::::::::is " + str(compare[0][k]*100) + " similar to :::::::: \n" + " " + data[k]
                        
                        # outputS = { "Briefly explain newness/uniqueness of the innovation - Given": Brief_Idea_input,
                        #             #"Briefly explain newness/uniqueness of the innovation - Old": Brief_Idea_data[k],
                        #             "Briefly explain newness/uniqueness of the innovation - Comparison": Brief_Idea_compare[0][k]*100,

                        #             "Concept & Objective - Given " : Concept_and_objective_Input,
                        #             #"Concept & Objective - Old " :Concept_and_objective_data[k],
                        #             "Concept & Objective": Concept_and_objective_compare[0][k]*100,

                        #             "Specify the potential areas of application in industry/market in brief - Given" : Potential_area_of_applicatioin_Input, 
                        #             #"Specify the potential areas of application in industry/market in brief - Old" : Potential_area_of_applicatioin_data[k],
                        #             "Specify the potential areas of application in industry/market in brief - Comparison": Potential_area_of_applicatioin_compare[0][k]*100,
                                    
                        #             "Idea Sector - Given" : Sector_Input,
                        #             #"Idea Sector - Old" : Sector_data[k],
                        #             "Idea Sector - Comparison" : Sector_compare[0][k]*100,

                        #             "Title_Of_Proposed_Idea": df['Title of proposed idea/innovation'][k], 
                        #             "Reference No" : df["Reference No"][k],
                        #             "Status " : "Duplicate Idea"
                        #         }
                        # li.append(outputS)
                        status=True
                        logging.info("Idea is Repeated") 
                        
        # if not li :
            
        #     outputS = {    "Briefly explain newness/uniqueness of the innovation - Given": Brief_Idea_input,
        #                             #"Briefly explain newness/uniqueness of the innovation - Old": "NA",
        #                             "Briefly explain newness/uniqueness of the innovation - Comparison": "0%",

        #                             "Concept & Objective - Given " : Concept_and_objective_Input,
        #                             #"Concept & Objective - Old " :"NA",
        #                             "Concept & Objective": "0%",

        #                             "Specify the potential areas of application in industry/market in brief - Given" : Potential_area_of_applicatioin_Input, 
        #                             #"Specify the potential areas of application in industry/market in brief - Old" : "NA",
        #                             "Specify the potential areas of application in industry/market in brief - Comparison": "0%",
                                    
        #                             "Idea Sector - Given" : Sector_Input,
        #                             #"Idea Sector - Old" : "NA",
        #                             "Idea Sector - Comparison" : "0%",

        #                             "Title_Of_Proposed_Idea": " ", 
        #                             "Reference No" : " ",
        #                             "Status " : "Hurray! New Idea"
        #                 }
        #     li.append(outputS)
        if status==False:
            logging.info("Idea is Unique") 
    except Exception as e:
        logging.info("Oops Exception Occured")
        print("Oops!", e.__class__, "occurred.")
    finally:
        logging.info("Inside Finally Block")
        del Brief_Idea_data
        del Concept_and_objective_data
        del Potential_area_of_applicatioin_data
        del Sector_data
        del Brief_Idea_vec 
        del Brief_Idea_compare 
        del Concept_and_objective_vec
        del Concept_and_objective_compare
        del Potential_area_of_applicatioin_vec
        del Potential_area_of_applicatioin_compare
        del Sector_vec
        del Sector_compare
        gc.collect()
        logging.info("Exiting Finally block")            
    #return li
    return status