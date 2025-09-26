import random
import pandas as pd
import matplotlib.pyplot as plt

def simulate_dice_rolls(num_simulations: int):
    '''Імітує кидання двох кубиків задану кількість разів'''
    # Ініціалізуємо словник для зберігання результатів (суми від 2 до 12)
    sums_counts = {i: 0 for i in range(2, 13)}

    # Проводимо симуляцію
    for _ in range(num_simulations):
        # Кидаємо два кубики
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        
        # Обчислюємо суму та збільшуємо лічильник
        roll_sum = dice1 + dice2
        sums_counts[roll_sum] += 1

    return sums_counts

def calculate_probabilities(sums_counts: dict, num_simulations: int):
    '''Обчислює ймовірність кожної суми на основі результатів симуляції'''
    probabilities = {sum_val: count / num_simulations for sum_val, count in sums_counts.items()}
    return probabilities

def display_results(probabilities: dict, sums_counts: dict, num_simulations: int):
    '''Виводить результати у вигляді таблиці та графіка'''
    # Теоретичні ймовірності для порівняння
    theoretical_probs = {
        2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
        8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
    }

    data = []
    for sum_val, prob in probabilities.items():
        data.append([
            sum_val, 
            sums_counts[sum_val], 
            f"{prob:.4f}", 
            f"{theoretical_probs[sum_val]:.4f}"
        ])
    
    df = pd.DataFrame(data, columns=["Сума", "Кількість випадінь", "Ймовірність (Монте-Карло)", "Теоретична ймовірність"])
    print(f"Результати симуляції для {num_simulations} кидків: 🎲\n")
    print(df.to_string(index=False))

    # Створення графіка
    sums = list(probabilities.keys())
    probs_values = list(probabilities.values())

    plt.figure(figsize=(10, 6))
    plt.bar(sums, probs_values, color='skyblue', edgecolor='black', label='Ймовірність (Монте-Карло)')
    
    # Додаємо лінію теоретичних ймовірностей для порівняння
    plt.plot(sums, theoretical_probs.values(), color='red', marker='o', linestyle='--', label='Теоретична ймовірність')

    plt.title('Ймовірності сум при киданні двох кубиків (Метод Монте-Карло)')
    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність')
    plt.xticks(sums)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Встановлюємо велику кількість кидків для точності
    NUM_SIMULATIONS = 1_000_000

    # Проводимо симуляцію
    counts = simulate_dice_rolls(NUM_SIMULATIONS)
    
    # Обчислюємо ймовірності
    probabilities = calculate_probabilities(counts, NUM_SIMULATIONS)
    
    # Відображаємо результати
    display_results(probabilities, counts, NUM_SIMULATIONS)