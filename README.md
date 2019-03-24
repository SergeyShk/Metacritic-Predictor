# Metacritic Predictor

<p align="center"> 
<img src="Images/metacritic-logo.jpg" width="600">
</p>

## Описание

Проект демонстрирует работу с данными аггрегатора оценок Metacritic и включает в себя следующие этапы:
* Выгрузка данных;
* Подготовка и очистка данных;
* Описательный анализ данных;
* Регрессионный анализ по предсказанию оценок.

## Структура проекта
### Code

Содержит скрипты для скраппинга данных на языке Python:
* [metacritic_scraper.py](Code/metacritic_scraper.py) - описывает класс для получения данных о видеоиграх с сайта metacritic.com;
* mobygames_scraper.py -  описывает класс для получения данных о видеоиграх с сайта mobygames.com (в разработке);
* [data_generator.py](Code/data_generator.py) - позволяет формировать набор данных из загруженной информации.

### Notebooks

Содержит ноутбуки, визуализирующие основные аналитические и статистические выкладки:
* [Part 0. Creating Dataset.ipynb](Notebooks/Part%200.%20Creating%20Dataset.ipynb) - отображает логику формирования исходного набора данных для исследования (загрузка сырых данных, их предобработка и очистка);
* Part 1. General Analysis.ipynb (в разработке) - содержит описательный анализ данных основных аспектов исходного набора данных.

### Data
Содержит исходные наборы данных:
* metacritic_###.csv - данные с сайта metacritic.com по каждой платформе;
* metacritic.csv - подготовленный набор данных по всем платформам с сайта metacritic.com;
* mobygames.csv - данные с сайта mobygames.com по всем выходившим играм (в разработке).
