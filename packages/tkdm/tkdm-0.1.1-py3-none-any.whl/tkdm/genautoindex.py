#!/usr/bin/env python3
# kdm9: This was originally taken from a gist, licensed under the Apache
# license There are so many pasted copies of the original, none of which have
# the author listed, so I'm not entirely sure who originally made it.
# Regardless, I've pretty much re-written the whole thing
# Copyright (c) 2022 Dr. K. D. Murray/Gekkonid Consulting <spam@gekkonid.com>

#  Recursively generate index.html files for
#  all subdirectories in a directory tree

import argparse
import fnmatch
import os
import sys
from .util import ask_yesno


index_file_name = 'index.html'

CSS = """<style>
body {
    background: #f4f4f4;
    margin: 2em 1.5em;
}
li {
    font-family: sans-serif;
    font-size: 12pt;
    line-height: 14pt;
    list-style:none;
    list-style-type:none;
    padding: 3px 10px;
    margin: 3px 15px;
    display: block;
    clear:both;
}
.content {
    width: 600px;
    background-color: white;
    margin-bottom: 5em;
    padding-bottom: 3em;
    -webkit-box-shadow: rgba(89, 89, 89, 0.449219) 2px 1px 9px 0px;
    -moz-box-shadow: rgba(89, 89, 89, 0.449219) 2px 1px 9px 0px;
    box-shadow: rgba(89, 89, 89, 0.449219) 2px 1px 9px 0px;
    border: 0;
    border-radius: 11px;
    -moz-border-radius: 11px;
    -webkit-border-radius: 11px;
    height: 96%;
    min-height: 90%;
}
.size {
    float: right;
    color: gray;
}
h1 {
    padding: 10px;
    margin: 15px;
    font-size:13pt;
    border-bottom: 1px solid lightgray;
}
a {
    font-weight: 500;
    perspective: 600px;
    perspective-origin: 50% 100%;
    transition: color 0.3s;
    text-decoration: none;
    color: #060606;
}
a:hover,
a:focus {
    color: #e74c3c;
}
a::before {
    background-color: #fff;
    transition: transform 0.2s;
    transition-timing-function: cubic-bezier(0.7,0,0.3,1);
    transform: rotateX(90deg);
    transform-origin: 50% 100%;
}
a:hover::before,
a:focus::before {
    transform: rotateX(0deg);
}
a::after {
    border-bottom: 2px solid #fff;
}
</style>
"""


def process_dir(top_dir, opts):
    for parentdir, dirs, files in os.walk(top_dir):
        if not opts.dryrun:
            abs_path = os.path.join(parentdir, index_file_name)
            try:
                index_file = open(abs_path, "w")
            except Exception as e:
                print('cannot create file %s %s' % (abs_path, e))
                continue
            if parentdir == top_dir:
                index_file.write('''<!DOCTYPE html>
    <html>
     <head>{css}</head>
     <body>
      <div class="content">
       <h1>{curr_dir}</h1>'''.format(
                    css=CSS,
                    curr_dir=os.path.basename(os.path.abspath(parentdir))
                ))
            else:
                index_file.write('''<!DOCTYPE html>
    <html>
     <head>{css}</head>
     <body>
      <div class="content">
       <h1>{curr_dir}</h1>
       <li><a style="display:block; width:100%" href="../index.html">&#x21B0;</a></li>'''.format(
                    css=CSS,
                    curr_dir=os.path.basename(os.path.abspath(parentdir))
                ))
        for dirname in sorted(dirs):
            absolute_dir_path = os.path.join(parentdir, dirname)
            flagfile_path = os.path.join(absolute_dir_path, "hiddendir")
            if os.path.isfile(flagfile_path):
                continue
            if not os.access(absolute_dir_path, os.W_OK):
                print("***ERROR*** folder {} is not writable! SKIPPING!".format(absolute_dir_path))
                continue
            if opts.verbose:
                print('DIR:{}'.format(absolute_dir_path))
            if not opts.dryrun:
                index_file.write("""
       <li><a style="display:block; width:100%" href="{link}/index.html">&#128193; {link_text}</a></li>""".format(
                    link=dirname,
                    link_text=dirname
                ))
        for filename in sorted(files):
            if filename == "hiddendir" or filename == "nobackup":
                continue
            if opts.filter and not fnmatch.fnmatch(filename, opts.filter):
                if opts.verbose:
                    print('SKIP: {}/{}'.format(parentdir, filename))
                continue
            if opts.verbose:
                print('{}/{}'.format(parentdir, filename))
            # don't include index.html in the file listing
            if filename.strip().lower() == index_file_name.lower():
                continue
            try:
                size = int(os.path.getsize(os.path.join(parentdir, filename)))
                if not opts.dryrun:
                    index_file.write("""
       <li>&#x1f4c4; <a href="{link}">{link_text}</a><span class="size">{size}</span></li>""".format(
                                link=filename,
                                link_text=filename,
                                size=pretty_size(size))
                    )
            except Exception as e:
                print('ERROR writing file name:', e)
                repr(filename)
        if not opts.dryrun:
            index_file.write("""
  </div>
 </body>
</html>""")
            index_file.close()


# bytes pretty-printing
UNITS_MAPPING = [
    (1000 ** 5, ' PB'),
    (1000 ** 4, ' TB'),
    (1000 ** 3, ' GB'),
    (1000 ** 2, ' MB'),
    (1000 ** 1, ' KB'),
    (1000 ** 0, ' byte'),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    """Human-readable file sizes.
    ripped from https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)
    return str(amount) + suffix


def main(argv=None):
    """Generate index.html files for a directory tree"""
    parser = argparse.ArgumentParser(description='''DESCRIPTION:
    Generate directory index files recursively.
    Start from current dir or from folder passed as first positional argument.
    Optionally filter by file types with --filter "*.py". ''')

    parser.add_argument('top_dir',
                        nargs='?',
                        action='store',
                        help='top folder from which to start generating indexes, '
                             'use current folder if not specified',
                        default=None)

    parser.add_argument('--filter', '-f',
                        help='only include files matching glob',
                        required=False)

    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='***WARNING: this can take a very long time with complex file tree structures***'
                             ' verbosely list every processed file',
                        required=False)

    parser.add_argument('--dryrun', '-d',
                        action='store_true',
                        help="don't write any files, just simulate the traversal",
                        required=False)

    parser.add_argument('--yes', action='store_true',
                        help="Don't ask for confirmation if run without args",
                        required=False)

    config = parser.parse_args(argv)
    if config.top_dir is None:
        if not config.yes and not ask_yesno("You seem to be running genautoindex from the current dir. Are you sure?"):
            sys.exit(0)
        config.top_dir = os.getcwd()
    process_dir(config.top_dir, config)


if __name__ == "__main__":
    main()
