def combiner(first: list, after: list) -> list:
    if len(after) == 0:
        return first
    out = []
    for i in range(0, len(after)):
        out.append(first+[after[i]])
    return out

print(combiner([0], [1, 2, 3]))
print(combiner([1], [2]))
print(combiner([1, 2, 3], [2, 3, 4]))
print("END COMBINER TEST")


def missing(total: list, already: list) -> list:
    missed = []
    for element in total:
        if total.count(element) > already.count(element) + missed.count(element):
            missed.append(element)
    return missed


print(missing([1, 2, 3, 3, 2, 1, 5, 6, 3, 6, 3], [1, 2, 3, 3]))
print(missing([1, 2], [1]))
print("END Missing test")


def permutations(array:  list) -> list:
    arrayed_array = [[array[i]] for i in range(0, len(array))]
    out_perms = arrayed_array
    for i in range(0, len(array)-1):
        j_len = len(out_perms)
        for j in range(0, j_len):
            combined = combiner(out_perms[0], missing(array, out_perms[0]))
            for k in range(0, len(combined)):
                out_perms.append(combined[k])
            out_perms.pop(0)
    return out_perms

print(permutations([1, 2, 3, 4]))
print(len(permutations([1, 2, 3, 4])))
