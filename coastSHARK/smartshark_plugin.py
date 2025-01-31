#!/usr/bin/env python

"""Plugin for execution with serverSHARK."""

import argparse
import os
import sys
import logging
import timeit

from util import error
from util.extract_ast import ExtractAstPython, ExtractAstJava
from util.write_mongo import MongoDb
from pycoshark.utils import get_base_argparser

# set up logging, we log everything to stdout except for errors which go to stderr
# this is then picked up by serverSHARK
log = logging.getLogger('coastSHARK')
log.setLevel(logging.INFO)
i = logging.StreamHandler(sys.stdout)
e = logging.StreamHandler(sys.stderr)

i.setLevel(logging.DEBUG)
e.setLevel(logging.ERROR)

log.addHandler(i)
log.addHandler(e)


def main(args):
    if args.log_level:
        log.setLevel(args.log_level)

    # unused for now
    ignore_files = []
    ignore_dirs = []

    # preflight checks
    if not os.path.isdir(args.input):
        raise Exception('--input {} is not valid'.format(args.input))
    if not os.access(args.input, os.R_OK):
        raise Exception('--input {} is not readable'.format(args.input))
    if not args.input.endswith('/'):
        raise Exception('--input needs trailing slash')

    # timing
    start = timeit.default_timer()

    # check mongodb connectivity
    m = MongoDb(args.db_database, args.db_user, args.db_password, args.db_hostname, args.db_port, args.db_authentication, args.ssl, args.project_name, args.repository_url, args.revision)
    m.connect()

    log.info("Starting AST extraction")

    for root, dirs, files in os.walk(args.input):

        if root.replace(args.input, '') in ignore_dirs:  # subtract base_dir then match against ignore_list
            continue

        for file in files:

            if file in ignore_files:
                continue

            filepath = os.path.join(root, file)
            mongo_filepath = filepath.replace(args.input, '')  # use relative path to find File Document in mongodb

            if file.lower().endswith('.java') or file.lower().endswith('.py'):
                log.debug('parsing file: {}'.format(mongo_filepath))
            try:
                if file.lower().endswith('.py'):
                    e = ExtractAstPython(filepath)
                    e.load()
                    m.write_imports(mongo_filepath, e.imports)
                    m.write_node_type_counts(mongo_filepath, e.node_count, e.type_counts)

                if file.lower().endswith('.java'):
                    e = ExtractAstJava(filepath)
                    e.load()
                    m.write_imports(mongo_filepath, e.imports)
                    m.write_node_type_counts(mongo_filepath, e.node_count, e.type_counts)
                    if args.method_metrics:
                        m.write_method_metrics(mongo_filepath, e.method_metrics())

            # this is not critical, we can still do the other files
            except error.ParserException as e:
                log.info(str(e))
            # this is not critical, we can still do the other files
            except TabError as e:
                log.info(str(e))
            # this is not ciritcal, we can still do the other files
            except IndentationError as e:
                log.info(str(e))
            # this is critical
            except Exception as e:
                log.exception(e)
                raise

    end = timeit.default_timer() - start
    log.info("Finished AST extraction in {:.5f}s".format(end))


if __name__ == '__main__':
    # we basically re-use the vcsSHARK argparse config here
    parser = get_base_argparser('Analyze the given URI. An URI should be a checked out GIT Repository.', '2.0.1')
    parser.add_argument('-i', '--input', help='Path to the checked out repository directory', required=True)
    parser.add_argument('-pn', '--project_name', help='Hash of the revision.', required=False)
    parser.add_argument('-r', '--revision', help='Hash of the revision.', required=True)
    parser.add_argument('-u', '--repository_url', help='URL of the project (e.g., GIT Url).', required=True)
    parser.add_argument('-ll', '--log_level', help='Log level for stdout (DEBUG, INFO), default INFO', default='INFO')
    parser.add_argument('-mm', '--method_metrics', help='Collect new method metrics (experimental)', default=False)
    main(parser.parse_args())
