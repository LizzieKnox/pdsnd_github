import time
import pandas as pd

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
city_name = ''

MONTH_DATA =  { 'Jan': 1,
                'Feb': 2,
                'Mar': 3, 
                'Apr': 4,     
                'May': 5,
                'Jun': 6,
                'All': -1 }

month_name = ''

DAY_DATA =   {  'Monday': 0,
                'Tuesday': 1,
                'Wednesday': 2,
                'Thursday': 3,
                'Friday': 4,
                'Saturday': 5,
                'Sunday': 6,
                'All':  -1 }

day_name = ''

for i in CITY_DATA:
    if list(CITY_DATA.keys())[0]==i :
        city_name += i
    else:
        city_name += ' , ' + i

for i in MONTH_DATA:
    if list(MONTH_DATA.keys())[0]==i :
        month_name += i
    else:
        month_name += ' , ' + i

for i in DAY_DATA:
    if list(DAY_DATA.keys())[0]==i :
        day_name += i
    else:
        day_name += ' , ' + i

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
    city = input('Enter name of the city ({}) to analyze: '.format(city_name))

    while city.title() not in CITY_DATA:
        city = input('{} isn\'t a vaild selection'.format(city))

    # get user input for month (all, january, february, ... , june)
    month = input('Enter the month ({}) to analyze: '.format(month_name))

    while month.title() not in MONTH_DATA:
        month = input('{} isn\'t a vaild selection'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter the day ({}) to analyze: '.format(day_name))
    while day.title() not in DAY_DATA:
        day = input('{} isn\'t a vaild selection'.format(day))

    print( 'City choosen {} , Month choosen : {} , Day choosen : {}'.format(city, month, day).title())
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
    city_file = CITY_DATA[city.title()]
    df = pd.read_csv(city_file)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    if month.title() != 'All':
        df = df.loc[df['Start Time'].dt.month ==MONTH_DATA[month.title()] ]
        
    if day.title() != 'All':
        df = df.loc[df['Start Time'].dt.dayofweek ==DAY_DATA[day.title()] ]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()

    common_month = list(df['month'].mode())

    print('The Most common Month is :', common_month[0])

    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()

    common_day = list(df['day'].mode())

    print('The Most common Day is :', common_day[0])

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour

    common_hour = list(df['hour'].mode())

    print('The Most common Hour is :', common_hour[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('\nThe most commonly used start station is :\n')

    print(df.groupby(['Start Station']).size().nlargest(1))

    # display most commonly used end station
    print('\nThe most commonly used end station is :\n')

    print(df.groupby(['End Station']).size().nlargest(1))

    # display most frequent combination of start station and end station trip
    print('\nThe most commonly used end station is :\n')

    print(df.groupby(['Start Station','End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel time'] = df['End Time'] - df['Start Time']

    print('\nTotal Travel Time is :\n')
    print(df['travel time'].sum())
    
   
    # display mean travel time
    print('\nMean Travel Time is :\n')
    print(df['travel time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    if city.title() == 'Washington':
            print('\n No Birth and User date for Washington available')
            end()
        

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\n Count of user type is :\n')
    print(df.groupby(['User Type']).size())

    # Display counts of gender

    print('\n Count of gender is :\n ')
    print(df.groupby(['Gender']).size())

    # Display earliest, most recent, and most common year of birth
    earliest_dob = df['Birth Year'].min()
    latest_dob = df['Birth Year'].max()
    common_dob = list(df['Birth Year'].mode())

    print('\nYear of Birth Information \n earliest year is {} \n lastest year is {} \n commonest year is {}'
          .format(int(earliest_dob), int(latest_dob), int(common_dob[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Asks the user if they would like to view individual trip data in loops of 5 rows"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0 
    view_data_output = ['Yes', 'No']

    while view_data.title() not in view_data_output:
        view_data  = input('{} isn\'t a vaild selection'.format(view_data))

    while view_data.lower() == 'yes':
        if start_loc > df.size:
            print('n\ No further data to display!')
            end()
        
        print(df.iloc[start_loc: start_loc + 5 ])
        start_loc += 5
        view_data = input("\n Do you wish to continue?: ").lower()
        
        while view_data.title() not in view_data_output:
            view_data  = input('{} isn\'t a vaild selection'.format(view_data))


def main():
    while True:
        pd.set_option('display.max_columns', None)

        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

