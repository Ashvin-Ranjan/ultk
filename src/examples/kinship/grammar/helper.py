def closure(x, y, a, visited=None):
    # Track visited nodes to avoid infinite loops
    if visited is None:
        visited = set()
    if (x, y) in visited:
        return False
    visited.add((x, y))

    # Base case: direct relationship exists
    if a(x)(y):
        return True

    # Recursive case: check for intermediary z
    return any(a(x)(z) and closure(z, y, a, visited) for z in universe if z != x)

helpers = {
    "closure": closure
}