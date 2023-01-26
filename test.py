data = [('день', 116), ('год', 103), ('просто', 97), ('просто', 90), ('хороший', 86), ('весь', 80), ('40', 79), ('dsp', 77), ('вообще', 75), ('хороший', 72)]



from datetime import datetime

dt = datetime.strptime(str(datetime.today()), '%Y-%m-%d %H:%M:%S')

print(dt)


print(datetime.today())