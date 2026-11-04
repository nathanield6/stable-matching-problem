from collections import deque

from groups import create_group, group


def gale_shapely(men, women):
    """Accept groups or ID-to-Person dictionaries; return {woman_id: man_id}."""
    if isinstance(men, group):
        men = {person.get_id(): person for person in men.get_members()}
    if isinstance(women, group):
        women = {person.get_id(): person for person in women.get_members()}

    if len(men) != len(women):
        raise ValueError("Groups must have equal sizes")

    free_men = deque(men)
    matches = {}

    # Rankings store ranks by ID, so sort IDs from best to worst.
    preferences = {
        man_id: sorted(women, key=man.get_ranking)
        for man_id, man in men.items()
    }
    next_proposal = {man_id: 0 for man_id in men}

    while free_men:
        man_id = free_men.popleft()
        woman_id = preferences[man_id][next_proposal[man_id]]
        next_proposal[man_id] += 1
        woman = women[woman_id]

        if woman_id not in matches:
            matches[woman_id] = man_id
        else:
            current_man_id = matches[woman_id]
            if woman.get_ranking(man_id) < woman.get_ranking(current_man_id):
                # Her previous partner continues with his next proposal.
                matches[woman_id] = man_id
                free_men.append(current_man_id)
            else:
                free_men.append(man_id)

    return matches


if __name__ == "__main__":
    group1 = create_group(5)
    group2 = create_group(5)

    print("Group 1 Members (rank 0 is best):")
    for member in group1.get_members():
        print(f"ID: {member.get_id()}, Rankings: {member.get_all_rankings()}")

    print("\nGroup 2 Members (rank 0 is best):")
    for member in group2.get_members():
        print(f"ID: {member.get_id()}, Rankings: {member.get_all_rankings()}")

    print("\nStable matching (Group 1 -> Group 2):")
    for woman_id, man_id in gale_shapely(group1, group2).items():
        print(f"{man_id} -> {woman_id}")
