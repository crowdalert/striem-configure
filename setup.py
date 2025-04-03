import os
import sys
import shutil

from pathlib import Path

from setuptools import setup
from setuptools.command.build import build
import subprocess

sys.path.append(os.path.dirname(__file__))


class BuildWithSubmodules(build):
    def run(self):
        '''
        Rather than forcing users of this repo to manually update
        submodules, pull the VRL transforms in the build step
        '''

        vrlpath = Path('build/lib/striem_configure/includes/vrl')

        subprocess.check_call(['git',
                               'clone',
                               '--depth',
                               '1',
                               'https://github.com/crowdalert/ocsf-vrl.git',
                               str(vrlpath)])

        # don't package git repository
        shutil.rmtree(Path(vrlpath, Path('.git')),
                      ignore_errors=True)

        # Remove files in the top-level (README, LICENSE, etc.)
        for entry in vrlpath.iterdir():
            if entry.is_file():
                entry.unlink()

        super().run()


setup(cmdclass={"build": BuildWithSubmodules})
