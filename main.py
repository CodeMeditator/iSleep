import re
import argparse
import os


GITHUB_README_COMMENTS = (
    "(<!--START_SECTION:{name}-->\n)(.*)(<!--END_SECTION:{name}-->\n)"
)
SLEEP_HEAD = "| Time | \n | ---- | ---- | \n"
SLEEP_STAT_TEMPLATE = "| {time} |\n"
OUT_FOLDER = os.path.join(os.getcwd(), "files")


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


def parse_ios_str_to_list(list_str):
    l = list_str.splitlines()
    # filter the empty value
    return [i for i in l if i]


def make_summary_str(time_list):
    s = SLEEP_HEAD
    for t in time_list:
        s += SLEEP_STAT_TEMPLATE.format(time=t)
    return s


def main(time_list_str):
    time_list = parse_ios_str_to_list(time_list_str)

    s = make_summary_str(time_list)
    replace_readme_comments("README.md", s, "my_sleep")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("time_list_str", help="time_list_str")
    options = parser.parse_args()
    main(options.time_list_str)
