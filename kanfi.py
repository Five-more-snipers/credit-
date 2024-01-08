import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv('./archive/balanced_dataset.csv')
data = data.drop(['nameOrig', 'nameDest'], axis=1)

# Preprocess data
X = data.drop('isFraud', axis=1)
y = data['isFraud']

dict1 = {'CASH_OUT': 0, 'TRANSFER': 1, 'PAYMENT': 2, 'CASH_IN': 3, 'DEBIT': 4}
data['type'] = data['type'].map(dict1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

X_train['type'] = X_train['type'].map(dict1)
X_test['type'] = X_test['type'].map(dict1)

sc = StandardScaler()
X_train_sc = sc.fit_transform(X_train)
X_test_sc = sc.transform(X_test)

# Train the model
model5 = RandomForestClassifier()
model5.fit(X_train_sc, y_train)

model6 = AdaBoostClassifier()
model6.fit(X_train_sc,y_train)

# Decision Tree Training
# Streamlit App
st.title("Fraud Detection App")

selected_model = st.radio("Pilih Model:", ["Random Forest", "AdaBoost"])

# Input Form
nameOrig = st.text_input("Enter ID for Original Destination/Sender:")
nameDest = st.text_input("Enter ID for Target Destination/Receiver:")

step = st.text_input("Hours since Last Update")
type = st.text_input("Type? (CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT):")
amount = st.text_input("Amount:")
oldbalanceOrg = st.text_input("Old Balance Origin:")
newbalanceOrig = st.text_input("New Balance Origin:")
oldbalanceDest = st.text_input("Old Balance Destination:")
newbalanceDest = st.text_input("New Balance Destination:")
isFlaggedFraud = st.text_input("You think this is fraud? (0: No/1: Yes):")

#Isola
# nameOrig = 'C1305486145'
# nameDest = 'C553264065'

# step = 1
# type = 'TRANSFER'
# amount = 181
# oldbalanceOrg = 181
# newbalanceOrig = 0
# oldbalanceDest = 0
# newbalanceDest = 0
# isFlaggedFraud = 1

# Confirmation button
if st.button("Confirm this!"):
    # Validate input
    if any(value == '' for value in [step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFlaggedFraud, nameOrig, nameDest]):
        st.warning("Please fill in all input fields.")
    else:
        detected_fraud_file = './archive/fraud2.csv'

        # Check if the CSV file exists, and if not, create it with columns
        try:
            detected_fraud = pd.read_csv(detected_fraud_file)
        except FileNotFoundError:
            detected_fraud = pd.DataFrame(columns=['nameOrig', 'nameDest'])
            detected_fraud.to_csv(detected_fraud_file, index=False)

        if ((detected_fraud['nameOrig'] == nameOrig) & (detected_fraud['nameDest'] == nameDest)).any():
            st.warning("IDs were previously flagged as fraud. Skipping analysis.")
        else:
            # Convert input to a DataFrame for model prediction
            input_data = pd.DataFrame({
                'step': [step],
                'type': [type],
                'amount': [amount],
                'oldbalanceOrg': [oldbalanceOrg],
                'newbalanceOrig': [newbalanceOrig],
                'oldbalanceDest': [oldbalanceDest],
                'newbalanceDest': [newbalanceDest],
                'isFlaggedFraud': [isFlaggedFraud]
            })

            # Apply type mapping
            input_data['type'] = input_data['type'].map(dict1)

            # Standardize input features
            input_data_sc = sc.transform(input_data)

            # # Make prediction
            # prediction = model5.predict(input_data_sc)
            if selected_model == "Random Forest":
                prediction = model5.predict(input_data_sc)
            elif selected_model == "AdaBoost":
                prediction = model6.predict(input_data_sc)

            # Display prediction
            # st.write(f"Prediction: {prediction}")
            if prediction[0] == 0:
                st.success("This Transaction is not considered as Fraud.")

            # type(detected_fraud)
            if prediction[0] == 1:
                detected_fraud_entry = pd.DataFrame({'nameOrig': [nameOrig], 'nameDest': [nameDest]})
                # detected_fraud = detected_fraud.append(detected_fraud_entry, ignore_index=True)
                detected_fraud = pd.concat([detected_fraud, detected_fraud_entry], ignore_index=True)
                detected_fraud.to_csv('./archive/fraud2.csv', index=False)
                st.success("Fraud detected! IDs stored in the detected fraud file.")

