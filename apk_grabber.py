#!/usr/bin/env python
# coding=utf-8
"""
Grab apks
"""

import argparse
import os
import re
import subprocess
import sys


OUTPUT_BASE_DIR = "cache"

def execute(cmd):
    print "running shell command:\n    " + cmd
    try:
        return subprocess.check_output(cmd, shell=True).strip()
    except subprocess.CalledProcessError, e:
        print "Error output:\n    ", e.output
        raise e

def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="apk grabber!", parents=())
    parser.add_argument('patterns', metavar='pattern', type=str, nargs='+',
                   help='pattern(s) to match package names on the device')
    args = parser.parse_args()

    print args.patterns


    # grab them from device
    packages = execute("adb shell pm list packages".format(**locals()))
    # print packages
    
    matching_packages = []

    print "now matching packages to {args.patterns}".format(**locals())

    # for each pattern, grep the name and store in a big list
    for pattern in args.patterns:
        for line in packages.splitlines():
            if re.search(pattern, line):
                matching_packages.append(line.split(':')[1])

    print "found the following packages on the device:"
    print matching_packages


    for matching_package in matching_packages:
        apk_path = execute("adb shell pm path {matching_package}".format(**locals())).split(':')[1]
        output_apk_path = os.path.join(OUTPUT_BASE_DIR, matching_package) + ".apk"
        execute("adb pull {apk_path} {output_apk_path}".format(**locals()))


    # download dex2jar


    # decompile dexes


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


