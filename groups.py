import random
class Person:
    def __init__(self, id, ranking):
        self.id = id
        self.ranking = ranking

    def get_id(self):
        return self.id
    def get_ranking(self, id):
        return self.ranking[id]
    def get_all_rankings(self):
        return self.ranking

def create_person(id, size):
    # Each index is a person in the other group; rank 0 is best.
    return Person(id, random.sample(range(size), size))

class group:
    def __init__(self, size,people):
        self.size = size
        self.members = people

    def get_members(self):
        return self.members
    def get_size(self):
        return self.size
    def get_id(self):
        return self.id  
    def get_member(self, id):
        for member in self.members:
            if member.get_id() == id:
                return member
        return None

def create_group(size):
    people = []
    for i in range(size):
        person = create_person(i, size)
        people.append(person)
    return group(size, people)
