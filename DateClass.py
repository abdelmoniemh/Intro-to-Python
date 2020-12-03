class Date:
    def __init__(self, d, m, y):
        try:
            self.Day = int(d)
            self.Month = int(m)
            self.Year = int(y)
            self.MonthLen()
        except:
            print("Invalid parameters")

    def getDay(self):    #returns day
        return self.Day

    def getMonth(self):    #returns month
        return self.Month

    def getYear(self):    #returns year
        return self.Year

    def MonthLen(self):    #returns the maximum amount of days in a month
        if self.Month in [1, 3, 5, 7, 8, 10, 12]:
            self.monthMax = 31
        elif self.Month in [4, 6, 9, 11]:
            self.monthMax = 30
        else:
            if self.Year % 400 == 0 or self.Year % 4 == 0 and self.Year % 100 != 0:
                self.monthMax = 29
            else:
                self.monthMax = 28

    def arbMonthLen(self, m, y):    #returns the maximum amount of days in an arbituary month
        if m == 0: #input is m-1 when function is called, needs to correct that if m = 1
            m = 12
            y -= 1
        if m in [1, 3, 5, 7, 8, 10, 12]: 
            Max = 31
        elif m in [4, 6, 9, 11]:
            Max = 30
        else:
            if y % 400 == 0 or y % 4 == 0 and y % 100 != 0:
                Max = 29
            else:
                Max = 28
        return Max

    def Next(self):    #returns the next day
        d, m, y = self.Day, self.Month, self.Year
        if self.Day + 1 <= self.monthMax: #checks if you can increment the day by one without crossing the maximum amount of days in a month
            d = self.Day + 1
        elif self.Month < 12: #case for when you start a new month
            d, m = 1, self.Month + 1
        else: #case for when you start a new year
            d, m, y = 1, 1, self.Year + 1
        return Date(d, m, y)

    def Prev(self):
        d, m, y = self.Day, self.Month, self.Year 
        if self.Day - 1 >= 1: #checks if you can decrease the day by one without crossing the minimum amount of days in a month
            d = self.Day - 1
        elif self.Month > 1: #case for when you go back a month 
            d, m = self.arbMonthLen(m - 1, y), self.Month - 1
        else:    #case for when you go back into the previous year
            d, m, y = 31, 12, self.Year - 1
        return Date(d, m, y)

    def isBefore(self, d): #checks if the current day is before another instance of the class
        if d.Year > self.Year:
            return True
        elif d.Month > self.Month and d.Year == self.Year:
            return True
        elif d.Day > self.Day and d.Month == self.Month and d.Year == self.Year:
            return True
        else:
            return False

    def isAfter(self, d): #checks if the current day is after another instance of the class
        if d.Year < self.Year:
            return True
        elif d.Month < self.Month and d.Year == self.Year :
            return True
        elif d.Day < self.Day and d.Month == self.Month and d.Year == self.Year:
            return True
        else:
            return False

    def isEqual(self, d): #checks if the two days are equal
        if not (self.isBefore(d)) and not (self.isAfter(d)):
            return True
        else:
            return False

    def add_days(self, n):
        day, month, year = self.Day, self.Month, self.Year
        daysLeft = n
        while daysLeft > 0:    #while loop runs until there are no days left to add
            monthMax = self.arbMonthLen(month, year) #generates the length of the current month
            if day + daysLeft <= monthMax: #if you can add the days without crossing the limit of the month
                day += daysLeft    #then you are at the last month and can break out of the loop
                daysAdded = day - daysLeft
                daysLeft -= daysAdded
                break 
            else: #if you cannot that means there is > 1 month left to be added
                daysAdded = monthMax - day
                daysLeft -= daysAdded
                day = 0
                if month + 1 <= 12: #case for when you start a new month
                    month += 1
                else: #case for when you cross over into a new year
                    month = 1
                    year +=1
        return Date(day, month, year)
    """Basically the add days function adds days until you reach a new month/year removes what you added
    to get to that point from what needs to be added and runs again until you are done adding all 
    the days"""

    def days_between(self, d): #attempt at a more effecient solution rather than just iterating from the smaller day to the bigger one and counting
        if self.isEqual(d):
            return 0
        elif self.isBefore(d): #establishes which day is bigger to prevent error with arithmetic
            biggerDate = d
            smallerDate = self
        else:
            biggerDate = self
            smallerDate = d

        if (biggerDate.Month, biggerDate.Year) == (smallerDate.Month, smallerDate.Year): #if the month and year are equivalent you can just take the difference of the days
            return biggerDate.Day - smallerDate.Day
        elif biggerDate.Year == smallerDate.Year: #if they are within the same year take the difference between the smaller date and 
            smallerDay = smallerDate.Day #the end of its month and the bigger date and the beginning its month and adds the months between them
            biggerDay = biggerDate.Day
            initError = self.arbMonthLen(smallerDate.Month, smallerDate.Year) - smallerDay 
            finError = biggerDay
            diffInDays = initError + finError
            for month in range(smallerDate.Month + 1, biggerDate.Month):
                diffInDays += self.arbMonthLen(month, smallerDate.Year)
        else:
            initEndyearDiff = smallerDate.days_between(Date(31, 12, smallerDate.Year)) #recursive function to determine the amount of days till the end of the year for the smaller date
            finEndyearDiff = biggerDate.days_between(Date(1, 1, biggerDate.Year)) #determines days between the enddate and the beginning of its year
            diffInDays = initEndyearDiff + finEndyearDiff
            if biggerDate.Year - smallerDate.Year > 1: #adds the amount of days in the years between them
                for i in range((biggerDate.Year - smallerDate.Year) - 1):
                    for j in range(1, 13):
                            diffInDays += self.arbMonthLen(j, smallerDate.Year + i)
            diffInDays +=1
        return diffInDays




today = Date(1,1,2020)
tomorrow = Date(30,7,2020)


future = today.days_between(tomorrow)
print(future)



