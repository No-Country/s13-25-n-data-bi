# s13-25-n-data-bi

Project of data

## Roles

Breyner Ocampo: DataScience, ETL

Mariela Abrego: DataScience

Leandro Luna: ML, ETL, PM

Alejandro Escudero: Data Analyst, Machine Learning

Jorge Henriquez Novoa: Data Analyst

David Ramirez Saez: Data engineer

### Activate virtual enviroment

Select source of enviroment

`
source env/Scripts/activate
`

VSC select enviroment

`
/env/scripts/python.exe
`

To install requirements:

`
pip install requirements.txt
`

To add  new requirement.

`
pip freeze > requirements.txt
`

To eliminate requirements.

`
pip freeze | cut -d "@" -f1 | xargs pip uninstall -y
`

## View

To display the project compile this command:

`
python -m streamlit run app.py
`
# Stack tecnological

Principals tools in the project

![Image text](/StackDS.png)