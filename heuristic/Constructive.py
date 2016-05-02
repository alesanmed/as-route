# -*- coding: utf-8 -*-
import numpy as np
import heuristic.utils as utils
import random

from heuristic.Graph import TSP_Graph
from heuristic.Solution import Solution

def random_solution(graph, customers_list):
    if not isinstance(graph, TSP_Graph):
        utils.raise_value_error(graph, TSP_Graph, type(graph))
    
    if not isinstance(customers_list, list):
        utils.raise_value_error(customers_list, list, type(customers_list))
        
    customers = np.empty((len(customers_list),), 
                         dtype=[('id', 'i4'), ('ws', 'i8'), ('t', 'i8')])
    
    for i, customer in enumerate(customers_list):
        depot_pos = graph.get_customer_index(0)        
        c_pos = customer.get_row()
        customers[i] = (customer.get_row(), 
                        customer.get_window_start(),
                        graph.get_value(depot_pos, c_pos))
    
    # Almacen siempre el primero, su ventana empieza en 0 y el tiempo hasta si
    # mismo es 0
    ###############
    ## Provisional, se quitara la inversion del orden, es para forzar una solucion
    ## inicial invalida
    customers = customers[np.argsort(customers, order=('ws', 't'))[::-1]]
    
    first = customers[0]
    last = customers[-1]
    customers = np.concatenate(([last], customers[1:-1], [first]))
    ###############
    
    solution = Solution(len(customers_list))
    
    solution.set_graph(graph)
    solution.set_solution(customers['id'])
    
    
    start_time = int(customers['ws'][1] - customers['t'][1])
    if start_time < 0:
        start_time = 0

    solution.set_start_time(start_time)
    
    curr_time = start_time
    for i, c_row in enumerate(solution.get_solution()):
        customer = next((c for c in customers_list if c.get_row() == c_row), None)
        time_visited = curr_time + customers['t'][i]

        if time_visited < customer.get_window_start():
            time_visited = customer.get_window_start()
        
        customer.set_time_visited(int(time_visited))
        curr_time = time_visited
    
    solution.set_customer_list(customers_list)
    
    return solution
    
def perturbation(solution, level):
    solution_new = Solution(solution.get_solution().size, solution=solution)
    
    min_index = -1
    for i in range(level):
        index_origin = random.randint(1, solution_new.get_solution().size)
        index_new = random.randint(1, solution_new.get_solution().size)
        
        curr_min = min(index_origin, index_new)
        
        if curr_min < min_index:
            min_index = curr_min
        
        solution_new.one_shift(index_origin, index_new)
    
    solution_new.recompute_validity(min_index)
    return solution_new