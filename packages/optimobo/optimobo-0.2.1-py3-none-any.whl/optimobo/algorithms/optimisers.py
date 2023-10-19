
import numpy as np
from scipy.stats import qmc
from scipy.stats import norm
from scipy.optimize import differential_evolution
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.indicators.hv import HV
import GPy

import optimobo.util_functions as util_functions
import optimobo.result as result

GPy.plotting.change_plotting_library('matplotlib')

# from scalarisations import ExponentialWeightedCriterion, IPBI, PBI, Tchebicheff, WeightedNorm, WeightedPower, WeightedProduct, AugmentedTchebicheff, ModifiedTchebicheff


class MultiSurrogateOptimiser:
    """
    Class that allows optimisation of multi-objective problems using a multi-surrogate methodology.
    This method creates multiple probabalistic models, one for each objective.
    Constraints not supported.
    This is a generic implementation, so perfomance is limited when compared to specialised algorithms with
    extra features.

    Param:
        test_problem: problem to be solved.
        ideal_point: also known as the utopian point. is the smallest possible value of an objective vector
                in the objective space.
        max_point: the upper boundary of the objective space. The upper boundary for an objective vector.
    """

    def __init__(self, test_problem, ideal_point=None, max_point=None):
        self.test_problem = test_problem
        self.max_point = max_point
        self.ideal_point = ideal_point
        self.n_vars = test_problem.n_var
        self.n_obj = test_problem.n_obj
        self.upper = test_problem.xu
        self.lower = test_problem.xl
        if ideal_point is None:
            self.is_ideal_known = False
        else:
            self.is_ideal_known = True
        if max_point is None:
            self.is_max_known = False
        else:
            self.is_max_known = True


    def _objective_function(self, problem, x):
        """
        Wrapper for the objective function, makes my code clearer.
        Returns objective values.
        Params:
            problem: Problem object
            x: input 
        """
        return problem.evaluate(x)

    
    def _get_proposed_scalarisation(self, function, models, min_val, scalar_func, ref_dir, cache):
        """
        Function to retieve the next sample point.
        This is called when a scalarisation function is being used as an acquisition function.
        Params:
            function: acqusition function to optimise
            models: array of the models trained on each objective
            min_val: the best scalarisation value from the current population; according to the ref_dir and 
                the scalarisation function used. 
            scalar_func: the scalarisation function being used as a convergence measure in the acquisition
                function
            ref_dir: randomly selected weight vector (row vector)
            cache: the premade samples that will transformed over the mean and standard deviation of each
                proposed point.

        returns:
            res.x: solution of the optimisation
            res.fun: values of the objective function
            ref_dir: weights used.
        """
        def obj(X):
            # return -function(X, models, ref_dir, ideal_point, max_point, min_val, cache)
            return -function(X, models, ref_dir, scalar_func, min_val, cache)

        x = list(zip(self.lower, self.upper))
        res = differential_evolution(obj, x)
        return res.x, res.fun, ref_dir


    def _get_proposed_EHVI(self, function, models, ideal_point, max_point, pf, cache):
        """
        Function to retrieve the next sample point using EHVI.
        This is a seperate function to _get_proposed_scalarisation as the parameters are different.

        Params:
            function: acqusition function to optimise.
            models: array of the models trained on each objective.
            ideal_point: also known as the utopian point. is the smallest possible value of an objective vector
                in the objective space.
            max_point: the upper boundary of the objective space. The upper boundary for an objective vector.
            pf: pareto front approximation of the current population
            cache: the premade samples that will transformed over the mean and standard deviation of each
                proposed point.
        
        returns:
            res.x: solution of the optimisation
            res.fun: values of the objective function 

        """
        def obj(X):
            return -function(X, models, max_point, pf, cache)

        # x = [(bounds[0], bounds[1])] * n_var
        # x = list(zip(self.lower, self.upper))
        x = list(zip(self.test_problem.xl, self.test_problem.xu))

        res = differential_evolution(obj, x)
        return res.x, res.fun

    def _get_cached_samples(self, dimensions, sample_exponent):
        """
        Generates a selected number of normally distibuted sobol samples, these samples are transformed.
        This is done so that 
        
        dimensions:
            number of dimensions the samples are generated within
        sample_exponent:
            The number of samples generated is a power of 2. This param sets the exponent of 2.
        
        returns: a np array of arrays. Contains normally distributed sobol samples.
        """
        sampler = qmc.Sobol(d=dimensions, scramble=True)
        sample = sampler.random_base2(m=sample_exponent)
        

        norm_samples = [norm.ppf(sample[:,i]) for i in range(dimensions)]
        # cached_samples = np.asarray(list(zip(norm_samples1, norm_samples2)))
        cached_samples = np.asarray(list(zip(*norm_samples)))
        # import pdb; pdb.set_trace()
        return cached_samples

    
    def solve(self, budget=100, n_init_samples=5, sample_exponent=5, acquisition_func=None):
        """
        This fcontains the main algorithm to solve the optimisation problem.

        Params:
            budget: the number of expensive function evaluations used in the optimisation process, not including initial samples.
            
            display_pareto_front: bool. When set to true, a matplotlib plot will show the pareto front 
                approximation discovered by the optimiser.
            
            n_init_samples: the number of initial samples evaluated before optimisation occurs.

            acquisition_func: the acquisition function used to select the next sample points. 
                            If left default it calls Expected Hypervolume improvement
                            EHVI. Scalarisation functions can be used also;
                            options include: ExponentialWeightedCriterion, IPBI, PBI, Tchebicheff, 
                            WeightedNorm, WeightedPower, WeightedProduct, AugmentedTchebicheff, ModifiedTchebicheff
        

        Returns: Four lists in a tuple.
            pf_approx, solution vectors on the pareto front approximation found by the optimiser.
            pf_inputs, corresponding inputs to the values in pf_approx.
            ysample, output objective vectors of all evaluated samples.
            Xsample, all samples that were evaluated.
        """
        problem = self.test_problem

        # Initial samples.
        variable_ranges = list(zip(self.test_problem.xl, self.test_problem.xu))
        Xsample = util_functions.generate_latin_hypercube_samples(n_init_samples, variable_ranges)
        
        # Evaluate inital samples.
        ysample = np.asarray([self._objective_function(problem, x) for x in Xsample])

        # Create cached samples, this is to speed up computation in calculation of the acquisition functions.
        cached_samples = self._get_cached_samples(self.n_obj, sample_exponent)

        # Reference directions, one of these is radnomly selected every iteration, this promotes diverity.
        ref_dirs = get_reference_directions("das-dennis", self.n_obj, n_partitions=100)


        hypervolume_convergence = []

        for i in range(budget):

            # if no bounds are set this sets the upper and lower bounds
            if self.is_ideal_known is False and self.is_max_known is False:
                upper = np.zeros(self.n_obj)
                lower = np.zeros(self.n_obj)
                for i in range(self.n_obj):
                    upper[i] = max(ysample[:,i])
                    lower[i] = min(ysample[:,i])
                self.max_point = upper
                self.ideal_point = lower
                # change the bounds of the scalarisation object
                acquisition_func.set_bounds(lower, upper)
            elif self.is_ideal_known is False:
                lower = np.zeros(self.n_obj)
                for i in range(self.n_obj):
                    lower[i] = min(ysample[:,i])
                self.ideal_point = lower
                # change the bounds of the scalarisation object
                acquisition_func.set_bounds(lower, self.max_point)
            elif self.is_max_known is False: 
                upper = np.zeros(self.n_obj)
                for i in range(self.n_obj):
                    upper[i] = max(ysample[:,i])
                self.max_point = upper
                # change the bounds of the scalarisation object
                acquisition_func.set_bounds(self.ideal_point, upper)

            # Get hypervolume metric.
            ref_point = self.max_point
            HV_ind = HV(ref_point=ref_point)
            # import pdb; pdb.set_trace()
            hv = HV_ind(ysample)
            hypervolume_convergence.append(hv)

            # Create models for each objective.
            models = []
            for i in range(problem.n_obj):
                ys = np.reshape(ysample[:,i], (-1,1))
                model = GPy.models.GPRegression(Xsample,ys, GPy.kern.Matern52(self.n_vars,ARD=True))


                model.Gaussian_noise.variance.fix(0)
                model.optimize(messages=False,max_f_eval=1000)
                models.append(model)

            # With each iteration we select a random weight vector, this is to improve diversity.
            ref_dir = np.asarray(ref_dirs[np.random.randint(0,len(ref_dirs))])

            # Retrieve the next sample point.
            X_next = None
            X_next = None
            min_scalar = None
            pf = None
            if acquisition_func is None:
                pf = util_functions.calc_pf(ysample)
                # import pdb; pdb.set_trace()

                if problem.n_obj == 2:
                    X_next, _, = self._get_proposed_EHVI(util_functions.EHVI, models, self.ideal_point, self.max_point, pf, cached_samples)
                else:
                    X_next, _, = self._get_proposed_EHVI(util_functions.EHVI_3D, models, self.ideal_point, self.max_point, pf, cached_samples)
            else:
                min_scalar =  np.min([acquisition_func(y, ref_dir) for y in ysample])
                # print(min_scalar)
                X_next, _, _ = self._get_proposed_scalarisation(util_functions.expected_decomposition, models, min_scalar, acquisition_func, ref_dir, cached_samples)


            # Evaluate the next input.
            y_next = self._objective_function(problem, X_next)

            # Add the new sample.
            ysample = np.vstack((ysample, y_next))

            # Update archive.
            Xsample = np.vstack((Xsample, X_next))


        pf_approx = util_functions.calc_pf(ysample)


        # Identify the inputs that correspond to the pareto front solutions.
        indicies = []
        for i, item in enumerate(ysample):
            if item in pf_approx:
                indicies.append(i)
        pf_inputs = Xsample[indicies]

        res = result.Res(pf_approx, pf_inputs, ysample, Xsample, hypervolume_convergence, problem.n_obj, n_init_samples)

        return res
        # return pf_approx, pf_inputs, ysample, Xsample, hypervolume_convergence




class MonoSurrogateOptimiser:
    """
    Class that enables optimisation of multi-objective problems using a mono-surrogate methodology.
    Mono-surrogate method aggregates multiple objectives into a single scalar value, this then allows optimisation of
    a multi-objective problem with a single probabalistic model.

    Param:
        test_problem: problem to be solved. Defined via pymoo.
    ideal_point: also known as the utopian point. is the smallest possible value of an objective vector
            in the objective space.
    max_point: the upper boundary of the objective space. The upper boundary for an objective vector.
    """
    def __init__(self, test_problem, ideal_point=None, max_point=None):
        self.test_problem = test_problem
        # self.aggregation_func = aggregation_func
        self.max_point = max_point
        self.ideal_point = ideal_point
        self.n_vars = test_problem.n_var
        self.n_obj = test_problem.n_obj
        self.upper = test_problem.xu
        self.lower = test_problem.xl
        if ideal_point is None:
            self.is_ideal_known = False
        else:
            self.is_ideal_known = True
        if max_point is None:
            self.is_max_known = False
        else:
            self.is_max_known = True


    def _objective_function(self, problem, x):
        """
        Wrapper for the objective function, makes my code clearer.
        Returns objective values.

        Params:
            problem: Problem object
            x: input 
        """
        return problem.evaluate(x)

    def _expected_improvement(self, X, model, opt_value, kappa=0.01):
        """
        EI, single objective acquisition function.

        Returns:
            EI: The Expected improvement of X over the opt_value given the information
                from the model.
        """

        # get the mean and s.d. of the proposed point
        X_aux = X.reshape(1, -1)
        mu_x, sigma_x = model.predict(X_aux)
        # is the variance therefore we need the square root it
        sigma_x = np.sqrt(sigma_x)
        mu_x = mu_x[0]
        sigma_x = sigma_x[0]

        gamma_x = (opt_value - mu_x) / (sigma_x + 1e-10)
        ei = sigma_x * (gamma_x * norm.cdf(gamma_x) + norm.pdf(gamma_x))
        return ei.flatten()        

    def _get_proposed(self, function, models, current_best):
        """
        Helper function to optimise the acquisition function. This is to identify the next sample point.

        Params:
            function: The acquisition function to be optimised.
            models: The model trained on the aggregated values.
            current_best: Best/most optimal solution found thus far.

        Returns:
            res.x: solution of the optimsiation.
            res.fun: function value of the optimisation.
        """

        def obj(X):
            # print("obj called")
            return -function(X, models, current_best)

        x = list(zip(self.test_problem.xl, self.test_problem.xu))

        res = differential_evolution(obj, x)
        return res.x, res.fun

    def _normalize_data(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    
    def solve(self, aggregation_func, budget=100, n_init_samples=5):
        """
        This function contains the main flow of the multi-objective optimisation algorithm. This function attempts
        to solve the MOP.

        Params:
            budget: the number of expensive function evaluations used in the optimisation process, not including initial samples.

            display_pareto_front: bool. When set to true, a matplotlib plot will show the pareto front approximation discovered by the optimiser.

            n_init_samples: the number of initial samples evaluated before optimisation occurs.

            aggregation_func: the aggregation function used to aggregate the objective vectors in a single scalar value. 
            Scalarisations are used. Options Include: ExponentialWeightedCriterion, IPBI, PBI, Tchebicheff, WeightedNorm, WeightedPower, WeightedProduct, AugmentedTchebicheff, ModifiedTchebicheff
            Imported from scalarisations.py

        
        Returns: Four lists in a tuple.
            pf_approx, solution vectors on the pareto front approximation found by the optimiser.
            pf_inputs, corresponding inputs to the values in pf_approx.
            ysample, output objective vectors of all evaluated samples.
            Xsample, all samples that were evaluated.
        """

        
        # ref_dirs = get_reference_directions("das-dennis", 2, n_partitions=12)
        problem = self.test_problem

        # 1/n_obj * 
        # initial weights are all the same
        weights = np.asarray([1/problem.n_obj]*problem.n_obj)

        # get the initial samples used to build first model
        # use latin hypercube sampling
        variable_ranges = list(zip(self.test_problem.xl, self.test_problem.xu))
        Xsample = util_functions.generate_latin_hypercube_samples(n_init_samples, variable_ranges)

        # Evaluate inital samples.
        
        ysample = np.asarray([self._objective_function(problem, x) for x in Xsample])
        # if no bounds are set this sets the upper and lower bounds
        if self.is_ideal_known is False and self.is_max_known is False:
            upper = np.zeros(self.n_obj)
            lower = np.zeros(self.n_obj)
            for i in range(self.n_obj):
                upper[i] = max(ysample[:,i])
                lower[i] = min(ysample[:,i])
            self.max_point = upper
            self.ideal_point = lower
            # change the bounds of the scalarisation object
            aggregation_func.set_bounds(lower, upper)
        elif self.is_ideal_known is False:
            lower = np.zeros(self.n_obj)
            for i in range(self.n_obj):
                lower[i] = min(ysample[:,i])
            self.ideal_point = lower
            # change the bounds of the scalarisation object
            aggregation_func.set_bounds(lower, self.max_point)
        elif self.is_max_known is False: 
            upper = np.zeros(self.n_obj)
            for i in range(self.n_obj):
                upper[i] = max(ysample[:,i])
            self.max_point = upper
            # change the bounds of the scalarisation object
            aggregation_func.set_bounds(self.ideal_point, upper)
        




        aggregated_samples = np.asarray([aggregation_func(i, weights) for i in ysample]).flatten()
        ys= np.reshape(aggregated_samples, (-1,1))

        # Build initial model
        kern = GPy.kern.Matern52(self.n_vars,ARD=True)
        model = GPy.models.GPRegression(Xsample, ys, kern)

        model.Gaussian_noise.variance.fix(0)
        model.optimize(messages=False,max_f_eval=1000)

        ref_dirs = get_reference_directions("das-dennis", problem.n_obj, n_partitions=100)
        hypervolume_convergence = []

        for i in range(budget):

            # if no bounds are set this sets the upper and lower bounds
            if self.is_ideal_known is False and self.is_max_known is False:
                upper = np.zeros(self.n_obj)
                lower = np.zeros(self.n_obj)
                for i in range(self.n_obj):
                    upper[i] = max(ysample[:,i])
                    lower[i] = min(ysample[:,i])
                self.max_point = upper
                self.ideal_point = lower
                # change the bounds of the scalarisation object
                aggregation_func.set_bounds(lower, upper)
            elif self.is_ideal_known is False:
                lower = np.zeros(self.n_obj)
                for i in range(self.n_obj):
                    lower[i] = min(ysample[:,i])
                self.ideal_point = lower
                # change the bounds of the scalarisation object
                aggregation_func.set_bounds(lower, self.max_point)
            elif self.is_max_known is False: 
                upper = np.zeros(self.n_obj)
                for i in range(self.n_obj):
                    upper[i] = max(ysample[:,i])
                self.max_point = upper
                # change the bounds of the scalarisation object
                aggregation_func.set_bounds(self.ideal_point, upper)

            # Hypervolume performance.
            ref_point = self.max_point
            HV_ind = HV(ref_point=ref_point)
            hv = HV_ind(ysample)
            hypervolume_convergence.append(hv)

            # Identify the current best sample, used for search.
            current_best = aggregated_samples[np.argmin(aggregated_samples)]
            
            # Reconstruct model.
            model = GPy.models.GPRegression(Xsample, np.reshape(aggregated_samples, (-1,1)), GPy.kern.Matern52(self.n_vars,ARD=True))
            model.Gaussian_noise.variance.fix(0)
            model.optimize(messages=False,max_f_eval=1000)

            # use the model, current best to get the next x value to evaluate.
            next_X, _ = self._get_proposed(self._expected_improvement, model, current_best)

            # Evaluate that point to get its objective values.
            next_y = self._objective_function(problem, next_X)

            # add the new sample to archive.
            ysample = np.vstack((ysample, next_y))

            ref_dir = ref_dirs[np.random.randint(0,len(ref_dirs))]

            # Aggregate new sample
            agg = aggregation_func(next_y, ref_dir)

            # Update archive.
            aggregated_samples = np.append(aggregated_samples, agg)          
            Xsample = np.vstack((Xsample, next_X))
        
        pf_approx = util_functions.calc_pf(ysample)

        # Find the inputs that correspond to the pareto front.
        indicies = []
        for i, item in enumerate(ysample):
            if item in pf_approx:
                indicies.append(i)
        pf_inputs = Xsample[indicies]

        res = result.Res(pf_approx, pf_inputs, ysample, Xsample, hypervolume_convergence, problem.n_obj, n_init_samples)

        return res
        # return pf_approx, pf_inputs, ysample, Xsample, hypervolume_convergence


