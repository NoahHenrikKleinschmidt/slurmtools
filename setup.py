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
                                "stools = slurmtools.main:main",

                                "viewmyqueue = slurmtools._cli_shortcuts:viewmyqueue",
                                "viewmyq = slurmtools._cli_shortcuts:viewmyqueue",
                                "vmyq = slurmtools._cli_shortcuts:viewmyqueue",

                                "myqueue = slurmtools._cli_shortcuts:myqueue",
                                "myq = slurmtools._cli_shortcuts:myqueue",

                                "qrun = slurmtools._cli_shortcuts:qrun",
                                "qrunpy = slurmtools._cli_shortcuts:qrun_py",
                                "qrunipy = slurmtools._cli_shortcuts:qrun_ipy",
                                "qrunR = slurmtools._cli_shortcuts:qrun_R",

        ],
    },

    python_requires='>=3.6',
)