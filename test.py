from datetime import datetime, timedelta

now = datetime.today()

msgs = [
    ("for delete", datetime.now() - timedelta(hours=2)),
    ("for delete", datetime.now() - timedelta(hours=2)),
    ("for delete", datetime.now() - timedelta(hours=2)),
    ("young", datetime.now() - timedelta(minutes=30)),
    ("young", datetime.now() - timedelta(minutes=30)),
    ("young", datetime.now() - timedelta(minutes=30)),
    ]


def clearr():
    young_msgs = []
    for msg, time in msgs:
        if now - timedelta(hours=1) > time:
            pass
        else:
            young_msgs.append((msg, time))

    msgs.clear()
    msgs.extend(young_msgs)

