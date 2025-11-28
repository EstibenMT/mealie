# Diseño de Casos de Prueba: Endpoints de Comentarios (`/api/comments/*` y relacionados)

A continuación, se detalla el diseño de los casos de prueba de integración para los endpoints de comentarios en recetas.

## 1. Endpoint: `POST /api/comments`

Este endpoint es responsable de la creación de un nuevo comentario en una receta.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CMT-01** | **Creación Exitosa de Comentario** | 1. Crear una receta de prueba.<br>2. Autenticar un usuario.<br>3. Enviar una solicitud `POST` a `/api/comments` con el `recipe_id` y el texto del comentario. | - Código de estado: `201 Created`.<br>- El cuerpo de la respuesta contiene el comentario creado, incluyendo el texto, el `id` del usuario y el `recipeId`. |

---

## 2. Endpoint: `GET /api/recipes/{slug}/comments`

Este endpoint recupera todos los comentarios asociados a una receta específica por su `slug`.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CMT-04** | **Obtener Comentarios de una Receta** | 1. Crear una receta y añadirle uno o más comentarios.<br>2. Autenticar un usuario.<br>3. Enviar una solicitud `GET` a `/api/recipes/{slug}/comments` usando el `slug` de la receta. | - Código de estado: `200 OK`.<br>- El cuerpo de la respuesta es una lista que contiene todos los comentarios de esa receta. |
---