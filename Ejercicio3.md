MAIL EXPLICACION API

Buenos días, 
He preparado esta guía pensando en alguien que tiene experiencia desarrollando software y sistemas de negocio, pero que todavía no ha trabajado con APIs REST.
Desde el punto de vista de tu ERP, simplemente tendrás que enviar peticiones HTTP y procesar las respuestas que devuelve el sistema.
Importante
No es necesario conocer ningún lenguaje o framework específico para seguir esta guía. Todos los ejemplos se realizan desde Swagger, utilizando únicamente el navegador web. Una vez entiendas el flujo manual, podrás reproducir exactamente las mismas llamadas desde tu ERP o desde cualquier lenguaje de programación.


0. ¿Cómo funciona una API REST?
Puedes imaginar la API como un empleado del almacén que está esperando instrucciones. Tu ERP le enviará una petición:
"Créame este artículo” o "Dime cuánto stock tengo".
La API procesa la petición y devuelve una respuesta.
Todas las integraciones que realizaremos consisten en repetir ese patrón:
 Enviar una petición.
 Esperar la respuesta.
 Procesar el resultado. 
1. ¿Qué hace esta API?
Esta API representa un pequeño sistema de gestión de almacén (WMS).
Permite realizar tres operaciones principales:
Crear artículos.
Consultar una fotografía paginada del stock disponible.
Registrar movimientos de almacén (entradas, salidas y ajustes).
Piensa en ella como un servicio remoto que mantiene el inventario y al que tu ERP puede preguntarle o enviarle información.

2. Antes de programar nada
La API incorpora una interfaz interactiva que permite probar todas las operaciones desde el navegador.
Documentación Swagger:
https://forklift-fhhqfpd2edhyf7g8.westeurope-01.azurewebsites.net/docs
Documentación ReDoc:
https://forklift-fhhqfpd2edhyf7g8.westeurope-01.azurewebsites.net/redoc
Mi recomendación es que hagas todas las pruebas manualmente desde Swagger antes de escribir una sola línea de código. A continuación te explicaré paso a paso cómo probar la API y cómo validar que todo funciona correctamente.

3. Primer paso: autenticarse
Antes de acceder a los recursos protegidos debemos identificarnos.
Abre el endpoint:

POST /auth/token, presiona el desplegable que tienes a la derecha, marcado con un 1 en el screenshot de abajo. Después haz clic en "Try it out". Verás que el botón cambia automáticamente a "Cancel" y se habilita la edición de los parámetros de la petición. 
Copia y pega lo siguiente en el campo:
{
"username": "admin",
"password": "admin123"
}


Pulsa “Execute” abajo del endpoint.
La API devolverá algo parecido a:
{
"access_token": "...",
"refresh_token": "...",
"expires_in": 3600
}

El dato importante es el “access_token” cópialo .

Ahora haz clic en "Authorize", pega el access_token obtenido anteriormente y pulsa nuevamente "Authorize".
A partir de este momento podrás acceder a todos los endpoints protegidos de la API.


4. Identificar quién soy
Una vez obtenido el token, prueba:
GET /auth/me
Este endpoint sirve para verificar que la autenticación funciona correctamente.
La respuesta será algo parecido a:
{"username": "admin",
"role": "admin"
}


5. Crear un artículo
Ahora vamos a crear nuestro primer material.
Utiliza:
POST /items
Ejemplo:
{ 
"sku": "SKU-001",
"name": "Caja de tornillos M6 x 20mm.", 
"description": "Caja de 100 tornillos de acero inoxidable M6 x 20mm.", 
"unit": "box",
"initial_stock": 50 
}


Si este producto no existía, la API devolverá el artículo creado con el código 201.

En cambio, si el producto ya existía dará el Error 409 (Conflict)


¿Qué estamos haciendo realmente?
Estamos dando de alta un material que el almacén podrá gestionar. 
Importante: es una alta NUEVA para un material que no existía en la base de datos.
También es importante: únicamente los administradores pueden crear este tipo de altas.
En un entorno real podría ser:
Tornillo M6
Palet EUR
Caja de cartón
Motor eléctrico de mantenimiento

6. Consultar stock
Endpoint: 
GET /stock
¿Qué hace? 
Devuelve una fotografía del stock actual de todos los artículos registrados en el sistema.
La respuesta está paginada, por lo que, si existen muchos artículos, puede ser necesario consultar varias páginas.
Busca:
SKU
Nombre
Cantidad disponible


7. Registrar una entrada de mercancía
Ahora vamos a simular la llegada de mercancía al almacén.
Utiliza:
POST /documents.
El documento se compone de: 
header: datos generales (almacén, tipo, número, tercero, fecha…).
lines: detalle por material; cada línea afecta al stock del material_id.
Estos movimientos pueden ser de tres tipos:
INBOUND: entrada de mercancía (incrementa stock).
OUTBOUND: salida de mercancía (decrementa stock).
ADJUSTMENT: ajuste de inventario (incrementa stock).

Ejemplo:

{
"header": {
"warehouse_id": "WH-01",
"document_type": "INBOUND"
},
"lines": [
{
"material_id": "ID_DEL_ARTICULO",
"quantity": 50
}
]
}


Este documento indica:
"Han entrado 50 unidades de este material."

8. Verificar el resultado
Vuelve a llamar a:
GET /stock
Ahora deberías observar que la cantidad ha aumentado. Si tienes dudas sobre el resultado obtenido, vuelve al apartado 6 para revisar cómo consultar el stock.
Este paso es muy importante porque te permite validar que:
la llamada fue correcta
el documento se registró
el stock se actualizó

9. Registrar una salida
Para simular una expedición utiliza:
POST /documents.


Verás el ejemplo anterior, tendras que cambiar el document_type de INBOUND a: 
document_type = OUTBOUND 
La cantidad indicada se descontará del stock.
Después vuelve a consultar el inventario para comprobar el resultado.


10. Flujo recomendado para la integración
Cuando desarrolles la integración desde tu ERP te recomiendo seguir este orden:
Obtener token.
Verificar autenticación.
Crear artículo de prueba.
Consultar stock.
Crear entrada.
Verificar stock.
Crear salida.
Verificar stock nuevamente.
Si estos ocho pasos funcionan correctamente, habrás validado prácticamente toda la funcionalidad principal de la API.
Resumen
La API está diseñada alrededor de una idea muy sencilla:
Los artículos representan materiales.
El stock representa existencias.
Los documentos representan movimientos.
El stock nunca se modifica directamente; siempre cambia mediante documentos.
Una vez interiorizado ese concepto, el resto de la integración resulta bastante natural.
Quedo a tu disposición para cualquier duda que surja durante las pruebas.
Un saludo.

FAQ
¿Tengo que hacer login en cada petición? No. Una vez obtenido el access_token, deberás enviarlo en todas las peticiones protegidas mediante la cabecera: Authorization: Bearer <access_token> Cuando trabajes desde Swagger, esto se configura automáticamente pulsando el botón "Authorize". Cuando implementes la integración desde tu ERP, deberás incluir esta cabecera en cada petición autenticada. 
¿Qué ocurre si mi access_token caduca? La API proporciona un refresh_token durante el login.Puedes utilizarlo en: POST /auth/refresh para obtener un nuevo access_token sin necesidad de volver a introducir usuario y contraseña.
¿Puedo consultar stock sin estar autenticado? No. El endpoint:GET /stockrequiere autenticación previa. Si intentas acceder sin token recibirás un error de autorización.




