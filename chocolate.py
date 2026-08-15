import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset 
df = pd.read_csv('flavors_of_cacao.csv')

# Clean up columns
df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()

# Map the column headers for clarity
# Expected columns: 'Company (Maker_if_known)', 'Review Date', 'Rating', 'Cocoa Percent', 'Broad Bean Origin'
company_col = [c for c in df.columns if 'Company' in c][0]
review_date_col = [c for c in df.columns if 'Review' in c][0]
rating_col = [c for c in df.columns if 'Rating' in c][0]
cocoa_col = [c for c in df.columns if 'Cocoa' in c][0]
missing_target_col = [c for c in df.columns if 'Broad Bean' in c][0]  # Example column for missing values

# Preprocess Cocoa Percent string (e.g., '70%' -> 70.0)
df['Cocoa Numeric'] = df[cocoa_col].astype(str).str.rstrip('%').astype(float)

# --- REQUIRED METRICS ---

# 1. Count of the tuples
tuple_count = len(df)

# 2. Count of unique company names
unique_companies = df[company_col].nunique()

# 3. Count of reviews in 2013
reviews_2013 = len(df[df[review_date_col] == 2013])

# 4. Count of missing values in a specific given column (using 'Broad Bean Origin' as the example target)
# In this dataset, missing values are often represented as an empty space string ' ' or actual NaNs
missing_values = df[missing_target_col].isna().sum() + (df[missing_target_col].astype(str).str.strip() == '').sum()

# 5. Min-Max Normalization of the Ratings column values
min_rating = df[rating_col].min()
max_rating = df[rating_col].max()
df['Normalized_Ratings'] = (df[rating_col] - min_rating) / (max_rating - min_rating)

# Print Summary Results
print(f"Total Tuples: {tuple_count}")
print(f"Unique Company Names: {unique_companies}")
print(f"Reviews in 2013: {reviews_2013}")
print(f"Missing Values in '{missing_target_col}': {missing_values}")
print("\nFirst 5 Normalized Ratings:")
print(df[['Normalized_Ratings']].head())


# --- VISUALIZATIONS ---

plt.figure(figsize=(12, 5))

# Plot 1: Histogram of Ratings
plt.subplot(1, 2, 1)
sns.histplot(df[rating_col], bins=15, kde=True, color='skyblue')
plt.title('Histogram of Chocolate Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')

# Plot 2: Scatter Plot of Cocoa Percent against Rating values
plt.subplot(1, 2, 2)
sns.scatterplot(data=df, x='Cocoa Numeric', y=rating_col, alpha=0.6, color='chocolate')
plt.title('Cocoa Percent vs. Rating')
plt.xlabel('Cocoa Percent (%)')
plt.ylabel('Rating')

plt.tight_layout()
plt.show()