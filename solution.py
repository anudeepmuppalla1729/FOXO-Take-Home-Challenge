from collections import defaultdict, deque


def route_messages(messages: list[dict]) -> list[str] | str:

    # Sort by 'id' (arrival order) -- this is there to correctly 
    # break ties when an agent has multiple outgoing handoffs.
    messages.sort(key=lambda x: x["id"])

    adj = defaultdict(list) 
    indegree = defaultdict(int) # dict for indegrees of each node
    agents = set()

    # Building the adjacency list and indegree list
    for msg in messages:
        u = msg["from"]
        v = msg["to"]

        agents.add(u)
        agents.add(v)

        adj[u].append(v)
        indegree[v] += 1
        indegree.setdefault(u, 0)

    # Initially the node with indegree zero is the starting node.
    entry = [node for node in agents if indegree[node] == 0]

    # If there are two or more initial nodes then it is a deadlock 
    if len(entry) != 1:
        return "DEADLOCK"

    q = deque(entry)
    order = []

    # Kahn's Algorithm: We are buliding the execution order by running all the 
    # outgoing dependencies of agents with zero incoming handoffs. 
    while q:

        node = q.popleft()
        order.append(node)

        for neigh in adj[node]:

            indegree[neigh] -= 1

            if indegree[neigh] == 0:
                q.append(neigh)

    # If every node or agent wasn't processed, it implies that a cycle is present, so DEADLOCK.
    if len(order) != len(agents):
        return "DEADLOCK"

    return order


if __name__ == "__main__":

    sample0 = [
        {"from": "Planner", "to": "Researcher", "id": 1},
        {"from": "Researcher", "to": "Critic", "id": 2},
        {"from": "Critic", "to": "Writer", "id": 3},
    ]

    print(route_messages(sample0))
    # ['Planner', 'Researcher', 'Critic', 'Writer'] should be printed 

    sample1 = [
        {"from": "Planner", "to": "Researcher", "id": 1},
        {"from": "Researcher", "to": "Critic", "id": 2},
        {"from": "Critic", "to": "Researcher", "id": 3},
    ]

    print(route_messages(sample1))
    # DEADLOCK should be printed
