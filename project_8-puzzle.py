import pygame
import sys
import heapq
from collections import deque
import time 
import random 
import math
import sys
sys.setrecursionlimit(10000)  
# Kích thước giao diện
WIDTH, HEIGHT = 650, 750  
GRID_SIZE = 3
TILE_SIZE = 120  
FONT_SIZE = 40  
EXECUTION_FONT_SIZE = 25
STEP_DELAY = 300
BUTTON_HEIGHT = 40  
BUTTON_WIDTH = (WIDTH - 60) // 5  
BUTTON_SPACING = 5 
BUTTON_START_Y = HEIGHT - 220  

# Màu sắc cho từng ô
TILE_COLORS = {
    1: (255, 100, 100), 2: (100, 255, 100), 3: (100, 100, 255),
    4: (255, 255, 100), 5: (255, 100, 255), 6: (100, 255, 255),
    7: (200, 150, 100), 8: (150, 200, 150), 0: (50, 50, 50)
}

# Trạng thái đầu & trạng thái mục tiêu
start_state = ((2, 6, 5), (8, 0, 7), (4, 3, 1))
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def print_state(state):
    """In trạng thái ra console dưới dạng bảng 3x3"""
    for row in state:
        print(" | ".join(f"{cell:2}" for cell in row))
    print("-" * 10)  
# Pygame khởi tạo
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle AI Solver")
font = pygame.font.Font(None, FONT_SIZE)
execution_font = pygame.font.Font(None, EXECUTION_FONT_SIZE)  
button_font = pygame.font.Font(None, 30)  
selected_algorithm = None
highlighted_tiles = []
execution_time = ""  

def draw_grid(state):
    """Vẽ lưới ô số với kích thước nhỏ hơn"""
    screen.fill((30, 30, 30))
    # Tính toán vị trí bắt đầu để căn giữa theo chiều ngang
    grid_start_x = (WIDTH - (TILE_SIZE * GRID_SIZE)) // 2
    grid_start_y = 30  
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            rect = pygame.Rect(
                grid_start_x + j * TILE_SIZE,
                grid_start_y + i * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            color = TILE_COLORS[value]
            pygame.draw.rect(screen, color, rect, border_radius=6)  
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            if value != 0:
                text = font.render(str(value), True, (255, 255, 255))
                # Căn giữa số trong ô
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
                
# Cập nhật hàm draw_buttons để hỗ trợ thêm nút
def draw_buttons():
    """Vẽ nút chọn thuật toán"""
    button_font = pygame.font.Font(None, 26)
    global selected_algorithm
    button_texts = ["BFS", "DFS", "UCS", "IDDFS", "A*", 
                   "IDA*", "Greedy", "Simple HC", "Steepest HC", "Stochastic HC", 
                   "SA","Beam", "GA", "Nondet", "Partial Obs",
                   "BT","BT_FC","Min-Conflicts","Q-Learning", "New State", "QUIT"]

    colors = [
        (255, 50, 50), (80, 80, 80), (255, 200, 50), (50, 200, 100), (220, 220, 220),
        (100, 50, 200), (150, 100, 200), (200, 100, 50), (200, 50, 100), (200, 150, 50),
        (50, 150, 200), (150, 200, 150), (100, 200, 100), (150, 150, 255), (255, 150, 150),
        (100, 255, 200), (50, 150, 50),(200, 100, 150),(150, 100, 150),(100, 200, 200),(200, 50, 50)
    ]

    buttons = []
    buttons_per_row = 5  
    button_width = (WIDTH - 60) // buttons_per_row  

    for i, text in enumerate(button_texts):
        row = i // buttons_per_row
        col = i % buttons_per_row
        rect = pygame.Rect(
            10 + col * (button_width + BUTTON_SPACING),
            BUTTON_START_Y + row * (BUTTON_HEIGHT + BUTTON_SPACING),
            button_width,
            BUTTON_HEIGHT
        )
        color = colors[i] if text != selected_algorithm else (0, 0, 0)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        button_font = pygame.font.Font(None, 24)  
        text_render = button_font.render(text, True, (255, 255, 255))

        while text_render.get_width() > rect.width - 10 and button_font.get_height() > 18:
            button_font = pygame.font.Font(None, button_font.get_height() - 2)
            text_render = button_font.render(text, True, (255, 255, 255))

        text_rect = text_render.get_rect(center=rect.center)
        screen.blit(text_render, text_rect)
        buttons.append((rect, text))
    return buttons

def draw_execution_time():
    """Vẽ ô thời gian chạy thuật toán"""
    time_box_rect = pygame.Rect(
        10, 
        TILE_SIZE * GRID_SIZE + 50, 
        WIDTH - 20, 
        40
    )
    pygame.draw.rect(screen, (50, 50, 50), time_box_rect, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), time_box_rect, 2)
    time_text = execution_font.render(f"Execution Time: {execution_time}", True, (255, 255, 255))
    text_rect = time_text.get_rect(center=time_box_rect.center)
    screen.blit(time_text, text_rect)
    
def find_blank(state):
    """Tìm vị trí ô trống"""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if state[i][j] == 0:
                return i, j

def swap_tiles(state, i1, j1, i2, j2):
    """Hoán đổi hai ô"""
    new_state = [list(row) for row in state]
    new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
    return tuple(tuple(row) for row in new_state)

def manhattan_distance(state):
    """Tính khoảng cách Manhattan"""
    total = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = (value - 1) // GRID_SIZE, (value - 1) % GRID_SIZE
                total += abs(i - goal_x) + abs(j - goal_y)
    return total

def get_neighbors(state):
    blank_i, blank_j = find_blank(state)
    neighbors = []
    for di, dj in directions:
        ni, nj = blank_i + di, blank_j + dj
        if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
            neighbors.append(swap_tiles(state, blank_i, blank_j, ni, nj))
    return neighbors

def ida_star_search(start, goal):
    """Giải bằng IDA*"""
    bound = manhattan_distance(start)
    path = [start]

    def search(g, bound):
        state = path[-1]
        f = g + manhattan_distance(state)
        if f > bound:
            return f
        if state == goal:
            return "FOUND"
        min_bound = float('inf')
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in path:
                    path.append(new_state)
                    result = search(g + 1, bound)
                    if result == "FOUND":
                        return "FOUND"
                    if result < min_bound:
                        min_bound = result
                    path.pop()
        return min_bound

    while True:
        result = search(0, bound)
        if result == "FOUND":
            return path
        if result == float('inf'):
            return None
        bound = result

def bfs(start, goal):
    """Giải bằng BFS"""
    queue = deque([(start, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [new_state]))
    return None

def dfs(start, goal, depth_limit=50):
    """Giải bằng DFS với giới hạn độ sâu"""
    stack = [(start, [], 0)]  
    visited = set()
    while stack:
        state, path, depth = stack.pop()
        if state == goal:
            return path + [goal]
        if depth >= depth_limit:
            continue  
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, path + [new_state], depth + 1))
    return None

def iddfs(start, goal):
    """Giải bằng IDDFS (Iterative Deepening DFS)"""
    depth_limit = 0
    while True:
        result = dfs(start, goal, depth_limit)
        if result is not None:
            return result
        depth_limit += 1

def greedy(start, goal):
    """Giải bằng Greedy"""
    priority_queue = [(manhattan_distance(start), start, [])]
    visited = set()
    while priority_queue:
        _, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    heapq.heappush(priority_queue, (manhattan_distance(new_state), new_state, path + [new_state]))
    return None

def ucs(start, goal):
    """Giải bằng UCS"""
    priority_queue = [(0, start, [])]
    visited = set()
    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    heapq.heappush(priority_queue, (cost + 1, new_state, path + [new_state]))
    return None

def a_star(start, goal):
    """Giải bằng A*"""
    priority_queue = [(manhattan_distance(start), 0, start, [])]
    visited = set()
    while priority_queue:
        _, cost, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    heapq.heappush(priority_queue, (cost + 1 + manhattan_distance(new_state), cost + 1, new_state, path + [new_state]))
    return None


def simple_hill_climbing(start, goal, max_steps=1000):
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    visited = set()  # Theo dõi các trạng thái đã thăm
    visited.add(current_state)
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        # Tạo các trạng thái kế cận chưa thăm
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    new_h = manhattan_distance(new_state)
                    neighbors.append((new_h, new_state))
        
        if not neighbors:
            break
            
        neighbors.sort()  
        
        # Chọn trạng thái tốt nhất chưa thăm
        for h, state in neighbors:
            if h <= current_h:  
                current_state = state
                current_h = h
                path.append(current_state)
                visited.add(current_state)
                break
        else:
            # Nếu không có trạng thái tốt hơn, chọn ngẫu nhiên trong các trạng thái chưa thăm
            unvisited = [state for h, state in neighbors if state not in visited]
            if unvisited:
                current_state = random.choice(unvisited)
                current_h = manhattan_distance(current_state)
                path.append(current_state)
                visited.add(current_state)
            else:
                break
    
    return path


def steepest_ascent_hill_climbing(start, goal, max_steps=1000):
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    visited = set()
    visited.add(tuple(map(tuple, current_state)))  
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                new_state_tuple = tuple(map(tuple, new_state))
                if new_state_tuple not in visited:
                    new_h = manhattan_distance(new_state)
                    neighbors.append((new_h, new_state))
        
        if not neighbors:
            break
            
        # Chọn trạng thái tốt nhất (Steepest Ascent)
        best_h, best_state = min(neighbors, key=lambda x: x[0])
        
        if best_h < current_h:
            current_state = best_state
            current_h = best_h
            path.append(current_state)
            visited.add(tuple(map(tuple, best_state)))  
        elif best_h == current_h:
           
            plateau_states = [state for h, state in neighbors if h == current_h]
            current_state = random.choice(plateau_states)
            path.append(current_state)
        else:
            break  
    
    return path

def stochastic_hill_climbing(start, goal, max_steps=1000):
    """Stochastic Hill Climbing với cơ chế thoát local optima"""
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    visited = set([current_state]) 
    stuck_count = 0
    max_stuck = 20  
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        # Tạo danh sách láng giềng hợp lệ
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    new_h = manhattan_distance(new_state)
                    neighbors.append((new_h, new_state))
        
        if not neighbors:
            break  # Không còn nước đi hợp lệ
            
        # Tách các láng giềng thành 2 nhóm: tốt hơn và xấu hơn
        improving = [(h, s) for h, s in neighbors if h < current_h]
        sideways = [(h, s) for h, s in neighbors if h == current_h]
        worsening = [(h, s) for h, s in neighbors if h > current_h]
        
        # Ưu tiên chọn từ các láng giềng tốt hơn
        if improving:
            # Tính trọng số (ưu tiên các bước cải thiện nhiều)
            weights = [1/(h+0.1) for h, s in improving]  # +0.1 để tránh chia cho 0
            total = sum(weights)
            if total > 0:
                probs = [w/total for w in weights]
                idx = random.choices(range(len(improving)), weights=probs)[0]
                current_h, current_state = improving[idx]
                path.append(current_state)
                visited.add(current_state)
                stuck_count = 0
                continue
        
        # Nếu không có láng giềng tốt hơn, xem xét đi ngang
        if sideways:
            current_h, current_state = random.choice(sideways)
            path.append(current_state)
            visited.add(current_state)
            stuck_count += 1
        else:
            stuck_count += 1
            
        # Nếu bị kẹt quá lâu, chấp nhận bước đi xấu hơn để thoát local optima
        if stuck_count > max_stuck and worsening:
            # Chọn ngẫu nhiên một bước đi xấu hơn
            current_h, current_state = random.choice(worsening)
            path.append(current_state)
            visited.add(current_state)
            stuck_count = 0
    
    return path


def simulated_annealing(start, goal, max_iterations=1000, initial_temp=1000, cooling_rate=0.99):
    """Giải bằng Simulated Annealing"""
    current_state = start
    path = [current_state]
    current_score = manhattan_distance(current_state)
    temp = initial_temp
    
    for i in range(max_iterations):
        if current_state == goal:
            return path
            
        # Giảm nhiệt độ theo tỉ lệ làm mát
        temp *= cooling_rate
        
        # Nếu nhiệt độ quá thấp, dừng lại
        if temp < 0.1:
            break
            
        neighbors = get_neighbors(current_state)
        next_state = random.choice(neighbors)
        next_score = manhattan_distance(next_state)
        
        # Tính toán sự thay đổi năng lượng (khoảng cách)
        delta_e = current_score - next_score
        
        # Nếu bước đi tốt hơn, luôn chấp nhận
        if delta_e > 0:
            current_state = next_state
            current_score = next_score
            path.append(current_state)
        else:
            # Nếu bước đi không tốt hơn, chấp nhận với xác suất e^(delta_e/temp)
            probability = min(1, math.exp(delta_e / temp))
            if random.random() < probability:
                current_state = next_state
                current_score = next_score
                path.append(current_state)
    
    print("Simulated Annealing reached max iterations without finding solution!")
    return path

def beam_search(start, goal, beam_width=2):
    """Giải bằng Beam Search"""
    # Hàm đánh giá cho Beam Search (sử dụng Manhattan distance)
    def evaluate(state):
        return manhattan_distance(state)
    
    current_states = [(start, [start], evaluate(start))]
    
    visited = set()
    visited.add(start)
    
    while current_states:
        next_level = []
        
        for state, path, score in current_states:
            if state == goal:
                return path
                
            blank_i, blank_j = find_blank(state)
            for di, dj in directions:
                ni, nj = blank_i + di, blank_j + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                    new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                    if new_state not in visited:
                        visited.add(new_state)
                        new_score = evaluate(new_state)
                        next_level.append((new_state, path + [new_state], new_score))
        
        # Sắp xếp các trạng thái tiếp theo theo điểm số và chọn beam_width trạng thái tốt nhất
        next_level.sort(key=lambda x: x[2])
        current_states = next_level[:beam_width]
        
        # Nếu không có trạng thái tiếp theo nào, thoát
        if not current_states:
            break
    
    print("Beam Search failed to find solution!")
    return None

def genetic_algorithm(start, goal, population_size=50, generations=1000, mutation_rate=0.2):
    """Giải bằng Genetic Algorithm"""
    # Hàm đánh giá độ thích nghi (fitness) - càng thấp càng tốt
    def fitness(state):
        return manhattan_distance(state)
    
    # Tạo một cá thể ngẫu nhiên bằng cách thực hiện các bước di chuyển ngẫu nhiên
    def create_individual(initial_state, steps=20):
        state = initial_state
        path = [state]
        for _ in range(steps):
            neighbors = get_neighbors(state)
            state = random.choice(neighbors)
            path.append(state)
        return path
    
    # Tạo quần thể ban đầu
    population = [create_individual(start) for _ in range(population_size)]
    
    best_solution = None
    best_fitness = float('inf')
    
    for generation in range(generations):
        # Đánh giá độ thích nghi
        fitness_scores = []
        for individual in population:
            last_state = individual[-1]
            current_fitness = fitness(last_state)
            fitness_scores.append(current_fitness)
            
            # Kiểm tra nếu tìm thấy giải pháp
            if last_state == goal:
                return individual
            
            # Cập nhật giải pháp tốt nhất
            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_solution = individual
        
        # Chọn lọc (tournament selection)
        parents = []
        for _ in range(population_size):
            # Chọn ngẫu nhiên 3 cá thể và chọn cá thể tốt nhất
            candidates = random.sample(list(zip(population, fitness_scores)), 3)
            winner = min(candidates, key=lambda x: x[1])[0]
            parents.append(winner)
        
        # Lai ghép (crossover)
        new_population = []
        for i in range(0, population_size, 2):
            parent1 = parents[i]
            parent2 = parents[i+1] if i+1 < len(parents) else parents[0]
            
            # Điểm lai ghép ngẫu nhiên
            crossover_point = random.randint(1, min(len(parent1), len(parent2))-1)
            
            # Tạo con cái bằng cách kết hợp 2 cha mẹ
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            
            new_population.extend([child1, child2])
        
        # Đột biến (mutation)
        for i in range(len(new_population)):
            if random.random() < mutation_rate:
                # Chọn ngẫu nhiên một điểm trong path và thay thế bằng một bước di chuyển ngẫu nhiên
                mutate_point = random.randint(0, len(new_population[i])-1)
                if mutate_point == 0:
                    # Nếu là điểm đầu, thêm một bước ngẫu nhiên từ start state
                    neighbors = get_neighbors(new_population[i][0])
                    if neighbors:
                        new_population[i] = [random.choice(neighbors)] + new_population[i][1:]
                else:
                    # Thay thế bằng một bước di chuyển hợp lệ từ state trước đó
                    prev_state = new_population[i][mutate_point-1]
                    neighbors = get_neighbors(prev_state)
                    if neighbors:
                        new_population[i][mutate_point] = random.choice(neighbors)
                        # Cắt bỏ các state sau điểm đột biến vì có thể không còn hợp lệ
                        new_population[i] = new_population[i][:mutate_point+1]
        
        population = new_population
    
    print(f"Genetic Algorithm finished after {generations} generations. Best fitness: {best_fitness}")
    return best_solution  
def get_nondeterministic_neighbors(state, success_prob=0.8):
    """Lấy các trạng thái kề với xác suất thành công"""
    blank_i, blank_j = find_blank(state)
    neighbors = []
    possible_moves = []
    
    # Đầu tiên lấy tất cả các hướng di chuyển có thể
    for di, dj in directions:
        ni, nj = blank_i + di, blank_j + dj
        if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
            possible_moves.append((di, dj))
    
    # Với mỗi hướng di chuyển, tạo các kết quả có thể
    for di, dj in possible_moves:
        ni, nj = blank_i + di, blank_j + dj
        # Di chuyển thành công (đúng hướng)
        neighbors.append((swap_tiles(state, blank_i, blank_j, ni, nj), success_prob))
        
        # Di chuyển thất bại (các hướng khác)
        remaining_prob = (1 - success_prob) / (len(possible_moves) - 1) if len(possible_moves) > 1 else 0
        for other_di, other_dj in possible_moves:
            if (other_di, other_dj) != (di, dj):
                oi, oj = blank_i + other_di, blank_j + other_dj
                if 0 <= oi < GRID_SIZE and 0 <= oj < GRID_SIZE:
                    neighbors.append((swap_tiles(state, blank_i, blank_j, oi, oj), remaining_prob))
    
    return neighbors

def nondeterministic_astar(start, goal, success_prob=0.8):
    """Thuật toán A* với hành động không xác định"""
    # Sử dụng khoảng cách Manhattan kỳ vọng làm heuristic
    def expected_heuristic(state):
        return manhattan_distance(state) * (1/success_prob) 
        
    open_set = [(expected_heuristic(start), 0, start, [start])]
    visited = set()
    
    while open_set:
        _, cost, state, path = heapq.heappop(open_set)
        
        if state == goal:
            return path
            
        if state in visited:
            continue
        visited.add(state)
        
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                # Với xác suất success_prob, ta có trạng thái mong muốn
                intended_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                # Ở đây đơn giản chỉ xét trạng thái mong muốn
                # Triển khai đầy đủ sẽ xét tất cả khả năng
                new_state = intended_state
                if new_state not in visited:
                    new_cost = cost + 1
                    heapq.heappush(open_set, 
                                  (new_cost + expected_heuristic(new_state), 
                                   new_cost, 
                                   new_state, 
                                   path + [new_state]))
    
    return None

def nondeterministic_search(start, goal):
    """Hàm gọi tìm kiếm không xác định (sử dụng A* làm cơ sở)"""
    return nondeterministic_astar(start, goal)


# Biến toàn cục để theo dõi các ô bị ẩn
hidden_tiles = set()

def hide_random_tiles(state, num_hidden=4):
    """Ẩn ngẫu nhiên một số ô trên bảng"""
    global hidden_tiles
    hidden_tiles = set()
    tiles = [(i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if state[i][j] != 0]
    
    # Không ẩn ô trống (0)
    if len(tiles) > num_hidden:
        hidden_tiles = set(random.sample(tiles, num_hidden))
    else:
        hidden_tiles = set(tiles)
    return hidden_tiles

def draw_partial_grid(state, hidden):
    """Vẽ bảng với các ô bị ẩn"""
    screen.fill((30, 30, 30))
    grid_start_x = (WIDTH - (TILE_SIZE * GRID_SIZE)) // 2
    grid_start_y = 30
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            rect = pygame.Rect(
                grid_start_x + j * TILE_SIZE,
                grid_start_y + i * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            
            # Xử lý ô bị ẩn
            if (i,j) in hidden:
                pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=6)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                text = font.render("?", True, (200, 200, 200))
            else:
                color = TILE_COLORS[value]
                pygame.draw.rect(screen, color, rect, border_radius=6)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                if value != 0:
                    text = font.render(str(value), True, (255, 255, 255))
            
            if (i,j) not in hidden or value == 0:  
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def belief_state_update(belief_states, action, observation):
    """Cập nhật trạng thái niềm tin sau khi thực hiện hành động"""
    new_belief_states = set()
    
    for state in belief_states:
        # Giả sử action là hướng di chuyển ô trống
        blank_i, blank_j = find_blank(state)
        di, dj = action
        
        # Kiểm tra hành động hợp lệ
        ni, nj = blank_i + di, blank_j + dj
        if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
            new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
            
            # Kiểm tra xem new_state có phù hợp với observation không
            match = True
            for (i,j), val in observation.items():
                if new_state[i][j] != val:
                    match = False
                    break
            
            if match:
                new_belief_states.add(new_state)
    
    return new_belief_states if new_belief_states else belief_states  

def partial_observation_search(start, goal, num_hidden=4):
    """Tìm kiếm với quan sát một phần"""
    global hidden_tiles
    hidden_tiles = hide_random_tiles(start, num_hidden)
    
    # Tạo observation từ trạng thái ban đầu (chỉ các ô không bị ẩn)
    observation = {}
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i,j) not in hidden_tiles:
                observation[(i,j)] = start[i][j]
    
    # Khởi tạo belief states (tất cả trạng thái phù hợp với observation)
    belief_states = set()
   
    belief_states.add(start)
    
    path = []
    current_state = start
    path.append(current_state)
    
    while True:
        if current_state == goal:
            return path
        
        # Chọn hành động dựa trên belief states (đơn giản là chọn ngẫu nhiên)
        possible_actions = []
        blank_i, blank_j = find_blank(current_state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                possible_actions.append((di, dj))
        
        if not possible_actions:
            break
        
        action = random.choice(possible_actions)
        
        # Thực hiện hành động (giả sử thành công)
        di, dj = action
        ni, nj = blank_i + di, blank_j + dj
        current_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
        path.append(current_state)
        
        # Cập nhật observation (các ô được tiết lộ sau khi di chuyển)
        for (i,j) in hidden_tiles.copy():
            if current_state[i][j] == 0:  
                hidden_tiles.remove((i,j))
                observation[(i,j)] = 0
        
        # Cập nhật belief states
        belief_states = belief_state_update(belief_states, action, observation)
        
        # Nếu chỉ còn 1 belief state, chuyển sang tìm kiếm thông thường
        if len(belief_states) == 1:
            current_state = next(iter(belief_states))
            # Tiếp tục với A* từ đây
            remaining_path = a_star(current_state, goal)
            if remaining_path:
                path.extend(remaining_path[1:])  
            break
    
    return path

#  Hàm Backtracking  solver
def BT (start, goal):
    """Giải bằng Backtracking"""
    try:
        # Chuyển đổi trạng thái thành danh sách phẳng
        flat_start = [num for row in start for num in row]
        flat_goal = [num for row in goal for num in row]
        
        # Tìm vị trí ô trống
        blank_pos = flat_start.index(0)
        
        # Hàm đệ quy để thử các bước đi
        def backtrack(current_state, path, visited, depth=0):
            # Giới hạn độ sâu để tránh đệ quy quá sâu
            if depth > 50:  # Giới hạn độ sâu tối đa
                return None
                
            if tuple(current_state) == tuple(flat_goal):
                return path
            
            blank_pos = current_state.index(0)
            x, y = blank_pos // GRID_SIZE, blank_pos % GRID_SIZE
            
            # Thử các hướng di chuyển có thể
            for di, dj in directions:
                ni, nj = x + di, y + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                    new_blank_pos = ni * GRID_SIZE + nj
                    new_state = current_state.copy()
                    # Hoán đổi ô trống với ô lân cận
                    new_state[blank_pos], new_state[new_blank_pos] = new_state[new_blank_pos], new_state[blank_pos]
                    
                    state_tuple = tuple(new_state)
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        result = backtrack(new_state, path + [new_state], visited, depth + 1)
                        if result is not None:
                            return result
                        visited.remove(state_tuple)  
            return None
        
        # Chạy backtracking
        visited = set()
        visited.add(tuple(flat_start))
        solution = backtrack(flat_start, [flat_start], visited)
        
        if solution:
            # Chuyển đổi lại về dạng tuple 2D
            converted_solution = []
            for state in solution:
                converted_state = (
                    (state[0], state[1], state[2]),
                    (state[3], state[4], state[5]),
                    (state[6], state[7], state[8])
                )
                converted_solution.append(converted_state)
            return converted_solution
        return None
    except Exception as e:
        print(f"Error in CSP solver: {e}")
        return None

def backtracking_with_forward_checking(start, goal, max_depth=30):
    """Giải bằng Backtracking với Forward Checking cải tiến"""
    path = []
    visited = set()
    
    # Chuyển đổi trạng thái sang tuple để có thể hash và lưu vào set
    start_tuple = tuple(tuple(row) for row in start)
    goal_tuple = tuple(tuple(row) for row in goal)
    
    def manhattan_distance(state):
        """Tính khoảng cách Manhattan đến goal"""
        distance = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                val = state[i][j]
                if val != 0:  
                    goal_i, goal_j = divmod(val-1, GRID_SIZE)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    def backtrack(current_state, depth):
        nonlocal path
        if depth > max_depth:
            return False
            
        current_tuple = tuple(tuple(row) for row in current_state)
        if current_tuple == goal_tuple:
            path.append(current_state)
            return True
            
        if current_tuple in visited:
            return False
            
        visited.add(current_tuple)
        blank_i, blank_j = find_blank(current_state)
        
        # Tạo danh sách các bước đi tiềm năng và sắp xếp theo heuristic
        moves = []
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                new_tuple = tuple(tuple(row) for row in new_state)
                if new_tuple not in visited:
                    # Ưu tiên các bước đi có khoảng cách Manhattan nhỏ hơn
                    moves.append((manhattan_distance(new_state), new_state))
        
        # Sắp xếp các bước đi theo heuristic tốt nhất trước
        moves.sort()
        
        for _, new_state in moves:
            path.append(current_state)
            if backtrack(new_state, depth+1):
                return True
            path.pop()
        
        visited.remove(current_tuple)
        return False
    
    if backtrack(start, 0):
        return path
    return None

def min_conflicts(start, goal, max_steps=1000):
    """Giải bằng thuật toán Min-Conflicts"""
    current = [list(row) for row in start]
    goal_positions = {}
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            goal_positions[goal[i][j]] = (i, j)
    
    for _ in range(max_steps):
        # Kiểm tra nếu đã đạt mục tiêu
        if tuple(tuple(row) for row in current) == goal:
            return [tuple(tuple(row) for row in current)]
        
        # Tìm ô có xung đột lớn nhất (không đúng vị trí)
        conflicts = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = current[i][j]
                if value != 0:
                    goal_i, goal_j = goal_positions[value]
                    if (i, j) != (goal_i, goal_j):
                        conflicts.append((abs(i-goal_i) + abs(j-goal_j), (i, j)))
        
        if not conflicts:
            break  
        
        # Chọn ô có xung đột lớn nhất
        _, (i, j) = max(conflicts)
        value = current[i][j]
        
        # Tìm vị trí tốt nhất để di chuyển ô này
        best_move = None
        min_conflict = float('inf')
        blank_i, blank_j = find_blank(tuple(tuple(row) for row in current))
        
        # Thử các hướng di chuyển có thể
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                
                pass
        
        
        
        blank_i, blank_j = find_blank(tuple(tuple(row) for row in current))
        best_move = None
        best_improvement = -1
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                # Tính số xung đột hiện tại
                current_conflicts = 0
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        val = current[x][y]
                        if val != 0:
                            gx, gy = goal_positions[val]
                            current_conflicts += abs(x - gx) + abs(y - gy)
                
                # Thử hoán đổi
                current[blank_i][blank_j], current[ni][nj] = current[ni][nj], current[blank_i][blank_j]
                
                # Tính số xung đột mới
                new_conflicts = 0
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        val = current[x][y]
                        if val != 0:
                            gx, gy = goal_positions[val]
                            new_conflicts += abs(x - gx) + abs(y - gy)
                
                # Hoàn tác hoán đổi
                current[blank_i][blank_j], current[ni][nj] = current[ni][nj], current[blank_i][blank_j]
                
                improvement = current_conflicts - new_conflicts
                if improvement > best_improvement:
                    best_improvement = improvement
                    best_move = (ni, nj)
        
        if best_move:
            ni, nj = best_move
            current[blank_i][blank_j], current[ni][nj] = current[ni][nj], current[blank_i][blank_j]
    
    return [tuple(tuple(row) for row in current)] if tuple(tuple(row) for row in current) == goal else None

#Triển khai thuật toán Q-learning
class QLearningSolver:
    def __init__(self):
        self.q_table = {}
        self.alpha = 0.1  
        self.gamma = 0.9  
        self.epsilon = 0.2  

    def state_to_key(self, state):
        """Chuyển trạng thái thành key hashable cho Q-table"""
        return str(state)

    def get_action(self, state, valid_actions):
        """Chọn hành động theo epsilon-greedy policy"""
        state_key = self.state_to_key(state)
        
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        else:
            if state_key not in self.q_table:
                self.q_table[state_key] = {action: 0 for action in valid_actions}
            return max(self.q_table[state_key].items(), key=lambda x: x[1])[0]

    def update_q_value(self, state, action, reward, next_state, next_actions):
        """Cập nhật Q-value theo công thức Q-learning"""
        state_key = self.state_to_key(state)
        next_state_key = self.state_to_key(next_state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0 for action in valid_actions}
        
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0 for action in next_actions}
        
        max_next_q = max(self.q_table[next_state_key].values())
        current_q = self.q_table[state_key][action]
        
        # Công thức Q-learning
        self.q_table[state_key][action] = current_q + self.alpha * (
            reward + self.gamma * max_next_q - current_q
        )

def q_learning(start, goal, episodes=1000, max_steps=100):
    """Giải bằng Q-learning"""
    solver = QLearningSolver()
    
    for episode in range(episodes):
        state = start
        path = [state]
        
        for step in range(max_steps):
            if state == goal:
                break
                
            blank_i, blank_j = find_blank(state)
            valid_actions = []
            for di, dj in directions:
                ni, nj = blank_i + di, blank_j + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                    valid_actions.append((di, dj))
            
            action = solver.get_action(state, valid_actions)
            
            # Thực hiện hành động
            ni, nj = blank_i + action[0], blank_j + action[1]
            next_state = swap_tiles(state, blank_i, blank_j, ni, nj)
            
            # Tính reward
            if next_state == goal:
                reward = 100
            else:
                reward = -1 + (0.1 * (manhattan_distance(state) - manhattan_distance(next_state)))
            
            # Cập nhật Q-value
            next_blank_i, next_blank_j = find_blank(next_state)
            next_valid_actions = []
            for di, dj in directions:
                ni, nj = next_blank_i + di, next_blank_j + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                    next_valid_actions.append((di, dj))
            
            solver.update_q_value(state, action, reward, next_state, next_valid_actions)
            
            state = next_state
            path.append(state)
    
    # Sau khi train, tìm đường đi tốt nhất
    state = start
    solution_path = [state]
    visited = set()
    
    while state != goal and len(solution_path) < 100:
        blank_i, blank_j = find_blank(state)
        valid_actions = []
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                valid_actions.append((di, dj))
        
        state_key = solver.state_to_key(state)
        if state_key not in solver.q_table:
            break
            
        action = max(solver.q_table[state_key].items(), key=lambda x: x[1])[0]
        ni, nj = blank_i + action[0], blank_j + action[1]
        state = swap_tiles(state, blank_i, blank_j, ni, nj)
        
        if state in visited:  # Tránh lặp vô hạn
            break
        visited.add(state)
        
        solution_path.append(state)
    
    return solution_path if solution_path[-1] == goal else None

def generate_new_state():
    """Tạo trạng thái ban đầu mới ngẫu nhiên nhưng có thể giải được"""
    # Tạo danh sách các số từ 0-8
    numbers = list(range(9))
    random.shuffle(numbers)
    
    # Kiểm tra xem trạng thái có thể giải được không
    def is_solvable(state):
        # Đếm số nghịch thế
        inversions = 0
        flat_state = [num for row in state for num in row]
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] != 0 and flat_state[j] != 0 and flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions % 2 == 0
    
    # Tạo trạng thái mới cho đến khi tìm được trạng thái có thể giải được
    while True:
        random.shuffle(numbers)
        new_state = (
            (numbers[0], numbers[1], numbers[2]),
            (numbers[3], numbers[4], numbers[5]),
            (numbers[6], numbers[7], numbers[8])
        )
        if is_solvable(new_state):
            return new_state

def main():
    global selected_algorithm, highlighted_tiles, execution_time, start_state
    running = True
    path = None
    step = 0
    
    while running:
        current_state = path[step] if path and len(path) > step else start_state
        draw_grid(current_state)
        draw_execution_time()
        buttons = draw_buttons()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for rect, algo in buttons:
                    if rect.collidepoint(x, y):
                        if algo == "QUIT":
                            running = False
                        elif algo == "New State":
                            start_state = generate_new_state()
                            path = None
                            step = 0
                            selected_algorithm = None
                            execution_time = ""
                        else:
                            selected_algorithm = algo
                            start_time = time.time()
                            if algo == "BFS":
                                path = bfs(start_state, goal_state)
                            elif algo == "DFS":
                                path = dfs(start_state, goal_state)
                            elif algo == "Greedy":
                                path = greedy(start_state, goal_state)
                            elif algo == "UCS":
                                path = ucs(start_state, goal_state)
                            elif algo == "A*":
                                path = a_star(start_state, goal_state)
                            elif algo == "IDA*":
                                path = ida_star_search(start_state, goal_state)
                            elif algo == "IDDFS":
                                path = iddfs(start_state, goal_state)
                            elif algo == "Simple HC":
                                path = simple_hill_climbing(start_state, goal_state)
                            elif algo == "Steepest HC":
                                path = steepest_ascent_hill_climbing(start_state, goal_state)
                            elif algo == "Stochastic HC":
                                path = stochastic_hill_climbing(start_state, goal_state)
                            elif algo == "SA":
                                path = simulated_annealing(start_state, goal_state)
                            elif algo == "Beam":
                                path = beam_search(start_state, goal_state)
                            elif algo == "GA":
                                path = genetic_algorithm(start_state, goal_state)
                            elif algo == "Nondet":
                                path = nondeterministic_search(start_state, goal_state)
                            elif algo == "Partial Obs":
                                path = partial_observation_search(start_state, goal_state)
                            elif algo == "BT_FC":
                                path = backtracking_with_forward_checking(start_state, goal_state)
                            elif algo == "BT":
                                path = BT(start_state, goal_state)
                            elif algo == "Min-Conflicts":
                                path = min_conflicts(start_state, goal_state)
                            elif algo == "Q-Learning":
                                path = q_learning(start_state, goal_state)
                            
                            end_time = time.time()
                            execution_time = f"{end_time - start_time:.4f} seconds"
                            if path:
                                print(f"\n{algo} path has {len(path)} steps")
                            else:
                                print(f"\n{algo} failed to find solution!")
                            step = 0
        
        if path and step < len(path) - 1:
            pygame.time.delay(STEP_DELAY)
            step += 1
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()