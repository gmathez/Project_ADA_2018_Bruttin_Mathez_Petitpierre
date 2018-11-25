# Expanding Nutri-Score  : take your menu to the next level

## Abstract
The nutrition is a major issue in the Western civilization. The bad eating habits are becoming one of the main causes of illness in the world, with very heavy impact on public health. Recently, the various products are being graded through nutrition benefits indices, as for example Nutri-Score. 
Nutri-Score can give an accurate estimation on how healthy an ingredient can be. However, if it can make sense at the ingredient scale, the concept of Nutri-Score would be way more valuable if it were computed considering wider time spans instead of individual ingredients. Indeed, in its present version, Nutri-Score would always give a very high grade to white rice, for example. However, if you only eat white rice, your overall nutrition will not be optimal. The present computation of Nutri-Score is strongly limited, as it is unable to contextualize the consumption of a certain product in regard with the daily feeding practises.

## Research questions
* Global nutritional evaluation across a short to middle period of time (days to weeks) instead of an ingredient focused approach
* List the consumption of additives with a short description and an health evaluation
* Warning about nutritional deficiencies, excesses and lack of diversity
* Proposition of healthier ingredients choices to improve the eating habits, based on the previous evaluations 

## Dataset
We will use the database from Open Food Facts that is a collaborative database. Users take a picture of a food product and the list of ingredients and provide useful information. The database contains more than 680’000 product at this day. 

The database is not complete. Every products do not have full information because the user may not take a picture of the list of ingredients or the information for a particular product do not exist (not public, differents laws). The terms of use say clearly that their database may contain errors, as the data is manually entered, often partially. Therefore, the data provided can only be used for informative information and not for medical purpose.

The database are in CSV and can be easily use in our computer because of its relatively small size. 

With Milestone 2, we clean and fill the database that you can download [here (using EPFL mail)](https://drive.google.com/drive/folders/1G8-zV0-ctUQSk3X2qqIoh6SKuCFYmmAd?usp=sharing). 

## List of internal milestones up until project milestone 2
* Check which fraction of the ingredients contains complete or almost complete raw nutritional data (nutrients, fats, etc.) ✓
* Check which fraction of the products from the database already have a Nutri-score and check if the latter seems coherent with the Nutri-score’s official computation criteria. Adapt our formula accordingly ✓
* Gather informations about nutritional recommendations in order to establish new computation criteria ✓
* Try to enrich and complete the data in regard with similar products ✓
* Treat the issue of very incomplete products within the data set ✓

## List of internal milestones up until poster presentation
### User interface design
* Develop an interface, so that the user can enter the aliments he eats into the program
* For missing information, the user must be able to choose either to enter the data himself/herself, or to use the automatic reconstruction of the data by the closest foods at category level, or to use the automatic data query of the US Department of Agriculture
* The interface must allow the user to enter the quantities consumed, for each food
* The interface must optionally allow the user to indicate the period over which he/she has consumed these foods (snacks, meals, days, etc.)
### Algorithm
* Adapt the algorithm to take the quantities into account and to weight them in order to obtain a global indice
* Adapt the algorithm to take into account the nutrients of the expanded Nutri-score
* Adapt the algorithm to determine if the quantity of food ingested during the specified time seems to be reasonable
* Improve the robustness of the algorithm by improving error handling when erroneous or non-numerical values are entered by the user
* Adapt the algorithm to compare the values entered with the nutritional recommandations and identify deficiencies, excesses and lack of diversity
* Adapt the algorithm to be able to retrieve elements with the desired nutritional values, so that it can be suggested to the user
### Information design
* The interface must present the user with the quantities of nutrients he/she has consumed
* The user must receive an indicative assessment of the nutritional quality of his/her food (expanded Nutri-score)
* The program must indicate to the user the main problems of his diet. Warn the user about nutritional deficiencies, excesses and lack of diversity
* The user should receive suggestions for foods that could help to fill nutritional gaps and achieve healthier eating habits
### Collect information for the poster
* Test the program with a volunteer and keep this test as a case study for using the program
* Extract the information, figures and charts necessary for the poster
* Writing the text of the poster
### Creation of the poster and presentation
* Assemble the elements for the poster and print it
* Prepare for the oral presentation
* Present the poster (21/22/23 Jan.)

## Questions for TAs
Nothing at this moment

## Files description
### computeNutriScore.py
This file contains the functions of the algorithm based on the indications of the French Ministry of Agriculture which allow us to calculate the nutriscore.
### Milestone_2.ipynb
The main notebook of our project. It contains the data presentation elements, cleaning, and all other processes included in milestone 2. 
### data Folder
This folder must contain the open food dataset, in csv format. It can also contain tab_for_filling.csv, which contains the medians of the elements by category and nutrient as well as data_food_final.csv ([downloadable here](https://drive.google.com/drive/folders/1G8-zV0-ctUQSk3X2qqIoh6SKuCFYmmAd?usp=sharing)), which contains the dataset completed by our preprocessing and which we used to present our data in the second part of the notebook. The calculation time for these last two files being long, it is indeed preferable to use the files already processed.
### Data_scrapping_USagriculture.ipynb
Secondary notebook, called by the main notebook and containing the algorithm to access the US Department of Agriculture database.


