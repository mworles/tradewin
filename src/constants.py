TEAM_MATCHER = {'JAX': 'JAC',
                'LAR': 'LA',
                'WAS': 'WSH'
                }

POSITIONS = ['QB', 'RB', 'WR', 'TE', 'FLEX']

POSITIONS_NOFLEX = ['QB', 'RB', 'WR', 'TE']

FLEX_POSITIONS = ['RB', 'WR', 'TE']

score_dict = {'pss_cmp': 0.25,
            'pss_inc': -0.25,
            'pss_yds': 0.04,
            'pss_td': 5,
            'pss_int': -2,
            'rsh_yds': 0.10,
            'rsh_td': 6,
            'rec_rec': 0.5,
            'rec_yds': 0.10,
            'rec_td': 6,
            'rsh_att': 0}

N_TEAMS = 14

ROSTER = {'qb': 1,
          'rb': 2,
          'wr': 2,
          'flex': 2,
          'te': 1,
          'bench': 4}

LINEUP_SLOTS = {'QB': 1,
                'RB': 2,
                'WR': 2,
                'TE': 1,
                'FLEX': 2}

ROSTER_SIZE = sum(ROSTER.values())

N_PLAYERS = N_TEAMS * ROSTER_SIZE

ROSTER_START = ROSTER.copy()
del ROSTER_START['bench']

N_START = sum(ROSTER_START.values())

BUDGET = 200

# target percentage of budget allocated to starting lineup
PCT_START = 0.90

# estimate of percentage of flex spots with RB
FLEX_SPLIT = 0.5

# estimate of the percentage of backups drafted for qb and te
DEPTH = 0.50

rep_start = {}
rep_start['qb'] = N_TEAMS * ROSTER['qb'] + 1
rep_start['rb'] = (N_TEAMS * ROSTER['rb']) + (N_TEAMS * ROSTER['flex'] * FLEX_SPLIT) + 1
rep_start['wr'] = (N_TEAMS * ROSTER['wr']) + (N_TEAMS * ROSTER['flex'] * FLEX_SPLIT) + 1
rep_start['te'] = N_TEAMS * ROSTER['te'] + 1

total_start = sum(rep_start.values())

# total number of bench players
total_bench = N_PLAYERS - total_start

# set position of replacement level bench
rep_bench = {}
rep_bench['qb'] = rep_start['qb'] + round(N_TEAMS * DEPTH) + 1
rep_bench['te'] = rep_start['te'] + round(N_TEAMS * DEPTH) + 1

total_bench -= (rep_bench['qb'] - rep_start['qb'])
total_bench -= (rep_bench['te'] - rep_start['te'])
rep_bench['rb'] = rep_start['rb'] + (total_bench / 2) + 1
rep_bench['wr'] = rep_start['wr'] + (total_bench / 2) + 1

TEAM_NAMES = {1: 'Putin Away',
              2: 'copperheads',
              3: 'PimpinSinceBeenPimpn',
              4: 'Silver Hawk',
              5: "It's Gonna Be HUGE",
              6: 'Killer Katz',
              7: 'I Have Andrews Luck',
              8: 'Knights of the Keg',
              9: 'Wentz Wagoneer',
              10: 'Hammer Down'}

MY_TEAM = 3
