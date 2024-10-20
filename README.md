# Navigable Graphs Python
Исследовательский инструмент на базе Python для изучения навигационных графов для поиска ближайших соседей

Использование набора данных SIFT:
```
python test-hnsw.py --dataset synthetic --K 20 --k 5 --dim 3 --n 500 --nq 100 --ef 20 --M 2
```
Результаты на наборе данных SIFT
HNSW из файла
![image](https://github.com/user-attachments/assets/e826a092-0d71-439a-a973-771e53893255)


модернизированный HNSW
![image](https://github.com/user-attachments/assets/bdbfdfff-1d8f-4d1f-ac1a-6d012e7c76a5)

Немного повысился recall, снизилось avg calc

Использование синтетических данных с 3D-векторами:
```
python test-hnsw.py --dataset synthetic --K 20 --k 5 --dim 3 --n 500 --nq 100 --ef 20 --M 2
```
Результаты на синтетических данных
HNSW из файла
![image](https://github.com/user-attachments/assets/5a756751-20d0-45b0-aec6-e595730b1195)

модернизированный HNSW
![image](https://github.com/user-attachments/assets/06170f24-0e00-4159-9880-055d5a2671aa)

recall остался 1.0, снизилось avg calc

