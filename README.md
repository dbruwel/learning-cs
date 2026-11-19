# Learning CS
This is a repo to store the code I write while learning CS related concepts. I'm not formally learning CS, this is mostly just situations where I ask myself "how does xyz work" and then when reading the answer think that I should try to implement it. More often than not, I'll read about some CS concept and decide not to implement it, so this is a very sparse repo.


> **Disclamer**: This is puerly for learning for me, it's not polished, it's not documented in detail (unless I thought that writing how soething works would help me understand it), and it's not structured as a package, rather it's a collection of files in some structure.

## Structure
```
src/
├ cryptography/
├ dsa/          # Data structures and algorithms
└ numerics/     # Numerics, e.g. numeric integration
```

## Contents
### Cryptography
> The keys used in any of the cryptography examples are not real keys, their presence on GitHub is not a security issue.
**Eliptic Curve Cryptography (ECC)**: Using the EC group to do standard DH key exchange.

### DSA
**Graphs**:
*Floyd Warshall*: Finds the shortest path between all pairs of nodes on a graph

### Numerics
**Integrators**:
*Quadrature*: Finds the integral of a 1D function by slicing it up and using polynomial interpolation.
