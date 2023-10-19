# Python packaging

Every python package MUST have the following layout:
|- Mother_Directory
    |- Source Directory
    |- Document Directory
    |- LICENCE.txt
    |- MANIFEST.in
    |- pyproject.toml
    |- README.md
    |- setup.cfg
    |- setup.py

### Mother directory

This directory is the container of the entire package. Its name must be the same
as the name of the packages as defined in the setup & toml-files.

### Source Directory

Here you put in the code that you would like to make pip-installable. The name of
the directory MUST be the same as that of the mother directory.

### Document directory.

Here you put any documentation files you would like the user to have access to (such as this file).
Traditionally, the directory is named 'docs', but one could deviate from this name.

### Licence file

Choosing a license for your package is a tricky legal business. The most common flavours to
choose from are the [PyPI license](https://docs.python-guide.org/writing/license/).
Creating a licence file is easy: just take a .txt-file and copy the appropriate text from
the internet model license (see the above url for the types) into the .txt-file and you are done.
<br />
<br />
The trouble is, for a public package, which software license to choose. This will have a huge impact
on what your users are allowed to do with the software. Licenses as BSD, MIT grant the most
freedom, but they also absolve the developers of any responsibility. Cop-left licenses like GNU, GPL
come with the problem that they cannot be used in commercial software, as you are not allowed to
make money with them. This is a huge problem, as your software will be subject to the licenses
of all python packages you use and roughly 18% of them is copy-left.
<br />
<br />
A quick workaround is to put the package in a private repository so that only people with
the password can install it. Then you do not have to worry about licenses until the moment
you decide to go public. Using an installation from a private repository is considered
a 'weak' security (and it is either security OR licensing, you have to deal with at least one of them),
as tokens & passwords can easily be distributed among people. A good solution (but much more work)
is to install your own personal license management server.

### Manifest file

This is a link to what is included in the package and what not. It must have at least the following lines: <br />
include LICENSE <br />
include README.md <br />
recursive-include source directory * <br />
recursive-include docs * <br />
recursive-include dist * <br />
The dist-directory will be automatically generated. We discuss this in just a moment.

### toml-file

Just copy this file from the current repo. The only thing you have to be cautious about, is the list
of 'requires'. These are all the packages that your software needs to run: the dependencies. So you
will have to adapt them to your needs.

### setup.cfg

You can also just copy it from this repo and adapt the tags to your needs. Again, the most critical is
the dependencies (which have to be synchronized with the toml-file). Also, the package name is critical,
as it must be the same as the directory-names.

### setup.py

There are multiple ways of defining this file. Experts are really enthousiastic about [setuptools](https://pythonhosted.org/an_example_pypi_project/setuptools.html),
but there are more ways to do it. The current repo at least works fine. Again, you could just
adapt the tags to your needs. Critical are again the dependencies and package-names. For the
rest, make sure that everything between the cfg-file and .py-file is consistent and that the
tags like target audience, programming language, description, link to readme, etc. all make sense.
URL is important for public installation, but less important for a private package.
<br />
<br />
There is one final issue: you HAVE to define in the packages-tag not just the source directory name (package name),
but also the name of any subdirectory of the source directory that has relevant code. Otherwise, those
subdirectories will NOT be copied into your virtual environment during installation.

# Init-files

Now comes the next important thing: defining __init__.py files in the source directory. The source directory
must have an init-file and also every subdirectory of the source directory that contains relevant code. Now,
every class or function that you would like the user to have access to, MUST be imported (with python import statements)
in the init-files. If the code is in a subdirectory of the source directory, the mother-init in the source directory should read: <br />
from .subdirectory.myfile import myclass <br />
And the init-file in the subdirectory should read: <br />
from .myfile import myclass <br />
All imports in the python-files themselves should also use [relative import statements](https://docs.python.org/3/reference/import.html)
and no sys.path.append techniques to import files from other directories. This is true for all python files that
carry code that can be invoked by user-calls (directly or indirectly).If the package includes, for example, test code that you only
want to be available for developers that work on the repo, sys.paths are fine there.

### Direct versus indirect calls

If you have a big class that you would like the user to have access to, but that also uses two small classes that you do not
want the user to have access to, only the big class needs to be included in ALL the init-files. But also the imports to
the small classes must follow the rules of relative imports in the source files and the entire directory (including both the big & small classes)
should be added to the setup-packages & manifest so that the source-code is copied along.

### Django apps

There is an excellent tutorial about how to make your django-app redistributable (a pypi-package): [Django docs](https://docs.djangoproject.com/en/4.2/intro/reusable-apps/).
The steps basically follow the approach outlined above, where the source directory now becomes the django-app folder.
Be sure to read the docs carefully, as apps with static files, templates, etc. require a little more work then our djangotextsplitter-app.
<br />
<br />
The thing that the django docs does NOT tell you is how to import such a django-app. After you pip-installed it into the virtual environment,
you can register it in settings.py under INSTALLED_APPS just like any other django-app and under the master urls-file. However, it is important
to know that when you run django (from shell, tests, migrations, runserver, etc.), The python django-module is imported and django.setup()
is run automatically with the parameters of settings.py. django.setup() uses the PYTHONPATH environment variable to decide where it has to look
for apps. It takes this variable from your OS and augments it with (among others tuff) the django project folder so that it can find your regular apps. The path
to the current virtual environment variable is already in the PYTHONPATH before django starts its work, so django also can automatically
detect apps that are pip-installed in the virtual environment. However, during the django.setup() function, the django-functionality is
not yet initialized, so setup() needs a regular python import to connect to your apps. For apps in your project folder, django can run these
python imports, but for apps in the virtual environment, you need to allow for this import manually. This is the Config-class in the apps.py
file of your specific app.
<br />
<br />
So for regular django apps, the init-file in your app-folder can just be an empty file. But for apps in the virtual environment, you need to
put the config-class in the init-file. Do not include ANY other classes or functions like models or views in the init-file. Once Django has
access to the config-class by regular python import, it can set up and then you can also access the virtual environment app like any other app.

### Access to the content of the package

After installing the package, the user can simply access it by running <br />
from mypackage import myclass <br />
For any class you defined in the init-file. Just make sure the user has the documentation so he/she knows which classes to import and how to use them. <br />
For django applications it just works the same, only now statements like <br />
from myapplications.models import mymodel <br />
will only works from within django-code and not from a regular python script. And for django applications the user automatically has access to all models, views, etc. as long as ONLY the config-class and nothing else is in the init-file.

# Testing code

You can include subfolders with tests in the source directory for a python-package. Simply do not include those functions in the init-files so that
users are not bothered by them, but developers can run them from their local clone of the entire repo.
<br />
<br />
For django applications, put a django root directory (with settings, urls, etc.), a db.sqlite3-file and a manage.py-file on the same level as your source directory (which is now your django-app). Make sure that this root django is a django-MVP with your app registered. The mother directory then becomes your django project directory. Then, within the repo your django app will be a regular app to this django-MVP so you can run test, runserver, migrations, etc. to test your app. This will not influence your pip-install.

# Building the package.

Now that you have properly configured everything into a package, it is time to perform the installation. You can install locally (for testing purposes), from a private repository, or from pypi.

### Local installation

First, create a new clean python virtual environment and, from within this environment, execute the following steps: <br />
pip install build setuptools # This will allow you to make tars, wheels, etc. from your package. <br />
python -m build # This will generate the build-files: egg-info and a dist-folder with at tar-file and a wheel-file <br />
pip install -e ./ # Run from the Mother directory to install your package into the venv. -e tells pip it is a local installation <br />
Now, you can navigate to any other directory you like and enjoy your local installation.

### Installation from private repository.

For users: <br />
pip install git+https://gitlab.datascience.rijkscloud.nl/data-fabriek/textsplitter.git <br />
Tokens can be used like: pip install git+https://oauth2:my-secret-token@gitlab.datascience.rijkscloud.nl/data-fabriek/textsplitter.git <br />
Installation from a requirementsfile works like:
textsplitter @ git+https://oauth2:my-secret-token@gitlab.datascience.rijkscloud.nl/data-fabriek/textsplitter.git
<br />
For developers: <br />
Clone the repo into a directory of your choice. <br />
Create a fresh virtual environment. <br />
Install all the dependencies in there (as defined in the setup-files), but NOT the package itself <br />
pip install build setuptools <br />
Do your development work <br />
Run the tests (they must all succeed <br />
* for testsplitter: python ./Tests/Scripts/AllTests.py dummy <br />
* for djangotextsplitter: python manage.py test <br />
* Use coverage to measure that the code coverage is high enough (coverage run pytest or coverage run manage.py test --no-input and then coverage report -m) <br />
Then, re-build the package with python -m build <br />
Commit your changes to the repo: git add ./* ; git commit -am "message" ; git push <br />
Merge your branch into main (do not forget the review process!) <br />
Once your changes are in the main (default) branch, follow the user-installation steps to enjoy your work in your virtual environment.

### Installation from PyPI

If you do this, you will be able to enjoy the installation with a command like pip install textsplitter. <br />
However, the PyPI filosofy is open-source software, meaning that password protection is impossible. So this requires you to move the package to a public github/gitlab repo. This requires you to think about the license-issues. Once this is done, upload your package to PyPI using the twine-tool (documentation not yet complete at this point). Then, developers can make changes to the code in a similar way as for a private repository.

# Pipelines

In the ideal case, a pipeline for this package should enforce:
* Running all available tests. They should all pass.
* Verifying code coverage: Each seperate file should be above a certain threshold. Exclude test-code and automatically generated code (like migrations)
* Verifying code formatting and clean code in a similar way as code coverage.
* re-build the package
Once it passes all these criteria, another developer can review the code and then put it through to main.

# Getting the code publish-ready

For PyPI packages, it is considered good-practise to take care of the following items before making the code public:
* Clean code (work in progress)
* No print statements, but python loggers (not yet taken care of)
* No ton of output files unless the user asks for them (not yet taken care of)
* Tests for all cases and with good code coverage (Done)
* Clean repo; no unessecary files (not yet taken care of)
