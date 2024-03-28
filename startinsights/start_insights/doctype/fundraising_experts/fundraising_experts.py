# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate,today,time_diff_in_hours,get_datetime,get_time,add_days,date_diff,now, add_to_date
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta, MO
from datetime import datetime, timedelta,time
from frappe import _



class FundraisingExperts(Document):
    
    def validate(self):
        if self.first_name and self.last_name:
            self.full_name = str(self.first_name) + ' ' + str(self.last_name)

    @frappe.whitelist()
    def get_total_dates(self):
        book_dict = {}
        get_date_diff = date_diff(self.to_date,self.from_date) + 1
        start_date = getdate(self.from_date)
        date_list = [add_days(start_date, i) for i in range(get_date_diff)]
        booking_time = self.get_booking_time()
        book_dict = {
            "dates":date_list,
            "time_list":booking_time
        }
        return book_dict

    #get the booking time slot 
    def get_booking_time(self):
        time_list = []
        book_start_time = datetime.strptime(self.start_time, '%H:%M:%S')
        book_end_time = datetime.strptime(self.end_time, '%H:%M:%S')
        duration = int(self.duration)

        if duration == int(30):
            number_of_intervals = int((book_end_time - book_start_time).total_seconds() / (60 * duration))
            for i in range(number_of_intervals):
                get_time_split = book_start_time + relativedelta(minutes=i * duration)
                time_list.append([get_time_split.strftime('%H:%M'), (get_time_split + relativedelta(minutes=duration)).strftime('%H:%M')])
            return time_list
        elif duration == int(45):
            number_of_intervals = int((book_end_time - book_start_time).total_seconds() / (60 * duration))
            for i in range(number_of_intervals):
                get_time_split = book_start_time + relativedelta(minutes=i * duration)
                time_list.append([get_time_split.strftime('%H:%M'), (get_time_split + relativedelta(minutes=duration)).strftime('%H:%M')])
            return time_list
        elif duration == int(1):
            duration_in_hours = (book_end_time - book_start_time).total_seconds() / 3600
            number_of_intervals = int(duration_in_hours)
            for i in range(number_of_intervals):
                get_time_split = book_start_time + relativedelta(hours=i * duration)
                start_time_str = get_time_split.strftime('%H:%M')
                end_time_str = (get_time_split + relativedelta(hours=duration)).strftime('%H:%M')
                time_list.append([start_time_str, end_time_str])
            return time_list
        else:
            frappe.throw(_('Please Select a Valid Duration and Create Booking'))