# -*- coding: utf-8 -*-

from jdwdate.Enums._TimeUnits cimport TimeUnits as tu

cpdef enum TimeUnits:
    BDays = tu.BDays
    Days = tu.Days
    Weeks = tu.Weeks
    Months = tu.Months
    Years = tu.Years