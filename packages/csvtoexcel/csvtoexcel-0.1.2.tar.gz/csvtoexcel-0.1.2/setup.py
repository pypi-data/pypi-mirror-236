# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csvtoexcel']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.5,<4.0.0']

entry_points = \
{'console_scripts': ['csvtoexcel = csvtoexcel.csvtoexcel:main',
                     'exceltocsv = csvtoexcel.exceltocsv:main']}

setup_kwargs = {
    'name': 'csvtoexcel',
    'version': '0.1.2',
    'description': 'Command-line tool to convert CSV-files (.csv) to Excel-files (.xlsx) and vice versa',
    'long_description': 'csvtoexcel\n==========\ncsvtoexcel is a tool that converts a .csv file to .xlsx (Excel) and vice versa.\n\nBy default `csvtoexcel` creates a file with the same filename, but the file\nextension changed from ".csv" to ".xlsx".\nThe `-o`/`--output` option can be used choose a different filename for the\noutput. \n\nSimilarly `exceltocsv` converts a .xlsx file to .csv.\n\nUsage\n-----\n\n    > csvtoexcel <file.csv>\n    <Creates the file file.xlsx>\n\n    > csvtoexcel <file.csv> -o <other_file.xlsx>\n    <Creates the file other_file.xlsx>\n\n    > exceltocsv <file.csv>\n    <Creates the file file.xlsx>\n\n    > exceltocsv <file.csv> -o <other_file.xlsx>\n    <Creates the file other_file.xlsx>\n\nInstall\n-------\nThe recommended way to install `csvtoexcel` is via [pipx]:\n\n    pipx csvtoexcel\n\n[pipx]: https://github.com/pypa/pipx',
    'author': 'Malthe Jørgensen',
    'author_email': 'malthe.jorgensen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/malthejorgensen/csvtoexcel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
