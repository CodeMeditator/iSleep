import re
import argparse
import os
from datetime import datetime, timedelta

GITHUB_README_COMMENTS = (
    "(<!--START_SECTION:{name}-->\n)(.*)(<!--END_SECTION:{name}-->\n)"
)
SLEEP_HEAD = "| Start Time | End Time |\n| ---- | ---- |\n"
SLEEP_STAT_TEMPLATE = "| {start_time} | {end_time} |\n"
OUT_FOLDER = os.path.join(os.getcwd(), "files")
DATE_FORMAT = "%b %d, %Y at %H:%M"


def replace_readme_comments(file_name, comment_str, comments_name):
    with open(file_name, "r+") as f:
        text = f.read()
        # regrex sub from github readme comments
        text = re.sub(
            GITHUB_README_COMMENTS.format(name=comments_name),
            r"\1{}\n\3".format(comment_str),
            text,
            flags=re.DOTALL,
        )
        f.seek(0)
        f.write(text)
        f.truncate()


def classify_date(date_obj):
    """
    start time: 18:00 ~ 6:00
    end time: 00:00 ~ 12:00
    241101 23:55 in list(241102)
    """
    if date_obj.hour > 18:
        return date_obj.date() + timedelta(days=1)
    else:
        return date_obj.date()


def parse_ios_str_to_list(list_str, is_start_time):
    date_list = list_str.splitlines()

    date_list = [datetime.strptime(date_str, DATE_FORMAT)
                 for date_str in date_list]

    classified_dates = {}
    for date_obj in date_list:
        classified_date = classify_date(date_obj)
        if classified_date not in classified_dates:
            classified_dates[classified_date] = []
        classified_dates[classified_date].append(date_obj)

    result_lists = list(classified_dates.values())

    if is_start_time:
        start_time_list = [time.strftime(DATE_FORMAT) for time in sorted(
            {min(sublist) for sublist in result_lists}, reverse=True)]
        return start_time_list[:-1]
    else:
        end_time_list = [time.strftime(DATE_FORMAT) for time in sorted(
            {max(sublist) for sublist in result_lists}, reverse=True)]
        return end_time_list[:-1]


def make_summary_str(start_time_list, end_time_list):
    s = SLEEP_HEAD
    for st, et in zip(start_time_list, end_time_list):
        s += SLEEP_STAT_TEMPLATE.format(start_time=st, end_time=et)
    return s


def main(start_time_list_str, end_time_list_str):
    start_time_list = parse_ios_str_to_list(
        start_time_list_str, True)
    end_time_list = parse_ios_str_to_list(end_time_list_str, False)

    s = make_summary_str(start_time_list, end_time_list)
    replace_readme_comments("README.md", s, "my_sleep")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start_time_list_str", help="start_time_list_str")
    parser.add_argument("end_time_list_str", help="end_time_list_str")
    options = parser.parse_args()
    main(options.start_time_list_str, options.end_time_list_str)
