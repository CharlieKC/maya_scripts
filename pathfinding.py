from implementation2 import *
came_from, cost_so_far = a_star_search(diagram4, (0, 1), (7, 8))
draw_grid(diagram4, width=3, point_to=came_from, start=(0, 1), goal=(7, 8))
print()
draw_grid(diagram4, width=3, number=cost_so_far, start=(0, 1), goal=(7, 8))
print("\n"*2)
print(reconstruct_path(came_from, (0,1),(7,8)))
