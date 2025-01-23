import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    message = re.split(pattern, data)[1:]
    timing = re.findall(pattern, data)

    df = pd.DataFrame({'message_timing':timing,'user_message':message})
    df['message_timing'] = pd.to_datetime(df['message_timing'], format='%m/%d/%y, %I:%M %p - ')

    users = []
    messages = []

    for i in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', i)

        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['message_timing'].dt.date
    df['year'] = df['message_timing'].dt.year
    df['month_no'] = df['message_timing'].dt.month
    df['month'] = df['message_timing'].dt.month_name()
    df['day'] = df['message_timing'].dt.day
    df['day_name'] = df['message_timing'].dt.day_name()
    df['hour'] = df['message_timing'].dt.hour
    df['minute'] = df['message_timing'].dt.minute
    df['am_pm'] = df['message_timing'].dt.strftime('%p')
    df['hour_12'] = df['message_timing'].dt.hour % 12
    df['hour_12'] = df['hour_12'].replace(0, 12)

    period = []

    for _, row in df[['hour', 'am_pm']].iterrows():
        hour = row['hour']
        am_pm = row['am_pm']
        
        if hour == 12 and am_pm == 'PM':  # Noon
            period.append(f"{hour}{am_pm}-1AM")
        elif hour == 12 and am_pm == 'AM':  # Midnight
            period.append(f"{hour}{am_pm}-1PM")
        elif hour == 11 and am_pm == 'AM':  # 11 AM to 12 PM transition
            period.append(f"{hour}{am_pm}-12PM")
        elif hour == 11 and am_pm == 'PM':  # 11 PM to 12 AM transition
            period.append(f"{hour}{am_pm}-12AM")
        else:
            next_hour = (hour % 12) + 1  # Calculate the next hour in 12-hour format
            period.append(f"{hour}{am_pm}-{next_hour}{am_pm}")

    df['period'] = period

    return df