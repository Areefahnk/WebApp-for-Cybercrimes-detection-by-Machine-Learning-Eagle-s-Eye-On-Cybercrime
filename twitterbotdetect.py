import pandas as pd
import numpy as np
file= 'twitterbotdataset.csv'
import warnings
warnings.filterwarnings("ignore")
import pickle

training_data = pd.read_csv(file)
bots = training_data[training_data.bot==1]
nonbots = training_data[training_data.bot==0]
##identifying imbalances in data
bots['friends_by_followers'] = bots.friends_count/bots.followers_count
bots[bots.friends_by_followers<1].shape

nonbots['friends_by_followers'] = nonbots.friends_count/nonbots.followers_count
nonbots[nonbots.friends_by_followers<1].shape

##conditions applicable in detecting bots / nonbots
#bots[bots.listedcount>10000]
condition = (bots.screen_name.str.contains("bot", case=0)==1)|(bots.description.str.contains("bot", case=0)==1)|(bots.location.isnull())|(bots.verified==0)

bots['screen_name_binary'] = (bots.screen_name.str.contains("bot", case=0)==1)
bots['location_binary'] = (bots.location.isnull())
bots['verified_binary'] = (bots.verified==0)
#print(bots.shape)

condition = (nonbots.screen_name.str.contains("bot", case=0)==0)| (nonbots.description.str.contains("bot", case=0)==0) |(nonbots.location.isnull()==0)|(nonbots.verified==1)

nonbots['screen_name_binary'] = (nonbots.screen_name.str.contains("bot", case=False)==0)
nonbots['location_binary'] = (nonbots.location.isnull()==0)
nonbots['verified_binary'] = (nonbots.verified==1)

#print(nonbots.shape)
df = pd.concat([bots, nonbots])
#print(df.shape)

##feature independence using using spearman corelation
df.corr(method='spearman')

###PERFORMING FEATURE ENGINEERING
file = open('twitterbotdataset.csv', mode='r', encoding='utf-8', errors='ignore')
training_data = pd.read_csv(file)

bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|yes_ofc|forget' \
                   r'expos|kill|clit|bbb|butt|fuck|XXX|sex|truthe|fake|anony|free|virus|funky|RNA|kuck|jargon' \
                   r'nerd|swag|jack|bang|bonsai|chick|prison|paper|pokem|xx|freak|ffd|dunia|clone|genie|bbb' \
                   r'ffd|onlyman|emoji|joke|troll|droop|free|every|wow|cheese|yeah|bio|magic|wizard|face'

training_data['screen_name_binary'] = training_data.screen_name.str.contains(bag_of_words_bot, case=0, na=0)
training_data['name_binary'] = training_data.name.str.contains(bag_of_words_bot, case=0, na=0)
training_data['description_binary'] = training_data.description.str.contains(bag_of_words_bot, case=0, na=0)
training_data['status_binary'] = training_data.status.str.contains(bag_of_words_bot, case=0, na=0)
#print("Done feature Engineering")

#def convert_to_int(word):
 #   word_dict ={'True':1, 'False':0}
  #  return word_dict[word]


##PERFORMING FEATURE EXTRACTION
training_data['listed_count_binary'] = (training_data.listed_count>20000)==0
features = ['screen_name_binary', 'name_binary', 'description_binary', 'status_binary', 'verified', 'followers_count', 'friends_count', 'statuses_count', 'listed_count_binary', 'bot']
#print("Feature Extraction Performed")

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.model_selection import train_test_split
X = training_data[features].iloc[:,:-1]
y = training_data[features].iloc[:,-1]
y=y.astype('int')
X = X.astype('int')
#print(X,y)
dt = DecisionTreeClassifier(criterion='entropy', min_samples_leaf=50, min_samples_split=10)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
#print("Splitting of dataset is done!!!")
dt = dt.fit(X_train, y_train)  ##giving training set as input

##we are going to import this into a pickle file.
##we don't want to run this entire python program again and again...whenever using the website.
##So we train our decisiontreeclassifier model once and importing that model somewhere else.from where u can directly fetch it
# and that's where pickle comes in.

inputt = [int(x) for x in "1 0 1 1 1 7892 340 450 1".split(' ')]
final = [np.array(inputt)]
b=dt.predict_proba(final)
#print(b)
saved_pickle_file = open('model.pkl', 'wb')
pickle.dump(dt,saved_pickle_file)
saved_pickle_file.close()
load_pickle_file = open('model.pkl', 'rb')
loaded_model = pickle.load(load_pickle_file)
#print("Done loading or reading data........")
    #y_pred_train = dt.predict(X_train)
    #y_pred_test = dt.predict(X_test)


#print("Let's display prediction:")
#print("Trainig Accuracy: %.5f" %accuracy_score(y_train, y_pred_train))
#print("Test Accuracy: %.5f" %accuracy_score(y_test, y_pred_test))

