
# MALAYSIAN TAX INPUT PROGRAM
# File: main.py

from functions import (
    display_title,
    register_user,
    login_user,
    calculate_tax,
    save_tax_record,
    retrieve_tax_records
)


# DISPLAY TAX CALCULATION RESULTS

def display_tax_result(result):

    print("\n========== TAX CALCULATION RESULT ==========")

    print("Year of Assessment:",
          result["YA"])

    print("Annual Income: RM",
          format(result["Annual_Income"], ",.2f"))

    print("Total Tax Relief: RM",
          format(result["Total_Tax_Relief"], ",.2f"))

    print("Chargeable Income: RM",
          format(result["Chargeable_Income"], ",.2f"))

    print("Tax Before Rebate: RM",
          format(result["Tax_Before_Rebate"], ",.2f"))

    print("Tax Rebate: RM",
          format(result["Tax_Rebate"], ",.2f"))

    print("Final Tax Payable: RM",
          format(result["Final_Tax_Payable"], ",.2f"))

    print("============================================")


# USER REGISTRATION MENU

def registration_menu():

    print("\n========== USER REGISTRATION ==========")

    user_id = input("Enter User ID: ")

    ic_number = input("Enter 12-digit IC Number: ")

    success, message = register_user(user_id, ic_number)

    print("\n" + message)


# USER LOGIN MENU

def login_menu():

    print("\n========== USER LOGIN ==========")

    user_id = input("Enter User ID: ")

    password = input("Enter Password (Last 4 digits of IC): ")

    success, message = login_user(user_id, password)

    print("\n" + message)

    if success:
        user_menu(user_id)


# INCOME TAX CALCULATION MENU

def tax_calculation_menu(user_id):

    print("\n========== INCOME TAX CALCULATION ==========")

    try:

        annual_income = float(
            input("Enter Annual Income (RM): ")
        )

        total_tax_relief = float(
            input("Enter Total Tax Relief (RM): ")
        )

        # Validate income and tax relief
        if annual_income < 0 or total_tax_relief < 0:
            print("\nIncome and Tax Relief cannot be negative.")
            return

        # Calculate tax
        result = calculate_tax(
            annual_income,
            total_tax_relief
        )

        # Display tax result
        display_tax_result(result)

        # Ask whether user wants to save the record
        choice = input(
            "\nDo you want to save this tax record? (Y/N): "
        ).strip().upper()

        if choice == "Y":

            success, message = save_tax_record(
                user_id,
                result
            )

            print("\n" + message)

        elif choice == "N":

            print("\nTax record was not saved.")

        else:

            print("\nInvalid choice. Tax record was not saved.")

    except ValueError:

        print("\nInvalid input. Please enter numeric values.")


# RETRIEVE TAX RECORDS MENU

def tax_records_menu(user_id):

    print("\n========== TAX RECORD HISTORY ==========")

    records = retrieve_tax_records(user_id)

    if records is not None:

        print("\nUser ID:", user_id)

        print("\nYour Tax Records:\n")

        print(records.to_string(index=False))

    else:

        print("\nNo tax records found for this user.")


# USER MENU

def user_menu(user_id):

    while True:

        print("\n========== USER MENU ==========")

        print("Welcome,", user_id)

        print("1. Calculate Income Tax")
        print("2. View Tax Records")
        print("3. Logout")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":

            tax_calculation_menu(user_id)

        elif choice == "2":

            tax_records_menu(user_id)

        elif choice == "3":

            print("\nLogout successful!")
            break

        else:

            print("\nInvalid choice. Please try again.")


# MAIN MENU

def main():

    display_title()

    while True:

        print("\n========== MAIN MENU ==========")

        print("1. User Registration")
        print("2. User Login")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":

            registration_menu()

        elif choice == "2":

            login_menu()

        elif choice == "3":

            print("\nThank you for using Malaysian Tax Input Program!")
            print("Program terminated.")
            break

        else:

            print("\nInvalid choice. Please enter 1, 2 or 3.")


# RUN PROGRAM

if __name__ == "__main__":

    main()
