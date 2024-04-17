        // Haal de huidige URL op
        var currentUrl = window.location.href;

        // Zoek naar het '=' teken om de parameterwaarde te isoleren
        var idIndex = currentUrl.indexOf('=') + 1;
        var idValue = currentUrl.substring(idIndex);

        // Toon de waarde van de parameter "id" in een HTML-element
        document.getElementById('id-field').value = idValue;