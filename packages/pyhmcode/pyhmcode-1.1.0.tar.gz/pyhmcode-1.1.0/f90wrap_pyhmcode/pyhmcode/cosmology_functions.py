"""
Module cosmology_functions


Defined at ../library/src/cosmology_functions.f90 lines 1-7935

"""
from __future__ import print_function, absolute_import, division
from . import _pyhmcode
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("pyhmcode.cosmology")
class cosmology(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=cosmology)
    
    
    Defined at ../library/src/cosmology_functions.f90 lines 185-244
    
    """
    def __init__(self, handle=None):
        """
        self = Cosmology()
        
        
        Defined at ../library/src/cosmology_functions.f90 lines 185-244
        
        
        Returns
        -------
        this : Cosmology
        	Object to be constructed
        
        
        Automatically generated constructor for cosmology
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _pyhmcode.f90wrap_cosmology_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Cosmology
        
        
        Defined at ../library/src/cosmology_functions.f90 lines 185-244
        
        Parameters
        ----------
        this : Cosmology
        	Object to be destructed
        
        
        Automatically generated destructor for cosmology
        """
        if self._alloc:
            _pyhmcode.f90wrap_cosmology_finalise(this=self._handle)
    
    @property
    def name(self):
        """
        Element name ftype=character(len=256) pytype=str
        
        
        Defined at ../library/src/cosmology_functions.f90 line 187
        
        """
        return _pyhmcode.f90wrap_cosmology__get__name(self._handle)
    
    @name.setter
    def name(self, name):
        _pyhmcode.f90wrap_cosmology__set__name(self._handle, name)
    
    @property
    def om_m(self):
        """
        Element om_m ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 188
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_m(self._handle)
    
    @om_m.setter
    def om_m(self, om_m):
        _pyhmcode.f90wrap_cosmology__set__om_m(self._handle, om_m)
    
    @property
    def om_b(self):
        """
        Element om_b ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 188
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_b(self._handle)
    
    @om_b.setter
    def om_b(self, om_b):
        _pyhmcode.f90wrap_cosmology__set__om_b(self._handle, om_b)
    
    @property
    def om_v(self):
        """
        Element om_v ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 188
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_v(self._handle)
    
    @om_v.setter
    def om_v(self, om_v):
        _pyhmcode.f90wrap_cosmology__set__om_v(self._handle, om_v)
    
    @property
    def om_w(self):
        """
        Element om_w ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 188
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_w(self._handle)
    
    @om_w.setter
    def om_w(self, om_w):
        _pyhmcode.f90wrap_cosmology__set__om_w(self._handle, om_w)
    
    @property
    def ns(self):
        """
        Element ns ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 189
        
        """
        return _pyhmcode.f90wrap_cosmology__get__ns(self._handle)
    
    @ns.setter
    def ns(self, ns):
        _pyhmcode.f90wrap_cosmology__set__ns(self._handle, ns)
    
    @property
    def nrun(self):
        """
        Element nrun ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 189
        
        """
        return _pyhmcode.f90wrap_cosmology__get__nrun(self._handle)
    
    @nrun.setter
    def nrun(self, nrun):
        _pyhmcode.f90wrap_cosmology__set__nrun(self._handle, nrun)
    
    @property
    def nrunrun(self):
        """
        Element nrunrun ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 189
        
        """
        return _pyhmcode.f90wrap_cosmology__get__nrunrun(self._handle)
    
    @nrunrun.setter
    def nrunrun(self, nrunrun):
        _pyhmcode.f90wrap_cosmology__set__nrunrun(self._handle, nrunrun)
    
    @property
    def h(self):
        """
        Element h ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 190
        
        """
        return _pyhmcode.f90wrap_cosmology__get__h(self._handle)
    
    @h.setter
    def h(self, h):
        _pyhmcode.f90wrap_cosmology__set__h(self._handle, h)
    
    @property
    def w(self):
        """
        Element w ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 190
        
        """
        return _pyhmcode.f90wrap_cosmology__get__w(self._handle)
    
    @w.setter
    def w(self, w):
        _pyhmcode.f90wrap_cosmology__set__w(self._handle, w)
    
    @property
    def wa(self):
        """
        Element wa ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 190
        
        """
        return _pyhmcode.f90wrap_cosmology__get__wa(self._handle)
    
    @wa.setter
    def wa(self, wa):
        _pyhmcode.f90wrap_cosmology__set__wa(self._handle, wa)
    
    @property
    def m_wdm(self):
        """
        Element m_wdm ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 190
        
        """
        return _pyhmcode.f90wrap_cosmology__get__m_wdm(self._handle)
    
    @m_wdm.setter
    def m_wdm(self, m_wdm):
        _pyhmcode.f90wrap_cosmology__set__m_wdm(self._handle, m_wdm)
    
    @property
    def yh(self):
        """
        Element yh ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 190
        
        """
        return _pyhmcode.f90wrap_cosmology__get__yh(self._handle)
    
    @yh.setter
    def yh(self, yh):
        _pyhmcode.f90wrap_cosmology__set__yh(self._handle, yh)
    
    @property
    def a1(self):
        """
        Element a1 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 191
        
        """
        return _pyhmcode.f90wrap_cosmology__get__a1(self._handle)
    
    @a1.setter
    def a1(self, a1):
        _pyhmcode.f90wrap_cosmology__set__a1(self._handle, a1)
    
    @property
    def a2(self):
        """
        Element a2 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 191
        
        """
        return _pyhmcode.f90wrap_cosmology__get__a2(self._handle)
    
    @a2.setter
    def a2(self, a2):
        _pyhmcode.f90wrap_cosmology__set__a2(self._handle, a2)
    
    @property
    def nstar(self):
        """
        Element nstar ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 191
        
        """
        return _pyhmcode.f90wrap_cosmology__get__nstar(self._handle)
    
    @nstar.setter
    def nstar(self, nstar):
        _pyhmcode.f90wrap_cosmology__set__nstar(self._handle, nstar)
    
    @property
    def ws(self):
        """
        Element ws ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 191
        
        """
        return _pyhmcode.f90wrap_cosmology__get__ws(self._handle)
    
    @ws.setter
    def ws(self, ws):
        _pyhmcode.f90wrap_cosmology__set__ws(self._handle, ws)
    
    @property
    def am(self):
        """
        Element am ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 191
        
        """
        return _pyhmcode.f90wrap_cosmology__get__am(self._handle)
    
    @am.setter
    def am(self, am):
        _pyhmcode.f90wrap_cosmology__set__am(self._handle, am)
    
    @property
    def dm(self):
        """
        Element dm ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 191
        
        """
        return _pyhmcode.f90wrap_cosmology__get__dm(self._handle)
    
    @dm.setter
    def dm(self, dm):
        _pyhmcode.f90wrap_cosmology__set__dm(self._handle, dm)
    
    @property
    def wm(self):
        """
        Element wm ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 191
        
        """
        return _pyhmcode.f90wrap_cosmology__get__wm(self._handle)
    
    @wm.setter
    def wm(self, wm):
        _pyhmcode.f90wrap_cosmology__set__wm(self._handle, wm)
    
    @property
    def t_cmb(self):
        """
        Element t_cmb ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 192
        
        """
        return _pyhmcode.f90wrap_cosmology__get__t_cmb(self._handle)
    
    @t_cmb.setter
    def t_cmb(self, t_cmb):
        _pyhmcode.f90wrap_cosmology__set__t_cmb(self._handle, t_cmb)
    
    @property
    def neff(self):
        """
        Element neff ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 193
        
        """
        return _pyhmcode.f90wrap_cosmology__get__neff(self._handle)
    
    @neff.setter
    def neff(self, neff):
        _pyhmcode.f90wrap_cosmology__set__neff(self._handle, neff)
    
    @property
    def m_nu(self):
        """
        Element m_nu ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 193
        
        """
        return _pyhmcode.f90wrap_cosmology__get__m_nu(self._handle)
    
    @m_nu.setter
    def m_nu(self, m_nu):
        _pyhmcode.f90wrap_cosmology__set__m_nu(self._handle, m_nu)
    
    @property
    def h0rc(self):
        """
        Element h0rc ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 194
        
        """
        return _pyhmcode.f90wrap_cosmology__get__h0rc(self._handle)
    
    @h0rc.setter
    def h0rc(self, h0rc):
        _pyhmcode.f90wrap_cosmology__set__h0rc(self._handle, h0rc)
    
    @property
    def fr0(self):
        """
        Element fr0 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 194
        
        """
        return _pyhmcode.f90wrap_cosmology__get__fr0(self._handle)
    
    @fr0.setter
    def fr0(self, fr0):
        _pyhmcode.f90wrap_cosmology__set__fr0(self._handle, fr0)
    
    @property
    def nfr(self):
        """
        Element nfr ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 194
        
        """
        return _pyhmcode.f90wrap_cosmology__get__nfr(self._handle)
    
    @nfr.setter
    def nfr(self, nfr):
        _pyhmcode.f90wrap_cosmology__set__nfr(self._handle, nfr)
    
    @property
    def om_m_pow(self):
        """
        Element om_m_pow ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 195
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_m_pow(self._handle)
    
    @om_m_pow.setter
    def om_m_pow(self, om_m_pow):
        _pyhmcode.f90wrap_cosmology__set__om_m_pow(self._handle, om_m_pow)
    
    @property
    def om_b_pow(self):
        """
        Element om_b_pow ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 195
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_b_pow(self._handle)
    
    @om_b_pow.setter
    def om_b_pow(self, om_b_pow):
        _pyhmcode.f90wrap_cosmology__set__om_b_pow(self._handle, om_b_pow)
    
    @property
    def h_pow(self):
        """
        Element h_pow ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 195
        
        """
        return _pyhmcode.f90wrap_cosmology__get__h_pow(self._handle)
    
    @h_pow.setter
    def h_pow(self, h_pow):
        _pyhmcode.f90wrap_cosmology__set__h_pow(self._handle, h_pow)
    
    @property
    def b0(self):
        """
        Element b0 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 196
        
        """
        return _pyhmcode.f90wrap_cosmology__get__b0(self._handle)
    
    @b0.setter
    def b0(self, b0):
        _pyhmcode.f90wrap_cosmology__set__b0(self._handle, b0)
    
    @property
    def b1(self):
        """
        Element b1 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 196
        
        """
        return _pyhmcode.f90wrap_cosmology__get__b1(self._handle)
    
    @b1.setter
    def b1(self, b1):
        _pyhmcode.f90wrap_cosmology__set__b1(self._handle, b1)
    
    @property
    def b2(self):
        """
        Element b2 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 196
        
        """
        return _pyhmcode.f90wrap_cosmology__get__b2(self._handle)
    
    @b2.setter
    def b2(self, b2):
        _pyhmcode.f90wrap_cosmology__set__b2(self._handle, b2)
    
    @property
    def b3(self):
        """
        Element b3 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 196
        
        """
        return _pyhmcode.f90wrap_cosmology__get__b3(self._handle)
    
    @b3.setter
    def b3(self, b3):
        _pyhmcode.f90wrap_cosmology__set__b3(self._handle, b3)
    
    @property
    def b4(self):
        """
        Element b4 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 196
        
        """
        return _pyhmcode.f90wrap_cosmology__get__b4(self._handle)
    
    @b4.setter
    def b4(self, b4):
        _pyhmcode.f90wrap_cosmology__set__b4(self._handle, b4)
    
    @property
    def a_bump(self):
        """
        Element a_bump ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 197
        
        """
        return _pyhmcode.f90wrap_cosmology__get__a_bump(self._handle)
    
    @a_bump.setter
    def a_bump(self, a_bump):
        _pyhmcode.f90wrap_cosmology__set__a_bump(self._handle, a_bump)
    
    @property
    def k_bump(self):
        """
        Element k_bump ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 197
        
        """
        return _pyhmcode.f90wrap_cosmology__get__k_bump(self._handle)
    
    @k_bump.setter
    def k_bump(self, k_bump):
        _pyhmcode.f90wrap_cosmology__set__k_bump(self._handle, k_bump)
    
    @property
    def sigma_bump(self):
        """
        Element sigma_bump ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 197
        
        """
        return _pyhmcode.f90wrap_cosmology__get__sigma_bump(self._handle)
    
    @sigma_bump.setter
    def sigma_bump(self, sigma_bump):
        _pyhmcode.f90wrap_cosmology__set__sigma_bump(self._handle, sigma_bump)
    
    @property
    def theat(self):
        """
        Element theat ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 198
        
        """
        return _pyhmcode.f90wrap_cosmology__get__theat(self._handle)
    
    @theat.setter
    def theat(self, theat):
        _pyhmcode.f90wrap_cosmology__set__theat(self._handle, theat)
    
    @property
    def lbox(self):
        """
        Element lbox ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 199
        
        """
        return _pyhmcode.f90wrap_cosmology__get__lbox(self._handle)
    
    @lbox.setter
    def lbox(self, lbox):
        _pyhmcode.f90wrap_cosmology__set__lbox(self._handle, lbox)
    
    @property
    def n_nu(self):
        """
        Element n_nu ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 200
        
        """
        return _pyhmcode.f90wrap_cosmology__get__n_nu(self._handle)
    
    @n_nu.setter
    def n_nu(self, n_nu):
        _pyhmcode.f90wrap_cosmology__set__n_nu(self._handle, n_nu)
    
    @property
    def bump(self):
        """
        Element bump ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 201
        
        """
        return _pyhmcode.f90wrap_cosmology__get__bump(self._handle)
    
    @bump.setter
    def bump(self, bump):
        _pyhmcode.f90wrap_cosmology__set__bump(self._handle, bump)
    
    @property
    def norm_method(self):
        """
        Element norm_method ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 202
        
        """
        return _pyhmcode.f90wrap_cosmology__get__norm_method(self._handle)
    
    @norm_method.setter
    def norm_method(self, norm_method):
        _pyhmcode.f90wrap_cosmology__set__norm_method(self._handle, norm_method)
    
    @property
    def iw(self):
        """
        Element iw ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 203
        
        """
        return _pyhmcode.f90wrap_cosmology__get__iw(self._handle)
    
    @iw.setter
    def iw(self, iw):
        _pyhmcode.f90wrap_cosmology__set__iw(self._handle, iw)
    
    @property
    def img(self):
        """
        Element img ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 204
        
        """
        return _pyhmcode.f90wrap_cosmology__get__img(self._handle)
    
    @img.setter
    def img(self, img):
        _pyhmcode.f90wrap_cosmology__set__img(self._handle, img)
    
    @property
    def itk(self):
        """
        Element itk ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 205
        
        """
        return _pyhmcode.f90wrap_cosmology__get__itk(self._handle)
    
    @itk.setter
    def itk(self, itk):
        _pyhmcode.f90wrap_cosmology__set__itk(self._handle, itk)
    
    @property
    def itc(self):
        """
        Element itc ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 206
        
        """
        return _pyhmcode.f90wrap_cosmology__get__itc(self._handle)
    
    @itc.setter
    def itc(self, itc):
        _pyhmcode.f90wrap_cosmology__set__itc(self._handle, itc)
    
    @property
    def box(self):
        """
        Element box ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 207
        
        """
        return _pyhmcode.f90wrap_cosmology__get__box(self._handle)
    
    @box.setter
    def box(self, box):
        _pyhmcode.f90wrap_cosmology__set__box(self._handle, box)
    
    @property
    def warm(self):
        """
        Element warm ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 208
        
        """
        return _pyhmcode.f90wrap_cosmology__get__warm(self._handle)
    
    @warm.setter
    def warm(self, warm):
        _pyhmcode.f90wrap_cosmology__set__warm(self._handle, warm)
    
    @property
    def power_omegas(self):
        """
        Element power_omegas ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 209
        
        """
        return _pyhmcode.f90wrap_cosmology__get__power_omegas(self._handle)
    
    @power_omegas.setter
    def power_omegas(self, power_omegas):
        _pyhmcode.f90wrap_cosmology__set__power_omegas(self._handle, power_omegas)
    
    @property
    def derive_gas_numbers(self):
        """
        Element derive_gas_numbers ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 210
        
        """
        return _pyhmcode.f90wrap_cosmology__get__derive_gas_numbers(self._handle)
    
    @derive_gas_numbers.setter
    def derive_gas_numbers(self, derive_gas_numbers):
        _pyhmcode.f90wrap_cosmology__set__derive_gas_numbers(self._handle, \
            derive_gas_numbers)
    
    @property
    def kpiv(self):
        """
        Element kpiv ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 212
        
        """
        return _pyhmcode.f90wrap_cosmology__get__kpiv(self._handle)
    
    @kpiv.setter
    def kpiv(self, kpiv):
        _pyhmcode.f90wrap_cosmology__set__kpiv(self._handle, kpiv)
    
    @property
    def as_(self):
        """
        Element as_ ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 212
        
        """
        return _pyhmcode.f90wrap_cosmology__get__as_(self._handle)
    
    @as_.setter
    def as_(self, as_):
        _pyhmcode.f90wrap_cosmology__set__as_(self._handle, as_)
    
    @property
    def kval(self):
        """
        Element kval ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 212
        
        """
        return _pyhmcode.f90wrap_cosmology__get__kval(self._handle)
    
    @kval.setter
    def kval(self, kval):
        _pyhmcode.f90wrap_cosmology__set__kval(self._handle, kval)
    
    @property
    def pval(self):
        """
        Element pval ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 212
        
        """
        return _pyhmcode.f90wrap_cosmology__get__pval(self._handle)
    
    @pval.setter
    def pval(self, pval):
        _pyhmcode.f90wrap_cosmology__set__pval(self._handle, pval)
    
    @property
    def sig8(self):
        """
        Element sig8 ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 212
        
        """
        return _pyhmcode.f90wrap_cosmology__get__sig8(self._handle)
    
    @sig8.setter
    def sig8(self, sig8):
        _pyhmcode.f90wrap_cosmology__set__sig8(self._handle, sig8)
    
    @property
    def mue(self):
        """
        Element mue ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 213
        
        """
        return _pyhmcode.f90wrap_cosmology__get__mue(self._handle)
    
    @mue.setter
    def mue(self, mue):
        _pyhmcode.f90wrap_cosmology__set__mue(self._handle, mue)
    
    @property
    def mup(self):
        """
        Element mup ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 213
        
        """
        return _pyhmcode.f90wrap_cosmology__get__mup(self._handle)
    
    @mup.setter
    def mup(self, mup):
        _pyhmcode.f90wrap_cosmology__set__mup(self._handle, mup)
    
    @property
    def a(self):
        """
        Element a ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 215
        
        """
        return _pyhmcode.f90wrap_cosmology__get__a(self._handle)
    
    @a.setter
    def a(self, a):
        _pyhmcode.f90wrap_cosmology__set__a(self._handle, a)
    
    @property
    def om(self):
        """
        Element om ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 216
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om(self._handle)
    
    @om.setter
    def om(self, om):
        _pyhmcode.f90wrap_cosmology__set__om(self._handle, om)
    
    @property
    def om_k(self):
        """
        Element om_k ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 216
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_k(self._handle)
    
    @om_k.setter
    def om_k(self, om_k):
        _pyhmcode.f90wrap_cosmology__set__om_k(self._handle, om_k)
    
    @property
    def om_c(self):
        """
        Element om_c ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 216
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_c(self._handle)
    
    @om_c.setter
    def om_c(self, om_c):
        _pyhmcode.f90wrap_cosmology__set__om_c(self._handle, om_c)
    
    @property
    def om_g(self):
        """
        Element om_g ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 216
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_g(self._handle)
    
    @om_g.setter
    def om_g(self, om_g):
        _pyhmcode.f90wrap_cosmology__set__om_g(self._handle, om_g)
    
    @property
    def om_r(self):
        """
        Element om_r ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 216
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_r(self._handle)
    
    @om_r.setter
    def om_r(self, om_r):
        _pyhmcode.f90wrap_cosmology__set__om_r(self._handle, om_r)
    
    @property
    def om_nu(self):
        """
        Element om_nu ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 217
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_nu(self._handle)
    
    @om_nu.setter
    def om_nu(self, om_nu):
        _pyhmcode.f90wrap_cosmology__set__om_nu(self._handle, om_nu)
    
    @property
    def f_nu(self):
        """
        Element f_nu ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 217
        
        """
        return _pyhmcode.f90wrap_cosmology__get__f_nu(self._handle)
    
    @f_nu.setter
    def f_nu(self, f_nu):
        _pyhmcode.f90wrap_cosmology__set__f_nu(self._handle, f_nu)
    
    @property
    def a_nu(self):
        """
        Element a_nu ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 217
        
        """
        return _pyhmcode.f90wrap_cosmology__get__a_nu(self._handle)
    
    @a_nu.setter
    def a_nu(self, a_nu):
        _pyhmcode.f90wrap_cosmology__set__a_nu(self._handle, a_nu)
    
    @property
    def om_nu_rad(self):
        """
        Element om_nu_rad ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 218
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_nu_rad(self._handle)
    
    @om_nu_rad.setter
    def om_nu_rad(self, om_nu_rad):
        _pyhmcode.f90wrap_cosmology__set__om_nu_rad(self._handle, om_nu_rad)
    
    @property
    def omega_nu(self):
        """
        Element omega_nu ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 218
        
        """
        return _pyhmcode.f90wrap_cosmology__get__omega_nu(self._handle)
    
    @omega_nu.setter
    def omega_nu(self, omega_nu):
        _pyhmcode.f90wrap_cosmology__set__omega_nu(self._handle, omega_nu)
    
    @property
    def t_nu(self):
        """
        Element t_nu ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 218
        
        """
        return _pyhmcode.f90wrap_cosmology__get__t_nu(self._handle)
    
    @t_nu.setter
    def t_nu(self, t_nu):
        _pyhmcode.f90wrap_cosmology__set__t_nu(self._handle, t_nu)
    
    @property
    def omega_m(self):
        """
        Element omega_m ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 219
        
        """
        return _pyhmcode.f90wrap_cosmology__get__omega_m(self._handle)
    
    @omega_m.setter
    def omega_m(self, omega_m):
        _pyhmcode.f90wrap_cosmology__set__omega_m(self._handle, omega_m)
    
    @property
    def omega_b(self):
        """
        Element omega_b ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 219
        
        """
        return _pyhmcode.f90wrap_cosmology__get__omega_b(self._handle)
    
    @omega_b.setter
    def omega_b(self, omega_b):
        _pyhmcode.f90wrap_cosmology__set__omega_b(self._handle, omega_b)
    
    @property
    def omega_c(self):
        """
        Element omega_c ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 219
        
        """
        return _pyhmcode.f90wrap_cosmology__get__omega_c(self._handle)
    
    @omega_c.setter
    def omega_c(self, omega_c):
        _pyhmcode.f90wrap_cosmology__set__omega_c(self._handle, omega_c)
    
    @property
    def k(self):
        """
        Element k ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 220
        
        """
        return _pyhmcode.f90wrap_cosmology__get__k(self._handle)
    
    @k.setter
    def k(self, k):
        _pyhmcode.f90wrap_cosmology__set__k(self._handle, k)
    
    @property
    def z_cmb(self):
        """
        Element z_cmb ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 221
        
        """
        return _pyhmcode.f90wrap_cosmology__get__z_cmb(self._handle)
    
    @z_cmb.setter
    def z_cmb(self, z_cmb):
        _pyhmcode.f90wrap_cosmology__set__z_cmb(self._handle, z_cmb)
    
    @property
    def om_c_pow(self):
        """
        Element om_c_pow ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 222
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_c_pow(self._handle)
    
    @om_c_pow.setter
    def om_c_pow(self, om_c_pow):
        _pyhmcode.f90wrap_cosmology__set__om_c_pow(self._handle, om_c_pow)
    
    @property
    def age(self):
        """
        Element age ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 223
        
        """
        return _pyhmcode.f90wrap_cosmology__get__age(self._handle)
    
    @age.setter
    def age(self, age):
        _pyhmcode.f90wrap_cosmology__set__age(self._handle, age)
    
    @property
    def horizon(self):
        """
        Element horizon ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 223
        
        """
        return _pyhmcode.f90wrap_cosmology__get__horizon(self._handle)
    
    @horizon.setter
    def horizon(self, horizon):
        _pyhmcode.f90wrap_cosmology__set__horizon(self._handle, horizon)
    
    @property
    def yhe(self):
        """
        Element yhe ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 224
        
        """
        return _pyhmcode.f90wrap_cosmology__get__yhe(self._handle)
    
    @yhe.setter
    def yhe(self, yhe):
        _pyhmcode.f90wrap_cosmology__set__yhe(self._handle, yhe)
    
    @property
    def om_ws(self):
        """
        Element om_ws ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 225
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_ws(self._handle)
    
    @om_ws.setter
    def om_ws(self, om_ws):
        _pyhmcode.f90wrap_cosmology__set__om_ws(self._handle, om_ws)
    
    @property
    def astar(self):
        """
        Element astar ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 225
        
        """
        return _pyhmcode.f90wrap_cosmology__get__astar(self._handle)
    
    @astar.setter
    def astar(self, astar):
        _pyhmcode.f90wrap_cosmology__set__astar(self._handle, astar)
    
    @property
    def a1n(self):
        """
        Element a1n ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 225
        
        """
        return _pyhmcode.f90wrap_cosmology__get__a1n(self._handle)
    
    @a1n.setter
    def a1n(self, a1n):
        _pyhmcode.f90wrap_cosmology__set__a1n(self._handle, a1n)
    
    @property
    def a2n(self):
        """
        Element a2n ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 225
        
        """
        return _pyhmcode.f90wrap_cosmology__get__a2n(self._handle)
    
    @a2n.setter
    def a2n(self, a2n):
        _pyhmcode.f90wrap_cosmology__set__a2n(self._handle, a2n)
    
    @property
    def om_de(self):
        """
        Element om_de ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 226
        
        """
        return _pyhmcode.f90wrap_cosmology__get__om_de(self._handle)
    
    @om_de.setter
    def om_de(self, om_de):
        _pyhmcode.f90wrap_cosmology__set__om_de(self._handle, om_de)
    
    @property
    def gnorm(self):
        """
        Element gnorm ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 227
        
        """
        return _pyhmcode.f90wrap_cosmology__get__gnorm(self._handle)
    
    @gnorm.setter
    def gnorm(self, gnorm):
        _pyhmcode.f90wrap_cosmology__set__gnorm(self._handle, gnorm)
    
    @property
    def kbox(self):
        """
        Element kbox ftype=real  pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 228
        
        """
        return _pyhmcode.f90wrap_cosmology__get__kbox(self._handle)
    
    @kbox.setter
    def kbox(self, kbox):
        _pyhmcode.f90wrap_cosmology__set__kbox(self._handle, kbox)
    
    @property
    def scale_dependent_growth(self):
        """
        Element scale_dependent_growth ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 229
        
        """
        return _pyhmcode.f90wrap_cosmology__get__scale_dependent_growth(self._handle)
    
    @scale_dependent_growth.setter
    def scale_dependent_growth(self, scale_dependent_growth):
        _pyhmcode.f90wrap_cosmology__set__scale_dependent_growth(self._handle, \
            scale_dependent_growth)
    
    @property
    def k_plin(self):
        """
        Element k_plin ftype=real pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 231
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_cosmology__array__k_plin(self._handle)
        if array_handle in self._arrays:
            k_plin = self._arrays[array_handle]
        else:
            k_plin = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_cosmology__array__k_plin)
            self._arrays[array_handle] = k_plin
        return k_plin
    
    @k_plin.setter
    def k_plin(self, k_plin):
        self.k_plin[...] = k_plin
    
    @property
    def a_plin(self):
        """
        Element a_plin ftype=real pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 231
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_cosmology__array__a_plin(self._handle)
        if array_handle in self._arrays:
            a_plin = self._arrays[array_handle]
        else:
            a_plin = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_cosmology__array__a_plin)
            self._arrays[array_handle] = a_plin
        return a_plin
    
    @a_plin.setter
    def a_plin(self, a_plin):
        self.a_plin[...] = a_plin
    
    @property
    def plin_array(self):
        """
        Element plin_array ftype=real pytype=float
        
        
        Defined at ../library/src/cosmology_functions.f90 line 231
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_cosmology__array__plin_array(self._handle)
        if array_handle in self._arrays:
            plin_array = self._arrays[array_handle]
        else:
            plin_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_cosmology__array__plin_array)
            self._arrays[array_handle] = plin_array
        return plin_array
    
    @plin_array.setter
    def plin_array(self, plin_array):
        self.plin_array[...] = plin_array
    
    @property
    def analytical_tk(self):
        """
        Element analytical_tk ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 235
        
        """
        return _pyhmcode.f90wrap_cosmology__get__analytical_tk(self._handle)
    
    @analytical_tk.setter
    def analytical_tk(self, analytical_tk):
        _pyhmcode.f90wrap_cosmology__set__analytical_tk(self._handle, analytical_tk)
    
    @property
    def has_distance(self):
        """
        Element has_distance ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 236
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_distance(self._handle)
    
    @has_distance.setter
    def has_distance(self, has_distance):
        _pyhmcode.f90wrap_cosmology__set__has_distance(self._handle, has_distance)
    
    @property
    def has_growth(self):
        """
        Element has_growth ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 236
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_growth(self._handle)
    
    @has_growth.setter
    def has_growth(self, has_growth):
        _pyhmcode.f90wrap_cosmology__set__has_growth(self._handle, has_growth)
    
    @property
    def has_sigma(self):
        """
        Element has_sigma ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 236
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_sigma(self._handle)
    
    @has_sigma.setter
    def has_sigma(self, has_sigma):
        _pyhmcode.f90wrap_cosmology__set__has_sigma(self._handle, has_sigma)
    
    @property
    def has_spherical(self):
        """
        Element has_spherical ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 236
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_spherical(self._handle)
    
    @has_spherical.setter
    def has_spherical(self, has_spherical):
        _pyhmcode.f90wrap_cosmology__set__has_spherical(self._handle, has_spherical)
    
    @property
    def has_power(self):
        """
        Element has_power ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 236
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_power(self._handle)
    
    @has_power.setter
    def has_power(self, has_power):
        _pyhmcode.f90wrap_cosmology__set__has_power(self._handle, has_power)
    
    @property
    def has_wiggle(self):
        """
        Element has_wiggle ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 237
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_wiggle(self._handle)
    
    @has_wiggle.setter
    def has_wiggle(self, has_wiggle):
        _pyhmcode.f90wrap_cosmology__set__has_wiggle(self._handle, has_wiggle)
    
    @property
    def has_spt(self):
        """
        Element has_spt ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 237
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_spt(self._handle)
    
    @has_spt.setter
    def has_spt(self, has_spt):
        _pyhmcode.f90wrap_cosmology__set__has_spt(self._handle, has_spt)
    
    @property
    def has_time(self):
        """
        Element has_time ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 237
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_time(self._handle)
    
    @has_time.setter
    def has_time(self, has_time):
        _pyhmcode.f90wrap_cosmology__set__has_time(self._handle, has_time)
    
    @property
    def has_xde(self):
        """
        Element has_xde ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 237
        
        """
        return _pyhmcode.f90wrap_cosmology__get__has_xde(self._handle)
    
    @has_xde.setter
    def has_xde(self, has_xde):
        _pyhmcode.f90wrap_cosmology__set__has_xde(self._handle, has_xde)
    
    @property
    def is_init(self):
        """
        Element is_init ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 238
        
        """
        return _pyhmcode.f90wrap_cosmology__get__is_init(self._handle)
    
    @is_init.setter
    def is_init(self, is_init):
        _pyhmcode.f90wrap_cosmology__set__is_init(self._handle, is_init)
    
    @property
    def is_normalised(self):
        """
        Element is_normalised ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 238
        
        """
        return _pyhmcode.f90wrap_cosmology__get__is_normalised(self._handle)
    
    @is_normalised.setter
    def is_normalised(self, is_normalised):
        _pyhmcode.f90wrap_cosmology__set__is_normalised(self._handle, is_normalised)
    
    @property
    def camb_exe(self):
        """
        Element camb_exe ftype=character(len=256) pytype=str
        
        
        Defined at ../library/src/cosmology_functions.f90 line 240
        
        """
        return _pyhmcode.f90wrap_cosmology__get__camb_exe(self._handle)
    
    @camb_exe.setter
    def camb_exe(self, camb_exe):
        _pyhmcode.f90wrap_cosmology__set__camb_exe(self._handle, camb_exe)
    
    @property
    def camb_temp_dir(self):
        """
        Element camb_temp_dir ftype=character(len=256) pytype=str
        
        
        Defined at ../library/src/cosmology_functions.f90 line 240
        
        """
        return _pyhmcode.f90wrap_cosmology__get__camb_temp_dir(self._handle)
    
    @camb_temp_dir.setter
    def camb_temp_dir(self, camb_temp_dir):
        _pyhmcode.f90wrap_cosmology__set__camb_temp_dir(self._handle, camb_temp_dir)
    
    @property
    def verbose(self):
        """
        Element verbose ftype=logical pytype=bool
        
        
        Defined at ../library/src/cosmology_functions.f90 line 242
        
        """
        return _pyhmcode.f90wrap_cosmology__get__verbose(self._handle)
    
    @verbose.setter
    def verbose(self, verbose):
        _pyhmcode.f90wrap_cosmology__set__verbose(self._handle, verbose)
    
    @property
    def status(self):
        """
        Element status ftype=integer  pytype=int
        
        
        Defined at ../library/src/cosmology_functions.f90 line 244
        
        """
        return _pyhmcode.f90wrap_cosmology__get__status(self._handle)
    
    @status.setter
    def status(self, status):
        _pyhmcode.f90wrap_cosmology__set__status(self._handle, status)
    
    def __str__(self):
        ret = ['<cosmology>{\n']
        ret.append('    name : ')
        ret.append(repr(self.name))
        ret.append(',\n    om_m : ')
        ret.append(repr(self.om_m))
        ret.append(',\n    om_b : ')
        ret.append(repr(self.om_b))
        ret.append(',\n    om_v : ')
        ret.append(repr(self.om_v))
        ret.append(',\n    om_w : ')
        ret.append(repr(self.om_w))
        ret.append(',\n    ns : ')
        ret.append(repr(self.ns))
        ret.append(',\n    nrun : ')
        ret.append(repr(self.nrun))
        ret.append(',\n    nrunrun : ')
        ret.append(repr(self.nrunrun))
        ret.append(',\n    h : ')
        ret.append(repr(self.h))
        ret.append(',\n    w : ')
        ret.append(repr(self.w))
        ret.append(',\n    wa : ')
        ret.append(repr(self.wa))
        ret.append(',\n    m_wdm : ')
        ret.append(repr(self.m_wdm))
        ret.append(',\n    yh : ')
        ret.append(repr(self.yh))
        ret.append(',\n    a1 : ')
        ret.append(repr(self.a1))
        ret.append(',\n    a2 : ')
        ret.append(repr(self.a2))
        ret.append(',\n    nstar : ')
        ret.append(repr(self.nstar))
        ret.append(',\n    ws : ')
        ret.append(repr(self.ws))
        ret.append(',\n    am : ')
        ret.append(repr(self.am))
        ret.append(',\n    dm : ')
        ret.append(repr(self.dm))
        ret.append(',\n    wm : ')
        ret.append(repr(self.wm))
        ret.append(',\n    t_cmb : ')
        ret.append(repr(self.t_cmb))
        ret.append(',\n    neff : ')
        ret.append(repr(self.neff))
        ret.append(',\n    m_nu : ')
        ret.append(repr(self.m_nu))
        ret.append(',\n    h0rc : ')
        ret.append(repr(self.h0rc))
        ret.append(',\n    fr0 : ')
        ret.append(repr(self.fr0))
        ret.append(',\n    nfr : ')
        ret.append(repr(self.nfr))
        ret.append(',\n    om_m_pow : ')
        ret.append(repr(self.om_m_pow))
        ret.append(',\n    om_b_pow : ')
        ret.append(repr(self.om_b_pow))
        ret.append(',\n    h_pow : ')
        ret.append(repr(self.h_pow))
        ret.append(',\n    b0 : ')
        ret.append(repr(self.b0))
        ret.append(',\n    b1 : ')
        ret.append(repr(self.b1))
        ret.append(',\n    b2 : ')
        ret.append(repr(self.b2))
        ret.append(',\n    b3 : ')
        ret.append(repr(self.b3))
        ret.append(',\n    b4 : ')
        ret.append(repr(self.b4))
        ret.append(',\n    a_bump : ')
        ret.append(repr(self.a_bump))
        ret.append(',\n    k_bump : ')
        ret.append(repr(self.k_bump))
        ret.append(',\n    sigma_bump : ')
        ret.append(repr(self.sigma_bump))
        ret.append(',\n    theat : ')
        ret.append(repr(self.theat))
        ret.append(',\n    lbox : ')
        ret.append(repr(self.lbox))
        ret.append(',\n    n_nu : ')
        ret.append(repr(self.n_nu))
        ret.append(',\n    bump : ')
        ret.append(repr(self.bump))
        ret.append(',\n    norm_method : ')
        ret.append(repr(self.norm_method))
        ret.append(',\n    iw : ')
        ret.append(repr(self.iw))
        ret.append(',\n    img : ')
        ret.append(repr(self.img))
        ret.append(',\n    itk : ')
        ret.append(repr(self.itk))
        ret.append(',\n    itc : ')
        ret.append(repr(self.itc))
        ret.append(',\n    box : ')
        ret.append(repr(self.box))
        ret.append(',\n    warm : ')
        ret.append(repr(self.warm))
        ret.append(',\n    power_omegas : ')
        ret.append(repr(self.power_omegas))
        ret.append(',\n    derive_gas_numbers : ')
        ret.append(repr(self.derive_gas_numbers))
        ret.append(',\n    kpiv : ')
        ret.append(repr(self.kpiv))
        ret.append(',\n    as_ : ')
        ret.append(repr(self.as_))
        ret.append(',\n    kval : ')
        ret.append(repr(self.kval))
        ret.append(',\n    pval : ')
        ret.append(repr(self.pval))
        ret.append(',\n    sig8 : ')
        ret.append(repr(self.sig8))
        ret.append(',\n    mue : ')
        ret.append(repr(self.mue))
        ret.append(',\n    mup : ')
        ret.append(repr(self.mup))
        ret.append(',\n    a : ')
        ret.append(repr(self.a))
        ret.append(',\n    om : ')
        ret.append(repr(self.om))
        ret.append(',\n    om_k : ')
        ret.append(repr(self.om_k))
        ret.append(',\n    om_c : ')
        ret.append(repr(self.om_c))
        ret.append(',\n    om_g : ')
        ret.append(repr(self.om_g))
        ret.append(',\n    om_r : ')
        ret.append(repr(self.om_r))
        ret.append(',\n    om_nu : ')
        ret.append(repr(self.om_nu))
        ret.append(',\n    f_nu : ')
        ret.append(repr(self.f_nu))
        ret.append(',\n    a_nu : ')
        ret.append(repr(self.a_nu))
        ret.append(',\n    om_nu_rad : ')
        ret.append(repr(self.om_nu_rad))
        ret.append(',\n    omega_nu : ')
        ret.append(repr(self.omega_nu))
        ret.append(',\n    t_nu : ')
        ret.append(repr(self.t_nu))
        ret.append(',\n    omega_m : ')
        ret.append(repr(self.omega_m))
        ret.append(',\n    omega_b : ')
        ret.append(repr(self.omega_b))
        ret.append(',\n    omega_c : ')
        ret.append(repr(self.omega_c))
        ret.append(',\n    k : ')
        ret.append(repr(self.k))
        ret.append(',\n    z_cmb : ')
        ret.append(repr(self.z_cmb))
        ret.append(',\n    om_c_pow : ')
        ret.append(repr(self.om_c_pow))
        ret.append(',\n    age : ')
        ret.append(repr(self.age))
        ret.append(',\n    horizon : ')
        ret.append(repr(self.horizon))
        ret.append(',\n    yhe : ')
        ret.append(repr(self.yhe))
        ret.append(',\n    om_ws : ')
        ret.append(repr(self.om_ws))
        ret.append(',\n    astar : ')
        ret.append(repr(self.astar))
        ret.append(',\n    a1n : ')
        ret.append(repr(self.a1n))
        ret.append(',\n    a2n : ')
        ret.append(repr(self.a2n))
        ret.append(',\n    om_de : ')
        ret.append(repr(self.om_de))
        ret.append(',\n    gnorm : ')
        ret.append(repr(self.gnorm))
        ret.append(',\n    kbox : ')
        ret.append(repr(self.kbox))
        ret.append(',\n    scale_dependent_growth : ')
        ret.append(repr(self.scale_dependent_growth))
        ret.append(',\n    k_plin : ')
        ret.append(repr(self.k_plin))
        ret.append(',\n    a_plin : ')
        ret.append(repr(self.a_plin))
        ret.append(',\n    plin_array : ')
        ret.append(repr(self.plin_array))
        ret.append(',\n    analytical_tk : ')
        ret.append(repr(self.analytical_tk))
        ret.append(',\n    has_distance : ')
        ret.append(repr(self.has_distance))
        ret.append(',\n    has_growth : ')
        ret.append(repr(self.has_growth))
        ret.append(',\n    has_sigma : ')
        ret.append(repr(self.has_sigma))
        ret.append(',\n    has_spherical : ')
        ret.append(repr(self.has_spherical))
        ret.append(',\n    has_power : ')
        ret.append(repr(self.has_power))
        ret.append(',\n    has_wiggle : ')
        ret.append(repr(self.has_wiggle))
        ret.append(',\n    has_spt : ')
        ret.append(repr(self.has_spt))
        ret.append(',\n    has_time : ')
        ret.append(repr(self.has_time))
        ret.append(',\n    has_xde : ')
        ret.append(repr(self.has_xde))
        ret.append(',\n    is_init : ')
        ret.append(repr(self.is_init))
        ret.append(',\n    is_normalised : ')
        ret.append(repr(self.is_normalised))
        ret.append(',\n    camb_exe : ')
        ret.append(repr(self.camb_exe))
        ret.append(',\n    camb_temp_dir : ')
        ret.append(repr(self.camb_temp_dir))
        ret.append(',\n    verbose : ')
        ret.append(repr(self.verbose))
        ret.append(',\n    status : ')
        ret.append(repr(self.status))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def assign_cosmology(icosmo, cosm, verbose):
    """
    assign_cosmology(icosmo, cosm, verbose)
    
    
    Defined at ../library/src/cosmology_functions.f90 lines 541-1646
    
    Parameters
    ----------
    icosmo : int
    cosm : Cosmology
    verbose : bool
    
    """
    _pyhmcode.f90wrap_assign_cosmology(icosmo=icosmo, cosm=cosm._handle, \
        verbose=verbose)

def init_cosmology(self):
    """
    init_cosmology(self)
    
    
    Defined at ../library/src/cosmology_functions.f90 lines 1648-1861
    
    Parameters
    ----------
    cosm : Cosmology
    
    """
    _pyhmcode.f90wrap_init_cosmology(cosm=self._handle)

def print_cosmology(self):
    """
    print_cosmology(self)
    
    
    Defined at ../library/src/cosmology_functions.f90 lines 1863-2015
    
    Parameters
    ----------
    cosm : Cosmology
    
    """
    _pyhmcode.f90wrap_print_cosmology(cosm=self._handle)

def init_external_linear_power_tables(self, k, a, pk):
    """
    init_external_linear_power_tables(self, k, a, pk)
    
    
    Defined at ../library/src/cosmology_functions.f90 lines 4924-4960
    
    Parameters
    ----------
    cosm : Cosmology
    k : float array
    a : float array
    pk : float array
    
    """
    _pyhmcode.f90wrap_init_external_linear_power_tables(cosm=self._handle, k=k, a=a, \
        pk=pk)

def get_iw_lcdm():
    """
    Element iw_lcdm ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 267
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_lcdm()

iw_LCDM = get_iw_lcdm()

def get_iw_quicc():
    """
    Element iw_quicc ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 268
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_quicc()

iw_QUICC = get_iw_quicc()

def get_iw_wacdm():
    """
    Element iw_wacdm ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 269
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_wacdm()

iw_waCDM = get_iw_wacdm()

def get_iw_wcdm():
    """
    Element iw_wcdm ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 270
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_wcdm()

iw_wCDM = get_iw_wcdm()

def get_iw_ide1():
    """
    Element iw_ide1 ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 271
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_ide1()

iw_IDE1 = get_iw_ide1()

def get_iw_ide2():
    """
    Element iw_ide2 ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 272
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_ide2()

iw_IDE2 = get_iw_ide2()

def get_iw_ide3():
    """
    Element iw_ide3 ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 273
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_ide3()

iw_IDE3 = get_iw_ide3()

def get_iw_bde():
    """
    Element iw_bde ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 274
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__iw_bde()

iw_BDE = get_iw_bde()

def get_img_none():
    """
    Element img_none ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 286
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__img_none()

img_none = get_img_none()

def get_img_ndgp():
    """
    Element img_ndgp ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 287
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__img_ndgp()

img_nDGP = get_img_ndgp()

def get_img_fr():
    """
    Element img_fr ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 288
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__img_fr()

img_fR = get_img_fr()

def get_img_ndgp_lin():
    """
    Element img_ndgp_lin ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 289
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__img_ndgp_lin()

img_nDGP_lin = get_img_ndgp_lin()

def get_img_fr_lin():
    """
    Element img_fr_lin ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 290
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__img_fr_lin()

img_fR_lin = get_img_fr_lin()

def get_itk_none():
    """
    Element itk_none ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 313
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__itk_none()

iTk_none = get_itk_none()

def get_itk_eh():
    """
    Element itk_eh ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 314
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__itk_eh()

iTk_EH = get_itk_eh()

def get_itk_camb():
    """
    Element itk_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 315
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__itk_camb()

iTk_CAMB = get_itk_camb()

def get_itk_defw():
    """
    Element itk_defw ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 316
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__itk_defw()

iTk_DEFW = get_itk_defw()

def get_itk_external():
    """
    Element itk_external ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 317
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__itk_external()

iTk_external = get_itk_external()

def get_itk_nw():
    """
    Element itk_nw ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 318
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__itk_nw()

iTk_nw = get_itk_nw()

def get_itk_bbks():
    """
    Element itk_bbks ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 319
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__itk_bbks()

iTk_BBKS = get_itk_bbks()

def get_norm_none():
    """
    Element norm_none ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 320
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__norm_none()

norm_none = get_norm_none()

def get_norm_sigma8():
    """
    Element norm_sigma8 ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 321
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__norm_sigma8()

norm_sigma8 = get_norm_sigma8()

def get_norm_pval():
    """
    Element norm_pval ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 322
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__norm_pval()

norm_pval = get_norm_pval()

def get_norm_as():
    """
    Element norm_as ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 323
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__norm_as()

norm_As = get_norm_as()

def get_flag_matter():
    """
    Element flag_matter ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 324
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__flag_matter()

flag_matter = get_flag_matter()

def get_flag_cold():
    """
    Element flag_cold ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 325
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__flag_cold()

flag_cold = get_flag_cold()

def get_flag_ucold():
    """
    Element flag_ucold ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 326
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__flag_ucold()

flag_ucold = get_flag_ucold()

def get_growth_index_default():
    """
    Element growth_index_default ftype=real pytype=float
    
    
    Defined at ../library/src/cosmology_functions.f90 line 423
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__growth_index_default()

growth_index_default = get_growth_index_default()

def get_halofit_smith_code():
    """
    Element halofit_smith_code ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 481
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_smith_code()

HALOFIT_Smith_code = get_halofit_smith_code()

def get_halofit_bird_code():
    """
    Element halofit_bird_code ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 482
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_bird_code()

HALOFIT_Bird_code = get_halofit_bird_code()

def get_halofit_takahashi():
    """
    Element halofit_takahashi ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 483
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_takahashi()

HALOFIT_Takahashi = get_halofit_takahashi()

def get_halofit_camb():
    """
    Element halofit_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 484
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_camb()

HALOFIT_CAMB = get_halofit_camb()

def get_halofit_class():
    """
    Element halofit_class ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 485
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_class()

HALOFIT_CLASS = get_halofit_class()

def get_halofit_smith_paper():
    """
    Element halofit_smith_paper ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 486
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_smith_paper()

HALOFIT_Smith_paper = get_halofit_smith_paper()

def get_halofit_bird_paper():
    """
    Element halofit_bird_paper ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 487
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_bird_paper()

HALOFIT_Bird_paper = get_halofit_bird_paper()

def get_halofit_bird_camb():
    """
    Element halofit_bird_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 488
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__halofit_bird_camb()

HALOFIT_Bird_CAMB = get_halofit_bird_camb()

def get_camb_halofit_smith():
    """
    Element camb_halofit_smith ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 494
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_halofit_smith()

CAMB_HALOFIT_Smith = get_camb_halofit_smith()

def get_camb_halofit_bird():
    """
    Element camb_halofit_bird ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 495
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_halofit_bird()

CAMB_HALOFIT_Bird = get_camb_halofit_bird()

def get_camb_halofit_takahashi():
    """
    Element camb_halofit_takahashi ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 496
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_halofit_takahashi()

CAMB_HALOFIT_Takahashi = get_camb_halofit_takahashi()

def get_camb_halofit_smith_paper():
    """
    Element camb_halofit_smith_paper ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 497
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_halofit_smith_paper()

CAMB_HALOFIT_Smith_paper = get_camb_halofit_smith_paper()

def get_camb_halofit_bird_paper():
    """
    Element camb_halofit_bird_paper ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 498
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_halofit_bird_paper()

CAMB_HALOFIT_Bird_paper = get_camb_halofit_bird_paper()

def get_camb_halofit_takahashi_paper():
    """
    Element camb_halofit_takahashi_paper ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 499
    
    """
    return \
        _pyhmcode.f90wrap_cosmology_functions__get__camb_halofit_takahashi_paper()

CAMB_HALOFIT_Takahashi_paper = get_camb_halofit_takahashi_paper()

def get_camb_hmcode2015():
    """
    Element camb_hmcode2015 ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 500
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_hmcode2015()

CAMB_HMcode2015 = get_camb_hmcode2015()

def get_camb_hmcode2016():
    """
    Element camb_hmcode2016 ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 501
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_hmcode2016()

CAMB_HMcode2016 = get_camb_hmcode2016()

def get_camb_hmcode2020():
    """
    Element camb_hmcode2020 ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 502
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_hmcode2020()

CAMB_HMcode2020 = get_camb_hmcode2020()

def get_camb_hmcode2020_feedback():
    """
    Element camb_hmcode2020_feedback ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 503
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__camb_hmcode2020_feedback()

CAMB_HMcode2020_feedback = get_camb_hmcode2020_feedback()

def get_irescale_sigma():
    """
    Element irescale_sigma ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 519
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__irescale_sigma()

irescale_sigma = get_irescale_sigma()

def get_irescale_power():
    """
    Element irescale_power ftype=integer pytype=int
    
    
    Defined at ../library/src/cosmology_functions.f90 line 520
    
    """
    return _pyhmcode.f90wrap_cosmology_functions__get__irescale_power()

irescale_power = get_irescale_power()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "cosmology_functions".')

for func in _dt_array_initialisers:
    func()
