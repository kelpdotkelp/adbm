"""
adbm

Command line interface for parsing and verifying input data.

Noah Stieler, 2023
"""

import database
import sys
import os

# URI for local connection
# uri = 'mongodb://localhost:27017'

_WRITE_TO_DB = True

args = {
    'uri': '',
    'db_name': '',
    'inc_path': '',
    'cal_path': '',
    'data_path': '',
    'collection_name': ''
}

args_req = ['uri', 'db_name']


def cli() -> None:
    if len(sys.argv) <= 1:
        print('Type adbm help for command information.')
        sys.exit()

    if sys.argv[1] == 'insert':
        _cmd_insert()
    elif sys.argv[1] == 'help':
        _cmd_help()
    else:
        print('type adbm help for command information.')
        sys.exit()


def _cmd_help() -> None:
    print('General syntax:\n\tadbm [command] --[option1] [value] --[option2] [value]')
    print('Commands:')

    print('help\n\tDisplay this message.')

    print('insert\n\tRecursively insert everything at the supplied paths to MongoDB.\n'
          '\tAll paths can be either absolute or relative. If a path contains a space, enclose it in " ".')
    print('\tOPTIONS:')
    print('\t(REQUIRED) --uri\n\t\tURI string of the database.')
    print('\t(REQUIRED) --db_name\n\t\tName of the database to insert documents in.')
    print('\t(OPTIONAL) --inc_path\n\t\tPath of the incident field data. Automatically goes into the \'incident\' '
          'collection.')
    print('\t(OPTIONAL) --cal_path\n\t\tPath of the calibration field data. Automatically goes into the '
          '\'calibration\' colleciton.')
    print(
        '\t(OPTIONAL) --data_path\n\t\tPath of the target scan data. This option must be used with --collection_name.')
    print('\t(OPTIONAL) --collection_name\n\t\tName of the collection for the target scan data.')


def _cmd_insert() -> None:
    global args

    if len(sys.argv) % 2 != 0:
        print('Invalid number of parameters.')
        sys.exit()

    # Populate args
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
                sys.exit()

    # Convert all paths to absolute
    if args['inc_path'] != '':
        _path_check('inc_path')
    if args['cal_path'] != '':
        _path_check('cal_path')
    if args['data_path'] != '':
        _path_check('data_path')

    _check_for_missing_args()
    # exit() would have been called if any input data is invalid/missing
    if _WRITE_TO_DB:
        _write_to_db()


def _check_for_missing_args():
    quit_program = False
    for arg_name in args_req:
        if args[arg_name] == '':
            print(f'Option --{arg_name} is missing.')
            quit_program = True
    # Extra checks
    if bool(args['data_path'] != '') != bool(args['collection_name'] != ''):
        print('Option --data_path and --collection_name must be used together.')
        quit_program = True

    if quit_program:
        print('Type adbm help for more information.')
        sys.exit()


def _path_check(arg_name: str) -> None:
    """Checks that input paths are valid directories and converts
    them to absolute paths."""
    global args
    args[arg_name] = os.path.abspath(args[arg_name])
    if not os.path.isdir(args[arg_name]):
        print(arg_name + ' directory not found: \'' + args[arg_name] + '\'')
        sys.exit()


def _write_to_db() -> None:
    database.connect(args['uri'])
    database.db_name = args['db_name']

    if args['inc_path'] != '':
        database.insert_recursive(args['inc_path'], 'incident')
    if args['cal_path'] != '':
        database.insert_recursive(args['cal_path'], 'calibration')
    if args['data_path'] != '' and args['collection_name'] != '':
        database.insert_recursive(args['data_path'], args['collection_name'])
