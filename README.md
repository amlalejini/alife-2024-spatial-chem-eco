# Role of spatial structure in a chemical ecology model

## Setup

### Git submodules

```
git submodule update --init --recursive
```

After updating the submodules, check that you have the `chemical-ecology` dependency.
You should be able to compile the chemical ecology software:

```
cd third-party/chemical-ecology
make debug
```

### Set up your python virtual environment

From the terminal inside this directory:

```
python -m venv pyenv
pip install -r requirements
```

## Running the code

(every time you open a new terminal and want to work/run this code)

From the terminal inside this directory:

- Activate the python virtual environment
  - `source pyenv/bin/activate`
- If you haven't installed the dependencies, install the dependencies:
  - `pip install -r requirements.txt`