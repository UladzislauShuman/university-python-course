import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.preprocessing import LabelEncoder


# --- РАСШИФРОВКА КОДОВ ---
# Словарь значений согласно документации german.doc
decoding_map = {
    # 1. Status of existing checking account
    'A11': '< 0 DM',
    'A12': '0 <= x < 200 DM',
    'A13': '>= 200 DM',
    'A14': 'No checking account',

    # 3. Credit history
    'A30': 'No credits taken',
    'A31': 'All credits paid back',
    'A32': 'Existing credits paid back',
    'A33': 'Delay in past',
    'A34': 'Critical account',

    # 4. Purpose
    'A40': 'Car (new)',
    'A41': 'Car (used)',
    'A42': 'Furniture/Equipment',
    'A43': 'Radio/TV',
    'A44': 'Domestic appliances',
    'A45': 'Repairs',
    'A46': 'Education',
    'A47': 'Vacation',
    'A48': 'Retraining',
    'A49': 'Business',
    'A410': 'Others',

    # 6. Savings account/bonds
    'A61': '< 100 DM',
    'A62': '100 <= x < 500 DM',
    'A63': '500 <= x < 1000 DM',
    'A64': '>= 1000 DM',
    'A65': 'Unknown/No savings',
    
    # 7. Employment present since
    'A71': 'Unemployed',
    'A72': '< 1 year',
    'A73': '1 <= x < 4 years',
    'A74': '4 <= x < 7 years',
    'A75': '>= 7 years',
}


# ЧТЕНИЕ ДАННЫХ
# Настройка стиля графиков
sns.set(style="whitegrid")

# Ссылка на файл данных
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"

# Имена столбцов согласно документации 
column_names = [
    "Checking_Account_Status", # Статус текущего счета
    "Duration_Months",         # Продолжительность кредита в месяцах
    "Credit_History",          # Кредитная история
    "Purpose",                 # Цель кредита
    "Credit_Amount",           # Сумма кредита
    "Savings_Account",         # Сберегательный счет/облигации
    "Employment_Since",        # Трудовой стаж
    "Installment_Rate",        # Ставка рассрочки в % от располагаемого дохода
    "Personal_Status_Sex",     # Личный статус и пол
    "Other_Debtors",           # Другие должники / поручители
    "Residence_Since",         # Проживание в текущем месте с
    "Property",                # Имущество
    "Age",                     # Возраст
    "Other_Installment_Plans", # Другие планы рассрочки
    "Housing",                 # Жилье
    "Existing_Credits",        # Количество существующих кредитов в этом банке
    "Job",                     # Работа
    "Dependents",              # Количество иждивенцев
    "Telephone",               # Телефон
    "Foreign_Worker",          # Иностранный работник
    "Credit_Risk"              # Целевая переменная (1 = Good, 2 = Bad)
]

# Чтение данных
try:
    df = pd.read_csv(url, sep=' ', names=column_names)
    print("Данные успешно загружены!")
except Exception as e:
    print(f"Ошибка при загрузке данных: {e}")

print(f"\nРазмер датасета: {df.shape}")
print("\nПервые 5 строк:")
print(df.head())

# Проверка на пропущенные значения
missing_values = df.isnull().sum()
print("\nПропущенные значения по столбцам:")
print(missing_values[missing_values > 0])

if df.isnull().sum().sum() == 0:
    print("\nПропущенных значений не обнаружено.")
else:
    # Если бы были пропуски, здесь был бы код для их обработки
    pass

# Применяем замену кодов на слова во всем датафрейме
# replace найдет в таблице значения 'A11', 'A40' и т.д. и заменит их на текст
df = df.replace(decoding_map)

print("Коды успешно заменены на понятные названия!")
print(df.head()) # Проверим, что теперь там слова

# перекодируем целевую переменную: 1 -> 0 (Good), 2 -> 1 (Bad)
df['Credit_Risk'] = df['Credit_Risk'].map({1: 0, 2: 1})
print("\nЦелевая переменная 'Credit_Risk' перекодирована: 0 - Good, 1 - Bad")



# АНАЛИЗ ДАННЫХ И КОДИРОВАНИЕ
# Описательная статистика числовых признаков
print("\n--- Статистика по числовым признакам ---")
# describe() показывает count, mean, std, min, 25%, 50% (медиана), 75%, max
print(df.describe().round(2))

# Анализ категориальных признаков
print("\n--- Статистика по категориальным признакам ---")
# include=['O'] выбирает только столбцы типа Object (текст)
print(df.describe(include=['O']))

# Анализ целевой переменной (баланс классов)
risk_counts = df['Credit_Risk'].value_counts(normalize=True) * 100
print("\nРаспределение целевой переменной Credit_Risk")
print(f"Good (0): {risk_counts[0]:.2f}%")
print(f"Bad (1):  {risk_counts[1]:.2f}%")

# Кодирование категориальных признаков
# Нам нужно превратить текст (например, "A11", "A12") в числа для корреляционного анализа.
# Создадим копию датафрейма для закодированных данных, чтобы не испортить оригинал для графиков
df_encoded = df.copy()
label_encoders = {}

# Список категориальных столбцов
categorical_cols = df.select_dtypes(include=['object']).columns

print(f"\nКодирование следующих столбцов методом Label Encoding: {list(categorical_cols)}")

for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le # Сохраняем энкодер, если вдруг нужно будет раскодировать обратно

print("Кодирование завершено. Первые 5 строк закодированного датасета:")
print(df_encoded.head())

# ВИЗУАЛИЗАЦИЯ ДАННЫХ
print("\nПостроение графиков...")

# Тепловая карта корреляций 
plt.figure(figsize=(14, 12))
correlation_matrix = df_encoded.corr()
# Рисуем карту. annot=True добавит цифры (может быть мелко), fmt='.2f' - формат цифр
sns.heatmap(correlation_matrix, annot=True, fmt='.1f', cmap='coolwarm', linewidths=0.5)
plt.title('Матрица корреляций признаков (German Credit Data)')
plt.show()

# Гистограммы распределения
# Построим 3 графика в ряд: Возраст, Сумма кредита, Длительность
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(df['Age'], bins=20, kde=True, color='skyblue', ax=axes[0])
axes[0].set_title('Распределение возраста')

sns.histplot(df['Credit_Amount'], bins=20, kde=True, color='orange', ax=axes[1])
axes[1].set_title('Распределение суммы кредита')

sns.histplot(df['Duration_Months'], bins=20, kde=True, color='green', ax=axes[2])
axes[2].set_title('Распределение срока кредита (мес)')

plt.tight_layout()
plt.show()

# Сравниваем распределение сумм для Good (0) и Bad (1)
plt.figure(figsize=(8, 6))
sns.boxplot(x='Credit_Risk', y='Credit_Amount', data=df, hue='Credit_Risk', palette='Set2', legend=False)
plt.title('Распределение суммы кредита в зависимости от риска')
plt.xticks([0, 1], ['Good (0)', 'Bad (1)'])
plt.show()

# Barplot: Статус текущего счета vs Риск
# Checking_Account_Status - сильный предиктор. Посмотрим, как он влияет.
plt.figure(figsize=(10, 6))
sns.countplot(x='Checking_Account_Status', hue='Credit_Risk', data=df, palette='viridis')
plt.title('Количество дефолтов в зависимости от статуса счета')
plt.legend(title='Risk', labels=['Good', 'Bad'])
plt.show()

# РАБОТА С БАЗОЙ ДАННЫХ SQLITE
print("\nРабота с SQL")

# Создаем подключение к файлу (он появится в папке проекта)
conn = sqlite3.connect('german_credit.db')
cursor = conn.cursor()

# Записываем датафрейм в таблицу 'credits'. 
# if_exists='replace' означает, что если таблица есть, она перезапишется.
# index=False, чтобы не писать индекс pandas как отдельную колонку.
df.to_sql('credits', conn, if_exists='replace', index=False)
print("База данных создана, данные загружены в таблицу 'credits'.")

# Выполнение SQL-запросов
# Функция для красивого вывода результатов запроса
def run_query(query, description):
    print(f"\nЗапрос: {description}")
    print(query)
    result = pd.read_sql_query(query, conn)
    print("Результат:")
    print(result)
    return result

# Сравнение среднего кредита и возраста для "Good" и "Bad" заемщиков
query1 = """
SELECT 
    Credit_Risk,
    COUNT(*) as Client_Count,
    ROUND(AVG(Credit_Amount), 2) as Avg_Credit_Amount,
    ROUND(AVG(Age), 1) as Avg_Age
FROM credits
GROUP BY Credit_Risk
"""
run_query(query1, "Агрегация по статусу риска (0=Good, 1=Bad)")

# Топ-5 целей кредита по количеству заявок
query2 = """
SELECT 
    Purpose, 
    COUNT(*) as Count, 
    ROUND(AVG(Credit_Amount), 2) as Avg_Amount
FROM credits 
GROUP BY Purpose 
ORDER BY Count DESC 
LIMIT 5
"""
run_query(query2, "Топ-5 целей кредитования")

# Анализ крупных рискованных кредитов (сумма > 10000)
query3 = """
SELECT 
    Purpose, 
    Credit_Amount, 
    Duration_Months, 
    Age 
FROM credits 
WHERE Credit_Amount > 10000 AND Credit_Risk = 1
ORDER BY Credit_Amount DESC
"""
run_query(query3, "Выборка крупных невозвратных кредитов (> 10 000 DM)")

# Закрываем соединение
conn.close()
print("\nРабота завершена.")