const API_URL = "http://localhost:3000";

const registerForm =
    document.getElementById("registerForm");

const loginForm =
    document.getElementById("loginForm");

const registerMessage =
    document.getElementById("registerMessage");

const loginMessage =
    document.getElementById("loginMessage");

function mostrarMensaje(elemento, texto, tipo) {

    elemento.textContent = texto;

    elemento.className =
        `message ${tipo}`;
}

mostrarMensaje(
    loginMessage,
    "Autenticación satisfactoria",
    "success"
);

mostrarMensaje(
    loginMessage,
    "Error en la autenticación",
    "error"
);

registerForm.addEventListener(
    "submit",
    async (event) => {

        // Evitamos que el navegador recargue la página.
        event.preventDefault();

        // Capturamos los datos escritos por el usuario.
        const datos = {

            nombre:
                document.getElementById("nombre").value,

            correo:
                document.getElementById(
                    "registroCorreo"
                ).value,

            password:
                document.getElementById(
                    "registroPassword"
                ).value
        };


        try {

            // Enviamos los datos al backend.
            const respuesta = await fetch(
                `${API_URL}/api/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(datos)
                }
            );


            // Convertimos la respuesta en JSON.
            const resultado =
                await respuesta.json();


            // Revisamos si fue exitoso.
            if (respuesta.ok) {

                mostrarMensaje(
                    registerMessage,
                    resultado.mensaje,
                    "success"
                );

                registerForm.reset();

            } else {

                mostrarMensaje(
                    registerMessage,
                    resultado.error,
                    "error"
                );
            }


        } catch (error) {

            mostrarMensaje(
                registerMessage,
                "No fue posible conectar con el servidor.",
                "error"
            );

        }

    }
);

loginForm.addEventListener(
    "submit",
    async (event) => {

        // Evitamos recargar la página.
        event.preventDefault();


        // Capturamos correo y contraseña.
        const datos = {

            correo:
                document.getElementById(
                    "loginCorreo"
                ).value,

            password:
                document.getElementById(
                    "loginPassword"
                ).value
        };


        try {

            // Enviamos las credenciales al backend.
            const respuesta = await fetch(
                `${API_URL}/api/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(datos)
                }
            );


            // Convertimos la respuesta a JSON.
            const resultado =
                await respuesta.json();


            // Si el servidor respondió correctamente.
            if (respuesta.ok) {

                mostrarMensaje(
                    loginMessage,
                    resultado.mensaje,
                    "success"
                );

            } else {

                // Si las credenciales son incorrectas.
                mostrarMensaje(
                    loginMessage,
                    resultado.error,
                    "error"
                );
            }


        } catch (error) {

            // Error de conexión.
            mostrarMensaje(
                loginMessage,
                "No fue posible conectar con el servidor.",
                "error"
            );

        }

    }
);