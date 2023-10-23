"""
Module hmx


Defined at ../library/src/hmx.f90 lines 1-9926

"""
from __future__ import print_function, absolute_import, division
from . import _pyhmcode
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("pyhmcode.halomod")
class halomod(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=halomod)
    
    
    Defined at ../library/src/hmx.f90 lines 315-433
    
    """
    def __init__(self, handle=None):
        """
        self = Halomod()
        
        
        Defined at ../library/src/hmx.f90 lines 315-433
        
        
        Returns
        -------
        this : Halomod
        	Object to be constructed
        
        
        Automatically generated constructor for halomod
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _pyhmcode.f90wrap_halomod_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Halomod
        
        
        Defined at ../library/src/hmx.f90 lines 315-433
        
        Parameters
        ----------
        this : Halomod
        	Object to be destructed
        
        
        Automatically generated destructor for halomod
        """
        if self._alloc:
            _pyhmcode.f90wrap_halomod_finalise(this=self._handle)
    
    @property
    def ihm(self):
        """
        Element ihm ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 317
        
        """
        return _pyhmcode.f90wrap_halomod__get__ihm(self._handle)
    
    @ihm.setter
    def ihm(self, ihm):
        _pyhmcode.f90wrap_halomod__set__ihm(self._handle, ihm)
    
    @property
    def z(self):
        """
        Element z ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 319
        
        """
        return _pyhmcode.f90wrap_halomod__get__z(self._handle)
    
    @z.setter
    def z(self, z):
        _pyhmcode.f90wrap_halomod__set__z(self._handle, z)
    
    @property
    def a(self):
        """
        Element a ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 319
        
        """
        return _pyhmcode.f90wrap_halomod__get__a(self._handle)
    
    @a.setter
    def a(self, a):
        _pyhmcode.f90wrap_halomod__set__a(self._handle, a)
    
    @property
    def ip2h(self):
        """
        Element ip2h ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__ip2h(self._handle)
    
    @ip2h.setter
    def ip2h(self, ip2h):
        _pyhmcode.f90wrap_halomod__set__ip2h(self._handle, ip2h)
    
    @property
    def ip1h(self):
        """
        Element ip1h ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__ip1h(self._handle)
    
    @ip1h.setter
    def ip1h(self, ip1h):
        _pyhmcode.f90wrap_halomod__set__ip1h(self._handle, ip1h)
    
    @property
    def ibias(self):
        """
        Element ibias ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__ibias(self._handle)
    
    @ibias.setter
    def ibias(self, ibias):
        _pyhmcode.f90wrap_halomod__set__ibias(self._handle, ibias)
    
    @property
    def imf(self):
        """
        Element imf ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__imf(self._handle)
    
    @imf.setter
    def imf(self, imf):
        _pyhmcode.f90wrap_halomod__set__imf(self._handle, imf)
    
    @property
    def iconc(self):
        """
        Element iconc ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__iconc(self._handle)
    
    @iconc.setter
    def iconc(self, iconc):
        _pyhmcode.f90wrap_halomod__set__iconc(self._handle, iconc)
    
    @property
    def idolag(self):
        """
        Element idolag ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__idolag(self._handle)
    
    @idolag.setter
    def idolag(self, idolag):
        _pyhmcode.f90wrap_halomod__set__idolag(self._handle, idolag)
    
    @property
    def ias(self):
        """
        Element ias ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__ias(self._handle)
    
    @ias.setter
    def ias(self, ias):
        _pyhmcode.f90wrap_halomod__set__ias(self._handle, ias)
    
    @property
    def i2hcor(self):
        """
        Element i2hcor ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 321
        
        """
        return _pyhmcode.f90wrap_halomod__get__i2hcor(self._handle)
    
    @i2hcor.setter
    def i2hcor(self, i2hcor):
        _pyhmcode.f90wrap_halomod__set__i2hcor(self._handle, i2hcor)
    
    @property
    def idc(self):
        """
        Element idc ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 322
        
        """
        return _pyhmcode.f90wrap_halomod__get__idc(self._handle)
    
    @idc.setter
    def idc(self, idc):
        _pyhmcode.f90wrap_halomod__set__idc(self._handle, idc)
    
    @property
    def idv(self):
        """
        Element idv ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 322
        
        """
        return _pyhmcode.f90wrap_halomod__get__idv(self._handle)
    
    @idv.setter
    def idv(self, idv):
        _pyhmcode.f90wrap_halomod__set__idv(self._handle, idv)
    
    @property
    def ieta(self):
        """
        Element ieta ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 322
        
        """
        return _pyhmcode.f90wrap_halomod__get__ieta(self._handle)
    
    @ieta.setter
    def ieta(self, ieta):
        _pyhmcode.f90wrap_halomod__set__ieta(self._handle, ieta)
    
    @property
    def i2hdamp(self):
        """
        Element i2hdamp ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 322
        
        """
        return _pyhmcode.f90wrap_halomod__get__i2hdamp(self._handle)
    
    @i2hdamp.setter
    def i2hdamp(self, i2hdamp):
        _pyhmcode.f90wrap_halomod__set__i2hdamp(self._handle, i2hdamp)
    
    @property
    def i1hdamp(self):
        """
        Element i1hdamp ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 322
        
        """
        return _pyhmcode.f90wrap_halomod__get__i1hdamp(self._handle)
    
    @i1hdamp.setter
    def i1hdamp(self, i1hdamp):
        _pyhmcode.f90wrap_halomod__set__i1hdamp(self._handle, i1hdamp)
    
    @property
    def itrans(self):
        """
        Element itrans ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 322
        
        """
        return _pyhmcode.f90wrap_halomod__get__itrans(self._handle)
    
    @itrans.setter
    def itrans(self, itrans):
        _pyhmcode.f90wrap_halomod__set__itrans(self._handle, itrans)
    
    @property
    def ikdamp(self):
        """
        Element ikdamp ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 322
        
        """
        return _pyhmcode.f90wrap_halomod__get__ikdamp(self._handle)
    
    @ikdamp.setter
    def ikdamp(self, ikdamp):
        _pyhmcode.f90wrap_halomod__set__ikdamp(self._handle, ikdamp)
    
    @property
    def flag_sigma(self):
        """
        Element flag_sigma ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 324
        
        """
        return _pyhmcode.f90wrap_halomod__get__flag_sigma(self._handle)
    
    @flag_sigma.setter
    def flag_sigma(self, flag_sigma):
        _pyhmcode.f90wrap_halomod__set__flag_sigma(self._handle, flag_sigma)
    
    @property
    def add_voids(self):
        """
        Element add_voids ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 326
        
        """
        return _pyhmcode.f90wrap_halomod__get__add_voids(self._handle)
    
    @add_voids.setter
    def add_voids(self, add_voids):
        _pyhmcode.f90wrap_halomod__set__add_voids(self._handle, add_voids)
    
    @property
    def add_variances(self):
        """
        Element add_variances ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 326
        
        """
        return _pyhmcode.f90wrap_halomod__get__add_variances(self._handle)
    
    @add_variances.setter
    def add_variances(self, add_variances):
        _pyhmcode.f90wrap_halomod__set__add_variances(self._handle, add_variances)
    
    @property
    def add_shotnoise(self):
        """
        Element add_shotnoise ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 326
        
        """
        return _pyhmcode.f90wrap_halomod__get__add_shotnoise(self._handle)
    
    @add_shotnoise.setter
    def add_shotnoise(self, add_shotnoise):
        _pyhmcode.f90wrap_halomod__set__add_shotnoise(self._handle, add_shotnoise)
    
    @property
    def proper_discrete(self):
        """
        Element proper_discrete ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 326
        
        """
        return _pyhmcode.f90wrap_halomod__get__proper_discrete(self._handle)
    
    @proper_discrete.setter
    def proper_discrete(self, proper_discrete):
        _pyhmcode.f90wrap_halomod__set__proper_discrete(self._handle, proper_discrete)
    
    @property
    def consistency(self):
        """
        Element consistency ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 326
        
        """
        return _pyhmcode.f90wrap_halomod__get__consistency(self._handle)
    
    @consistency.setter
    def consistency(self, consistency):
        _pyhmcode.f90wrap_halomod__set__consistency(self._handle, consistency)
    
    @property
    def dc(self):
        """
        Element dc ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 328
        
        """
        return _pyhmcode.f90wrap_halomod__get__dc(self._handle)
    
    @dc.setter
    def dc(self, dc):
        _pyhmcode.f90wrap_halomod__set__dc(self._handle, dc)
    
    @property
    def dv(self):
        """
        Element dv ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 328
        
        """
        return _pyhmcode.f90wrap_halomod__get__dv(self._handle)
    
    @dv.setter
    def dv(self, dv):
        _pyhmcode.f90wrap_halomod__set__dv(self._handle, dv)
    
    @property
    def mass_dependent_dv(self):
        """
        Element mass_dependent_dv ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 329
        
        """
        return _pyhmcode.f90wrap_halomod__get__mass_dependent_dv(self._handle)
    
    @mass_dependent_dv.setter
    def mass_dependent_dv(self, mass_dependent_dv):
        _pyhmcode.f90wrap_halomod__set__mass_dependent_dv(self._handle, \
            mass_dependent_dv)
    
    @property
    def fix_star_concentration(self):
        """
        Element fix_star_concentration ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 331
        
        """
        return _pyhmcode.f90wrap_halomod__get__fix_star_concentration(self._handle)
    
    @fix_star_concentration.setter
    def fix_star_concentration(self, fix_star_concentration):
        _pyhmcode.f90wrap_halomod__set__fix_star_concentration(self._handle, \
            fix_star_concentration)
    
    @property
    def different_gammas(self):
        """
        Element different_gammas ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 331
        
        """
        return _pyhmcode.f90wrap_halomod__get__different_gammas(self._handle)
    
    @different_gammas.setter
    def different_gammas(self, different_gammas):
        _pyhmcode.f90wrap_halomod__set__different_gammas(self._handle, different_gammas)
    
    @property
    def theat_array(self):
        """
        Element theat_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 332
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__theat_array(self._handle)
        if array_handle in self._arrays:
            theat_array = self._arrays[array_handle]
        else:
            theat_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__theat_array)
            self._arrays[array_handle] = theat_array
        return theat_array
    
    @theat_array.setter
    def theat_array(self, theat_array):
        self.theat_array[...] = theat_array
    
    @property
    def pivot_mass(self):
        """
        Element pivot_mass ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 332
        
        """
        return _pyhmcode.f90wrap_halomod__get__pivot_mass(self._handle)
    
    @pivot_mass.setter
    def pivot_mass(self, pivot_mass):
        _pyhmcode.f90wrap_halomod__set__pivot_mass(self._handle, pivot_mass)
    
    @property
    def alpha(self):
        """
        Element alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 333
        
        """
        return _pyhmcode.f90wrap_halomod__get__alpha(self._handle)
    
    @alpha.setter
    def alpha(self, alpha):
        _pyhmcode.f90wrap_halomod__set__alpha(self._handle, alpha)
    
    @property
    def alphap(self):
        """
        Element alphap ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 333
        
        """
        return _pyhmcode.f90wrap_halomod__get__alphap(self._handle)
    
    @alphap.setter
    def alphap(self, alphap):
        _pyhmcode.f90wrap_halomod__set__alphap(self._handle, alphap)
    
    @property
    def alphaz(self):
        """
        Element alphaz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 333
        
        """
        return _pyhmcode.f90wrap_halomod__get__alphaz(self._handle)
    
    @alphaz.setter
    def alphaz(self, alphaz):
        _pyhmcode.f90wrap_halomod__set__alphaz(self._handle, alphaz)
    
    @property
    def alpha_array(self):
        """
        Element alpha_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 333
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__alpha_array(self._handle)
        if array_handle in self._arrays:
            alpha_array = self._arrays[array_handle]
        else:
            alpha_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__alpha_array)
            self._arrays[array_handle] = alpha_array
        return alpha_array
    
    @alpha_array.setter
    def alpha_array(self, alpha_array):
        self.alpha_array[...] = alpha_array
    
    @property
    def alphap_array(self):
        """
        Element alphap_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 333
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__alphap_array(self._handle)
        if array_handle in self._arrays:
            alphap_array = self._arrays[array_handle]
        else:
            alphap_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__alphap_array)
            self._arrays[array_handle] = alphap_array
        return alphap_array
    
    @alphap_array.setter
    def alphap_array(self, alphap_array):
        self.alphap_array[...] = alphap_array
    
    @property
    def alphaz_array(self):
        """
        Element alphaz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 333
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__alphaz_array(self._handle)
        if array_handle in self._arrays:
            alphaz_array = self._arrays[array_handle]
        else:
            alphaz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__alphaz_array)
            self._arrays[array_handle] = alphaz_array
        return alphaz_array
    
    @alphaz_array.setter
    def alphaz_array(self, alphaz_array):
        self.alphaz_array[...] = alphaz_array
    
    @property
    def beta(self):
        """
        Element beta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 334
        
        """
        return _pyhmcode.f90wrap_halomod__get__beta(self._handle)
    
    @beta.setter
    def beta(self, beta):
        _pyhmcode.f90wrap_halomod__set__beta(self._handle, beta)
    
    @property
    def betap(self):
        """
        Element betap ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 334
        
        """
        return _pyhmcode.f90wrap_halomod__get__betap(self._handle)
    
    @betap.setter
    def betap(self, betap):
        _pyhmcode.f90wrap_halomod__set__betap(self._handle, betap)
    
    @property
    def betaz(self):
        """
        Element betaz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 334
        
        """
        return _pyhmcode.f90wrap_halomod__get__betaz(self._handle)
    
    @betaz.setter
    def betaz(self, betaz):
        _pyhmcode.f90wrap_halomod__set__betaz(self._handle, betaz)
    
    @property
    def eps(self):
        """
        Element eps ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 335
        
        """
        return _pyhmcode.f90wrap_halomod__get__eps(self._handle)
    
    @eps.setter
    def eps(self, eps):
        _pyhmcode.f90wrap_halomod__set__eps(self._handle, eps)
    
    @property
    def epsz(self):
        """
        Element epsz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 335
        
        """
        return _pyhmcode.f90wrap_halomod__get__epsz(self._handle)
    
    @epsz.setter
    def epsz(self, epsz):
        _pyhmcode.f90wrap_halomod__set__epsz(self._handle, epsz)
    
    @property
    def eps_array(self):
        """
        Element eps_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 335
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__eps_array(self._handle)
        if array_handle in self._arrays:
            eps_array = self._arrays[array_handle]
        else:
            eps_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__eps_array)
            self._arrays[array_handle] = eps_array
        return eps_array
    
    @eps_array.setter
    def eps_array(self, eps_array):
        self.eps_array[...] = eps_array
    
    @property
    def epsz_array(self):
        """
        Element epsz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 335
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__epsz_array(self._handle)
        if array_handle in self._arrays:
            epsz_array = self._arrays[array_handle]
        else:
            epsz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__epsz_array)
            self._arrays[array_handle] = epsz_array
        return epsz_array
    
    @epsz_array.setter
    def epsz_array(self, epsz_array):
        self.epsz_array[...] = epsz_array
    
    @property
    def eps2(self):
        """
        Element eps2 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 336
        
        """
        return _pyhmcode.f90wrap_halomod__get__eps2(self._handle)
    
    @eps2.setter
    def eps2(self, eps2):
        _pyhmcode.f90wrap_halomod__set__eps2(self._handle, eps2)
    
    @property
    def eps2z(self):
        """
        Element eps2z ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 336
        
        """
        return _pyhmcode.f90wrap_halomod__get__eps2z(self._handle)
    
    @eps2z.setter
    def eps2z(self, eps2z):
        _pyhmcode.f90wrap_halomod__set__eps2z(self._handle, eps2z)
    
    @property
    def eps2_array(self):
        """
        Element eps2_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 336
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__eps2_array(self._handle)
        if array_handle in self._arrays:
            eps2_array = self._arrays[array_handle]
        else:
            eps2_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__eps2_array)
            self._arrays[array_handle] = eps2_array
        return eps2_array
    
    @eps2_array.setter
    def eps2_array(self, eps2_array):
        self.eps2_array[...] = eps2_array
    
    @property
    def eps2z_array(self):
        """
        Element eps2z_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 336
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__eps2z_array(self._handle)
        if array_handle in self._arrays:
            eps2z_array = self._arrays[array_handle]
        else:
            eps2z_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__eps2z_array)
            self._arrays[array_handle] = eps2z_array
        return eps2z_array
    
    @eps2z_array.setter
    def eps2z_array(self, eps2z_array):
        self.eps2z_array[...] = eps2z_array
    
    @property
    def gamma(self):
        """
        Element gamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 337
        
        """
        return _pyhmcode.f90wrap_halomod__get__gamma(self._handle)
    
    @gamma.setter
    def gamma(self, gamma):
        _pyhmcode.f90wrap_halomod__set__gamma(self._handle, gamma)
    
    @property
    def gammap(self):
        """
        Element gammap ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 337
        
        """
        return _pyhmcode.f90wrap_halomod__get__gammap(self._handle)
    
    @gammap.setter
    def gammap(self, gammap):
        _pyhmcode.f90wrap_halomod__set__gammap(self._handle, gammap)
    
    @property
    def gammaz(self):
        """
        Element gammaz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 337
        
        """
        return _pyhmcode.f90wrap_halomod__get__gammaz(self._handle)
    
    @gammaz.setter
    def gammaz(self, gammaz):
        _pyhmcode.f90wrap_halomod__set__gammaz(self._handle, gammaz)
    
    @property
    def gamma_array(self):
        """
        Element gamma_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 337
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__gamma_array(self._handle)
        if array_handle in self._arrays:
            gamma_array = self._arrays[array_handle]
        else:
            gamma_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__gamma_array)
            self._arrays[array_handle] = gamma_array
        return gamma_array
    
    @gamma_array.setter
    def gamma_array(self, gamma_array):
        self.gamma_array[...] = gamma_array
    
    @property
    def gammap_array(self):
        """
        Element gammap_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 337
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__gammap_array(self._handle)
        if array_handle in self._arrays:
            gammap_array = self._arrays[array_handle]
        else:
            gammap_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__gammap_array)
            self._arrays[array_handle] = gammap_array
        return gammap_array
    
    @gammap_array.setter
    def gammap_array(self, gammap_array):
        self.gammap_array[...] = gammap_array
    
    @property
    def gammaz_array(self):
        """
        Element gammaz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 337
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__gammaz_array(self._handle)
        if array_handle in self._arrays:
            gammaz_array = self._arrays[array_handle]
        else:
            gammaz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__gammaz_array)
            self._arrays[array_handle] = gammaz_array
        return gammaz_array
    
    @gammaz_array.setter
    def gammaz_array(self, gammaz_array):
        self.gammaz_array[...] = gammaz_array
    
    @property
    def zamma(self):
        """
        Element zamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 338
        
        """
        return _pyhmcode.f90wrap_halomod__get__zamma(self._handle)
    
    @zamma.setter
    def zamma(self, zamma):
        _pyhmcode.f90wrap_halomod__set__zamma(self._handle, zamma)
    
    @property
    def zammap(self):
        """
        Element zammap ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 338
        
        """
        return _pyhmcode.f90wrap_halomod__get__zammap(self._handle)
    
    @zammap.setter
    def zammap(self, zammap):
        _pyhmcode.f90wrap_halomod__set__zammap(self._handle, zammap)
    
    @property
    def zammaz(self):
        """
        Element zammaz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 338
        
        """
        return _pyhmcode.f90wrap_halomod__get__zammaz(self._handle)
    
    @zammaz.setter
    def zammaz(self, zammaz):
        _pyhmcode.f90wrap_halomod__set__zammaz(self._handle, zammaz)
    
    @property
    def zamma_array(self):
        """
        Element zamma_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 338
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__zamma_array(self._handle)
        if array_handle in self._arrays:
            zamma_array = self._arrays[array_handle]
        else:
            zamma_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__zamma_array)
            self._arrays[array_handle] = zamma_array
        return zamma_array
    
    @zamma_array.setter
    def zamma_array(self, zamma_array):
        self.zamma_array[...] = zamma_array
    
    @property
    def zammap_array(self):
        """
        Element zammap_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 338
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__zammap_array(self._handle)
        if array_handle in self._arrays:
            zammap_array = self._arrays[array_handle]
        else:
            zammap_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__zammap_array)
            self._arrays[array_handle] = zammap_array
        return zammap_array
    
    @zammap_array.setter
    def zammap_array(self, zammap_array):
        self.zammap_array[...] = zammap_array
    
    @property
    def zammaz_array(self):
        """
        Element zammaz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 338
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__zammaz_array(self._handle)
        if array_handle in self._arrays:
            zammaz_array = self._arrays[array_handle]
        else:
            zammaz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__zammaz_array)
            self._arrays[array_handle] = zammaz_array
        return zammaz_array
    
    @zammaz_array.setter
    def zammaz_array(self, zammaz_array):
        self.zammaz_array[...] = zammaz_array
    
    @property
    def m0(self):
        """
        Element m0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 339
        
        """
        return _pyhmcode.f90wrap_halomod__get__m0(self._handle)
    
    @m0.setter
    def m0(self, m0):
        _pyhmcode.f90wrap_halomod__set__m0(self._handle, m0)
    
    @property
    def m0z(self):
        """
        Element m0z ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 339
        
        """
        return _pyhmcode.f90wrap_halomod__get__m0z(self._handle)
    
    @m0z.setter
    def m0z(self, m0z):
        _pyhmcode.f90wrap_halomod__set__m0z(self._handle, m0z)
    
    @property
    def m0_array(self):
        """
        Element m0_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 339
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__m0_array(self._handle)
        if array_handle in self._arrays:
            m0_array = self._arrays[array_handle]
        else:
            m0_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__m0_array)
            self._arrays[array_handle] = m0_array
        return m0_array
    
    @m0_array.setter
    def m0_array(self, m0_array):
        self.m0_array[...] = m0_array
    
    @property
    def m0z_array(self):
        """
        Element m0z_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 339
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__m0z_array(self._handle)
        if array_handle in self._arrays:
            m0z_array = self._arrays[array_handle]
        else:
            m0z_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__m0z_array)
            self._arrays[array_handle] = m0z_array
        return m0z_array
    
    @m0z_array.setter
    def m0z_array(self, m0z_array):
        self.m0z_array[...] = m0z_array
    
    @property
    def astar(self):
        """
        Element astar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 340
        
        """
        return _pyhmcode.f90wrap_halomod__get__astar(self._handle)
    
    @astar.setter
    def astar(self, astar):
        _pyhmcode.f90wrap_halomod__set__astar(self._handle, astar)
    
    @property
    def astarz(self):
        """
        Element astarz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 340
        
        """
        return _pyhmcode.f90wrap_halomod__get__astarz(self._handle)
    
    @astarz.setter
    def astarz(self, astarz):
        _pyhmcode.f90wrap_halomod__set__astarz(self._handle, astarz)
    
    @property
    def astar_array(self):
        """
        Element astar_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 340
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__astar_array(self._handle)
        if array_handle in self._arrays:
            astar_array = self._arrays[array_handle]
        else:
            astar_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__astar_array)
            self._arrays[array_handle] = astar_array
        return astar_array
    
    @astar_array.setter
    def astar_array(self, astar_array):
        self.astar_array[...] = astar_array
    
    @property
    def astarz_array(self):
        """
        Element astarz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 340
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__astarz_array(self._handle)
        if array_handle in self._arrays:
            astarz_array = self._arrays[array_handle]
        else:
            astarz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__astarz_array)
            self._arrays[array_handle] = astarz_array
        return astarz_array
    
    @astarz_array.setter
    def astarz_array(self, astarz_array):
        self.astarz_array[...] = astarz_array
    
    @property
    def twhim(self):
        """
        Element twhim ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 341
        
        """
        return _pyhmcode.f90wrap_halomod__get__twhim(self._handle)
    
    @twhim.setter
    def twhim(self, twhim):
        _pyhmcode.f90wrap_halomod__set__twhim(self._handle, twhim)
    
    @property
    def twhimz(self):
        """
        Element twhimz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 341
        
        """
        return _pyhmcode.f90wrap_halomod__get__twhimz(self._handle)
    
    @twhimz.setter
    def twhimz(self, twhimz):
        _pyhmcode.f90wrap_halomod__set__twhimz(self._handle, twhimz)
    
    @property
    def twhim_array(self):
        """
        Element twhim_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 341
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__twhim_array(self._handle)
        if array_handle in self._arrays:
            twhim_array = self._arrays[array_handle]
        else:
            twhim_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__twhim_array)
            self._arrays[array_handle] = twhim_array
        return twhim_array
    
    @twhim_array.setter
    def twhim_array(self, twhim_array):
        self.twhim_array[...] = twhim_array
    
    @property
    def twhimz_array(self):
        """
        Element twhimz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 341
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__twhimz_array(self._handle)
        if array_handle in self._arrays:
            twhimz_array = self._arrays[array_handle]
        else:
            twhimz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__twhimz_array)
            self._arrays[array_handle] = twhimz_array
        return twhimz_array
    
    @twhimz_array.setter
    def twhimz_array(self, twhimz_array):
        self.twhimz_array[...] = twhimz_array
    
    @property
    def cstar(self):
        """
        Element cstar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 342
        
        """
        return _pyhmcode.f90wrap_halomod__get__cstar(self._handle)
    
    @cstar.setter
    def cstar(self, cstar):
        _pyhmcode.f90wrap_halomod__set__cstar(self._handle, cstar)
    
    @property
    def cstarp(self):
        """
        Element cstarp ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 342
        
        """
        return _pyhmcode.f90wrap_halomod__get__cstarp(self._handle)
    
    @cstarp.setter
    def cstarp(self, cstarp):
        _pyhmcode.f90wrap_halomod__set__cstarp(self._handle, cstarp)
    
    @property
    def cstarz(self):
        """
        Element cstarz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 342
        
        """
        return _pyhmcode.f90wrap_halomod__get__cstarz(self._handle)
    
    @cstarz.setter
    def cstarz(self, cstarz):
        _pyhmcode.f90wrap_halomod__set__cstarz(self._handle, cstarz)
    
    @property
    def cstar_array(self):
        """
        Element cstar_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 342
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__cstar_array(self._handle)
        if array_handle in self._arrays:
            cstar_array = self._arrays[array_handle]
        else:
            cstar_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__cstar_array)
            self._arrays[array_handle] = cstar_array
        return cstar_array
    
    @cstar_array.setter
    def cstar_array(self, cstar_array):
        self.cstar_array[...] = cstar_array
    
    @property
    def cstarp_array(self):
        """
        Element cstarp_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 342
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__cstarp_array(self._handle)
        if array_handle in self._arrays:
            cstarp_array = self._arrays[array_handle]
        else:
            cstarp_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__cstarp_array)
            self._arrays[array_handle] = cstarp_array
        return cstarp_array
    
    @cstarp_array.setter
    def cstarp_array(self, cstarp_array):
        self.cstarp_array[...] = cstarp_array
    
    @property
    def cstarz_array(self):
        """
        Element cstarz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 342
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__cstarz_array(self._handle)
        if array_handle in self._arrays:
            cstarz_array = self._arrays[array_handle]
        else:
            cstarz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__cstarz_array)
            self._arrays[array_handle] = cstarz_array
        return cstarz_array
    
    @cstarz_array.setter
    def cstarz_array(self, cstarz_array):
        self.cstarz_array[...] = cstarz_array
    
    @property
    def sstar(self):
        """
        Element sstar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 343
        
        """
        return _pyhmcode.f90wrap_halomod__get__sstar(self._handle)
    
    @sstar.setter
    def sstar(self, sstar):
        _pyhmcode.f90wrap_halomod__set__sstar(self._handle, sstar)
    
    @property
    def mstar(self):
        """
        Element mstar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 344
        
        """
        return _pyhmcode.f90wrap_halomod__get__mstar(self._handle)
    
    @mstar.setter
    def mstar(self, mstar):
        _pyhmcode.f90wrap_halomod__set__mstar(self._handle, mstar)
    
    @property
    def mstarz(self):
        """
        Element mstarz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 344
        
        """
        return _pyhmcode.f90wrap_halomod__get__mstarz(self._handle)
    
    @mstarz.setter
    def mstarz(self, mstarz):
        _pyhmcode.f90wrap_halomod__set__mstarz(self._handle, mstarz)
    
    @property
    def mstar_array(self):
        """
        Element mstar_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 344
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__mstar_array(self._handle)
        if array_handle in self._arrays:
            mstar_array = self._arrays[array_handle]
        else:
            mstar_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__mstar_array)
            self._arrays[array_handle] = mstar_array
        return mstar_array
    
    @mstar_array.setter
    def mstar_array(self, mstar_array):
        self.mstar_array[...] = mstar_array
    
    @property
    def mstarz_array(self):
        """
        Element mstarz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 344
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__mstarz_array(self._handle)
        if array_handle in self._arrays:
            mstarz_array = self._arrays[array_handle]
        else:
            mstarz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__mstarz_array)
            self._arrays[array_handle] = mstarz_array
        return mstarz_array
    
    @mstarz_array.setter
    def mstarz_array(self, mstarz_array):
        self.mstarz_array[...] = mstarz_array
    
    @property
    def fcold(self):
        """
        Element fcold ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 345
        
        """
        return _pyhmcode.f90wrap_halomod__get__fcold(self._handle)
    
    @fcold.setter
    def fcold(self, fcold):
        _pyhmcode.f90wrap_halomod__set__fcold(self._handle, fcold)
    
    @property
    def fhot(self):
        """
        Element fhot ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 346
        
        """
        return _pyhmcode.f90wrap_halomod__get__fhot(self._handle)
    
    @fhot.setter
    def fhot(self, fhot):
        _pyhmcode.f90wrap_halomod__set__fhot(self._handle, fhot)
    
    @property
    def eta(self):
        """
        Element eta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 347
        
        """
        return _pyhmcode.f90wrap_halomod__get__eta(self._handle)
    
    @eta.setter
    def eta(self, eta):
        _pyhmcode.f90wrap_halomod__set__eta(self._handle, eta)
    
    @property
    def etaz(self):
        """
        Element etaz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 347
        
        """
        return _pyhmcode.f90wrap_halomod__get__etaz(self._handle)
    
    @etaz.setter
    def etaz(self, etaz):
        _pyhmcode.f90wrap_halomod__set__etaz(self._handle, etaz)
    
    @property
    def eta_array(self):
        """
        Element eta_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 347
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__eta_array(self._handle)
        if array_handle in self._arrays:
            eta_array = self._arrays[array_handle]
        else:
            eta_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__eta_array)
            self._arrays[array_handle] = eta_array
        return eta_array
    
    @eta_array.setter
    def eta_array(self, eta_array):
        self.eta_array[...] = eta_array
    
    @property
    def etaz_array(self):
        """
        Element etaz_array ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 347
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__etaz_array(self._handle)
        if array_handle in self._arrays:
            etaz_array = self._arrays[array_handle]
        else:
            etaz_array = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__etaz_array)
            self._arrays[array_handle] = etaz_array
        return etaz_array
    
    @etaz_array.setter
    def etaz_array(self, etaz_array):
        self.etaz_array[...] = etaz_array
    
    @property
    def ibeta(self):
        """
        Element ibeta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 348
        
        """
        return _pyhmcode.f90wrap_halomod__get__ibeta(self._handle)
    
    @ibeta.setter
    def ibeta(self, ibeta):
        _pyhmcode.f90wrap_halomod__set__ibeta(self._handle, ibeta)
    
    @property
    def ibetap(self):
        """
        Element ibetap ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 348
        
        """
        return _pyhmcode.f90wrap_halomod__get__ibetap(self._handle)
    
    @ibetap.setter
    def ibetap(self, ibetap):
        _pyhmcode.f90wrap_halomod__set__ibetap(self._handle, ibetap)
    
    @property
    def ibetaz(self):
        """
        Element ibetaz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 348
        
        """
        return _pyhmcode.f90wrap_halomod__get__ibetaz(self._handle)
    
    @ibetaz.setter
    def ibetaz(self, ibetaz):
        _pyhmcode.f90wrap_halomod__set__ibetaz(self._handle, ibetaz)
    
    @property
    def gbeta(self):
        """
        Element gbeta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 349
        
        """
        return _pyhmcode.f90wrap_halomod__get__gbeta(self._handle)
    
    @gbeta.setter
    def gbeta(self, gbeta):
        _pyhmcode.f90wrap_halomod__set__gbeta(self._handle, gbeta)
    
    @property
    def gbetaz(self):
        """
        Element gbetaz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 349
        
        """
        return _pyhmcode.f90wrap_halomod__get__gbetaz(self._handle)
    
    @gbetaz.setter
    def gbetaz(self, gbetaz):
        _pyhmcode.f90wrap_halomod__set__gbetaz(self._handle, gbetaz)
    
    @property
    def a_alpha(self):
        """
        Element a_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 353
        
        """
        return _pyhmcode.f90wrap_halomod__get__a_alpha(self._handle)
    
    @a_alpha.setter
    def a_alpha(self, a_alpha):
        _pyhmcode.f90wrap_halomod__set__a_alpha(self._handle, a_alpha)
    
    @property
    def b_alpha(self):
        """
        Element b_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 353
        
        """
        return _pyhmcode.f90wrap_halomod__get__b_alpha(self._handle)
    
    @b_alpha.setter
    def b_alpha(self, b_alpha):
        _pyhmcode.f90wrap_halomod__set__b_alpha(self._handle, b_alpha)
    
    @property
    def c_alpha(self):
        """
        Element c_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 353
        
        """
        return _pyhmcode.f90wrap_halomod__get__c_alpha(self._handle)
    
    @c_alpha.setter
    def c_alpha(self, c_alpha):
        _pyhmcode.f90wrap_halomod__set__c_alpha(self._handle, c_alpha)
    
    @property
    def d_alpha(self):
        """
        Element d_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 353
        
        """
        return _pyhmcode.f90wrap_halomod__get__d_alpha(self._handle)
    
    @d_alpha.setter
    def d_alpha(self, d_alpha):
        _pyhmcode.f90wrap_halomod__set__d_alpha(self._handle, d_alpha)
    
    @property
    def e_alpha(self):
        """
        Element e_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 353
        
        """
        return _pyhmcode.f90wrap_halomod__get__e_alpha(self._handle)
    
    @e_alpha.setter
    def e_alpha(self, e_alpha):
        _pyhmcode.f90wrap_halomod__set__e_alpha(self._handle, e_alpha)
    
    @property
    def a_eps(self):
        """
        Element a_eps ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 354
        
        """
        return _pyhmcode.f90wrap_halomod__get__a_eps(self._handle)
    
    @a_eps.setter
    def a_eps(self, a_eps):
        _pyhmcode.f90wrap_halomod__set__a_eps(self._handle, a_eps)
    
    @property
    def b_eps(self):
        """
        Element b_eps ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 354
        
        """
        return _pyhmcode.f90wrap_halomod__get__b_eps(self._handle)
    
    @b_eps.setter
    def b_eps(self, b_eps):
        _pyhmcode.f90wrap_halomod__set__b_eps(self._handle, b_eps)
    
    @property
    def c_eps(self):
        """
        Element c_eps ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 354
        
        """
        return _pyhmcode.f90wrap_halomod__get__c_eps(self._handle)
    
    @c_eps.setter
    def c_eps(self, c_eps):
        _pyhmcode.f90wrap_halomod__set__c_eps(self._handle, c_eps)
    
    @property
    def d_eps(self):
        """
        Element d_eps ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 354
        
        """
        return _pyhmcode.f90wrap_halomod__get__d_eps(self._handle)
    
    @d_eps.setter
    def d_eps(self, d_eps):
        _pyhmcode.f90wrap_halomod__set__d_eps(self._handle, d_eps)
    
    @property
    def a_gamma(self):
        """
        Element a_gamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 355
        
        """
        return _pyhmcode.f90wrap_halomod__get__a_gamma(self._handle)
    
    @a_gamma.setter
    def a_gamma(self, a_gamma):
        _pyhmcode.f90wrap_halomod__set__a_gamma(self._handle, a_gamma)
    
    @property
    def b_gamma(self):
        """
        Element b_gamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 355
        
        """
        return _pyhmcode.f90wrap_halomod__get__b_gamma(self._handle)
    
    @b_gamma.setter
    def b_gamma(self, b_gamma):
        _pyhmcode.f90wrap_halomod__set__b_gamma(self._handle, b_gamma)
    
    @property
    def c_gamma(self):
        """
        Element c_gamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 355
        
        """
        return _pyhmcode.f90wrap_halomod__get__c_gamma(self._handle)
    
    @c_gamma.setter
    def c_gamma(self, c_gamma):
        _pyhmcode.f90wrap_halomod__set__c_gamma(self._handle, c_gamma)
    
    @property
    def d_gamma(self):
        """
        Element d_gamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 355
        
        """
        return _pyhmcode.f90wrap_halomod__get__d_gamma(self._handle)
    
    @d_gamma.setter
    def d_gamma(self, d_gamma):
        _pyhmcode.f90wrap_halomod__set__d_gamma(self._handle, d_gamma)
    
    @property
    def e_gamma(self):
        """
        Element e_gamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 355
        
        """
        return _pyhmcode.f90wrap_halomod__get__e_gamma(self._handle)
    
    @e_gamma.setter
    def e_gamma(self, e_gamma):
        _pyhmcode.f90wrap_halomod__set__e_gamma(self._handle, e_gamma)
    
    @property
    def a_m0(self):
        """
        Element a_m0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 356
        
        """
        return _pyhmcode.f90wrap_halomod__get__a_m0(self._handle)
    
    @a_m0.setter
    def a_m0(self, a_m0):
        _pyhmcode.f90wrap_halomod__set__a_m0(self._handle, a_m0)
    
    @property
    def b_m0(self):
        """
        Element b_m0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 356
        
        """
        return _pyhmcode.f90wrap_halomod__get__b_m0(self._handle)
    
    @b_m0.setter
    def b_m0(self, b_m0):
        _pyhmcode.f90wrap_halomod__set__b_m0(self._handle, b_m0)
    
    @property
    def c_m0(self):
        """
        Element c_m0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 356
        
        """
        return _pyhmcode.f90wrap_halomod__get__c_m0(self._handle)
    
    @c_m0.setter
    def c_m0(self, c_m0):
        _pyhmcode.f90wrap_halomod__set__c_m0(self._handle, c_m0)
    
    @property
    def d_m0(self):
        """
        Element d_m0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 356
        
        """
        return _pyhmcode.f90wrap_halomod__get__d_m0(self._handle)
    
    @d_m0.setter
    def d_m0(self, d_m0):
        _pyhmcode.f90wrap_halomod__set__d_m0(self._handle, d_m0)
    
    @property
    def e_m0(self):
        """
        Element e_m0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 356
        
        """
        return _pyhmcode.f90wrap_halomod__get__e_m0(self._handle)
    
    @e_m0.setter
    def e_m0(self, e_m0):
        _pyhmcode.f90wrap_halomod__set__e_m0(self._handle, e_m0)
    
    @property
    def a_astar(self):
        """
        Element a_astar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 357
        
        """
        return _pyhmcode.f90wrap_halomod__get__a_astar(self._handle)
    
    @a_astar.setter
    def a_astar(self, a_astar):
        _pyhmcode.f90wrap_halomod__set__a_astar(self._handle, a_astar)
    
    @property
    def b_astar(self):
        """
        Element b_astar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 357
        
        """
        return _pyhmcode.f90wrap_halomod__get__b_astar(self._handle)
    
    @b_astar.setter
    def b_astar(self, b_astar):
        _pyhmcode.f90wrap_halomod__set__b_astar(self._handle, b_astar)
    
    @property
    def c_astar(self):
        """
        Element c_astar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 357
        
        """
        return _pyhmcode.f90wrap_halomod__get__c_astar(self._handle)
    
    @c_astar.setter
    def c_astar(self, c_astar):
        _pyhmcode.f90wrap_halomod__set__c_astar(self._handle, c_astar)
    
    @property
    def d_astar(self):
        """
        Element d_astar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 357
        
        """
        return _pyhmcode.f90wrap_halomod__get__d_astar(self._handle)
    
    @d_astar.setter
    def d_astar(self, d_astar):
        _pyhmcode.f90wrap_halomod__set__d_astar(self._handle, d_astar)
    
    @property
    def a_twhim(self):
        """
        Element a_twhim ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 358
        
        """
        return _pyhmcode.f90wrap_halomod__get__a_twhim(self._handle)
    
    @a_twhim.setter
    def a_twhim(self, a_twhim):
        _pyhmcode.f90wrap_halomod__set__a_twhim(self._handle, a_twhim)
    
    @property
    def b_twhim(self):
        """
        Element b_twhim ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 358
        
        """
        return _pyhmcode.f90wrap_halomod__get__b_twhim(self._handle)
    
    @b_twhim.setter
    def b_twhim(self, b_twhim):
        _pyhmcode.f90wrap_halomod__set__b_twhim(self._handle, b_twhim)
    
    @property
    def c_twhim(self):
        """
        Element c_twhim ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 358
        
        """
        return _pyhmcode.f90wrap_halomod__get__c_twhim(self._handle)
    
    @c_twhim.setter
    def c_twhim(self, c_twhim):
        _pyhmcode.f90wrap_halomod__set__c_twhim(self._handle, c_twhim)
    
    @property
    def d_twhim(self):
        """
        Element d_twhim ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 358
        
        """
        return _pyhmcode.f90wrap_halomod__get__d_twhim(self._handle)
    
    @d_twhim.setter
    def d_twhim(self, d_twhim):
        _pyhmcode.f90wrap_halomod__set__d_twhim(self._handle, d_twhim)
    
    @property
    def mmin(self):
        """
        Element mmin ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 360
        
        """
        return _pyhmcode.f90wrap_halomod__get__mmin(self._handle)
    
    @mmin.setter
    def mmin(self, mmin):
        _pyhmcode.f90wrap_halomod__set__mmin(self._handle, mmin)
    
    @property
    def mmax(self):
        """
        Element mmax ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 360
        
        """
        return _pyhmcode.f90wrap_halomod__get__mmax(self._handle)
    
    @mmax.setter
    def mmax(self, mmax):
        _pyhmcode.f90wrap_halomod__set__mmax(self._handle, mmax)
    
    @property
    def c(self):
        """
        Element c ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__c(self._handle)
        if array_handle in self._arrays:
            c = self._arrays[array_handle]
        else:
            c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__c)
            self._arrays[array_handle] = c
        return c
    
    @c.setter
    def c(self, c):
        self.c[...] = c
    
    @property
    def rv(self):
        """
        Element rv ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__rv(self._handle)
        if array_handle in self._arrays:
            rv = self._arrays[array_handle]
        else:
            rv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__rv)
            self._arrays[array_handle] = rv
        return rv
    
    @rv.setter
    def rv(self, rv):
        self.rv[...] = rv
    
    @property
    def nu(self):
        """
        Element nu ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__nu(self._handle)
        if array_handle in self._arrays:
            nu = self._arrays[array_handle]
        else:
            nu = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__nu)
            self._arrays[array_handle] = nu
        return nu
    
    @nu.setter
    def nu(self, nu):
        self.nu[...] = nu
    
    @property
    def sig(self):
        """
        Element sig ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__sig(self._handle)
        if array_handle in self._arrays:
            sig = self._arrays[array_handle]
        else:
            sig = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__sig)
            self._arrays[array_handle] = sig
        return sig
    
    @sig.setter
    def sig(self, sig):
        self.sig[...] = sig
    
    @property
    def zc(self):
        """
        Element zc ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__zc(self._handle)
        if array_handle in self._arrays:
            zc = self._arrays[array_handle]
        else:
            zc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__zc)
            self._arrays[array_handle] = zc
        return zc
    
    @zc.setter
    def zc(self, zc):
        self.zc[...] = zc
    
    @property
    def m(self):
        """
        Element m ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__m(self._handle)
        if array_handle in self._arrays:
            m = self._arrays[array_handle]
        else:
            m = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__m)
            self._arrays[array_handle] = m
        return m
    
    @m.setter
    def m(self, m):
        self.m[...] = m
    
    @property
    def rr(self):
        """
        Element rr ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__rr(self._handle)
        if array_handle in self._arrays:
            rr = self._arrays[array_handle]
        else:
            rr = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__rr)
            self._arrays[array_handle] = rr
        return rr
    
    @rr.setter
    def rr(self, rr):
        self.rr[...] = rr
    
    @property
    def sigf(self):
        """
        Element sigf ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__sigf(self._handle)
        if array_handle in self._arrays:
            sigf = self._arrays[array_handle]
        else:
            sigf = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__sigf)
            self._arrays[array_handle] = sigf
        return sigf
    
    @sigf.setter
    def sigf(self, sigf):
        self.sigf[...] = sigf
    
    @property
    def log_m(self):
        """
        Element log_m ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 361
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__log_m(self._handle)
        if array_handle in self._arrays:
            log_m = self._arrays[array_handle]
        else:
            log_m = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__log_m)
            self._arrays[array_handle] = log_m
        return log_m
    
    @log_m.setter
    def log_m(self, log_m):
        self.log_m[...] = log_m
    
    @property
    def mvir(self):
        """
        Element mvir ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 362
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__mvir(self._handle)
        if array_handle in self._arrays:
            mvir = self._arrays[array_handle]
        else:
            mvir = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__mvir)
            self._arrays[array_handle] = mvir
        return mvir
    
    @mvir.setter
    def mvir(self, mvir):
        self.mvir[...] = mvir
    
    @property
    def rvir(self):
        """
        Element rvir ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 362
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__rvir(self._handle)
        if array_handle in self._arrays:
            rvir = self._arrays[array_handle]
        else:
            rvir = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__rvir)
            self._arrays[array_handle] = rvir
        return rvir
    
    @rvir.setter
    def rvir(self, rvir):
        self.rvir[...] = rvir
    
    @property
    def cvir(self):
        """
        Element cvir ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 362
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__cvir(self._handle)
        if array_handle in self._arrays:
            cvir = self._arrays[array_handle]
        else:
            cvir = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__cvir)
            self._arrays[array_handle] = cvir
        return cvir
    
    @cvir.setter
    def cvir(self, cvir):
        self.cvir[...] = cvir
    
    @property
    def m500(self):
        """
        Element m500 ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 363
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__m500(self._handle)
        if array_handle in self._arrays:
            m500 = self._arrays[array_handle]
        else:
            m500 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__m500)
            self._arrays[array_handle] = m500
        return m500
    
    @m500.setter
    def m500(self, m500):
        self.m500[...] = m500
    
    @property
    def r500(self):
        """
        Element r500 ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 363
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__r500(self._handle)
        if array_handle in self._arrays:
            r500 = self._arrays[array_handle]
        else:
            r500 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__r500)
            self._arrays[array_handle] = r500
        return r500
    
    @r500.setter
    def r500(self, r500):
        self.r500[...] = r500
    
    @property
    def c500(self):
        """
        Element c500 ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 363
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__c500(self._handle)
        if array_handle in self._arrays:
            c500 = self._arrays[array_handle]
        else:
            c500 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__c500)
            self._arrays[array_handle] = c500
        return c500
    
    @c500.setter
    def c500(self, c500):
        self.c500[...] = c500
    
    @property
    def m200(self):
        """
        Element m200 ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 364
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__m200(self._handle)
        if array_handle in self._arrays:
            m200 = self._arrays[array_handle]
        else:
            m200 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__m200)
            self._arrays[array_handle] = m200
        return m200
    
    @m200.setter
    def m200(self, m200):
        self.m200[...] = m200
    
    @property
    def r200(self):
        """
        Element r200 ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 364
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__r200(self._handle)
        if array_handle in self._arrays:
            r200 = self._arrays[array_handle]
        else:
            r200 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__r200)
            self._arrays[array_handle] = r200
        return r200
    
    @r200.setter
    def r200(self, r200):
        self.r200[...] = r200
    
    @property
    def c200(self):
        """
        Element c200 ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 364
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__c200(self._handle)
        if array_handle in self._arrays:
            c200 = self._arrays[array_handle]
        else:
            c200 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__c200)
            self._arrays[array_handle] = c200
        return c200
    
    @c200.setter
    def c200(self, c200):
        self.c200[...] = c200
    
    @property
    def m500c(self):
        """
        Element m500c ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 365
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__m500c(self._handle)
        if array_handle in self._arrays:
            m500c = self._arrays[array_handle]
        else:
            m500c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__m500c)
            self._arrays[array_handle] = m500c
        return m500c
    
    @m500c.setter
    def m500c(self, m500c):
        self.m500c[...] = m500c
    
    @property
    def r500c(self):
        """
        Element r500c ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 365
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__r500c(self._handle)
        if array_handle in self._arrays:
            r500c = self._arrays[array_handle]
        else:
            r500c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__r500c)
            self._arrays[array_handle] = r500c
        return r500c
    
    @r500c.setter
    def r500c(self, r500c):
        self.r500c[...] = r500c
    
    @property
    def c500c(self):
        """
        Element c500c ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 365
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__c500c(self._handle)
        if array_handle in self._arrays:
            c500c = self._arrays[array_handle]
        else:
            c500c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__c500c)
            self._arrays[array_handle] = c500c
        return c500c
    
    @c500c.setter
    def c500c(self, c500c):
        self.c500c[...] = c500c
    
    @property
    def m200c(self):
        """
        Element m200c ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 366
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__m200c(self._handle)
        if array_handle in self._arrays:
            m200c = self._arrays[array_handle]
        else:
            m200c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__m200c)
            self._arrays[array_handle] = m200c
        return m200c
    
    @m200c.setter
    def m200c(self, m200c):
        self.m200c[...] = m200c
    
    @property
    def r200c(self):
        """
        Element r200c ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 366
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__r200c(self._handle)
        if array_handle in self._arrays:
            r200c = self._arrays[array_handle]
        else:
            r200c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__r200c)
            self._arrays[array_handle] = r200c
        return r200c
    
    @r200c.setter
    def r200c(self, r200c):
        self.r200c[...] = r200c
    
    @property
    def c200c(self):
        """
        Element c200c ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 366
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__c200c(self._handle)
        if array_handle in self._arrays:
            c200c = self._arrays[array_handle]
        else:
            c200c = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__c200c)
            self._arrays[array_handle] = c200c
        return c200c
    
    @c200c.setter
    def c200c(self, c200c):
        self.c200c[...] = c200c
    
    @property
    def n(self):
        """
        Element n ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 367
        
        """
        return _pyhmcode.f90wrap_halomod__get__n(self._handle)
    
    @n.setter
    def n(self, n):
        _pyhmcode.f90wrap_halomod__set__n(self._handle, n)
    
    @property
    def k(self):
        """
        Element k ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 369
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__k(self._handle)
        if array_handle in self._arrays:
            k = self._arrays[array_handle]
        else:
            k = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__k)
            self._arrays[array_handle] = k
        return k
    
    @k.setter
    def k(self, k):
        self.k[...] = k
    
    @property
    def wk(self):
        """
        Element wk ftype=real pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 369
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _pyhmcode.f90wrap_halomod__array__wk(self._handle)
        if array_handle in self._arrays:
            wk = self._arrays[array_handle]
        else:
            wk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _pyhmcode.f90wrap_halomod__array__wk)
            self._arrays[array_handle] = wk
        return wk
    
    @wk.setter
    def wk(self, wk):
        self.wk[...] = wk
    
    @property
    def nk(self):
        """
        Element nk ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 370
        
        """
        return _pyhmcode.f90wrap_halomod__get__nk(self._handle)
    
    @nk.setter
    def nk(self, nk):
        _pyhmcode.f90wrap_halomod__set__nk(self._handle, nk)
    
    @property
    def knl(self):
        """
        Element knl ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__knl(self._handle)
    
    @knl.setter
    def knl(self, knl):
        _pyhmcode.f90wrap_halomod__set__knl(self._handle, knl)
    
    @property
    def rnl(self):
        """
        Element rnl ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__rnl(self._handle)
    
    @rnl.setter
    def rnl(self, rnl):
        _pyhmcode.f90wrap_halomod__set__rnl(self._handle, rnl)
    
    @property
    def mnl(self):
        """
        Element mnl ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__mnl(self._handle)
    
    @mnl.setter
    def mnl(self, mnl):
        _pyhmcode.f90wrap_halomod__set__mnl(self._handle, mnl)
    
    @property
    def rh(self):
        """
        Element rh ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__rh(self._handle)
    
    @rh.setter
    def rh(self, rh):
        _pyhmcode.f90wrap_halomod__set__rh(self._handle, rh)
    
    @property
    def mh(self):
        """
        Element mh ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__mh(self._handle)
    
    @mh.setter
    def mh(self, mh):
        _pyhmcode.f90wrap_halomod__set__mh(self._handle, mh)
    
    @property
    def mp(self):
        """
        Element mp ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__mp(self._handle)
    
    @mp.setter
    def mp(self, mp):
        _pyhmcode.f90wrap_halomod__set__mp(self._handle, mp)
    
    @property
    def sigv(self):
        """
        Element sigv ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__sigv(self._handle)
    
    @sigv.setter
    def sigv(self, sigv):
        _pyhmcode.f90wrap_halomod__set__sigv(self._handle, sigv)
    
    @property
    def rhh(self):
        """
        Element rhh ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__rhh(self._handle)
    
    @rhh.setter
    def rhh(self, rhh):
        _pyhmcode.f90wrap_halomod__set__rhh(self._handle, rhh)
    
    @property
    def neff(self):
        """
        Element neff ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 372
        
        """
        return _pyhmcode.f90wrap_halomod__get__neff(self._handle)
    
    @neff.setter
    def neff(self, neff):
        _pyhmcode.f90wrap_halomod__set__neff(self._handle, neff)
    
    @property
    def nu_saturation(self):
        """
        Element nu_saturation ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 374
        
        """
        return _pyhmcode.f90wrap_halomod__get__nu_saturation(self._handle)
    
    @nu_saturation.setter
    def nu_saturation(self, nu_saturation):
        _pyhmcode.f90wrap_halomod__set__nu_saturation(self._handle, nu_saturation)
    
    @property
    def saturation(self):
        """
        Element saturation ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 375
        
        """
        return _pyhmcode.f90wrap_halomod__get__saturation(self._handle)
    
    @saturation.setter
    def saturation(self, saturation):
        _pyhmcode.f90wrap_halomod__set__saturation(self._handle, saturation)
    
    @property
    def mhalo_min(self):
        """
        Element mhalo_min ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 377
        
        """
        return _pyhmcode.f90wrap_halomod__get__mhalo_min(self._handle)
    
    @mhalo_min.setter
    def mhalo_min(self, mhalo_min):
        _pyhmcode.f90wrap_halomod__set__mhalo_min(self._handle, mhalo_min)
    
    @property
    def mhalo_max(self):
        """
        Element mhalo_max ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 377
        
        """
        return _pyhmcode.f90wrap_halomod__get__mhalo_max(self._handle)
    
    @mhalo_max.setter
    def mhalo_max(self, mhalo_max):
        _pyhmcode.f90wrap_halomod__set__mhalo_max(self._handle, mhalo_max)
    
    @property
    def n_c(self):
        """
        Element n_c ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 378
        
        """
        return _pyhmcode.f90wrap_halomod__get__n_c(self._handle)
    
    @n_c.setter
    def n_c(self, n_c):
        _pyhmcode.f90wrap_halomod__set__n_c(self._handle, n_c)
    
    @property
    def n_s(self):
        """
        Element n_s ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 378
        
        """
        return _pyhmcode.f90wrap_halomod__get__n_s(self._handle)
    
    @n_s.setter
    def n_s(self, n_s):
        _pyhmcode.f90wrap_halomod__set__n_s(self._handle, n_s)
    
    @property
    def n_g(self):
        """
        Element n_g ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 378
        
        """
        return _pyhmcode.f90wrap_halomod__get__n_g(self._handle)
    
    @n_g.setter
    def n_g(self, n_g):
        _pyhmcode.f90wrap_halomod__set__n_g(self._handle, n_g)
    
    @property
    def n_h(self):
        """
        Element n_h ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 378
        
        """
        return _pyhmcode.f90wrap_halomod__get__n_h(self._handle)
    
    @n_h.setter
    def n_h(self, n_h):
        _pyhmcode.f90wrap_halomod__set__n_h(self._handle, n_h)
    
    @property
    def shot_gg(self):
        """
        Element shot_gg ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 378
        
        """
        return _pyhmcode.f90wrap_halomod__get__shot_gg(self._handle)
    
    @shot_gg.setter
    def shot_gg(self, shot_gg):
        _pyhmcode.f90wrap_halomod__set__shot_gg(self._handle, shot_gg)
    
    @property
    def shot_hh(self):
        """
        Element shot_hh ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 378
        
        """
        return _pyhmcode.f90wrap_halomod__get__shot_hh(self._handle)
    
    @shot_hh.setter
    def shot_hh(self, shot_hh):
        _pyhmcode.f90wrap_halomod__set__shot_hh(self._handle, shot_hh)
    
    @property
    def ihod(self):
        """
        Element ihod ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 379
        
        """
        return _pyhmcode.f90wrap_halomod__get__ihod(self._handle)
    
    @ihod.setter
    def ihod(self, ihod):
        _pyhmcode.f90wrap_halomod__set__ihod(self._handle, ihod)
    
    @property
    def rho_hi(self):
        """
        Element rho_hi ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 382
        
        """
        return _pyhmcode.f90wrap_halomod__get__rho_hi(self._handle)
    
    @rho_hi.setter
    def rho_hi(self, rho_hi):
        _pyhmcode.f90wrap_halomod__set__rho_hi(self._handle, rho_hi)
    
    @property
    def himin(self):
        """
        Element himin ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 382
        
        """
        return _pyhmcode.f90wrap_halomod__get__himin(self._handle)
    
    @himin.setter
    def himin(self, himin):
        _pyhmcode.f90wrap_halomod__set__himin(self._handle, himin)
    
    @property
    def himax(self):
        """
        Element himax ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 382
        
        """
        return _pyhmcode.f90wrap_halomod__get__himax(self._handle)
    
    @himax.setter
    def himax(self, himax):
        _pyhmcode.f90wrap_halomod__set__himax(self._handle, himax)
    
    @property
    def sigma_conc(self):
        """
        Element sigma_conc ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 384
        
        """
        return _pyhmcode.f90wrap_halomod__get__sigma_conc(self._handle)
    
    @sigma_conc.setter
    def sigma_conc(self, sigma_conc):
        _pyhmcode.f90wrap_halomod__set__sigma_conc(self._handle, sigma_conc)
    
    @property
    def conc_scatter(self):
        """
        Element conc_scatter ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 385
        
        """
        return _pyhmcode.f90wrap_halomod__get__conc_scatter(self._handle)
    
    @conc_scatter.setter
    def conc_scatter(self, conc_scatter):
        _pyhmcode.f90wrap_halomod__set__conc_scatter(self._handle, conc_scatter)
    
    @property
    def rcore(self):
        """
        Element rcore ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 387
        
        """
        return _pyhmcode.f90wrap_halomod__get__rcore(self._handle)
    
    @rcore.setter
    def rcore(self, rcore):
        _pyhmcode.f90wrap_halomod__set__rcore(self._handle, rcore)
    
    @property
    def hmass(self):
        """
        Element hmass ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 387
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmass(self._handle)
    
    @hmass.setter
    def hmass(self, hmass):
        _pyhmcode.f90wrap_halomod__set__hmass(self._handle, hmass)
    
    @property
    def gmin(self):
        """
        Element gmin ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 389
        
        """
        return _pyhmcode.f90wrap_halomod__get__gmin(self._handle)
    
    @gmin.setter
    def gmin(self, gmin):
        _pyhmcode.f90wrap_halomod__set__gmin(self._handle, gmin)
    
    @property
    def gmax(self):
        """
        Element gmax ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 389
        
        """
        return _pyhmcode.f90wrap_halomod__get__gmax(self._handle)
    
    @gmax.setter
    def gmax(self, gmax):
        _pyhmcode.f90wrap_halomod__set__gmax(self._handle, gmax)
    
    @property
    def gbmin(self):
        """
        Element gbmin ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 389
        
        """
        return _pyhmcode.f90wrap_halomod__get__gbmin(self._handle)
    
    @gbmin.setter
    def gbmin(self, gbmin):
        _pyhmcode.f90wrap_halomod__set__gbmin(self._handle, gbmin)
    
    @property
    def gbmax(self):
        """
        Element gbmax ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 389
        
        """
        return _pyhmcode.f90wrap_halomod__get__gbmax(self._handle)
    
    @gbmax.setter
    def gbmax(self, gbmax):
        _pyhmcode.f90wrap_halomod__set__gbmax(self._handle, gbmax)
    
    @property
    def gnorm(self):
        """
        Element gnorm ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 389
        
        """
        return _pyhmcode.f90wrap_halomod__get__gnorm(self._handle)
    
    @gnorm.setter
    def gnorm(self, gnorm):
        _pyhmcode.f90wrap_halomod__set__gnorm(self._handle, gnorm)
    
    @property
    def dv0(self):
        """
        Element dv0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__dv0(self._handle)
    
    @dv0.setter
    def dv0(self, dv0):
        _pyhmcode.f90wrap_halomod__set__dv0(self._handle, dv0)
    
    @property
    def dv1(self):
        """
        Element dv1 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__dv1(self._handle)
    
    @dv1.setter
    def dv1(self, dv1):
        _pyhmcode.f90wrap_halomod__set__dv1(self._handle, dv1)
    
    @property
    def dc0(self):
        """
        Element dc0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__dc0(self._handle)
    
    @dc0.setter
    def dc0(self, dc0):
        _pyhmcode.f90wrap_halomod__set__dc0(self._handle, dc0)
    
    @property
    def dc1(self):
        """
        Element dc1 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__dc1(self._handle)
    
    @dc1.setter
    def dc1(self, dc1):
        _pyhmcode.f90wrap_halomod__set__dc1(self._handle, dc1)
    
    @property
    def eta0(self):
        """
        Element eta0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__eta0(self._handle)
    
    @eta0.setter
    def eta0(self, eta0):
        _pyhmcode.f90wrap_halomod__set__eta0(self._handle, eta0)
    
    @property
    def eta1(self):
        """
        Element eta1 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__eta1(self._handle)
    
    @eta1.setter
    def eta1(self, eta1):
        _pyhmcode.f90wrap_halomod__set__eta1(self._handle, eta1)
    
    @property
    def f0(self):
        """
        Element f0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__f0(self._handle)
    
    @f0.setter
    def f0(self, f0):
        _pyhmcode.f90wrap_halomod__set__f0(self._handle, f0)
    
    @property
    def f1(self):
        """
        Element f1 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__f1(self._handle)
    
    @f1.setter
    def f1(self, f1):
        _pyhmcode.f90wrap_halomod__set__f1(self._handle, f1)
    
    @property
    def ks(self):
        """
        Element ks ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__ks(self._handle)
    
    @ks.setter
    def ks(self, ks):
        _pyhmcode.f90wrap_halomod__set__ks(self._handle, ks)
    
    @property
    def as_(self):
        """
        Element as_ ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__as_(self._handle)
    
    @as_.setter
    def as_(self, as_):
        _pyhmcode.f90wrap_halomod__set__as_(self._handle, as_)
    
    @property
    def alp0(self):
        """
        Element alp0 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__alp0(self._handle)
    
    @alp0.setter
    def alp0(self, alp0):
        _pyhmcode.f90wrap_halomod__set__alp0(self._handle, alp0)
    
    @property
    def alp1(self):
        """
        Element alp1 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__alp1(self._handle)
    
    @alp1.setter
    def alp1(self, alp1):
        _pyhmcode.f90wrap_halomod__set__alp1(self._handle, alp1)
    
    @property
    def dvnu(self):
        """
        Element dvnu ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__dvnu(self._handle)
    
    @dvnu.setter
    def dvnu(self, dvnu):
        _pyhmcode.f90wrap_halomod__set__dvnu(self._handle, dvnu)
    
    @property
    def dcnu(self):
        """
        Element dcnu ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 391
        
        """
        return _pyhmcode.f90wrap_halomod__get__dcnu(self._handle)
    
    @dcnu.setter
    def dcnu(self, dcnu):
        _pyhmcode.f90wrap_halomod__set__dcnu(self._handle, dcnu)
    
    @property
    def hmcode_kstar(self):
        """
        Element hmcode_kstar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 392
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmcode_kstar(self._handle)
    
    @hmcode_kstar.setter
    def hmcode_kstar(self, hmcode_kstar):
        _pyhmcode.f90wrap_halomod__set__hmcode_kstar(self._handle, hmcode_kstar)
    
    @property
    def hmcode_fdamp(self):
        """
        Element hmcode_fdamp ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 392
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmcode_fdamp(self._handle)
    
    @hmcode_fdamp.setter
    def hmcode_fdamp(self, hmcode_fdamp):
        _pyhmcode.f90wrap_halomod__set__hmcode_fdamp(self._handle, hmcode_fdamp)
    
    @property
    def hmcode_kdamp(self):
        """
        Element hmcode_kdamp ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 392
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmcode_kdamp(self._handle)
    
    @hmcode_kdamp.setter
    def hmcode_kdamp(self, hmcode_kdamp):
        _pyhmcode.f90wrap_halomod__set__hmcode_kdamp(self._handle, hmcode_kdamp)
    
    @property
    def hmcode_alpha(self):
        """
        Element hmcode_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 392
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmcode_alpha(self._handle)
    
    @hmcode_alpha.setter
    def hmcode_alpha(self, hmcode_alpha):
        _pyhmcode.f90wrap_halomod__set__hmcode_alpha(self._handle, hmcode_alpha)
    
    @property
    def hmcode_eta(self):
        """
        Element hmcode_eta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 392
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmcode_eta(self._handle)
    
    @hmcode_eta.setter
    def hmcode_eta(self, hmcode_eta):
        _pyhmcode.f90wrap_halomod__set__hmcode_eta(self._handle, hmcode_eta)
    
    @property
    def hmcode_a(self):
        """
        Element hmcode_a ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 392
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmcode_a(self._handle)
    
    @hmcode_a.setter
    def hmcode_a(self, hmcode_a):
        _pyhmcode.f90wrap_halomod__set__hmcode_a(self._handle, hmcode_a)
    
    @property
    def dmonly_baryon_recipe(self):
        """
        Element dmonly_baryon_recipe ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 393
        
        """
        return _pyhmcode.f90wrap_halomod__get__dmonly_baryon_recipe(self._handle)
    
    @dmonly_baryon_recipe.setter
    def dmonly_baryon_recipe(self, dmonly_baryon_recipe):
        _pyhmcode.f90wrap_halomod__set__dmonly_baryon_recipe(self._handle, \
            dmonly_baryon_recipe)
    
    @property
    def dmonly_neutrino_halo_mass_correction(self):
        """
        Element dmonly_neutrino_halo_mass_correction ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 393
        
        """
        return \
            _pyhmcode.f90wrap_halomod__get__dmonly_neutrino_halo_mass_correction(self._handle)
    
    @dmonly_neutrino_halo_mass_correction.setter
    def dmonly_neutrino_halo_mass_correction(self, \
        dmonly_neutrino_halo_mass_correction):
        _pyhmcode.f90wrap_halomod__set__dmonly_neutrino_halo_mass_correction(self._handle, \
            dmonly_neutrino_halo_mass_correction)
    
    @property
    def dmonly_neutrinos_affect_virial_radius(self):
        """
        Element dmonly_neutrinos_affect_virial_radius ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 394
        
        """
        return \
            _pyhmcode.f90wrap_halomod__get__dmonly_neutrinos_affect_virial_radius(self._handle)
    
    @dmonly_neutrinos_affect_virial_radius.setter
    def dmonly_neutrinos_affect_virial_radius(self, \
        dmonly_neutrinos_affect_virial_radius):
        _pyhmcode.f90wrap_halomod__set__dmonly_neutrinos_affect_virial_radius(self._handle, \
            dmonly_neutrinos_affect_virial_radius)
    
    @property
    def one_parameter_baryons(self):
        """
        Element one_parameter_baryons ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 396
        
        """
        return _pyhmcode.f90wrap_halomod__get__one_parameter_baryons(self._handle)
    
    @one_parameter_baryons.setter
    def one_parameter_baryons(self, one_parameter_baryons):
        _pyhmcode.f90wrap_halomod__set__one_parameter_baryons(self._handle, \
            one_parameter_baryons)
    
    @property
    def kd(self):
        """
        Element kd ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__kd(self._handle)
    
    @kd.setter
    def kd(self, kd):
        _pyhmcode.f90wrap_halomod__set__kd(self._handle, kd)
    
    @property
    def kdp(self):
        """
        Element kdp ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__kdp(self._handle)
    
    @kdp.setter
    def kdp(self, kdp):
        _pyhmcode.f90wrap_halomod__set__kdp(self._handle, kdp)
    
    @property
    def ap(self):
        """
        Element ap ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__ap(self._handle)
    
    @ap.setter
    def ap(self, ap):
        _pyhmcode.f90wrap_halomod__set__ap(self._handle, ap)
    
    @property
    def ac(self):
        """
        Element ac ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__ac(self._handle)
    
    @ac.setter
    def ac(self, ac):
        _pyhmcode.f90wrap_halomod__set__ac(self._handle, ac)
    
    @property
    def kp(self):
        """
        Element kp ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__kp(self._handle)
    
    @kp.setter
    def kp(self, kp):
        _pyhmcode.f90wrap_halomod__set__kp(self._handle, kp)
    
    @property
    def nd(self):
        """
        Element nd ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__nd(self._handle)
    
    @nd.setter
    def nd(self, nd):
        _pyhmcode.f90wrap_halomod__set__nd(self._handle, nd)
    
    @property
    def alp2(self):
        """
        Element alp2 ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__alp2(self._handle)
    
    @alp2.setter
    def alp2(self, alp2):
        _pyhmcode.f90wrap_halomod__set__alp2(self._handle, alp2)
    
    @property
    def fm(self):
        """
        Element fm ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__fm(self._handle)
    
    @fm.setter
    def fm(self, fm):
        _pyhmcode.f90wrap_halomod__set__fm(self._handle, fm)
    
    @property
    def fd(self):
        """
        Element fd ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__fd(self._handle)
    
    @fd.setter
    def fd(self, fd):
        _pyhmcode.f90wrap_halomod__set__fd(self._handle, fd)
    
    @property
    def zd(self):
        """
        Element zd ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__zd(self._handle)
    
    @zd.setter
    def zd(self, zd):
        _pyhmcode.f90wrap_halomod__set__zd(self._handle, zd)
    
    @property
    def az(self):
        """
        Element az ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 398
        
        """
        return _pyhmcode.f90wrap_halomod__get__az(self._handle)
    
    @az.setter
    def az(self, az):
        _pyhmcode.f90wrap_halomod__set__az(self._handle, az)
    
    @property
    def mbar(self):
        """
        Element mbar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 399
        
        """
        return _pyhmcode.f90wrap_halomod__get__mbar(self._handle)
    
    @mbar.setter
    def mbar(self, mbar):
        _pyhmcode.f90wrap_halomod__set__mbar(self._handle, mbar)
    
    @property
    def nbar(self):
        """
        Element nbar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 399
        
        """
        return _pyhmcode.f90wrap_halomod__get__nbar(self._handle)
    
    @nbar.setter
    def nbar(self, nbar):
        _pyhmcode.f90wrap_halomod__set__nbar(self._handle, nbar)
    
    @property
    def sbar(self):
        """
        Element sbar ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 399
        
        """
        return _pyhmcode.f90wrap_halomod__get__sbar(self._handle)
    
    @sbar.setter
    def sbar(self, sbar):
        _pyhmcode.f90wrap_halomod__set__sbar(self._handle, sbar)
    
    @property
    def mbarz(self):
        """
        Element mbarz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 399
        
        """
        return _pyhmcode.f90wrap_halomod__get__mbarz(self._handle)
    
    @mbarz.setter
    def mbarz(self, mbarz):
        _pyhmcode.f90wrap_halomod__set__mbarz(self._handle, mbarz)
    
    @property
    def sbarz(self):
        """
        Element sbarz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 399
        
        """
        return _pyhmcode.f90wrap_halomod__get__sbarz(self._handle)
    
    @sbarz.setter
    def sbarz(self, sbarz):
        _pyhmcode.f90wrap_halomod__set__sbarz(self._handle, sbarz)
    
    @property
    def mbar_t(self):
        """
        Element mbar_t ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 400
        
        """
        return _pyhmcode.f90wrap_halomod__get__mbar_t(self._handle)
    
    @mbar_t.setter
    def mbar_t(self, mbar_t):
        _pyhmcode.f90wrap_halomod__set__mbar_t(self._handle, mbar_t)
    
    @property
    def as_t(self):
        """
        Element as_t ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 400
        
        """
        return _pyhmcode.f90wrap_halomod__get__as_t(self._handle)
    
    @as_t.setter
    def as_t(self, as_t):
        _pyhmcode.f90wrap_halomod__set__as_t(self._handle, as_t)
    
    @property
    def sbar_t(self):
        """
        Element sbar_t ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 400
        
        """
        return _pyhmcode.f90wrap_halomod__get__sbar_t(self._handle)
    
    @sbar_t.setter
    def sbar_t(self, sbar_t):
        _pyhmcode.f90wrap_halomod__set__sbar_t(self._handle, sbar_t)
    
    @property
    def mbarz_t(self):
        """
        Element mbarz_t ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 400
        
        """
        return _pyhmcode.f90wrap_halomod__get__mbarz_t(self._handle)
    
    @mbarz_t.setter
    def mbarz_t(self, mbarz_t):
        _pyhmcode.f90wrap_halomod__set__mbarz_t(self._handle, mbarz_t)
    
    @property
    def sbarz_t(self):
        """
        Element sbarz_t ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 400
        
        """
        return _pyhmcode.f90wrap_halomod__get__sbarz_t(self._handle)
    
    @sbarz_t.setter
    def sbarz_t(self, sbarz_t):
        _pyhmcode.f90wrap_halomod__set__sbarz_t(self._handle, sbarz_t)
    
    @property
    def az_t(self):
        """
        Element az_t ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 400
        
        """
        return _pyhmcode.f90wrap_halomod__get__az_t(self._handle)
    
    @az_t.setter
    def az_t(self, az_t):
        _pyhmcode.f90wrap_halomod__set__az_t(self._handle, az_t)
    
    @property
    def halo_dmonly(self):
        """
        Element halo_dmonly ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 402
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_dmonly(self._handle)
    
    @halo_dmonly.setter
    def halo_dmonly(self, halo_dmonly):
        _pyhmcode.f90wrap_halomod__set__halo_dmonly(self._handle, halo_dmonly)
    
    @property
    def halo_cdm(self):
        """
        Element halo_cdm ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 402
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_cdm(self._handle)
    
    @halo_cdm.setter
    def halo_cdm(self, halo_cdm):
        _pyhmcode.f90wrap_halomod__set__halo_cdm(self._handle, halo_cdm)
    
    @property
    def halo_normal_bound_gas(self):
        """
        Element halo_normal_bound_gas ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 402
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_normal_bound_gas(self._handle)
    
    @halo_normal_bound_gas.setter
    def halo_normal_bound_gas(self, halo_normal_bound_gas):
        _pyhmcode.f90wrap_halomod__set__halo_normal_bound_gas(self._handle, \
            halo_normal_bound_gas)
    
    @property
    def halo_cold_bound_gas(self):
        """
        Element halo_cold_bound_gas ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 402
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_cold_bound_gas(self._handle)
    
    @halo_cold_bound_gas.setter
    def halo_cold_bound_gas(self, halo_cold_bound_gas):
        _pyhmcode.f90wrap_halomod__set__halo_cold_bound_gas(self._handle, \
            halo_cold_bound_gas)
    
    @property
    def halo_hot_bound_gas(self):
        """
        Element halo_hot_bound_gas ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 402
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_hot_bound_gas(self._handle)
    
    @halo_hot_bound_gas.setter
    def halo_hot_bound_gas(self, halo_hot_bound_gas):
        _pyhmcode.f90wrap_halomod__set__halo_hot_bound_gas(self._handle, \
            halo_hot_bound_gas)
    
    @property
    def halo_ejected_gas(self):
        """
        Element halo_ejected_gas ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 402
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_ejected_gas(self._handle)
    
    @halo_ejected_gas.setter
    def halo_ejected_gas(self, halo_ejected_gas):
        _pyhmcode.f90wrap_halomod__set__halo_ejected_gas(self._handle, halo_ejected_gas)
    
    @property
    def halo_central_stars(self):
        """
        Element halo_central_stars ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 403
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_central_stars(self._handle)
    
    @halo_central_stars.setter
    def halo_central_stars(self, halo_central_stars):
        _pyhmcode.f90wrap_halomod__set__halo_central_stars(self._handle, \
            halo_central_stars)
    
    @property
    def halo_satellite_stars(self):
        """
        Element halo_satellite_stars ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 403
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_satellite_stars(self._handle)
    
    @halo_satellite_stars.setter
    def halo_satellite_stars(self, halo_satellite_stars):
        _pyhmcode.f90wrap_halomod__set__halo_satellite_stars(self._handle, \
            halo_satellite_stars)
    
    @property
    def halo_hi(self):
        """
        Element halo_hi ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 403
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_hi(self._handle)
    
    @halo_hi.setter
    def halo_hi(self, halo_hi):
        _pyhmcode.f90wrap_halomod__set__halo_hi(self._handle, halo_hi)
    
    @property
    def halo_neutrino(self):
        """
        Element halo_neutrino ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 403
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_neutrino(self._handle)
    
    @halo_neutrino.setter
    def halo_neutrino(self, halo_neutrino):
        _pyhmcode.f90wrap_halomod__set__halo_neutrino(self._handle, halo_neutrino)
    
    @property
    def halo_satellites(self):
        """
        Element halo_satellites ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 403
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_satellites(self._handle)
    
    @halo_satellites.setter
    def halo_satellites(self, halo_satellites):
        _pyhmcode.f90wrap_halomod__set__halo_satellites(self._handle, halo_satellites)
    
    @property
    def halo_centrals(self):
        """
        Element halo_centrals ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 403
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_centrals(self._handle)
    
    @halo_centrals.setter
    def halo_centrals(self, halo_centrals):
        _pyhmcode.f90wrap_halomod__set__halo_centrals(self._handle, halo_centrals)
    
    @property
    def halo_void(self):
        """
        Element halo_void ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 404
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_void(self._handle)
    
    @halo_void.setter
    def halo_void(self, halo_void):
        _pyhmcode.f90wrap_halomod__set__halo_void(self._handle, halo_void)
    
    @property
    def halo_compensated_void(self):
        """
        Element halo_compensated_void ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 404
        
        """
        return _pyhmcode.f90wrap_halomod__get__halo_compensated_void(self._handle)
    
    @halo_compensated_void.setter
    def halo_compensated_void(self, halo_compensated_void):
        _pyhmcode.f90wrap_halomod__set__halo_compensated_void(self._handle, \
            halo_compensated_void)
    
    @property
    def electron_pressure(self):
        """
        Element electron_pressure ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 404
        
        """
        return _pyhmcode.f90wrap_halomod__get__electron_pressure(self._handle)
    
    @electron_pressure.setter
    def electron_pressure(self, electron_pressure):
        _pyhmcode.f90wrap_halomod__set__electron_pressure(self._handle, \
            electron_pressure)
    
    @property
    def normalise_baryons(self):
        """
        Element normalise_baryons ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 406
        
        """
        return _pyhmcode.f90wrap_halomod__get__normalise_baryons(self._handle)
    
    @normalise_baryons.setter
    def normalise_baryons(self, normalise_baryons):
        _pyhmcode.f90wrap_halomod__set__normalise_baryons(self._handle, \
            normalise_baryons)
    
    @property
    def frac_central_stars(self):
        """
        Element frac_central_stars ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 407
        
        """
        return _pyhmcode.f90wrap_halomod__get__frac_central_stars(self._handle)
    
    @frac_central_stars.setter
    def frac_central_stars(self, frac_central_stars):
        _pyhmcode.f90wrap_halomod__set__frac_central_stars(self._handle, \
            frac_central_stars)
    
    @property
    def frac_stars(self):
        """
        Element frac_stars ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 407
        
        """
        return _pyhmcode.f90wrap_halomod__get__frac_stars(self._handle)
    
    @frac_stars.setter
    def frac_stars(self, frac_stars):
        _pyhmcode.f90wrap_halomod__set__frac_stars(self._handle, frac_stars)
    
    @property
    def frac_hi(self):
        """
        Element frac_hi ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 407
        
        """
        return _pyhmcode.f90wrap_halomod__get__frac_hi(self._handle)
    
    @frac_hi.setter
    def frac_hi(self, frac_hi):
        _pyhmcode.f90wrap_halomod__set__frac_hi(self._handle, frac_hi)
    
    @property
    def frac_bound_gas(self):
        """
        Element frac_bound_gas ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 408
        
        """
        return _pyhmcode.f90wrap_halomod__get__frac_bound_gas(self._handle)
    
    @frac_bound_gas.setter
    def frac_bound_gas(self, frac_bound_gas):
        _pyhmcode.f90wrap_halomod__set__frac_bound_gas(self._handle, frac_bound_gas)
    
    @property
    def frac_cold_bound_gas(self):
        """
        Element frac_cold_bound_gas ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 408
        
        """
        return _pyhmcode.f90wrap_halomod__get__frac_cold_bound_gas(self._handle)
    
    @frac_cold_bound_gas.setter
    def frac_cold_bound_gas(self, frac_cold_bound_gas):
        _pyhmcode.f90wrap_halomod__set__frac_cold_bound_gas(self._handle, \
            frac_cold_bound_gas)
    
    @property
    def frac_hot_bound_gas(self):
        """
        Element frac_hot_bound_gas ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 408
        
        """
        return _pyhmcode.f90wrap_halomod__get__frac_hot_bound_gas(self._handle)
    
    @frac_hot_bound_gas.setter
    def frac_hot_bound_gas(self, frac_hot_bound_gas):
        _pyhmcode.f90wrap_halomod__set__frac_hot_bound_gas(self._handle, \
            frac_hot_bound_gas)
    
    @property
    def has_hi(self):
        """
        Element has_hi ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 410
        
        """
        return _pyhmcode.f90wrap_halomod__get__has_hi(self._handle)
    
    @has_hi.setter
    def has_hi(self, has_hi):
        _pyhmcode.f90wrap_halomod__set__has_hi(self._handle, has_hi)
    
    @property
    def has_mass_conversions(self):
        """
        Element has_mass_conversions ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 410
        
        """
        return _pyhmcode.f90wrap_halomod__get__has_mass_conversions(self._handle)
    
    @has_mass_conversions.setter
    def has_mass_conversions(self, has_mass_conversions):
        _pyhmcode.f90wrap_halomod__set__has_mass_conversions(self._handle, \
            has_mass_conversions)
    
    @property
    def has_hod(self):
        """
        Element has_hod ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 410
        
        """
        return _pyhmcode.f90wrap_halomod__get__has_hod(self._handle)
    
    @has_hod.setter
    def has_hod(self, has_hod):
        _pyhmcode.f90wrap_halomod__set__has_hod(self._handle, has_hod)
    
    @property
    def has_haloes(self):
        """
        Element has_haloes ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 410
        
        """
        return _pyhmcode.f90wrap_halomod__get__has_haloes(self._handle)
    
    @has_haloes.setter
    def has_haloes(self, has_haloes):
        _pyhmcode.f90wrap_halomod__set__has_haloes(self._handle, has_haloes)
    
    @property
    def simple_pivot(self):
        """
        Element simple_pivot ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 412
        
        """
        return _pyhmcode.f90wrap_halomod__get__simple_pivot(self._handle)
    
    @simple_pivot.setter
    def simple_pivot(self, simple_pivot):
        _pyhmcode.f90wrap_halomod__set__simple_pivot(self._handle, simple_pivot)
    
    @property
    def safe_negative(self):
        """
        Element safe_negative ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 413
        
        """
        return _pyhmcode.f90wrap_halomod__get__safe_negative(self._handle)
    
    @safe_negative.setter
    def safe_negative(self, safe_negative):
        _pyhmcode.f90wrap_halomod__set__safe_negative(self._handle, safe_negative)
    
    @property
    def response_baseline(self):
        """
        Element response_baseline ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 414
        
        """
        return _pyhmcode.f90wrap_halomod__get__response_baseline(self._handle)
    
    @response_baseline.setter
    def response_baseline(self, response_baseline):
        _pyhmcode.f90wrap_halomod__set__response_baseline(self._handle, \
            response_baseline)
    
    @property
    def response_denominator(self):
        """
        Element response_denominator ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 414
        
        """
        return _pyhmcode.f90wrap_halomod__get__response_denominator(self._handle)
    
    @response_denominator.setter
    def response_denominator(self, response_denominator):
        _pyhmcode.f90wrap_halomod__set__response_denominator(self._handle, \
            response_denominator)
    
    @property
    def response_matter_only(self):
        """
        Element response_matter_only ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 415
        
        """
        return _pyhmcode.f90wrap_halomod__get__response_matter_only(self._handle)
    
    @response_matter_only.setter
    def response_matter_only(self, response_matter_only):
        _pyhmcode.f90wrap_halomod__set__response_matter_only(self._handle, \
            response_matter_only)
    
    @property
    def acc(self):
        """
        Element acc ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 416
        
        """
        return _pyhmcode.f90wrap_halomod__get__acc(self._handle)
    
    @acc.setter
    def acc(self, acc):
        _pyhmcode.f90wrap_halomod__set__acc(self._handle, acc)
    
    @property
    def name(self):
        """
        Element name ftype=character(len=256) pytype=str
        
        
        Defined at ../library/src/hmx.f90 line 417
        
        """
        return _pyhmcode.f90wrap_halomod__get__name(self._handle)
    
    @name.setter
    def name(self, name):
        _pyhmcode.f90wrap_halomod__set__name(self._handle, name)
    
    @property
    def hmx_mode(self):
        """
        Element hmx_mode ftype=integer  pytype=int
        
        
        Defined at ../library/src/hmx.f90 line 418
        
        """
        return _pyhmcode.f90wrap_halomod__get__hmx_mode(self._handle)
    
    @hmx_mode.setter
    def hmx_mode(self, hmx_mode):
        _pyhmcode.f90wrap_halomod__set__hmx_mode(self._handle, hmx_mode)
    
    @property
    def tinker_biga(self):
        """
        Element tinker_biga ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 420
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_biga(self._handle)
    
    @tinker_biga.setter
    def tinker_biga(self, tinker_biga):
        _pyhmcode.f90wrap_halomod__set__tinker_biga(self._handle, tinker_biga)
    
    @property
    def tinker_bigb(self):
        """
        Element tinker_bigb ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 420
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_bigb(self._handle)
    
    @tinker_bigb.setter
    def tinker_bigb(self, tinker_bigb):
        _pyhmcode.f90wrap_halomod__set__tinker_bigb(self._handle, tinker_bigb)
    
    @property
    def tinker_bigc(self):
        """
        Element tinker_bigc ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 420
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_bigc(self._handle)
    
    @tinker_bigc.setter
    def tinker_bigc(self, tinker_bigc):
        _pyhmcode.f90wrap_halomod__set__tinker_bigc(self._handle, tinker_bigc)
    
    @property
    def tinker_a(self):
        """
        Element tinker_a ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 420
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_a(self._handle)
    
    @tinker_a.setter
    def tinker_a(self, tinker_a):
        _pyhmcode.f90wrap_halomod__set__tinker_a(self._handle, tinker_a)
    
    @property
    def tinker_b(self):
        """
        Element tinker_b ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 420
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_b(self._handle)
    
    @tinker_b.setter
    def tinker_b(self, tinker_b):
        _pyhmcode.f90wrap_halomod__set__tinker_b(self._handle, tinker_b)
    
    @property
    def tinker_c(self):
        """
        Element tinker_c ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 420
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_c(self._handle)
    
    @tinker_c.setter
    def tinker_c(self, tinker_c):
        _pyhmcode.f90wrap_halomod__set__tinker_c(self._handle, tinker_c)
    
    @property
    def tinker_alpha(self):
        """
        Element tinker_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 421
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_alpha(self._handle)
    
    @tinker_alpha.setter
    def tinker_alpha(self, tinker_alpha):
        _pyhmcode.f90wrap_halomod__set__tinker_alpha(self._handle, tinker_alpha)
    
    @property
    def tinker_beta(self):
        """
        Element tinker_beta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 421
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_beta(self._handle)
    
    @tinker_beta.setter
    def tinker_beta(self, tinker_beta):
        _pyhmcode.f90wrap_halomod__set__tinker_beta(self._handle, tinker_beta)
    
    @property
    def tinker_gamma(self):
        """
        Element tinker_gamma ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 421
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_gamma(self._handle)
    
    @tinker_gamma.setter
    def tinker_gamma(self, tinker_gamma):
        _pyhmcode.f90wrap_halomod__set__tinker_gamma(self._handle, tinker_gamma)
    
    @property
    def tinker_phi(self):
        """
        Element tinker_phi ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 421
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_phi(self._handle)
    
    @tinker_phi.setter
    def tinker_phi(self, tinker_phi):
        _pyhmcode.f90wrap_halomod__set__tinker_phi(self._handle, tinker_phi)
    
    @property
    def tinker_eta(self):
        """
        Element tinker_eta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 421
        
        """
        return _pyhmcode.f90wrap_halomod__get__tinker_eta(self._handle)
    
    @tinker_eta.setter
    def tinker_eta(self, tinker_eta):
        _pyhmcode.f90wrap_halomod__set__tinker_eta(self._handle, tinker_eta)
    
    @property
    def alpha_numu(self):
        """
        Element alpha_numu ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 422
        
        """
        return _pyhmcode.f90wrap_halomod__get__alpha_numu(self._handle)
    
    @alpha_numu.setter
    def alpha_numu(self, alpha_numu):
        _pyhmcode.f90wrap_halomod__set__alpha_numu(self._handle, alpha_numu)
    
    @property
    def st_p(self):
        """
        Element st_p ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 423
        
        """
        return _pyhmcode.f90wrap_halomod__get__st_p(self._handle)
    
    @st_p.setter
    def st_p(self, st_p):
        _pyhmcode.f90wrap_halomod__set__st_p(self._handle, st_p)
    
    @property
    def st_q(self):
        """
        Element st_q ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 423
        
        """
        return _pyhmcode.f90wrap_halomod__get__st_q(self._handle)
    
    @st_q.setter
    def st_q(self, st_q):
        _pyhmcode.f90wrap_halomod__set__st_q(self._handle, st_q)
    
    @property
    def st_a(self):
        """
        Element st_a ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 423
        
        """
        return _pyhmcode.f90wrap_halomod__get__st_a(self._handle)
    
    @st_a.setter
    def st_a(self, st_a):
        _pyhmcode.f90wrap_halomod__set__st_a(self._handle, st_a)
    
    @property
    def amf(self):
        """
        Element amf ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 423
        
        """
        return _pyhmcode.f90wrap_halomod__get__amf(self._handle)
    
    @amf.setter
    def amf(self, amf):
        _pyhmcode.f90wrap_halomod__set__amf(self._handle, amf)
    
    @property
    def amfz(self):
        """
        Element amfz ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 423
        
        """
        return _pyhmcode.f90wrap_halomod__get__amfz(self._handle)
    
    @amfz.setter
    def amfz(self, amfz):
        _pyhmcode.f90wrap_halomod__set__amfz(self._handle, amfz)
    
    @property
    def has_mass_function(self):
        """
        Element has_mass_function ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 424
        
        """
        return _pyhmcode.f90wrap_halomod__get__has_mass_function(self._handle)
    
    @has_mass_function.setter
    def has_mass_function(self, has_mass_function):
        _pyhmcode.f90wrap_halomod__set__has_mass_function(self._handle, \
            has_mass_function)
    
    @property
    def has_bnl(self):
        """
        Element has_bnl ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 428
        
        """
        return _pyhmcode.f90wrap_halomod__get__has_bnl(self._handle)
    
    @has_bnl.setter
    def has_bnl(self, has_bnl):
        _pyhmcode.f90wrap_halomod__set__has_bnl(self._handle, has_bnl)
    
    @property
    def stitch_bnl_nu(self):
        """
        Element stitch_bnl_nu ftype=logical pytype=bool
        
        
        Defined at ../library/src/hmx.f90 line 428
        
        """
        return _pyhmcode.f90wrap_halomod__get__stitch_bnl_nu(self._handle)
    
    @stitch_bnl_nu.setter
    def stitch_bnl_nu(self, stitch_bnl_nu):
        _pyhmcode.f90wrap_halomod__set__stitch_bnl_nu(self._handle, stitch_bnl_nu)
    
    @property
    def bnl_path(self):
        """
        Element bnl_path ftype=character(len=256) pytype=str
        
        
        Defined at ../library/src/hmx.f90 line 429
        
        """
        return _pyhmcode.f90wrap_halomod__get__bnl_path(self._handle)
    
    @bnl_path.setter
    def bnl_path(self, bnl_path):
        _pyhmcode.f90wrap_halomod__set__bnl_path(self._handle, bnl_path)
    
    @property
    def bnl_dir(self):
        """
        Element bnl_dir ftype=character(len=256) pytype=str
        
        
        Defined at ../library/src/hmx.f90 line 429
        
        """
        return _pyhmcode.f90wrap_halomod__get__bnl_dir(self._handle)
    
    @bnl_dir.setter
    def bnl_dir(self, bnl_dir):
        _pyhmcode.f90wrap_halomod__set__bnl_dir(self._handle, bnl_dir)
    
    @property
    def bnl_cat(self):
        """
        Element bnl_cat ftype=character(len=256) pytype=str
        
        
        Defined at ../library/src/hmx.f90 line 429
        
        """
        return _pyhmcode.f90wrap_halomod__get__bnl_cat(self._handle)
    
    @bnl_cat.setter
    def bnl_cat(self, bnl_cat):
        _pyhmcode.f90wrap_halomod__set__bnl_cat(self._handle, bnl_cat)
    
    @property
    def pt_alpha(self):
        """
        Element pt_alpha ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 431
        
        """
        return _pyhmcode.f90wrap_halomod__get__pt_alpha(self._handle)
    
    @pt_alpha.setter
    def pt_alpha(self, pt_alpha):
        _pyhmcode.f90wrap_halomod__set__pt_alpha(self._handle, pt_alpha)
    
    @property
    def pt_beta(self):
        """
        Element pt_beta ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 431
        
        """
        return _pyhmcode.f90wrap_halomod__get__pt_beta(self._handle)
    
    @pt_beta.setter
    def pt_beta(self, pt_beta):
        _pyhmcode.f90wrap_halomod__set__pt_beta(self._handle, pt_beta)
    
    @property
    def pt_a(self):
        """
        Element pt_a ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 431
        
        """
        return _pyhmcode.f90wrap_halomod__get__pt_a(self._handle)
    
    @pt_a.setter
    def pt_a(self, pt_a):
        _pyhmcode.f90wrap_halomod__set__pt_a(self._handle, pt_a)
    
    @property
    def halofit_knl(self):
        """
        Element halofit_knl ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 433
        
        """
        return _pyhmcode.f90wrap_halomod__get__halofit_knl(self._handle)
    
    @halofit_knl.setter
    def halofit_knl(self, halofit_knl):
        _pyhmcode.f90wrap_halomod__set__halofit_knl(self._handle, halofit_knl)
    
    @property
    def halofit_neff(self):
        """
        Element halofit_neff ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 433
        
        """
        return _pyhmcode.f90wrap_halomod__get__halofit_neff(self._handle)
    
    @halofit_neff.setter
    def halofit_neff(self, halofit_neff):
        _pyhmcode.f90wrap_halomod__set__halofit_neff(self._handle, halofit_neff)
    
    @property
    def halofit_ncur(self):
        """
        Element halofit_ncur ftype=real  pytype=float
        
        
        Defined at ../library/src/hmx.f90 line 433
        
        """
        return _pyhmcode.f90wrap_halomod__get__halofit_ncur(self._handle)
    
    @halofit_ncur.setter
    def halofit_ncur(self, halofit_ncur):
        _pyhmcode.f90wrap_halomod__set__halofit_ncur(self._handle, halofit_ncur)
    
    def __str__(self):
        ret = ['<halomod>{\n']
        ret.append('    ihm : ')
        ret.append(repr(self.ihm))
        ret.append(',\n    z : ')
        ret.append(repr(self.z))
        ret.append(',\n    a : ')
        ret.append(repr(self.a))
        ret.append(',\n    ip2h : ')
        ret.append(repr(self.ip2h))
        ret.append(',\n    ip1h : ')
        ret.append(repr(self.ip1h))
        ret.append(',\n    ibias : ')
        ret.append(repr(self.ibias))
        ret.append(',\n    imf : ')
        ret.append(repr(self.imf))
        ret.append(',\n    iconc : ')
        ret.append(repr(self.iconc))
        ret.append(',\n    idolag : ')
        ret.append(repr(self.idolag))
        ret.append(',\n    ias : ')
        ret.append(repr(self.ias))
        ret.append(',\n    i2hcor : ')
        ret.append(repr(self.i2hcor))
        ret.append(',\n    idc : ')
        ret.append(repr(self.idc))
        ret.append(',\n    idv : ')
        ret.append(repr(self.idv))
        ret.append(',\n    ieta : ')
        ret.append(repr(self.ieta))
        ret.append(',\n    i2hdamp : ')
        ret.append(repr(self.i2hdamp))
        ret.append(',\n    i1hdamp : ')
        ret.append(repr(self.i1hdamp))
        ret.append(',\n    itrans : ')
        ret.append(repr(self.itrans))
        ret.append(',\n    ikdamp : ')
        ret.append(repr(self.ikdamp))
        ret.append(',\n    flag_sigma : ')
        ret.append(repr(self.flag_sigma))
        ret.append(',\n    add_voids : ')
        ret.append(repr(self.add_voids))
        ret.append(',\n    add_variances : ')
        ret.append(repr(self.add_variances))
        ret.append(',\n    add_shotnoise : ')
        ret.append(repr(self.add_shotnoise))
        ret.append(',\n    proper_discrete : ')
        ret.append(repr(self.proper_discrete))
        ret.append(',\n    consistency : ')
        ret.append(repr(self.consistency))
        ret.append(',\n    dc : ')
        ret.append(repr(self.dc))
        ret.append(',\n    dv : ')
        ret.append(repr(self.dv))
        ret.append(',\n    mass_dependent_dv : ')
        ret.append(repr(self.mass_dependent_dv))
        ret.append(',\n    fix_star_concentration : ')
        ret.append(repr(self.fix_star_concentration))
        ret.append(',\n    different_gammas : ')
        ret.append(repr(self.different_gammas))
        ret.append(',\n    theat_array : ')
        ret.append(repr(self.theat_array))
        ret.append(',\n    pivot_mass : ')
        ret.append(repr(self.pivot_mass))
        ret.append(',\n    alpha : ')
        ret.append(repr(self.alpha))
        ret.append(',\n    alphap : ')
        ret.append(repr(self.alphap))
        ret.append(',\n    alphaz : ')
        ret.append(repr(self.alphaz))
        ret.append(',\n    alpha_array : ')
        ret.append(repr(self.alpha_array))
        ret.append(',\n    alphap_array : ')
        ret.append(repr(self.alphap_array))
        ret.append(',\n    alphaz_array : ')
        ret.append(repr(self.alphaz_array))
        ret.append(',\n    beta : ')
        ret.append(repr(self.beta))
        ret.append(',\n    betap : ')
        ret.append(repr(self.betap))
        ret.append(',\n    betaz : ')
        ret.append(repr(self.betaz))
        ret.append(',\n    eps : ')
        ret.append(repr(self.eps))
        ret.append(',\n    epsz : ')
        ret.append(repr(self.epsz))
        ret.append(',\n    eps_array : ')
        ret.append(repr(self.eps_array))
        ret.append(',\n    epsz_array : ')
        ret.append(repr(self.epsz_array))
        ret.append(',\n    eps2 : ')
        ret.append(repr(self.eps2))
        ret.append(',\n    eps2z : ')
        ret.append(repr(self.eps2z))
        ret.append(',\n    eps2_array : ')
        ret.append(repr(self.eps2_array))
        ret.append(',\n    eps2z_array : ')
        ret.append(repr(self.eps2z_array))
        ret.append(',\n    gamma : ')
        ret.append(repr(self.gamma))
        ret.append(',\n    gammap : ')
        ret.append(repr(self.gammap))
        ret.append(',\n    gammaz : ')
        ret.append(repr(self.gammaz))
        ret.append(',\n    gamma_array : ')
        ret.append(repr(self.gamma_array))
        ret.append(',\n    gammap_array : ')
        ret.append(repr(self.gammap_array))
        ret.append(',\n    gammaz_array : ')
        ret.append(repr(self.gammaz_array))
        ret.append(',\n    zamma : ')
        ret.append(repr(self.zamma))
        ret.append(',\n    zammap : ')
        ret.append(repr(self.zammap))
        ret.append(',\n    zammaz : ')
        ret.append(repr(self.zammaz))
        ret.append(',\n    zamma_array : ')
        ret.append(repr(self.zamma_array))
        ret.append(',\n    zammap_array : ')
        ret.append(repr(self.zammap_array))
        ret.append(',\n    zammaz_array : ')
        ret.append(repr(self.zammaz_array))
        ret.append(',\n    m0 : ')
        ret.append(repr(self.m0))
        ret.append(',\n    m0z : ')
        ret.append(repr(self.m0z))
        ret.append(',\n    m0_array : ')
        ret.append(repr(self.m0_array))
        ret.append(',\n    m0z_array : ')
        ret.append(repr(self.m0z_array))
        ret.append(',\n    astar : ')
        ret.append(repr(self.astar))
        ret.append(',\n    astarz : ')
        ret.append(repr(self.astarz))
        ret.append(',\n    astar_array : ')
        ret.append(repr(self.astar_array))
        ret.append(',\n    astarz_array : ')
        ret.append(repr(self.astarz_array))
        ret.append(',\n    twhim : ')
        ret.append(repr(self.twhim))
        ret.append(',\n    twhimz : ')
        ret.append(repr(self.twhimz))
        ret.append(',\n    twhim_array : ')
        ret.append(repr(self.twhim_array))
        ret.append(',\n    twhimz_array : ')
        ret.append(repr(self.twhimz_array))
        ret.append(',\n    cstar : ')
        ret.append(repr(self.cstar))
        ret.append(',\n    cstarp : ')
        ret.append(repr(self.cstarp))
        ret.append(',\n    cstarz : ')
        ret.append(repr(self.cstarz))
        ret.append(',\n    cstar_array : ')
        ret.append(repr(self.cstar_array))
        ret.append(',\n    cstarp_array : ')
        ret.append(repr(self.cstarp_array))
        ret.append(',\n    cstarz_array : ')
        ret.append(repr(self.cstarz_array))
        ret.append(',\n    sstar : ')
        ret.append(repr(self.sstar))
        ret.append(',\n    mstar : ')
        ret.append(repr(self.mstar))
        ret.append(',\n    mstarz : ')
        ret.append(repr(self.mstarz))
        ret.append(',\n    mstar_array : ')
        ret.append(repr(self.mstar_array))
        ret.append(',\n    mstarz_array : ')
        ret.append(repr(self.mstarz_array))
        ret.append(',\n    fcold : ')
        ret.append(repr(self.fcold))
        ret.append(',\n    fhot : ')
        ret.append(repr(self.fhot))
        ret.append(',\n    eta : ')
        ret.append(repr(self.eta))
        ret.append(',\n    etaz : ')
        ret.append(repr(self.etaz))
        ret.append(',\n    eta_array : ')
        ret.append(repr(self.eta_array))
        ret.append(',\n    etaz_array : ')
        ret.append(repr(self.etaz_array))
        ret.append(',\n    ibeta : ')
        ret.append(repr(self.ibeta))
        ret.append(',\n    ibetap : ')
        ret.append(repr(self.ibetap))
        ret.append(',\n    ibetaz : ')
        ret.append(repr(self.ibetaz))
        ret.append(',\n    gbeta : ')
        ret.append(repr(self.gbeta))
        ret.append(',\n    gbetaz : ')
        ret.append(repr(self.gbetaz))
        ret.append(',\n    a_alpha : ')
        ret.append(repr(self.a_alpha))
        ret.append(',\n    b_alpha : ')
        ret.append(repr(self.b_alpha))
        ret.append(',\n    c_alpha : ')
        ret.append(repr(self.c_alpha))
        ret.append(',\n    d_alpha : ')
        ret.append(repr(self.d_alpha))
        ret.append(',\n    e_alpha : ')
        ret.append(repr(self.e_alpha))
        ret.append(',\n    a_eps : ')
        ret.append(repr(self.a_eps))
        ret.append(',\n    b_eps : ')
        ret.append(repr(self.b_eps))
        ret.append(',\n    c_eps : ')
        ret.append(repr(self.c_eps))
        ret.append(',\n    d_eps : ')
        ret.append(repr(self.d_eps))
        ret.append(',\n    a_gamma : ')
        ret.append(repr(self.a_gamma))
        ret.append(',\n    b_gamma : ')
        ret.append(repr(self.b_gamma))
        ret.append(',\n    c_gamma : ')
        ret.append(repr(self.c_gamma))
        ret.append(',\n    d_gamma : ')
        ret.append(repr(self.d_gamma))
        ret.append(',\n    e_gamma : ')
        ret.append(repr(self.e_gamma))
        ret.append(',\n    a_m0 : ')
        ret.append(repr(self.a_m0))
        ret.append(',\n    b_m0 : ')
        ret.append(repr(self.b_m0))
        ret.append(',\n    c_m0 : ')
        ret.append(repr(self.c_m0))
        ret.append(',\n    d_m0 : ')
        ret.append(repr(self.d_m0))
        ret.append(',\n    e_m0 : ')
        ret.append(repr(self.e_m0))
        ret.append(',\n    a_astar : ')
        ret.append(repr(self.a_astar))
        ret.append(',\n    b_astar : ')
        ret.append(repr(self.b_astar))
        ret.append(',\n    c_astar : ')
        ret.append(repr(self.c_astar))
        ret.append(',\n    d_astar : ')
        ret.append(repr(self.d_astar))
        ret.append(',\n    a_twhim : ')
        ret.append(repr(self.a_twhim))
        ret.append(',\n    b_twhim : ')
        ret.append(repr(self.b_twhim))
        ret.append(',\n    c_twhim : ')
        ret.append(repr(self.c_twhim))
        ret.append(',\n    d_twhim : ')
        ret.append(repr(self.d_twhim))
        ret.append(',\n    mmin : ')
        ret.append(repr(self.mmin))
        ret.append(',\n    mmax : ')
        ret.append(repr(self.mmax))
        ret.append(',\n    c : ')
        ret.append(repr(self.c))
        ret.append(',\n    rv : ')
        ret.append(repr(self.rv))
        ret.append(',\n    nu : ')
        ret.append(repr(self.nu))
        ret.append(',\n    sig : ')
        ret.append(repr(self.sig))
        ret.append(',\n    zc : ')
        ret.append(repr(self.zc))
        ret.append(',\n    m : ')
        ret.append(repr(self.m))
        ret.append(',\n    rr : ')
        ret.append(repr(self.rr))
        ret.append(',\n    sigf : ')
        ret.append(repr(self.sigf))
        ret.append(',\n    log_m : ')
        ret.append(repr(self.log_m))
        ret.append(',\n    mvir : ')
        ret.append(repr(self.mvir))
        ret.append(',\n    rvir : ')
        ret.append(repr(self.rvir))
        ret.append(',\n    cvir : ')
        ret.append(repr(self.cvir))
        ret.append(',\n    m500 : ')
        ret.append(repr(self.m500))
        ret.append(',\n    r500 : ')
        ret.append(repr(self.r500))
        ret.append(',\n    c500 : ')
        ret.append(repr(self.c500))
        ret.append(',\n    m200 : ')
        ret.append(repr(self.m200))
        ret.append(',\n    r200 : ')
        ret.append(repr(self.r200))
        ret.append(',\n    c200 : ')
        ret.append(repr(self.c200))
        ret.append(',\n    m500c : ')
        ret.append(repr(self.m500c))
        ret.append(',\n    r500c : ')
        ret.append(repr(self.r500c))
        ret.append(',\n    c500c : ')
        ret.append(repr(self.c500c))
        ret.append(',\n    m200c : ')
        ret.append(repr(self.m200c))
        ret.append(',\n    r200c : ')
        ret.append(repr(self.r200c))
        ret.append(',\n    c200c : ')
        ret.append(repr(self.c200c))
        ret.append(',\n    n : ')
        ret.append(repr(self.n))
        ret.append(',\n    k : ')
        ret.append(repr(self.k))
        ret.append(',\n    wk : ')
        ret.append(repr(self.wk))
        ret.append(',\n    nk : ')
        ret.append(repr(self.nk))
        ret.append(',\n    knl : ')
        ret.append(repr(self.knl))
        ret.append(',\n    rnl : ')
        ret.append(repr(self.rnl))
        ret.append(',\n    mnl : ')
        ret.append(repr(self.mnl))
        ret.append(',\n    rh : ')
        ret.append(repr(self.rh))
        ret.append(',\n    mh : ')
        ret.append(repr(self.mh))
        ret.append(',\n    mp : ')
        ret.append(repr(self.mp))
        ret.append(',\n    sigv : ')
        ret.append(repr(self.sigv))
        ret.append(',\n    rhh : ')
        ret.append(repr(self.rhh))
        ret.append(',\n    neff : ')
        ret.append(repr(self.neff))
        ret.append(',\n    nu_saturation : ')
        ret.append(repr(self.nu_saturation))
        ret.append(',\n    saturation : ')
        ret.append(repr(self.saturation))
        ret.append(',\n    mhalo_min : ')
        ret.append(repr(self.mhalo_min))
        ret.append(',\n    mhalo_max : ')
        ret.append(repr(self.mhalo_max))
        ret.append(',\n    n_c : ')
        ret.append(repr(self.n_c))
        ret.append(',\n    n_s : ')
        ret.append(repr(self.n_s))
        ret.append(',\n    n_g : ')
        ret.append(repr(self.n_g))
        ret.append(',\n    n_h : ')
        ret.append(repr(self.n_h))
        ret.append(',\n    shot_gg : ')
        ret.append(repr(self.shot_gg))
        ret.append(',\n    shot_hh : ')
        ret.append(repr(self.shot_hh))
        ret.append(',\n    ihod : ')
        ret.append(repr(self.ihod))
        ret.append(',\n    rho_hi : ')
        ret.append(repr(self.rho_hi))
        ret.append(',\n    himin : ')
        ret.append(repr(self.himin))
        ret.append(',\n    himax : ')
        ret.append(repr(self.himax))
        ret.append(',\n    sigma_conc : ')
        ret.append(repr(self.sigma_conc))
        ret.append(',\n    conc_scatter : ')
        ret.append(repr(self.conc_scatter))
        ret.append(',\n    rcore : ')
        ret.append(repr(self.rcore))
        ret.append(',\n    hmass : ')
        ret.append(repr(self.hmass))
        ret.append(',\n    gmin : ')
        ret.append(repr(self.gmin))
        ret.append(',\n    gmax : ')
        ret.append(repr(self.gmax))
        ret.append(',\n    gbmin : ')
        ret.append(repr(self.gbmin))
        ret.append(',\n    gbmax : ')
        ret.append(repr(self.gbmax))
        ret.append(',\n    gnorm : ')
        ret.append(repr(self.gnorm))
        ret.append(',\n    dv0 : ')
        ret.append(repr(self.dv0))
        ret.append(',\n    dv1 : ')
        ret.append(repr(self.dv1))
        ret.append(',\n    dc0 : ')
        ret.append(repr(self.dc0))
        ret.append(',\n    dc1 : ')
        ret.append(repr(self.dc1))
        ret.append(',\n    eta0 : ')
        ret.append(repr(self.eta0))
        ret.append(',\n    eta1 : ')
        ret.append(repr(self.eta1))
        ret.append(',\n    f0 : ')
        ret.append(repr(self.f0))
        ret.append(',\n    f1 : ')
        ret.append(repr(self.f1))
        ret.append(',\n    ks : ')
        ret.append(repr(self.ks))
        ret.append(',\n    as_ : ')
        ret.append(repr(self.as_))
        ret.append(',\n    alp0 : ')
        ret.append(repr(self.alp0))
        ret.append(',\n    alp1 : ')
        ret.append(repr(self.alp1))
        ret.append(',\n    dvnu : ')
        ret.append(repr(self.dvnu))
        ret.append(',\n    dcnu : ')
        ret.append(repr(self.dcnu))
        ret.append(',\n    hmcode_kstar : ')
        ret.append(repr(self.hmcode_kstar))
        ret.append(',\n    hmcode_fdamp : ')
        ret.append(repr(self.hmcode_fdamp))
        ret.append(',\n    hmcode_kdamp : ')
        ret.append(repr(self.hmcode_kdamp))
        ret.append(',\n    hmcode_alpha : ')
        ret.append(repr(self.hmcode_alpha))
        ret.append(',\n    hmcode_eta : ')
        ret.append(repr(self.hmcode_eta))
        ret.append(',\n    hmcode_a : ')
        ret.append(repr(self.hmcode_a))
        ret.append(',\n    dmonly_baryon_recipe : ')
        ret.append(repr(self.dmonly_baryon_recipe))
        ret.append(',\n    dmonly_neutrino_halo_mass_correction : ')
        ret.append(repr(self.dmonly_neutrino_halo_mass_correction))
        ret.append(',\n    dmonly_neutrinos_affect_virial_radius : ')
        ret.append(repr(self.dmonly_neutrinos_affect_virial_radius))
        ret.append(',\n    one_parameter_baryons : ')
        ret.append(repr(self.one_parameter_baryons))
        ret.append(',\n    kd : ')
        ret.append(repr(self.kd))
        ret.append(',\n    kdp : ')
        ret.append(repr(self.kdp))
        ret.append(',\n    ap : ')
        ret.append(repr(self.ap))
        ret.append(',\n    ac : ')
        ret.append(repr(self.ac))
        ret.append(',\n    kp : ')
        ret.append(repr(self.kp))
        ret.append(',\n    nd : ')
        ret.append(repr(self.nd))
        ret.append(',\n    alp2 : ')
        ret.append(repr(self.alp2))
        ret.append(',\n    fm : ')
        ret.append(repr(self.fm))
        ret.append(',\n    fd : ')
        ret.append(repr(self.fd))
        ret.append(',\n    zd : ')
        ret.append(repr(self.zd))
        ret.append(',\n    az : ')
        ret.append(repr(self.az))
        ret.append(',\n    mbar : ')
        ret.append(repr(self.mbar))
        ret.append(',\n    nbar : ')
        ret.append(repr(self.nbar))
        ret.append(',\n    sbar : ')
        ret.append(repr(self.sbar))
        ret.append(',\n    mbarz : ')
        ret.append(repr(self.mbarz))
        ret.append(',\n    sbarz : ')
        ret.append(repr(self.sbarz))
        ret.append(',\n    mbar_t : ')
        ret.append(repr(self.mbar_t))
        ret.append(',\n    as_t : ')
        ret.append(repr(self.as_t))
        ret.append(',\n    sbar_t : ')
        ret.append(repr(self.sbar_t))
        ret.append(',\n    mbarz_t : ')
        ret.append(repr(self.mbarz_t))
        ret.append(',\n    sbarz_t : ')
        ret.append(repr(self.sbarz_t))
        ret.append(',\n    az_t : ')
        ret.append(repr(self.az_t))
        ret.append(',\n    halo_dmonly : ')
        ret.append(repr(self.halo_dmonly))
        ret.append(',\n    halo_cdm : ')
        ret.append(repr(self.halo_cdm))
        ret.append(',\n    halo_normal_bound_gas : ')
        ret.append(repr(self.halo_normal_bound_gas))
        ret.append(',\n    halo_cold_bound_gas : ')
        ret.append(repr(self.halo_cold_bound_gas))
        ret.append(',\n    halo_hot_bound_gas : ')
        ret.append(repr(self.halo_hot_bound_gas))
        ret.append(',\n    halo_ejected_gas : ')
        ret.append(repr(self.halo_ejected_gas))
        ret.append(',\n    halo_central_stars : ')
        ret.append(repr(self.halo_central_stars))
        ret.append(',\n    halo_satellite_stars : ')
        ret.append(repr(self.halo_satellite_stars))
        ret.append(',\n    halo_hi : ')
        ret.append(repr(self.halo_hi))
        ret.append(',\n    halo_neutrino : ')
        ret.append(repr(self.halo_neutrino))
        ret.append(',\n    halo_satellites : ')
        ret.append(repr(self.halo_satellites))
        ret.append(',\n    halo_centrals : ')
        ret.append(repr(self.halo_centrals))
        ret.append(',\n    halo_void : ')
        ret.append(repr(self.halo_void))
        ret.append(',\n    halo_compensated_void : ')
        ret.append(repr(self.halo_compensated_void))
        ret.append(',\n    electron_pressure : ')
        ret.append(repr(self.electron_pressure))
        ret.append(',\n    normalise_baryons : ')
        ret.append(repr(self.normalise_baryons))
        ret.append(',\n    frac_central_stars : ')
        ret.append(repr(self.frac_central_stars))
        ret.append(',\n    frac_stars : ')
        ret.append(repr(self.frac_stars))
        ret.append(',\n    frac_hi : ')
        ret.append(repr(self.frac_hi))
        ret.append(',\n    frac_bound_gas : ')
        ret.append(repr(self.frac_bound_gas))
        ret.append(',\n    frac_cold_bound_gas : ')
        ret.append(repr(self.frac_cold_bound_gas))
        ret.append(',\n    frac_hot_bound_gas : ')
        ret.append(repr(self.frac_hot_bound_gas))
        ret.append(',\n    has_hi : ')
        ret.append(repr(self.has_hi))
        ret.append(',\n    has_mass_conversions : ')
        ret.append(repr(self.has_mass_conversions))
        ret.append(',\n    has_hod : ')
        ret.append(repr(self.has_hod))
        ret.append(',\n    has_haloes : ')
        ret.append(repr(self.has_haloes))
        ret.append(',\n    simple_pivot : ')
        ret.append(repr(self.simple_pivot))
        ret.append(',\n    safe_negative : ')
        ret.append(repr(self.safe_negative))
        ret.append(',\n    response_baseline : ')
        ret.append(repr(self.response_baseline))
        ret.append(',\n    response_denominator : ')
        ret.append(repr(self.response_denominator))
        ret.append(',\n    response_matter_only : ')
        ret.append(repr(self.response_matter_only))
        ret.append(',\n    acc : ')
        ret.append(repr(self.acc))
        ret.append(',\n    name : ')
        ret.append(repr(self.name))
        ret.append(',\n    hmx_mode : ')
        ret.append(repr(self.hmx_mode))
        ret.append(',\n    tinker_biga : ')
        ret.append(repr(self.tinker_biga))
        ret.append(',\n    tinker_bigb : ')
        ret.append(repr(self.tinker_bigb))
        ret.append(',\n    tinker_bigc : ')
        ret.append(repr(self.tinker_bigc))
        ret.append(',\n    tinker_a : ')
        ret.append(repr(self.tinker_a))
        ret.append(',\n    tinker_b : ')
        ret.append(repr(self.tinker_b))
        ret.append(',\n    tinker_c : ')
        ret.append(repr(self.tinker_c))
        ret.append(',\n    tinker_alpha : ')
        ret.append(repr(self.tinker_alpha))
        ret.append(',\n    tinker_beta : ')
        ret.append(repr(self.tinker_beta))
        ret.append(',\n    tinker_gamma : ')
        ret.append(repr(self.tinker_gamma))
        ret.append(',\n    tinker_phi : ')
        ret.append(repr(self.tinker_phi))
        ret.append(',\n    tinker_eta : ')
        ret.append(repr(self.tinker_eta))
        ret.append(',\n    alpha_numu : ')
        ret.append(repr(self.alpha_numu))
        ret.append(',\n    st_p : ')
        ret.append(repr(self.st_p))
        ret.append(',\n    st_q : ')
        ret.append(repr(self.st_q))
        ret.append(',\n    st_a : ')
        ret.append(repr(self.st_a))
        ret.append(',\n    amf : ')
        ret.append(repr(self.amf))
        ret.append(',\n    amfz : ')
        ret.append(repr(self.amfz))
        ret.append(',\n    has_mass_function : ')
        ret.append(repr(self.has_mass_function))
        ret.append(',\n    has_bnl : ')
        ret.append(repr(self.has_bnl))
        ret.append(',\n    stitch_bnl_nu : ')
        ret.append(repr(self.stitch_bnl_nu))
        ret.append(',\n    bnl_path : ')
        ret.append(repr(self.bnl_path))
        ret.append(',\n    bnl_dir : ')
        ret.append(repr(self.bnl_dir))
        ret.append(',\n    bnl_cat : ')
        ret.append(repr(self.bnl_cat))
        ret.append(',\n    pt_alpha : ')
        ret.append(repr(self.pt_alpha))
        ret.append(',\n    pt_beta : ')
        ret.append(repr(self.pt_beta))
        ret.append(',\n    pt_a : ')
        ret.append(repr(self.pt_a))
        ret.append(',\n    halofit_knl : ')
        ret.append(repr(self.halofit_knl))
        ret.append(',\n    halofit_neff : ')
        ret.append(repr(self.halofit_neff))
        ret.append(',\n    halofit_ncur : ')
        ret.append(repr(self.halofit_ncur))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def assign_halomod(ihm, verbose):
    """
    hmod = assign_halomod(ihm, verbose)
    
    
    Defined at ../library/src/hmx.f90 lines 746-2233
    
    Parameters
    ----------
    ihm : int
    verbose : bool
    
    Returns
    -------
    hmod : Halomod
    
    """
    hmod = _pyhmcode.f90wrap_assign_halomod(ihm=ihm, verbose=verbose)
    hmod = f90wrap.runtime.lookup_class("pyhmcode.halomod").from_handle(hmod, \
        alloc=True)
    return hmod

def init_halomod(a, hmod, cosm, verbose):
    """
    init_halomod(a, hmod, cosm, verbose)
    
    
    Defined at ../library/src/hmx.f90 lines 2235-2464
    
    Parameters
    ----------
    a : float
    hmod : Halomod
    cosm : Cosmology
    verbose : bool
    
    """
    _pyhmcode.f90wrap_init_halomod(a=a, hmod=hmod._handle, cosm=cosm._handle, \
        verbose=verbose)

def print_halomod(self, cosm, verbose):
    """
    print_halomod(self, cosm, verbose)
    
    
    Defined at ../library/src/hmx.f90 lines 2466-2929
    
    Parameters
    ----------
    hmod : Halomod
    cosm : Cosmology
    verbose : bool
    
    """
    _pyhmcode.f90wrap_print_halomod(hmod=self._handle, cosm=cosm._handle, \
        verbose=verbose)

def calculate_hmx_old(ifield, nf, k, nk, a, na, pow_li, pow_2h, pow_1h, pow_hm, \
    hmod, cosm, verbose):
    """
    calculate_hmx_old(ifield, nf, k, nk, a, na, pow_li, pow_2h, pow_1h, pow_hm, \
        hmod, cosm, verbose)
    
    
    Defined at ../library/src/hmx.f90 lines 3295-3341
    
    Parameters
    ----------
    ifield : int array
    nf : int
    k : float array
    nk : int
    a : float array
    na : int
    pow_li : float array
    pow_2h : float array
    pow_1h : float array
    pow_hm : float array
    hmod : Halomod
    cosm : Cosmology
    verbose : bool
    
    """
    _pyhmcode.f90wrap_calculate_hmx_old(ifield=ifield, nf=nf, k=k, nk=nk, a=a, \
        na=na, pow_li=pow_li, pow_2h=pow_2h, pow_1h=pow_1h, pow_hm=pow_hm, \
        hmod=hmod._handle, cosm=cosm._handle, verbose=verbose)

def init_windows(k, fields, nf, wk, nm, hmod, cosm):
    """
    init_windows(k, fields, nf, wk, nm, hmod, cosm)
    
    
    Defined at ../library/src/hmx.f90 lines 3569-3621
    
    Parameters
    ----------
    k : float
    fields : int array
    nf : int
    wk : float array
    nm : int
    hmod : Halomod
    cosm : Cosmology
    
    """
    _pyhmcode.f90wrap_init_windows(k=k, fields=fields, nf=nf, wk=wk, nm=nm, \
        hmod=hmod._handle, cosm=cosm._handle)

def add_smooth_component_to_windows(fields, nf, wk, nm, hmod, cosm):
    """
    add_smooth_component_to_windows(fields, nf, wk, nm, hmod, cosm)
    
    
    Defined at ../library/src/hmx.f90 lines 3696-3777
    
    Parameters
    ----------
    fields : int array
    nf : int
    wk : float array
    nm : int
    hmod : Halomod
    cosm : Cosmology
    
    """
    _pyhmcode.f90wrap_add_smooth_component_to_windows(fields=fields, nf=nf, wk=wk, \
        nm=nm, hmod=hmod._handle, cosm=cosm._handle)

def get_field_dmonly():
    """
    Element field_dmonly ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 538
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_dmonly()

field_dmonly = get_field_dmonly()

def get_field_matter():
    """
    Element field_matter ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 539
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_matter()

field_matter = get_field_matter()

def get_field_cdm():
    """
    Element field_cdm ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 540
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_cdm()

field_cdm = get_field_cdm()

def get_field_gas():
    """
    Element field_gas ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 541
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_gas()

field_gas = get_field_gas()

def get_field_stars():
    """
    Element field_stars ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 542
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_stars()

field_stars = get_field_stars()

def get_field_bound_gas():
    """
    Element field_bound_gas ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 543
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_bound_gas()

field_bound_gas = get_field_bound_gas()

def get_field_ejected_gas():
    """
    Element field_ejected_gas ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 544
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_ejected_gas()

field_ejected_gas = get_field_ejected_gas()

def get_field_electron_pressure():
    """
    Element field_electron_pressure ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 545
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_electron_pressure()

field_electron_pressure = get_field_electron_pressure()

def get_field_void():
    """
    Element field_void ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 546
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_void()

field_void = get_field_void()

def get_field_compensated_void():
    """
    Element field_compensated_void ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 547
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_compensated_void()

field_compensated_void = get_field_compensated_void()

def get_field_centrals():
    """
    Element field_centrals ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 548
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_centrals()

field_centrals = get_field_centrals()

def get_field_satellites():
    """
    Element field_satellites ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 549
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_satellites()

field_satellites = get_field_satellites()

def get_field_galaxies():
    """
    Element field_galaxies ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 550
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_galaxies()

field_galaxies = get_field_galaxies()

def get_field_hi():
    """
    Element field_hi ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 551
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_hi()

field_HI = get_field_hi()

def get_field_cold_bound_gas():
    """
    Element field_cold_bound_gas ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 552
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_cold_bound_gas()

field_cold_bound_gas = get_field_cold_bound_gas()

def get_field_hot_bound_gas():
    """
    Element field_hot_bound_gas ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 553
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_hot_bound_gas()

field_hot_bound_gas = get_field_hot_bound_gas()

def get_field_normal_bound_gas():
    """
    Element field_normal_bound_gas ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 554
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_normal_bound_gas()

field_normal_bound_gas = get_field_normal_bound_gas()

def get_field_central_stars():
    """
    Element field_central_stars ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 555
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_central_stars()

field_central_stars = get_field_central_stars()

def get_field_satellite_stars():
    """
    Element field_satellite_stars ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 556
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_satellite_stars()

field_satellite_stars = get_field_satellite_stars()

def get_field_cib_353():
    """
    Element field_cib_353 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 557
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_cib_353()

field_CIB_353 = get_field_cib_353()

def get_field_cib_545():
    """
    Element field_cib_545 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 558
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_cib_545()

field_CIB_545 = get_field_cib_545()

def get_field_cib_857():
    """
    Element field_cib_857 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 559
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_cib_857()

field_CIB_857 = get_field_cib_857()

def get_field_neutrino():
    """
    Element field_neutrino ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 560
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_neutrino()

field_neutrino = get_field_neutrino()

def get_field_haloes():
    """
    Element field_haloes ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 561
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_haloes()

field_haloes = get_field_haloes()

def get_field_n():
    """
    Element field_n ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 562
    
    """
    return _pyhmcode.f90wrap_hmx__get__field_n()

field_n = get_field_n()

def get_irho_delta():
    """
    Element irho_delta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 564
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_delta()

irho_delta = get_irho_delta()

def get_irho_iso():
    """
    Element irho_iso ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 565
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_iso()

irho_iso = get_irho_iso()

def get_irho_tophat():
    """
    Element irho_tophat ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 566
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_tophat()

irho_tophat = get_irho_tophat()

def get_irho_m99():
    """
    Element irho_m99 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 567
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_m99()

irho_M99 = get_irho_m99()

def get_irho_hernquest():
    """
    Element irho_hernquest ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 568
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_hernquest()

irho_Hernquest = get_irho_hernquest()

def get_irho_nfw():
    """
    Element irho_nfw ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 569
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_nfw()

irho_NFW = get_irho_nfw()

def get_irho_beta():
    """
    Element irho_beta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 570
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_beta()

irho_beta = get_irho_beta()

def get_irho_star_f14():
    """
    Element irho_star_f14 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 571
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_star_f14()

irho_star_F14 = get_irho_star_f14()

def get_irho_ks02_st15():
    """
    Element irho_ks02_st15 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 572
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ks02_st15()

irho_KS02_ST15 = get_irho_ks02_st15()

def get_irho_star_st15():
    """
    Element irho_star_st15 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 573
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_star_st15()

irho_star_ST15 = get_irho_star_st15()

def get_irho_ejected_st15():
    """
    Element irho_ejected_st15 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 574
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ejected_st15()

irho_ejected_ST15 = get_irho_ejected_st15()

def get_irho_ks02s_dens():
    """
    Element irho_ks02s_dens ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 575
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ks02s_dens()

irho_KS02s_dens = get_irho_ks02s_dens()

def get_irho_ks02s_temp():
    """
    Element irho_ks02s_temp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 576
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ks02s_temp()

irho_KS02s_temp = get_irho_ks02s_temp()

def get_irho_ks02s_pres():
    """
    Element irho_ks02s_pres ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 577
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ks02s_pres()

irho_KS02s_pres = get_irho_ks02s_pres()

def get_irho_upp():
    """
    Element irho_upp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 578
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_upp()

irho_UPP = get_irho_upp()

def get_irho_beta_ma15():
    """
    Element irho_beta_ma15 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 579
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_beta_ma15()

irho_beta_Ma15 = get_irho_beta_ma15()

def get_irho_iso_ext():
    """
    Element irho_iso_ext ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 580
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_iso_ext()

irho_iso_ext = get_irho_iso_ext()

def get_irho_powlaw():
    """
    Element irho_powlaw ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 581
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_powlaw()

irho_powlaw = get_irho_powlaw()

def get_irho_cubic():
    """
    Element irho_cubic ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 582
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_cubic()

irho_cubic = get_irho_cubic()

def get_irho_smooth():
    """
    Element irho_smooth ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 583
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_smooth()

irho_smooth = get_irho_smooth()

def get_irho_exp():
    """
    Element irho_exp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 584
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_exp()

irho_exp = get_irho_exp()

def get_irho_ks02_dens():
    """
    Element irho_ks02_dens ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 585
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ks02_dens()

irho_KS02_dens = get_irho_ks02_dens()

def get_irho_ks02_temp():
    """
    Element irho_ks02_temp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 586
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ks02_temp()

irho_KS02_temp = get_irho_ks02_temp()

def get_irho_ks02_pres():
    """
    Element irho_ks02_pres ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 587
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_ks02_pres()

irho_KS02_pres = get_irho_ks02_pres()

def get_irho_nfw_cored():
    """
    Element irho_nfw_cored ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 588
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_nfw_cored()

irho_NFW_cored = get_irho_nfw_cored()

def get_irho_poly_hole():
    """
    Element irho_poly_hole ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 589
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_poly_hole()

irho_poly_hole = get_irho_poly_hole()

def get_irho_nfw_hole():
    """
    Element irho_nfw_hole ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 590
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_nfw_hole()

irho_NFW_hole = get_irho_nfw_hole()

def get_irho_nfw_mod():
    """
    Element irho_nfw_mod ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 591
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_nfw_mod()

irho_NFW_mod = get_irho_nfw_mod()

def get_irho_shell():
    """
    Element irho_shell ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 592
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_shell()

irho_shell = get_irho_shell()

def get_irho_burket():
    """
    Element irho_burket ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 593
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_burket()

irho_Burket = get_irho_burket()

def get_irho_einasto():
    """
    Element irho_einasto ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 594
    
    """
    return _pyhmcode.f90wrap_hmx__get__irho_einasto()

irho_Einasto = get_irho_einasto()

def get_idv_200():
    """
    Element idv_200 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 596
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_200()

iDv_200 = get_idv_200()

def get_idv_bryan():
    """
    Element idv_bryan ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 597
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_bryan()

iDv_Bryan = get_idv_bryan()

def get_idv_hmcode2016():
    """
    Element idv_hmcode2016 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 598
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_hmcode2016()

iDv_HMcode2016 = get_idv_hmcode2016()

def get_idv_mead():
    """
    Element idv_mead ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 599
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_mead()

iDv_Mead = get_idv_mead()

def get_idv_sc():
    """
    Element idv_sc ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 600
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_sc()

iDv_SC = get_idv_sc()

def get_idv_lagrange():
    """
    Element idv_lagrange ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 601
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_lagrange()

iDv_Lagrange = get_idv_lagrange()

def get_idv_200c():
    """
    Element idv_200c ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 602
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_200c()

iDv_200c = get_idv_200c()

def get_idv_hmcode2015():
    """
    Element idv_hmcode2015 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 603
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_hmcode2015()

iDv_HMcode2015 = get_idv_hmcode2015()

def get_idv_178():
    """
    Element idv_178 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 604
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_178()

iDv_178 = get_idv_178()

def get_idv_user():
    """
    Element idv_user ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 605
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_user()

iDv_user = get_idv_user()

def get_idv_virial():
    """
    Element idv_virial ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 606
    
    """
    return _pyhmcode.f90wrap_hmx__get__idv_virial()

iDv_virial = get_idv_virial()

def get_imf_ps():
    """
    Element imf_ps ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 608
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_ps()

imf_PS = get_imf_ps()

def get_imf_st():
    """
    Element imf_st ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 609
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_st()

imf_ST = get_imf_st()

def get_imf_t10_pbs_z():
    """
    Element imf_t10_pbs_z ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 610
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_t10_pbs_z()

imf_T10_PBS_z = get_imf_t10_pbs_z()

def get_imf_delta():
    """
    Element imf_delta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 611
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_delta()

imf_delta = get_imf_delta()

def get_imf_jenkins():
    """
    Element imf_jenkins ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 612
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_jenkins()

imf_Jenkins = get_imf_jenkins()

def get_imf_despali():
    """
    Element imf_despali ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 613
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_despali()

imf_Despali = get_imf_despali()

def get_imf_t08_z():
    """
    Element imf_t08_z ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 614
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_t08_z()

imf_T08_z = get_imf_t08_z()

def get_imf_warren():
    """
    Element imf_warren ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 615
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_warren()

imf_Warren = get_imf_warren()

def get_imf_bhattacharya():
    """
    Element imf_bhattacharya ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 617
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_bhattacharya()

imf_Bhattacharya = get_imf_bhattacharya()

def get_imf_courtin():
    """
    Element imf_courtin ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 618
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_courtin()

imf_Courtin = get_imf_courtin()

def get_imf_st2002():
    """
    Element imf_st2002 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 619
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_st2002()

imf_ST2002 = get_imf_st2002()

def get_imf_st_free():
    """
    Element imf_st_free ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 620
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_st_free()

imf_ST_free = get_imf_st_free()

def get_imf_philcox():
    """
    Element imf_philcox ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 621
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_philcox()

imf_Philcox = get_imf_philcox()

def get_imf_t08():
    """
    Element imf_t08 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 622
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_t08()

imf_T08 = get_imf_t08()

def get_imf_t10_pbs():
    """
    Element imf_t10_pbs ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 623
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_t10_pbs()

imf_T10_PBS = get_imf_t10_pbs()

def get_imf_t10_cal_z():
    """
    Element imf_t10_cal_z ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 624
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_t10_cal_z()

imf_T10_cal_z = get_imf_t10_cal_z()

def get_imf_t10_cal():
    """
    Element imf_t10_cal ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 625
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_t10_cal()

imf_T10_cal = get_imf_t10_cal()

def get_imf_smt():
    """
    Element imf_smt ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 626
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_smt()

imf_SMT = get_imf_smt()

def get_imf_peacock():
    """
    Element imf_peacock ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 627
    
    """
    return _pyhmcode.f90wrap_hmx__get__imf_peacock()

imf_Peacock = get_imf_peacock()

def get_iconc_bullock_full():
    """
    Element iconc_bullock_full ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 630
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_bullock_full()

iconc_Bullock_full = get_iconc_bullock_full()

def get_iconc_bullock_simple():
    """
    Element iconc_bullock_simple ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 631
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_bullock_simple()

iconc_Bullock_simple = get_iconc_bullock_simple()

def get_iconc_duffy_full_200():
    """
    Element iconc_duffy_full_200 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 632
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_duffy_full_200()

iconc_Duffy_full_200 = get_iconc_duffy_full_200()

def get_iconc_duffy_full_vir():
    """
    Element iconc_duffy_full_vir ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 633
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_duffy_full_vir()

iconc_Duffy_full_vir = get_iconc_duffy_full_vir()

def get_iconc_duffy_full_200c():
    """
    Element iconc_duffy_full_200c ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 634
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_duffy_full_200c()

iconc_Duffy_full_200c = get_iconc_duffy_full_200c()

def get_iconc_duffy_relaxed_200():
    """
    Element iconc_duffy_relaxed_200 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 635
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_duffy_relaxed_200()

iconc_Duffy_relaxed_200 = get_iconc_duffy_relaxed_200()

def get_iconc_duffy_relaxed_vir():
    """
    Element iconc_duffy_relaxed_vir ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 636
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_duffy_relaxed_vir()

iconc_Duffy_relaxed_vir = get_iconc_duffy_relaxed_vir()

def get_iconc_duffy_relaxed_200c():
    """
    Element iconc_duffy_relaxed_200c ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 637
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_duffy_relaxed_200c()

iconc_Duffy_relaxed_200c = get_iconc_duffy_relaxed_200c()

def get_iconc_child():
    """
    Element iconc_child ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 638
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_child()

iconc_Child = get_iconc_child()

def get_iconc_diemer():
    """
    Element iconc_diemer ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 639
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_diemer()

iconc_Diemer = get_iconc_diemer()

def get_iconc_neto_full():
    """
    Element iconc_neto_full ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 640
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_neto_full()

iconc_Neto_full = get_iconc_neto_full()

def get_iconc_neto_relaxed():
    """
    Element iconc_neto_relaxed ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 641
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_neto_relaxed()

iconc_Neto_relaxed = get_iconc_neto_relaxed()

def get_iconc_nfw():
    """
    Element iconc_nfw ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 642
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_nfw()

iconc_NFW = get_iconc_nfw()

def get_iconc_ens():
    """
    Element iconc_ens ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 643
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_ens()

iconc_ENS = get_iconc_ens()

def get_iconc_prada():
    """
    Element iconc_prada ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 644
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_prada()

iconc_Prada = get_iconc_prada()

def get_iconc_klypin():
    """
    Element iconc_klypin ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 645
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_klypin()

iconc_Klypin = get_iconc_klypin()

def get_iconc_okoli():
    """
    Element iconc_okoli ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 646
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_okoli()

iconc_Okoli = get_iconc_okoli()

def get_iconc_maccio():
    """
    Element iconc_maccio ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 647
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_maccio()

iconc_Maccio = get_iconc_maccio()

def get_iconc_seljak():
    """
    Element iconc_seljak ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 648
    
    """
    return _pyhmcode.f90wrap_hmx__get__iconc_seljak()

iconc_Seljak = get_iconc_seljak()

def get_param_alpha():
    """
    Element param_alpha ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 650
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_alpha()

param_alpha = get_param_alpha()

def get_param_eps():
    """
    Element param_eps ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 651
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_eps()

param_eps = get_param_eps()

def get_param_gamma():
    """
    Element param_gamma ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 652
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_gamma()

param_gamma = get_param_gamma()

def get_param_m0():
    """
    Element param_m0 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 653
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_m0()

param_M0 = get_param_m0()

def get_param_astar():
    """
    Element param_astar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 654
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_astar()

param_Astar = get_param_astar()

def get_param_twhim():
    """
    Element param_twhim ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 655
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_twhim()

param_Twhim = get_param_twhim()

def get_param_cstar():
    """
    Element param_cstar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 656
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_cstar()

param_cstar = get_param_cstar()

def get_param_fcold():
    """
    Element param_fcold ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 657
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_fcold()

param_fcold = get_param_fcold()

def get_param_mstar():
    """
    Element param_mstar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 658
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_mstar()

param_mstar = get_param_mstar()

def get_param_sstar():
    """
    Element param_sstar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 659
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_sstar()

param_sstar = get_param_sstar()

def get_param_alphap():
    """
    Element param_alphap ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 660
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_alphap()

param_alphap = get_param_alphap()

def get_param_gammap():
    """
    Element param_gammap ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 661
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_gammap()

param_Gammap = get_param_gammap()

def get_param_cstarp():
    """
    Element param_cstarp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 662
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_cstarp()

param_cstarp = get_param_cstarp()

def get_param_fhot():
    """
    Element param_fhot ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 663
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_fhot()

param_fhot = get_param_fhot()

def get_param_alphaz():
    """
    Element param_alphaz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 664
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_alphaz()

param_alphaz = get_param_alphaz()

def get_param_gammaz():
    """
    Element param_gammaz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 665
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_gammaz()

param_Gammaz = get_param_gammaz()

def get_param_m0z():
    """
    Element param_m0z ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 666
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_m0z()

param_M0z = get_param_m0z()

def get_param_astarz():
    """
    Element param_astarz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 667
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_astarz()

param_Astarz = get_param_astarz()

def get_param_twhimz():
    """
    Element param_twhimz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 668
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_twhimz()

param_Twhimz = get_param_twhimz()

def get_param_eta():
    """
    Element param_eta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 669
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_eta()

param_eta = get_param_eta()

def get_param_hmcode_dv0():
    """
    Element param_hmcode_dv0 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 670
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_dv0()

param_HMcode_Dv0 = get_param_hmcode_dv0()

def get_param_hmcode_dv1():
    """
    Element param_hmcode_dv1 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 671
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_dv1()

param_HMcode_Dv1 = get_param_hmcode_dv1()

def get_param_hmcode_dc0():
    """
    Element param_hmcode_dc0 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 672
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_dc0()

param_HMcode_dc0 = get_param_hmcode_dc0()

def get_param_hmcode_dc1():
    """
    Element param_hmcode_dc1 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 673
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_dc1()

param_HMcode_dc1 = get_param_hmcode_dc1()

def get_param_hmcode_eta0():
    """
    Element param_hmcode_eta0 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 674
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_eta0()

param_HMcode_eta0 = get_param_hmcode_eta0()

def get_param_hmcode_eta1():
    """
    Element param_hmcode_eta1 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 675
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_eta1()

param_HMcode_eta1 = get_param_hmcode_eta1()

def get_param_hmcode_f0():
    """
    Element param_hmcode_f0 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 676
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_f0()

param_HMcode_f0 = get_param_hmcode_f0()

def get_param_hmcode_f1():
    """
    Element param_hmcode_f1 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 677
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_f1()

param_HMcode_f1 = get_param_hmcode_f1()

def get_param_hmcode_kstar():
    """
    Element param_hmcode_kstar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 678
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_kstar()

param_HMcode_kstar = get_param_hmcode_kstar()

def get_param_hmcode_as():
    """
    Element param_hmcode_as ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 679
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_as()

param_HMcode_As = get_param_hmcode_as()

def get_param_hmcode_alpha0():
    """
    Element param_hmcode_alpha0 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 680
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_alpha0()

param_HMcode_alpha0 = get_param_hmcode_alpha0()

def get_param_hmcode_alpha1():
    """
    Element param_hmcode_alpha1 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 681
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_alpha1()

param_HMcode_alpha1 = get_param_hmcode_alpha1()

def get_param_epsz():
    """
    Element param_epsz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 682
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_epsz()

param_epsz = get_param_epsz()

def get_param_beta():
    """
    Element param_beta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 683
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_beta()

param_beta = get_param_beta()

def get_param_betap():
    """
    Element param_betap ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 684
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_betap()

param_betap = get_param_betap()

def get_param_betaz():
    """
    Element param_betaz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 685
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_betaz()

param_betaz = get_param_betaz()

def get_param_etaz():
    """
    Element param_etaz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 686
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_etaz()

param_etaz = get_param_etaz()

def get_param_cstarz():
    """
    Element param_cstarz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 687
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_cstarz()

param_cstarz = get_param_cstarz()

def get_param_mstarz():
    """
    Element param_mstarz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 688
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_mstarz()

param_mstarz = get_param_mstarz()

def get_param_ibeta():
    """
    Element param_ibeta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 689
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_ibeta()

param_ibeta = get_param_ibeta()

def get_param_ibetap():
    """
    Element param_ibetap ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 690
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_ibetap()

param_ibetap = get_param_ibetap()

def get_param_ibetaz():
    """
    Element param_ibetaz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 691
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_ibetaz()

param_ibetaz = get_param_ibetaz()

def get_param_gbeta():
    """
    Element param_gbeta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 692
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_gbeta()

param_gbeta = get_param_gbeta()

def get_param_gbetaz():
    """
    Element param_gbetaz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 693
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_gbetaz()

param_gbetaz = get_param_gbetaz()

def get_param_hmcode_dvnu():
    """
    Element param_hmcode_dvnu ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 694
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_dvnu()

param_HMcode_Dvnu = get_param_hmcode_dvnu()

def get_param_hmcode_dcnu():
    """
    Element param_hmcode_dcnu ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 695
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_dcnu()

param_HMcode_dcnu = get_param_hmcode_dcnu()

def get_param_eps2():
    """
    Element param_eps2 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 696
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_eps2()

param_eps2 = get_param_eps2()

def get_param_eps2z():
    """
    Element param_eps2z ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 697
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_eps2z()

param_eps2z = get_param_eps2z()

def get_param_zamma():
    """
    Element param_zamma ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 698
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_zamma()

param_Zamma = get_param_zamma()

def get_param_zammap():
    """
    Element param_zammap ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 699
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_zammap()

param_Zammap = get_param_zammap()

def get_param_zammaz():
    """
    Element param_zammaz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 700
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_zammaz()

param_Zammaz = get_param_zammaz()

def get_param_hmcode_mbar():
    """
    Element param_hmcode_mbar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 701
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_mbar()

param_HMcode_mbar = get_param_hmcode_mbar()

def get_param_hmcode_nbar():
    """
    Element param_hmcode_nbar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 702
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_nbar()

param_HMcode_nbar = get_param_hmcode_nbar()

def get_param_hmcode_amf():
    """
    Element param_hmcode_amf ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 703
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_amf()

param_HMcode_Amf = get_param_hmcode_amf()

def get_param_hmcode_sbar():
    """
    Element param_hmcode_sbar ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 704
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_sbar()

param_HMcode_sbar = get_param_hmcode_sbar()

def get_param_hmcode_stp():
    """
    Element param_hmcode_stp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 705
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_stp()

param_HMcode_STp = get_param_hmcode_stp()

def get_param_hmcode_stq():
    """
    Element param_hmcode_stq ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 706
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_stq()

param_HMcode_STq = get_param_hmcode_stq()

def get_param_hmcode_kd():
    """
    Element param_hmcode_kd ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 707
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_kd()

param_HMcode_kd = get_param_hmcode_kd()

def get_param_hmcode_ap():
    """
    Element param_hmcode_ap ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 708
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_ap()

param_HMcode_Ap = get_param_hmcode_ap()

def get_param_hmcode_ac():
    """
    Element param_hmcode_ac ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 709
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_ac()

param_HMcode_Ac = get_param_hmcode_ac()

def get_param_hmcode_kp():
    """
    Element param_hmcode_kp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 710
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_kp()

param_HMcode_kp = get_param_hmcode_kp()

def get_param_hmcode_kdp():
    """
    Element param_hmcode_kdp ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 711
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_kdp()

param_HMcode_kdp = get_param_hmcode_kdp()

def get_param_hmcode_mbarz():
    """
    Element param_hmcode_mbarz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 712
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_mbarz()

param_HMcode_mbarz = get_param_hmcode_mbarz()

def get_param_hmcode_sbarz():
    """
    Element param_hmcode_sbarz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 713
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_sbarz()

param_HMcode_sbarz = get_param_hmcode_sbarz()

def get_param_hmcode_amfz():
    """
    Element param_hmcode_amfz ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 714
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_amfz()

param_HMcode_Amfz = get_param_hmcode_amfz()

def get_param_hmcode_nd():
    """
    Element param_hmcode_nd ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 715
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_nd()

param_HMcode_nd = get_param_hmcode_nd()

def get_param_hmcode_alpha2():
    """
    Element param_hmcode_alpha2 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 716
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_alpha2()

param_HMcode_alpha2 = get_param_hmcode_alpha2()

def get_param_hmcode_fm():
    """
    Element param_hmcode_fm ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 717
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_fm()

param_HMcode_fM = get_param_hmcode_fm()

def get_param_hmcode_fd():
    """
    Element param_hmcode_fd ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 718
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_fd()

param_HMcode_fD = get_param_hmcode_fd()

def get_param_hmcode_zd():
    """
    Element param_hmcode_zd ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 719
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_zd()

param_HMcode_zD = get_param_hmcode_zd()

def get_param_hmcode_az():
    """
    Element param_hmcode_az ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 720
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_hmcode_az()

param_HMcode_Az = get_param_hmcode_az()

def get_param_pt_a():
    """
    Element param_pt_a ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 721
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_pt_a()

param_PT_A = get_param_pt_a()

def get_param_pt_alpha():
    """
    Element param_pt_alpha ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 722
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_pt_alpha()

param_PT_alpha = get_param_pt_alpha()

def get_param_pt_beta():
    """
    Element param_pt_beta ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 723
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_pt_beta()

param_PT_beta = get_param_pt_beta()

def get_param_n():
    """
    Element param_n ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 724
    
    """
    return _pyhmcode.f90wrap_hmx__get__param_n()

param_n = get_param_n()

def get_hmcode2015():
    """
    Element hmcode2015 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 726
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2015()

HMcode2015 = get_hmcode2015()

def get_hmcode2015_camb():
    """
    Element hmcode2015_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 727
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2015_camb()

HMcode2015_CAMB = get_hmcode2015_camb()

def get_hmcode2016():
    """
    Element hmcode2016 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 728
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2016()

HMcode2016 = get_hmcode2016()

def get_hmcode2016_camb():
    """
    Element hmcode2016_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 729
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2016_camb()

HMcode2016_CAMB = get_hmcode2016_camb()

def get_hmcode2016_neutrinofix():
    """
    Element hmcode2016_neutrinofix ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 730
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2016_neutrinofix()

HMcode2016_neutrinofix = get_hmcode2016_neutrinofix()

def get_hmcode2016_neutrinofix_camb():
    """
    Element hmcode2016_neutrinofix_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 731
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2016_neutrinofix_camb()

HMcode2016_neutrinofix_CAMB = get_hmcode2016_neutrinofix_camb()

def get_hmcode2018():
    """
    Element hmcode2018 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 732
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2018()

HMcode2018 = get_hmcode2018()

def get_hmcode2019():
    """
    Element hmcode2019 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 733
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2019()

HMcode2019 = get_hmcode2019()

def get_hmcode2020():
    """
    Element hmcode2020 ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 734
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2020()

HMcode2020 = get_hmcode2020()

def get_hmcode2020_camb():
    """
    Element hmcode2020_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 735
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2020_camb()

HMcode2020_CAMB = get_hmcode2020_camb()

def get_hmcode2020_feedback():
    """
    Element hmcode2020_feedback ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 736
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2020_feedback()

HMcode2020_feedback = get_hmcode2020_feedback()

def get_hmcode2020_feedback_camb():
    """
    Element hmcode2020_feedback_camb ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 737
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2020_feedback_camb()

HMcode2020_feedback_CAMB = get_hmcode2020_feedback_camb()

def get_hmcode2020_feedback_lowkfix():
    """
    Element hmcode2020_feedback_lowkfix ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 738
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2020_feedback_lowkfix()

HMcode2020_feedback_lowkfix = get_hmcode2020_feedback_lowkfix()

def get_hmcode2020_feedback_camb_lowkfix():
    """
    Element hmcode2020_feedback_camb_lowkfix ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 739
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmcode2020_feedback_camb_lowkfix()

HMcode2020_feedback_CAMB_lowkfix = get_hmcode2020_feedback_camb_lowkfix()

def get_hmx2020_matter_w_temp_scaling():
    """
    Element hmx2020_matter_w_temp_scaling ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 741
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmx2020_matter_w_temp_scaling()

HMx2020_matter_w_temp_scaling = get_hmx2020_matter_w_temp_scaling()

def get_hmx2020_matter_pressure_w_temp_scaling():
    """
    Element hmx2020_matter_pressure_w_temp_scaling ftype=integer pytype=int
    
    
    Defined at ../library/src/hmx.f90 line 742
    
    """
    return _pyhmcode.f90wrap_hmx__get__hmx2020_matter_pressure_w_temp_scaling()

HMx2020_matter_pressure_w_temp_scaling = \
    get_hmx2020_matter_pressure_w_temp_scaling()

def get_acc_win():
    """
    Element acc_win ftype=real  pytype=float
    
    
    Defined at ../library/src/hmx.f90 line 744
    
    """
    return _pyhmcode.f90wrap_hmx__get__acc_win()

def set_acc_win(acc_win):
    _pyhmcode.f90wrap_hmx__set__acc_win(acc_win)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "hmx".')

for func in _dt_array_initialisers:
    func()
