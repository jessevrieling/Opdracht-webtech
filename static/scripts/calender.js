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

    // const dbPath = '.../database.db';
    // const hID = document.getElementById("id-field");
    // let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE);
    // var dates = new Array();
    // window.alert(toString(dates[0]));

    // const query = `SELECT date_arrival, date_departure FROM reservations where houseId = ${hID}`;
    // db.all(query, [], (rows) => {

    //     rows.forEach((row) => {
    //         dates.push(row)
    //         window.alert(row);
    //     });
    
    //     db.close();
    // });

    // for (var i = 0; i < dates.length; i++){
    //     window.alert(dates[i])
    // }

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
 document.getElementById("submit-button").addEventListener("click", function() {
        // Haal de waarden van de invoervelden op
        var arrivalDate = arrivalDateInput.value;
        var departureDate = departureDateInput.value;
        var userId = document.getElementById("user-id").value; // Als je de gebruikers-ID niet uit de URL krijgt
        var houseId = houseIdInput.value; // Gebruik het huis-ID uit de URL
        var comments = document.getElementById("comments").value;

        // Maak een object met de reserveringsgegevens
        var reservationData = {
            arrival_date: arrivalDate,
            departure_date: departureDate,
            user_id: userId,
            house_id: houseId,
            comments: comments
        };

        // Maak een HTTP POST-verzoek naar de server om de reservering toe te voegen aan de database
        fetch('/add_reservation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reservationData)
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);
            // Toon een succesbericht of eventuele foutmeldingen
            document.getElementById("error-message").textContent = data;
        })
        .catch((error) => {
            console.error('Error:', error);
            // Toon een foutmelding als er een probleem is met het maken van de reservering
            document.getElementById("error-message").textContent = 'Er is een fout opgetreden bij het maken van de reservering.';
        });
    });
});