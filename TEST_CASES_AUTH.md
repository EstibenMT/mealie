# Diseño de Casos de Prueba: Endpoints de Autenticación (`/api/auth/*`)

A continuación, se detalla el diseño de los casos de prueba de integración para los endpoints de autenticación del sistema Mealie.

## 1. Endpoint: `POST /api/auth/token`

Este endpoint es responsable de la autenticación del usuario y la emisión de un token de acceso.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **AUTH-01** | **Login Exitoso** | 1. Crear un usuario de prueba con credenciales conocidas (email y contraseña).<br>2. Enviar una solicitud `POST` a `/api/auth/token` con el email y la contraseña correctos en el cuerpo (`form-data`). | - Código de estado de la respuesta: `200 OK`.<br>- El cuerpo de la respuesta contiene un JSON con `access_token` y `token_type: "bearer"`.<br>- La respuesta establece una cookie `mealie.access_token`. |
| **AUTH-02**| **Login con Contraseña Incorrecta** | 1. Crear un usuario de prueba.<br>2. Enviar una solicitud `POST` a `/api/auth/token` con el email correcto pero una contraseña incorrecta. | - Código de estado de la respuesta: `401 Unauthorized`.<br>- El cuerpo de la respuesta contiene un detalle del error.<br>- No se establece ninguna cookie de acceso. |
| **AUTH-03** | **Login con Usuario Inexistente** | 1. Enviar una solicitud `POST` a `/api/auth/token` con un email que no corresponde a ningún usuario registrado. | - Código de estado de la respuesta: `401 Unauthorized`.<br>- No se establece ninguna cookie de acceso. |
| **AUTH-04** | **Login de Usuario Bloqueado** | 1. Simular una condición de usuario bloqueado (si la lógica de negocio lo soporta).<br>2. Intentar iniciar sesión con las credenciales del usuario bloqueado. | - Código de estado de la respuesta: `423 Locked`. |

---

## 2. Endpoint: `GET /api/auth/refresh`

Este endpoint permite a un usuario autenticado obtener un nuevo token de acceso sin necesidad de reenviar sus credenciales.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **AUTH-05** | **Refresco de Token Exitoso** | 1. Obtener un token de acceso válido para un usuario.<br>2. Enviar una solicitud `GET` a `/api/auth/refresh` incluyendo el token de acceso válido en la cabecera `Authorization`. | - Código de estado de la respuesta: `200 OK`.<br>- El cuerpo de la respuesta contiene un JSON con un nuevo `access_token`. |
| **AUTH-06** | **Refresco con Token Inválido** | 1. Enviar una solicitud `GET` a `/api/auth/refresh` con un token de acceso inválido o malformado en la cabecera `Authorization`. | - Código de estado de la respuesta: `401 Unauthorized`. |
| **AUTH-07** | **Refresco sin Token** | 1. Enviar una solicitud `GET` a `/api/auth/refresh` sin la cabecera `Authorization`. | - Código de estado de la respuesta: `401 Unauthorized`. |

---

## 3. Endpoint: `POST /api/auth/logout`

Este endpoint es responsable de invalidar la sesión del usuario.

| ID de Prueba | Escenario de Prueba | Pasos de Ejecución | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **AUTH-08** | **Logout Exitoso** | 1. Iniciar sesión para obtener un token y una cookie de acceso.<br>2. Enviar una solicitud `POST` a `/api/auth/logout` con el token de acceso en la cabecera `Authorization`. | - Código de estado de la respuesta: `200 OK`.<br>- La respuesta debe contener una cabecera `set-cookie`.<br>- El header `set-cookie` debe contener `mealie.access_token=""` y `Max-Age=0` para verificar que la cookie ha sido eliminada. |
| **AUTH-09** | **Logout sin Token** | 1. Enviar una solicitud `POST` a `/api/auth/logout` sin un token de acceso. | - El endpoint está protegido, por lo que el resultado esperado es un código de estado `401 Unauthorized`. |
