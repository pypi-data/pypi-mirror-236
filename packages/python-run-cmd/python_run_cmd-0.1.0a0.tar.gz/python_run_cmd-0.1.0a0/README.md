# run-cmd
[![pytest](https://github.com/ffreemt/run-cmd/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/run-cmd/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/python-run-cmd.svg)](https://badge.fury.io/py/python-run-cmd)

Run a command within python

## Install it

```shell
pip install python-run-cmd
# pip install git+https://github.com/ffreemt/run-cmd
# poetry add git+https://github.com/ffreemt/run-cmd
# git clone https://github.com/ffreemt/run-cmd && cd run-cmd
```

## Use it
```python
from python_run_cmd import run_cmd

ret = run_cmd("ls -l")
if ret.returncode:
  print("Failed")
else:
  print("OK")

```
