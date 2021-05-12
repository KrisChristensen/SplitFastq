# SplitFastq
A script to split a fastq file (can be compressed) into a chosen number of files.

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

This script has been tested with Python 2.7 and 3 and should work with either.
The script requires a fastq file.  The fastq file can be compressed with gzip.

<!-- usage -->
## Usage

python SplitFastqFile.v1.0.py -fastq file.fastq -out prefix -files 2 -load 1000 -overwrite yes

To see the usage and get futher information: python SplitFastqFile.v1.0.py -h

<!-- license -->
## License 

Distributed under the MIT License.
