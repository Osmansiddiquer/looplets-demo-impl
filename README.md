The goal is to implement the Looplets language.

# Looplets
Looplets are abstract descriptions of regular or irregular pat-
terns in a sequence of values, together with the code needed
to iterate over the sequence. Looplets represent sequences
using hierarchical descriptions of the values within each
region or subregion. Regions are specified by their absolute
starting and ending index, referred to together as an extent.

# Example:

Considering val is a vector representation of a lower-triangular matrix, the following looplet Pipeline
allows us to iterate over the lower-triangular matrix as if it were a matrix:
```
val = [1, 2, 3, 4, 5, 6]
#  1 0 0
#  2 3 0
#  4 5 6

offset = i*(i-1)/2
matrix = Pipeline(
    Phase(
        stride = i,
        body = Lookup(
            body(j) = val[offset+j]
        )
    ),
    Phase(
        body = Run(0)
    )
)
print(matrix[1, 2])
# 0
print(matrix[1, 1])
# 3
```

We shall start by implementing Pipeline, Phase, Lookup, and Run in python.


To represt a 2D matrix with all zeros, one can do:

```
A = Pipeline(
    Phase(
        Run(
            Pipeline(
                Phase(
                    Run(0),
                )
            )
        )
    )
)
```

The following nested pipeline represents a row of zeros:
Pipeline(
            Phase(
                Run(0),
            )
        )

Note, that the matrix is infinite. This is because this is an iterator.
Underneath, A is a generator function that yields the values of the matrix
according to its definition.


