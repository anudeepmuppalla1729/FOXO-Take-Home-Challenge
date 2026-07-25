# Agent Handoff Router

## Problem

In a multi-agent system, each message declares who an agent is handing
off to next. Given the messages from one session, figure out the valid
execution order of agents, or detect a deadlock — a cycle where agents
just keep handing off to each other with no exit.

## Approach

This is basically a topological sort with cycle detection on a directed
graph.

- Each **agent** is a node
- Each **message** `{"from": u, "to": v, "id": n}` is a directed edge `u -> v`

So something like:

```
Planner -> Researcher -> Critic -> Writer
```

is just a chain in the graph, and we want to find that ordering (or spot
a cycle).

**Steps (Kahn's algorithm)**

1. Sort the messages by `id` first. Doing this means that whenever we
   later walk an agent's outgoing edges, we naturally walk them in the
   order they arrived, so ties (like one agent handing off to two
   different agents) get resolved in arrival order automatically instead
   of depending on whatever order the messages happened to be passed in.
2. Build an adjacency list and an in-degree count from the sorted
   messages.
3. Find the entry point — the one agent with in-degree 0. If there isn't
   exactly one, return `"DEADLOCK"` right away.
4. Run Kahn's BFS. Start with just the entry point in the queue, since
   it's the only agent with nothing blocking it. Then repeat:
   - pop a node from the front of the queue and add it to the result
     (this is the agent "running")
   - for each agent it hands off to, decrement that agent's in-degree
     by 1, since one of the handoffs it was waiting on just happened
   - if an agent's in-degree hits 0, that means everyone who was
     supposed to hand off to it already has, so it's ready — push it
     into the queue

   Because the edges were added in `id` order back in step 2, agents
   get pushed and popped in the correct arrival order without any
   extra bookkeeping.
5. If every agent made it into the result, that's the execution order.
   If some agents got left out, they never hit in-degree 0, which means
   they're stuck in a cycle — return `"DEADLOCK"`.

## Complexity

Let `V` = number of agents, `E` = number of messages.

- Time: `O(E log E + V)` — sorting the messages dominates, the BFS part
  itself is linear
- Space: `O(V + E)` for the adjacency list, in-degree map, and queue

## Files

```
solution.py                    # route_messages implementation
tests/test_route_messages.py   # pytest test suite
```

## Running it

```bash
# runs the two sample inputs from the problem statement
python solution.py

# runs the test suite
pip install pytest
python -m pytest tests/ -v
```

## What the tests cover

- Both sample cases from the problem statement
- A simple two-agent case
- Self-loop (should be a deadlock)
- A cycle that doesn't involve the entry point
- No valid entry point at all (every agent has an incoming edge)
- One agent with multiple outgoing handoffs, checking the `id` tie-break
- Messages passed in out of arrival order
- A diamond-shaped graph (one agent fans out, then it fans back in)
- A longer 5-agent chain