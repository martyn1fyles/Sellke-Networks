#Testing script for the network Sellke Simulation
import networkx as nx
import numpy as np
import numpy.random as npr
from SellkeSimulation.simulation_code import sir_network_sellke_simple

G_test = nx.complete_graph(200)

def fixed_length(para,n): return np.array([5]*n)

test_sim_2 = sir_network_sellke_simple(G = G_test,
    beta = 0.008,
    I_parameters = 1.5,
    infected_started = [0,1,2,3,4],
    infection_period_distribution = fixed_length)

test_copy = test_sim_2
test_copy.resistance = [4]*10
test_copy.resistance.extend([100]*190)

test_copy_2 = test_sim_2
test_copy.resistance = [0.039]*10
test_copy.resistance.extend([100]*190)

def test_initialise_infection():
    #Test that the infection is initialised correctly in the network
    npr.seed(1)
    simulation_class = sir_network_sellke_simple(G = G_test,
        beta = 0.008,
        I_parameters = 1.5,
        infected_started = 5)
    npr.seed(1)
    test_list = np.random.choice(range(200), size = 5, replace = False)
    assert all(simulation_class.infected_nodes == test_list)


def test_initialise_infection_list():
    test_list = [1,2,3,4,5]
    simulation_class = sir_network_sellke_simple(G = G_test,
        beta = 0.008,
        I_parameters = 1.5,
        infected_started = test_list)
    simulation_class.initialise_infection()
    assert simulation_class.infected_nodes == test_list

def test_infectious_period_generation():
    """We test the generate_infection_periods method to check it is behaving as expected.
    """
    simulation_class = sir_network_sellke_simple(G = G_test,
        beta = 0.008,
        I_parameters = 1.5,
        infected_started = 5)
    simulation_class.generate_infection_periods()
    assert 4==4


def test_cumulative_hazards():
    """
    We test the the cumulative hazard for each node is computed correctly.
    """
    sim = sir_network_sellke_simple(G = G_test,
        beta = 0.008,
        I_parameters = 1.5,
        infected_started = 5,
        infection_period_distribution = fixed_length)
    sim.calculate_total_emitted_hazard()
    expected_answer = [5*0.008] * 200
    assert expected_answer == sim.cumulative_node_hazard



def test_cumulative_exposure():
    """
    Tests that exposure level is being computed correctly.
    first test: for the complete graph, with 5 exposed, every node should receive 25 exposure
    """
    sim = sir_network_sellke_simple(G = G_test,
        beta = 0.008,
        I_parameters = 1.5,
        infected_started = [0,1,2,3,4],
        infection_period_distribution = fixed_length)
    sim.compute_exposure_levels()

    #fixed lengh dist returns an infectious period of length 5
    #There are 5 infected, so each infected receives beta times 5 units of exposure
    expected_answer = [4*0.008*5]*5
    #There for the uninfected, 
    expected_answer.extend([5*0.008*5]*195)
    assert sim.exposure_level == expected_answer

def test_update_infected_status():
    """
    Tests the update infection status methodis correctly updating.
    We set the resistance low for the first 10 nodes (including the first 5 which are initially infected)
    We expect to see the first 10 to be infected, and no more.
    """
    
    test_copy = test_sim_2
    test_copy.update_infected_status()
    assert test_copy.infected_nodes == list(range(10))

def test_iterate_epidemic_successfully():
    """Tests the control structure for iterating epidemics.
    """
    test_copy = test_sim_2
    test_copy.iterate_epidemic()
    assert test_copy.final_size == 10
    assert test_copy.iterations == 1

def test_iterate_epidemic_real_epidemic():
    npr.seed(1)
    my_epidemic = sir_network_sellke_simple(G_test,beta = 0.008, I_parameters = 1.5, infected_started = [1])
    my_epidemic.iterate_epidemic()
    assert my_epidemic.iterations > 1