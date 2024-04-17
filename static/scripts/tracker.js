// script.js

// Functie om de tekst van de paragraaf aan te passen op basis van de pagina waar de bezoeker vandaan komt
function pasTekstAan() {
    var pagina = document.referrer;
    var tekstElement = document.getElementById("tekst");

    if (pagina.includes("registreren")) {
        tekstElement.textContent = "Uw account is succesvol aangemaakt! U kunt deze pagina verlaten.";
    } else if (pagina.includes("boeking")) {
        tekstElement.textContent = "Uw verblijf is succesvol geboekt! U kunt deze pagina verlaten.";
    }
    else {
        tekstElement.textContent = "Welkom! Je komt van een onbekende pagina.";
    }
}

// Roep de functie aan wanneer de pagina geladen is
window.onload = pasTekstAan;
