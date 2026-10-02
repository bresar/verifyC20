"""
Verification: Fixed 3-coloring (pattern 3,1,2,1 repeated) on C20
- k=3: List all pairwise disjoint A1 ∪ A2 ∪ A3
- k=4: Search for existence of a 4-partition
"""

from itertools import combinations

# ============================================================
# 1. Graph setup
# ============================================================
n = 20
coloring = [3, 1, 2, 1] * 5  # pattern [3,1,2,1] repeated 5 times


def dist(i, j):
    """Shortest distance between two vertices on cycle C20"""
    return min(abs(i - j), n - abs(i - j))


def is_dom_broadcast(subset):
    """Check if a vertex subset is a dominating broadcast"""
    if not subset:
        return False
    for v in range(n):
        if not any(dist(v, u) <= coloring[u] for u in subset):
            return False
    return True


# ============================================================
# 2. Precompute all dominating broadcast subsets (sizes 4-8)
# ============================================================
print("=" * 70)
print("Precomputing all dominating broadcast subsets")
print("=" * 70)

dom = {}
for size in [4, 5, 6, 7, 8]:
    dom[size] = []
    for subset in combinations(range(n), size):
        if is_dom_broadcast(list(subset)):
            dom[size].append(set(subset))
    print(f"  Size {size}: found {len(dom[size])}")

print()

# ============================================================
# 3. k=3: List all pairwise disjoint A1 ∪ A2 ∪ A3
# ============================================================
print("=" * 70)
print("k=3: List all pairwise disjoint A1 ∪ A2 ∪ A3")
print("Condition: (A1∩A2) ∪ (A1∩A3) ∪ (A2∩A3) = ∅")
print("=" * 70)
print()

size_combos_3 = [(4, 4, 4), (4, 4, 5), (4, 4, 6), (4, 5, 5), (5, 5, 5)]

for sizes in size_combos_3:
    print(f"Size combination {sizes}:")
    lists = [dom[s] for s in sizes]

    if any(len(lst) == 0 for lst in lists):
        print("  WARNING: Some size has no dominating subsets, skipping")
        print()
        continue

    union_set = set()
    count = 0
    max_display = 5

    for a1 in lists[0]:
        for a2 in lists[1]:
            if a1 & a2:
                continue
            for a3 in lists[2]:
                if (a1 & a3) or (a2 & a3):
                    continue
                union = frozenset(a1 | a2 | a3)
                if union not in union_set:
                    union_set.add(union)
                    count += 1
                    if count <= max_display:
                        print(f"  Union {count}: A1={sorted(a1)}, A2={sorted(a2)}, A3={sorted(a3)}")
                        print(f"           A1∪A2∪A3 = {sorted(union)}")
                        print(f"           |union| = {len(union)}")
                        print()

    print(f"  Total disjoint unions for this size combo: {count}")
    if count > max_display:
        print(f"  (Showing only first {max_display})")
    print()

# ============================================================
# 4. k=4: Search for a 4-partition
# ============================================================
print("=" * 70)
print("k=4: Search for 4-partition (A1 ∪ A2 ∪ A3 ∪ A4 = V(C20))")
print("Conditions: Each Ai is a dominating broadcast, pairwise disjoint")
print("=" * 70)
print()

size_combos_4 = [
    (4, 4, 4, 8),
    (4, 4, 5, 7),
    (4, 4, 6, 6),
    (4, 5, 5, 6),
    (5, 5, 5, 5),
]

found4 = False

for sizes in size_combos_4:
    print(f"Trying size combination {sizes}:")
    lists = [dom[s] for s in sizes]

    if any(len(lst) == 0 for lst in lists):
        print("  WARNING: Some size has no dominating subsets, skipping")
        print()
        continue


    def backtrack(level, selected):
        """Recursive backtracking: choose one subset from each list,
        pairwise disjoint, and the union covers all vertices."""
        if level == 4:
            union = set()
            for s in selected:
                union.update(s)
            return len(union) == n

        for subset in lists[level]:
            disjoint = True
            for s in selected:
                if subset & s:
                    disjoint = False
                    break
            if not disjoint:
                continue

            if backtrack(level + 1, selected + [subset]):
                return True
        return False


    if backtrack(0, []):
        found4 = True
        print(f"  FOUND partition!")
        break
    else:
        print("  NOT found")
        print()

# ============================================================
# 5. Final conclusion
# ============================================================
print("=" * 70)
print("Final Conclusion")
print("=" * 70)

if found4:
    print("WARNING: This 3-coloring CAN be partitioned into 4 dominating broadcast parts")
else:
    print("NOT found: 4-partition does not exist")
    print("Under all 5 size combinations, no 4 mutually disjoint")
    print("dominating broadcast subsets cover all vertices.")
    print()
    print("Therefore, this 3-coloring CANNOT be partitioned")
    print("into 4 dominating broadcast parts.")
    print()
    print("CONCLUSION: χ_{ρ,4}(C20) ≥ 4")
print("=" * 70)