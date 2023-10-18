## Introduction

Add extra functions for use with pymupdf module

## Installation

1. Install dev environment

```
make install
```

2. Create wheel of the package

```
python setup.py bdist_wheel
```

3. Install the package

```
pip install dist/fitz_utils-0.0.13-py3-none-any.whl
```

4. Install the package with poetry (If you're using poetry) - OPTIONAL <br/>
   Copy the `dist/fitz_utils-0.0.13-py3-none-any.whl` into your project folder such as `your_project/packages/fitz-utils/fitz_utils-0.0.13-py3-none-any.whl`

```
poetry add packages/fitz-utils/fitz_utils-0.0.13-py3-none-any.whl
```
