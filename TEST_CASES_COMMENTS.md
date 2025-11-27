# Diseño de Casos de Prueba: Endpoints de Comentarios (`/api/comments/*` y relacionados)

A continuación, se detalla el diseño de los casos de prueba de integración para los endpoints de comentarios en recetas.

## 1. Endpoint: `POST /api/comments`

Este endpoint es responsable de la creación de un nuevo comentario en una receta.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CMT-01** | **Creación Exitosa de Comentario** | 1. Crear una receta de prueba.<br>2. Autenticar un usuario.<br>3. Enviar una solicitud `POST` a `/api/comments` con el `recipe_id` y el texto del comentario. | - Código de estado: `201 Created`.<br>- El cuerpo de la respuesta contiene el comentario creado, incluyendo el texto, el `id` del usuario y el `recipeId`. |
| **CMT-02**| **Crear Comentario sin Autenticación** | 1. Crear una receta de prueba.<br>2. Enviar una solicitud `POST` a `/api/comments` sin un token de autenticación. | - Código de estado: `401 Unauthorized`. |
| **CMT-03** | **Crear Comentario para Receta Inexistente** | 1. Autenticar un usuario.<br>2. Enviar una solicitud `POST` a `/api/comments` con un `recipe_id` que no existe. | - Código de estado: `422 Unprocessable Entity` o `500 Internal Server Error` (dependiendo de la validación de la base de datos). |

---

## 2. Endpoint: `GET /api/recipes/{slug}/comments`

Este endpoint recupera todos los comentarios asociados a una receta específica por su `slug`.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CMT-04** | **Obtener Comentarios de una Receta** | 1. Crear una receta y añadirle uno o más comentarios.<br>2. Autenticar un usuario.<br>3. Enviar una solicitud `GET` a `/api/recipes/{slug}/comments` usando el `slug` de la receta. | - Código de estado: `200 OK`.<br>- El cuerpo de la respuesta es una lista que contiene todos los comentarios de esa receta. |
| **CMT-05** | **Obtener Comentarios de una Receta sin Comentarios** | 1. Crear una receta sin comentarios.<br>2. Autenticar un usuario.<br>3. Enviar una solicitud `GET` a `/api/recipes/{slug}/comments`. | - Código de estado: `200 OK`.<br>- El cuerpo de la respuesta es una lista vacía `[]`. |

---

## 3. Endpoint: `PUT /api/comments/{item_id}`

Este endpoint actualiza el contenido de un comentario existente.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CMT-06** | **Actualizar Comentario Propio** | 1. Un usuario crea un comentario en una receta.<br>2. El mismo usuario envía una solicitud `PUT` a `/api/comments/{item_id}` con el nuevo texto. | - Código de estado: `200 OK`.<br>- El cuerpo de la respuesta contiene el comentario con el texto actualizado. |


---

## 4. Endpoint: `DELETE /api/comments/{item_id}`

Este endpoint elimina un comentario existente.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CMT-09** | **Eliminar Comentario Propio** | 1. Un usuario crea un comentario.<br>2. El mismo usuario envía una solicitud `DELETE` a `/api/comments/{item_id}`. | - Código de estado: `200 OK`.<br>- Una solicitud posterior `GET` al mismo `item_id` debe devolver `404 Not Found`. |
| **CMT-10**| **Intentar Eliminar Comentario Ajeno (sin ser admin)** | 1. El `Usuario A` crea un comentario.<br>2. El `Usuario B` (un usuario diferente, no admin, **pero en el mismo grupo que el Usuario A**) intenta enviar una solicitud `DELETE` para eliminar el comentario del `Usuario A`. | - Código de estado: `403 Forbidden`. |
| **CMT-11**| **Un Administrador Elimina un Comentario Ajeno** | 1. Un usuario normal (`Usuario A`) crea un comentario.<br>2. Un usuario `admin` (**que está en el mismo grupo que el Usuario A**) envía una solicitud `DELETE` para eliminar dicho comentario. | - Código de estado: `200 OK`.<br>- Una solicitud posterior `GET` al mismo `item_id` debe devolver `404 Not Found`. |

---

## 5. Endpoint: `GET /api/comments/{item_id}`

Este endpoint recupera un comentario específico por su ID.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CMT-12** | **Obtener un Comentario por ID** | 1. Crear un comentario y obtener su `id`.<br>2. Autenticar un usuario.<br>3. Enviar una solicitud `GET` a `/api/comments/{item_id}`. | - Código de estado: `200 OK`.<br>- El cuerpo de la respuesta contiene los datos del comentario solicitado. |
| **CMT-13** | **Obtener Comentario Inexistente por ID** | 1. Autenticar un usuario.<br>2. Enviar una solicitud `GET` a `/api/comments/{item_id}` con un UUID que no corresponde a ningún comentario. | - Código de estado: `404 Not Found`. |
