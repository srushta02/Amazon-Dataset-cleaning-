import pandas as pd

# ==========================
# 1. Load dataset
# ==========================
INPUT_FILE = r"C:\Users\srush\Downloads\archive (2)\amazon.csv"
OUTPUT_FILE = r"C:\Users\srush\Downloads\archive (2)\amazon_cleaned.csv"

df = pd.read_csv(INPUT_FILE)
print("Initial shape:", df.shape)

# ==========================
# 2. Check missing values
# ==========================
missing_before = df.isnull().sum()

# Fill numeric columns with median
for col in df.select_dtypes(include=["float64", "int64"]).columns:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)

# Fill text columns with "Unknown"
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].fillna("Unknown")


# ==========================
# 3. Remove duplicates
# ==========================
duplicates_before = df.duplicated().sum()
df.drop_duplicates(inplace=True)
duplicates_after = df.duplicated().sum()

# ==========================
# 4. Standardize text
# ==========================
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip().str.lower()

# Example: standardize gender (if exists)
if "gender" in df.columns:
    df["gender"] = df["gender"].replace({
        "m": "male", "f": "female", "malee": "male", "fem": "female"
    })

# ==========================
# 5. Convert dates
# ==========================
for col in df.columns:
    if "date" in col or "time" in col:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        except:
            pass

# ==========================
# 6. Rename columns
# ==========================
df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

# ==========================
# 7. Fix numeric data types
# ==========================
for col in df.select_dtypes(include="object").columns:
    # Try converting numbers stored as text
    try:
        df[col] = pd.to_numeric(df[col])
    except:
        pass

# ==========================
# 8. Save cleaned dataset
# ==========================
df.to_csv(OUTPUT_FILE, index=False)
print("Cleaned dataset saved at:", OUTPUT_FILE)

# ==========================
# 9. Summary of changes
# ==========================
print("\n===== SUMMARY OF CHANGES =====")
print("Initial shape:", missing_before.shape)
print("Final shape:", df.shape)
print("Missing values before:\n", missing_before)
print("\nDuplicates removed:", duplicates_before - duplicates_after)
print("\nFinal missing values:\n", df.isnull().sum())
print("===============================")
