## wsgi-shim

This repository contains files to set up and configure a Python-based
website using the WSGI protocol for infrastructure that uses Phusion Passenger.
While the anticipated audience are folks using "project webspace" in the
Department of Computer Science at Princeton University, this package may have
broader utility.

This package provides a shim between Phusion Passenger and the WSGI application
that performs some file system checks at start-up.  If any checks fail, a page
request to the website will return an error page with feedback rather than a
generic message from the webserver with error details going to a system log.
The benefit is that in some system configurations, developers do not have
direct real-time access to server logs.

Additionally, this package provides a `wsgi-shim` command that can set up
a correct directory structure.

The following sections describe the package in general.  Additional details
specific to Princeton CS can be found at [CS Guide: Python-based Websites
Using WSGI](https://csguide.cs.princeton.edu/software/python-wsgi).

## Infrastructure Assumptions

* Developer has no direct access to the webserver machine and no direct access to
webserver logs.
* Files are stored on a shared file system
* Developer has shell access to a shared machine that can access the shared file system
* Multiple virtual hosts are served by the webserver.  Files are segregated using
POSIX permissions
* The webserver runs Passenger Phusion and can run processes as you
* The webserver initially runs under a private username and group

## ⚠️ Security Considerations

### File Permissions

The webserver will run your Python code with your UID/NetID (i.e., "as you") and
with a GID/group (to which you belong) of your choosing.  This has the benefit
that you can include secrets/credentials in files that are not world-readable.
A consideration to remember is that because the webserver will run "as you",
your running code will have access to any project space files (in any project)
that you have access.

Note that before running "as you," the webserver is running as a user/group that
can only read certain configuration/control files if they are world-readable.
These files are noted in the documentation below.

### Environment Variables

If your shell is `bash`, all the environment variables you set up in your
`.bashrc` and `.bash_profile` will be available to your running Python code.
(See: the default "on" configuration of
[PassengerLoadShellEnvvars](https://www.phusionpassenger.com/library/config/apache/reference/#passengerloadshellenvvars).)
This can obviously be
handy; however, there are some downsides.  First, from a security perspective,
environment variables containing secrets can be exposed to other running
processes on the shared webserver.  Second, from a configuration management
perspective, having some of the configuration for your site be in your personal
`.bashrc` file in your home directory and the rest of the configuration in the
project space for the site may lead to issues when you are ready to hand the
reins over to another person.

When the webserver runs your `.bashrc` and `.bash_profile`, it will have set the
environment variable `IN_PASSENGER`.  If you want the webserver to effectively
skip your normal Bash configuration, you can put this at the top of your
`.bashrc` and `.bash_profile` files:

    if [ -n "$IN_PASSENGER" ]; then
        return 0
    fi

As an alternative, you can pass environment variables and secrets to the webserver
application, you can use the `[environment]` and `[secret_files]` sections in the
`config.toml` file as described below.

## Requesting Resources / Initial Set-up

The step-by-step instructions in this section assume you are starting from scratch.
If you already have some of the resources that you wish to use, adapt
these instructions as appropriate.

> 📝 **Note:** You won't have direct access to web server logs for debugging.
> Therefore, it's important to be methodical and test along the way.  The
> `wsgi-shim` package can catch common configuration mistakes and give feedback
> without access to the web server logs.

### 1. Request "project disk space"

From your sysadmin, request project disk space and a new POSIX group for the files.

In these steps, we will assume the disk space is at `/n/fs/myproject`, the
POSIX group is `mygroup`, and your username is `mynetid`.

### 2. Verify/set permissions on the project space

After receiving notification that the disk space has been created, verify that it
exists with the correct group and permissions.

Verify project space permissions:

    ls -ld /n/fs/myproject

The output should look like something like this:

    drwxr-sr-x. 4 mynetid mygroup 59 Sep 20 13:24 /n/fs/myproject

If the owner is not `mynetid` (i.e., *your* username), contact support.

The group should **not** be your default group (i.e., the one displayed when you
run the `id -gn` command).  If it is your default group, contact support.

If the permissions are not `drwxr-sr-x` (note the lowercase "s"), change them with
`chmod 2755 /n/fs/myproject`.  The lowercase "s" in this position is the SETGID bit
and ensures that files and subdirectories created under `/n/fs/myproject` will belong
to the `mygroup` group by default.

### 3. Build Python

Build a local-to-your-website version of Python 3.11 or greater.  You will build
this in the same directory that is shared with the webserver.  Note that the
webserver machine and your access machine must be configured such that Python
built on the access machine will work on the webserver (same architecture, same OS,
same shared libraries, etc.).

These are abbreviated instructions from the
[CS Guide: Building a Local Version of
Python](https://csguide.cs.princeton.edu/software/virtualenv#build).
To build Python 3.11.5 and install it in your project space at
`/n/fs/myproject/python-3.11.5` use these commands (adjusting `PROJECT_DIR`
and `PYVER` as appropriate):

    PROJECT_DIR="/n/fs/myproject"
    PYVER="3.11.5"
    cd $PROJECT_DIR
    mkdir temp
    cd temp
    wget https://www.python.org/ftp/python/$PYVER/Python-$PYVER.tar.xz
    tar xJf Python-$PYVER.tar.xz
    cd Python-$PYVER
    ./configure --prefix=$PROJECT_DIR/python-$PYVER
    make
    make install
    cd /n/fs/myproject
    rm -rf temp

Test the Python installation:

    /n/fs/myproject/python-3.11.5/bin/python3 --version

Output should be:

    Python 3.11.5

### 4. Create Website Directory and Build Python Virtual Environment

Create the directory to hold the files associated with your website.
This directory must be world-readable but not world-writeable:

    mkdir /n/fs/myproject/mywebsitefiles
    chmod o=rx /n/fs/myproject/mywebsitefiles

Build the Python virtual environment for your website in `venv`.

    cd /n/fs/myproject/mywebsitefiles
    /n/fs/myproject/python-3.11.5/bin/python3 -m venv venv

> 📝 **Note:** This is the Python virtual environment that will be
> used for the running website.  This is, for example, where you
> would "pip install" packages such as Flask or Django.

### 5. Install wsgi-shim and Create Initial Configuration

Activate your virtual environment, install the `wsgi-shim` package,
and create the initial PassengerAppRoot directory:

    cd /n/fs/myproject/mywebsitefiles
    source venv/bin/activate
    pip install wsgi-shim
    wsgi-shim install /n/fs/myproject/mywebsitefiles/www
    deactivate

At this point, your project space directory structure will look like this:

    /n/fs/myproject
    ├── python-3.11.5
    │   └── ...
    └── mywebsitefiles
        ├── venv
        │   └── ...
        └── www
            ├── config.toml
            ├── passenger_wsgi.py
            └── tmp
                ├── maint.txt
                └── restart.txt

### 6. Request "project web space"

With the directory structure created, it is time to request that your sysadmins
configure the webserver to recognize your domain (e.g., mywebsite.example.com) as
a valid website and route its requests to your Python code via the provided
`passenger_wsgi.py` file.

You may need to provide the key/value pairs in the `[passenger]` section of the
`/n/fs/myproject/mywebsitefiles/config.toml` file created in the previous step
to your sysadmins.

### 7. Test Initial Configuration

When you get verification from your sysadmins that the project web space is
set up, verify that the DNS name for the website is in place:

    host mywebsite.example.com

If you get a response indicating "not found," wait an hour and try again.
If at that point you are still getting a "not found" indication, follow-up
with your sysadmins.

Open a browser and visit `https://mywebsite.example.com`

You should see a "Maintenance" page.  Now, disable
[maintenance mode](#maintenance) and force a restart of your site:

1. Run: `rm /n/fs/myproject/mywebsitewsgi/www/tmp/maint.txt`
1. Run: `touch /n/fs/myproject/mywebsitewsgi/www/tmp/restart.txt`
1. Reload the site a few times (waiting several seconds between reloads)
until it shows updated content.

You should see a "Hello, World" page.  If so, congratulations!  You're
ready to start installing and developing code as described in the next
section.

If you are not getting the "Hello, World" page, carefully review your
steps and also refer to the Troubleshooting section, below.

## Install / Develop Site-Specific Code

### Directory Structure

Other than being readable by the user/group specified in the `config.toml`
file, the webserver doesn't put specific restrictions on where in project
space the code implementing your web application must go.  One possibility
is the following layout:

    /n/fs/myproject
    ├── python-3.11.5
    │   └── ...
    └── mywebsitefiles
        ├── venv
        │   └── ...
        ├── www
        │   ├── config.toml
        │   ├── passenger_wsgi.py
        │   └── tmp
        │       └── restart.txt
        ├── secrets
        │   └── credentials.env
        ├── log
        │   └── logfile
        └── myapp
            ├── file1.py
            ├── file2.py
            └── ...

In this example, the `secrets` directory contains credentials and, as such,
should not be world-readable; the `myapp` directory contains the Python code
making up the web application.  The `myapp` directory might reasonably be
a checked out Git repository of your code.

The next section describes how to edit your `config.toml` file to point
to your application in `myapp`.

### Configuration Settings

The `config.toml` file created by the `wsgi-shim install` contains
the documentation on available settings.  Here is an example
using the directory structure above with the `application` callable
defined in `file1.py`:

    [passenger]
    passenger_user = "mynetid"
    passenger_group = "projectgroup"
    passenger_app_root = "/n/fs/myproject/mywebsitefiles/www"
    passenger_python = "/n/fs/myproject/mywebsitefiles/venv/bin/python"
    [wsgi]
    module = "/n/fs/myproject/mywebsitefiles/www/myapp/file1.py"
    app = "app"
    [secret_files]
    SECRETS = "/n/fs/myproject/mywebsitefiles/secrets/credentials.env"
    [environment]
    LOG_FILENAME = "/n/fs/myproject/mywebsitefiles/log/logfile"

### Logging

Under the assumption that you don't have ready access to the webserver logs,
it is important to set up logging as early as possible in your application.

#### Flask Example

Here is an example Flask application that would work with the example
`config.toml` shown above.

    # /n/fs/myproject/mywebsitefiles/www/myapp/file1.py
    import logging.config
    import os

    from flask import Flask

    # Configure logging before instantiating Flask app
    if LOG_FILENAME := os.environ.get('LOG_FILENAME'):
        logging.config.dictConfig({
            'version': 1,
            'formatters': {'default': {
                'format': '%(asctime)s %(levelname)s %(name)s '
                          '%(threadName)s : %(message)s',
            }},
            'handlers': {'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': LOG_FILENAME,
                'maxBytes': 40000,
                'backupCount': 2,
            }},
            'root': {
                'level': 'INFO',
                'handlers': ['file'],
            }
        })

    app = Flask(__name__)


    @app.route("/")
    def hello_world():
        app.logger.info('Request: /')
        return "<p>Hello, World!</p>"


## Operation

The webserver will start your application when it receives a request to a URL
in `https://mywebsite.example.com`.  This process will generally handle
multiple requests.  After a period of inactivity, the webserver will kill the
process until there is another request.

### Restarting Your Application

Phusion Passenger allows you to force a restart of your application by
updating the timestamp of the `restart.txt` file:

    touch /n/fs/myproject/mywebsitewsgi/www/tmp/restart.txt

Note that the restart is not immediate and the file is only checked when a
URL is visited on your site but no more often than every 10 seconds (the value
of PassengerStatThrottleRate in the webserver global configuration)

### [Using Maintenance Mode]{#maintenance}

The provided `passenger_wsgi.py` file (via `uwsgi-shim install`) implements
a mechanism that, when enabled, will not load your website code but, instead,
show a "maintenance" page where all requests to the site return a
`503 Service Unavailable` response.  In this mode,  your site-specific code
(e.g., based on Django, Flask, etc.) will not be accessed.

To enable maintenance mode, create the sentinel file:

    touch /n/fs/myproject/mywebsitewsgi/www/tmp/maint.txt

To disable maintenance mode, delete the sentinel file:

    rm /n/fs/myproject/mywebsitewsgi/www/tmp/maint.txt

Note that the existence of this file is only checked when the WSGI server
(e.g., Phusion Passenger) restarts the application.  Therefore, anytime you
enable/disable maintenance mode, you need to force a restart of the
application.  For example, to update the code for a website, one might
follow these steps:

1. Run: `touch /n/fs/myproject/mywebsitewsgi/www/tmp/maint.txt`
1. Run: `touch /n/fs/myproject/mywebsitewsgi/www/tmp/restart.txt`
1. Reload the site a few times until it shows the maintenance page.  This can
   take up to 10 seconds.
1. Update the site
1. Run: `rm /n/fs/myproject/mywebsitewsgi/www/tmp/maint.txt`
1. Run: `touch /n/fs/myproject/mywebsitewsgi/www/tmp/restart.txt`
1. Reload the site a few times until it shows the updated content.

Note that the `restart.txt` file must be world-readable.  If you
delete this file and later recreate it, be sure it is world-readable.

## Troubleshooting

* Check that your website host name is resolvable in DNS:

        host mywebsite.example.com
* Use the `wsgi-shim check` command to verify directory structure and
permissions:

        cd /n/fs/myproject/mywebsitefiles
        source venv/bin/activate
        wsgi-shim check /n/fs/myproject/mywebsitefiles/www
        deactivate

* Verify that your `.bashrc` and `.bash_profile` are not exiting
when invoked by the webserver (i.e., when `IN_PASSENGER` is set)?
* If you have set up logging, check your logs.
* If your application writes to the file system, verify that you
haven't run out of space.

If you believe there is a key bit of information in the webserver logs,
contact your sysadmins and specify the URL that is not working along
with a specific timestamp.

## Development

For those developing or maintaining the `wsgi-shim` package itself,
be sure to install it with the `[dev]` option to pull in packages
used when developing.

    pip install --editable .[dev]

When developing, this package uses `pre-commit`.  After the initial
clone of the repository, you will need to set up pre-commit with:

    # in the top level of the checked-out repository:
    pre-commit install

## Changelog

### 0.0.6 released 2023-10-20
* fixed a README.md typo

### 0.0.5 released 2023-10-20
* config.toml `[passenger]` fields updated to `passenger_user` and `passenger_group`
* Error and maintenance pages now show a timestamp
* config.toml now requires `[passenger]` section
* Running process user and group checked against `[passenger]` section
* fixed loading app from package

### 0.0.4 released 2023-10-17
* Error/Maintenance HTML responses point to developer

### 0.0.3 released 2023-10-14
* Fixed disconnect between generated `passenger_wsgi.py` and this module

### 0.0.2 released 2023-10-13
* Documentation is more site agnostic
* Additional tests

### 0.0.1 released 2023-10-05
* Initial Beta Version
