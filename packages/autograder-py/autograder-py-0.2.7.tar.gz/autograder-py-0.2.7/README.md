# Python Interface for Autograder

The Python interface for the autograding server.

## The CLI

This project contains several tools for interacting with an autograding server and testing
via the `autograder.cli` package.
All tools will show their usage if given the `--help` options.

You can get al list of tools by invoking `autograder.cli` directly:
```sh
python3 -m autograder.cli
```


### Server API Tools

These set of tools interact with an autograding server's API and typically revolve around working with assignments.

#### Configuration

To know who you are and what you are working on the autograder needs a few configuration options:
 - `server` -- The autograding server to connect to.
 - `course` -- The ID for the course you are enrolled in.
 - `assignment` -- The current assignment you are working on.
 - `user` -- Your username (which is also your email).
 - `pass` -- You password (probably sent to you by a TA or the autograding server in an email).

All these options can be set on the command line when invoking on of these tools, e.g.,:
```sh
python3 -m autograder.cli.submit --user sammy@ucsc.edu --pass pass123 my_file.py
```

There are several other places that config options can be specified,
with each later location overriding any earlier options.
Here are the places options can be specified in the order that they are checked:
 1. `./config.json` -- If a `config.json` exists in the current directory, it is loaded.
 2. `<platform-specific user config location>/autograder.json` -- A directory which is considered the "proper" place to store user-related config for the platform you are using (according to [platformdirs](https://github.com/platformdirs/platformdirs)). Use `--help` to see the exact place in your specific case. This is a great place to store login credentials.
 3. Files specified by `--config` -- These files are loaded in the order they appear on the command-line.
 4. Bare Options -- Options specified directly like `--user` or `--pass`. These will override all previous options.

A base config file (`config.json`) is often distributed with assignments that contains most the settings you need.
You can modify this config to include your settings and use that for setting all your configuration options.

Using the default config file (`config.json`):
```sh
# `./config.json` will be looked for and loaded if it exists.
python3 -m autograder.cli.submit my_file.py
```

Using a custom config file (`my_config.json`):
```sh
# `./my_config.json` will be used.
python3 -m autograder.cli.submit --config my_config.json my_file.py
```

You can also use multiple config files (latter files will override settings from previous ones).
This is useful if you want to use the config files provided with assignments, but keep your user credentials in a more secure location:
```sh
# Use the default config file (config.json), but then override any settings in there with another config file:
python3 -m autograder.cli.submit --config config.json --config ~/.secrets/autograder.json my_file.py
```

For brevity, all future commands in this document will assume that all standard config options are in the default
config files (and thus will not need to be specified).

#### Submitting an Assignment

Submitting an assignment to an autograder is done using the `autograder.cli.submit` command.
This command takes the standard config options as well as an optional message to attach to the submission (like a commit message)
as well as all files to be included in the submission.

```sh
python3 -m autograder.cli.submit --message "This is my submit message!" my_file.py
```

As many files as you need can be submitted (directories cannot be submitted):
```sh
python3 -m autograder.cli.submit my_first_file.py my_second_file.java some_dir/*
```

The autograder will attempt to grade your assignment and will return some message about the result of grading.
For example, a successful grading may look like:
```
The autograder successfully graded your assignment.
Autograder transcript for assignment: HO0.
Grading started at 2023-09-26 08:35 and ended at 2023-09-26 08:35.
Task 1.A (my_function): 40 / 40
Task 2.A (test_my_function_value): 30 / 30
Task 2.B (TestMyFunction): 30 / 30
Style: 0 / 0
   Style is clean!

Total: 100 / 100
```

On any successful grading (even if you got a zero), your result has been saved by the autograder and is in the system.
On a submission failure, the autograder will tell you and you will not receive any grade for your submission.
A failure may look like:
```
The autograder failed to grade your assignment.
Message from the autograder: Request could not be authenticated. Ensure that your username, password, and course are properly set.
```

#### Checking Your Last Submission

You can ask the autograder to show you the grade report for your last submission using the
`autograder.cli.peek` command.

```sh
python3 -m autograder.cli.peek
```

The output may look like:
```
Found a past submission for this assignment.
Autograder transcript for assignment: HO0.
Grading started at 2023-09-26 08:35 and ended at 2023-09-26 08:35.
Task 1.A (my_function): 40 / 40
Task 2.A (test_my_function_value): 30 / 30
Task 2.B (TestMyFunction): 30 / 30
Style: 0 / 0
   Style is clean!

Total: 100 / 100
```

If you have made no past (successful) submissions, then your output may look like:
```
No past submission found for this assignment.
```

#### Getting a History of All Past Submissions

You can use the `autograder.cli.history` command to get a summary of all your past submissions for an assignment.

```sh
python3 -m autograder.cli.history
```

The output may look like:
```
Found 2 submissions.
    Submission ID: 1695682455, Score: 24 / 100, Time: 2023-09-25 17:54.
    Submission ID: 1695735313, Score: 100 / 100, Time: 2023-09-26 08:35, Message: 'I did it!'
```

If you have made no past (successful) submissions, then your output may look like:
```
No past submission found for this assignment.
```


### General Tools

This project also provides tools to use on local code and does not interact with an autograding server.

#### Checking Style

You can invoke the default style checker (often used in assignments) with the `autograader.cli.style` command.
The style checker works with Python files (.py) and iPython Notebooks (.ipynb).

```sh
python3 -m autograder.cli.style my_file.py
```

Multiple files and directories can be specified (directories will be recursively descended):
```sh
python3 -m autograder.cli.style my_first_file.py my_second_file.ipynb some_dir/*
```


### Utilities

These commands are general utilities that students and graders may both find useful.

#### Extracting Sanitized Code

It may be difficult to view a student's code on the command line.
Whether it is inside an iPython notebook or just messy,
it can be hard to tell what code the autograder it actually going to look at.
You can use `autograder.cli.util.extract-code` to pull Python code out of
a vanilla Python (.py) file or iPython notebook (.ipynb) and either output it to the screen or write it out to another file.

```sh
python3 -m autograder.cli.util.extract-code path/to/some/code.ipynb
```

Note that the code that is output is post-sanitization, so loose code and comments may be discarded.
Additionally the code is rebuilt from an AST, so all style is ignored.


### TA Tools

This project also provides administrative tools for interacting with an autograding server.
Test tools live in the `autograder.cli.ta` package.
These tools typically require more permissions than a student has (so students can ignore this section).

#### Fetch Grades for an Assignment

TAs can fetch the grades for an assignment in TSV format using the `autograder.cli.ta.fetch-grades` command.

#### Fetch Most Recent Submission for a User

TAs can fetch the most recent submission for a user/assignment using the `autograder.cli.ta.fetch-submission` command.

For example, you can fetch Sammy Slug's most recent submission for "HW1" using:
```
python3 -m autograder.cli.ta.fetch-submission sslug@ucsc.edu --assignment HW1
```

On success, this will write out a file called submission.zip (you can change where it writes out with `-o`) that contains a user's full submission and result.

#### Fetch All Most Recent Submission for an Assignment

TAs can fetch all the most recent submission for an assignment using the `autograder.cli.ta.fetch-submissions` command.

For example, you can fetch all the submissions for "HW1" using:
```
python3 -m autograder.cli.ta.fetch-submissions --assignment HW1
```

On success, this will write out a file called submissions.zip (you can change where it writes out with `-o`) that contains all the submissions.


### Testing Tools

This project also provides several tools that are useful for testing assignments.
These are generally used by those developing courses rather than students (so students can ignore this section).
Only an overview of these tools will be provided in this document, see the specific usage for each tool for details.

#### Grading an Assignment

This project can perform a full grading of a submission like the autograder would,
but in a Python (rather than docker) environment.
The output of a docker-based grading should exactly match the output of a Python-based grading.
`autograder.cli.grade-assignment` can be used to perform a full grading of an assignment without any additional setup.
Note that this command will also perform static steps (which are usually performed when creating the docker image)
in a temp directory.

When developing/debugging assignments, this should be be your go-to command.

#### Grading a Partially Formed Submission

`autograder.cli.grade-submission` can be used instead of `autograder.cli.grade-assignment` when the static steps
of preparing a submission have already been completed.
This command pairs with `autograder.cli.setup-grading-dir`.

#### Prepare a Grading Directory

`autograder.cli.setup-grading-dir` takes in an assignment and submission and prepares a set of directories as if it was being graded,
but does not actually perform the grading.
This command pairs with `autograder.cli.grade-submission`.

#### Preparing for Docker-Based Grading

Docker-based grading is typically only performed on an autograding server,
but when debugging that it can be helpful to see the input that a docker-based grading system would be using.
The `autograder.cli.pre-docker-grading` command can be used to emulate the steps done in-preparation for docker-based grading.

#### Test with an Example/Test Submission

Test submissions are example submissions that include a `test-submission.json` file containing the expected grading output.
The `autograder.cli.test-submissions` command can be used to run one or more test submissions using the local Python grader
and ensure that the output matches the expected result (from `test-submission.json`).

This command is especially useful as part of a CI to ensure that all assignments are getting the right answer.

#### Test Against a Remote Server

The `autograder.cli.test-remote-submissions` command works like the `autograder.cli.test-submissions` command,
except it sends the test submissions off to be graded by an autograding server (instead of local Python-based grading).
The server can be local (e.g. `127.0.0.1`), but just needs to be accepting connections.
It is recommended, but not required to run the server with the following options when testing:
 - `-c web.noauth=true` -- Do not authenticate API requests.
 - `-c grader.nostore=true` -- Do not store the result of grading.


### User Management

The tools for user management all start live in the `autograder.cli.user` package.
These tools generally require `admin` privileges.

#### Add a User

Use the `autograder.cli.user.add` command to add users to the course.
If a password is not specified, it will be generated on the server side and must be sent out to the user in an email
(therefore `--send-email` is required when no password is specified).
The `--force` parameter can also be used to update an existing user.

#### Auth as a User

You can use the `autograder.cli.user.auth` command to authenticate as the given user.
This command is useful for checking a user's password.

#### Get a User

The `autograder.cli.user.get` command can be used to get basic information about a user.

#### List all Users

The `autograder.cli.user.list` command can be used to list all the users in the course.

#### Remove a User

To remove a user, use the `autograder.cli.user.remove` command.
