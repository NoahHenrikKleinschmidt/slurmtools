from importlib_metadata import entry_points
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="slurmtools", 
    version="1.0.0",
    author="Noah H. Kleinschmidt",
    author_email="noah.kleinschmidt@students.unibe.ch",
    description="A package to provide both a python API and CLI to the SLURM job-handler.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoahHenrikKleinschmidt/slurmtools.git",

    packages=setuptools.find_packages( where = "." ),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

    entry_points={

        "console_scripts": [
                                "slurmtools = slurmtools.main:main",

                                "viewmyqueue = slurmtools.cli_shortcuts:viewmyqueue",
                                "viewmyq = slurmtools.cli_shortcuts:viewmyqueue",
                                "vmyq = slurmtools.cli_shortcuts:viewmyqueue",

                                "myqueue = slurmtools.cli_shortcuts:myqueue",
                                "myq = slurmtools.cli_shortcuts:myqueue",

                                "qrun = slurmtools.cli_shortcuts:qrun",
                                "qrunpy = slurmtools.cli_shortcuts:qrun_py",
                                "qrunipy = slurmtools.cli_shortcuts:qrun_ipy",
                                "qrunR = slurmtools.cli_shortcuts:qrun_R",

        ],
    },

    python_requires='>=3.6',
)