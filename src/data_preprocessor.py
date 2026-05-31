import pandas as pd
import numpy as np
import re
import config

class DataPreprocessor:
    def __init__(self):
        pass

    @staticmethod
    def _convert_credit_history_age(x):
        if pd.isna(x):
            return np.nan
        x = str(x)
        years = 0
        months = 0
        if "Years" in x:
            years = int(x.split("Years")[0].strip())
        if "Months" in x:
            months = int(x.split("Months")[0].split()[-1].strip())
        return years * 12 + months

    @staticmethod
    def _count_loans(type_str):
        if pd.isna(type_str) or str(type_str).strip() == "":
            return 0
        s = str(type_str).strip()
        s = re.sub(r"\s+and\s+", ",", s)
        items = [x.strip() for x in s.split(",") if x.strip() != ""]
        return len(items)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        drop_cols = ["Unnamed: 0", "ID", "Customer_ID", "Name", "SSN"]
        df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')
        
        for col in config.not_numeric_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace("_", "", regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        if "Monthly_Balance" in df.columns:
            
            df["Monthly_Balance"] = df["Monthly_Balance"].fillna(df["Monthly_Balance"].median())
        
        if "Occupation" in df.columns:
            df["Occupation"] = df["Occupation"].replace("_______", "Unknown")
        if "Credit_Mix" in df.columns:
            df["Credit_Mix"] = df["Credit_Mix"].replace("_", "Unknown")
        if "Payment_of_Min_Amount" in df.columns:
            df["Payment_of_Min_Amount"] = df["Payment_of_Min_Amount"].replace("NM", "No")
        if "Payment_Behaviour" in df.columns:
            df["Payment_Behaviour"] = df["Payment_Behaviour"].replace("!@9#%8", "Unknown")
            
        neg_cols = ["Age", "Num_Bank_Accounts", "Num_of_Loan", "Delay_from_due_date", 
                    "Num_of_Delayed_Payment", "Changed_Credit_Limit", "Monthly_Balance"]
        for col in neg_cols:
            if col in df.columns:
                df.loc[df[col] < 0, col] = np.nan
                
        if "Credit_Mix" in df.columns:
            df["Credit_Mix"] = df["Credit_Mix"].fillna("Unknown")
        if "Occupation" in df.columns:
            df["Occupation"] = df["Occupation"].fillna("Unknown")
        if "Payment_Behaviour" in df.columns:
            df["Payment_Behaviour"] = df["Payment_Behaviour"].fillna("Unknown")
            
        return df

    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        epsilon = 1e-5
        if 'Payment_Behaviour' in df.columns:
            # Membuat mapping dinamis dari list payment_order
            mapping = {val: i for i, val in enumerate(config.payment_order)}
            # Map ke nilai numerik, isi yang tidak ditemukan dengan 0 (Unknown)
            df['Payment_Behaviour'] = df['Payment_Behaviour'].map(mapping).fillna(0).astype(int)
        
        if "Credit_History_Age" in df.columns:
            df["Credit_History_Age"] = df["Credit_History_Age"].apply(self._convert_credit_history_age)
            
            
        if "Type_of_Loan" in df.columns:
            type_of_loan_temp = df['Type_of_Loan'].fillna('No Loan')
            for loan in config.common_loans:
                col_name = f"Has_{loan.replace(' ', '_')}"
                df[col_name] = type_of_loan_temp.apply(lambda x: 1 if loan.lower() in str(x).lower() else 0)
            df["Type_of_Loan"] = df["Type_of_Loan"].apply(self._count_loans)
            
        df['DTI'] = df['Outstanding_Debt'] / (df['Annual_Income'] + epsilon)
        df['EMI_to_Income_Ratio'] = df['Total_EMI_per_month'] / (df['Monthly_Inhand_Salary'] + epsilon)
        df['Savings_Rate'] = df['Monthly_Balance'] / (df['Monthly_Inhand_Salary'] + epsilon)
        
        df['Total_Active_Credits'] = df['Num_Bank_Accounts'] + df['Num_Credit_Card'] + df['Num_of_Loan']
        df['Delay_Ratio'] = df['Num_of_Delayed_Payment'] / (df['Num_Bank_Accounts'] + df['Num_Credit_Card'] + epsilon)
        df['Inquiry_Intensity'] = df['Num_Credit_Inquiries'] / (df['Num_Credit_Card'] + 1)
        
        df['Age_Group'] = pd.cut(df['Age'], bins=config.age_bins, labels=config.age_labels)
        df['Age_Group'] = df['Age_Group'].astype(str).replace('nan', 'Unknown')
        
        df['Credit_Mix_Encoded'] = df['Credit_Mix'].map(config.credit_mix_map).fillna(-1)
        df['Payment_Min_Encoded'] = df['Payment_of_Min_Amount'].map(config.payment_min_map).fillna(-1)
        
        return df