document.addEventListener("DOMContentLoaded", function () {
   const CONSENT_NAME = "_ga_consent";
   const ONE_YEAR = 60 * 60 * 24 * 365;
   const THEME_COOKIE = "_theme"; // Nombre de la cookie para el tema

   function getCookie(name) {
       return document.cookie
           .split("; ")
           .find(row => row.startsWith(name + "="))
           ?.split("=")[1] || "";
   }

   // Comprobar el consentimiento de cookies
   if (getCookie(CONSENT_NAME) === "true") {
       loadGA();
   } else {
       const banner = document.getElementById("cookie-banner");
       if (banner) {
           banner.style.display = "block";
       }

       document.getElementById("btn-accept")?.addEventListener("click", () => {
           document.cookie = `${CONSENT_NAME}=true; max-age=${ONE_YEAR}; path=/; samesite=Lax`;
           loadGA();
           if (banner) banner.remove();
       });

       document.getElementById("btn-reject")?.addEventListener("click", () => {
           if (banner) banner.remove();
           document.cookie = `${CONSENT_NAME}=false; max-age=${ONE_YEAR}; path=/; samesite=Lax`;
       });
   }


   function loadGA() {
       if (window.GA_INITIALIZED) return;
       window.GA_INITIALIZED = true;

       const script = document.createElement("script");
       script.src = "https://www.googletagmanager.com/gtag/js?id=G-XXXXX"; // Reemplazar por tu ID de GA
       script.async = true;
       document.head.appendChild(script);

       window.dataLayer = window.dataLayer || [];
       function gtag() { dataLayer.push(arguments); }
       gtag('js', new Date());
       gtag('config', 'G-XXXXX', { anonymize_ip: true }); // Reemplazar con tu ID
   }


   const savedTheme = getCookie(THEME_COOKIE);
   if (savedTheme === "dark") {
       document.body.classList.add("dark-mode");
       const themeButton = document.getElementById("btn-theme-toggle");
       if (themeButton) {
           themeButton.textContent = "Modo Claro";
       }
   } else {
       document.body.classList.remove("dark-mode");
       const themeButton = document.getElementById("btn-theme-toggle");
       if (themeButton) {
           themeButton.textContent = "Modo Oscuro";
       }
   }

   
   const themeButton = document.getElementById("btn-theme-toggle");
   if (themeButton) {
       themeButton.addEventListener("click", () => {
           const isDarkMode = document.body.classList.toggle("dark-mode");
           document.cookie = `${THEME_COOKIE}=${isDarkMode ? "dark" : "light"}; max-age=${ONE_YEAR}; path=/; samesite=Lax`;

           // Cambiar el texto del botón
           themeButton.textContent = isDarkMode ? "Modo Claro" : "Modo Oscuro";
       });
   }
});
