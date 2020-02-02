class Tools:
    """ Easy Tools """

    def is_int(self, val):
        """ Check if value is a possible integer. """
        try:
            int(val)
            return True
        except:
            return False

    def clean(self, val):
        """ Generic string cleaning. """
        return str(val).strip().lower()

    def are_equal(self, val1, val2):
        """ Check if values are equal. """
        return self.clean(val1) == self.clean(val2)
