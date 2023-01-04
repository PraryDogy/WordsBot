from datetime import datetime



datetime_str = '01/03/23 21:42:00'
datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
datetime_object = datetime_object.timestamp()

print(datetime_object)

next_update = datetime.fromtimestamp(datetime_object+86400)

if next_update.date() <= datetime.today().date():
    print('today')
else:
    print('tomorrow')