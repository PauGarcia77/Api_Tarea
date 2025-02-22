# Activitat Git

El projecte és una primera aproximació a les API RestFul

## Instal·lació

Per poder instal·lar el projecte s'haurà de tenir:
* La versió 3.13 de python
* Instal·lar [Pipenv](https://pipenv-es.readthedocs.io/es/latest/)

Instal·lar els paquets de python:
```bash
pipenv install --dev
```

Activar entorn virtual:
```bash
pipenv shell
```

Per executar el projecte:
```bash
uvicorn main:app --reload
```
