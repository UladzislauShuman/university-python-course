# Как запустить
- перейдите в директорию `src`
- настроить виртуальное окружение
    - `python -m venv venv`
    - `source venv/bin/activate`
- загрузить все зависимости
    - `pip install -r requirements.txt`

# Пример работы программы
```
(.venv) (base) vladsuman@MacBook-Pro-Vlad-2 src % python main.py           
Данные успешно загружены!

Размер датасета: (1000, 21)

Первые 5 строк:
  Checking_Account_Status  Duration_Months Credit_History Purpose  Credit_Amount Savings_Account Employment_Since  ...  Housing Existing_Credits   Job  Dependents Telephone  Foreign_Worker Credit_Risk
0                     A11                6            A34     A43           1169             A65              A75  ...     A152                2  A173           1      A192            A201           1
1                     A12               48            A32     A43           5951             A61              A73  ...     A152                1  A173           1      A191            A201           2
2                     A14               12            A34     A46           2096             A61              A74  ...     A152                1  A172           2      A191            A201           1
3                     A11               42            A32     A42           7882             A61              A74  ...     A153                1  A173           2      A191            A201           1
4                     A11               24            A33     A40           4870             A61              A73  ...     A153                2  A173           2      A191            A201           2

[5 rows x 21 columns]

Пропущенные значения по столбцам:
Series([], dtype: int64)

Пропущенных значений не обнаружено.

Целевая переменная 'Credit_Risk' перекодирована: 0 - Good, 1 - Bad

--- Статистика по числовым признакам ---
       Duration_Months  Credit_Amount  Installment_Rate  Residence_Since      Age  Existing_Credits  Dependents  Credit_Risk
count          1000.00        1000.00           1000.00          1000.00  1000.00           1000.00     1000.00      1000.00
mean             20.90        3271.26              2.97             2.84    35.55              1.41        1.16         0.30
std              12.06        2822.74              1.12             1.10    11.38              0.58        0.36         0.46
min               4.00         250.00              1.00             1.00    19.00              1.00        1.00         0.00
25%              12.00        1365.50              2.00             2.00    27.00              1.00        1.00         0.00
50%              18.00        2319.50              3.00             3.00    33.00              1.00        1.00         0.00
75%              24.00        3972.25              4.00             4.00    42.00              2.00        1.00         1.00
max              72.00       18424.00              4.00             4.00    75.00              4.00        2.00         1.00

--- Статистика по категориальным признакам ---
       Checking_Account_Status Credit_History Purpose Savings_Account Employment_Since Personal_Status_Sex Other_Debtors Property Other_Installment_Plans Housing   Job Telephone Foreign_Worker
count                     1000           1000    1000            1000             1000                1000          1000     1000                    1000    1000  1000      1000           1000
unique                       4              5      10               5                5                   4             3        4                       3       3     4         2              2
top                        A14            A32     A43             A61              A73                 A93          A101     A123                    A143    A152  A173      A191           A201
freq                       394            530     280             603              339                 548           907      332                     814     713   630       596            963

Распределение целевой переменной Credit_Risk
Good (0): 70.00%
Bad (1):  30.00%

Кодирование следующих столбцов методом Label Encoding: ['Checking_Account_Status', 'Credit_History', 'Purpose', 'Savings_Account', 'Employment_Since', 'Personal_Status_Sex', 'Other_Debtors', 'Property', 'Other_Installment_Plans', 'Housing', 'Job', 'Telephone', 'Foreign_Worker']
Кодирование завершено. Первые 5 строк закодированного датасета:
   Checking_Account_Status  Duration_Months  Credit_History  Purpose  Credit_Amount  Savings_Account  Employment_Since  ...  Housing  Existing_Credits  Job  Dependents  Telephone  Foreign_Worker  Credit_Risk
0                        0                6               4        4           1169                4                 4  ...        1                 2    2           1          1               0            0
1                        1               48               2        4           5951                0                 2  ...        1                 1    2           1          0               0            1
2                        3               12               4        7           2096                0                 3  ...        1                 1    1           2          0               0            0
3                        0               42               2        3           7882                0                 3  ...        2                 1    2           2          0               0            0
4                        0               24               3        0           4870                0                 2  ...        2                 2    2           2          0               0            1

[5 rows x 21 columns]

Построение графиков...
2025-12-03 13:09:27.515 python[57667:5052457] +[IMKClient subclass]: chose IMKClient_Modern
2025-12-03 13:09:27.515 python[57667:5052457] +[IMKInputSession subclass]: chose IMKInputSession_Modern
/Users/vladsuman/git/famcs/university-python-course/lab3/src/main.py:134: FutureWarning: 

Passing `palette` without assigning `hue` is deprecated and will be removed in v0.14.0. Assign the `x` variable to `hue` and set `legend=False` for the same effect.

  sns.boxplot(x='Credit_Risk', y='Credit_Amount', data=df, palette='Set2')

Работа с SQL
База данных создана, данные загружены в таблицу 'credits'.

Запрос: Агрегация по статусу риска (0=Good, 1=Bad)

SELECT 
    Credit_Risk,
    COUNT(*) as Client_Count,
    ROUND(AVG(Credit_Amount), 2) as Avg_Credit_Amount,
    ROUND(AVG(Age), 1) as Avg_Age
FROM credits
GROUP BY Credit_Risk

Результат:
   Credit_Risk  Client_Count  Avg_Credit_Amount  Avg_Age
0            0           700            2985.46     36.2
1            1           300            3938.13     34.0

Запрос: Топ-5 целей кредитования

SELECT 
    Purpose, 
    COUNT(*) as Count, 
    ROUND(AVG(Credit_Amount), 2) as Avg_Amount
FROM credits 
GROUP BY Purpose 
ORDER BY Count DESC 
LIMIT 5

Результат:
  Purpose  Count  Avg_Amount
0     A43    280     2487.65
1     A40    234     3063.03
2     A42    181     3066.99
3     A41    103     5370.22
4     A49     97     4158.04

Запрос: Выборка крупных невозвратных кредитов (> 10 000 DM)

SELECT 
    Purpose, 
    Credit_Amount, 
    Duration_Months, 
    Age 
FROM credits 
WHERE Credit_Amount > 10000 AND Credit_Risk = 1
ORDER BY Credit_Amount DESC

Результат:
   Purpose  Credit_Amount  Duration_Months  Age
0     A410          18424               48   32
1      A49          15945               54   58
2      A49          15672               48   23
3      A40          14896                6   68
4     A410          14782               60   60
5      A40          14555                6   23
6      A49          14421               48   25
7      A40          14318               36   57
8      A40          14027               60   27
9      A41          12976               18   38
10     A40          12680               21   30
11     A46          12612               36   47
12     A41          12579               24   44
13     A40          12389               36   37
14     A45          11998               30   34
15    A410          11938               24   39
16     A49          11816               45   29
17     A41          11590               48   24
18     A41          11560               24   23
19    A410          11328               24   29
20     A42          10974               36   26
21     A43          10961               48   27
22     A41          10297               48   39
23     A40          10127               48   44

Работа завершена.
```