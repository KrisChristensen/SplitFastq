##########################################################
### Import Necessary Modules

import argparse                       #provides options at the command line
import sys                       #take command line arguments and uses it in the script
import gzip                       #allows gzipped files to be read
import re                       #allows regular expressions to be used
import os                       #allows file to be removed

##########################################################
### Command-line Arguments
parser = argparse.ArgumentParser(description="A script to split a fastq file into X number of files, will overwrite any existing files with the same names")
parser.add_argument("-fastq", help = "The location of the fastq file (can be compressed)", default=sys.stdin, required=True)
parser.add_argument("-out", help = "The output prefix, default=out", default="out")
parser.add_argument("-files", help = "The number of files to split sequences, default=2", default=2)
parser.add_argument("-load", help = "The number of sequences to load before outputting to file, default=1000", default=1000)
parser.add_argument("-overwrite", help = "overwrite existing files, default=no, option=yes", default="no")
args = parser.parse_args()

class OpenFile():
    ### Opens the file either using a regular mechanism or opens it after uncompressing the data
    def __init__ (self, cb, t):
        """Opens a file (gzipped accepted)"""
        if re.search(".gz$", cb):
            self.filename = gzip.open(cb, 'rb')
        else:
            self.filename = open(cb, 'r')
        if t == "fastq":
            FastqFile(self.filename)

class FastqFile():
    def __init__ (self, f):
        """Removes sequences from the fasta file"""
        self.filename = f
        self.number_seqs = 1
        self.seq = []
        self.fileNum = 1
        self.lineCount = 0
        self.beginning = {}
        for line in self.filename:
            try:
                line = line.decode('utf-8')
            except:
                pass            
            line = line.rstrip('\n')
            if re.search("^\@", line) and self.lineCount == 4:
                if int(self.number_seqs) % int(args.load) == 0 and self.number_seqs >= int(args.load):
                    sys.stderr.write("\tRead #{} sequences\n".format(self.number_seqs))
                    output = open("{}.{}.fastq".format(args.out, self.fileNum), 'a')
                    if "{}.{}.fastq".format(args.out, self.fileNum) in self.beginning:
                        output.write("\n{}".format("\n".join(self.seq)))
                    else:
                        output.write("{}".format("\n".join(self.seq)))
                        self.beginning["{}.{}.fastq".format(args.out, self.fileNum)] = 1
                    output.close()        
                    del self.seq[:]
                    self.fileNum += 1
                    if self.fileNum > int(args.files):
                        self.fileNum = 1
                self.number_seqs += 1
                self.lineCount = 0
            self.lineCount += 1
            self.seq.append(line)
        output = open("{}.{}.fastq".format(args.out, self.fileNum), 'a')
        if "{}.{}.fastq".format(args.out, self.fileNum) in self.beginning:
            output.write("\n{}".format("\n".join(self.seq)))
        else:
            output.write("{}".format("\n".join(self.seq)))
        output.close() 
        del self.seq[:]
        sys.stderr.write("Found {} sequences and attempted to split into {} files\n\n".format(self.number_seqs, args.files))
        self.filename.close()


if __name__ == '__main__':
    count = 1
    while (count <= int(args.files)):
        if args.overwrite == "yes":
            try:
                output = open("{}.{}.fastq".format(args.out, count), 'r')
                sys.stderr.write("\tFound file: {} Overwriting\n".format("{}.{}.fastq".format(args.out, count)))
                os.remove("{}.{}.fastq".format(args.out, count))
                output.close
            except IOError:
                pass
        else:
            try:
                output = open("{}.{}.fastq".format(args.out, count), 'r')
                output.close()
                sys.stderr.write("\n{}.{}.fastq exists already, will not overwrite, please select overwriting in options or change output name\n\n".format(args.out, count))
                quit()
            except IOError:
                pass
        count += 1
    open_file2 = OpenFile(args.fastq, "fastq")
