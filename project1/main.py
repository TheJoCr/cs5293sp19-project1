# Main file which supports all of the orchestration and handling
# user input.
import glob
import argparse
import os
import os.path
from project1 import nouns, concepts

def obfuscate_text(args, text):
    """
    Handles logic for the actual obfuscation of
    a block of text, finding everything that needs
    to be obfuscated and then replacing it with
    the full block character. Returns stats about
    what got removed.
    """
    redact = []
    stats = {}
    if args.names:
        names = nouns.mark_names(text)
        stats['names'] = len(names)
        redact += names
    if args.genders:
        genders = nouns.mark_genders(text)
        stats['genders'] = len(genders)
        redact += genders
    if args.dates:
        dates = nouns.mark_dates(text)
        stats['dates'] = len(dates)
        redact += dates
    if args.addresses:
        addresses = nouns.mark_addresses(text)
        stats['addresses'] = len(addresses)
        redact += addresses
    if args.phones:
        phones = nouns.mark_phones(text)
        stats['phones'] = len(phones)
        redact += phones
    for c in args.concept:
        r = concepts.mark_concept_sentences(text, c)
        stats[c] = len(r)
        redact += r
    # Copy text into a mutable buffer:
    text = list(text)
    for start, end in redact:
        for i in range(start, end):
            text[i] = '\u2588'
    return ''.join(text), stats

def obfuscate_file(args, f, output_dir):
    """
    Obfuscates the file at f per args and stores
    the result in output_dir.
    """
    with open(f, 'r') as input_file:
        text = input_file.read()
    ob_text, stats = obfuscate_text(args, text)
    file_name = os.path.basename(f) + '.redacted'
    output_file_path = output_dir + '/' + file_name
    with open(output_file_path, 'w') as output_file:
        output_file.write(ob_text)
    return stats

def print_stats(args, stats):
    potential_keys = ['names', 'genders', 'dates', 'addresses', 'phones']
    keys = []
    for key in potential_keys:
        if getattr(args, key):
            keys.append(key)
    keys += args.concept
    total = {}
    for k in keys:
        total[k] = sum( [file_stats[k] for file_stats in stats.values()] )
    with open(args.stats, 'w') as stats_file:
        stats_file.write("Obfuscation stats\n")
        stats_file.write("Overall stats:\n")
        for k in keys:
            stats_file.write("\t%s: %d\n" % (k, total[k]))
        for in_file in stats.keys():
            stats_file.write("For file %s\n" % in_file)
            for k in keys:
                stats_file.write("\t%s: %d\n" % (k, stats[in_file][k]))

def execute(args):
    input_files = [f for input_glob in args.input for f in glob.glob(input_glob)]
    if len(input_files) == 0:
        print("No input files found! Exiting...")
        exit(1)
    # setup_stats(args.stats)
    output_dir = args.output
    # Try to make the dir if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    stats = {}
    for f in input_files:
        stats[f] = obfuscate_file(args, f, output_dir)
    print_stats(args, stats)

parser = argparse.ArgumentParser(
    description='Obfuscate files on specified fields and store to output'
)
# Input and Output
parser.add_argument('--input', action='append', required=True)
parser.add_argument('--output', default='out')
parser.add_argument('--stats', default='stderr')
# 'Nouns' to redact
parser.add_argument('--names', action='store_true')
parser.add_argument('--genders', action='store_true')
parser.add_argument('--dates', action='store_true')
parser.add_argument('--addresses', action='store_true')
parser.add_argument('--phones', action='store_true')
# 'Concepts' to redact
parser.add_argument('--concept', action='append', default=[])

def main():
    """
    Executes the program, parsing args, locating input files,
    running the obfuscation logic, and printing out stats.
    """
    # parse args
    args = parser.parse_args()
    execute(args)

if __name__ == "__main__":
    main()

