# Environmental connectivity influences the origination of adaptive processes

[![supplemental](https://img.shields.io/badge/go%20to-supplemental%20material-ff69b4)](https://lalejini.com/alife-2024-spatial-chem-eco/web-supplement)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10891182.svg)](https://doi.org/10.5281/zenodo.10891182)
[![OSF](https://img.shields.io/badge/data%20%40%20OSF-10.17605%2FOSF.IO%2FK3D8G-blue)](https://osf.io/k3d8g/)

This repository is associated with our submission to the 2024 Artificial Life conference, "Environmental connectivity influences the origination of adaptive processes".

## Overview

### Abstract

> Spatial structure is hypothesized to be an important factor in the origin of life, wherein encapsulated chemical reaction networks came together to form systems capable adaptive complexification via Darwinian evolution.
  In this work, we use a computational model to investigate
  how different patterns of environmental connectivity might influence the emergence of adaptive processes in simulated systems of self-amplifying networks of interacting chemical reactions (autocatalytic cycles, ``ACs'').
  Specifically, we measured adaptive dynamics of nine systems with distinct patterns of interactions among their constituent components, each on ten different patterns of environmental connectivity.
  We found that the pattern of connectivity can dramatically influence the emergence of adaptive processes; however, the effect of any particular spatial structure varied across systems of ACs.
  Relative to a well-mixed (fully connected) environment, each spatial structure that we investigated amplified adaptive processes for at least one system of ACs and suppressed adaptive processes for at least one other system.
  Our findings suggest that there may be no single environment that universally promotes the emergence of adaptive processes in a system of interacting components (e.g., ACs).
  Instead, the ideal environment for amplifying (or suppressing) adaptive dynamics will depend on the particularities of the system.

## Repository guide

- `bookdown/` - contains configuration for bookdown build of supplemental material
- `docs/` - contains supplemental documentation of our methods, including data availability, guides for compiling experiment software, etc.
- `experiments/` - contains HPC job submission scripts, configuration files, and data analyses for experiments
- `scripts/` - contains generically useful scripts used in this work
- `web-supplement/` - contains the compiled (using bookdown) web-based supplemental material