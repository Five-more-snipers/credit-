
# Credit Card Fraud Detection with Classifier System.
This Python Program was created as a part of our Data-Mining Project of "Navigating the Labyrinth of Credit Card Fraud A Novel Perspective with Decision Tree Algorithms". This program simulates the system in which it detects whenever the transaction constitutes as fraudlent.

# General "How-it-Works"
The system first detects whenever both sender and receiver have engaged in fraudlent transactions before from the records. Then it records the thye of transaction, amount of transfer, and before/after the account balance of both sender/receiver. The system detects whenever the transaction constitutes as Fraudlent based on RandomForest & Adabooster classifier and flags both account as fraudlent for further references.

# Requirements
This Program works on Python 3.12.0 and several Libraries

-   Streamlit
-   Pandas
-   Scikit-learn

# How to Run
1. If you want to preprocess your own data, you can use 
.ipynb as algorithm test.

2. You can use the "kanfi.py" file to test the program.
-   You must run "streamlit run kanfi.py" to run the streamlit program. The application will be provided on web browser.