"""
adbm

Command line interface for parsing and verifying input data.

Noah Stieler, 2023
"""

import database
import sys
import os

# uri = 'mongodb://localhost:27017'

# TODO allow for relative paths

args = {
    'uri': '',
    'db_name': '',
    'inc_path': '',
    'cal_path': '',
    'data_path': '',
    'collection_name': ''
}


def cli():
    _parse_input()

    # exit() would have been called if any input data is invalid/missing

    database.connect(args['uri'])
    database.db_name = args['db_name']

    database.insert_recursive(args['data_path'], args['collection_name'])
    database.insert_recursive(args['inc_path'], 'incident')
    database.insert_recursive(args['cal_path'], 'calibration')


def _parse_input() -> None:

    if len(sys.argv) <= 1:
        print('Invalid command.')
        exit()

    if sys.argv[1] == 'insert':
        _cmd_insert()
    else:
        print('Invalid command.')
        exit()


def _cmd_insert() -> None:
    global args

    for i in range(len(sys.argv)):

        if i % 2 == 0 and i != 0:  # parameter name ex. --db_name

            valid_param_name = False

            for arg_key in args.keys():
                if '--' + arg_key == sys.argv[i]:
                    valid_param_name = True

            if valid_param_name:
                args[sys.argv[i][2:]] = sys.argv[i + 1]
            else:
                print(f'Unrecognized parameter name: \'{sys.argv[i]}\'')
                exit()

    if not os.path.isdir(args['inc_path']):
        print('Directory not found: \'' + args['inc_path'] + '\'')
        args['inc_path'] = ''
    if not os.path.isdir(args['cal_path']):
        print('Directory not found: \'' + args['cal_path'] + '\'')
        args['cal_path'] = ''
    if not os.path.isdir(args['data_path']):
        print('Directory not found: \'' + args['data_path'] + '\'')
        args['data_path'] = ''

    _check_for_missing_args()


def _check_for_missing_args():
    quit_program = False
    for key in args:
        if args[key] == '':
            print(f'Option --{key} is missing.')
            quit_program = True

    if quit_program:
        exit()