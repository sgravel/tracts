from tracts.chrom import Chrom
import numpy as np


class Chropair:
    """ A pair of chromosomes. Using pairs of chromosomes allows us to model
        diploid individuals.
    """

    def __init__(self, chroms=None, chropair_len=1, auto=True, label="POP"):
        """ Can instantiate by explictly providing two chromosomes as a tuple
            or an ancestry label, length and autosome status. """
        if chroms is None:
            self.copies = [Chrom(chropair_len, auto, label), Chrom(chropair_len, auto, label)]
            self.len = chropair_len
        else:
            if chroms[0].len != chroms[1].len:
                raise ValueError('chromosome pairs of different lengths!')
            self.len = chroms[0].len
            self.copies = chroms

    def recombine(self):
        # decide on the number of recombinations
        n = np.random.poisson(self.len)
        # get recombination points
        unif = (self.len * np.random.random(n)).tolist()
        unif.extend([0, self.len])
        unif.sort()
        # start with a random chromosome
        startchrom = np.random.random_integers(0, 1)
        tractlist = []
        for startpos in range(len(unif) - 1):
            tractlist.extend(
                self.copies[(startchrom + startpos) % 2]
                .extract(unif[startpos],
                         unif[startpos + 1]))
        newchrom = Chrom(self.copies[0].len, self.copies[0].auto)
        newchrom.init_list_tracts(tractlist)
        return newchrom

    def applychrom(self, func):
        """apply func to chromosomes"""
        ls = []
        for copy in self.copies:
            ls.append(func(copy))
        return ls

    def plot(self, canvas, colordict, height=0):
        self.copies[0].plot(canvas, colordict, height=height + 0.1)
        self.copies[1].plot(canvas, colordict, height=height + 0.22)

    def __iter__(self):
        return self.copies.__iter__()

    def __getitem__(self, index):
        return self.copies[index]