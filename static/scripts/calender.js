document.addEventListener("DOMContentLoaded", function () {
    const stayLengthSpan = document.getElementById("stay-length");
    const today = new Date();
    today.setDate(today.getDate());
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    let disabledDates;
    const arrivalDateInput = flatpickr('#arrival-date', {
        minDate: today,
        onChange: updateStayLength
    });
    const departureDateInput = flatpickr('#departure-date', {
        minDate: tomorrow,
        onChange: updateStayLength
    });

    fetch('/disable_dates?hID=' + document.getElementById("id-field").value)
        .then(response => response.json())
        .then(data => {
            disabledDates = data.map(dateStr => new Date(dateStr));
            arrivalDateInput.set('disable', disabledDates); // Set disabled dates for arrival date picker
            departureDateInput.set('disable', disabledDates); // Set disabled dates for departure date picker
        })
        .catch(error => window.alert('Error fetching disabled dates:', error));

    function updateStayLength() {
        window.alert("CHANGED");

        const arrivalStr = arrivalDateInput.input.value;
        const departureStr = departureDateInput.input.value;

        const arrival = new Date(arrivalStr);
        const departure = new Date(departureStr);

        arrivalDateInput.set('minDate', today);
        departureDateInput.set('minDate', tomorrow);

        arrivalDateInput.set('disable', disabledDates);
        departureDateInput.set('disable', disabledDates);

        window.alert("WORK");

        const nextDay = new Date(arrival);
        nextDay.setDate(nextDay.getDate() + 1);

        if (arrival) {
            departureDateInput.set('minDate', nextDay);

            let lowestDate = new Date();
            lowestDate.setFullYear(lowestDate.getFullYear() + 1);
            disabledDates.forEach(date => {
                if (date > arrival && date < lowestDate)
                    lowestDate = date;
            });
            departureDateInput.set('maxDate', lowestDate);
            window.alert(lowestDate);
        }

        if (arrival && departure) {
            if (departure <= arrival) {

                departureDateInput.setDate(null);
                departureDateInput.set('minDate', nextDay);

                window.alert("Should reset departure")
            }
        }
    }

    document.getElementById("submit-button").addEventListener("click", function () {
        // Haal de waarden van de invoervelden op
        var arrivalDate = arrivalDateInput.input.value;
        var departureDate = departureDateInput.input.value;
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