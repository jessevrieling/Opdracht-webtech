        // Haal de huidige URL op
        var currentUrl = window.location.href;

        // Zoek naar het '=' teken om de parameterwaarde te isoleren
        var idIndex = currentUrl.indexOf('=') + 1;
        var idValue = currentUrl.substring(idIndex);

        // Toon de waarde van de parameter "id" in een HTML-element
        document.getElementById('id-field').value = idValue;

        var startChar = '!'; // Het teken waarvan je wilt dat de waarde begint
        var endChar = '&';   // Het teken waarvan je wilt dat de waarde eindigt
        var startIndex = currentUrl.indexOf(startChar) + 1;
        var endIndex = currentUrl.indexOf(endChar);
        var price = currentUrl.substring(startIndex, endIndex);

        document.getElementById('price-per-day').value = price
          
