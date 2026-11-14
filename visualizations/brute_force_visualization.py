from itertools import permutations
from groups import group


def check_list(test_list, group1, group2, *, on_candidate=None):
    """Check one matching and optionally report its first blocking pair."""
    for i, (man_id, assigned_woman) in enumerate(test_list):
        for j, (assigned_man, woman_id) in enumerate(test_list):
            if i == j:
                continue
            man = group1.get_member(man_id)
            man_ranks = (man.get_ranking(woman_id), man.get_ranking(assigned_woman))
            if man_ranks[0] < man_ranks[1]:
                woman = group2.get_member(woman_id)
                woman_ranks = (woman.get_ranking(man_id), woman.get_ranking(assigned_man))
                if woman_ranks[0] < woman_ranks[1]:
                    if on_candidate is not None:
                        on_candidate({
                            "status": "Unstable",
                            "active": (man_id, woman_id),
                            "ranks": man_ranks + woman_ranks,
                            "pairs": list(test_list),
                        })
                    return False

    if on_candidate is not None:
        on_candidate({"status": "Stable", "active": None, "ranks": None, "pairs": list(test_list)})
    return True


def find_matches(group1: group, group2: group, *, on_candidate=None):
    """Return the first stable matching and optionally report every candidate."""
    if group1.get_size() != group2.get_size():
        raise ValueError("Groups must have equal sizes")

    for order in permutations(range(group2.get_size())):
        pairing = list(enumerate(order))
        if check_list(pairing, group1, group2, on_candidate=on_candidate):
            return pairing

    return None
