import sys

import autograder.api.common
import autograder.api.user.auth

KEY_SUCCESS = 'success'
KEY_FOUND_USER = 'found-user'

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    config_data['email'] = arguments.email
    config_data['user-pass'] = arguments.userpass

    success, result = autograder.api.user.auth.send(config_data.get("server"), config_data)

    if (not success):
        print(result)
        return 1

    if (not result[KEY_FOUND_USER]):
        print("No matching user found.")
        return 0

    if (result[KEY_SUCCESS]):
        print("Authentication successful.")
    else:
        print("Authentication failed.")

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(
        description = 'Authenticate as a user in this course.',
        include_assignment = False)

    parser.add_argument('email', metavar = 'EMAIL',
        action = 'store', type = str,
        help = 'The email of the user to auth.')

    parser.add_argument('userpass', metavar = 'PASS',
        action = 'store', type = str,
        help = 'The password of the user to auth.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
