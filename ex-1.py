# Exercise 1: Age Calculator (20 points) 
# Create a program that: 
# 1. Asks the user to input their birth date in mm/dd/yyyy format 
# 2. Validates the input format and ensures it’s a valid date 
# 3. Calculates and displays their current age in years 
# 4. Converts and displays the birthdate in European format (dd/mm/yyyy) 
# 5. Handles all possible errors gracefully with appropriate messages 

#import datetime and date module
from datetime import datetime, date

#base class 
class AgeCalculator:
    
    #validate the date format and ensure it's a valid date
    def date_validate(self, date_str: str, date_format: str) -> date | str:
        '''validate the date against mm/dd/yyy format
            return date object if valid, 'format_error' if format is wrong, 'future_error' if date is in future'''
        
        try:
            datetime_obj = datetime.strptime(date_str, date_format)
            birth_date = datetime_obj.date()
            
            # Check if the date is in the future
            if birth_date > date.today():
                return "future_error"

            return birth_date
        
        except ValueError:
            return "format_error"
    
    #calculate age and return year
    def calculate_age(self, dob: date) -> int:
        '''calculate user age by calculating the difference between today's date and input date'''

        today = date.today()
        age = today.year - dob.year

        # Adjust age if the birth month and day haven't occurred yet this year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
        return age
    
    #return the date in european format
    def european_format(self, date_obj: date) -> str:
        '''convert date to European format (dd/mm/yyyy)'''
        return date_obj.strftime("%d/%m/%Y")
        
def main():
    '''main loop to get user input and calculate age'''

    #create instance of base class
    handler = AgeCalculator()
    while True:
        user = input("PLEASE ENTER YOUR BIRTH DATE IN MM/DD/YYYY FORMAT : ").strip()
        user_dob = handler.date_validate(user, "%m/%d/%Y")
        
        if user_dob == "format_error":
            print("ERROR, INVALID FORMAT, PLEASE ENTER DATE IN MM/DD/YYYY FORMAT")
            continue
        elif user_dob == "future_error":
            print("ERROR, DATE CANNOT BE IN THE FUTURE, PLEASE ENTER A VALID BIRTH DATE")
            continue

        age = handler.calculate_age(user_dob)
        print(f"YOUR CURRENT AGE IS (YEARS): {age}")
        eu_format = handler.european_format(user_dob)
        print(f"DATE OF BIRTH IN EUROPEAN FORMAT: {eu_format}")
        break

if __name__ == "__main__":
    main()