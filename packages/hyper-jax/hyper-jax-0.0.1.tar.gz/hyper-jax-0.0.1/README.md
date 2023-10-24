# hyper-jax
[Hyperdimensional computing](https://en.wikipedia.org/wiki/Hyperdimensional_computing) with Jax. This library provides a very minimal implementation of MAP (Multiply, add, permute) operations over bipolar vectors originally proposed [here](https://www.researchgate.net/publication/215992330_Multiplicative_Binding_Representation_Operators_Analogy).

# Install

Coming soon...

# How to use
Generate 2 random vectors with dimension of 10 000
```
from generator import random_vectors

dimensions = 10000
count = 2

key = random.PRNGKey(0)
vectors = random_vectors(key, dimensions, count)
```

Bundle two hypervectors
```
from operation import bundle, unbundle

hypervector = bundle(vectors[0], vectors[1])
```
Unbundle two hypervectors
```
# original_vector == vectors[0]
original_vector = unbundle(hypervector, vectors[1])
```
Bind two hypervectors
```
from operation import bind, unbind

bound_vector = bind(vectors[0], vectors[1])
```
Unbind the hypervector
```
# original_vector == vectors[1]
unbound_vector = unbind(bound_vector, vectors[0])
```
