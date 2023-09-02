from datetime import date, timedelta

from src.database import db
from src.database.models import User
from typing import Type
from datetime import date, timedelta


from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import UserModel

# list_of_7_dates = []
# today_date = date.today()
# str_today_date = str(today_date)
# for i in range(7):
#     list_of_7_dates.append(str(today_date + timedelta(days=i)))
# print(list_of_7_dates)
#
# for i in list_of_7_dates:
#     if str_today_date[5:] in i[5:]:
#         print(today_date)
#
# print((today_date + timedelta(days=7)))

today_date = date.today()
seventh_day_date = today_date + timedelta(days=7)
# delta1 = date(today_date.year, today_date.month, today_date.day)

delta1 = date(today_date.year, User.day_of_born.month, User.day_of_born.day)
# res = db.query(User).filter(today_date < delta1, delta1 <= seventh_day_date).all()
print(delta1)

date_str = '09-19-2022'
date_object = datetime.strptime(date_str, '%m-%d-%Y').date()
User.day_of_born.month
date_object = datetime.strptime(User.day_of_born, '%Y-%m-%d').date()

