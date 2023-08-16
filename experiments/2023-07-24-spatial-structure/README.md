# 2023-07-24 Spatial structure

Initial exploratory experiment investigating whether/how spatial structure influences dynamics in the chemical ecology model.

Varies spatial structure:

```
well-mixed:
--nodes 100
toroidal-lattice: height x width
height 10
width 10
comet-kite:
--coresize 40
--tail-size 20
--additional-tails 40
linear-chain:
--nodes 100
barabasi:
--nodes 100
--edges 10
waxman:
--nodes 100
--beta 0.4
--alpha 0.2
```

Fixed parameters from `class1.sb` in `third-party/chemical-ecology/config/`:

```
-REPRO_THRESHOLD 10000000000 -MAX_POP 10000 -SEEDING_PROB 1 -DIFFUSION .549 -PROB_CLEAR 0 -WORLD_X 10 -WORLD_Y 10 -INTERACTION_SOURCE evolve/class1interaction_matrix.dat -N_TYPES 9 -UPDATES 1000
```

- N_TYPES = 9
- UPDATES = 1000
- MAX_POP = 10000
- V = 0
- DIFFUSION = 0.549
- SEEDING_PROB = 1.0
- PROB_CLEAR = 0.0
- REPRO_DILUTION = 0.1
- INTERACTION_SOURCE = class1 interaction matrix
- INTERACTION_MAGNITUDE 1
- PROB_INTERACTION 0.1


## `hpc/`

- `config/` contains configuration files necessary for all runs for this experiment
- `base_slurm_script.txt` template slurm submissions script, used by `gen-sub.py` to generate submission files for all experiment treatments (specified inside `gen-sub.py`)
- `gen-graphs.py` generates graph files for experiment (graph types specified inside `gen-graphs.py`)
- `gen-sub.py` generates slurm submission scripts, one for each treatment
- `job-gen.sh` runs `gen-graphs.py` and `gen-sub.py` parameterized appropriately for this experiment (and your account)
- `local-job-gen.sh` same as `job-gen.sh` but works locally on your machine for checking whether everything is being generated as expected