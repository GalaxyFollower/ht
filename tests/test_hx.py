# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, Caleb Bell <Caleb.Andrew.Bell@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from __future__ import division
from math import log, exp, sqrt, tanh
from ht import *
import numpy as np
from numpy.testing import assert_allclose
import pytest
from random import uniform, randint


### TODO hx requires testing, but perhaps first improvement
def test_Ntubes_Perrys():
    Nt_perry = [[Ntubes_Perrys(DBundle=1.184, Ntp=i, do=.028, angle=j) for i in [1,2,4,6]] for j in [30, 45, 60, 90]]
    Nt_values = [[1001, 973, 914, 886], [819, 803, 784, 769], [1001, 973, 914, 886], [819, 803, 784, 769]]
    assert_allclose(Nt_perry, Nt_values)
#    angle = 30 or 60 and ntubes = 1.5 raise exception

    with pytest.raises(Exception):
        Ntubes_Perrys(DBundle=1.184, Ntp=5, do=.028, angle=30)
    with pytest.raises(Exception):
        Ntubes_Perrys(DBundle=1.184, Ntp=5, do=.028, angle=45)


def test_Ntubes_VDI():
    VDI_t = [[Ntubes_VDI(DBundle=1.184, Ntp=i, do=.028, pitch=.036, angle=j) for i in [1,2,4,6,8]] for j in [30, 45, 60, 90]]
    VDI_values = [[983, 966, 929, 914, 903], [832, 818, 790, 778, 769], [983, 966, 929, 914, 903], [832, 818, 790, 778, 769]]
    assert_allclose(VDI_t, VDI_values)
    with pytest.raises(Exception):
        Ntubes_VDI(DBundle=1.184, Ntp=5, do=.028, pitch=.036, angle=30)
    with pytest.raises(Exception):
        Ntubes_VDI(DBundle=1.184, Ntp=2, do=.028, pitch=.036, angle=40)


def test_Ntubes_Phadkeb():
    
    Ntubes_calc = [Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=i, angle=45.) for i in [1,2,4,6,8]]
    assert_allclose(Ntubes_calc, [805, 782, 760, 698, 680])
    Ntubes_calc = [Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.035, Ntp=i, angle=45.) for i in [1,2,4,6,8]]
    assert_allclose(Ntubes_calc, [861, 838, 816, 750, 732])
    
    # Extra tests
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=2, angle=30.)
    assert N == 898
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=2, angle=60.)
    assert N == 876
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=6, angle=60.)
    assert N == 858
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=8, angle=60.)
    assert N == 808
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.092, Ntp=8, angle=60.)
    assert N == 100
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=8, angle=30.)
    assert N == 788
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.04, Ntp=6, angle=30.)
    assert N == 652
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=8, angle=90.)
    assert N == 684
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=2, angle=90.)
    assert N == 772
    N = Ntubes_Phadkeb(DBundle=1.200-.008*2, do=.028, pitch=.036, Ntp=6, angle=90.)
    assert N == 712
    
    # Big case
    N = Ntubes_Phadkeb(DBundle=5, do=.028, pitch=.036, Ntp=2, angle=90.)
    assert N == 14842


@pytest.mark.slow
def test_Phadkeb_numbers():
    # One pain point of this code is that it takes 880 kb to store the results
    # in memory as a list
    from ht.hx import triangular_Ns, triangular_C1s, square_Ns, square_C1s
    from math import floor, ceil
    # Triangular Ns 
    # https://oeis.org/A003136
    # Translated expression originally in Wolfram Mathematica
    # nn = 14; Select[Union[Flatten[Table[x^2 + x*y + y^2, {x, 0, nn}, {y, 0, x}]]], # <= nn^2 &] (* T. D. Noe, Apr 18 2011 *) 
    nums = []
    nn = 400 # Increase this to generate more numbers
    for x in range(0, nn+1):
        for y in range(0, x+1):
            nums.append(x*x + x*y + y*y)
    
    nums = sorted(list(set(nums)))
    nums = [i for i in nums if i < nn**2]
    
    nums = nums[0:len(triangular_Ns)]
    assert_allclose(nums, triangular_Ns)
    
    
    # triangular C1s
    # https://oeis.org/A038590 is the sequence, and it is the unique numbers in: 
    # https://oeis.org/A038589
    # Translated from pari expression a(n)=1+6*sum(k=0, n\3, (n\(3*k+1))-(n\(3*k+2)))
    # Tested with the online interpreter http://pari.math.u-bordeaux.fr/gp.html
    # This one is very slow, 300 seconds+
    
    def a(n):
        tot = 0
        for k in range(0, int(ceil(n/3.))):
            tot += floor(n/(3.*k + 1.)) - floor(n/(3.*k + 2.))
        return 1 + 6*int(tot)
    ans = [a(i) for i in range(50000)]
    ans = sorted(list(set(ans)))
    ans = ans[0:len(triangular_C1s)]
    assert_allclose(ans, triangular_C1s)
    
    # square Ns
    # https://oeis.org/A001481
    # Quick and efficient
    # Translated from Mathematica
    # upTo = 160; With[{max = Ceiling[Sqrt[upTo]]}, Select[Union[Total /@ (Tuples[Range[0, max], {2}]^2)], # <= upTo &]]  (* Harvey P. Dale, Apr 22 2011 *) 
    # 10 loops, best of 3: 17.3 ms per loop
    upTo = 100000
    max_range = int(ceil(upTo**0.5))
    squares = [i*i for i in range(max_range+1)]
    seq = [i+j for i in squares for j in squares]
    seq = [i for i in set(seq) if i < upTo] # optional
    nums = seq[0:len(square_Ns)]
    assert_allclose(nums, square_Ns)

    # square C1s
    # https://oeis.org/A057961 is the sequence, there is one mathematica expression
    # but it needs SymPy or some hard work to be done
    # It is also the uniqiue elements in https://oeis.org/A057655
    # That has a convenient expression for pari, tested online and translated
    # a(n)=1+4*sum(k=0, sqrtint(n), sqrtint(n-k^2) ); /* Benoit Cloitre, Oct 08 2012 */ 
    # Currently 1.8 seconds
    def a2(n):
        sqrtint = lambda i: int(i**0.5)
        return 1 + 4*sum([sqrtint(n - k*k) for k in range(0, sqrtint(n) + 1)])
    
    ans = set([a2(i) for i in range(35000)])
    ans = sorted(list(ans))
    nums = ans[0:len(square_C1s)]
    assert_allclose(nums, square_C1s)



def test_Ntubes_HEDH():
    Ntubes_HEDH_c = [Ntubes_HEDH(DBundle=1.200-.008*2, do=.028, pitch=.036, angle=i) for i in [30, 45, 60, 90]]
    assert_allclose(Ntubes_HEDH_c, [928, 804, 928, 804])
    with pytest.raises(Exception):
        Ntubes_HEDH(DBundle=1.200-.008*2, do=.028, pitch=.036, angle=20)

def test_Ntubes():
    methods = Ntubes(DBundle=1.2, do=0.025, AvailableMethods=True)
    Ntubes_calc = [Ntubes(DBundle=1.2, do=0.025, Method=i) for i in methods]
    assert Ntubes_calc == [1285, 1272, 1340, 1297, None]

    assert_allclose(Ntubes(DBundle=1.2, do=0.025), 1285)

    with pytest.raises(Exception):
        Ntubes(DBundle=1.2, do=0.025, Method='failure')


def test_D_for_Ntubes_VDI():
    D_VDI =  [[D_for_Ntubes_VDI(Nt=970, Ntp=i, do=0.00735, pitch=0.015, angle=j) for i in [1, 2, 4, 6, 8]] for j in [30, 60, 45, 90]]
    D_VDI_values = [[0.489981989464919, 0.5003600119829544, 0.522287673753684, 0.5311570964003711, 0.5377131635291736], [0.489981989464919, 0.5003600119829544, 0.522287673753684, 0.5311570964003711, 0.5377131635291736], [0.5326653264480428, 0.5422270203444146, 0.5625250342473964, 0.5707695340997739, 0.5768755899087357], [0.5326653264480428, 0.5422270203444146, 0.5625250342473964, 0.5707695340997739, 0.5768755899087357]]
    assert_allclose(D_VDI, D_VDI_values)

    with pytest.raises(Exception):
        D_for_Ntubes_VDI(Nt=970, Ntp=5., do=0.00735, pitch=0.015, angle=30.)
    with pytest.raises(Exception):
        D_for_Ntubes_VDI(Nt=970, Ntp=2., do=0.00735, pitch=0.015, angle=40.)


def test_effectiveness_NTU():
    # Counterflow
    for i in range(20):
        eff = uniform(0, 1)
        Cr = uniform(0, 1)
        units = NTU_from_effectiveness(effectiveness=eff, Cr=Cr, subtype='counterflow')
        eff_calc = effectiveness_from_NTU(NTU=units, Cr=Cr, subtype='counterflow')
        assert_allclose(eff, eff_calc)
    # Case with Cr = 1
    NTU = NTU_from_effectiveness(effectiveness=.9, Cr=1, subtype='counterflow')
    assert_allclose(NTU, 9)
    e = effectiveness_from_NTU(NTU=9, Cr=1, subtype='counterflow')
    assert_allclose(e, 0.9)
        
        
    # Parallel
    for i in range(20):
        Cr = uniform(0, 1)
        eff = uniform(0, 1./(Cr + 1.)*(1-1E-7))
        units = NTU_from_effectiveness(effectiveness=eff, Cr=Cr, subtype='parallel')
        eff_calc = effectiveness_from_NTU(NTU=units, Cr=Cr, subtype='parallel')
        assert_allclose(eff, eff_calc)
        
    with pytest.raises(Exception):
        Cr = 0.6
        NTU_from_effectiveness(effectiveness=0.62500001, Cr=Cr, subtype='parallel')
        
        
    # Crossflow, Cmin mixed, Cmax unmixed
    
    for i in range(20):
        Cr = uniform(0, 1)
        eff = uniform(0, (1 - exp(-1/Cr))*(1-1E-7))
        N = NTU_from_effectiveness(eff, Cr=Cr, subtype='crossflow, mixed Cmin')
        eff_calc = effectiveness_from_NTU(N, Cr=Cr, subtype='crossflow, mixed Cmin')
        assert_allclose(eff, eff_calc)
        
    with pytest.raises(Exception):
        Cr = 0.7
        NTU_from_effectiveness(0.760348963559, Cr=Cr, subtype='crossflow, mixed Cmin')
        
            
    # Crossflow, Cmax mixed, Cmin unmixed
    for i in range(20):
        Cr = uniform(0, 1)
        eff = uniform(0, (exp(Cr) - 1)*exp(-Cr)/Cr-1E-5)
        N = NTU_from_effectiveness(eff, Cr=Cr, subtype='crossflow, mixed Cmax')
        eff_calc = effectiveness_from_NTU(N, Cr=Cr, subtype='crossflow, mixed Cmax')
        assert_allclose(eff, eff_calc)

    with pytest.raises(Exception):
        Cr = 0.7
        eff = 0.7201638517265581
        NTU_from_effectiveness(eff, Cr=Cr, subtype='crossflow, mixed Cmax')
        
        
    # Crossflow, this one needed a closed-form solver
    for i in range(100):
        Cr = uniform(0, 1)
        eff = uniform(0, 1)
        N = NTU_from_effectiveness(eff, Cr=Cr, subtype='crossflow')
        eff_calc = effectiveness_from_NTU(N, Cr=Cr, subtype='crossflow')
        assert_allclose(eff, eff_calc, rtol=1E-6) # brenth differs in old Python versions, rtol is needed 

    # Shell and tube - this one doesn't have a nice effectiveness limit,
    # and it depends on the number of shells
    
    for i in range(20):
        Cr = uniform(0, 1)
        shells = randint(1, 10)
        eff_max = (-((-Cr + sqrt(Cr**2 + 1) + 1)/(Cr + sqrt(Cr**2 + 1) - 1))**shells + 1)/(Cr - ((-Cr + sqrt(Cr**2 + 1) + 1)/(Cr + sqrt(Cr**2 + 1) - 1))**shells)
        eff = uniform(0, eff_max-1E-5)
        N = NTU_from_effectiveness(eff, Cr=Cr, subtype=str(shells)+'S&T')
        eff_calc = effectiveness_from_NTU(N, Cr=Cr, subtype=str(shells)+'S&T')
        assert_allclose(eff, eff_calc)
        
    with pytest.raises(Exception):
        NTU_from_effectiveness(.99, Cr=.7, subtype='5S&T')
        
    # Easy tests
    effectiveness = effectiveness_from_NTU(NTU=5, Cr=0.7, subtype='crossflow, mixed Cmin')
    assert_allclose(effectiveness, 0.7497843941508544)
    NTU = NTU_from_effectiveness(effectiveness=effectiveness, Cr=0.7, subtype='crossflow, mixed Cmin')
    assert_allclose(NTU, 5)
    
    eff = effectiveness_from_NTU(NTU=5, Cr=0.7, subtype='crossflow, mixed Cmax')
    assert_allclose(eff, 0.7158099831204696)
    NTU = NTU_from_effectiveness(eff, Cr=0.7, subtype='crossflow, mixed Cmax')
    assert_allclose(5, NTU)
    
    eff = effectiveness_from_NTU(NTU=5, Cr=0, subtype='boiler')
    assert_allclose(eff, 0.9932620530009145)
    NTU = NTU_from_effectiveness(eff, Cr=0, subtype='boiler')
    assert_allclose(NTU, 5)
    
    with pytest.raises(Exception):
        effectiveness_from_NTU(NTU=5, Cr=1.01, subtype='crossflow, mixed Cmin')

    with pytest.raises(Exception):
        NTU_from_effectiveness(effectiveness=.2, Cr=1.01, subtype='crossflow, mixed Cmin')
        
        
    # bad names
    with pytest.raises(Exception):
        NTU_from_effectiveness(.99, Cr=.7, subtype='FAIL')
    with pytest.raises(Exception):
        effectiveness_from_NTU(NTU=5, Cr=.5, subtype='FAIL')

    
    
def test_effectiveness_NTU_method():
    ans_known = {'Q': 192850.0, 'Thi': 130, 'Cmax': 9672.0, 'Tho': 110.06100082712986, 'Cmin': 2755.0, 'NTU': 1.1040839095588, 'Tco': 85, 'Tci': 15, 'Cr': 0.2848428453267163, 'effectiveness': 0.6086956521739131, 'UA': 3041.751170834494}
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tci=15, Tco=85, Tho=110.06100082712986)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tci=15, Tco=85, Thi=130)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]

    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Thi=130, Tho=110.06100082712986, Tci=15)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Thi=130, Tho=110.06100082712986, Tco=85)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]

    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tco=85, Tho=110.06100082712986, UA=3041.751170834494)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tci=15, Thi=130, UA=3041.751170834494)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]
    
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tci=15, Tho=110.06100082712986, UA=3041.751170834494)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tco=85, Thi=130, UA=3041.751170834494)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]
    
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tci=15, Tco=85, Tho=110.06100082712986, UA=3041.751170834494)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tco=85, Thi=130, Tho=110.06100082712986, UA=3041.751170834494)
    [assert_allclose(ans_known[i], ans[i]) for i in ans_known.keys()]

    with pytest.raises(Exception):
        # Test raising an error with only on set of stream information 
        effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Thi=130, Tho=110.06100082712986, UA=3041.751170834494)
        
    with pytest.raises(Exception):
        # Inconsistent hot and cold temperatures and heat capacity ratios
        effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Thi=130, Tho=110.06100082712986, Tco=85, Tci=5)

    with pytest.raises(Exception):
        # Calculate UA, but no code side temperature information given
        effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Thi=130, Tho=110.06100082712986)
        
    with pytest.raises(Exception):
        # Calculate UA, but no hot side temperature information given
        effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tci=15, Tco=85)
        
        
def test_F_LMTD_Fakheri():
    '''Number of tube passes must be a multiple of 2N for correlation to work.
    N can be 1.

    Example from http://excelcalculations.blogspot.ca/2011/06/lmtd-correction-factor.html 
    spreadsheet file which Bowman et al (1940).
    This matches for 3, 6, and 11 shell passes perfectly.

    This also matches that from the sheet: 
    http://www.mhprofessional.com/getpage.php?c=0071624082_download.php&cat=113
    '''    
    F_calc = F_LMTD_Fakheri(Tci=15, Tco=85, Thi=130, Tho=110, shells=1)
    assert_allclose(F_calc, 0.9438358829645933)
    
    # R = 1 check
    F_calc = F_LMTD_Fakheri(Tci=15, Tco=35, Thi=130, Tho=110, shells=1)
    assert_allclose(F_calc, 0.9925689447100824)
    
    for i in range(1, 10):
        ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype=str(i)+'S&T', Tci=15, Tco=85, Thi=130)
        dTlm = LMTD(Thi=130, Tho=110.06100082712986,  Tci=15, Tco=85)
        F_expect = ans['Q']/ans['UA']/dTlm
        
        F_calc = F_LMTD_Fakheri(Tci=15, Tco=85, Thi=130, Tho=110.06100082712986, shells=i)
        assert_allclose(F_expect, F_calc)
        F_calc = F_LMTD_Fakheri(Thi=15, Tho=85, Tci=130, Tco=110.06100082712986, shells=i)
        assert_allclose(F_expect, F_calc)


def test_temperature_effectiveness_basic():
    # Except for the crossflow mixed 1&2 cases, taken from an example and checked that
    # it matches the e-NTU method. The approximate formula for crossflow is somewhat
    # different - it is believed the approximations are different.
    
    P1 = temperature_effectiveness_basic(R1=3.5107078039927404, NTU1=0.29786672449248663, subtype='counterflow')
    assert_allclose(P1, 0.173382601503)
    P1 = temperature_effectiveness_basic(R1=3.5107078039927404, NTU1=0.29786672449248663, subtype='parallel')
    assert_allclose(P1, 0.163852912049)
    P1 = temperature_effectiveness_basic(R1=3.5107078039927404, NTU1=0.29786672449248663, subtype='crossflow')
    assert_allclose(P1, 0.149974594007)
    P1 = temperature_effectiveness_basic(R1=3.5107078039927404, NTU1=0.29786672449248663, subtype='crossflow, mixed 1')
    assert_allclose(P1, 0.168678230894)
    P1 = temperature_effectiveness_basic(R1=3.5107078039927404, NTU1=0.29786672449248663, subtype='crossflow, mixed 2')
    assert_allclose(P1, 0.16953790774)
    P1 = temperature_effectiveness_basic(R1=3.5107078039927404, NTU1=0.29786672449248663, subtype='crossflow, mixed 1&2')
    assert_allclose(P1, 0.168411216829)

    with pytest.raises(Exception):
        temperature_effectiveness_basic(R1=3.5107078039927404, NTU1=0.29786672449248663, subtype='FAIL')
        
    # Formulas are in [1]_, [3]_, and [2]_.
    
def test_temperature_effectiveness_TEMA_J():
    # All three models are checked with Rosenhow and then Shaw
    # Formulas presented in Thulukkanam are with respect to the other side of the
    # exchanger
    P1 = temperature_effectiveness_TEMA_J(R1=1/3., NTU1=1., Ntp=1)
    assert_allclose(P1, 0.5699085193651295)
    P1 = temperature_effectiveness_TEMA_J(R1=2., NTU1=1.,  Ntp=1) # R = 2 case
    assert_allclose(P1, 0.3580830895954234)
    P1 = temperature_effectiveness_TEMA_J(R1=1/3., NTU1=1., Ntp=2)
    assert_allclose(P1, 0.5688878232315694)
    P1 = temperature_effectiveness_TEMA_J(R1=1/3., NTU1=1., Ntp=4)
    assert_allclose(P1, 0.5688711846568247)
    
    with pytest.raises(Exception):
        temperature_effectiveness_TEMA_J(R1=1/3., NTU1=1., Ntp=3)
        
        
def test_temperature_effectiveness_TEMA_H():
    P1 = temperature_effectiveness_TEMA_H(R1=1/3., NTU1=1., Ntp=1)
    assert_allclose(P1, 0.5730728284905833)
    P1 = temperature_effectiveness_TEMA_H(R1=2., NTU1=1., Ntp=1) # R = 2 case
    assert_allclose(P1, 0.3640257049950876)
    P1 = temperature_effectiveness_TEMA_H(R1=1/3., NTU1=1., Ntp=2)
    assert_allclose(P1, 0.5824437803128222)
    P1 = temperature_effectiveness_TEMA_H(R1=4., NTU1=1., Ntp=2) # R = 4 case
    assert_allclose(P1, 0.2366953352462191)
    
    P1 = temperature_effectiveness_TEMA_H(R1=1/3., NTU1=1., Ntp=2, optimal=False)
    assert_allclose(P1, 0.5560057072310012)
    P1 = temperature_effectiveness_TEMA_H(R1=4, NTU1=1., Ntp=2, optimal=False)
    assert_allclose(P1, 0.19223481412807347) # R2 = 0.25
    
    # The 1 and 2 case by default are checked with Rosenhow and Shah
    # for the two pass unoptimal case, the result is from Thulukkanam only.
    # The 2-pass optimal arrangement from  Rosenhow and Shaw is the same
    # as that of Thulukkanam however, and shown below.
    m1 = .5
    m2 = 1.2
    Cp1 = 1800.
    Cp2 = 2200.
    UA = 500.
    C1 = m1*Cp1
    C2 = m2*Cp2
    R1_orig = R1 = C1/C2
    NTU1 = UA/C1
    R2 = C2/C1
    NTU2 = UA/C2
    
    R1 = R2
    NTU1 = NTU2
    
    alpha = NTU1*(4*R1 + 1)/8.
    beta = NTU1*(4*R1 - 1)/8.
    D = (1 - exp(-alpha))/(4.*R1 + 1)
    
    E = (1 - exp(-beta))/(4*R1 - 1)
    H = (1 - exp(-2*beta))/(4.*R1 - 1)
    
    G = (1-D)**2*(D**2 + E**2) + D**2*(1+E)**2
    B = (1 + H)*(1 + E)**2
    P1 = (1 - (1-D)**4/(B - 4.*R1*G))
    P1 = P1/R1_orig 
    assert_allclose(P1, 0.40026600037802335)


    with pytest.raises(Exception):
        temperature_effectiveness_TEMA_H(R1=1/3., NTU1=1., Ntp=5)


def test_temperature_effectiveness_TEMA_G():
        # Checked with Shah and Rosenhow, formula typed and then the other case is working
    P1 = temperature_effectiveness_TEMA_G(R1=1/3., NTU1=1., Ntp=1)
    assert_allclose(P1, 0.5730149350867675)
    P1 = temperature_effectiveness_TEMA_G(R1=1/3., NTU1=1., Ntp=2) # TEST CASSE
    assert_allclose(P1, 0.5824238778134628)
    
    # Ntp = 1, R=1 case
    P1_Ntp_R1 = 0.8024466201983814
    P1 = temperature_effectiveness_TEMA_G(R1=1., NTU1=7., Ntp=1) # R = 1 case
    assert_allclose(P1, P1_Ntp_R1)
    P1_near = temperature_effectiveness_TEMA_G(R1=1-1E-9, NTU1=7, Ntp=1)
    assert_allclose(P1_near, P1_Ntp_R1)
    
    # Ntp = 2, optimal, R=2 case
    P1_Ntp_R1 = 0.4838424889135673
    P1 = temperature_effectiveness_TEMA_G(R1=2., NTU1=7., Ntp=2) # R = 2 case
    assert_allclose(P1, P1_Ntp_R1)
    P1_near = temperature_effectiveness_TEMA_G(R1=2-1E-9, NTU1=7., Ntp=2)
    assert_allclose(P1_near, P1_Ntp_R1)


    # Ntp = 2, not optimal case, R1=0.5 case
    P1 = temperature_effectiveness_TEMA_G(R1=1/3., NTU1=1., Ntp=2, optimal=False)
    assert_allclose(P1, 0.5559883028569507)

    P1_Ntp_R1 = 0.3182960796403764
    P1 = temperature_effectiveness_TEMA_G(R1=2, NTU1=1., Ntp=2, optimal=False)
    assert_allclose(P1, P1_Ntp_R1)
    P1_near = temperature_effectiveness_TEMA_G(R1=2-1E-9, NTU1=1., Ntp=2, optimal=False)
    assert_allclose(P1_near, P1_Ntp_R1)
    
    with pytest.raises(Exception):
        temperature_effectiveness_TEMA_G(R1=2., NTU1=7., Ntp=5)

    # The optimal 2 pass case from Thulukkanam is checked with the following case
    # to be the same as those in Rosenhow and Shah
    # Believed working great.
    m1 = .5
    m2 = 1.2
    Cp1 = 1800.
    Cp2 = 2200.
    UA = 500.
    C1 = m1*Cp1
    C2 = m2*Cp2
    R1_orig = R1 = C1/C2
    NTU1 = UA/C1
    R2 = C2/C1
    NTU2 = UA/C2
    
    P1_good = temperature_effectiveness_TEMA_G(R1=R1, NTU1=NTU1, Ntp=2)


    # Good G 2 pass case, working
    R1 = R2
    NTU1 = NTU2
    
    beta = exp(-NTU1*(2*R1 - 1)/2.)
    alpha = exp(-NTU1*(2*R1 + 1)/4.)
    B = (4*R1 - beta*(2*R1 + 1))/(2*R1 - 1.)
    A = -1*(1-alpha)**2/(R1 + 0.5)
    P1 = (B - alpha**2)/(R1*(A + 2 + B/R1))
    
    P1 = P1/R1_orig 
    assert_allclose(P1, P1_good)
    
    
def test_temperature_effectiveness_TEMA_E():
    # 1, 2 both cases are perfect
    eff = temperature_effectiveness_TEMA_E(R1=1/3., NTU1=1., Ntp=1)
    assert_allclose(eff, 0.5870500654031314)
    eff = temperature_effectiveness_TEMA_E(R1=1., NTU1=7., Ntp=1)
    assert_allclose(eff, 0.875)
    
    # Remaining E-shells, checked
    eff = temperature_effectiveness_TEMA_E(R1=1/3., NTU1=1., Ntp=2)
    assert_allclose(eff, 0.5689613217664634)
    eff = temperature_effectiveness_TEMA_E(R1=1., NTU1=7., Ntp=2) # R = 1 case
    assert_allclose(eff, 0.5857620762776082)
    
    eff = temperature_effectiveness_TEMA_E(R1=1/3., NTU1=1., Ntp=2, optimal=False)
    assert_allclose(eff, 0.5699085193651295) # unoptimal case
    eff = temperature_effectiveness_TEMA_E(R1=2, NTU1=1., Ntp=2, optimal=False)
    assert_allclose(eff, 0.3580830895954234)
    
    
    
    eff = temperature_effectiveness_TEMA_E(R1=1/3., NTU1=1., Ntp=3)
    assert_allclose(eff, 0.5708624888990603)
    eff = temperature_effectiveness_TEMA_E(R1=1., NTU1=7., Ntp=3) # R = 1 case
    assert_allclose(eff, 0.6366132064792461)
    
    eff = temperature_effectiveness_TEMA_E(R1=3., NTU1=1., Ntp=3, optimal=False)
    assert_allclose(eff, 0.276815590660033)
    
    eff = temperature_effectiveness_TEMA_E(R1=1/3., NTU1=1., Ntp=4)
    assert_allclose(eff, 0.56888933865756)
    eff = temperature_effectiveness_TEMA_E(R1=1., NTU1=7., Ntp=4) # R = 1 case, even though it's no longer used
    assert_allclose(eff, 0.5571628802075902)
    
    
    with pytest.raises(Exception):
         temperature_effectiveness_TEMA_E(R1=1., NTU1=7., Ntp=7)

    # Compare the expression for 4 tube passes in two of the sources with that
    # in the third.
    R1 = 1/3.
    NTU1 = 1
    D = (4 + R1**2)**0.5
    B = tanh(R1*NTU1/4.)
    A = 1/tanh(D*NTU1/4.)
    P1 = 4*(2*(1 + R1) + D*A + R1*B)**-1
    assert_allclose(P1, 0.56888933865756)
    
    
def test_P_NTU_method():
    # Counterflow case
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='counterflow', Tci=15, Tco=85, Tho=110.06100082712986)
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1i=130, T2i=15, subtype='counterflow')
    assert_allclose(ans2['Q'], ans['Q'])
    # Parallel flow case
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='parallel', Tci=15, Tco=85, Tho=110.06100082712986)
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1i=130, T2i=15, subtype='parallel')
    assert_allclose(ans2['Q'], ans['Q'])
    # Mixed Cmax/ 1
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmax', Tci=15, Tco=85, Tho=110.06100082712986)
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1i=130, T2i=15, subtype='crossflow, mixed 1')
    assert_allclose(ans2['Q'], ans['Q'])
    # Mixed Cmin/2
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='crossflow, mixed Cmin', Tci=15, Tco=85, Tho=110.06100082712986)
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1i=130, T2i=15, subtype='crossflow, mixed 2')
    assert_allclose(ans2['Q'], ans['Q'])
    
    # Counterflow case but with all five different temperature input cases (both inlets known already done)
    ans = effectiveness_NTU_method(mh=5.2, mc=1.45, Cph=1860., Cpc=1900, subtype='counterflow', Tci=15, Tco=85, Tho=110.06100082712986)
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1o=110.06100082712986, T2o=85, subtype='counterflow')
    assert_allclose(ans2['Q'], ans['Q'])
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1i=130, T2o=85, subtype='counterflow')
    assert_allclose(ans2['Q'], ans['Q'])
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1o=110.06100082712986, T2i=15, subtype='counterflow')
    assert_allclose(ans2['Q'], ans['Q'])
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T2o=85, T2i=15, subtype='counterflow')
    assert_allclose(ans2['Q'], ans['Q'])
    ans2 = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=ans['UA'], T1o=110.06100082712986, T1i=130, subtype='counterflow')
    assert_allclose(ans2['Q'], ans['Q'])
    
    # Only 1 temperature input
    with pytest.raises(Exception):
        P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=300, T1i=130, subtype='counterflow')
        
    # Bad HX type input
    with pytest.raises(Exception):
        P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=300, T1i=130, T2i=15, subtype='BADTYPE')

    ans = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=300, T1i=130, T2i=15, subtype='E', Ntp=10)
    assert_allclose(ans['Q'], 32212.185563086336,)

    ans = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=300, T1i=130, T2i=15, subtype='G', Ntp=2)
    assert_allclose(ans['Q'], 32224.88788570008)
    
    ans = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=300, T1i=130, T2i=15, subtype='H', Ntp=2)
    assert_allclose(ans['Q'], 32224.888572366734)
    
    ans = P_NTU_method(m1=5.2, m2=1.45, Cp1=1860., Cp2=1900., UA=300, T1i=130, T2i=15, subtype='J', Ntp=2)
    assert_allclose(ans['Q'], 32212.185699719837)


def test_DBundle_min():
    assert_allclose(DBundle_min(0.0254), 1)
    assert_allclose(DBundle_min(0.005), .1)
    assert_allclose(DBundle_min(0.014), .3)
    assert_allclose(DBundle_min(0.015), .5)
    assert_allclose(DBundle_min(.1), 1.5)

def test_shell_clearance():
    assert_allclose(shell_clearance(DBundle=1.245), 0.0064)
    assert_allclose(shell_clearance(DBundle=4), 0.011)
    assert_allclose(shell_clearance(DBundle=.2), .0032)
    assert_allclose(shell_clearance(DBundle=1.778), 0.0095)
    
    assert_allclose(shell_clearance(DShell=1.245), 0.0064)
    assert_allclose(shell_clearance(DShell=4), 0.011)
    assert_allclose(shell_clearance(DShell=.2), .0032)
    assert_allclose(shell_clearance(DShell=1.778), 0.0095)
    
    with pytest.raises(Exception):
        shell_clearance()

def test_L_unsupported_max():
    assert_allclose(L_unsupported_max(Do=.0254, material='CS'), 1.88)
    assert_allclose(L_unsupported_max(Do=.0253, material='CS'), 1.753)
    assert_allclose(L_unsupported_max(Do=1E-5, material='CS'), 0.66)
    assert_allclose(L_unsupported_max(Do=.00635, material='CS'), 0.66)
    
    assert_allclose(L_unsupported_max(Do=.00635, material='aluminium'), 0.559)
    
    with pytest.raises(Exception):
        L_unsupported_max(Do=.0254, material='BADMATERIAL')
        
    # Terribly pessimistic
    assert_allclose(L_unsupported_max(Do=10, material='CS'), 3.175)