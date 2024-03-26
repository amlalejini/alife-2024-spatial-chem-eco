# Local compilation

You will need a C++ compiler that supports at least C++17.
We used g++13 for all local compilations.

First, clone the `alife-2024-env-connectivity-influences-origins-of-adaptive-processes` repository, which contains the code needed to run our experiment software:
<https://github.com/amlalejini/alife-2024-env-connectivity-influences-origins-of-adaptive-processes.git>

Once cloned, `cd` into your local repository directory.
Then, initialize and update all of the git submodules:

```
git submodule update --init --recursive
```

This will download the correct version of the `chemical-ecology` repository into the `third-party` directory, which contains the implementation of the artificial ecology model that we used in our experiments.
Specifically, we used this version of the `chemical-ecology` code base:

- <https://github.com/amlalejini/chemical-ecology/tree/2024-01-09-spatial-struct-exp>
  - Commit hash: `9a7022c238e04103bad2e399477b7f9bbe2ec9f4`

To compile the model:

```
cd third-party/chemical-ecology
make native
```

This will create an executable `chemical-ecology`.

Once you have an executable, you can generate a configuration file by running:

```
./chemical-ecology --gen chemical-ecology.cfg
```

You may also use the configuration files from any of our experiments, which can be found in the `experiments` directory.


