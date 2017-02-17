from collections import Counter


class Validator:
    def __init__(self):
        """ Define the Constraints

        """
        self._lectures = list()
        self._instructor = list()
        self._room = list()

        ###########Def Lectures
        lecture_idx = 0
        for i in range(5):  # 1-5
            lecture_idx += 1
            self._lectures.append(Lecture(lecture_idx, (1, 2, 4), (1, 2)))

        for i in range(5):  # 6-10
            lecture_idx += 1
            self._lectures.append(Lecture(lecture_idx, (1, 2, 4), (3, 4)))

        for i in range(5):  # 11-15
            lecture_idx += 1
            self._lectures.append(Lecture(lecture_idx, (1, 3, 5), (2, 5)))

        for i in range(5):  # 16-20
            lecture_idx += 1
            self._lectures.append(Lecture(lecture_idx, (1, 3, 5), (3, 5)))

        ##########Def Instructor
        self._instructor.append(Instructor(1, (2, 3, 4), (1, 2, 3)))
        self._instructor.append(Instructor(2, (1, 2, 3), (1, 2, 3)))
        self._instructor.append(Instructor(3, (4, 5), (1, 2, 3)))
        self._instructor.append(Instructor(4, (1, 2, 3, 4, 5), (2, 3)))
        self._instructor.append(Instructor(5, (1, 2, 3, 4, 5), (1, 2)))

        ##########Def room
        self._room.append(Room(1, (1,), (1, 2, 3)))
        self._room.append(Room(2, (1, 2, 3, 4), (1, 2, 3)))
        self._room.append(Room(3, (2, 3, 4, 5), (1, 2, 3)))
        self._room.append(Room(4, (1, 2, 3, 4, 5), (1,)))
        self._room.append(Room(5, (1, 2, 3, 4, 5), (3,)))

    def check(self, lectures):
        # <<I_idx,room_idx,time_idx,day_idx>
        # <I_idx,room_idx,time_idx,day_idx>
        # <...>
        # <I_idx,room_idx,time_idx,day_idx>> #20 time for each Lecture
        if len(lectures) != 20:
            print("Check Candidate Fail, len(candidate) != 20 ->" + str(len(lectures)))
        error = 0
        # One Lecture per Room and time             (room_idx,day_idx,time_idx)
        # One Instructor only one Lecture per time  (I_idx,day_idx,time_idx)
        # One Instructor can give 5 Lecture         (I_idx)
        self._counter_lecture_room = Counter()
        self._counter_instructor_time = Counter()
        self._counter_instructor_lecture = Counter()

        for lecture_idx, lecture in enumerate(lectures):
            error += self._check_one(lecture_idx, lecture)


        for cnt_per_room_time in self._counter_lecture_room.values():
            if cnt_per_room_time > 1:
                error +=1
        for cnt_per_instructor_time in self._counter_instructor_time.values():
            if cnt_per_instructor_time > 1:
                error += 1
        for cnt_per_instructor_lectures in self._counter_instructor_lecture.values():
            if cnt_per_instructor_lectures > 5:
                error += 1
        return error

    def _check_one(self, idx, lecture):
        # <I_idx, room_idx, time_idx, day_idx >
        # check Lecture constraints
        self._counter_lecture_room[(lecture[1], lecture[3], lecture[2])] += 1
        self._counter_instructor_time[(lecture[0], lecture[3], lecture[2])] += 1
        self._counter_instructor_lecture[(lecture[0])] += 1
        error = 0
        error += self._lectures[idx - 1].check_constraint(lecture[1], lecture[0])
        error += self._room[lecture[1] - 1].check_constraint(lecture[3], lecture[2])
        error += self._instructor[lecture[0] - 1].check_constraint(lecture[3], lecture[2])
        return error


class Room:

    def __init__(self, idx, day, time):
        """
        set availability of rooms in time slots
        :param idx:
        :param day:
        :param time:
        """
        self.idx = idx
        self.valid_days = day
        self.valid_times = time

    def check_constraint(self, day, time):
        """
        check constraint consistency
        :param day:
        :param time:
        :return: number of inconsistent constraints
        """
        error = 0
        if (day not in self.valid_days):
            error += 1
        if time not in self.valid_times:
            error += 1
        return error


class Instructor:

    def __init__(self, idx, day, time):
        """
        set availability of instructors in time slots
        :param idx:
        :param day:
        :param time:
        """
        self.idx = idx
        self.valid_days = day
        self.valid_times = time

    def check_constraint(self, day, time):
        """
        checks constraints consistency
        :param day:
        :param time:
        :return:
        """
        error = 0
        if (day not in self.valid_days):
            error += 1
        if time not in self.valid_times:
            error += 1
        return error


class Lecture:

    def __init__(self, idx, rooms, instructors):
        """ Define a Lecture; to each lecture assign index, possible locations and possible instructors.

        :param idx:
        :param rooms:
        :param instructors:
        """
        self.idx = idx
        self.rooms = rooms
        self.instructors = instructors

    def check_constraint(self, room, instructor):
        """ rooms and instructors; check constraints satisfaction

        :param room:
        :param instructor:
        :return: number of inconsistent constraints
        """
        error = 0
        if (room not in self.rooms):
            error += 1
        if instructor not in self.instructors:
            error += 1
        return error
