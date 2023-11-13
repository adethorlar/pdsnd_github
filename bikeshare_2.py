import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input("Which city would you like to see data for: Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Sorry, that is not a valid city name. Please enter one of the city names above.")


    # Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Which month? January, February, March, April, May, June, or type 'all' if you do not have any preference? ").lower()
        if month in months:
            break
        else:
            print("Sorry, that is not a valid month. Please choose again.")


    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day? Please type a day of the week, or type 'all' if you do not have any preference. ").lower()
        if day in days:
            break
        else:
            print("Sorry, that's not a valid day of the week. Please choose again.")


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is : ', most_common_month)

    # Display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of the week is: ', most_common_day_of_week)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', most_common_start_hour)


    # Display time it took
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ', most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: ', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most common trip from start to end is:', ' to '.join(most_common_trip))


    # Display time it took
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ', mean_travel_time)


    # Display time it took
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are:\n', user_types)

    # Check if Gender column exists in the DataFrame
    if 'Gender' in df.columns:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('The counts of gender are:\n', gender_counts)

    # Check if Birth Year column exists in the DataFrame
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('The earliest year of birth is: ', earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('The most recent year of birth is :', most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('The most common year of birth is: ', most_common_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data 5 lines at a time upon request by the user."""
    start_loc = 0
    end_loc = 5

    show_data = input("Would you like to see the raw data? Enter yes or no: ").lower()
    if show_data == 'yes':
        while True:
            print(df.iloc[start_loc:end_loc])
            start_loc += 5
            end_loc += 5

            show_more = input("Would you like to see 5 more lines of raw data? Enter yes or no: ").lower()
            if show_more != 'yes':
                break
            if end_loc > df.shape[0]:
                print("You've reached the end of the data.")
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
