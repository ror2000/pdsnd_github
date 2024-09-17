import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    # Get user input for city
    city = input("Choose a city (Chicago, New York City, Washington):\n").lower()
    while city not in CITY_DATA:
        city = input("Invalid input. Choose a city (Chicago, New York City, Washington):\n").lower()

    # Get user input for filter type
    filter_type = input("\nFilter by month, day, both, or not at all? Type \"all\" for no filter:\n").lower()
    while filter_type not in ['month', 'day', 'both', 'all']:
        filter_type = input("\nInvalid input. Filter by month, day, both, or not at all? Type \"all\" for no filter:\n").lower()

    month, day = 'all', 'all'  # Default values

    if filter_type in ['month', 'both']:
        month = input("\nWhich month? (January, February, March, April, May, June):\n").lower()
        while month not in months:
            month = input("\nInvalid input. Which month? (January, February, March, April, May, June):\n").lower()

    if filter_type in ['day', 'both']:
        day = input("\nWhich day? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday):\n").lower()
        while day not in days:
            day = input("\nInvalid input. Which day? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday):\n").lower()

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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
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

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day: ', popular_day)

    # display the most common start hour
    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]
    print('Most Frequent Start Station - End Station Combo:',
          popular_start_end_station[0], '-', popular_start_end_station[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total of travel time is ', df['Trip Duration'].sum())

    # display mean travel time
    print('The mean of travel time is ', df['Trip Duration'].mean(numeric_only=True))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types is:\n', user_types)

    # Display counts of gender
    user_genders = df['Gender'].value_counts()
    print('\nThe counts of Genders is:\n', user_genders)

    # Display earliest, most recent, and most common year of birth
    print('\nThe earliest year of birth', df['Birth Year'].min())
    print('The most recent year of birth', df['Birth Year'].max())
    print('The most common year of birth', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """ Display 5 rows each time the user requests to display the Dataframe data. """
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    end_loc = 5
    
    while view_data == 'yes':
        print(df.iloc[start_loc: end_loc])
        start_loc += 5
        end_loc += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        if city != 'washington':
            user_stats(df)

        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
