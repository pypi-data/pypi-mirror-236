"""
author: Fabian Schaipp
"""
import numpy as np
from numpy.testing import assert_array_almost_equal

from gglasso.helper.data_generation import time_varying_power_network, group_power_network, sample_covariance_matrix, generate_precision_matrix
from gglasso.problem import glasso_problem
from gglasso.helper.ext_admm_helper import construct_trivial_G
from gglasso.helper.basic_linalg import scale_array_by_diagonal

p = 20
K = 3
N = 1000
M = 4

###############################################################
### TEST MGL
###############################################################

def template_problem_MGL(S, N, reg = 'GGL', latent = False, G = None):
    """
    template for testing the MGL problem object
    """
    P = glasso_problem(S = S, N = N, reg = reg, latent = latent, G = G)
    print(P)
    
    modelselectparams = dict()
    modelselectparams['lambda1_range'] = np.logspace(-3,0,4)
    modelselectparams['lambda2_range'] = np.logspace(-1,-3,3)
              
    if latent:
        modelselectparams['mu1_range'] = np.logspace(-2,0,4)
    else:
        modelselectparams['mu1_range'] = None
    
    
    reg_params = {'lambda1': 0.01, 'lambda2': 0.001}
    if latent:
        reg_params['mu1'] = 1.
    
    # set reg params and solve again
    P.set_reg_params(reg_params)
    P.solve(verbose = True)
    
    # test model selection
    P.model_selection(method = 'AIC')
    P.model_selection(modelselect_params = modelselectparams, method = 'eBIC', gamma = 0.1)
    
    #tmp = P.modelselect_stats.copy()
    _ = P.solution.calc_ebic(gamma = 0.1)
    P.solution.calc_adjacency()
    
    return P

def test_GGL():
    Sigma, Theta = group_power_network(p, K, M)    
    S, samples = sample_covariance_matrix(Sigma, N)
    _ = template_problem_MGL(S, N, reg = 'GGL', latent = False)   
    return

def test_GGL_latent():
    Sigma, Theta = group_power_network(p, K, M)    
    S, samples = sample_covariance_matrix(Sigma, N)
    _ = template_problem_MGL(S, N, reg = 'GGL', latent = True)
    return

def test_FGL():
    Sigma, Theta = time_varying_power_network(p, K, M)
    S, samples = sample_covariance_matrix(Sigma, N)
    _ = template_problem_MGL(S, N, reg = 'FGL', latent = False)
    return

def test_FGL_latent():
    Sigma, Theta = time_varying_power_network(p, K, M)
    S, samples = sample_covariance_matrix(Sigma, N)
    _ = template_problem_MGL(S, N, reg = 'FGL', latent = True)
    return

def test_GGL_ext():
    Sigma, Theta = group_power_network(p, K, M)
    S, samples = sample_covariance_matrix(Sigma, N)
    
    Sdict = dict()
    for k in np.arange(K):
        Sdict[k] = S[k,:,:].copy()
        
    G = construct_trivial_G(p, K)
    _ = template_problem_MGL(Sdict, N, reg = 'GGL', latent = False, G = G)
    return

def test_GGL_ext_latent():
    Sigma, Theta = group_power_network(p, K, M)
    S, samples = sample_covariance_matrix(Sigma, N)
    
    Sdict = dict()
    for k in np.arange(K):
        Sdict[k] = S[k,:,:].copy()
        
    G = construct_trivial_G(p, K)
    _ = template_problem_MGL(Sdict, N, reg = 'GGL', latent = True, G = G)
    return

###############################################################
### TEST SGL
###############################################################

def template_problem_SGL(S, N, latent = False):
    """
    template for testing the SGL problem object
    """
    P = glasso_problem(S = S, N = N, reg = None, latent = latent)
    print(P)
    

    reg_params = {'lambda1': 0.01}
    if latent:
        reg_params['mu1'] = 1.
    
    # set reg params and solve again
    P.set_reg_params(reg_params)
    P.solve()
    
    # test model selection    
    P.model_selection(method = 'AIC')
    P.model_selection(modelselect_params = None, method = 'eBIC', gamma = 0.1)
    
    #tmp = P.modelselect_stats.copy()
    _ = P.solution.calc_ebic(gamma = 0.1)
    P.solution.calc_adjacency()
    return P

def test_SGL():
    Sigma, Theta = group_power_network(p, K = 1, M = 2, seed = 1234)
    S, samples = sample_covariance_matrix(Sigma, N, seed = 1234); S = S[0,:,:]  
    P = template_problem_SGL(S, N, latent = False)
    
    first_row = np.zeros(p); first_row[:2] = np.array([0.0945606, 0.91819399])
    assert_array_almost_equal(P.solution.precision_[1,:], first_row)
    
    assert P.reg_params['lambda1'] == 0.1
    return
    
def test_SGL_latent():
    Sigma, Theta = group_power_network(p, K = 1, M = 2)
    S, samples = sample_covariance_matrix(Sigma, N); S = S[0,:,:]  
    P = template_problem_SGL(S, N, latent = True)
    return
        

def test_scaling_SGL():
    
    Sigma, Theta = generate_precision_matrix(p, M=2, style = 'powerlaw', gamma = 2.8, prob = 0.1, scale = True, seed = 789)
    S, samples = sample_covariance_matrix(Sigma, 10000, seed = 789)
    
    # create matrix with ones on diagonal
    np.fill_diagonal(S,1)
    
    sc = 1+np.random.rand(p)*10
    S2 = scale_array_by_diagonal(S, 1/sc)
    reg_params = {'lambda1': 0.1}
    
    solver_params = {'rho': 1., 'update_rho': False}
    
    # solve without scaling
    P = glasso_problem(S = S, N = N, reg = None, latent = False, do_scaling = False)
    P.set_reg_params(reg_params)
    P.solve(tol = 1e-15, rtol = 1e-15, solver_params = solver_params)
    
    # solve with scaling
    P2 = glasso_problem(S = S2, N = N, reg = None, latent = False, do_scaling = True)
    P2.set_reg_params(reg_params)
    P2.solve(tol = 1e-15, rtol = 1e-15, solver_params = solver_params)
    
    # precision is rescaled with 1/sc
    Theta = P.solution.precision_
    Theta2 = P2.solution.precision_
    
    Theta2 = scale_array_by_diagonal(Theta2, 1/sc) # from covariances to correlations on inverse
    
    assert_array_almost_equal(Theta, Theta2, decimal=3)
    assert_array_almost_equal(P.solution.adjacency_, P2.solution.adjacency_)
    
    return
    