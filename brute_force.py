from itertools import permutations
from groups import *



# Create sample groups for the demonstration at the bottom of the file.
group1 = create_group(5)
group2 = create_group(5)


def check_list(test_list,group1,group2):
    """Return whether a list of (group1 ID, group2 ID) pairs is stable."""
    # Compare each group1 member with every group2 member in another pair.
    for i in range(0,len(test_list)):
        for j in range(0,len(test_list)):
            guy = group1.get_member(test_list[i][0])
            girl = group2.get_member(test_list[j][1])
            if i != j:
                # Lower ranks mean stronger preferences. If both prefer each
                # other over their assigned partners, they form a blocking pair.
                if (guy.get_ranking(test_list[j][1]) < guy.get_ranking(test_list[i][1])
                        and girl.get_ranking(test_list[i][0]) < girl.get_ranking(test_list[j][0])):
                    return False

    # No blocking pair exists, so the matching is stable.
    return True


def find_matches(group1:group, group2:group):
    """Try every possible pairing and return the first stable matching."""
    if group1.get_size() != group2.get_size():
        raise ValueError("Groups must have equal sizes")

    # Keep group1 IDs fixed and permute group2 IDs to cover all n! matchings.
    for order in permutations(range(group2.get_size())):
        # Each index is a group1 ID; its value is the assigned group2 ID.
        pairing = list(enumerate(order))
        if check_list(pairing, group1, group2):
            return pairing

    # Report failure if none of the candidate matchings passes the stability check.
    return None
        


if __name__ == "__main__":
    print("Group 1 Members (IDs from first choice to last):")
    for member in group1.get_members():
        print(f"ID: {member.get_id()}, Rankings: {member.get_all_rankings()}")

    print("\nGroup 2 Members (IDs from first choice to last):")
    for member in group2.get_members():
        print(f"ID: {member.get_id()}, Rankings: {member.get_all_rankings()}")

    print("\nFirst stable matching:")
    print(find_matches(group1, group2))
