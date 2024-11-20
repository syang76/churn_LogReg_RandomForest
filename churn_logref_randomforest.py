# compare Random Forest and Logistic Regression

# Import libraries and methods/functions
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# loading the data
df_dem = pd.read_csv('telecom_demographics.csv')
df_use = pd.read_csv('telecom_usage.csv')
#df_dem.head()
#df_use.head()

# join the two df
churn_df = df_dem.merge(df_use, on='customer_id')
#churn_df.head(20)

# calculate churn rate
churn_rate = churn_df['churn'].value_counts() / len(churn_df)
print(churn_rate)

# one-hot encoding for categorical variables: telecom_partner, gender, state, city, 
churn_df = pd.get_dummies(churn_df, columns=['telecom_partner', 'gender', 'state', 'city','registration_event'])

# feature scaler
scaler = StandardScaler()

# drop customer_id and churn columns
features = churn_df.drop(['customer_id', 'churn'], axis=1)
features_scaled = scaler.fit_transform(features)

# target
target = churn_df['churn']

# split data
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, random_state=42)

# Logistic regression
logreg = LogisticRegression(random_state=42)
logreg.fit(X_train, y_train)
logreg_pred = logreg.predict(X_test)

# Logistic regression evaluation
cm_logreg = confusion_matrix(y_test, logreg_pred)
print(cm_logreg)
print(classification_report(y_test, logreg_pred))
accuracy_logreg = classification_report(y_test, logreg_pred, output_dict=True)['accuracy']

# Random Forest model
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

# Random Forest evaluation
cm_rf = confusion_matrix(y_test, rf_pred)
accuracy_rf = classification_report(y_test, rf_pred, output_dict=True)['accuracy']
print(cm_rf)
print(classification_report(y_test, rf_pred))

higher_accuracy = "RandomForest" if accuracy_rf > accuracy_logreg else "Logistic Regression"
print(higher_accuracy)