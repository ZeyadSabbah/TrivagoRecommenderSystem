# Trivago Recommender System
## Definition
Session-based recommender system that re-ranks given list of accommodations based on user's interactions in a session.

## Data Source
To understand more about the data, this link https://recsys.trivago.cloud/challenge/dataset/
To obtain the dataset, one should register first, then go to the Dataset tab on the webpage, and download the dataset from there.
Here is the link to download it https://recsys.trivago.cloud/challenge/dataset/?download=1

## Introduction
trivago is well-known in Europe as an e-commerce website that gives recommendations of accommodations to users. The recommendations are personalized based on the interaction of users with the different items they are looking for. The whole purpose of the project or the Challenge is to re-rank the items that had been provided to the users so that the item the user had chosen is at the top of the list.

Dataset used in this project is from RecSys 2019 Challenge. The size of the training set is about 2 Gb. There are 2 datasets, one of them is a session-item relationship which is very rich in information about how users are interacting with different accommodations (items), and the other is metadata information about the items which can be used to get more features about the items such as the rating of different items.

## Metric
The metric used to evaluate participants' models is Mean Reciprocal Rank.
Let's say that there is a list of 5 items, the user chose the first item, then the Reciprocal Rank would be 1 if the item chose the second, the score would then be 0.5, and so on. But, there isn't just one user, there are many users, so the Mean Reciprocal Rank would be the average score of all the scores.

## Data Exploratoration Research Questions
- What is the timeline of the training and test sets?
6 and 2 days for train and test sets, respectively.

- What is the distribution of the number of steps users take on Trivago?
It's a right-skewed data distribution, users click out in their early steps on the app or the website. That matches with the duration of the session as well.

- What is the most repeated action on Trivago?
Interaction with items' images is the first action, comes in second clicking out the item.

- Which platforms most of the users use?
The first is the Brazilian, the second is the United States, the third is the Japanese, fourth in the United Kingdom.

- Is there a difference in traffic on Trivago through the week?
Sessions seem to be increasing a bin from the drop that happened on Saturday. The data is not enough to be sure that this is the case every week since this is the only data for one week.

- What is the relationship between the number of steps and the duration of the session?
There is a weak positive relationship.

- What is the percentage of users selecting the item that comes first in the list?
Around 38% of the users select the first item in the list which assures that their recommendation engine is doing a great job addressing the right items to the users.

Note: Some of the data are not consistent. Some selected items do not lie in the impressions lists.

Key Insights
1. The more steps are taken the higher the rank (in terms of order only) of the selected items.
2. The device used in the session affects the Average Step, the larger the device is the higher the average step for the same rank of items.
3. The users are mainly from Brazil, the US, Japan, United Kingdom, German, India, Mexico, and Australia.

## Strategy
The idea I have been following to tackle this Ranking Problem is actually by converting the Ranking Problem into Binary Classification Problem, so instead of ranking the items, I would design the model to answer the question "Would the user select this item?" for every item in the list, I would not care that much about the answer of the model, but I would be really interested in the Probability of the user selecting this item, and based on the probabilities of selecting the items, items can then be sorted in descending order.

## ML Research Questions  
**1st Question**
If the user is provided with a list of 25 items, and the user selects only one item, and the re-ranking problem became a binary classification problem, would not that leave us with the imbalanced dataset to train models on?
The question is "Would different resampling techniques help the model becomes better giving better recommendations?"

**2nd Question**  
The Challenge is only concerned with one selection of a list even if the user had seen multiple lists, but what if the user is booking accommodations for a multi-city trip in the same session. That would leave us with more than one satisfying item. Actually, this will give an advantage of generating more data because older lists that were given to the users are discarded and only the latest list is taken into consideration.
The question is "Would deal with users who selected more than one item in different cities as multiple items satisfied user help in training models better?"

## Projects' Details

### Datasets Split
Since the Challenge is over, and there is no way to submit the test set provided by RecSys, the original test set is discarded, and the training set provided was actually split into training, validation, and test sets where the test set was only used in the final selection of which structure is best.

### Files

1. ProjectEDA  
This file gives an intuition about the nature of the datasets in general and splitting the datasets that will be later used.

2. TrainEDA  
This file is about the exploration of the training data after the split has occurred in ProjectEDA, it gets the general findings.

3. FeatureEngineering  
Features of this dataset mostly can't be processed and it requires feature engineering and data preparation.
Features generated were either Global or Local.
*Global Features* are the features where the aggregations were done across the whole training regardless of the values being in sessions.
*Local Features* are the features engineered on the sessions' scope

4. data_transformation  
Is the class where all the functions used to transform data are.

5. Modeling  
After features were engineered, it comes the part where the most important features are selected and trying different techniques to train the model best.

*Models*  
Models used in this approach were Logistic Regression, Random Forest, and XGBoost.

*Resampling Techniques*  
To answer the first question, different two resampling techniques were used; SMOTE and Under Sampling.
First, I trained the selected models without applying any resampling techniques.
Second, I used SMOTE, and I trained the same models with the same hyperparameters.
Third, I used Under Sampling, and I did the same once again.

*Generating More Data*  
To answer the second question, I had to look up the sessions that had more than one selected item in different cities.
The increase was almost 5% of the original data.

*Items Properties*  
Used complementary data provided, but because the dataset is relatively big, I could not engineer features out of it, it is really easy to do that as the data is pretty much straightforward, the main challenge was that the session in Google Colab was keeping on crashing because of RAM limitation.
That's when I decided to use the dimensionality reduction technique Principal Component Analysis to reduce the properties, and also K-means to have just 5 clusters of items alike.

6. Evaluation
After training many models, it's time to check which technique is best for the Challenge.  
Models were evaluated on the validation set that has never been seen by the models.  

*Resampling Techniques*  
 Although resampling techniques succeeded in giving better scores for the Recall metric, for example, it failed and actually gave worse results in the MRR metric. The best performing model was the Random Forest with a score of 0.61245.

 *More Data*  
 Evaluating the More Trained Model on the same validation set, gave a slightly better score. Although the difference is not that big, an increase in the data by 5% has increased the score by almost 0.2%, which in the real world is something valuable and a high increase in the profit margin. The score ended up being 0.61268.

 *Items' Properties*  
 The way I combined the properties actually made the score worse, for future completion of this project is to consider more resources and carefully generate features that really matter and make the model perform better.

 *Test Evaluation*  
 Since More Trained Model performed the best, the model was being evaluated on the test set that has never been used in any selection or has ever been seen by the model.
 The MRR score is 0.61719.

### Conclusion

Balancing datasets is not a mandatory step to proceed with any project, it may enhance one metric and worsen another, it really depends on what metrics are used to evaluate how good the model is.

Collecting more data is not necessary if one can interpret data differently, considering disregarded data can improve training models and can help businesses achieve higher levels of success.
