class CenterWindowHelper:

    @staticmethod
    def center_window(self, w, h):

        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()  # dimensions of screen
        x, y = (ws / 2) - (w / 2), (hs / 2) - (h / 2)  # calculate center

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
