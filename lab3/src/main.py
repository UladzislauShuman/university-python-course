import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import sys
from sklearn.preprocessing import LabelEncoder

# --- настройка записи вывода в файл и консоль одновременно ---
class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # этот метод нужен для совместимости с системным выводом
        self.terminal.flush()
        self.log.flush()

# перенаправляем стандартный вывод в наш логгер
sys.stdout = Logger("output.txt")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


# --- расшифровка кодов ---
# словарь значений согласно документации german.doc
decoding_map = {
    # 1. status of existing checking account
    'A11': '< 0 DM',
    'A12': '0 <= x < 200 DM',
    'A13': '>= 200 DM',
    'A14': 'No checking account',

    # 3. credit history
    'A30': 'No credits taken',
    'A31': 'All credits paid back',
    'A32': 'Existing credits paid back',
    'A33': 'Delay in past',
    'A34': 'Critical account',

    # 4. purpose
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

    # 6. savings account/bonds
    'A61': '< 100 DM',
    'A62': '100 <= x < 500 DM',
    'A63': '500 <= x < 1000 DM',
    'A64': '>= 1000 DM',
    'A65': 'Unknown/No savings',
    
    # 7. employment present since
    'A71': 'Unemployed',
    'A72': '< 1 year',
    'A73': '1 <= x < 4 years',
    'A74': '4 <= x < 7 years',
    'A75': '>= 7 years',
}


stat_translation = {
    'count': 'Количество',
    'unique': 'Уникальных',
    'top': 'Самое частое',
    'freq': 'Частота',
    'mean': 'Среднее',
    'std': 'Станд. откл.',
    'min': 'Минимум',
    '25%': '25%',
    '50%': 'Медиана',
    '75%': '75%',
    'max': 'Максимум'
}

# --- чтение данных ---
# настройка стиля графиков
sns.set(style="whitegrid")

# ссылка на файл данных
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
url_file = "data/german.data"

# имена столбцов согласно документации 
column_names = [
    "Checking_Account_Status", # статус текущего счета
    "Duration_Months",         # продолжительность кредита в месяцах
    "Credit_History",          # кредитная история
    "Purpose",                 # цель кредита
    "Credit_Amount",           # сумма кредита
    "Savings_Account",         # сберегательный счет/облигации
    "Employment_Since",        # трудовой стаж
    "Installment_Rate",        # ставка рассрочки в % от располагаемого дохода
    "Personal_Status_Sex",     # личный статус и пол
    "Other_Debtors",           # другие должники / поручители
    "Residence_Since",         # проживание в текущем месте с
    "Property",                # имущество
    "Age",                     # возраст
    "Other_Installment_Plans", # другие планы рассрочки
    "Housing",                 # жилье
    "Existing_Credits",        # количество существующих кредитов в этом банке
    "Job",                     # работа
    "Dependents",              # количество иждивенцев
    "Telephone",               # телефон
    "Foreign_Worker",          # иностранный работник
    "Credit_Risk"              # целевая переменная (1 = Good, 2 = Bad)
]

# чтение данных
try:
    # если файл лежит локально в папке data, используем url_file, иначе url
    df = pd.read_csv(url_file, sep=' ', names=column_names)
    print("Данные успешно загружены!")
except Exception as e:
    print(f"Ошибка при загрузке данных: {e}")

print(f"\nРазмер датасета: {df.shape}")
print("\nПервые 5 строк:")
print(df.head())

# проверка на пропущенные значения
missing_values = df.isnull().sum()
print("\nПропущенные значения по столбцам:")
print(missing_values[missing_values > 0])

if df.isnull().sum().sum() == 0:
    print("\nПропущенных значений не обнаружено.")
else:
    # если бы были пропуски, здесь был бы код для их обработки
    pass

# применяем замену кодов на слова во всем датафрейме
# replace найдет в таблице значения 'A11', 'A40' и т.д. и заменит их на текст
df = df.replace(decoding_map)

print("Коды успешно заменены на понятные названия!")
print(df.head()) # проверим, что теперь там слова

# перекодируем целевую переменную: 1 -> 0 (Good), 2 -> 1 (Bad)
df['Credit_Risk'] = df['Credit_Risk'].map({1: 0, 2: 1})
print("\nЦелевая переменная 'Credit_Risk' перекодирована: 0 - Good, 1 - Bad")



# --- анализ данных и кодирование ---
# описательная статистика числовых признаков
print("\n--- Статистика по числовым признакам ---")
# describe() показывает count, mean, std, min, 25%, 50% (медиана), 75%, max
stats_num = df.describe().round(2).rename(index=stat_translation)
print(stats_num)

# анализ категориальных признаков
print("\n--- Статистика по категориальным признакам ---")
# include=['O'] выбирает только столбцы типа Object (текст)
stats_cat = df.describe(include=['O']).rename(index=stat_translation)
print(stats_cat)

# анализ целевой переменной (баланс классов)
risk_counts = df['Credit_Risk'].value_counts(normalize=True) * 100
print("\nРаспределение целевой переменной Credit_Risk")
print(f"Good (0): {risk_counts[0]:.2f}%")
print(f"Bad (1):  {risk_counts[1]:.2f}%")

# кодирование категориальных признаков
# нам нужно превратить текст (например, "A11", "A12") в числа для корреляционного анализа.
# создадим копию датафрейма для закодированных данных, чтобы не испортить оригинал для графиков
df_encoded = df.copy()
label_encoders = {}

# список категориальных столбцов
categorical_cols = df.select_dtypes(include=['object']).columns

print(f"\nКодирование следующих столбцов методом Label Encoding: {list(categorical_cols)}")

for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le # сохраняем энкодер, если вдруг нужно будет раскодировать обратно

print("Кодирование завершено. Первые 5 строк закодированного датасета:")
print(df_encoded.head())

# --- визуализация данных ---
print("\nПостроение графиков...")

# тепловая карта корреляций 
plt.figure(figsize=(14, 12))
correlation_matrix = df_encoded.corr()
# рисуем карту. annot=True добавит цифры (может быть мелко), fmt='.2f' - формат цифр
sns.heatmap(correlation_matrix, annot=True, fmt='.1f', cmap='coolwarm', linewidths=0.5)
plt.title('Матрица корреляций признаков (German Credit Data)')
plt.show()

# гистограммы распределения
# построим 3 графика в ряд: Возраст, Сумма кредита, Длительность
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(df['Age'], bins=20, kde=True, color='skyblue', ax=axes[0])
axes[0].set_title('Распределение возраста')

sns.histplot(df['Credit_Amount'], bins=20, kde=True, color='orange', ax=axes[1])
axes[1].set_title('Распределение суммы кредита')

sns.histplot(df['Duration_Months'], bins=20, kde=True, color='green', ax=axes[2])
axes[2].set_title('Распределение срока кредита (мес)')

plt.tight_layout()
plt.show()

# сравниваем распределение сумм для Good (0) и Bad (1)
plt.figure(figsize=(8, 6))
sns.boxplot(x='Credit_Risk', y='Credit_Amount', data=df, hue='Credit_Risk', palette='Set2', legend=False)
plt.title('Распределение суммы кредита в зависимости от риска')
plt.xticks([0, 1], ['Good (0)', 'Bad (1)'])
plt.show()

# barplot: статус текущего счета vs риск
# checking_account_status - сильный предиктор. посмотрим, как он влияет.
plt.figure(figsize=(10, 6))
sns.countplot(x='Checking_Account_Status', hue='Credit_Risk', data=df, palette='viridis')
plt.title('Количество дефолтов в зависимости от статуса счета')
plt.legend(title='Risk', labels=['Good', 'Bad'])
plt.show()

# --- работа с базой данных sqlite ---
print("\nРабота с SQL")

# создаем подключение к файлу (он появится в папке проекта)
conn = sqlite3.connect('german_credit.db')
cursor = conn.cursor()

# записываем датафрейм в таблицу 'credits'. 
# if_exists='replace' означает, что если таблица есть, она перезапишется.
# index=False, чтобы не писать индекс pandas как отдельную колонку.
df.to_sql('credits', conn, if_exists='replace', index=False)
print("База данных создана, данные загружены в таблицу 'credits'.")

# выполнение sql-запросов
# функция для красивого вывода результатов запроса
def run_query(query, description):
    print(f"\nЗапрос: {description}")
    print(query)
    result = pd.read_sql_query(query, conn)
    print("Результат:")
    print(result)
    return result

# сравнение среднего кредита и возраста для "good" и "bad" заемщиков
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

# топ-5 целей кредита по количеству заявок
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

# анализ крупных рискованных кредитов (сумма > 10000)
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

# закрываем соединение
conn.close()
print("\nРабота завершена.")