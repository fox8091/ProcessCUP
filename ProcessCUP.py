#!/usr/bin/env python3

__author__ = "fox8091"
__version__ = "1.0.0"

import os
import sys
import argparse

from pyctr.type.cci import CCIReader, CCISection, InvalidCCIError
from pyctr.type.cia import CIAReader

def parseUpdateSection(cci: 'CCIReader', cup_dir, isN3DS: bool):
    content = os.path.join(cup_dir, os.path.join(cci.media_id, "content6" if isN3DS else "content7"))
    os.makedirs(content, exist_ok=True)
    section = CCISection.UpdateNew3DS if isN3DS else CCISection.UpdateOld3DS
    romfs = cci.contents[section].romfs
    for f in romfs.get_info_from_path('/SNAKE' if isN3DS else '/').contents:
        with open(os.path.join(content, f), 'wb') as g:
            g.write(romfs.open(('/SNAKE/' if isN3DS else '/') + f).read())

def writeCSV(cci: 'CCIReader', csv: str, isN3DS: bool):
    os.makedirs(csv, exist_ok=True)
    with open(os.path.join(csv, str(cci.media_id).upper() + ("_N3DS_CUP.csv" if isN3DS else "_CUP.csv")), "w") as f:
        f.write("TitleID,Region,Title versions,Update versions")
    section = CCISection.UpdateNew3DS if isN3DS else CCISection.UpdateOld3DS
    romfs = cci.contents[section].romfs
    for f in romfs.get_info_from_path('/SNAKE' if isN3DS else '/').contents:
        if ".cia" in f:
            cia = CIAReader(romfs.open(('/SNAKE/' if isN3DS else '/') + f))
            with open(os.path.join(csv, cci.media_id + ("_N3DS_CUP.csv" if isN3DS else "_CUP.csv")), "a") as g:
                g.write("\n" + str(str(cia.tmd.title_id).upper() + "," + cci.cart_region.value +",v" + str(int(cia.tmd.title_version)) + "," + str(cci.media_id).upper() + ("_N3DS_CUP" if isN3DS else "_CUP")))

def parseCCI(file, csv_dir, cup_dir):
    cci = CCIReader(file)
    app = cci.contents[CCISection.Application]
    print(app.exefs.icon.get_app_title('English').short_desc)
    print('TitleID: ' + cci.media_id)
    
    print("Updates:")
    if CCISection.UpdateOld3DS in cci.contents.keys():
        print("\t✅ Has O3DS Update")
        if cup_dir is not None:
            parseUpdateSection(cci, cup_dir, False)
        if csv_dir is not None:
            writeCSV(cci, csv_dir, False)
    else:
        print("\t❌ Has O3DS Update")

    if CCISection.UpdateNew3DS in cci.contents.keys():
        print("\t✅ Has N3DS Update")
        if cup_dir is not None:
            parseUpdateSection(cci, cup_dir, True)
        if csv_dir is not None:
            writeCSV(cci, csv_dir, True)
    else:
        print("\t❌ Has N3DS Update")
    print('')

def parseDirectory(path, csv_dir, cup_dir):
    for root, dir, files in os.walk(path):
        for filename in files:
            try:
                parseCCI(os.path.join(root,filename), csv_dir, cup_dir)
            except InvalidCCIError:
                pass

def is_path(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid file or directory")

def main():
    parser = argparse.ArgumentParser(description="Processes 3DS CUPs from cartridge dumps")
    parser.add_argument("path", help="Path to either a 3DS cartridge dump or directory of cartridge dumps", type=is_path)
    parser.add_argument("--cupdir", help="Path to output CUPs", nargs='?', default=None)
    parser.add_argument("--csvdir", help="Path to output CSVs", nargs='?', default=None)
    args = parser.parse_args(args=sys.argv[1:] or ['--help'])

    if os.path.isdir(args.path):
        parseDirectory(args.path, args.csvdir, args.cupdir)
    else:
        parseCCI(args.path, args.csvdir, args.cupdir)

        
if __name__ == "__main__":
    main()