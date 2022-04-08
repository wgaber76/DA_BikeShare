import time
import pandas as pd
import numpy as np

# define global variables that can be used by all functions
city = ""
month = ""
day = ""

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# Dictionary for the months names and their relevant ordring
Months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
          'september': 9, 'october': 10,
          'november': 11, 'december': 12, 'all': 13}

Days = {'saturday': 1, 'sunday': 2, 'monday': 3, 'tuesday': 4, 'wednesday': 5, 'thursday': 6, 'friday': 7, 'all': 8}


def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter city name ({}):".format(CITY_DATA.keys()))
    city = city.lower()
    while city not in CITY_DATA.keys():
        city = input("Please enter city name (make sure it is from the following list!) ({}):".format(CITY_DATA.keys()))
        city = city.lower()
    # get user input for month (all, january, february, ... , june)
    month = input("Please enter 'all' or month name ({}):".format(Months.keys()))
    month = month.lower()
    while month not in Months.keys():
        month = input(
            "Please enter 'all' or month name (make sure it is from the following list!) ({}):".format(Months.keys()))
        month = month.lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter 'all' or day name ({}):".format(Days.keys()))
    day = day.lower()
    while day not in Days.keys():
        day = input(
            "Please enter 'all' or day name (make sure it is from the following list!) ({}):".format(Days.keys()))
        day = day.lower()
    print('-' * 40)
    # city = 'new york city'
    # month = 'all'
    # day = 'all'
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read the CSV file relevant to the user city selection
    try:
        df = pd.read_csv(CITY_DATA[city])
        if (month != 'all'):  # handle filtering df by month or no filtering
            df['StartTime month'] = pd.DatetimeIndex(df['Start Time']).month
            df = df[df['StartTime month'] == Months[month]]
        if (day != 'all'):  # handle filtering df by weekday or no filtering
            df['StartTime day_of_week'] = pd.to_datetime(df['Start Time']).dt.day_name()
            df['StartTime day_of_week'] = df['StartTime day_of_week'].str.lower()
            df = df[df['StartTime day_of_week'] == day]

    except FileNotFoundError:  # in case data files are missing. I will return empty dataframe
        # How to handle this error if happens
        print('Data File Not found! \n Please make sure data file are in the same folder of the program. \n')
        df = pd.DataFrame()

    # Filter the data frame based on month or day selection. it add extra two columns for month and day of the week

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month. Create month column which is not early created if the criteria wasn't all
    if month == 'all':
        df['StartTime month'] = pd.DatetimeIndex(df['Start Time']).month
        keys_list = list(Months.keys())
        print('The most common month is : \'{}\' \n '.format(keys_list[(df['StartTime month'].mode()[0]) - 1]))

    # display the most common day of week. Create weekday column which is not early created of the criteria wasn't all
    if day == 'all':
        df['StartTime day_of_week'] = pd.to_datetime(df['Start Time']).dt.day_name()
        df['StartTime day_of_week'] = df['StartTime day_of_week'].str.lower()
        print('The most common weekday is : \'{}\' \n'.format(df['StartTime day_of_week'].mode()[0]))

    # display the most common start hour
    df['Start Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    print('The most common start hour is {} o\'clock \n'.format(df['Start Hour'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips (from->to stations)."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('The most common start station is \'{}\' \n'.format(df['Start Station'].value_counts().index[0]))

    # display most commonly used end station

    print('The most common end station is \'{}\' \n'.format(df['End Station'].value_counts().index[0]))

    # display most frequent combination of start station and end station trip

    df['Trip Path'] = df['Start Station'] + ' -> ' + df['End Station']
    print('The most common Trip is \'{}\' \n'.format(df['Trip Path'].value_counts().index[0]))

    # print('The most common trip is from  \'{}\'  to \'{}\' '.format(df['Trip_Path'].value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration in hours."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time is {} hours \n'.format(df['Trip Duration'].sum() / 60 / 60))
    # display mean travel time
    print('Average Trip duration is {} hours \n'.format(df['Trip Duration'].mean() / 60 / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users. It takes dataframe and
    print the user types count, gender data if available and birth year statistics if available"""
    # As the columns "Gender" and "Birth Year" are not available in all data files
    # I handled here the exception of referring to them in washington case
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\n User Types : \n", df['User Type'].value_counts())
    # Handle the case where washington file doesn't have Gender or birth year data
    if "Gender" in df.columns:
        # Display counts of gender
        print("\n Gender: \n", df['Gender'].value_counts())
    else:
        print("\n Unable to find (Gender) data in this data file! \n ")

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print("\n Earliest year of birth is : ", df['Birth Year'].min())
        print("Most recent year of birth is :", df['Birth Year'].max())
        print('The most common year of birth is {} :'.format(df['Birth Year'].value_counts().index[0]))
    else:
        print("\n Unable to find (Birth Year) data in this data file! \n ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df, city):
    """ This function takes dataframe and the city name and print 5 rows by 5 rows from the dataframe until the user
    says no """
    index = 0
    user_input = input(' \n would you like to display 5 rows of raw data?  ').lower()
    while user_input in ['yes', 'y', 'yep', 'yea'] and index + 5 < df.shape[0]:
        if city != "washington":  # I added this to show only original data not the added columns for calculations
            print("\n\n")
            print(df.iloc[index:index + 5, 0:9])
        else:
            print("\n\n")
            print(df.iloc[index:index + 5, 0:7])
        index += 5
        user_input = input(' \n would you like to display more 5 rows of raw data? ').lower()


def main(city, month, day):
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)
        if len(df) == 0:
            print('No data to show using this criteria City of :{} Month of :{} Day of :{} \n Please try again!'.format(
                city, month, day))
        else:
            print(df.head)
            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main(city, month, day)
