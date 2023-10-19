class TreePrint:
    """
    Class containing the prefixes for printing trees.
    """
    def __init__(self, t_print: str = "t", l_print: str = "l", s_print: str = "s", e_print: str = "e"):
        self.e_print = e_print
        self.s_print = s_print
        self.l_print = l_print
        self.t_print = t_print

    def apply_to_dict(self, dict_to_modify: dict):
        """
        Modifies the dict object with new values.
        @param dict_to_modify: the dict object to modify.
        """
        dict_to_modify['t'] = self.t_print
        dict_to_modify['l'] = self.l_print
        dict_to_modify['s'] = self.s_print
        dict_to_modify['e'] = self.e_print

    def read_from_dict(self, new_values: dict):
        """Reads from a dict and applies new values."""
        self.t_print = new_values.get('t', self.t_print)
        self.l_print = new_values.get('l', self.l_print)
        self.s_print = new_values.get('s', self.s_print)
        self.e_print = new_values.get('e', self.e_print)

