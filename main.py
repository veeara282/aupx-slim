import argparse
import sqlite3

from collections import namedtuple


# Sample format IDs as defined in Audacity's SampleFormat.h
undefinedSample = 0
int16Sample = 0x00020001
int24Sample = 0x00040001
floatSample = 0x0004000F

# Length of each sample in bytes. Use a placeholder value of 1 byte for undefinedSample
sample_length_bytes = {
    int16Sample: 2,
    int24Sample: 3,
    floatSample: 4,
    undefinedSample: 1,
}

SampleBlock = namedtuple(
    "SampleBlock",
    field_names=["blockid", "sampleformat", "length_bytes", "num_samples"]
)


class AUP3ProjectWrapper:
    def __init__(self, filename):
        # .aup3 is an SQLite3 database
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def list_silent_blocks(self):
        self.cursor.execute(
            "select blockid, sampleformat, length(samples) from sampleblocks where summin = 0 and summax = 0"
        )
        # Each row: (block id, sample format id, length in bytes)
        raw_result_set = self.cursor.fetchall()

        block_lengths = [
            SampleBlock(
                blockid,
                sampleformat,
                length,
                length // sample_length_bytes[sampleformat],
            )
            for (blockid, sampleformat, length) in raw_result_set
        ]

        return block_lengths


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    return parser.parse_args()


def main():
    args = get_args()
    filename = args.filename

    project = AUP3ProjectWrapper(filename)
    silent_blocks = project.list_silent_blocks()

    for block in silent_blocks[:10]:
        print(block)


if __name__ == "__main__":
    main()
