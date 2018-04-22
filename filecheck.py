# -*- coding: iso-8859-1 -*-
"""Report or replace non-ascii characters and tabs in python files.

Usage::

    python filecheck.py -f yourfile.py [-o youroutput.py]
"""

from __future__ import print_function

import os
import sys
from optparse import OptionParser

try:
    import wx         # try to import wx
except ImportError:
    wx = None         # wx is not available


def report(datastring):                                 # pylint: disable=R0912
    """ Report only on long lines, non-ascii's, and tabs.
    """
    lines = datastring.splitlines()
    tabs, nonasciis, lengths = [], [], []

    # check every line and save for report
    for i in xrange(len(lines)):
        if "\t" in lines[i]:
            tabs.append(i + 1)

        count = 0
        for s in lines[i]:
            if ord(s) > 127:
                count += 1                     # utf-8 chars are counted twice

        if count != 0:
            nonasciis.append([i + 1, count])

        # Check if lines are not too long:
        if len(lines[i]) > 80:
            lengths.append(i + 1)

    # report results:
    if len(tabs) > 0:
        print("TAB's found in lines:")
        for line in tabs:
            print("line ", line)

    if len(nonasciis) > 0:
        print("non-ascii characters in lines:")
        for line in nonasciis:
            print("line ", line[0], " counts:", line[1])

    if len(lengths) > 0:
        print("lines too long:")
        for line in lengths:
            print("line ", line)

    if len(tabs) + len(nonasciis) + len(lengths) == 0:
        print("Nothing found.")


def replace(datastring):
    """ Replace non-ascii's and tabs. Report on long lines.
    """
    # possibly incomlete, add lines if necessary
    datastring = datastring.replace("\xe4", "ae")  # replace typical non-ascii
    datastring = datastring.replace("\xc4", "Ae")  # iso-8859-1
    datastring = datastring.replace("\xf6", "oe")
    datastring = datastring.replace("\xd6", "Oe")
    datastring = datastring.replace("\xfc", "ue")
    datastring = datastring.replace("\xdc", "Ue")
    datastring = datastring.replace("\xdf", "ss")

    datastring = datastring.replace("\xc3\xa4", "ae")  # utf-8
    datastring = datastring.replace("\xc3\x84", "Ae")
    datastring = datastring.replace("\xc3\xb6", "oe")
    datastring = datastring.replace("\xc3\x96", "Oe")
    datastring = datastring.replace("\xc3\xbc", "ue")
    datastring = datastring.replace("\xc3\x9c", "Ue")
    datastring = datastring.replace("\xc3\x9f", "ss")

    datastring = datastring.replace("^\xdf", "ue")
    datastring = datastring.replace("^\xda", "oe")

    datastring = datastring.replace("\t", "    ")  # replace tab's

    for i in xrange(len(datastring)):              # search for non-ascii chars
        if ord(datastring[i]) > 127:               # non-ascii = index > 127
            datastring = datastring.replace(datastring[i], "@")
            print("unknown character replaced with '@'")

    # check line length and remove trailing whitespaces
    lines = datastring.splitlines()
    lengths = []

    for i in xrange(len(lines)):
        lines[i] = lines[i].rstrip()
        if len(lines[i]) > 80:
            lengths.append(i + 1)

    print(lines)
    datastring = lines.join(lines, "\n")

    if len(lengths) > 0:
        print("lines too long:")
        for line in lengths:
            print("line ", line)

    return datastring


def main():
    """ Main routine: reads parameters from the command line
        or by using wx-dialogs
    """
    # parse any command line options
    parser = OptionParser()
    parser.add_option("-f", "--file", action="store",
                      type="string", default=None,
                      dest="inputfile", metavar="filename.py",
                      help="file to be checked")

    parser.add_option("-o", "--output", action="store",
                      type="string", default=None,
                      dest="outputfile", metavar="filename_replaced.py",
                      help="file to save changes (optional)")

    (options, _args) = parser.parse_args()

    # if no arguments were given try wx.FileDialogs to select them
    if options.inputfile is None and wx is not None:
        app = wx.PySimpleApp()                          # pylint: disable=W0612
        dlg = wx.FileDialog(None, message="Open file to check...",
                            defaultDir=os.getcwd(), defaultFile="",
                            wildcard="Python source (*.py)|*.py",
                            style=wx.OPEN)
        status = dlg.ShowModal()
        if status == wx.ID_OK:                  # proceed if "open" was pressed
            options.inputfile = dlg.GetPath()
            dlg.Destroy()
            dlg = wx.FileDialog(None, message="Save modifications in file...",
                                defaultDir=os.getcwd(), defaultFile="",
                                wildcard="Python source (*.py)|*.py",
                                style=wx.SAVE)
            status = dlg.ShowModal()
            if status == wx.ID_OK:               # "save" button pressed?
                options.outputfile = dlg.GetPath()
        dlg.Destroy()

    if options.inputfile is None:                # input filename is required
        parser.print_help()
        sys.exit(1)

    fsrc = file(options.inputfile, 'r')          # open source for reading
    contents = fsrc.read()                       # read the whole source file
    fsrc.close()                                 # close file

    if options.outputfile is None:
        report(contents)                         # only report

    else:
        contents = replace(contents)             # change data

        if os.path.exists(options.outputfile):
            try:
                os.remove(options.outputfile + "~")
            except OSError:
                pass
            os.rename(options.outputfile, options.outputfile + "~")

        fdst = file(options.outputfile, 'w')     # open destination for writing
        fdst.write(contents)                     # write new file
        fdst.close()                             # close file
    raw_input("Press <ENTER>!")                  # keep terminal open (windows)


if __name__ == "__main__":
    main()
