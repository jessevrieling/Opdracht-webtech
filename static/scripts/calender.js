document.addEventListener("DOMContentLoaded", function() {
    const arrivalDateInput = document.getElementById("arrival-date");
    const departureDateInput = document.getElementById("departure-date");
    const stayLengthSpan = document.getElementById("stay-length");

    // Stel minimum aankomstdatum in op vandaag
    const today = new Date();
    today.setDate(today.getDate() + 1);
    arrivalDateInput.min = today.toISOString().split('T')[0];

    // Stel minimum vertrekdatum in op overmorgen
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 2);
    departureDateInput.min = tomorrow.toISOString().split('T')[0];

    // Luister naar veranderingen in de aankomstdatum
    arrivalDateInput.addEventListener("change", updateStayLength);

    // Luister naar veranderingen in de vertrekdatum
    departureDateInput.addEventListener("change", updateStayLength);

    // Functie om de lengte van het verblijf bij te werken
    function updateStayLength() {
        const arrivalDate = new Date(arrivalDateInput.value);
        const departureDate = new Date(departureDateInput.value);

        // Update de 'min' attribuut van de vertrekdatum input om eerdere data te blokkeren
        departureDateInput.min = arrivalDateInput.value;
        
        // Update de 'max' attribuut van de aankomstdatum input om latere data te blokkeren
        arrivalDateInput.max = departureDateInput.value;
        
        // Stel minimum vertrekdatum in op minimaal een dag na aankomstdatum
        const minDepartureDate = new Date(arrivalDate);
        minDepartureDate.setDate(minDepartureDate.getDate() + 1);
        departureDateInput.min = minDepartureDate.toISOString().slice(0, 10);

        // Stel maximum aankomstdatum in op maximaal een dag voor vertrekdatum
        const maxArrivalDate = new Date(departureDate);
        maxArrivalDate.setDate(maxArrivalDate.getDate() - 1);
        arrivalDateInput.max = maxArrivalDate.toISOString().slice(0, 10);

        // Voer alleen de berekening uit als beide datums zijn geselecteerd en de vertrekdatum niet eerder is dan de aankomstdatum
        if (arrivalDate && departureDate && departureDate >= arrivalDate) {
            const differenceInTime = departureDate.getTime() - arrivalDate.getTime();
            const differenceInDays = differenceInTime / (1000 * 3600 * 24);
            stayLengthSpan.textContent = differenceInDays + " dagen";
        } else {
            stayLengthSpan.textContent = "-";
        }


    }
});
