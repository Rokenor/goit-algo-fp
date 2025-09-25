import uuid

import networkx as nx
import matplotlib.pyplot as plt

import heapq

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла


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


def draw_tree(tree_root):
    '''Малює дерево за допомогою networkx та matplotlib'''
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)} # Використовуйте значення вузла для міток

    plt.figure(figsize=(10, 7))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors, font_size=12, font_color="black")
    plt.title("Візуалізація Бінарної Купи", fontsize=16)
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

def visualize_heap(heap_array):
    '''Головна функція для візуалізації бінарної купи'''

    # Перетворюємо масив купи на деревоподібну структуру
    root = build_tree_from_heap(heap_array)

    # Візуалізуємо отримане дерево
    draw_tree(root)

if __name__ == "__main__":
    # Тестові дані
    data = [10, 4, 9, 1, 7, 5, 3]
    large_data = [3, 9, 4, 11, 15, 10, 8, 17, 20, 22, 18]

    # Перетворимо списки на бінарну купу (min-heap)
    heapq.heapify(data)
    heapq.heapify(large_data)

    print(f"Масив, що представляє бінарну купу: {data}")
    print(f"Масив для великої бінарної купи: {large_data}")

    # Візуалізуємо бінарну купу
    visualize_heap(data)
    visualize_heap(large_data)