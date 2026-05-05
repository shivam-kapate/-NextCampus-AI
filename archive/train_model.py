import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
import joblib

def main():
    print("Loading dataset: kaggle_sw_raw.csv...")
    try:
        df = pd.read_csv('kaggle_sw_raw.csv')
    except FileNotFoundError:
        print("Error: 'kaggle_sw_raw.csv' not found. Please ensure it is in the same directory.")
        return

    # Drop missing values for the relevant columns
    columns_to_check = ['percentile', 'branch', 'gender', 'category', 'college_name']
    
    # Check if columns exist
    missing_cols = [col for col in columns_to_check if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing columns in dataset: {missing_cols}")
        return

    print("Dropping missing values...")
    df.dropna(subset=columns_to_check, inplace=True)

    print("Initializing and fitting LabelEncoders...")
    branch_encoder = LabelEncoder()
    gender_encoder = LabelEncoder()
    category_encoder = LabelEncoder()

    # Encode categorical features
    df['branch_encoded'] = branch_encoder.fit_transform(df['branch'])
    df['gender_encoded'] = gender_encoder.fit_transform(df['gender'])
    df['category_encoded'] = category_encoder.fit_transform(df['category'])

    # Define X (features) and Y (target)
    X = df[['percentile', 'branch_encoded', 'gender_encoded', 'category_encoded']]
    Y = df['college_name']

    # Train KNN Model
    print("Training the KNeighborsClassifier (n_neighbors=5)...")
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X, Y)

    # Save the trained model and encoders
    print("Saving the trained model and encoders to disk...")
    joblib.dump(knn_model, 'knn_model.joblib')
    joblib.dump(branch_encoder, 'branch_encoder.joblib')
    joblib.dump(gender_encoder, 'gender_encoder.joblib')
    joblib.dump(category_encoder, 'category_encoder.joblib')

    print("\nTraining complete! The following files have been saved:")
    print(" - knn_model.joblib")
    print(" - branch_encoder.joblib")
    print(" - gender_encoder.joblib")
    print(" - category_encoder.joblib")

if __name__ == '__main__':
    main()
