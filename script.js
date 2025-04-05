document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const action = params.get("action") || "login";
    const formTitle = document.getElementById("form-title");
    const formButton = document.querySelector("#auth-form button");
    const toggleText = document.getElementById("toggle-form");

    function updateForm(mode) {
        if (mode === "register") {
            formTitle.textContent = "Rejestracja";
            formButton.textContent = "Zarejestruj";
            toggleText.innerHTML = "Masz już konto? <a href='#'>Zaloguj się</a>";
        } else {
            formTitle.textContent = "Logowanie";
            formButton.textContent = "Zaloguj";
            toggleText.innerHTML = "Nie masz konta? <a href='#'>Zarejestruj się</a>";
        }
    }

    updateForm(action);

    toggleText.addEventListener("click", (e) => {
        e.preventDefault();
        const newAction = action === "login" ? "register" : "login";
        window.location.search = `?action=${newAction}`;
    });

    document.getElementById("auth-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const response = await fetch("http://127.0.0.1:5000/auth", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, action }),
        });

        const data = await response.json();
        alert(data.message);
        if (data.success) window.location.href = "index.html";
    });
});
