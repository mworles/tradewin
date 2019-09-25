import pickle

pik_now = "../trades/trade_run.dat"
infile = open(pik_now,'rb')
tr = pickle.load(infile)
infile.close()

trades = tr
trades = [t for t in trades if t.my_nf_gain > 0 and t.other_yh_gain > 0]
#remove_teams = [1, 2, 3]
#trades = [t for t in trades if t.other_team.team_number not in remove_teams]
sortfunc = lambda x: x.my_nf_gain #+ x.other_yh_gain
trades.sort(key=sortfunc) #, reverse=True)

for t in trades[-50:]:
    t.print_trade()
