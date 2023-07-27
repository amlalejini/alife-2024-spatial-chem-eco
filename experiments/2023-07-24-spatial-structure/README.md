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