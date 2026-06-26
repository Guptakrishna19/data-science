"""
Dot product and matrix multiplication implemented from scratch,
verified against NumPy.
"""
import numpy as np


# ---------------------------------------------------------
# 1. Dot product from scratch
# ---------------------------------------------------------
def dot_scratch(a, b):
    """Dot product of two 1D vectors (lists)."""
    if len(a) != len(b):
        raise ValueError("Vectors must be the same length")
    total = 0
    for ai, bi in zip(a, b):
        total += ai * bi
    return total


# ---------------------------------------------------------
# 2. Matrix multiplication from scratch
# ---------------------------------------------------------
def matmul_scratch(A, B):
    """Multiply matrix A (m x n) by matrix B (n x p) -> result (m x p)."""
    m = len(A)          # rows in A
    n = len(A[0])        # cols in A == rows in B
    if len(B) != n:
        raise ValueError("Inner dimensions must match: A is m x n, B must be n x p")
    p = len(B[0])         # cols in B

    # result is m x p, initialised to zeros
    result = [[0] * p for _ in range(m)]

    for i in range(m):           # each row of A
        for j in range(p):       # each column of B
            s = 0
            for k in range(n):   # walk along the shared dimension
                s += A[i][k] * B[k][j]
            result[i][j] = s
    return result


# ---------------------------------------------------------
# Verification against NumPy
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== DOT PRODUCT ===")
    a = [1, 2, 3]
    b = [4, 5, 6]

    my_dot = dot_scratch(a, b)
    np_dot = np.dot(a, b)

    print(f"From scratch : {my_dot}")
    print(f"NumPy        : {np_dot}")
    print(f"Match        : {my_dot == np_dot}\n")

    print("=== MATRIX MULTIPLICATION ===")
    A = [[1, 2, 3],
         [4, 5, 6]]          # 2x3
    B = [[7, 8],
         [9, 10],
         [11, 12]]           # 3x2

    my_C = matmul_scratch(A, B)
    np_C = (np.array(A) @ np.array(B)).tolist()

    print("From scratch:")
    for row in my_C:
        print(row)

    print("\nNumPy (@):")
    for row in np_C:
        print(row)

    print(f"\nMatch: {my_C == np_C}")

