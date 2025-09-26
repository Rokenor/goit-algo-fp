def greedy_algorithm(items, budget):
    '''Вибирає страви на основі максимального співвідношення калорій до вартості'''
    # Створюємо список страв, додаючи співвідношення калорій до вартості
    sorted_items = sorted(items.items(), key=lambda x: x[1]['calories'] / x[1]['cost'], reverse=True)

    chosen_items = []
    total_calories = 0
    total_cost = 0

    # Проходимо по відсортованих стравах
    for item_name, item_data in sorted_items:
        cost = item_data['cost']
        if total_cost + cost <= budget:
            chosen_items.append(item_name)
            total_cost += cost
            total_calories += item_data['calories']

    return chosen_items, total_calories, total_cost

def dynamic_programming(items, budget):
    '''Знаходить оптимальний набір страв для максимізації калорійності за допомогою динамічного програмування'''
    # Таблиця для зберігання максимальної калорійності для кожного бюджету
    dp = [0] * (budget + 1)

    # Таблиця для відстеження обраних предметів
    item_selection = [[] for _ in range(budget + 1)]

    item_list = list(items.items())

    # Ітерація по кожній страві
    for item_name, item_data in item_list:
        cost = item_data['cost']
        calories = item_data['calories']
        
        # Ітерація по бюджету у зворотному порядку
        for b in range(budget, cost - 1, -1):

            # Перевіряємо, чи вигідніше додати поточну страву
            if dp[b - cost] + calories > dp[b]:
                dp[b] = dp[b - cost] + calories
                item_selection[b] = item_selection[b - cost] + [item_name]

    # Визначення фінальних результатів
    max_calories = dp[budget]
    chosen_items = item_selection[budget]
    total_cost = sum(items[item]['cost'] for item in chosen_items)

    return chosen_items, max_calories, total_cost

if __name__ == "__main__":
    # Вхідні дані
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }
    budget = 100

    # Виклик жадібного алгоритму
    greedy_items, greedy_calories, greedy_cost = greedy_algorithm(items, budget)
    print("--- Жадібний алгоритм ---")
    print(f"Обрані страви: {greedy_items}")
    print(f"Загальна вартість: {greedy_cost}")
    print(f"Сумарна калорійність: {greedy_calories}\n")

    # Виклик алгоритму динамічного програмування
    dp_items, dp_calories, dp_cost = dynamic_programming(items, budget)
    print("--- Динамічне програмування ---")
    print(f"Обрані страви: {dp_items}")
    print(f"Загальна вартість: {dp_cost}")
    print(f"Сумарна калорійність: {dp_calories}")