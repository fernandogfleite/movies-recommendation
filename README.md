# movies-recommendation

Buildar container docker com docker-compose: 
```
docker-compose -d --buld
```

Criar superusuario:
```
docker-compose run server sh -c "python manage.py createsuperuser"
```

Subir aplicação:
```
docker-compose up
```

Abra o navegador e vá para: localhost:8000/admin