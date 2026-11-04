from itertools import permutations
from groups import *



group1 = create_group(5)
group2 = create_group(5)


def check_list(test_list,group1,group2):
    for i in range(0,len(test_list)):
        for j in range(0,len(test_list)):
            guy = group1.get_member(test_list[i][0])
            girl = group2.get_member(test_list[j][1])
            if i != j:
                if (guy.get_ranking(test_list[j][1]) < guy.get_ranking(test_list[i][1])
                        and girl.get_ranking(test_list[i][0]) < girl.get_ranking(test_list[j][0])):
                    return False

    return True


def find_matches(group1:group, group2:group):
    if group1.get_size() != group2.get_size():
        raise ValueError("Groups must have equal sizes")

    for order in permutations(range(group2.get_size())):
        pairing = list(enumerate(order))
        if check_list(pairing, group1, group2):
            return pairing

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
