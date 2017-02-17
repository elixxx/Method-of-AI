from validator import Validator
import random
from itertools import chain


class CandidateAI:
    """ Implement the Candidate and the Function used by the genetic Algorithm
    """
    _fitness = None

    def __init__(self, assignments):
        """ Create an Candidate


        :param assignments:List of Lists. Possible assignments of Lectures of Instructors of rooms to time and day.
        EXAMPLE:
                <<instructor_idx,room_idx,time_idx,day_idx>
                 <instructor_idx,room_idx,time_idx,day_idx>
                                .....
                 <instructor_idx,room_idx,time_idx,day_idx>>
        """
        self.assignments = assignments

        # Initialize the Constraint Validator
        self._validator = Validator()

    def crossover(self, other_candidate, strategy="onePointSwap"):
        """Exchange of Properties of two Candidates

        :param other_candidate: Object of the other Candidate, given by the genetic Algorithm.
        :param strategy: Crossover Strategy that should be used.
        :return: empty
        """
        self._fitness = None
        if (strategy == "onePointSwap"):
            self._crossing_one_point_swap(other_candidate)
        elif strategy == "twoPointSwap":
            self._crossing_two_point_swap(other_candidate)

    def mutation(self, mutation_rate):
        """ Check which Property should changed and change it

        :param mutation_rate: Probability (from 0.0 ... 1.0) of mutation for each Property
        :return: empty
        """
        # Reset Fitness score
        self._fitness = None

        # Get index Property
        for lecture_idx, lecture in enumerate(self.assignments):
            for element_idx, element in enumerate(self.assignments[lecture_idx]):
                # Check whether property classifies for mutation
                if (random.random() < mutation_rate):
                    if element_idx == 2:  # Days only 1 to 3
                        self.assignments[lecture_idx][element_idx] = randTo(3)
                    else:  # Else 1 to 5
                        self.assignments[lecture_idx][element_idx] = randTo(5)

    def get_diversity(self, other_candidate):
        """ Compare the error between two Candidates

        :param other_candidate:
        :return: difference between Candidates in percent
        """
        div = 0
        all_elements = 0
        for lecture_idx in range(len(self.assignments)):
            for idx_inner in range(len(self.assignments[lecture_idx])):
                all_elements += 1
                if self.assignments[lecture_idx][idx_inner] != other_candidate.assignments[lecture_idx][idx_inner]:
                    div += 1

        return div/ all_elements

    def get_fitness(self):
        """ Evaluate Candidate

        :return: Fitness from 0 to 1 and 1.5 if it is a valid Solution
        """
        if (self._fitness is None):
            constraint_errors = self._validator.check(self.assignments)
            if constraint_errors == 0:
                self._fitness = 1.5
            else:
                self._fitness = 1 / constraint_errors
        return self._fitness

    def _crossing_one_point_swap(self, other_candidate):
        """ One Point crossing

        :param other_candidate:
        :return:
        """
        cut_idx = randTo(4*19+3)  # 19 times 4 cut points + 3 in the end
        swap_idx = None
        if 0.5 < random.random():
            swap_idx = range(cut_idx, 4*20-1)  # Forward from idx
        else:
            swap_idx = range(0, cut_idx)# Backward from idx
        for idx in swap_idx:
            # Split long index in Lecture and field index
            lecture_idx = int( idx /4 )
            field_idx = idx % 4
            tmp = other_candidate.assignments[lecture_idx][field_idx]
            other_candidate.assignments[lecture_idx][field_idx] = self.assignments[lecture_idx][field_idx]
            self.assignments[lecture_idx][field_idx] = tmp

    def _crossing_two_point_swap(self, other_candidate):
        """ Two Point Crossing

        :param other_candidate:
        :return:
        """
        cut_from = random.randint(0, 4*19+3)
        cut_to = random.randint(0, 4*19+3)

        if cut_from < cut_to:
            swap_idx = range(cut_from, cut_to)
        else:
            swap_idx = range(cut_to, cut_from)

        for idx in swap_idx:
            # Split long index in Lecture and field index
            lecture_idx = int( idx /4 )
            field_idx = idx % 4
            tmp = other_candidate.assignments[lecture_idx][field_idx]
            other_candidate.assignments[lecture_idx][field_idx] = self.assignments[lecture_idx][field_idx]
            self.assignments[lecture_idx][field_idx] = tmp

def create_random_CandidateAI():
    """ Create a random Solution of a Candidate

    :return:
    """
    candidates = list()
    # <I_idx,room_idx,time_idx,day_idx>
    for L_idx in range(20):
        candidates.append([randTo(5), randTo(5), randTo(3), randTo(5)])
    return CandidateAI(candidates)


def randTo(x):
    return random.randint(1, x)
