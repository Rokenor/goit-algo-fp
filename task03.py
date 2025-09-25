import heapq
import sys

# Представлення нескінченності
infinity = sys.maxsize

class Graph:
    '''Клас для представлення неорієнтованого зваженого графа'''
    def __init__(self):
        # Словник для зберігання графа: {вершина: [(сусід, вага), ...]}
        self.vertices = {}

    def add_edge(self, source, destination, weight):
        '''Додає неорієнтоване ребро між вершинами source і destination'''
        if source not in self.vertices:
            self.vertices[source] = []
        if destination not in self.vertices:
            self.vertices[destination] = []

        # Додаємо ребро в обидва боки
        self.vertices[source].append((destination, weight))
        self.vertices[destination].append((source, weight))

def dijkstra_algorithm(graph, start_vertex):
    '''Реалізація алгоритму Дейкстри з використанням бінарної купи'''
    # Словник, який буде зберігати найкоротшу знайдену відстань від початкової вершини до кожної іншої
    distances = {vertex: infinity for vertex in graph.vertices}

    # Відстань від початкової точки до самої себе
    distances[start_vertex] = 0

    # Бінарна купа з вершинами та її обробка
    priority_queue = [(0, start_vertex)]
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        if current_vertex in graph.vertices:
            for neighbor, weight in graph.vertices[current_vertex]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

if __name__ == "__main__":
    # Створення графа та додавання ребер
    my_graph = Graph()
    my_graph.add_edge('A', 'B', 1)
    my_graph.add_edge('A', 'C', 4)
    my_graph.add_edge('B', 'C', 2)
    my_graph.add_edge('B', 'D', 5)
    my_graph.add_edge('C', 'D', 1)
    my_graph.add_edge('D', 'E', 3)
    my_graph.add_edge('E', 'A', 2)

    start_node = 'A'

    # Обчислення найкоротших шляхів
    shortest_paths = dijkstra_algorithm(my_graph, start_node)

    # Виведення результатів
    print(f"Найкоротші шляхи від вершини '{start_node}' у неорієнтованому графі:")
    for vertex, distance in shortest_paths.items():
        if distance == infinity:
            print(f"До вершини {vertex}: шлях недосяжний")
        else:
            print(f"До вершини {vertex}: {distance}")