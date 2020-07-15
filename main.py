#!/usr/bin/python3

import template
from argparse import ArgumentParser
from csv import reader as csvreader
from time import time
from sys import stderr, exit
from os import path, makedirs
from mimetypes import guess_type

def cli_args():
    parser = ArgumentParser()

    # Positional arguments
    parser.add_argument("csvfile", help="CSV file to use to create the fake files", type=str)

    # Optional arguments
    parser.add_argument("--use-memory", help="load the templates into the memory, allowing a faster treatment.", action='store_true')
    parser.add_argument("--template-folder", help="folder where the templates are stored", type=str, default="templates")
    parser.add_argument("-o", "--output", help="output folder", type=str, default="output")

    parser.add_argument("--csv-delimiter", help="delimiter used in the CSV file", type=str, default=";")
    parser.add_argument("--csv-quote-char", help="quote character used in the CSV file", type=str, default='"')

    return parser

def perf_counter(start_time: float) -> str:
    current_time = time()
    if current_time < start_time:
        raise Exception("start_time ({start_time}) should not be higher than the current time ({current_time})")
    delta = current_time - start_time

    if delta < 1:
        return "0s"

    delta_d = {
        "d" : int(delta // (60 * 60 * 24)),
        "h" : int(delta // (60 * 60)),
        "m" : int(delta // 60),
        "s" : int(delta % 60)
    }

    return "".join("{value}{fmt}".format(value, fmt) for fmt, value in delta_d.items() if value != 0)

def number_of_lines(filename):
    with open(filename, "r") as f:
        return sum(1 for row in f)

def templatize_csv_line_by_line(csvfile: str, templates: template.Templates, output_directory: str, csv_delimiter = ";", csv_quote_char = '"', verbose = True):
    # list of output path we created
    # used to reduce the number of io calls
    output_path_checked = []

    stats = {
        "total"   : 0,
        "success" : 0,
        "lines" : number_of_lines(csvfile), # TODO put a flag to disable it
        "checkpoint_value" : 10000, # verify every X runs at which point we are.
        "auto_increase_checkpoint" : False
    }
    if verbose:
        print("[0s] Starting to create the files - "+str(stats['lines'])+" lines to check")
    start_time = time()

    with open(csvfile, newline='') as f:
        csv_content = csvreader(f, delimiter=csv_delimiter, quotechar=csv_quote_char)
        for line in csv_content:
            if len(line) == 0:
                continue

            # increase the stats
            stats["total"]+=1
            if stats["total"] % stats["checkpoint_value"] == 0:
                if stats['auto_increase_checkpoint']:
                    stats["checkpoint_value"] = 10 ** (len(str(stats["total"])) - 1 )

                if verbose:
                    print("[{delay}] Doing... {done} / {total} [{done_percent:.0f}%] (success : {done_success}, failed : {done_failed})".format(
                        delay = perf_counter(start_time),
                        done = stats['total'],
                        total = stats['lines'],
                        done_percent = 100*stats['total']/stats['lines'],
                        done_success = stats['success'],
                        done_failed = stats['total'] - stats['success']
                    ))

            filename = line[0]
            mimetype_encoding = guess_type(filename) if (len(line) < 2 or len(line[1].strip()) == 0) else (line[1], None)
            template_subfolder = None if len(line) < 3 else line[2]

            destination = path.join(output_directory, filename)
            destination_folder = path.split(destination)[0]

            # verify if the destination folder exists; if it has not, force the creation and remember it
            if destination_folder not in output_path_checked:
                makedirs(destination_folder, exist_ok=True)
                output_path_checked.append(destination_folder)

            templates.write_random_template_to(destination, mimetype_encoding, template_subfolder)
            stats['success']+=1
    if verbose:
        print("DONE ! {done_success} / {done} done without errors ( {done_failed} failed )".format(
            done = stats['total'],
            done_success = stats['success'],
            done_failed = stats['total'] - stats['success']
        ))

    return (stats['success'], stats['total'] - stats['success'])

if __name__ == "__main__" :
    args = cli_args().parse_args()

    LOAD_FILES_INTO_MEMORY = args.use_memory
    TEMPLATE_DIRECTORY = args.template_folder
    OUTPUT_DIRECTORY = args.output
    INPUT_CSV_FILE = args.csvfile
    CSV_DELIMITER  = args.csv_delimiter
    CSV_QUOTE_CHAR = args.csv_quote_char

    if not path.exists(INPUT_CSV_FILE):
      raise FileNotFoundError("the csv file '"+ INPUT_CSV_FILE + "' does not exists")

    templates = template.Templates(TEMPLATE_DIRECTORY, LOAD_FILES_INTO_MEMORY)
    done_success, done_failed = templatize_csv_line_by_line(INPUT_CSV_FILE, templates, OUTPUT_DIRECTORY, CSV_DELIMITER, CSV_QUOTE_CHAR)

    if done_failed > 0:
        if done_success == 0:
            exit(1)
        else:
            exit(2)
    exit(0)
