

class NFLPlayer():

    def __init__(self, name, position, team, nf_projection=None,
                 yh_projection=None):
        self.name = name
        self.team = team
        self.position = position
        self.nf_projection = nf_projection
        self.yh_projection = yh_projection
        self.nf_yh = None

    def update_nf_projection(self, nf_projection):
        self.nf_projection = nf_projection

    def update_yh_projection(self, yahoo):
        fi = self.name[0]
        last = self.name.split(' ')[1]
        yp = [p for p in yahoo if p[0] == fi and p[1] == last and p[2] == self.team]
        if len(yp) == 1:
            self.yh_projection = yp[0][-1]
        else:
            print fi
            print last
            self.yh_projection = 0
            print 'yahoo player not found'

    def update_nf_yh(self):
        try:
            self.nf_yh = self.nf_projection - self.yh_projection
        except:
            self.nf_yh = None
