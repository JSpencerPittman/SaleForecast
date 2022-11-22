from bisect import bisect_left
import pandas as pd
from typing import Tuple

# REQUIRES a formatted holiday dataset already
class HolidayUtility:
    def __init__(self, holiday):
        self.holiday = holiday
        
        
    def findHolidaysOnDate(self, date: pd.Timestamp) -> pd.DataFrame:
        left = bisect_left(self.holiday.date, date)
        
        # True if a holiday on that day wasn't found
        if(self.holiday.iloc[left].date != date):
            return pd.DataFrame()
       
        # Include all following holidays on the
        # same day
        right = left
        while(self.holiday.date[right+1] == date):
            right+=1
            
        # Only one holiday
        if left == right:
            return pd.DataFrame(self.holiday.iloc[left]).T
        # more than one holiday
        else:
            return self.holiday.iloc[left:right+1]
    
    
    # Metric for how important a holiday is
    # based on specificity and occurences
    def holiday_importance(self, description):
        specificity = 1
        locale = self.holiday.locale.loc[self.holiday.description == description].iloc[0]
        # The more local the higher the specificity
        if locale == "Local":
            specificity = 10
        elif locale == "Regional":
            specificity = 5

        occurences = len(self.holiday.loc[self.holiday.description == description])

        return occurences * specificity
    
    # Is the holiday celebrated in the same region
    def holidayCelebratedInLocale(self, holiday_row: pd.Series, train_row: pd.Series) -> bool:
        if holiday_row.locale == "National":
            return True
        elif holiday_row.locale == "Regional" and holiday_row.locale_name == train_row.state:
            return True
        elif holiday_row.locale_name == train_row.city:
            return True
        else:
            return False
        
        
    # Calculates corresponding holiday data for each row
    def calculateHolidayValues(self, train_row: pd.Series) -> Tuple[int, str]:
        # All holidays occuring on the same day
        sameDayHolidays = self.findHolidaysOnDate(train_row.date)
        
        # All holidays that are actually relevant
        relevantHolidays = []

        # Narrow down the found holidays to ones that are
        # celebrated in the region
        for i, sameDayHoliday in sameDayHolidays.iterrows():
            if self.holidayCelebratedInLocale(sameDayHoliday, train_row):
                relevantHolidays.append(sameDayHoliday)

        # Calculate the cumalative importance of all holidays
        importance = sum([self.holiday_importance(holiday.description) for holiday in relevantHolidays])

        # Find the holiday type
        if len(relevantHolidays) > 1:
            holiType = "Combined"
        elif len(relevantHolidays) == 1:
            holiType = sameDayHolidays.iloc[0].type
        else:
            holiType = "None"

        return (importance, holiType)
    