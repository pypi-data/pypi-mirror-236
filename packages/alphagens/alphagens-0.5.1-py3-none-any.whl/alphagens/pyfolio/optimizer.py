from abc import ABC, abstractmethod
import numpy as np
from scipy.optimize import minimize


class BaseOptimizer(ABC):
 
    def __init__(self, mu, cov):
        assert len(mu) == len(cov)
        assert isinstance(mu, np.ndarray)
        assert isinstance(cov, np.ndarray)
        self.mu = mu
        self.cov = cov
        self.solution = None
        self.n_assets = len(self.mu)
    
    @abstractmethod
    def objective_function(self, weights):
        raise NotImplementedError("should implement in the derived class")

    @abstractmethod
    def constraints(self):
        raise NotImplementedError("should implement in the derived class")
    
    @abstractmethod
    def bounds(self):
        return tuple((0, 1) for _ in range(self.n_assets))

    def _optimize(self):
        self.solution = minimize(
            lambda weights: self.objective_function(weights), 
            self.initial_guess(), 
            method='SLSQP', 
            bounds=self.bounds(), 
            constraints=self.constraints()
            )

    def get_optimal_weights(self):
        return self.solution.x

    def initial_guess(self):
        init = np.random.uniform(0, 1, size=self.n_assets)
        return init / np.sum(init)
    
    def run(self):
        self._optimize()
        if self.solution.x is None:
            return "FAILED"
        else:
            return "SUCCESS"

    def __call__(self):
        self._optimize()
        if self.solution.x is None:
            return "FAILED"
        else:
            return "SUCCESS"
    

class MinVarPortfolio(BaseOptimizer):

    def __init__(self, mu, cov):
        super().__init__(mu, cov)
    
    def objective_function(self, weights):
        mu = self.mu
        cov = self.cov
        portfolio_mean = weights.T @ mu
        portfolio_variance = weights.T @ cov @ weights
        max_obj = - portfolio_variance
        return - max_obj

    def constraints(self):
        constraints_list = []


        return ({'type': 'eq', 
                 'fun': lambda weights: np.sum(weights) - 1})
    
    def bounds(self):
        bounds_list = []
        for i in range(self.n_assets):
            upper_bound = 1
            lower_bound = 0
            bounds_list.append((lower_bound, upper_bound))
        return tuple(bounds_list)


class MeanVarPortfolio(BaseOptimizer):

    def __init__(self, mu, cov, target_return):
        super().__init__(mu, cov)
        self.target_return = target_return

    def objective_function(self, weights):
        portfolio_mean = weights.T @ self.mu
        portfolio_variance = weights.T @ self.cov @ weights
        max_obj = - portfolio_variance
        return - max_obj

    def constraints(self):
        return ({'type': 'eq', 
                 'fun': lambda weights: np.sum(weights) - 1},
                {'type': 'eq',
                 'fun': lambda weights: weights.T @ self.mu - self.target_return})
    
    def bounds(self):
        bounds = []
        for i in range(self.n_assets):
            upper_bound = 1
            lower_bound = 0
            bounds.append((lower_bound, upper_bound))
        return tuple(bounds)
    

class QuadraticUtilityPortfolio(BaseOptimizer):
    def __init__(self, mu, cov, penalty):
        super().__init__(mu, cov)
        self.penalty = penalty

    def objective_function(self, weights):
        portfolio_mean = weights.T @ self.mu
        portfolio_variance = weights.T @ self.cov @ weights
        max_obj =  portfolio_mean - 0.5 * self.penalty * portfolio_variance
        return - max_obj

    def constraints(self):
        return ({'type': 'eq', 
                 'fun': lambda weights: np.sum(weights) - 1})
    
    def bounds(self):
        return tuple((0, 1) for _ in range(self.n_assets))


class CustomTypeA(BaseOptimizer):

    def __init__(self, 
        mu: np.ndarray, 
        cov: np.ndarray, 
        penalty: float, 
        scores: np.ndarray,
        component_weights: np.ndarray,
        industry_dummies: np.ndarray,
    ):
        """Custom type optimizer

        Parameters
        ----------
        mu : np.ndarray
            The mean returns
        cov : np.ndarray
            The covariance of returns
        penalty : float
            The Risk aversion coefficient
        scores : np.ndarray
            Factor Exposures
        component_weights : np.ndarray
            The weights of the components of an index
        industry_dummies : np.ndarray

        Raises
        ------
        None
        
        Notes
        -----
        None

        """
        super().__init__(mu, cov)
        self.penalty = penalty
        self.scores = scores
        self.component_weights = component_weights
        self.industry_dummies = industry_dummies
    
    def objective_function(self, omega):
        mu = self.mu
        cov = self.cov
        portfolio_mean = omega.T @ mu
        portfolio_variance = omega.T @ cov @ omega
        max_obj = omega.T @ self.scores - self.penalty * portfolio_variance
        return - max_obj

    def constraints(self):
        upper_limit = 0.1
        constraints_list = []

        def constraint1(omega):
            return np.sum(omega) - 1
        
        constraints_list.append({'type': 'eq', "fun": constraint1})

        for j in range(self.industry_dummies.shape[1]):
            industry_dummy = self.industry_dummies[:, j] 
            def aux_func(omega):
                result = np.abs(np.dot(omega - self.component_weights, industry_dummy)) - upper_limit
                return -result

            constraints_list.append({'type': 'ineq', "fun": aux_func})

        return constraints_list
    
    def bounds(self):
        result = []
        upper_bound = 0.02
        for i in range(self.n_assets):
            bound_i_up = self.component_weights[i] + upper_bound
            bound_i_down = max(self.component_weights[i] - upper_bound, 0)
            result.append((bound_i_down, bound_i_up))
        return tuple(result)