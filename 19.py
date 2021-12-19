import collections
import functools

import aoc


EXAMPLE1 = '''
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
'''


class Scanner:
    def __init__(self, index):
        self.index = index
        self.beacons = []
        self.global_beacons = None
        self.transform = None

    def set_transform(self, transform):
        self.transform = transform
        self.global_beacons = set(self.transform.apply(b) for b in self.beacons)

    def __repr__(self):
        return f'Scanner({self.index}) at {self.transform}'


class Vec(collections.namedtuple('Vec', ('x', 'y', 'z'))):
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self, other):
        return Vec(-self.x, -self.y, -self.z)

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __repr__(self):
        return repr((self.x, self.y, self.z))

    def manhattan_length(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Transform:
    def __init__(self, r, t):
        self.r = r
        self.t = t

    @classmethod
    def identity(cls):
        return cls((Vec(1, 0, 0), Vec(0, 1, 0), Vec(0, 0, 1)), Vec(0, 0, 0))

    def apply(self, v):
        return Vec(self.r[0] * v, self.r[1] * v, self.r[2] * v) + self.t

    def __str__(self):
        return str(self.t)


@functools.cache
def all_rotations():
    '''
    >>> len(all_rotations())
    24
    '''
    def rotation(permutation, fx, fy, fz):
        px, py, pz = permutation
        return (
            Vec(fx if px == 'x' else 0, fx if px == 'y' else 0, fx if px == 'z' else 0),
            Vec(fy if py == 'x' else 0, fy if py == 'y' else 0, fy if py == 'z' else 0),
            Vec(fz if pz == 'x' else 0, fz if pz == 'y' else 0, fz if pz == 'z' else 0),
        )
    return [
        rotation(permutation, fx, fy, fz)
        for permutation, p in (
            ('xyz', 1),
            ('xzy', -1),
            ('zxy', 1),
            ('zyx', -1),
            ('yzx', 1),
            ('yxz', -1),
        )
        for fx in (1, -1)
        for fy in (1, -1)
        for fz in (1, -1)
        if fx * fy * fz * p > 0
    ]


def place_scanner(scanner, placed_scanners, min_beacons):
    for rotation in all_rotations():
        transform = Transform(rotation, Vec(0, 0, 0))
        for placed_scanner in placed_scanners:
            transform.t = Vec(0, 0, 0)
            local_unplaced_unrotated_beacons = [
                transform.apply(b)
                for b in scanner.beacons
            ]
            counts = collections.defaultdict(int)
            for a in placed_scanner.global_beacons:
                for b in local_unplaced_unrotated_beacons:
                    counts[a - b] += 1
            translation, count = max(counts.items(), key=lambda kv: kv[1])
            if count >= min_beacons:
                transform.t = translation
                return transform
    return None


def solve(input, min_beacons = 12):
    '''
    >>> solve("""
    ... --- scanner 0 ---
    ... 0,2,0
    ... 4,1,0
    ... 3,3,0
    ...
    ... --- scanner 1 ---
    ... -1,-1,0
    ... -5,0,0
    ... -2,1,0
    ... """, 3)
    (3, 7)
    >>> solve(EXAMPLE1)
    (79, 3621)
    '''
    unplaced_scanners = []
    scanner = None
    next_scanner_index = 0
    for line in input.strip().splitlines():
        if line.startswith('---'):
            scanner = Scanner(next_scanner_index)
            next_scanner_index += 1
            unplaced_scanners.append(scanner)
        elif line:
            scanner.beacons.append(Vec(*map(int, line.split(','))))

    placed_scanners = [unplaced_scanners.pop(0)]
    placed_scanners[0].set_transform(Transform.identity())
    while unplaced_scanners:
        placed = False
        for scanner in unplaced_scanners:
            transform = place_scanner(scanner, placed_scanners, min_beacons)
            if transform:
                scanner.set_transform(transform)
                placed_scanners.append(scanner)
                unplaced_scanners.remove(scanner)
                placed = True
                break
        assert placed, f'Placed: {placed_scanners}\nUnplaced: {unplaced_scanners}'

    beacons = set()
    for scanner in placed_scanners:
        for beacon in scanner.global_beacons:
            beacons.add(beacon)
    answer1 = len(beacons)

    answer2 = 0
    for a in placed_scanners:
        for b in placed_scanners:
            answer2 = max(answer2, (a.transform.t - b.transform.t).manhattan_length())

    return answer1, answer2
