Contributing
============

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/mmore500/outset/issues.

If you are reporting a bug, please include:

-  Your operating system name and version.
-  Matplotlib and seaborn versions.
-  Any other details about your local setup that might be helpful in troubleshooting.
-  Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs.
Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

outset could always use more documentation, whether as part of the official outset docs, in docstrings, or even on the web in blog posts, articles, and such.

To build and preview the documentation locally,

.. code:: bash

   make -C docs html
   make -C docs serve

You will need to load a development virtual environment first (described below).

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/mmore500/outset/issues.

If you are proposing a feature:

-  Explain in detail how it would work.
-  Keep the scope as narrow as possible, to make it easier to implement.
-  Remember that this is a volunteer-driven project, and that contributions are welcome :)

First-time Open-source Contributors
-----------------------------------

First-time open source contributor? Welcome!

If you're looking for introductory information about how open-source software works, `opensource.guide <https://opensource.guide>`__ provides several excellent primers. Project maintainers are happy to provide further guidance --- please feel free to reach out directly.

Get Started!
------------

Ready to contribute?
Here's how to set up ``outset`` for local development.

1. Fork the ``outset`` repo on GitHub.

2. Clone your fork locally:

   .. code:: bash

      git clone git@github.com:your_name_here/outset.git --recursive cd outset

3. Create a virtual environment for local development:

   .. code:: bash

      python3 -m venv env source env/bin/activate python3 -m pip install -r requirements.txt

4. Create a branch for local development:

   .. code:: bash

      git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, recompile the bindings and check that your changes pass the tests:

   .. code:: bash

      python3 -m pytest


6. Commit your changes and push your branch to GitHub:

   .. code:: bash

      git add .
      git commit -m "Your detailed description of your changes."
      git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated.
   Put your new functionality into a function with a docstring, and add the feature to the list in README.rst.
3. All GitHub Actions tests should pass.

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed. Then run:

.. code:: bash

   bumpversion patch # possible: major / minor / patch
   git push git push --tags

Github Actions will then deploy to PyPI if tests pass.
