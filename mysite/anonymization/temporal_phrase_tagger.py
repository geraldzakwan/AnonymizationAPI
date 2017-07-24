# Code for tagging temporal expressions in text
# For details of the TIMEX format, see http://timex2.mitre.org/

import re
import string
import os
import sys
import nltk

# Requires eGenix.com mx Base Distribution
# http://www.egenix.com/products/python/mxBase/
# try:
#     from mx.DateTime import *
# except ImportError:
#     print """
# Requires eGenix.com mx Base Distribution
# http://www.egenix.com/products/python/mxBase/"""

# Predefined strings.
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
          eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
          eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
          ninety|hundred|thousand)"
hour_number = "(1|2|3|4|5|6|7|8|9|10|11|12)"
single_number = "(1|2|3|4|5|6|7|8|9|0)"
minute_number = "(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50|51|52|53|54|55|56|57|58|59)"
date_number = "(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
month = "(january|february|march|april|may|june|july|august|september| \
          october|november|december|jan|feb|mar|apr|jul|aug|sept|oct|nov|dec)"
dmy = "(year|day|week|month)"
rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
exp1 = "(before|after|earlier|later|ago)"
exp2 = "(this|next|last)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"
prep_day = "(on|this|next|last)"
at = "(at)"
at_or_around = "(at|around)"
on = "(on)"
around = "(around)"
o_clock = "(o'clock)"
prep_in = "(in)"
the = "(the)"
conj = "(.|:)"
num_ord = "(st|nd|rd|th)"
daytime = "(morning|afternoon|evening|night)"
hour_desc = "(AM|PM|am|pm|a.m.|p.m.|A.M.|P.M.|a.m|p.m|A.M|P.M)"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"

# ASUMSI : TEMPORAL PHRASE TAGGING DILAKUKAN DI AWAL BGT
# on / this / next / last Sunday
regxp17 = prep_day + " " + day + " " + daytime

# on / this / next / last Sunday
regxp6 = prep_day + " " + day
# at 3 pm
regxp7 = at_or_around + " " + hour_number + " " + hour_desc
# at 3 o'clock in the afternoon
regxp8 = at_or_around + " " + hour_number + " " + o_clock + " " + prep_in + " " + the + " " + daytime
# at 3 o'clock
regxp9 = at_or_around + " " + hour_number + " " + o_clock
# at 3.20 pm
# regxp10 = at + " " + hour_number + " " + conj + " " + minute_number + " " + hour_desc
regxp10 = at_or_around + " " + hour_number + conj + minute_number + " " + hour_desc

# Date 20 June
regxp12 = on + " " + date_number + " " + month

# Date 20th June
regxp11 = on + " " + date_number + num_ord + " " + month

# Date June 20
regxp14 = on + " " + month + " " + single_number + single_number

# Date June 20th
regxp13 = on + " " + month + " " + date_number + num_ord

# Date June 2
regxp15 = on + " " + month + " " + single_number

this_week_1 = "(tomorrow|the day after tomorrow|in a day|in one day|in 1 day|in two days|in three days|in 2 days|in 3 days|in four days|in 4 days|the next day|the next two days|the next three days|the next four days|the next five days|the next six days)"
regxp16 = this_week_1

reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
reg5 = re.compile(year)

reg6 = re.compile(regxp6, re.IGNORECASE)
reg7 = re.compile(regxp7, re.IGNORECASE)
reg8 = re.compile(regxp8, re.IGNORECASE)
reg9 = re.compile(regxp9, re.IGNORECASE)
reg10 = re.compile(regxp10, re.IGNORECASE)
reg11 = re.compile(regxp11, re.IGNORECASE)
reg12 = re.compile(regxp12, re.IGNORECASE)
reg13 = re.compile(regxp13, re.IGNORECASE)
reg14 = re.compile(regxp14, re.IGNORECASE)
reg15 = re.compile(regxp15, re.IGNORECASE)
reg16 = re.compile(regxp16, re.IGNORECASE)
reg17 = re.compile(regxp17, re.IGNORECASE)

def concatenate_tuple_to_str(tuple_list):
    concatenated_str = ""

    tuple_length = len(tuple_list)
    for i in range(0, tuple_length):
        concatenated_str = concatenated_str + tuple_list[i]
        if (i < tuple_length - 1):
            concatenated_str = concatenated_str + " "

    return concatenated_str

def am_or_pm(str):
    str = str.lower()
    if("a.m" in str or "am" in str):
        return "am"
    elif("p.m" in str or "pm" in str):
        return "pm"

def extract_simple_hour(str):
    if('1' in str):
        return 1
    if('2' in str):
        return 2
    if('3' in str):
        return 3
    if('4' in str):
        return 4
    if('5' in str):
        return 5
    if('6' in str):
        return 6
    if('7' in str):
        return 7
    if('8' in str):
        return 8
    if('9' in str):
        return 9

def tag_2(text):
    # on Friday morning
    for m in reg17.finditer(text):
        start = m.start()
        substring = m.group()
        idx_daytime = substring.rfind(' ')
        text = text.replace(substring, 'this week in the' + substring[idx_daytime:])

    # On Sunday
    for m in reg6.finditer(text):
        start = m.start()
        substring = m.group()
        # print('SINI GAN')
        # print(substring)
        if("on " in substring or "this " in substring):
            text = text.replace(substring, 'this week')
        elif("last " in substring):
            text = text.replace(substring, 'last week')
        elif("next " in substring):
            text = text.replace(substring, 'next week')

    # At 3 pm
    for m in reg7.finditer(text):
        start = m.start()
        substring = m.group()
        idx_space = substring.find(' ')
        number = int(substring[idx_space + 1])
        # number = extract_simple_hour(substring)
        if(am_or_pm(substring) == "am"):
            if(number < 4):
                text = text.replace(substring, 'in the night')
            elif(number < 11):
                text = text.replace(substring, 'in the morning')
            else:
                text = text.replace(substring, 'in the afternoon')
        else:
            if(number < 4):
                text = text.replace(substring, 'in the afternoon')
            elif(number < 9):
                text = text.replace(substring, 'in the evening')
            else:
                text = text.replace(substring, 'in the night')

    # At 3 o'clock in the afternoon
    for m in reg8.finditer(text):
        start = m.start()
        substring = m.group()
        idx_2 = substring.find('in')
        replacement = substring[idx_2:]
        text = text.replace(substring, replacement)

    # At 3 o'clock
    for m in reg9.finditer(text):
        start = m.start()
        substring = m.group()
        text = text.replace(substring, 'in the afternoon')

    # At 3.20 pm
    for m in reg10.finditer(text):
        start = m.start()
        substring = m.group()
        idx_space = substring.find(' ')
        number = int(substring[idx_space + 1])
        # number = extract_simple_hour(substring)
        if(am_or_pm(substring) == "am"):
            if(number < 4):
                text = text.replace(substring, 'in the night')
            elif(number < 11):
                text = text.replace(substring, 'in the morning')
            else:
                text = text.replace(substring, 'in the afternoon')
        else:
            if(number < 4):
                text = text.replace(substring, 'in the afternoon')
            elif(number < 9):
                text = text.replace(substring, 'in the evening')
            else:
                text = text.replace(substring, 'in the night')

    # on 20th June
    for m in reg11.finditer(text):
        start = m.start()
        substring = m.group()
        idx_space = substring.rfind(' ')
        replacement = substring[(idx_space + 1):]
        text = text.replace(substring, 'in ' + replacement)

    # on 20 June
    for m in reg12.finditer(text):
        start = m.start()
        substring = m.group()
        idx_space = substring.rfind(' ')
        replacement = substring[(idx_space + 1):]
        text = text.replace(substring, 'in ' + replacement)

    # on June 20th
    for m in reg13.finditer(text):
        start = m.start()
        substring = m.group()
        idx_space_1 = substring.find(' ')
        idx_space_2 = substring.rfind(' ')
        replacement = substring[(idx_space_1 + 1):idx_space_2]
        text = text.replace(substring, 'in ' + replacement)

    # on June 20
    for m in reg14.finditer(text):
        start = m.start()
        substring = m.group()
        idx_space_1 = substring.find(' ')
        idx_space_2 = substring.rfind(' ')
        replacement = substring[(idx_space_1 + 1):idx_space_2]
        text = text.replace(substring, 'in ' + replacement)

    # on June 2
    for m in reg15.finditer(text):
        start = m.start()
        substring = m.group()
        idx_space_1 = substring.find(' ')
        idx_space_2 = substring.rfind(' ')
        replacement = substring[(idx_space_1 + 1):idx_space_2]
        text = text.replace(substring, 'in ' + replacement)

    for m in reg16.finditer(text):
        start = m.start()
        substring = m.group()
        text = text.replace(substring, 'this week')

    return text

def tag(text):

    # Initialization
    timex_found = []

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
    # found = reg1.findall(text)
    # found = [a[0] for a in found if len(a) > 1]
    # for timex in found:
    #     timex_found.append(timex)

    # # Variations of this thursday, next year, etc
    # found = reg2.findall(text)
    # found = [a[0] for a in found if len(a) > 1]
    # for timex in found:
    #     timex_found.append(timex)
    #
    # # today, tomorrow, etc
    # found = reg3.findall(text)
    # for timex in found:
    #     timex_found.append(timex)
    #
    # # ISO
    # found = reg4.findall(text)
    # for timex in found:
    #     timex_found.append(timex)
    #
    # # Year
    # found = reg5.findall(text)
    # for timex in found:
    #     timex_found.append(timex)

    # Day
    found = reg6.findall(text)
    # print(found)
    for timex in found:
        # print(timex)
        # print(concatenate_tuple_to_str(timex))
        timex_found.append(concatenate_tuple_to_str(timex))

    # Hour
    found = reg7.findall(text)
    print('Private temporal phrases : ')
    print(str(found))
    for timex in found:
        timex_found.append(concatenate_tuple_to_str(timex))

    # Hour
    found = reg8.findall(text)
    for timex in found:
        timex_found.append(concatenate_tuple_to_str(timex))

    found = reg9.findall(text)
    for timex in found:
        timex_found.append(concatenate_tuple_to_str(timex))

    found = reg10.findall(text)
    print('Found, ' + str(found))
    for timex in found:
        timex_found.append(concatenate_tuple_to_str(timex))

    # Tag only temporal expressions which haven't been tagged.
    for timex in timex_found:
        text = re.sub(timex + '(?!</TIMEX2>)', '<TIMEX2>' + timex + '</TIMEX2>', text)

    # text = text.replace("<TIMEX2>at 3 pm</TIMEX2>", "in the afternoon")

    return text

# Hash function for week days to simplify the grounding task.
# [Mon..Sun] -> [0..6]
hashweekdays = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6}

# Hash function for months to simplify the grounding task.
# [Jan..Dec] -> [1..12]
hashmonths = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12}

# Hash number in words into the corresponding integer value
def hashnum(number):
    if re.match(r'one|^a\b', number, re.IGNORECASE):
        return 1
    if re.match(r'two', number, re.IGNORECASE):
        return 2
    if re.match(r'three', number, re.IGNORECASE):
        return 3
    if re.match(r'four', number, re.IGNORECASE):
        return 4
    if re.match(r'five', number, re.IGNORECASE):
        return 5
    if re.match(r'six', number, re.IGNORECASE):
        return 6
    if re.match(r'seven', number, re.IGNORECASE):
        return 7
    if re.match(r'eight', number, re.IGNORECASE):
        return 8
    if re.match(r'nine', number, re.IGNORECASE):
        return 9
    if re.match(r'ten', number, re.IGNORECASE):
        return 10
    if re.match(r'eleven', number, re.IGNORECASE):
        return 11
    if re.match(r'twelve', number, re.IGNORECASE):
        return 12
    if re.match(r'thirteen', number, re.IGNORECASE):
        return 13
    if re.match(r'fourteen', number, re.IGNORECASE):
        return 14
    if re.match(r'fifteen', number, re.IGNORECASE):
        return 15
    if re.match(r'sixteen', number, re.IGNORECASE):
        return 16
    if re.match(r'seventeen', number, re.IGNORECASE):
        return 17
    if re.match(r'eighteen', number, re.IGNORECASE):
        return 18
    if re.match(r'nineteen', number, re.IGNORECASE):
        return 19
    if re.match(r'twenty', number, re.IGNORECASE):
        return 20
    if re.match(r'thirty', number, re.IGNORECASE):
        return 30
    if re.match(r'forty', number, re.IGNORECASE):
        return 40
    if re.match(r'fifty', number, re.IGNORECASE):
        return 50
    if re.match(r'sixty', number, re.IGNORECASE):
        return 60
    if re.match(r'seventy', number, re.IGNORECASE):
        return 70
    if re.match(r'eighty', number, re.IGNORECASE):
        return 80
    if re.match(r'ninety', number, re.IGNORECASE):
        return 90
    if re.match(r'hundred', number, re.IGNORECASE):
        return 100
    if re.match(r'thousand', number, re.IGNORECASE):
      return 1000

# Given a timex_tagged_text and a Date object set to base_date,
# returns timex_grounded_text
def ground(tagged_text, base_date):

    # Find all identified timex and put them into a list
    timex_regex = re.compile(r'<TIMEX2>.*?</TIMEX2>', re.DOTALL)
    timex_found = timex_regex.findall(tagged_text)
    timex_found = map(lambda timex:re.sub(r'</?TIMEX2.*?>', '', timex), \
                timex_found)

    # Calculate the new date accordingly
    for timex in timex_found:
        timex_val = 'UNKNOWN' # Default value

        timex_ori = timex   # Backup original timex for later substitution

        # If numbers are given in words, hash them into corresponding numbers.
        # eg. twenty five days ago --> 25 days ago
        if re.search(numbers, timex, re.IGNORECASE):
            split_timex = re.split(r'\s(?=days?|months?|years?|weeks?)', \
                                                              timex, re.IGNORECASE)
            value = split_timex[0]
            unit = split_timex[1]
            num_list = map(lambda s:hashnum(s),re.findall(numbers + '+', \
                                          value, re.IGNORECASE))
            timex = `sum(num_list)` + ' ' + unit

        # If timex matches ISO format, remove 'time' and reorder 'date'
        if re.match(r'\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+', timex):
            dmy = re.split(r'\s', timex)[0]
            dmy = re.split(r'/|-', dmy)
            timex_val = str(dmy[2]) + '-' + str(dmy[1]) + '-' + str(dmy[0])

        # Specific dates
        elif re.match(r'\d{4}', timex):
            timex_val = str(timex)

        # Relative dates
        elif re.match(r'tonight|tonite|today', timex, re.IGNORECASE):
            timex_val = str(base_date)
        elif re.match(r'yesterday', timex, re.IGNORECASE):
            timex_val = str(base_date + RelativeDateTime(days=-1))
        elif re.match(r'tomorrow', timex, re.IGNORECASE):
            timex_val = str(base_date + RelativeDateTime(days=+1))

        # Weekday in the previous week.
        elif re.match(r'last ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays[timex.split()[1]]
            timex_val = str(base_date + RelativeDateTime(weeks=-1, \
                            weekday=(day,0)))

        # Weekday in the current week.
        elif re.match(r'this ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays[timex.split()[1]]
            timex_val = str(base_date + RelativeDateTime(weeks=0, \
                            weekday=(day,0)))

        # Weekday in the following week.
        elif re.match(r'next ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays[timex.split()[1]]
            timex_val = str(base_date + RelativeDateTime(weeks=+1, \
                              weekday=(day,0)))

        # Last, this, next week.
        elif re.match(r'last week', timex, re.IGNORECASE):
            year = (base_date + RelativeDateTime(weeks=-1)).year

            # iso_week returns a triple (year, week, day) hence, retrieve
            # only week value.
            week = (base_date + RelativeDateTime(weeks=-1)).iso_week[1]
            timex_val = str(year) + 'W' + str(week)
        elif re.match(r'this week', timex, re.IGNORECASE):
            year = (base_date + RelativeDateTime(weeks=0)).year
            week = (base_date + RelativeDateTime(weeks=0)).iso_week[1]
            timex_val = str(year) + 'W' + str(week)
        elif re.match(r'next week', timex, re.IGNORECASE):
            year = (base_date + RelativeDateTime(weeks=+1)).year
            week = (base_date + RelativeDateTime(weeks=+1)).iso_week[1]
            timex_val = str(year) + 'W' + str(week)

        # Month in the previous year.
        elif re.match(r'last ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year - 1) + '-' + str(month)

        # Month in the current year.
        elif re.match(r'this ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year) + '-' + str(month)

        # Month in the following year.
        elif re.match(r'next ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year + 1) + '-' + str(month)
        elif re.match(r'last month', timex, re.IGNORECASE):

            # Handles the year boundary.
            if base_date.month == 1:
                timex_val = str(base_date.year - 1) + '-' + '12'
            else:
                timex_val = str(base_date.year) + '-' + str(base_date.month - 1)
        elif re.match(r'this month', timex, re.IGNORECASE):
                timex_val = str(base_date.year) + '-' + str(base_date.month)
        elif re.match(r'next month', timex, re.IGNORECASE):

            # Handles the year boundary.
            if base_date.month == 12:
                timex_val = str(base_date.year + 1) + '-' + '1'
            else:
                timex_val = str(base_date.year) + '-' + str(base_date.month + 1)
        elif re.match(r'last year', timex, re.IGNORECASE):
            timex_val = str(base_date.year - 1)
        elif re.match(r'this year', timex, re.IGNORECASE):
            timex_val = str(base_date.year)
        elif re.match(r'next year', timex, re.IGNORECASE):
            timex_val = str(base_date.year + 1)
        elif re.match(r'\d+ days? (ago|earlier|before)', timex, re.IGNORECASE):

            # Calculate the offset by taking '\d+' part from the timex.
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date + RelativeDateTime(days=-offset))
        elif re.match(r'\d+ days? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date + RelativeDateTime(days=+offset))
        elif re.match(r'\d+ weeks? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            year = (base_date + RelativeDateTime(weeks=-offset)).year
            week = (base_date + \
                            RelativeDateTime(weeks=-offset)).iso_week[1]
            timex_val = str(year) + 'W' + str(week)
        elif re.match(r'\d+ weeks? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            year = (base_date + RelativeDateTime(weeks=+offset)).year
            week = (base_date + RelativeDateTime(weeks=+offset)).iso_week[1]
            timex_val = str(year) + 'W' + str(week)
        elif re.match(r'\d+ months? (ago|earlier|before)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])

            # Checks if subtracting the remainder of (offset / 12) to the base month
            # crosses the year boundary.
            if (base_date.month - offset % 12) < 1:
                extra = 1

            # Calculate new values for the year and the month.
            year = str(base_date.year - offset // 12 - extra)
            month = str((base_date.month - offset % 12) % 12)

            # Fix for the special case.
            if month == '0':
                month = '12'
            timex_val = year + '-' + month
        elif re.match(r'\d+ months? (later|after)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])
            if (base_date.month + offset % 12) > 12:
                extra = 1
            year = str(base_date.year + offset // 12 + extra)
            month = str((base_date.month + offset % 12) % 12)
            if month == '0':
                month = '12'
            timex_val = year + '-' + month
        elif re.match(r'\d+ years? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date.year - offset)
        elif re.match(r'\d+ years? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date.year + offset)

        # Remove 'time' from timex_val.
        # For example, If timex_val = 2000-02-20 12:23:34.45, then
        # timex_val = 2000-02-20
        timex_val = re.sub(r'\s.*', '', timex_val)

        # Substitute tag+timex in the text with grounded tag+timex.
        tagged_text = re.sub('<TIME>' + timex_ori + '</TIME>', '<TIME val=\"' \
            + timex_val + '\">' + timex_ori + '</TIME>', tagged_text)

    return tagged_text

####

def demo():
    text = nltk.corpus.abc.raw('rural.txt')[:10000]
    print tag(text)

def do_temporal_tag(text):
    return tag_2(text)

if __name__ == '__main__':
    # demo2(sys.argv[1])
    # print(do_temporal_tag(sys.argv[1]))
    do_temporal_tag(sys.argv[1])
