#TODO: write bad algorithm
from groups import *



group1 = create_group(5)
group2 = create_group(5)


def check_list(test_list,group1,group2):
    for i in range(0,len(test_list)):
        for j in range(0,len(test_list)):
            guy = group1.get_member(test_list[i][0])
            girl = group2.get_member(test_list[j][1])
            if i != j:
                


def find_matches(group1:group, group2:group):
    pairings = list[list(int,int)*group2.get_size()]
    counter = 0
    testList = list(set()*group2.get_size())
    for i in range(0,group1.get_size()):
        for j in range(0,group2.get_size()):
            if j not in testList[counter]:
                pairings[counter].append(i,j)
                testList[counter].add(j)
                counter = counter +1

    for option in pairings:
        if check_list(option,group1, group2):
            return option
        


if __name__ == "__main__":
    print("Group 1 Members:")
    for member in group1.get_members():
        print(f"ID: {member.get_id()}, Ranking: {member.get_ranking(member.get_id())}")

    print("\nGroup 2 Members:")
    for member in group2.get_members():
        print(f"ID: {member.get_id()}, Ranking: {member.get_ranking(member.get_id())}")