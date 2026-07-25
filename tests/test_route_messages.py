import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solution import route_messages


def test_sample_0_linear_chain():
    messages = [
        {"from": "Planner", "to": "Researcher", "id": 1},
        {"from": "Researcher", "to": "Critic", "id": 2},
        {"from": "Critic", "to": "Writer", "id": 3},
    ]
    assert route_messages(messages) == ["Planner", "Researcher", "Critic", "Writer"]


def test_sample_1_deadlock_cycle():
    messages = [
        {"from": "Planner", "to": "Researcher", "id": 1},
        {"from": "Researcher", "to": "Critic", "id": 2},
        {"from": "Critic", "to": "Researcher", "id": 3},
    ]
    assert route_messages(messages) == "DEADLOCK"


def test_single_agent_pair():
    messages = [{"from": "A", "to": "B", "id": 1}]
    assert route_messages(messages) == ["A", "B"]


def test_self_loop_is_deadlock():
    messages = [{"from": "A", "to": "A", "id": 1}]
    assert route_messages(messages) == "DEADLOCK"


def test_cycle_not_involving_entry_point():
    # Entry -> B -> C -> B (cycle between B and C, Entry has no incoming edge)
    messages = [
        {"from": "Entry", "to": "B", "id": 1},
        {"from": "B", "to": "C", "id": 2},
        {"from": "C", "to": "B", "id": 3},
    ]
    assert route_messages(messages) == "DEADLOCK"


def test_multiple_outgoing_edges_tie_broken_by_id():
    # Planner hands off to both Researcher and Auditor; id determines order.
    messages = [
        {"from": "Planner", "to": "Auditor", "id": 2},
        {"from": "Planner", "to": "Researcher", "id": 1},
        {"from": "Researcher", "to": "Critic", "id": 3},
        {"from": "Auditor", "to": "Critic", "id": 4},
    ]
    result = route_messages(messages)
    assert result[0] == "Planner"
    # Researcher's edge (id=1) is before Auditor's edge (id=2)
    assert result.index("Researcher") < result.index("Auditor")
    assert result[-1] == "Critic"
    assert set(result) == {"Planner", "Researcher", "Auditor", "Critic"}


def test_out_of_order_ids_still_resolve_correctly():
    # Messages listed out of arrival order; id should still drive tie-break.
    messages = [
        {"from": "Critic", "to": "Writer", "id": 3},
        {"from": "Planner", "to": "Researcher", "id": 1},
        {"from": "Researcher", "to": "Critic", "id": 2},
    ]
    assert route_messages(messages) == ["Planner", "Researcher", "Critic", "Writer"]


def test_no_entry_point_all_in_cycle():
    messages = [
        {"from": "A", "to": "B", "id": 1},
        {"from": "B", "to": "C", "id": 2},
        {"from": "C", "to": "A", "id": 3},
    ]
    assert route_messages(messages) == "DEADLOCK"


def test_diamond_shaped_dag():
    # Planner -> Researcher, Planner -> Auditor, both -> Critic
    messages = [
        {"from": "Planner", "to": "Researcher", "id": 1},
        {"from": "Planner", "to": "Auditor", "id": 2},
        {"from": "Researcher", "to": "Critic", "id": 3},
        {"from": "Auditor", "to": "Critic", "id": 4},
    ]
    result = route_messages(messages)
    assert result[0] == "Planner"
    assert result[-1] == "Critic"
    assert len(result) == 4
    assert len(set(result)) == 4
