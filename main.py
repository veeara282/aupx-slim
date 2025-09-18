import argparse
import sqlite3


# Sample format IDs as defined in Audacity's SampleFormat.h
undefinedSample = 0
int16Sample = 0x00020001
int24Sample = 0x00040001
floatSample = 0x0004000F


class AUP3ProjectWrapper:
    def __init__(self, filename):
        # .aup3 is an SQLite3 database
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()
    
    def __del__(self):
        self.conn.close()
    
    def list_silent_blocks(self):
        self.cursor.execute(
            "select * from sampleblocks where summin = 0 and summax = 0"
            )
        rows = self.cursor.fetchall()
        return rows

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    return parser.parse_args()

def main():
    args = get_args()
    filename = args.filename

    project = AUP3ProjectWrapper(filename)


if __name__ == "__main__":
    main()
