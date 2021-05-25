# 3월 25일 실습 1.2: uninformed and informed search algorithms
# 학번: 2017320123
# 이름: 김장영

# TODO: module import code
from implementation import *
 
# ===========================================================================
# TODO: large grid - BFS
grid1 = SquareGrid(30, 15)
grid1.walls = DIAGRAM1_WALLS
#draw_grid(grid1)

# TODO: small grid with weights
#draw_grid(grid2, number=grid2.weights)

# TODO: small grid
#draw_grid(grid3)

# ===========================================================================
# TODO 1. Breath First Search on grid1
start1, goal1 = (8, 7), (27, 2)
# came_from_b = breadth_first_search(grid1, start1, goal1)
# draw_grid(grid1, path=reconstruct_path(came_from_b, start=start1, goal=goal1), start= start1, goal=goal1)

# ===========================================================================
# TODO: BFS on grid2
start2, goal2 = (1, 4), (8, 3)
# came_from_b = breadth_first_search(grid2, start2, goal2)
# draw_grid(grid2, path=reconstruct_path(came_from_b, start=start2, goal=goal2), start= start2, goal=goal2)


# TODO: Dijkstra’s Algorithm on grid2
# came_from_d, cost_so_far_d = dijkstra_search(grid2, start2, goal2)
# draw_grid(grid2, path=reconstruct_path(came_from_d, start=start2, goal=goal2), start= start2, goal=goal2)

# TODO: Greedy best Search on grid2
# came_from_g = greedy_best_first_search(grid2, start2, goal2)
# draw_grid(grid2, path=reconstruct_path(came_from_g, start=start2, goal=goal2), number=grid2.weights, start= start2, goal=goal2)


# TODO: A* Search on grid2
# came_from_a, cost_so_far_a = a_star_search(grid2, start2, goal2)
# draw_grid(grid2, path=reconstruct_path(came_from_a, start=start2, goal=goal2), number=grid2.weights, start= start2, goal=goal2)


# ===========================================================================
# ===========================================================================
# TODO: 실습 과제 3번 - Dijkstra’s Algorithm on grid3
start3, goal3 = (0, 12), (14, 2)
came_from_d, cost_so_far_d = dijkstra_search(grid3, start3, goal3)
draw_grid(grid3, path=reconstruct_path(came_from_d, start=start3, goal=goal3), start= start3, goal=goal3)

# TODO: 실습 과제 3번 - Greedy Best First Search on grid3
came_from_g = greedy_best_first_search(grid3, start3, goal3)
draw_grid(grid3, path=reconstruct_path(came_from_g, start=start3, goal=goal3), start= start3, goal=goal3)


# TODO: 실습 과제 3번 - A* Search on grid3
came_from_a, cost_so_far_a = a_star_search(grid3, start3, goal3)
draw_grid(grid3, path=reconstruct_path(came_from_a, start=start3, goal=goal3), start= start3, goal=goal3)

# ===========================================================================
# TODO: 실습 과제 6번 - Dijkstra’s Algorithm on grid4
came_from_d, cost_so_far_d = dijkstra_search(grid4, start3, goal3)
draw_grid(grid4, path=reconstruct_path(came_from_d, start=start3, goal=goal3), start= start3, goal=goal3)

# TODO: 실습 과제 6번 - Greedy Best First Search on grid4
came_from_g = greedy_best_first_search(grid4, start3, goal3)
draw_grid(grid4, path=reconstruct_path(came_from_g, start=start3, goal=goal3), start= start3, goal=goal3)

# TODO: 실습 과제 6번 - A* Search on grid4
came_from_a, cost_so_far_a = a_star_search(grid4, start3, goal3)
draw_grid(grid4, path=reconstruct_path(came_from_a, start=start3, goal=goal3), start= start3, goal=goal3)