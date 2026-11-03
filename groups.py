import random
class Person:
    def __init__(self, id, ranking):
        self.id = id
        self.ranking = ranking

    def get_id(self):
        return self.id
    def get_ranking(self, id):
        return self.ranking[id]

def create_person(id, size):
    arr = [0] * size
    for i in range(size):
        arr[i] = random.sample(range (0, size),size)  # Assuming you want to assign random rankings
    return Person(id, arr)

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