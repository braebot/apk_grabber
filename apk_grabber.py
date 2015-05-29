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
import urllib
import zipfile

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
    parser.add_argument('--output_dir', dest='output', action='store', default='output',
        help="output directory of the apk and jar files")
    args = parser.parse_args()

    print args.patterns


    # grab them from device
    packages = execute("adb shell pm list packages".format(**locals()))
    # print packages
    
    matching_packages = []

    print "matching packages to {args.patterns}".format(**locals())

    # for each pattern, grep the name and store in a big list
    for pattern in args.patterns:
        for line in packages.splitlines():
            if re.search(pattern, line):
                matching_packages.append(line.split(':')[1])

    print "matched these packages on the device:" + str(matching_packages)


    for matching_package in matching_packages:
        # find path to apk
        apk_path = execute("adb shell pm path {matching_package}".format(**locals())).split(':')[1]
        apk_base_file_name = os.path.join(args.output, matching_package)
        output_apk_path = apk_base_file_name + ".apk"

        # pull apk off device
        execute("adb pull {apk_path} {output_apk_path}".format(**locals()))

        # unzip apk contents (gets everything but dex)
        execute("rm -rf {apk_base_file_name}".format(**locals()))
        execute("mkdir {apk_base_file_name}".format(**locals()))
        execute("unzip -x {output_apk_path} -d {apk_base_file_name}".format(**locals()))

        output_jar_path = os.path.join(apk_base_file_name, "classes") + ".jar"
        # decompile apk into jar file
        execute("dex2jar-2.0/d2j-dex2jar.sh -f -o {output_jar_path} {output_apk_path}".format(**locals()))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


