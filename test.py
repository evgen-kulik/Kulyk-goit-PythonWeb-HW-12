from datetime import date, timedelta

from src.database import db
from src.database.models import User
from typing import Type
from datetime import date, timedelta


from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import UserModel

list_of_7_dates = []
today_date = date.today()
str_today_date = str(today_date)
for i in range(7):
    list_of_7_dates.append(str(today_date + timedelta(days=i)))
print(list_of_7_dates)

for i in list_of_7_dates:
    if str_today_date[5:] in i[5:]:
        print(today_date)

print((today_date + timedelta(days=7)))


