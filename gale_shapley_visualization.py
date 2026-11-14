from collections import deque

from groups import group


def gale_shapley(men, women, *, on_proposal=None):
    """Return {woman_id: man_id} from groups or ID-to-Person dictionaries.

    If supplied, on_proposal receives a snapshot after each proposal decision.
    """
    if isinstance(men, group):
        men = {person.get_id(): person for person in men.get_members()}
    if isinstance(women, group):
        women = {person.get_id(): person for person in women.get_members()}

    if len(men) != len(women):
        raise ValueError("Groups must have equal sizes")

    free_men = deque(men)
    matches = {}

    # IDs are already ordered from first choice to last choice.
    preferences = {
        man_id: man.get_all_rankings()
        for man_id, man in men.items()
    }
    next_proposal = {man_id: 0 for man_id in men}

    while free_men:
        man_id = free_men.popleft()
        woman_id = preferences[man_id][next_proposal[man_id]]
        next_proposal[man_id] += 1
        woman = women[woman_id]

        current_man_id = matches.get(woman_id)
        ranks = None
        if current_man_id is None:
            matches[woman_id] = man_id
            status = "Accepted"
        else:
            ranks = (woman.get_ranking(man_id), woman.get_ranking(current_man_id))
            if ranks[0] < ranks[1]:
                # Her previous partner continues with his next proposal.
                matches[woman_id] = man_id
                free_men.append(current_man_id)
                status = "Switched"
            else:
                free_men.append(man_id)
                status = "Rejected"

        if on_proposal is not None:
            on_proposal({
                "status": status,
                "active": (man_id, woman_id),
                "previous": current_man_id,
                "ranks": ranks,
                "pairs": sorted((man, woman) for woman, man in matches.items()),
            })

    return matches
