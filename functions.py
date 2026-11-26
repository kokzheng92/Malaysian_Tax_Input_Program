
# Malaysian Tax Input Program
# File: functions.py


from pathlib import Path
import pandas as pd


# CSV FILE LOCATION

USERS_FILE = Path(__file__).resolve().parent / "users.csv"
TAX_RECORDS_FILE = Path(__file__).resolve().parent / "tax_records.csv"

# DISPLAY PROGRAM TITLE

def display_title():


    print("===================================")
    print("     MALAYSIAN TAX INPUT PROGRAM")
    print("===================================")

# LOAD REGISTERED USERS

def load_users():

    if not USERS_FILE.exists():
        return []

    try:
        df = pd.read_csv(
            USERS_FILE,
            dtype="str",
            keep_default_na=False
        )

        return df.to_dict(orient="records")

    except pd.errors.EmptyDataError:
        return []

# SAVE REGISTERED USERS

def save_users(users):


    df = pd.DataFrame(
        users,
        columns=["User_ID", "IC_Number"]
    )

    df.to_csv(str(USERS_FILE), index=False)


# USER REGISTRATION

def register_user(user_id, ic_number):


    # Remove unnecessary spaces
    user_id = user_id.strip()
    ic_number = ic_number.strip()

    # Validate User ID
    if user_id == "":
        return False, "User ID cannot be empty."

    # Validate IC Number
    if len(ic_number) != 12 or not ic_number.isdigit():
        return False, "IC Number must contain exactly 12 digits."

    # Load existing users
    users = load_users()

    # Check duplicate User ID
    for user in users:
        if user["User_ID"] == user_id:
            return False, "User ID already exists."

    new_user = {
        "User_ID": user_id,
        "IC_Number": ic_number
    }

    users.append(new_user)

    # Save updated user information
    try:
        save_users(users)

        return True, "Registration successful!"

    except OSError:
        return False, "Unable to save user information."


# USER LOGIN

def login_user(user_id, password):

    # Remove unnecessary spaces
    user_id = user_id.strip()
    password = password.strip()

    # Validate input
    if user_id == "" or password == "":
        return False, "User ID and Password cannot be empty."

    if len(password) != 4 or not password.isdigit():
        return False, "Password must contain exactly 4 digits."

    # Load registered users
    users = load_users()

    # Check whether the User ID exists
    for user in users:

        if user["User_ID"] == user_id:

            # Get the last 4 digits of IC Number
            correct_password = user["IC_Number"][-4:]

            # Compare passwords
            if password == correct_password:
                return True, "Login successful!"

            else:
                return False, "Incorrect password."

    # User ID does not exist
    return False, "User ID not found."

# INCOME TAX CALCULATION

def calculate_tax(annual_income, total_tax_relief):

    # Step 1: Calculate Chargeable Income
    chargeable_income = max(0, annual_income - total_tax_relief)

    # Step 2: Define YA 2026 progressive tax brackets
    tax_brackets = [
        (0, 5000, 0.00),
        (5000, 20000, 0.01),
        (20000, 35000, 0.03),
        (35000, 50000, 0.06),
        (50000, 70000, 0.11),
        (70000, 100000, 0.19),
        (100000, 400000, 0.25),
        (400000, 600000, 0.26),
        (600000, 2000000, 0.28),
        (2000000, float("inf"), 0.30)
    ]

    # Step 3: Calculate Tax Before Rebate
    tax_before_rebate = 0

    for lower_limit, upper_limit, rate in tax_brackets:

        if chargeable_income > lower_limit:

            taxable_amount = min(
                chargeable_income, upper_limit
            ) - lower_limit

            tax_before_rebate += taxable_amount * rate

    # Step 4: Calculate Individual Tax Rebate
    if chargeable_income <= 35000:
        tax_rebate = min(400, tax_before_rebate)
    else:
        tax_rebate = 0

    # Step 5: Calculate Final Tax Payable
    final_tax_payable = tax_before_rebate - tax_rebate

    # Return all calculation results
    return {
        "YA": 2026,
        "Annual_Income": round(annual_income, 2),
        "Total_Tax_Relief": round(total_tax_relief, 2),
        "Chargeable_Income": round(chargeable_income, 2),
        "Tax_Before_Rebate": round(tax_before_rebate, 2),
        "Tax_Rebate": round(tax_rebate, 2),
        "Final_Tax_Payable": round(final_tax_payable, 2)
    }

# SAVE TAX RECORDS

def save_tax_record(user_id, tax_result, test_case_id=""):

    # Define CSV column names
    columns = [
        "User_ID",
        "Test_Case_ID",
        "YA",
        "Annual_Income",
        "Total_Tax_Relief",
        "Chargeable_Income",
        "Tax_Before_Rebate",
        "Tax_Rebate",
        "Final_Tax_Payable"
    ]

    # Create a dictionary for the tax record
    new_record = {
        "User_ID": user_id,
        "Test_Case_ID": test_case_id,
        "YA": tax_result["YA"],
        "Annual_Income": tax_result["Annual_Income"],
        "Total_Tax_Relief": tax_result["Total_Tax_Relief"],
        "Chargeable_Income": tax_result["Chargeable_Income"],
        "Tax_Before_Rebate": tax_result["Tax_Before_Rebate"],
        "Tax_Rebate": tax_result["Tax_Rebate"],
        "Final_Tax_Payable": tax_result["Final_Tax_Payable"]
    }

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame([new_record], columns=columns)

    try:
        # Check whether the CSV file already contains data
        file_exists = (
            TAX_RECORDS_FILE.exists()
            and TAX_RECORDS_FILE.stat().st_size > 0
        )

        # Append the new record into CSV
        df.to_csv(
            str(TAX_RECORDS_FILE),
            mode="a",
            header=not file_exists,
            index=False
        )

        return True, "Tax record saved successfully!"

    except OSError:
        return False, "Unable to save tax record."


# RETRIEVE TAX RECORDS

def retrieve_tax_records(user_id):

    # Check whether the CSV file exists
    if not TAX_RECORDS_FILE.exists():
        return None

    try:
        # Read tax records from CSV
        df = pd.read_csv(
            str(TAX_RECORDS_FILE),
            dtype=str,
            keep_default_na=False
        )

        # Check whether the CSV file contains records
        if df.empty:
            return None

        # Filter records using User ID
        user_records = df[df["User_ID"] == user_id]

        # Check whether the user has any tax records
        if user_records.empty:
            return None

        return user_records

    except (OSError, pd.errors.EmptyDataError):
        return None
