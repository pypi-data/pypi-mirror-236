import jax.numpy as jnp
from jax import random, jit

@jit
def bundle(a, b):
    return a + b

@jit
def bind(key, value):
    return key * value

@jit
def unbundle(a, b):
    return a + jnp.negative(b)

@jit
def unbind(value, key):
    return value * key

@jit
def permute(a, shifts=1):
    return jnp.roll(a, shifts)
