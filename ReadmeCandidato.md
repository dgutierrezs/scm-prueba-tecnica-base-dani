# Prueba Técnica SCM

# Ejercicio 1 - Backend

## Objetivo

Sustituir el filtrado basado en SQL libre por un sistema de filtros estructurados y seguros.

## Decisiones tomadas

### Contrato JSON

Se ha definido un contrato basado en:

```json
{
  "filters": [
    {
      "field": "status",
      "operator": "=",
      "value": "active"
    }
  ]
}
```

Esto evita permitir SQL arbitrario enviado por el cliente.

---

### Whitelist de campos

La whitelist se obtiene directamente desde el modelo ORM:

```python
column.key for column in Item.__table__.columns
```

De esta forma los campos permitidos permanecen actualizados con el modelo.

---

### Whitelist de operadores

Se permiten únicamente los siguientes operadores, me hubiera gustado poner más pero por tiempo no he podido:

```text
=
!=
>
<
LIKE
IN
IS NULL
```

Las peticiones con operadores no permitidos devuelven un error HTTP 400.

---

### Validación de errores

Cuando el cliente envía:

- Un campo inválido.
- Un operador inválido.

La API devuelve:

```text
400 Bad Request
```

junto con un mensaje descriptivo, field o operator incorrecto.

---

### Protección adicional

Se ha añadido:

- Límite máximo de filtros por petición, he puesto 10 como en el enunciado. He puesto una excepción para los 0 filtros ya que me daba error.
- Límite máximo de resultados devueltos, máximo 100.


---

# Ejercicio 2 - Frontend

## Funcionalidades implementadas

### Login

Autenticación mediante:

```text
POST /auth/login
```

---

### Gestión de token

El token JWT se almacena en:

```javascript
localStorage
```

para mantener la sesión tras recargar la página.

---

### Área protegida

Una vez autenticado, el usuario puede:

- Consultar artículos.
- Cerrar sesión.

---

### Manejo de errores

Se muestra un mensaje de error cuando las credenciales son incorrectas.

---

### Gestión de sesiones expiradas

Cuando el backend devuelve:

```text
401 Unauthorized
```

la aplicación elimina el token almacenado y redirige al usuario nuevamente a la pantalla de login. En la conclusión explico por qué lo he dejado así.

---

# Ejercicio 3 - Guía de integración

Se ha elaborado un documento PDF orientado a desarrolladores sin experiencia previa en APIs REST.

La guía explica:

- Conceptos básicos de API REST.
- Obtención de tokens.
- Uso de Swagger.
- Creación de artículos.
- Consulta de stock.
- Registro de documentos de movimiento.
- Renovación de tokens.
- Preguntas frecuentes.

El objetivo ha sido priorizar la claridad y la facilidad de aprendizaje frente a una explicación excesivamente técnica.

---

# Limitaciones y mejoras futuras

Debido al tiempo disponible se han priorizado las funcionalidades principales y no se ha realizado ninguna opcional.


# Comentarios finales

No tenía experiencia previa desarrollando aplicaciones con FastAPI ni Vue. 

Durante la realización de la prueba he priorizado comprender primero el flujo completo de la aplicación.

El tiempo empleado ha sido de aproximadamente 5 h. La mayor parte ha sido en el backend, 2 h 30 min.

En el frontend he estado 1 h 30 min y en la explicación de la API un poco más de 1 h, ya que quería complementarlo lo mejor posible.
