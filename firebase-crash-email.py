#!/usr/bin/env python
# -*- encoding: utf8 -*-

from imap_tools import MailBox
from imap_tools import AND
import datetime
from datetime import timezone, timedelta

account = 'YOUR_ACCOUNT'
password = 'YOUR_PASSWORD'
filterSender = 'YOUR_SENDER'
tw_timezone = timezone(timedelta(hours=+8))
since_days = 6
start_time = datetime.date.today() - datetime.timedelta(days=since_days)
filterSubjects = ["當機風險驟升快訊", "新的 ANR 問題", "新的嚴重問題"]
velocity_alert_count = 0
fatal_count = 0
anr_count = 0
print(f"開始時間: {start_time}")
with MailBox('imap.gmail.com').login(account, password, 'INBOX') as mailbox:
    result = mailbox.fetch(criteria=AND(date_gte=start_time, from_=filterSender))
    for msg in result:
        subject = msg.subject
        isInCondition = False
        for filterCondition in filterSubjects:
            if filterCondition in subject:
                if filterCondition == "當機風險驟升快訊":
                    velocity_alert_count += 1
                elif filterCondition == "新的 ANR 問題":
                    anr_count += 1
                elif filterCondition == "新的嚴重問題":
                    fatal_count += 1
                isInCondition = True
                break
        if not isInCondition:
            continue
        date = msg.date.astimezone(tw_timezone)
        html = msg.html
        print(date, subject, len(msg.text or msg.html))
        print(msg.html)
        print("--------------------------------------------------")

    print("當機風險驟升快訊: ", velocity_alert_count)
    print("新的 ANR 問題: ", anr_count)
    print("新的嚴重問題: ", fatal_count)
