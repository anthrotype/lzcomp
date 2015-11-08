import os
from setuptools import setup, Command
from setuptools.command.build_ext import build_ext
from distutils.command.build import build
from setuptools.command.install import install
from setuptools.command.test import test
import platform
import sys
import os
import re


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


requirements = []
if platform.python_implementation() == "PyPy":
    if sys.pypy_version_info < (2, 6):
        raise RuntimeError(
            "LZCOMP is not compatible with PyPy < 2.6. Please "
            "upgrade PyPy to use this library."
        )
else:
    requirements.append("cffi>=1.1.0")


class TestCommand(Command):
    """ Run all *_test.py scripts in 'tests' folder with the same Python
    interpreter used to run setup.py.
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess, glob

        test_dir = os.path.join(CURR_DIR, 'tests')
        os.chdir(test_dir)

        for test in glob.glob("*_test.py"):
            try:
                subprocess.check_call([sys.executable, test])
            except subprocess.CalledProcessError:
                raise SystemExit(1)


class BuildExt(build_ext):
    def get_source_files(self):
        filenames = build_ext.get_source_files(self)
        for ext in self.extensions:
            filenames.extend(ext.depends)
        return filenames


def keywords_with_side_effects(argv):
    """
    Get a dictionary with setup keywords that (can) have side effects.

    :param argv: A list of strings with command line arguments.
    :returns: A dictionary with keyword arguments for the ``setup()`` function.

    This setup.py script uses the setuptools 'setup_requires' feature because
    this is required by the cffi package to compile extension modules. The
    purpose of ``keywords_with_side_effects()`` is to avoid triggering the cffi
    build process as a result of setup.py invocations that don't need the cffi
    module to be built (setup.py serves the dual purpose of exposing package
    metadata).

    All of the options listed by ``python setup.py --help`` that print
    information should be recognized here. The commands ``clean``,
    ``egg_info``, ``register``, ``sdist`` and ``upload`` are also recognized.
    Any combination of these options and commands is also supported.

    This function is based on the `setup.py script`_ of cryptography, which in
    turn was originally based on the `setup.py script`_ of SciPy (see
    also the discussion in `pip issue #25`_).

    .. _pip issue #25: https://github.com/pypa/pip/issues/25
    .. _setup.py scripts:
    ..    https://github.com/pyca/cryptography/blob/master/setup.py
    ..    https://github.com/scipy/scipy/blob/master/setup.py
    """
    no_setup_requires_arguments = (
        '-h', '--help',
        '-n', '--dry-run',
        '-q', '--quiet',
        '-v', '--verbose',
        '-V', '--version',
        '--author',
        '--author-email',
        '--classifiers',
        '--contact',
        '--contact-email',
        '--description',
        '--egg-base',
        '--fullname',
        '--help-commands',
        '--keywords',
        '--licence',
        '--license',
        '--long-description',
        '--maintainer',
        '--maintainer-email',
        '--name',
        '--no-user-cfg',
        '--obsoletes',
        '--platforms',
        '--provides',
        '--requires',
        '--url',
        'clean',
        'egg_info',
        'register',
        'sdist',
        'upload',
    )

    def is_short_option(argument):
        """Check whether a command line argument is a short option."""
        return len(argument) >= 2 and argument[0] == '-' and argument[1] != '-'

    def expand_short_options(argument):
        """Expand combined short options into canonical short options."""
        return ('-' + char for char in argument[1:])

    def argument_without_setup_requirements(argv, i):
        """Check whether a command line argument needs setup requirements."""
        if argv[i] in no_setup_requires_arguments:
            # Simple case: An argument which is either an option or a command
            # which doesn't need setup requirements.
            return True
        elif (is_short_option(argv[i]) and
              all(option in no_setup_requires_arguments
                  for option in expand_short_options(argv[i]))):
            # Not so simple case: Combined short options none of which need
            # setup requirements.
            return True
        elif argv[i - 1:i] == ['--egg-base']:
            # Tricky case: --egg-info takes an argument which should not make
            # us use setup_requires (defeating the purpose of this code).
            return True
        else:
            return False

    if all(argument_without_setup_requirements(argv, i)
           for i in range(1, len(argv))):
        return {
            "cmdclass": {
                "build": DummyBuild,
                "install": DummyInstall,
                "test": DummyPyTest,
            }
        }
    else:
        cffi_modules = [
            "src/python/build_lzcomp.py:ffi",
        ]

        return {
            "setup_requires": requirements,
            "cmdclass": {
                "build_ext": BuildExt,
                "test": TestCommand,
            },
            "cffi_modules": cffi_modules
        }


setup_requires_error = ("Requested setup command that needs 'setup_requires' "
                        "while command line arguments implied a side effect "
                        "free command or option.")


class DummyBuild(build):
    """
    This class makes it very obvious when ``keywords_with_side_effects()`` has
    incorrectly interpreted the command line arguments to ``setup.py build`` as
    one of the 'side effect free' commands or options.
    """

    def run(self):
        raise RuntimeError(setup_requires_error)


class DummyInstall(install):
    """
    This class makes it very obvious when ``keywords_with_side_effects()`` has
    incorrectly interpreted the command line arguments to ``setup.py install``
    as one of the 'side effect free' commands or options.
    """

    def run(self):
        raise RuntimeError(setup_requires_error)


class DummyPyTest(test):
    """
    This class makes it very obvious when ``keywords_with_side_effects()`` has
    incorrectly interpreted the command line arguments to ``setup.py test`` as
    one of the 'side effect free' commands or options.
    """

    def run_tests(self):
        raise RuntimeError(setup_requires_error)


setup(
    name="lzcomp",
    version='0.1',
    url="https://github.com/google/brotli",
    description="Python binding of the LZCOMP compression library",
    author="Cosimo Lupo",
    author_email="cosimo.lupo@daltonmaag.com",
    license="Apache 2.0",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Utilities',
        ],
    package_dir={"": "src/python"},
    packages=['lzcomp'],

    tests_require=requirements,
    install_requires=requirements,

    zip_safe=False,
    entry_points={
        'console_scripts': ["lzcomp = lzcomp.cli:main"]
        },
    **keywords_with_side_effects(sys.argv)
)
