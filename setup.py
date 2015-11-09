import os
from setuptools import setup, Command
from setuptools.command.build_ext import build_ext
import platform
import sys


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
        import subprocess
        import glob

        self.run_command('build')

        test_dir = os.path.join(CURR_DIR, 'tests')
        os.chdir(test_dir)

        for test_script in glob.glob("*_test.py"):
            try:
                subprocess.check_call([sys.executable, test_script])
            except subprocess.CalledProcessError:
                raise SystemExit(1)


class BuildExt(build_ext):
    def get_source_files(self):
        filenames = build_ext.get_source_files(self)
        for ext in self.extensions:
            filenames.extend(ext.depends)
        return filenames


def keywords_require_cffi(argv):
    """ This setup.py script uses the setuptools 'setup_requires' feature
    to ensures the cffi package is installed before compiling the extension
    module.
    This function parses the command line arguments to setup.py, and if none
    of these need the cffi module, then it returns an empty dictionary.
    """
    setup_requires_arguments = (
        'build',
        'build_ext',
        'build_clib',
        'install',
        'install_lib',
        'install_headers',
        'bdist',
        'bdist_dumb',
        'bdist_rpm',
        'bdist_wininst',
        'upload',
        'develop',
        'test',
        'bdist_wheel',
        'bdist_egg',
    )

    if any(argv[i] in setup_requires_arguments for i in range(1, len(argv))):
        return {
            "setup_requires": requirements,
            "cffi_modules": [
                "src/python/build_lzcomp.py:ffi",
            ]
        }
    else:
        return {}


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
    cmdclass={
        "build_ext": BuildExt,
        "test": TestCommand,
        },
    **keywords_require_cffi(sys.argv)
)
