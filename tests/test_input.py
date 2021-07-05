import unittest
import tracts
import time
import numpy as np
import sys
sys.path.append('../')
sys.path.append('../example/2pops')
sys.path.append('../example/3pops')
import pp
import models_3pop as threepop


class ManipsTestCase(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f seconds" % (self.id(), t))

    def test_load_data_2pop(self):
        """"Load data from 2 pop example and check that loaded data is as expected"""
        cutoff = 2
        directory = "../example/2pops/G10/"
        names = [
            "NA19700", "NA19701", "NA19704", "NA19703", "NA19819", "NA19818",
            "NA19835", "NA19834", "NA19901", "NA19900", "NA19909", "NA19908",
            "NA19917", "NA19916", "NA19713", "NA19982", "NA20127", "NA20126",
            "NA20357", "NA20356"
        ]
        chroms = ['%d' % (i,) for i in range(1, 23)]

        pop = tracts.population(
            names=names, fname=(directory, "", ".bed"), selectchrom=chroms)
        (bins, data) = pop.get_global_tractlengths(npts=50)

        self.assertTrue(np.sum(data['AFR']) == 2210)
        self.assertTrue(list(data.keys())[0] == 'AFR')
        self.assertTrue(list(data.keys())[1] == 'EUR')
        self.assertTrue(len(bins) == 51)

        rep_pp = 1

        labels = ['EUR', 'AFR']
        data = [data[poplab] for poplab in labels]

        startparams = np.array([0.1683211])

        Ls = pop.Ls
        nind = pop.nind

        def randomize(arr, scale=2):
            """ Scale each element of an array by some random factor between zero and a
                limit (default: 2), capping the result at 1.
            """
            return [min(i, 1) for i in scale * np.random.random(arr.shape) * arr]

        bypopfrac = [[] for i in range(len(labels))]

        for ind in pop.indivs:
            for ii, poplab in enumerate(labels):
                bypopfrac[ii].append(ind.ancestryProps([poplab]))

        props = np.mean(bypopfrac, axis=1).flatten()

        # we compare two models; single pulse versus two European pulses.
        func = pp.pp_fix
        bound = pp.outofbounds_pp_fix

        optmod = tracts.demographic_model(func(startparams, fracs=props))

        liks_orig_pp = []
        maxlik = -1e18
        startrand = startparams





suite = unittest.TestLoader().loadTestsFromTestCase(ManipsTestCase)
