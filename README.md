# movies-recommendation

Buildar container docker com docker-compose: 
```
docker-compose -d --buld
```

Subir aplicação:
```
docker-compose up
```

Criar superusuario:
```
docker-compose run server sh -c "python manage.py createsuperuser"
```

Criar superusuario:
```
docker-compose run server sh -c "python manage.py createsuperuser"
```

Rodar script:
```
docker-compose run server sh -c "python manage.py script"
```


Abra o navegador e vá para: localhost:8000/admin