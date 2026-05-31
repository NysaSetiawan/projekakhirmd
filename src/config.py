import numpy as np

not_numeric_columns = [
    "Age", "Annual_Income", "Num_of_Loan", "Num_of_Delayed_Payment", 
    "Changed_Credit_Limit", "Outstanding_Debt", "Amount_invested_monthly", "Monthly_Balance"
]

missing_cat_cols = ["Credit_History_Age", "Payment_Behaviour", "Occupation"]

common_loans = ['Home Loan', 'Personal Loan', 'Credit Builder Loan', 'Auto Loan', 'Student Loan']

age_bins = [0, 25, 40, 60, np.inf]
age_labels = ['Muda (<25)', 'Dewasa Muda (25-40)', 'Paruh Baya (41-60)', 'Senior (>60)']

credit_mix_map = {'Bad': 0, 'Standard': 1, 'Good': 2}
payment_min_map = {'No': 0, 'NM': 0, 'Yes': 2}
target_mapping = {'Poor': 0, 'Standard': 1, 'Good': 2}
target_names = ['Poor', 'Standard', 'Good']

payment_order = [
    'Unknown',
    'Low_spent_Small_value_payments', 'Low_spent_Medium_value_payments', 'Low_spent_Large_value_payments',
    'High_spent_Small_value_payments', 'High_spent_Medium_value_payments', 'High_spent_Large_value_payments'
]

num_cols = [
    'Monthly_Inhand_Salary', 'Delay_from_due_date', 'Changed_Credit_Limit',
    'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age', 'Monthly_Balance',
    'Amount_invested_monthly', 'Num_Bank_Accounts', 'Interest_Rate',
    'Annual_Income', 'Num_of_Delayed_Payment', 'Age',
    'Total_EMI_per_month', 'Num_Credit_Card', 'Num_Credit_Inquiries', 'Num_of_Loan',
    'Type_of_Loan', 'DTI', 'EMI_to_Income_Ratio', 'Savings_Rate', 
    'Total_Active_Credits', 'Delay_Ratio', 'Inquiry_Intensity',
    'Credit_Mix_Encoded', 'Payment_Min_Encoded',
    'Has_Home_Loan', 'Has_Personal_Loan', 'Has_Credit_Builder_Loan', 'Has_Auto_Loan', 'Has_Student_Loan',
]

ordinal_cols = ['Payment_Behaviour']
cat_cols = ['Month', 'Occupation', 'Payment_of_Min_Amount', 'Credit_Mix', 'Age_Group']