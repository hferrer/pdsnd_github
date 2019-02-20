import time
import pandas as pd
import numpy as np
from datetime import timedelta


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june','all']

weekdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        input1 = input("\nEnter the city (Chicago, New York, or Washington): ")
        if input1.lower() not in CITY_DATA.keys():
            print("\nPlease select one of the three available cities.")
        else:
            city = input1.lower()
            print("\nYou chose {}.".format(city.title()))
            break

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        input2 = input("\nYou can select a specific month of data or request all the data. If you want to view a specific month, enter the month using its full name (January through June). Otherwise, choose 'All': ")
        if input2.lower() not in months:
            print("\nPlease select an appropriate month or choose 'All'.")
        else:
            month = input2.lower()
            print("\nYou chose {}.".format(month.title()))
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        input3 = input("\nYou can select a specific weekday of data or request all the days in a week. If you want to view a specific weekday, enter the weekday using its full name (Sunday through Saturday). Otherwise, choose 'All'.: ")
        if input3.title() not in weekdays:
            print("\nPlease select an appropriate day of the week, using its full name or 'All'.")
        else:
            day = input3.title()
            print("\nYou chose {}.".format(day))
            break

    print('-'*40)
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

    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name
    df['Weekday'] = df['Start Time'].dt.weekday
    df['Start Hour'] = df['Start Time'].dt.hour
    df['PATH'] = df['Start Station']+" - "+df['End Station']

    # filter by month if applicable

    if month != 'all':

        ref_month = months.index(month)+1
        df = df[df['Month'] == ref_month]

    # filter by day of week if applicable
    if day != 'All':
        df = df[df['Day_of_Week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if df['Month'].std() !=0:
        print("\nThe most frequent month for travel is {}.".format(months[(df['Month'].mode()[0])-1].title()))
    else:
        print("\nYou have chosen to view data for a single month so we cannot compare it to other months.  If you would like to see the overall most frequent month for travel for the city in the dataset, please choose 'All'.")

    if df['Weekday'].std() !=0:
        wkdy = df['Weekday'].mode()[0]
        print("\nThe most frequent weekday for travel is {}.".format(weekdays[wkdy]))
    else:
        print("\nYou have chosen to view data for a single weekday so we cannot compare it to other weekdays.  If you would like to see the overall most frequent weekday for travel for the city in the dataset, please choose 'All'.")

    freq_hr = df['Start Hour'].mode()[0]
    print("\nThe most common hour for travel is {}.".format(freq_hr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    #if month == "all" and day.lower() == "all":

    often_start_stations_name = df['Start Station'].describe()[2]
    often_start_stations_freq = df['Start Station'].describe()[3]

    print("\nThe most commonly used start station is {} ({} occurrences).".format(often_start_stations_name, often_start_stations_freq))

########

    # TO DO: display most commonly used end station

    often_end_stations_name = df['End Station'].describe()[2]
    often_end_stations_freq = df['End Station'].describe()[3]

    print("\nThe most commonly used end station is {} ({} occurrences).".format(often_end_stations_name, often_end_stations_freq))

    # TO DO: display most frequent combination of start station and end station trip

    often_path_name = df['PATH'].describe()[2]
    often_path_freq = df['PATH'].describe()[3]

    print("\nThe most common combination of a start station and end station is {} ({} occurrences).".format(often_path_name, often_path_freq))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_time = df['Trip Duration'].sum()
    total_trip = timedelta(seconds = int(total_trip_time))

    # TO DO: display mean travel time
    avg_trip_time = (df['Trip Duration'].mean())
    avg_trip = timedelta(seconds = int(avg_trip_time))

    #Longest trip
    longest_trip_time = (df['Trip Duration'].max())
    longest_trip = timedelta(seconds = int(longest_trip_time))

    # Shortest trip
    shortest_trip_time = (df['Trip Duration'].min())
    shortest_trip = timedelta(seconds = int(shortest_trip_time))
    print("\nThe total amount traveled in the city is {}.\n".format(total_trip))
    print("\nThe average amount of time traveled in the city is {}.\n".format(avg_trip))
    print("\nThe longest trip time in the city is {}.\n".format(longest_trip))
    print("\nThe shortest trip time in the city is {}.\n".format(shortest_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        test_na_user = df['User Type'].isnull().sum()
        print("\nThere are a total of {} 'nan' in the User Type column.".format(test_na_user))
        user_types = df['User Type'].dropna(axis=0)
        user_types = user_types.unique().tolist()
        type_counts = []
        for type in user_types:
            type_counts.append(df['User Type'].str.count(type).sum())
        type_info = dict(zip(user_types, type_counts))
        for key,val in type_info.items():
            print ("The following types of customers are represented in the data:", key, " - ", val)
    except:
        print("\nThere does not appear to be any User Type data for that city.")


    # TO DO: Display counts of gender

    try:
        test_na_gender = df['Gender'].isnull().sum()
        print("\nThere are a total of {} 'nan' in the Gender column.".format(test_na_gender))
        gender_types = df['Gender'].dropna(axis=0)

        gender_types = gender_types.unique().tolist()

        gender_type_counts = []
        for genders in gender_types:
            gender_type_counts.append(df['Gender'].str.count(str(genders)).sum())

        gender_info = dict(zip(gender_types, gender_type_counts))
        for key,val in gender_info.items():
            print ("The following customer genders represented in the data:", key, " - ", val)

    except KeyError:
        print("\nThere does not appear to be any Gender data for that city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        test_na_birthyear = df['Birth Year'].isnull().sum()
        print("\nThere are a total of {} 'nan' in the Birth Year column.".format(test_na_birthyear))
        birth_years_clean = df.dropna(axis=0)

        birth_years_max = birth_years_clean['Birth Year'].max()
        birth_years_min = birth_years_clean['Birth Year'].min()
        birth_years_common = birth_years_clean['Birth Year'].mode()[0]

        print("The earliest birth year in the system is {}.".format(birth_years_min))
        print("The most recent birth year in the system is {}.".format(birth_years_max))
        print("The most common birth year in the system is {}.".format(birth_years_common))
    except KeyError:
        print("There does not appear to be Birth Year data for that city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):

    view_data = input("\nWould you like to see the data?  Enter 'yes'. Otherwise, enter anything else.\n")
    if view_data.lower() == 'yes':
        views_list = range(0,len(df),5)
        for view in views_list:
            df_view = df.iloc[view:view+5,]  #https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
            print(df_view)
            keep_viewing = input("\nWould you like to see more data?  Enter 'yes'.  Otherwise, enter anything else.\n")
            if keep_viewing.lower() == 'yes':
                continue
            break


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        time.sleep(4)
        station_stats(df)
        time.sleep(4)
        trip_duration_stats(df)
        time.sleep(4)
        user_stats(df)
        time.sleep(4)
        view_data(df)

        restart = input('\nWould you like to restart? Enter "yes". Otherwise, feel free to bang on the keyboard.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
