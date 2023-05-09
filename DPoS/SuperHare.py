from collections import defaultdict
from typing import List, Tuple

def calculate_quota(total_votes: int, num_seats: int) -> float:
    #Calculate the quota for SuperHare.
    return total_votes / num_seats + 1

def distribute_surplus_votes(candidate_votes: float, quota: float) -> Tuple[float, defaultdict]:
    #Distribute surplus votes to other candidates.
    surplus = candidate_votes - quota
    redistributed_votes = defaultdict(float)
    if surplus > 0:
        for pref_list in candidate_preferences:
            if candidate_id in pref_list:
                pref_index = pref_list.index(candidate_id)
                for i in range(pref_index+1, len(pref_list)):
                    pref_candidate = pref_list[i]
                    redistributed_votes[pref_candidate] += surplus * (candidate_votes / (candidate_votes + surplus))
        candidate_votes -= surplus
    return candidate_votes, redistributed_votes

def eliminate_candidate(candidate_id: int, candidate_votes: float, candidate_preferences: List[List[int]]) -> Tuple[float, defaultdict]:
    #Eliminate a candidate and transfer their votes to other candidates.
    redistributed_votes = defaultdict(float)
    for pref_list in candidate_preferences:
        if candidate_id in pref_list:
            pref_index = pref_list.index(candidate_id)
            for i in range(pref_index+1, len(pref_list)):
                pref_candidate = pref_list[i]
                redistributed_votes[pref_candidate] += candidate_votes / (len(pref_list) - pref_index)
    candidate_votes = 0
    return candidate_votes, redistributed_votes

def calculate_vote_values(candidate_votes: float, num_seats_won: int) -> float:
    #Calculate the vote value of a candidate.
    return candidate_votes / (num_seats_won + 1)

def superhare(candidate_votes: List[float], candidate_preferences: List[List[int]], num_seats: int) -> List[int]:
    #Perform SuperHare algorithm to elect candidates.
    num_candidates = len(candidate_votes)
    quota = calculate_quota(sum(candidate_votes), num_seats)
    elected_candidates = []
    while len(elected_candidates) < num_seats:
        # Calculate vote values for each candidate
        vote_values = [calculate_vote_values(candidate_votes[i], elected_candidates.count(i)) for i in range(num_candidates)]
        # Find candidate(s) with highest vote value
        max_vote_value = max(vote_values)
        max_candidates = [i for i, value in enumerate(vote_values) if value == max_vote_value]
        # If only one candidate has the highest vote value, elect them
        if len(max_candidates) == 1:
            candidate_id = max_candidates[0]
            elected_candidates.append(candidate_id)
            candidate_votes[candidate_id], redistributed_votes = distribute_surplus_votes(candidate_votes[candidate_id], quota)
            for redistributed_candidate, redistributed_vote in redistributed_votes.items():
                candidate_votes[redistributed_candidate] += redistributed_vote
        # If multiple candidates have the highest vote value, eliminate the candidate with the fewest votes
        else:
            min_votes = float('inf')
            min_candidate_id = None
            for candidate_id in max_candidates:
                if candidate_votes[candidate_id] < min_votes:
                    min_votes = candidate_votes[candidate_id]
                    min_candidate_id = candidate_id
            candidate_votes[min_candidate_id], redistributed_votes = eliminate_candidate(min_candidate_id, candidate_votes[min_candidate_id], candidate_preferences)
            for redistributed_candidate, redistributed_vote in redistributed_votes.items():
                candidate_votes[redistributed_candidate] += redistributed_vote
    return elected_candidates
