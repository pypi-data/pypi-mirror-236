import jax.numpy as jnp
from jax import random, jit

def random_vectors(key, dimensions=100, count=1):
    vec = random.bernoulli(key, 0.5, [count, dimensions])
    vec = jnp.where(vec, 1.0, -1.0)
    return vec
