# Diseño de Casos de Prueba: Endpoints de Autenticación (`/api/auth/*`)

A continuación, se detalla el diseño de los casos de prueba de integración para los endpoints de autenticación del sistema Mealie.

## 1. Endpoint: `POST /api/auth/token`

Este endpoint es responsable de la autenticación del usuario y la emisión de un token de acceso.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **AUTH-01** | **Login Exitoso** | 1. Crear un usuario de prueba con credenciales conocidas (email y contraseña).<br>2. Enviar una solicitud `POST` a `/api/auth/token` con el email y la contraseña correctos en el cuerpo (`form-data`). | - Código de estado de la respuesta: `200 OK`.<br>- El cuerpo de la respuesta contiene un JSON con `access_token` y `token_type: "bearer"`.<br>- La respuesta establece una cookie `mealie.access_token`. |
| **AUTH-03** | **Login con Usuario Inexistente** | 1. Enviar una solicitud `POST` a `/api/auth/token` con un email que no corresponde a ningún usuario registrado. | - Código de estado de la respuesta: `401 Unauthorized`.<br>- No se establece ninguna cookie de acceso. |

---

## 3. Endpoint: `POST /api/auth/logout`

Este endpoint es responsable de invalidar la sesión del usuario.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **AUTH-08** | **Logout Exitoso** | 1. Iniciar sesión para obtener un token y una cookie de acceso.<br>2. Enviar una solicitud `POST` a `/api/auth/logout` con el token de acceso en la cabecera `Authorization`. | - Código de estado de la respuesta: `200 OK`.<br>- La respuesta debe contener una cabecera `set-cookie`.<br>- El header `set-cookie` debe contener `mealie.access_token=""` y `Max-Age=0` para verificar que la cookie ha sido eliminada. |