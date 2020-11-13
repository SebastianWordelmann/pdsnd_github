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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city do you want to explore? Please type the full city name: Chicago, New York City or Washington: \n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("That\'s not a valid city")
        else:
            print("Ok - we are going to explore the data for {}".format(city))
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("In which month are you interested in? Please type the full month name: January, February, March, April, May, June or All to apply no filter? : \n").lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("That\'s not a valid month")
        else:
            print("Ok - we are going to explore the data for {} in {}".format(city, month))
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("In which day are you interested in? Please type the full day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All to apply no filter? : \n").lower()
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("That\'s not a valid month")
        else:
            print("Ok - we are going to explore the data for {} in {} on {}".format(city, month, day))
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
        df - pandas DataFrame containing city data filtered by month and day
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
        month = months.index(month) +1

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
    print('Most Frequent Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    popular_combination = ('\nStart: ' + df['Start Station'] + '\nEnd: ' + df['End Station']).mode()[0]
    print('Most Frequent Combination of Start and End Station:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/60/60
    print('Total Travel Time:', total_travel_time.round(2), 'hours')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('Mean Travel Time:', mean_travel_time.round(2), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    try:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
        user_birth_earl = df['Birth Year'].min()
        user_birth_old = df['Birth Year'].max()
        user_birth_mc = df['Birth Year'].mode()[0]
        print('Earliest Year of Birth:', user_birth_earl)
        print('Most Recent Year of Birth:', user_birth_old)
        print('Most Common Year of Birth:', user_birth_mc)
    except:
        print('There is no data for gender and birth.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Displays raw data if the user wants to.

        start = -5
        end = 0

        raw_data = input('\nWould you like to see 5 lines of raw user data? Enter yes or no.\n')
        while True:
            if raw_data.lower() == 'yes':
                start += 5
                end += 5
                print(df[start:end])
                raw_data = input('\nWould you like to see further 5 lines of raw user data? Enter yes or no.\n')
            else:
                break

        #Restarts the program if the user wants to.

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
