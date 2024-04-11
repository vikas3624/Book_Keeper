function addBook() {
    
    fetch('/addBook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pet_owner: petOwner,
            pet_name: petName,
            appointment_time: appointmentTime,
            address: address, // Include address in the request
            appointment_type: appointmentType // Include appointment type in the request
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));

}
/*function scheduleAppointment() {
    const petOwner = document.getElementById('pet-owner').value;
    const petName = document.getElementById('pet-name').value;
    const appointmentTime = document.getElementById('appointment-time').value;
    const address = document.getElementById('address').value; // Get address value
    const appointmentType = document.getElementById('appointment-type').value; // Get appointment type value

    fetch('/schedule_appointment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pet_owner: petOwner,
            pet_name: petName,
            appointment_time: appointmentTime,
            address: address, // Include address in the request
            appointment_type: appointmentType // Include appointment type in the request
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));

}
function cancelAppointment() {
    const appointmentId = document.getElementById('appointment-id').value;

    fetch('/cancel_appointment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            appointment_id: appointmentId
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

function displaySchedule() {
    fetch('/display_schedule')
    .then(response => response.json())
    .then(data => {
        const appointmentsList = document.getElementById('appointments');
        appointmentsList.innerHTML = '';

        data.appointments.forEach(appointment => {
            const listItem = document.createElement('li');
            listItem.textContent = `ID: ${appointment[0]}, Pet Owner: ${appointment[1]}, Pet Name: ${appointment[2]}, Time: ${appointment[3]} , Address : ${appointment[4]} , Service : ${appointment[5]}`;
            appointmentsList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error:', error));
}


*/