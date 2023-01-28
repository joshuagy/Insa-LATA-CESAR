class EmpireDate :
    def __init__(self, plateau) :
        self.cmpt = 0
        self.plateau = plateau
        self.month = 0
        self.year = 340
        self.era = 0
        self.visualDate = "Jan 340 BC"
        self.months = ["Jan","Feb","Mar","Apr", "May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        self.eras = ["BC","AC"]
        pass

    def update(self) :
        self.cmpt = self.cmpt + 1
        if self.cmpt >= 1500 :
            self.cmpt = 0
            if self.month == 11 :
                self.month = 0
                if self.era == 0 :
                    self.year = self.year-1
                    if self.year == 0 :
                        self.era = 1
                else : 
                    self.year = self.year +1
            else : self.month = self.month + 1
        self.visualDate = (self.months[self.month]+" "+str(self.year) +" "+ self.eras[self.era])


