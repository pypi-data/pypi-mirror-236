"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy
import time
from typing import Callable

from systemID.core.algorithms.eigensystem_realization_algorithm import eigensystem_realization_algorithm
from systemID.core.algorithms.eigensystem_realization_algorithm_with_data_correlation import eigensystem_realization_algorithm_with_data_correlation
from systemID.core.algorithms.eigensystem_realization_algorithm_from_initial_condition_response import eigensystem_realization_algorithm_from_initial_condition_response
from systemID.core.algorithms.eigensystem_realization_algorithm_with_data_correlation_from_initial_condition_response import eigensystem_realization_algorithm_with_data_correlation_from_initial_condition_response

from systemID.core.algorithms.time_varying_eigensystem_realization_algorithm_from_initial_condition_response import time_varying_eigensystem_realization_algorithm_from_initial_condition_response
from systemID.core.algorithms.time_varying_eigensystem_realization_algorithm import time_varying_eigensystem_realization_algorithm

from systemID.core.algorithms.observer_kalman_identification_algorithm import observer_kalman_identification_algorithm
from systemID.core.algorithms.observer_kalman_identification_algorithm_with_observer import observer_kalman_identification_algorithm_with_observer
from systemID.core.algorithms.markov_parameters_from_observer_markov_parameters import markov_parameters_from_observer_markov_parameters

from systemID.core.algorithms.time_varying_observer_kalman_identification_algorithm_with_observer import time_varying_observer_kalman_identification_algorithm_with_observer

from systemID.core.functions.propagate import propagate_discrete_ss_model
from systemID.core.functions.augment_data import augment_data_with_polynomial_basis_functions



class model:

    def __init__(self,
                 model_type: str,
                 output_dimension: int = None,
                 input_dimension: int = None,
                 parameter_dimension: int = None):

        model_types = ['linear', 'bilinear', 'nonlinear']
        if model_type not in model_types:
            raise ValueError("model_type must be one of {}".format(model_types))
        self.model_type = model_type

        if output_dimension is not None and (not isinstance(output_dimension, int) or output_dimension <= 0):
            raise ValueError("output_dimension must be a positive integer")
        self.output_dimension = output_dimension

        if input_dimension is not None and (not isinstance(input_dimension, int) or input_dimension <= 0):
            raise ValueError("input_dimension must be a positive integer")
        self.input_dimension = input_dimension

        if parameter_dimension is not None and (not isinstance(parameter_dimension, int) or parameter_dimension <= 0):
            raise ValueError("parameter_dimension must be a positive integer")
        self.parameter_dimension = parameter_dimension

class discrete_ss_model(model):

    def __init__(self,
                 model_type: str,
                 dt: float,
                 state_dimension: int,
                 input_dimension: int = None,
                 output_dimension: int = None,
                 parameter_dimension: int = None,
                 A: Callable[[float], numpy.ndarray] = None,
                 N: Callable[[float], numpy.ndarray] = None,
                 B: Callable[[float], numpy.ndarray] = None,
                 C: Callable[[float], numpy.ndarray] = None,
                 D: Callable[[float], numpy.ndarray] = None,
                 F: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None,
                 G: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None
    ):
        super().__init__(model_type, output_dimension, input_dimension, parameter_dimension)

        if not isinstance(dt, float) or dt <= 0:
            raise ValueError("dt must be a positive float")
        self.dt = dt

        if not isinstance(state_dimension, int) or state_dimension <= 0:
            raise ValueError("state_dimension must be a positive integer")
        self.state_dimension = state_dimension

        if A is not None and not (isinstance(A, Callable) and isinstance(A(0), numpy.ndarray) and A(0).shape == (self.state_dimension, self.state_dimension)):
            raise ValueError("A must be a callable function that returns a numpy.ndarray of shape (state_dimension, state_dimension)")
        self.A = A

        if N is not None and not (isinstance(N, Callable) and isinstance(N(0), numpy.ndarray) and N(0).shape == (self.state_dimension, self.state_dimension)):
            raise ValueError("N must be a callable function that returns a numpy.ndarray of shape (state_dimension, state_dimension)")
        self.N = N

        if B is not None and not (isinstance(B, Callable) and isinstance(B(0), numpy.ndarray) and B(0).ndim == 2 and B(0).shape[0] == self.state_dimension):
            raise ValueError("B must be a callable function that returns a numpy.ndarray of shape (state_dimension, input_dimension)")
        self.B = B
        if B is not None:
            self.input_dimension = B(0).shape[1]

        if C is not None and not (isinstance(C, Callable) and isinstance(C(0), numpy.ndarray) and C(0).ndim == 2 and C(0).shape[1] == self.state_dimension):
            raise ValueError("C must be a callable function that returns a numpy.ndarray of shape (output_dimension, state_dimension)")
        self.C = C
        if C is not None:
            self.output_dimension = C(0).shape[0]

        if D is not None and not (isinstance(D, Callable) and isinstance(D(0), numpy.ndarray) and D(0).ndim == 2):
            raise ValueError("D must be a callable function that returns a numpy.ndarray of shape (output_dimension, input_dimension)")
        self.D = D
        if D is not None:
            self.output_dimension, self.input_dimension = D(0).shape

        if F is not None and not isinstance(F, Callable):
            raise ValueError("F must be a callable function that returns a numpy.ndarray of shape (state_dimension,)")
        self.F = F

        if G is not None and not isinstance(G, Callable):
            raise ValueError("G must be a callable function that returns a numpy.ndarray of shape (output_dimension,)")
        self.G = G


    # Funcion for LTI fit
    def lti_fit(self,
                output_data: numpy.ndarray,
                input_data: numpy.ndarray = None,
                parameter_data: numpy.ndarray = None,
                number_markov_parameters: int = None,
                observer_order: int = None,
                stable_order: int = None,
                p: int = None,
                q: int = None,
                xi: int = None,
                zeta: int = None,
                tau: int = None,
                lifting_order: int = 1,
                data_correlations: bool = False
    ):

        t = time.time()
        self.fit_config = {}

        if not isinstance(output_data, numpy.ndarray) or \
           output_data.ndim != 3 or \
            (self.output_dimension is not None and output_data.shape[0] != self.output_dimension):
            raise ValueError("output_data must be a numpy.ndarray of shape (output_dimension, number_steps, number_experiments)")
        self.fit_config['output_data'] = output_data
        self.output_dimension = output_data.shape[0]
        self.fit_config['number_steps'] = output_data.shape[1]
        self.fit_config['number_experiments'] = output_data.shape[2]

        if input_data is not None and not (isinstance(input_data, numpy.ndarray) and input_data.ndim == 3) or \
           input_data is not None and self.input_dimension is not None and input_data.shape[0] != self.input_dimension or \
           input_data is not None and (input_data.shape[1] != self.fit_config['number_steps'] or input_data.shape[2] != self.fit_config['number_experiments']):
            raise ValueError("input_data must be a numpy.ndarray of shape (input_dimension, number_steps, number_experiments)")
        self.fit_config['input_data'] = input_data
        if input_data is not None:
            self.input_dimension = input_data.shape[0]

        self.fit_config['parameter_data'] = parameter_data
        if self.fit_config['parameter_data'] is not None:
            self.parameter_dimension = parameter_data.shape[0]
        self.fit_config['number_markov_parameters'] = number_markov_parameters
        self.fit_config['observer_order'] = observer_order

        if stable_order is None:
            self.fit_config['stable_order'] = 0
        else:
            self.fit_config['stable_order'] = stable_order


        self.fit_config['p'] = p
        self.fit_config['q'] = q
        self.fit_config['xi'] = xi
        self.fit_config['zeta'] = zeta
        self.fit_config['tau'] = tau
        self.fit_config['lifting_order'] = lifting_order
        self.fit_config['data_correlations'] = data_correlations

        if lifting_order > 1:
            self.fit_config['output_data'] = augment_data_with_polynomial_basis_functions(data=self.fit_config['output_data'],
                                                                                          order=lifting_order,
                                                                                          max_order=lifting_order)
            self.state_dimension = self.fit_config['output_data'].shape[0]
            self.output_dimension = self.fit_config['output_data'].shape[0]


        if self.fit_config['input_data'] is None:
            if self.fit_config['data_correlations']:
                era_ic = eigensystem_realization_algorithm_with_data_correlation_from_initial_condition_response(output_data=self.fit_config['output_data'],
                                                                                                                 state_dimension=self.state_dimension,
                                                                                                                 p=self.fit_config['p'],
                                                                                                                 q=self.fit_config['q'],
                                                                                                                 xi=self.fit_config['xi'],
                                                                                                                 zeta=self.fit_config['zeta'],
                                                                                                                 tau=self.fit_config['tau'])
                self.fit_config.update(era_ic)
                self.A = self.fit_config['A']
                self.C = self.fit_config['C']

            else:
                era_ic = eigensystem_realization_algorithm_from_initial_condition_response(output_data=self.fit_config['output_data'],
                                                                                           state_dimension=self.state_dimension,
                                                                                           p=self.fit_config['p'],
                                                                                           q=self.fit_config['q'])
                self.fit_config.update(era_ic)
                self.A = self.fit_config['A']
                self.C = self.fit_config['C']

        else:
            if observer_order is None:
                okid = observer_kalman_identification_algorithm(input_data=self.fit_config['input_data'],
                                                                output_data=self.fit_config['output_data'],
                                                                number_markov_parameters=self.fit_config['number_markov_parameters'],
                                                                stable_order=self.fit_config['stable_order'])
            else:
                okid = observer_kalman_identification_algorithm_with_observer(input_data=self.fit_config['input_data'],
                                                                              output_data=self.fit_config['output_data'],
                                                                              observer_order=self.fit_config['observer_order'],
                                                                              stable_order=self.fit_config['stable_order'])

                markov_parameters = markov_parameters_from_observer_markov_parameters(observer_markov_parameters=okid['observer_markov_parameters'],
                                                                                      number_markov_parameters=self.fit_config['number_markov_parameters'])

                self.fit_config.update(markov_parameters)

            self.fit_config.update(okid)

            if self.fit_config['data_correlations']:
                era = eigensystem_realization_algorithm_with_data_correlation(markov_parameters=self.fit_config['markov_parameters'],
                                                                              state_dimension=self.state_dimension,
                                                                              p=self.fit_config['p'],
                                                                              q=self.fit_config['q'],
                                                                              xi=self.fit_config['xi'],
                                                                              zeta=self.fit_config['zeta'],
                                                                              tau=self.fit_config['tau'])
                self.fit_config.update(era)
                self.A = self.fit_config['A']
                self.B = self.fit_config['B']
                self.C = self.fit_config['C']
                self.D = self.fit_config['D']

            else:
                era = eigensystem_realization_algorithm(markov_parameters=self.fit_config['markov_parameters'],
                                                        state_dimension=self.state_dimension,
                                                        p=self.fit_config['p'],
                                                        q=self.fit_config['q'])
                self.fit_config.update(era)
                self.A = self.fit_config['A']
                self.B = self.fit_config['B']
                self.C = self.fit_config['C']
                self.D = self.fit_config['D']

        self.fit_config['Training time'] = time.time() - t




    # Function for LTV fit
    def ltv_fit(self,
                forced_response_output_data: numpy.ndarray = None,
                input_data: numpy.ndarray = None,
                free_response_output_data: numpy.ndarray = None,
                parameter_data: numpy.ndarray = None,
                observer_order: int = None,
                p: int = None,
                q: int = None,
                lifting_order: int = 1,
                data_correlations: bool = False,
                max_time_step: int = None,
                apply_transformation: bool = True,
                show_progress: bool = False
                ):

        t = time.time()
        self.fit_config = {}

        # if not isinstance(forced_response_output_data, numpy.ndarray) or \
        #         forced_response_output_data.ndim != 3 or \
        #         self.output_dimension is not None and forced_response_output_data.shape[0] != self.output_dimension:
        #     raise ValueError(
        #         "output_data must be a numpy.ndarray of shape (output_dimension, number_steps, number_experiments)")
        self.fit_config['forced_response_output_data'] = forced_response_output_data
        if forced_response_output_data is not None:
            self.output_dimension = forced_response_output_data.shape[0]
            self.fit_config['number_steps'] = forced_response_output_data.shape[1]
            self.fit_config['number_experiments'] = forced_response_output_data.shape[2]

        if input_data is not None and not (isinstance(input_data, numpy.ndarray) and input_data.ndim == 3) or \
                input_data is not None and self.input_dimension is not None and input_data.shape[
            0] != self.input_dimension or \
                input_data is not None and (
                input_data.shape[1] != self.fit_config['number_steps'] or input_data.shape[2] != self.fit_config[
            'number_experiments']):
            raise ValueError(
                "input_data must be a numpy.ndarray of shape (input_dimension, number_steps, number_experiments)")
        self.fit_config['input_data'] = input_data
        if input_data is not None:
            self.input_dimension = input_data.shape[0]

        self.fit_config['free_response_output_data'] = free_response_output_data
        self.output_dimension = free_response_output_data.shape[0]
        self.fit_config['number_steps'] = free_response_output_data.shape[1]
        self.fit_config['number_experiments'] = free_response_output_data.shape[2]

        self.fit_config['parameter_data'] = parameter_data
        if self.fit_config['parameter_data'] is not None:
            self.parameter_dimension = parameter_data.shape[0]
        self.fit_config['observer_order'] = observer_order
        self.fit_config['p'] = p
        self.fit_config['q'] = q
        self.fit_config['lifting_order'] = lifting_order
        self.fit_config['data_correlations'] = data_correlations
        self.fit_config['max_time_step'] = max_time_step
        self.fit_config['apply_transformation'] = apply_transformation
        self.fit_config['show_progress'] = show_progress

        if self.fit_config['input_data'] is None:
            tvera_ic = time_varying_eigensystem_realization_algorithm_from_initial_condition_response(output_data=self.fit_config['free_response_output_data'],
                                                                                                      state_dimension=self.state_dimension,
                                                                                                      dt=self.dt,
                                                                                                      p=self.fit_config['p'],
                                                                                                      max_time_step=self.fit_config['max_time_step'])
            self.fit_config.update(tvera_ic)
            self.A = self.fit_config['A']
            self.C = self.fit_config['C']

        else:
            tvokid = time_varying_observer_kalman_identification_algorithm_with_observer(input_data=self.fit_config['input_data'],
                                                                                         output_data=self.fit_config['forced_response_output_data'],
                                                                                         observer_order=self.fit_config['observer_order'])

            self.fit_config.update(tvokid)

            tvera = time_varying_eigensystem_realization_algorithm(hki=self.fit_config['hki'],
                                                                   D=self.fit_config['D'],
                                                                   state_dimension=self.state_dimension,
                                                                   dt=self.dt,
                                                                   free_response_data=self.fit_config['free_response_output_data'],
                                                                   p=self.fit_config['p'],
                                                                   q=self.fit_config['q'],
                                                                   apply_transformation=self.fit_config['apply_transformation'],
                                                                   show_progress=self.fit_config['show_progress'])
            self.fit_config.update(tvera)
            self.A = self.fit_config['A']
            self.B = self.fit_config['B']
            self.C = self.fit_config['C']
            self.D = self.fit_config['D']





        self.fit_config['Training time'] = time.time() - t


    def predict(self,
                number_steps: numpy.ndarray,
                x0: numpy.ndarray = None,
                input_data: numpy.ndarray = None,
                parameter_data: numpy.ndarray = None
                ):

        if (x0 is None) and (input_data is None) and (parameter_data is None):
            raise ValueError('x0, input_data and parameters_data cannot all be None')
        else:
            if x0 is None:
                x0 = (self.fit_config['X0']@numpy.linalg.pinv(self.fit_config['parameter_data']))@parameter_data

            y, x = propagate_discrete_ss_model(model=self,
                                               number_steps=number_steps,
                                               x0=x0,
                                               input_data=input_data)

        return y, x






