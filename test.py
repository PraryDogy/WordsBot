from datetime import datetime

test_time = '2023-01-06 16:04:06'

test_time = datetime.strptime(test_time, '%Y-%m-%d %H:%M:%S')


print(test_time.strftime('%H:%M'))