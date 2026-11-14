from collections import deque

from groups import create_group, group


def gale_shapley(men, women):
    """Accept groups or ID-to-Person dictionaries; return {woman_id: man_id}."""
    # Normalize group objects into dictionaries for direct lookup by member ID.
    if isinstance(men, group):
        men = {person.get_id(): person for person in men.get_members()}
    if isinstance(women, group):
        women = {person.get_id(): person for person in women.get_members()}

    if len(men) != len(women):
        raise ValueError("Groups must have equal sizes")

    # Every man starts unmatched. The queue holds men who still need to propose.
    free_men = deque(men)
    # Engagements are tentative: each woman keeps her preferred proposal so far.
    matches = {}

    # IDs are already ordered from first choice to last choice.
    preferences = {
        man_id: man.get_all_rankings()
        for man_id, man in men.items()
    }
    # Remember each man's next choice so he never proposes to the same woman twice.
    next_proposal = {man_id: 0 for man_id in men}
    # Precompute ranks so each proposal comparison takes constant time.
    women_ranks = {
        woman_id: {man_id: rank for rank, man_id in enumerate(woman.get_all_rankings())}
        for woman_id, woman in women.items()
    }

    while free_men:
        # The next free man proposes to his highest-ranked untried choice.
        man_id = free_men.popleft()
        woman_id = preferences[man_id][next_proposal[man_id]]
        next_proposal[man_id] += 1

        if woman_id not in matches:
            # An unmatched woman accepts her first proposal.
            matches[woman_id] = man_id
        else:
            current_man_id = matches[woman_id]
            # A smaller rank means she prefers the new proposer to her partner.
            if women_ranks[woman_id][man_id] < women_ranks[woman_id][current_man_id]:
                # Her previous partner continues with his next proposal.
                matches[woman_id] = man_id
                free_men.append(current_man_id)
            else:
                # A rejected man returns to the queue to try his next choice.
                free_men.append(man_id)

    # With complete preference lists and equal group sizes, everyone is matched.
    return matches


if __name__ == "__main__":
    # Generate an example and display preferences followed by the stable matching.
    group1 = create_group(5)
    group2 = create_group(5)

    print("Group 1 Members (IDs from first choice to last):")
    for member in group1.get_members():
        print(f"ID: {member.get_id()}, Rankings: {member.get_all_rankings()}")

    print("\nGroup 2 Members (IDs from first choice to last):")
    for member in group2.get_members():
        print(f"ID: {member.get_id()}, Rankings: {member.get_all_rankings()}")

    print("\nStable matching (Group 1 -> Group 2):")
    for woman_id, man_id in gale_shapley(group1, group2).items():
        print(f"{man_id} -> {woman_id}")
