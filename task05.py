import uuid
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from collections import deque

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла

def hex_to_rgb(hex_color):
    '''Перетворює HEX колір у RGB'''
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    '''Перетворює RGB колір у HEX'''
    return '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))

def generate_gradient_colors(start_hex, end_hex, n):
    '''Генерує градієнт з n кольорів від start_hex до end_hex'''
    if n == 0:
        return []
    if n == 1:
        return [start_hex]
    
    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    colors = []
    for i in range(n):
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (n - 1)
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (n - 1)
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (n - 1)
        colors.append(rgb_to_hex((r, g, b)))
    return colors

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    '''Рекурсивно додає ребра та позиції вузлів для візуалізаці'''
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val) # Використання id та збереження значення вузла
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root, title=""):
    '''Малює дерево за допомогою networkx та matplotlib'''
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)} # Використовуйте значення вузла для міток

    plt.figure(figsize=(10, 7))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors, font_size=12, font_color="black")
    plt.title(title, fontsize=16)
    plt.show()

def build_tree_from_heap(heap_array, index=0):
    '''Рекурсивно будує бінарне дерево з масиву, що представляє купу'''
    # Базовий випадок
    if index >= len(heap_array):
        return None
    
    # Створюємо кореневий вузол для поточного піддерева
    root = Node(heap_array[index])

    # Рекурсивно будуємо ліве піддерево
    left_child_index = 2 * index + 1
    root.left = build_tree_from_heap(heap_array, left_child_index)

    # Рекурсивно будуємо праве піддерево
    right_child_index = 2 * index + 2
    root.right = build_tree_from_heap(heap_array, right_child_index)

    return root

def count_nodes(root):
    '''Підраховує кількість вузлів у дереві'''
    if not root:
        return 0
    
    q = deque([root])
    count = 0
    while q:
        node = q.popleft()
        count += 1
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return count

def visualize_bfs(root):
    num_nodes = count_nodes(root)

    # Градієнт для BFS: від темно-синього до світло-блакитного
    colors = generate_gradient_colors("#0D47A1", "#B3E5FC", num_nodes)

    # Скидання кольорів до початкового стану
    q_reset = deque([root])
    while q_reset:
        node = q_reset.popleft()
        node.color = "#DDDDDD" # Сірий колір для невідвіданих вузлів
        if node.left:
            q_reset.append(node.left)
        if node.right:
            q_reset.append(node.right)

    # Ітеративний обхід в ширину з використанням черги
    queue = deque([root])
    visited_order = []
    visited_ids = set()

    while queue:
        node = queue.popleft()
        if node.id not in visited_ids:
            visited_ids.add(node.id)
            visited_order.append(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    # Покрокова візуалізація
    for i, node in enumerate(visited_order):
        node.color = colors[i]
        draw_tree(root, title=f"Обхід в ширину (BFS): Крок {i+1}")

def visualize_dfs(root):
    num_nodes = count_nodes(root)

    # Градієнт для DFS: від темно-зеленого до світло-салатового
    colors = generate_gradient_colors("#1B5E20", "#C8E6C9", num_nodes)

    # Скидання кольорів до початкового стану
    q_reset = deque([root])
    while q_reset:
        node = q_reset.popleft()
        node.color = "#DDDDDD" # Сірий колір для невідвіданих вузлів
        if node.left:
            q_reset.append(node.left)
        if node.right:
            q_reset.append(node.right)

    # Ітеративний обхід в глибину з використанням стека
    stack = [root]
    visited_order = []
    visited_ids = set()

    while stack:
        node = stack.pop()
        if node.id not in visited_ids:
            visited_ids.add(node.id)
            visited_order.append(node)

            # Додаємо правого нащадка в стек першим, щоб лівий оброблявся раніше
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
    
    # Покрокова візуалізація
    for i, node in enumerate(visited_order):
        node.color = colors[i]
        draw_tree(root, title=f"Обхід в глибину (DFS): Крок {i+1}")

if __name__ == "__main__":
    # Тестові дані та побудова бінарної купи
    data = [3, 9, 4, 11, 15, 10, 8, 17, 20, 22, 18]
    heapq.heapify(data)
    print(f"Масив, що представляє бінарну купу: {data}")

    # Побудова дерева з купи
    root = build_tree_from_heap(data)

    # Початкова візуалізація дерева
    draw_tree(root, "Початкове Дерево")

    # Візуалізація обходу в ширину (BFS)
    visualize_bfs(root)

    # Візуалізація обходу в глибину (DFS)
    visualize_dfs(root)