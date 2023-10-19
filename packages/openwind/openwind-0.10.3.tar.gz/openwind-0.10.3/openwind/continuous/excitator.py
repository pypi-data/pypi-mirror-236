
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2019-2023, INRIA
#
# This file is part of Openwind.
#
# Openwind is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Openwind is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openwind.  If not, see <https://www.gnu.org/licenses/>.
#
# For more informations about authors, see the CONTRIBUTORS file

"""Module for the exitator classes"""

from abc import ABC, abstractmethod
import warnings
import numpy as np

from openwind.continuous import NetlistConnector


def create_excitator(player, label, scaling, convention):
    """
    Instanciate the right excitator according to the player information

    Parameters
    ----------
    player : :py:class:`Player<openwind.technical.player.Player>`
        The object with the excitator information.
    label : str
        The label of the connector.
    scaling : :py:class: `Scaling <openwind.continuous.scaling.Scaling>`
        Nondimensionalization coefficients.
    convention : str, optional
        Must be one out of {'PH1', 'VH1'} \
        The convention used in this component. The default is 'PH1'.

    Returns
    -------
    :py:class:`Excitator<Excitator>`
        The rigth excitator object.

    """
    exc_type = player.excitator_type

    if exc_type == "Flow":
        return Flow(player.control_parameters, label, scaling, convention)
    elif exc_type == "Reed1dof":
        return Reed1dof(player.control_parameters, label, scaling, convention)
    elif exc_type == "Reed1dof_scaled":
        return Reed1dof_Scaled(player.control_parameters, label, scaling, convention)
    else:
        raise ValueError("Could not convert excitator type '{:s}'; please chose"
                         " between {}".format(exc_type, ["Flow", "Reed1dof", "Reed1dof_scaled"]))

class ExcitatorParameter(ABC):
    """
    Abstract class for excitator parameter

    An excitator parameter can be any parameter asociated to the model of
    the excitator. It can be stationnary or evolving with respect to time.

    """
    @abstractmethod
    def get_value(self,t):
        """
        Method which returns the curve value for a given time t

        Parameters
        ----------
        t : float
            The time at which we want to get the curve value

        Returns
        -------
        float
            the value of the parameter at the time t
        """
        pass


class VariableExcitatorParameter(ExcitatorParameter):
    """
    Class for any excitator parameter which varies with respect to time.

    Parameters
    ----------
    curve : callable
        time dependant function. For example, you can use a curve from the
        module :py:mod:`Temporal Curve <openwind.technical.temporal_curves>`.

    """
    def __init__(self,curve):
        self._variable_value = curve

    def get_value(self,t):
        return self._variable_value(t)


class FixedExcitatorParameter(ExcitatorParameter):
    """
    Class for stationnary excitator parameter

    Parameters
    ----------
    curve : float
        Fixed value for the parameter
    """
    def __init__(self, curve):
        self._fixed_value = curve


    def get_value(self,t):
        return self._fixed_value


class Excitator(ABC, NetlistConnector):
    """
    One excitator, a source of the acoustic oscillations.

    It a component of a :py:class:`Netlist<openwind.continuous.netlist.Netlist>`
    which interacts with a :py:class:`PipeEnd<openwind.continuous.netlist.PipeEnd>`.

    The excitator is typically an oscillator coupled with the acoustic fields.
    It brings the energy into the acoustical system. It is generally described
    trough a set of ODE, the coefficients of which can vary with time.

    Parameters
    ----------
    control_parameters : dict
        Associate each controle parameter (coefficient of the ODE) to its value
        and the evolution with respect to time. It must have all the keys
        necessary to instanciate the right excitator.
    label : str
        the label of the connector
    scaling : :py:class:`Scaling<openwind.continuous.scaling.Scaling>`
        object which knows the value of the coefficient used to scale the
        equations
    convention : {'PH1', 'VH1'}
        The basis functions for our finite elements must be of regularity
        H1 for one variable, and L2 for the other.
        Regularity L2 means that some degrees of freedom are duplicated
        between elements, whereas they are merged in H1.
        Convention chooses whether P (pressure) or V (flow) is the H1
        variable.
    """

    NEEDED_PARAMS = list()
    """list of str: Needed parameters to instanciate the excitator"""

    def __init__(self, control_parameters, label, scaling, convention):
        super().__init__(label, scaling, convention)
        self.check_needed_params(control_parameters)
        self._update_fields(control_parameters)

    def check_needed_params(self, control_parameters):
        if not set(self.NEEDED_PARAMS) <= set(control_parameters):
            missing = list(set(self.NEEDED_PARAMS) - set(control_parameters))
            raise ValueError(f'The following parameters are missing in "Player": {missing}')

    @abstractmethod
    def _update_fields(self, control_parameters):
        """
        This method update all the attributes according to the
        control_parameters fields attributes

        Parameters
        ----------
        control_parameters : dict
            Associate each controle parameter (coefficient of the ODE) to its value
            and the evolution with respect to time. It must have all the keys
            necessary to instanciate the right excitator.
        """

    @staticmethod
    def _create_parameter(curve):
        if callable(curve):
            return VariableExcitatorParameter(curve)
        else:
            return FixedExcitatorParameter(curve)


class Flow(Excitator):
    """
    Flow excitator: imposes the value of the flow at the connected pipe-end.

    This excitator simply imposes the flow at the pipe-end connected to it. The
    only parameter is the flow in m^3/s


    See Also
    --------
    :py:class:`FrequentialSource\
        <openwind.frequential.frequential_source.FrequentialSource>`
        The frequential version of this excitator (only has a sense for dirac flow)
    :py:class:`TemporalFlowCondition\
        <openwind.temporal.tflow_condition.TemporalFlowCondition>`
        The temporal version of this excitator

    Parameters
    ----------
    control_parameters : dict
        Associate each controle parameter (coefficient of the ODE) to its value
        and the evolution with respect to time. It must have only the key
        "input_flow".
    label : str
        the label of the connector
    scaling : :py:class:`Scaling<openwind.continuous.scaling.Scaling>`
        object which knows the value of the coefficient used to scale the
        equations
    convention : {'PH1', 'VH1'}
        The basis functions for our finite elements must be of regularity
        H1 for one variable, and L2 for the other.
        Regularity L2 means that some degrees of freedom are duplicated
        between elements, whereas they are merged in H1.
        Convention chooses whether P (pressure) or V (flow) is the H1
        variable.

    Attributes
    ----------
    input_flow : float or callable
        The value in m^3/s of the flow at the entrance of the instrument or its
        evolution with time
    """

    def _update_fields(self, control_parameters):
        self.input_flow = self._create_parameter(control_parameters["input_flow"])


# TODO : write this class methods
class Flute(Excitator):
    """class for a flute excitator, to define"""
    def __init__(self, player, label, scaling, convention):
        raise NotImplementedError()


class Reed1dof(Excitator):
    """
    Reed excitator (cane or lips): non-linear excitator

    A reed excitator is used to model both brass (lips-reeds) and woodwind
    (cane-reed) instruments. It can be, following [Fletcher]_ nomeclature, an:

    - outwards valve (lips-reeds) for brass: the reed opens when the supply \
    pressure is higher than the pressure inside the instrument
    - inwards valve (cane-reed) for simple or double reed instruments: the reed \
    opens when the supply pressure is smaller than the pressure inside the\
    instrument

    The reed is modelled by a 1D damped mass-spring oscillator following
    [Bilbao]_. The contact at closure is modelled through a penalizating term.

    .. math::
        \\begin{align}
        &\\ddot{y} + g \\dot{y} + \\omega_0^2 (y - y_0) - \
            \\frac{\\omega_1^{\\alpha+1}}{y_0^{\\alpha-1}}(|[y]^{-}|)^{\\alpha}\
            =  \\epsilon \\frac{S_r \\Delta p}{M_r} \\\\
        &\\Delta p = p_m - p \\\\
        & u = w [y]^{+} \\sqrt{\\frac{2 |\\Delta p|}{\\rho}} sign(\\Delta p) \
            \\epsilon S_r \\dot{y}
        \\end{align}

    With :math:`y` the position of the reed, :math:`[y]^{\\pm}` the positive
    or negative part of :math:`y`, :math:`p,u` the acoustic fields inside the
    instrument and :math:`\\rho` the air density.

    The other coefficients must be specified by the user. They are:

    - "opening" :math:`y_0` : the resting opening height of the reed (in m)
    - "mass" :math:`M_r` : the effective mass of the reed (in kg)
    - "section" :math:`S_r` : the effective vibrating surface of the reed  \
    (and not the opening) (in m²)
    - "pulsation" :math:`\\omega_0` : the resonant angular frequency of the reed
    - "dissip" :math:`g` : the damping coefficient
    - "width" :math:`w` : the effective width of the reed channel opening (in m)
    - "mouth_pressure" :math:`p_m` : the supply pressure (in Pa)
    - "model" : string coefficient that specifies if it is a "cane" (inwards)\
        or "lips" (inwards) reed. It fixes the value of :math:`\\epsilon` to \
        1 (cane) or -1 (lips)
    - "contact_pulsation" :math:`\\omega_1` : the angular frequency associated\
        to the contact law when the reed is closed.
    - "contact_exponent" :math:`\\alpha` : the exponent associated to the \
        contact law when the reed is closed.


    .. warning::
        This excitator can be used only in temporal domain

    See Also
    --------
    :py:class:`TemporalReed1dof\
        <openwind.temporal.treed.TemporalReed1dof>`
        The temporal version of this excitator

    References
    ----------
    .. [Bilbao] Bilbao, S. (2009). Direct simulation of reed wind instruments.\
        Computer Music Journal, 33(4), 43-55.
    .. [Fletcher] Fletcher, N H. 1979. “Excitation Mechanisms in Woodwind and \
        Brass Instruments.” Acustica 43: 10.


    Parameters
    ----------
    control_parameters : dict
        Associate each controle parameter (coefficient of the ODE) to its value
        and the evolution with respect to time. It must have the keys
        `["opening", "mass", "section", "pulsation", "dissip", "width",
        "mouth_pressure", "model", "contact_pulsation", "contact_exponent"]`.
    label : str
        the label of the connector
    scaling : :py:class:`Scaling<openwind.continuous.scaling.Scaling>`
        object which knows the value of the coefficient used to scale the
        equations
    convention : {'PH1', 'VH1'}
        The basis functions for our finite elements must be of regularity
        H1 for one variable, and L2 for the other.
        Regularity L2 means that some degrees of freedom are duplicated
        between elements, whereas they are merged in H1.
        Convention chooses whether P (pressure) or V (flow) is the H1
        variable.

    Attributes
    ----------
    opening : float or callable
        :math:`y_0` : the resting opening height of the reed (in m)
    mass : float or callable
        :math:`M_r` : the effective mass of the reed (in kg)
    section : float or callable
        :math:`S_r` : the effective vibrating surface of the reed
        (and not the opening) (in m²)
    pulsation : float or callable
        :math:`\\omega_0` : the resonant angular frequency of the reed
    dissip : float or callable
        :math:`\\sigma` : the damping coefficient
    width : float or callable
        :math:`w` : the effective width of the reed channel opening (in m)
    mouth_pressure : float or callable
        :math:`p_m` : the supply pressure (in Pa)
    model : -1 or 1
        :math:`\\epsilon` the opening sens of the reed: 1 (cane,\
        inwards) or -1 (lips, outwards)
    contact_pulsation : float or callable
        :math:`\\omega_1` : the angular frequency associated to the contact \
        law when the reed is closed.
    contact_exponent : float or callable
        :math:`\\alpha` : the exponent associated to the contact law when the\
        reed is closed.
    """

    NEEDED_PARAMS = ["mouth_pressure", "opening",  "mass", "section",
                     "pulsation", "dissip", "width", "contact_pulsation",
                     "contact_exponent", "model"]
    """list of str: Needed parameters to instanciate the excitator"""

    def _update_fields(self, control_parameters):

        self.mouth_pressure = self._create_parameter(control_parameters["mouth_pressure"])

        # currently only constant value are accepted for other parameters
        # the numerical schemes are not compatible with varaible coefficients.
        self.opening = self._create_cst_param(control_parameters["opening"])
        self.mass = self._create_cst_param(control_parameters["mass"])
        self.section = self._create_cst_param(control_parameters["section"])
        self.pulsation = self._create_cst_param(control_parameters["pulsation"])
        self.dissip = self._create_cst_param(control_parameters["dissip"])
        self.width = self._create_cst_param(control_parameters["width"])
        self.contact_pulsation =  self._create_cst_param(control_parameters["contact_pulsation"])
        self.contact_exponent =  self._create_cst_param(control_parameters["contact_exponent"])

        # the value of epsilon is set by interpreting the keyword in "model"
        model = control_parameters['model']
        if model in ["lips","outwards"]:
            model_value = 1
        elif model in ["cane","inwards"]:
            model_value= -1
        else:
            warnings.warn("WARNING : your model is %s, but it must "
                  "be in {'lips', 'outwards', 'cane', 'inwards'}, it "
                  "will be set to default (lips)"
                  %model)
            model_value = 1
        self.model = FixedExcitatorParameter(model_value)


    @staticmethod
    def _create_cst_param(curve):
        if callable(curve):
            raise ValueError("Except 'mouth_pressure', evolving parameters of "
                             "Reed1dof Excitator are not supported yet, must be a"
                             " constant value")
        else:
            return FixedExcitatorParameter(curve)


    def get_dimensionfull_values(self, t, Zc=1, rho=1):
        """
        Method that returns the values of all the dimensionfull parameters at a given time

        Parameters
        ----------
        t : int
            The given time we want to get the curves values from
        Zc : float, UNUSED
            The characteristic (real) impedance at the entry of the instrument.
        rho : float, UNUSED
            the air density.

        Returns
        -------
        Sr : float
            the effective cross section area of the reed (in m²)
        Mr: float
            the effecitve mass of the read (in kg)
        g: float
            the damping coefficient
        omega02: float
             the squared resonant angular frequency
        w: float
            the effective width of the reed channel opening (in m)
        y0: float
            the resting opening of the reed (in m)
        epsilon: float
            1 (for lips/outwards) or -1 (cane/inwards) following the model
        pm: float
            the supply pressure (in Pa)
        """
        Sr = self.section.get_value(t)
        Mr = self.mass.get_value(t)
        g = self.dissip.get_value(t)
        omega02 = self.pulsation.get_value(t)**2
        w = self.width.get_value(t)
        y0 = self.opening.get_value(t)
        epsilon = self.model.get_value(t)
        pm= self.mouth_pressure.get_value(t)

        omega_c = self.contact_pulsation.get_value(t)
        alpha_c = self.contact_exponent.get_value(t)

        return (Sr, Mr, g, omega02, w, y0, epsilon, pm, omega_c, alpha_c)

    def get_dimensionless_values(self, t, Zc, rho):
        """
        Return the values of all dimensionless parameter at a given time:

        Parameters
        ----------
        t : float
            The given time we want to get the curves values from.
        Zc : float
            The characteristic (real) impedance at the entry of the instrument.
        rho : float
            the air density.

        Returns
        -------
        gamma : float
            Dimensionless parameter relative to the supply pressure.
        zeta : float
            Dimensionless parameter relative to the reed opening.
        kappa : float
            The dimensionless parameter relative to the "reed flow".
        Qr : float
            the quality factor of the ree.
        omegar : float
            The resonant angular frequency of the reed in rad/s.
        Kc : float
            The contact force stifness.
        alpha_c : TYPE
            DESCRIPTION.
        epsilon : float
            1 (for lips/outwards) or -1 (cane/inwards) following the model.

        """
        (Sr, Mr, g, omega02, w, y0, epsilon, pm, omega_nl, alpha_c) = self.get_dimensionfull_values(t)

        omegar = np.sqrt(omega02)
        Kc = omega_nl**(alpha_c+1)/omega02
        Qr = omegar/g

        Pclosed = self.get_Pclosed(t)

        gamma = pm/Pclosed
        zeta = Zc*y0*w*np.sqrt(2/(rho*Pclosed))
        kappa = y0*Zc*Sr*omegar/Pclosed
        return gamma, zeta, kappa, Qr, omegar, Kc, alpha_c, epsilon

    def get_Pclosed(self, t):
        r"""
        Return the closing pressure of the reed.

        This value does not modify the response of the system. It is only necessary
        to rescale the results of the equations.

        .. math::
            P_{\text{closed}} = \frac{K_r }{S_r}  y_0 =  \omega_r^2 \frac{M_r}{S_r} y_0

        Parameters
        ----------
        t : float
            The given time we want to get the curves values from.

        Returns
        -------
        Pclosed : float
            The closing pressure in Pa.

        """
        Sr = self.section.get_value(t)
        Mr = self.mass.get_value(t)
        omegar = self.pulsation.get_value(t)
        y0 = self.opening.get_value(t)
        Kr = omegar**2*Mr # the reed stiffness
        Pclosed = Kr*y0/Sr
        return Pclosed



class Reed1dof_Scaled(Excitator):
    r"""
    Reed excitator (cane or lips): non-linear excitator with dimensionless parameters

    A reed excitator is used to model both brass (lips-reeds) and woodwind
    (cane-reed) instruments. It can be, following [Fletcher_sclaled]_ nomenclature, an:

    - outwards valve (lips-reeds) for brass: the reed opens when the supply\
      pressure is higher than the pressure inside the instrument
    - inwards valve (cane-reed) for simple or double reed instruments: the reed\
      opens when the supply pressure is smaller than the pressure inside the instrument

    The reed is modelled by a 1D damped mass-spring oscillator following
    [Bilbao_sclaled]_. The contact at closure is modelled through a penalizating term.
    The equations are scaled to make appear dimensionless coefficients and
    variables (e.g. [Chabassier_scaling]_):

    .. math::
        \begin{align}
        &\frac{1}{\omega_r^2}\ddot{y} + \frac{1}{\omega_r Q_r} \dot{y} +  y
        - K_c \left\vert \left[ y \right]^{-} \right\vert^{\alpha}   =  1 +\epsilon  \Delta p \\
        &p  = \gamma - \Delta p  \\
        &u = \zeta [y]^{+} \text{sign}(\Delta p) \sqrt{ \vert \Delta p \vert}
        + \epsilon \kappa \frac{1}{\omega_r} \dot{y}
        \end{align}

    With :math:`y` the dimensionless position of the reed, :math:`[y]^{\\pm}` the positive
    or negative part of :math:`y`, :math:`p,u` the dimensionless acoustic fields inside the
    instrument.

    The other coefficients must be specified by the user. They are:

    - "gamma" :math:`\gamma` : the first dimensionless parameter relative to the supply pressure
    - "zeta" :math:`\zeta` : the second dimensionless parameter relative to the "reed opening"
    - "kappa" :math:`\kappa` : the third dimensionless parameter relative to the "reed flow"
    - "pulsation" :math:`\omega_r` : the resonant angular frequency of the reed (in rad/s)
    - "qfactor" :math:`Q_r` : the quality factor of the reed
    - "model" : string coefficient that specifies if it is a "cane" (inwards) \
      or "lips" (inwards) reed. It fixes the value of :math:`\\epsilon` to 1 (cane) or -1 (lips)
    - "contact_stifness" :math:`K_c` : the stifness associated to the contact law when the reed is closed.
    - "contact_exponent" :math:`\\alpha` : the exponent associated to the contact law when the reed is closed.

    In order to rescale the variables, two other parameters can be given.
    They do not influence the result of the simulation, only the magnitude of the signals.

    - "closing_pressure" :math:`P_{closed}` the minimal pressure for which the reed is closed (in Pa)
    - "opening" :math:`y_0` : the resting opening height of the reed (in m)

    The "real" variables with dimensions are:

    - :math:`y \times y_0`
    - :math:`p \times P_{closed}`
    - :math:`u \times P_{closed} /Z_c` (with :math: `Z_c` the caracteristic impedance of the pipe)

    .. warning::
        This excitator can be used only in temporal domain

    See Also
    --------
    :py:class:`TemporalReed1dof <openwind.temporal.treed.TemporalReed1dof>`
        The temporal version of this excitator

    References
    ----------
    .. [Bilbao_sclaled] Bilbao, S. (2009). Direct simulation of reed wind instruments.\
        Computer Music Journal, 33(4), 43-55.
    .. [Fletcher_sclaled] Fletcher, N H. 1979. “Excitation Mechanisms in Woodwind and \
        Brass Instruments.” Acustica 43: 10.
    .. [Chabassier_scaling] J. Chabassier and R. Auvray 2022. "Control Parameters\
        for Reed Wind Instruments or Organ Pipes with Reed Induced Flow". 25th \
        International Conference on Digital Audio Effects (Vienna, Austria).



    Parameters
    ----------
    control_parameters : dict
        Associate each controle parameter (coefficient of the ODE) to its value\
        and the evolution with respect to time. It must have the keys\
        `["gamma", "zeta", "kappa", "pulsation", "qfactor", "model",\
        "contact_stifness", "contact_exponent", "closing_pressure", "opening"]`.
    label : str
        the label of the connector
    scaling : :py:class:`Scaling<openwind.continuous.scaling.Scaling>`
        object which knows the value of the coefficient used to scale the
        equations
    convention : {'PH1', 'VH1'}
        The basis functions for our finite elements must be of regularity
        H1 for one variable, and L2 for the other.
        Regularity L2 means that some degrees of freedom are duplicated
        between elements, whereas they are merged in H1.
        Convention chooses whether P (pressure) or V (flow) is the H1
        variable.

    Attributes
    ----------
    gamma: float or callable
        :math:`\gamma` : the first dimensionless parameter relative to the supply pressure
    zeta: float or callable
        :math:`\zeta` : the second dimensionless parameter relative to the "reed opening"
    kappa: float or callable
        :math:`\kappa` : the third dimensionless parameter relative to the "reed flow"
    pulsation: float or callable
        :math:`\omega_r` : the resonant angular frequency of the reed (in rad/s)
    qfactor: float or callable
        :math:`Q_r` : the quality factor of the reed
    model : -1 or 1
        :math:`\\epsilon` the opening sens of the reed: 1 (cane,\
        inwards) or -1 (lips, outwards)
    contact_stifness : float or callable
        :math:`Kc` : the stifness associated to the contact law when the reed is closed.
    contact_exponent : float or callable
        :math:`\\alpha` : the exponent associated to the contact law when the\
        reed is closed.
    opening : float or callable
        :math:`y_0` : the resting opening height of the reed (in m)
    closing_pressure: float or callable
        :math:`P_{closed}` the minimal pressure for which the reed is closed (in Pa)
    """

    NEEDED_PARAMS = ["gamma", "kappa",  "zeta", "pulsation", "qfactor",
                     "contact_stifness", "contact_exponent", "model"]
    """list of str: Needed parameters to instanciate the excitator"""

    def _update_fields(self, control_parameters):

        self.gamma = self._create_parameter(control_parameters["gamma"])

        # currently only constant value are accepted for other parameters
        # the numerical schemes are not compatible with varaible coefficients.

        self.zeta = self._create_cst_param(control_parameters["zeta"])
        self.kappa = self._create_cst_param(control_parameters["kappa"])
        self.pulsation = self._create_cst_param(control_parameters["pulsation"])
        self.qfactor = self._create_cst_param(control_parameters["qfactor"])
        self.contact_stifness =  self._create_cst_param(control_parameters["contact_stifness"])
        self.contact_exponent =  self._create_cst_param(control_parameters["contact_exponent"])

        # "opening" and "closing_pressure" are otpional as they do not influence the solution (excepting the scaling)
        if "opening" in control_parameters:
            self.opening = self._create_cst_param(control_parameters["opening"])
        else:
            self.opening = 1
        if "closing_pressure" in control_parameters:
            self.closing_pressure = self._create_cst_param(control_parameters["closing_pressure"])
        else:
            self.closing_pressure = 1

        # the value of epsilon is set by interpreting the keyword in "model"
        model = control_parameters['model']
        if model in ["lips","outwards"]:
            model_value = 1
        elif model in ["cane","inwards"]:
            model_value= -1
        else:
            warnings.warn("WARNING : your model is %s, but it must "
                  "be in {'lips', 'outwards', 'cane', 'inwards'}, it "
                  "will be set to default (lips)"
                  %model)
            model_value = 1
        self.model = FixedExcitatorParameter(model_value)


    @staticmethod
    def _create_cst_param(curve):
        if callable(curve):
            raise ValueError("Except 'mouth_pressure', evolving parameters of "
                             "Reed1dof Excitator are not supported yet, must be a"
                             " constant value")
        else:
            return FixedExcitatorParameter(curve)

    def get_dimensionfull_values(self, t, Zc, rho):
        """
        Return the values of all dimensionfull parameters at a given time:

        Parameters
        ----------
        t : float
            The given time we want to get the curves values from.
        Zc : float
            The characteristic (real) impedance at the entry of the instrument.
        rho : float
            the air density.

        Returns
        -------
        Sr : float
            the effective cross section area of the reed (in m²)
        Mr: float
            the effecitve mass of the read (in kg)
        g: float
            the damping coefficient
        omega02: float
             the squared resonant angular frequency
        w: float
            the effective width of the reed channel opening (in m)
        y0: float
            the resting opening of the reed (in m)
        epsilon: float
            1 (for lips/outwards) or -1 (cane/inwards) following the model
        pm: float
            the supply pressure (in Pa)
        """
        gamma, zeta, kappa, Qr, omegar, Kc, alpha_c, epsilon = self.get_dimensionless_values(t, Zc, rho)
        Pclosed = self.get_Pclosed(t)
        y0 = self.opening.get_value(t)

        pm = gamma*Pclosed
        w = zeta*np.sqrt(.5*rho*Pclosed)/(Zc*y0)
        Sr = kappa*Pclosed/(omegar*Zc*y0)

        Mr = Pclosed*Sr/(omegar**2 * y0)

        g = omegar/Qr

        omega02 = omegar**2

        omega_c = (Kc*omegar**2)**(1/(alpha_c + 1))
        return (Sr, Mr, g, omega02, w, y0, epsilon, pm, omega_c, alpha_c)


    def get_dimensionless_values(self, t, Zc=1, rho=1):
        """
        Return the values of all dimensionless parameters at a given time:

        Parameters
        ----------
        t : float
            The given time we want to get the curves values from.
        Zc : float, UNUSED
            The characteristic (real) impedance at the entry of the instrument.
        rho : float, UNUSED
            the air density.

        Returns
        -------
        gamma : float
            Dimensionless parameter relative to the supply pressure.
        zeta : float
            Dimensionless parameter relative to the reed opening.
        kappa : float
            The dimensionless parameter relative to the "reed flow".
        Qr : float
            the quality factor of the ree.
        omegar : float
            The resonant angular frequency of the reed in rad/s.
        Kc : float
            The contact force stifness.
        alpha_c : TYPE
            DESCRIPTION.
        epsilon : float
            1 (for lips/outwards) or -1 (cane/inwards) following the model.

        """
        gamma = self.gamma.get_value(t)
        zeta = self.zeta.get_value(t)
        kappa = self.kappa.get_value(t)
        omegar = self.pulsation.get_value(t)
        Qr = self.qfactor.get_value(t)
        Kc = self.contact_stifness.get_value(t)
        alpha_c = self.contact_exponent.get_value(t)
        epsilon = self.model.get_value(t)
        return gamma, zeta, kappa, Qr, omegar, Kc, alpha_c, epsilon

    def get_Pclosed(self, t):
        r"""
        Return the closing pressure of the reed.

        This value does not modify the response of the system. It is only necessary
        to rescale the results of the equations.

        .. math::
            P_{\text{closed}} = \frac{K_r }{S_r}  y_0 =  \omega_r^2 \frac{M_r}{S_r} y_0

        Parameters
        ----------
        t : float
            The given time we want to get the curves values from.

        Returns
        -------
        Pclosed : float
            The closing pressure in Pa.

        """
        return self.closing_pressure.get_value(t)
