.. image:: https://img.shields.io/pypi/pyversions/bumpymcbumpface.svg
    :target: https://pypi.python.org/pypi/bumpymcbumpface

.. image:: https://img.shields.io/github/tag/cjrh/bumpymcbumpface.svg
    :target: https://img.shields.io/github/tag/cjrh/bumpymcbumpface.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20bumpymcbumpface-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20$bumpymcbumpface-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/bumpymcbumpface.svg
    :target: https://img.shields.io/pypi/v/bumpymcbumpface.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/


Bumpy McBumpface
================

TL,DR
-----

To run:

.. code-block:: shell

    /home/blah/myproject $ bumpymcbumpface --push-git --push-pypi

To get help:

.. code-block:: shell

    /home/blah/myproject $ bumpymcbumpface -h
    usage: bumpymcbumpface.py [-h] [--debug] [--show] [--dry-run] [--push-git]
                              [--push-pypi]
                              [{major,minor,patch}]

    bumpymcbumpface - version-bump, tag, push, deploy

    positional arguments:
      {major,minor,patch}

    optional arguments:
      -h, --help           show this help message and exit
      --debug              Print debugging messages (default: False)
      --show               Show the current version and exit (default: False)
      --dry-run            Describe what would be done, and exit (default: False)
      --push-git           Push the new commit and tag to github (default: False)
      --push-pypi          Push the new built packages to PyPI (default: False)
    /home/blah/myproject $

Overview
--------

When doing a new release, I got real tired of doing these things by hand:

1. Update the version number of my package
2. Commit that change to git
3. Create a git tag with the new version
4. Push the tag (and the new commit) to github
5. Build new distributable packages: wheel (``.whl``) and source dist (``.tar.gz``)
6. Upload the new packages to pypi

*Bumpy McBumpface* will do these things, and will not ask questions.

Requirements
------------

You need to have these:

- A file called ``VERSION`` in your project root, with MAJOR.MINOR.PATCH numbers
- git
- twine (set up `keyring <https://twine.readthedocs.io/en/latest/#keyring-support>`_
  so that twine won't ask you for login/password)
- pip
- wheel

You probably **SHOULD BE** in master branch branch when you run, but you
only need to be in a branch that has a valid remote.

Instructions
------------

There are a several options, but only two important ones. By default,
it will NOT do these things automatically:

- Push to github
- Deploy to PyPI

This is just so that it defaults to "safe" by not affecting anything
beyond your computer during testing. To make it do these things too,
run it like this:

.. code-block:: shell

    $ bumpymcbumpface --push-git --push-pypi

*Bumpy McBumpface* assumes that your version number is in the following
format::

    MAJOR.MINOR.PATCH

where each of the three fields is an integer. This also works for
calendar-based versioning. By default, the PATCH value will be increased
by 1 if you run without arguments. These two are the same:

.. code-block:: shell

    $ bumpymcbumpface --push-git --push-pypi
    $ bumpymcbumpface --push-git --push-pypi patch

For a MINOR bump, change the word *patch* to *minor*. Likewise for *major*.

Now that you're using a file called ``VERSION`` in your project root to
store your version number, how do you get it into your ``setup.py``?
Just read it in, like this:

.. code-block:: python

    # setup.py
    from os import path
    from io import open  # For universal packages + py27

    here = path.abspath(path.dirname(__file__))

    setup(
        name='bumpymcbumpface',
        version=open(path.join(here, 'VERSION')).readline().strip(),
        ...
    )


Good luck!
