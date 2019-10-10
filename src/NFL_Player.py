

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
        elif len(yp) == 2:
            if self.name.split(' ')[0] == 'Damien':
                self.yh_projection = yp[0][-1]
            elif self.name_split(' ')[0] == 'Darrel':
                self.yh_projection = yp[1][-1]
            else:
                pass
        else:
            self.yh_projection = 0
            print '%s %s %s yahoo not found' % (fi, last, self.team)

    def update_nf_yh(self):
        try:
            self.nf_yh = self.nf_projection - self.yh_projection
        except:
            self.nf_yh = None
