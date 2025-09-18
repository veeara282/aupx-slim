import argparse
import sqlite3


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    return parser.parse_args()

def main():
    args = get_args()
    filename = args.filename

    # .aup3 is an SQLite3 database
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()


if __name__ == "__main__":
    main()
