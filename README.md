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
*
### Information design
* The interface must present the user with the quantities of nutrients he/she has consumed
* The user must receive an indicative assessment of the nutritional quality of his/her food (expanded Nutri-score)
* (if enough time) The program must indicate to the user the main problems of his diet. Insufficient nutrients must be indicated
* (if enough time) The user should receive suggestions for foods that could help to fill nutritional gaps
### Collect information for the poster
* Test the program with a volunteer and keep this test as a case study for using the program
* Extract the information and charts necessary for the poster
### Creation of the poster and presentation
* Create the poster and print it
* Prepare for the oral presentation
* Present the poster (21/22/23 Jan.)

## Questions for TAs
Nothing at this moment


