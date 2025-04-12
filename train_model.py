import pandas as pd
import joblib
from copy import deepcopy
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_excel("car_parking_dataset.xlsx")
data = deepcopy(df)

# Drop unnecessary columns
data = data.drop(['Entry_ID', 'Vehicle_Number', 'Entry_Time', 'Exit_Time'], axis=1)

# Define 'Space_Available' based on duration (assuming > 30 minutes means not available)
data['Space_Available'] = data['Duration_Minutes'].apply(lambda x: 0 if x > 30 else 1)

categorical_cols = ['Vehicle_Type', 'Parking_Slot', 'Parking_Level', 'Payment_Status']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    encoders[col] = le

X = data.drop(['Amount_Charged', 'Space_Available'], axis=1)
y_price = data['Amount_Charged']
y_availability = data['Space_Available']

X_train, X_test, y_price_train, y_price_test, y_avail_train, y_avail_test = train_test_split(
    X, y_price, y_availability, test_size=0.2, random_state=42
)

# Train price model (regression)
price_model = RandomForestRegressor()
price_model.fit(X_train, y_price_train)

# Train availability model (binary classification)
availability_model = RandomForestRegressor()  # Or RandomForestClassifier()
availability_model.fit(X_train, y_avail_train)

# Save models
joblib.dump(price_model, 'parking_price_model.pkl')
joblib.dump(availability_model, 'parking_avail_model.pkl')
joblib.dump(encoders, 'encoders.pkl')

print("Models and encoders saved successfully!")
