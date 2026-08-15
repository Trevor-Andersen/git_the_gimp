import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# --- STEP 1: Load/Replicate the German Credit Dataset (OpenML ID 31) ---
# Since live fetching requires an active internet connection, we create 
# a DataFrame replicating its specific feature constraints for this notebook.
#np.random.seed(42)
#n_samples = 1000

import arff
import pandas as pd

# 1. Open and parse the ARFF file
with open("C:\\Users\\ander\\AppData\\Local\\Programs\\Microsoft VS Code\\dataset_31_credit-g .arff", "r") as f:
    dataset = arff.load(f)

# 2. Extract column names and row data
column_names = [attr[0] for attr in dataset["attributes"]]
df = pd.DataFrame(dataset["data"], columns=column_names)

print(df.head(1000))
n_samples = 1000

# Select 4 Numeric Features and 3 Nominal (Categorical) Features
data = {
    # Numeric features
    'duration': np.random.randint(4, 72, size=n_samples),
    'credit_amount': np.random.randint(250, 18000, size=n_samples),
    'installment_commitment': np.random.randint(1, 5, size=n_samples),
    'residence_since': np.random.randint(1, 5, size=n_samples),
    # Nominal features
    'checking_status': np.random.choice(['<0', '0<=X<200', '>=200', 'no checking'], size=n_samples),
    'credit_history': np.random.choice(['critical', 'delayed', 'existing', 'all paid', 'no credits'], size=n_samples),
    'purpose': np.random.choice(['new car', 'used car', 'furniture', 'radio/tv', 'appliances', 'repairs', 'education', 'business'], size=n_samples),
    # Target variable (class: 1 = Good, 2 = Bad)
    'class': np.random.choice([1, 2], size=n_samples, p=[0.7, 0.3])
}

df = pd.DataFrame(data)

# --- STEP 2: Check for Missing Values ---
missing_count = df.isnull().sum().sum()
print(f"Number of missing values in the dataset: {missing_count}")
if missing_count > 0:
    df = df.dropna()
    print("Missing values dropped.")

# Separate Features (X) and Target (y)
X = df.drop(columns=['class'])
y = df['class']

# --- STEP 3: Preprocessing Setup ---
numeric_features = ['duration', 'credit_amount', 'installment_commitment', 'residence_since']
nominal_features = ['checking_status', 'credit_history', 'purpose']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), nominal_features)
    ]
)

# --- STEP 4: Split Data (80% Train, 10% Validation, 10% Test) ---
# First split: 80% train, 20% temporary (which will become validation + test)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, train_size=0.8, random_state=42, stratify=y)

# Second split: Split the 20% temporary set equally into validation (10%) and test (10%)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

# Fit and transform the data partitions
X_train_proc = preprocessor.fit_transform(X_train)
X_val_proc = preprocessor.transform(X_val)
X_test_proc = preprocessor.transform(X_test)

# --- STEP 5: Hyperparameter Tuning for KNN on Validation Set ---
best_k = 1
best_val_accuracy = 0

print("\nTuning KNN hyperparameter 'k' on the Validation Set:")
for k in range(1, 21, 2):  # Trying odd values of k to avoid ties
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_proc, y_train)
    val_preds = knn.predict(X_val_proc)
    val_acc = accuracy_score(y_val, val_preds)
    print(f"k = {k} -> Validation Accuracy: {val_acc:.4f}")
    
    if val_acc > best_val_accuracy:
        best_val_accuracy = val_acc
        best_k = k

print(f"\nBest k selected: {best_k} (Validation Accuracy: {best_val_accuracy:.4f})")

# --- STEP 6: Final Evaluation on Test Set ---
final_knn = KNeighborsClassifier(n_neighbors=best_k)
final_knn.fit(X_train_proc, y_train)
test_preds = final_knn.predict(X_test_proc)

test_accuracy = accuracy_score(y_test, test_preds)
conf_matrix = confusion_matrix(y_test, test_preds)

print("\n================ FINAL RESULTS ================")
print(f"Final Test Accuracy Score: {test_accuracy:.4f}")
print("Confusion Matrix:")
print(conf_matrix)
print("===============================================")
