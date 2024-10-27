const daysContainer = document.getElementById("days-container");
    const monthName = document.getElementById("month-name");

    const today = new Date();
    let currentDate = new Date();
    currentDate.setDate(1);

    // Simulated booked dates for demonstration (replace this with actual data)

    const months = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ];

    async function renderCalendar() {
        try {
            const bookings = await getBookings();
            // Map visit_date from the fetched bookings to Date objects and store in bookedDates
            bookedDates = bookings.map(booking => new Date(booking.visit_date));
        } catch (error) {
            console.error("Error updating bookedDates:", error);
        }

        daysContainer.innerHTML = "";
        monthName.textContent = `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

        const firstDayIndex = currentDate.getDay();
        const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();

        // Fill previous month dates (empty cells)
        for (let i = 0; i < firstDayIndex; i++) {
            const emptyDiv = document.createElement("div");
            daysContainer.appendChild(emptyDiv);
        }

        // Fill current month dates
        for (let i = 1; i <= lastDay; i++) {
            const dayButton = document.createElement("button");
            dayButton.textContent = i;

            const buttonDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), i);

            // Apply past styling for past dates but keep them clickable
            if (buttonDate < today && buttonDate.toDateString() !== today.toDateString()) {
                dayButton.classList.add("past"); // Apply the past class to visually disable it
            }

            // Check if the date is booked
            if (bookedDates.some(bookedDate => bookedDate.toDateString() === buttonDate.toDateString())) {
                dayButton.classList.add('booked'); // Add booked class to style the button
            }

            // Add click listener for both past and future dates
            dayButton.addEventListener("click", () => showBookings(buttonDate.toDateString()));

            daysContainer.appendChild(dayButton);
        }
    }

    function changeMonth(direction) {
       // Update the current date by the direction (1 for next month, -1 for previous month)
       currentDate.setMonth(currentDate.getMonth() + direction);
    
        // No restrictions on navigating to past months
        renderCalendar(); // Re-render the calendar
    }

    document.getElementById("prev-month").addEventListener("click", () => changeMonth(-1));
    document.getElementById("next-month").addEventListener("click", () => changeMonth(1));

    // Initial render
    renderCalendar();


     // Function to convert the date format
    function formatDate(dateStr) {
        const dateParts = dateStr.split(' ');
        const month = dateParts[1]; // "Oct"
        const day = dateParts[2];    // "26"
        const year = dateParts[3];    // "2024"

        // Create a mapping of month names to numbers
        const monthMap = {
            Jan: '01', Feb: '02', Mar: '03', Apr: '04',
            May: '05', Jun: '06', Jul: '07', Aug: '08',
            Sep: '09', Oct: '10', Nov: '11', Dec: '12'
        };

        // Convert the month name to a number using the mapping
        const monthNumber = monthMap[month];

        // Return the formatted date as "YYYY-MM-DD"
        return `${year}-${monthNumber}-${day.padStart(2, '0')}`;
    }


    function showBookings(date) {
        const element = document.getElementById("bookings");
        const bookButton = document.getElementById("book_button");

        // Convert the selected date to a Date object and compare it to today
        const selectedDate = new Date(date);
        const today = new Date(); // Ensure 'today' is defined here

        // Set the time of today to midnight to compare only the date part
        today.setHours(0, 0, 0, 0);

        // Show or hide the "Book a new appointment" button based on the date
        if (selectedDate < today) {
            bookButton.style.display = "none"; // Hide button
        } else {
            bookButton.style.display = "block"; // Show button
        }

        // Display the bookings
        element.style.display = "flex";
        refreshBookings(date);
}

    function showBookingsCancelButton(){
    
        const dateHeader = document.getElementById("date_header").innerHTML;
        
        refreshBookings("   " + dateHeader);
        document.getElementById('book_button').style.display = 'block';

    }

    async function getBookings() {
        return fetch("{% url 'bookshowroom:show_json' %}")
            .then((res) => res.json());
    }

    async function getBookingById(booking_id){
        // Encode the showroom name to be URL-safe
        const encodedShowroomId = encodeURIComponent(booking_id);

        // Generate base URL and remove the trailing slash if there is one
        const baseUrl = "{% url 'bookshowroom:get_booking_by_id' booking_id_str='dummy_id' %}".replace('dummy_id', '');

        // Remove any potential trailing slash in baseUrl to avoid double slashes
        const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;

        // Construct the full URL by appending the encoded showroom name
        const url = `${cleanBaseUrl}${encodedShowroomId}/`;

        return fetch(url)
            .then((res) => res.json());
        
    }

    async function getBookingsFiltered() {
        var dateHeader = document.getElementById("date_header").innerHTML;

        // Replace spaces with dashes for a URL-friendly format
        dateHeader = dateHeader.trim()

         // Encode the showroom name to be URL-safe
        const encodedBookingDate = encodeURIComponent(dateHeader);

        // Generate base URL and remove the trailing slash if there is one
        const baseUrl = "{% url 'bookshowroom:get_bookings' visit_date='dummy_id' %}".replace('dummy_id', '');

        // Remove any potential trailing slash in baseUrl to avoid double slashes
        const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;

        // Construct the full URL by appending the encoded showroom name
        const url = `${cleanBaseUrl}${encodedBookingDate}/`;

        return fetch(url)
            .then((res) => res.json());
    }


    async function refreshBookings(date) {
// Clear existing booking cards
document.getElementById("booking_cards").innerHTML = "";
document.getElementById("booking_cards").className = "";

// Slicing the date to get a specific format, if needed
const slicedDate = date.slice(3);
document.getElementById("date_header").innerHTML = slicedDate; // Update the date header

// Fetch bookings (assuming this is a function that returns a promise)
const bookings = await getBookingsFiltered();

// // Initialize the HTML string
// let htmlString = `<div>${slicedDate}</div>`; // Include slicedDate in header

let htmlString = ''
// Check if there are any bookings
if (bookings.length === 0) {
    htmlString += `<div>No bookings have been made for this date.</div>`; // Display message if no bookings
    document.getElementById("booking_cards").style.justifyContent = 'center';
} else {
    // Iterate through each booking to build the HTML string 
    document.getElementById("booking_cards").style.justifyContent = 'top';
    bookings.forEach((booking) => {
        
        const brand = booking.car.brand
        const name = booking.car.car_type; // Access the car name from the booking object
        const visitDate = booking.visit_date; // Get visit date
        const visitTime = booking.visit_time; // Get visit time
        const status = booking.status; // Get booking status
        const notes = booking.notes; // Get notes
        const showroom = booking.showroom; // Get showroom name
        const myStaticUrl = "{% static 'images/' %}" + brand + ".png";

        // Build the HTML string for the booking card
        htmlString += `<div id="${booking.id}" class="booking-card">
            <div class="booking-header">
                <h3>${showroom.name}</h3>
                <div class="booking-status status-${status}">
                    ${status.charAt(0).toUpperCase() + status.slice(1)}
                </div>
            </div>
            <img src="{% static 'images/Gmaps.png' %}" alt="Google Maps" class="location-img" style="display:none;">
            <div class="booking-detail" style="display:none;">
                    <strong>Location:</strong>
                    <span>${booking.showroom.location}, ${booking.showroom.regency}</span>
                </div>
            <div class="booking-details">
                <img src="${myStaticUrl}" alt="${brand} logo" class="car-img">
                <div class="booking-detail">
                    <strong>Car:</strong>
                    <span>${booking.car.brand}, ${booking.car.car_type}, ${booking.car.model}</span>
                </div>
                <div class="booking-detail">
                    <strong>Visit Date:</strong>
                    <span>${visitDate}</span>
                </div>
                <div class="booking-detail">
                    <strong>Visit Time:</strong>
                    <span>${visitTime}</span>
                </div>
             
           `;
            if (notes) {
                htmlString += `<div class="booking-detail">
                    <strong>Notes:</strong>
                    
                </div>
                </div>
                
                <div class="booking-notes">
                    <p>${notes}</p>
                </div>`;
            } else {
                htmlString += '</div>'
            }
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const visit = new Date(booking.visit_date);
        if (visit >= today) {
            htmlString += `<div class="booking-actions">
                <button class="edit-button" onclick="editBooking('${booking.id}')">Edit</button>
                <button class="delete-button" onclick="deleteBooking('${booking.id}')">Delete</button>
                <button class="location-button" onclick="showLocation('${booking.id}')">Location</button>
            </div>
            <div class="back-card-button-div" style="display:none;">
            <button class="back-card-button" onclick="showCard('${booking.id}')">Back</button></div></div>`;
        } else {
            htmlString += `<div class="booking-actions"><button class="location-button" onclick="showLocation('${booking.id}')">Location</button>
            </div>
            <div class="back-card-button-div" style="display:none;">
            <button class="back-card-button" onclick="showCard('${booking.id}')">Back</button></div></div>`; // Close the booking card div
        }

    });
}

    // Update the DOM with the constructed HTML
    document.getElementById("booking_cards").innerHTML = htmlString; // Set the HTML content of the booking cards
    
}

function showCard(booking_id){
    const parentElement = document.getElementById(booking_id);
    const bookingDetails = parentElement.querySelector('.booking-details');
    const bookingActions = parentElement.querySelector('.booking-actions');
    const locationImage = parentElement.querySelector('.location-img');
    const bookingNotes = parentElement.querySelector('.booking-notes');
    const backButton = parentElement.querySelector('.back-card-button-div');
    const bookingLocation = parentElement.querySelector('.booking-detail');

    if (bookingNotes) {
    // Element exists, perform your actions here
    bookingNotes.style.display = 'block';
    // You can add additional logic or manipulate the element
    }   
    backButton.style.display = 'none';
    bookingDetails.style.display = 'block';
    bookingActions.style.display = 'block';
    locationImage.style.display = 'none';
    bookingLocation.style.display = 'none';
}
function showLocation(booking_id){
    const parentElement = document.getElementById(booking_id);
    const bookingDetails = parentElement.querySelector('.booking-details');
    const bookingActions = parentElement.querySelector('.booking-actions');
    const locationImage = parentElement.querySelector('.location-img');
    const bookingNotes = parentElement.querySelector('.booking-notes');
    const backButton = parentElement.querySelector('.back-card-button-div');
    const bookingLocation = parentElement.querySelector('.booking-detail');

    if (bookingNotes) {
    // Element exists, perform your actions here
    bookingNotes.style.display = 'none';
    // You can add additional logic or manipulate the element
    }   
    backButton.style.display = 'block';
    bookingDetails.style.display = 'none';
    bookingActions.style.display = 'none';
    locationImage.style.display = 'block';
    bookingLocation.style.display = 'block';

}

function addBooking() {
    const dateHeader = document.getElementById("date_header").innerHTML;
    const formattedDate = formatDate(dateHeader);
    let htmlString = `
        <form id="bookingForm" onsubmit="return addBookingEntry()">
        {% csrf_token %}
        <!-- Showroom selection -->
        <label for="showroom">Showroom:</label><br>
        <select id="showroom" name="showroom" required onchange="fetchLocations()">
            <option value="">Select a showroom</option> <!-- Default option -->
        </select>
        <br>

        <div id="location-container" style="display: block;">
            <label for="location">Location:</label>
            <div>
            <select id="location" name="showroom_id" required onchange="fetchCars()">
            <option value="">Select a location</option> <!-- Default option -->
            </select>
            </div>
            <br>
        </div>

        <div id="car-container" style="display: block;">
            <label for="car">Car:</label>
            <div>
            <select id="car" name="car_id" required>
            <option value="">Select a car</option> <!-- Default option -->
            </select>
            </div>
            <br>
        </div>

        <!-- Visit date -->
        <label for="visit_date">Visit Date:</label>
        <input type="date" id="visit_date" name="visit_date" required readonly>
        <br>

        <!-- Visit time -->
        <label for="visit_time">Visit Time:</label>
        <input type="time" id="visit_time" name="visit_time" value="12:00" required>
        <br>

        <!-- Notes -->
        <label for="notes">Notes:</label>
        <textarea id="notes" name="notes" rows="4" cols="50" placeholder="Additional information (optional)"></textarea>
        <br>

        <!-- Submit button -->
        <button type="submit">Submit Booking</button>

        <button type="button" onclick="showBookingsCancelButton()">Cancel</button>
        </form>

        `;


// Set the inner HTML of the booking cards
document.getElementById("booking_cards").innerHTML = htmlString;
document.getElementById('visit_date').value = formattedDate;
document.getElementById('book_button').style.display = 'none';

// Fetch showrooms after the form is added to the DOM
fetch("{% url 'bookshowroom:get_showrooms' %}")
  .then(response => response.json())
  .then(data => {
    const showroomSelect = document.getElementById('showroom');
    showroomSelect.innerHTML = ''; // Clear existing options
    showroomSelect.innerHTML += '<option value="">Select a showroom</option>'; // Default option
    data.forEach(showroom => {
      showroomSelect.innerHTML += `<option value="${showroom.showroom_name}">${showroom.showroom_name}</option>`;
    });
  })
  .catch(error => console.error('Error fetching showrooms:', error));


}

function fetchLocations() {
const showroomSelect = document.getElementById('showroom');
const selectedShowroomName = showroomSelect.value;
const locationContainer = document.getElementById('location-container');
const locationSelect = document.getElementById('location');

// Reset locations
locationSelect.innerHTML = '<option value="">Select a location</option>';

if (!selectedShowroomName) {  // Use the correct variable here
     // Hide the location dropdown if no showroom is selected
    return; // No showroom selected
} else {
  
    

   // Encode the showroom name to be URL-safe
   const encodedShowroomName = encodeURIComponent(selectedShowroomName);

    // Generate base URL and remove the trailing slash if there is one
    const baseUrl = "{% url 'bookshowroom:get_locations' showroom_name='dummy_id' %}".replace('dummy_id', '');

    // Remove any potential trailing slash in baseUrl to avoid double slashes
    const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;

    // Construct the full URL by appending the encoded showroom name
    const url = `${cleanBaseUrl}${encodedShowroomName}/`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                locationSelect.innerHTML += '<option value="">No locations available</option>';
                return;
            }

            // Create options
            const options = data.map(location => 
                `<option value="${location.id}">${location.showroom_location}, ${location.showroom_regency}</option>`
            ).join('');

            locationSelect.innerHTML += options; // Set options all at once
        })
        .catch(error => console.error('Error fetching locations:', error));
}
}

function fetchCars() {
const locationSelect = document.getElementById('location');
const selectedShowroomId = locationSelect.value;
const carContainer = document.getElementById('car-container');
const carSelect = document.getElementById('car');

// Reset locations
carSelect.innerHTML = '<option value="">Select a car</option>';

if (!selectedShowroomId) {  // Use the correct variable here
     // Hide the location dropdown if no showroom is selected
    return; // No showroom selected
} else {
  
    

   // Encode the showroom name to be URL-safe
   const encodedShowroomId = encodeURIComponent(selectedShowroomId);

    // Generate base URL and remove the trailing slash if there is one
    const baseUrl = "{% url 'bookshowroom:get_cars' showroom_id_str='dummy_id' %}".replace('dummy_id', '');

    // Remove any potential trailing slash in baseUrl to avoid double slashes
    const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;

    // Construct the full URL by appending the encoded showroom name
    const url = `${cleanBaseUrl}${encodedShowroomId}/`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.length === 0) {
               
                return;
            }

            // Create options
            const options = data.map(car => 
                `<option value="${car.id}">${car.brand}, ${car.car_type}, ${car.model}</option>`
            ).join('');

            carSelect.innerHTML += options; // Set options all at once
        })
        .catch(error => console.error('Error fetching cars:', error));
}
}

function addBookingEntry() {
fetch("{% url 'bookshowroom:create_booking_ajax' %}", {
    method: "POST",
    body: new FormData(document.querySelector('#bookingForm')),
  })
  .then(response => {
    if (response.ok) {
      document.getElementById('book_button').style.display = 'block';
      showBookingsCancelButton(); // Assuming refreshBookings updates the bookings list

      renderCalendar()
    } else {
      throw new Error('Error creating booking');
    }
  })
  .catch(error => {

  });

// Prevent default form submission
return false;
}

async function deleteBooking(booking_id) {
// Encode the showroom name to be URL-safe
const encodedShowroomId = encodeURIComponent(booking_id);

// Generate base URL and remove the trailing slash if there is one
const baseUrl = "{% url 'bookshowroom:delete_booking' booking_id_str='dummy_id' %}".replace('dummy_id', '');

// Remove any potential trailing slash in baseUrl to avoid double slashes
const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;

// Construct the full URL by appending the encoded showroom name
const url = `${cleanBaseUrl}${encodedShowroomId}/`;

try {
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
            'Content-Type': 'application/json',
        },
    });

    const data = await response.json();  // Parse JSON response

    if (response.ok) {
        const dateHeader = document.getElementById("date_header").innerHTML;
        
        refreshBookings("   " + dateHeader);
        renderCalendar()
    } else {
        // Handle errors
        alert('Error: ' + data.message);
    }
} catch (error) {
    // Handle network errors
    console.error('Network error:', error);
    alert('An error occurred while trying to delete the booking.');
}
}

async function editBooking(booking_id){

const booking = await getBookingById(booking_id)
const dateHeader = document.getElementById("date_header").innerHTML;
const formattedDate = formatDate(dateHeader);

let htmlString = `
    <form id="editForm" onsubmit="return editBookingEntry()">
    {% csrf_token %}
    <!-- Showroom selection -->
    <label for="showroom">Showroom:</label>
    <select id="showroom" name="showroom" required onchange="fetchLocations()">
        <option value="">Select a showroom</option> <!-- Default option -->
    </select>
    <br>

    <input type="hidden" id="booking_id" name="booking_id" value="${booking.id}">

    <div id="location-container" style="display: block;">
        <label for="location">Location:</label>
        <div>
        <select id="location" name="showroom_id" required onchange="fetchCars()">
        <option value="${booking.showroom.id}">${booking.showroom.location}, ${booking.showroom.regency}</option>
        </select>
        </div>
        <br>
    </div>

    <div id="car-container" style="display: block;">
        <label for="car">Car:</label>
        <div>
        <select id="car" name="car_id" required>
        <option value="${booking.car.id}">${booking.car.brand}, ${booking.car.car_type}, ${booking.car.model}</option>
        </select>
        </div>
        <br>
    </div>


    <!-- Visit date -->
    <label for="visit_date">Visit Date:</label>
    <input type="date" id="visit_date" name="visit_date" required readonly>
    <br>

    <!-- Visit time -->
    <label for="visit_time">Visit Time:</label>
    <input type="time" id="visit_time" name="visit_time" value="${booking.visit_time}" required>
    <br>

    <!-- Notes -->
    <label for="notes">Notes:</label>
    <textarea id="notes" name="notes" rows="4" cols="50" placeholder="Additional information (optional)">${booking.notes}</textarea>
    <br>

    <!-- Submit button -->
    <button type="submit">Edit Booking</button>

    <button type="button" onclick="showBookingsCancelButton()">Cancel</button>
    </form>

    `;


// Set the inner HTML of the booking cards
document.getElementById("booking_cards").innerHTML = htmlString;
document.getElementById('visit_date').value = formattedDate;
document.getElementById('book_button').style.display = 'none';

// Fetch showrooms after the form is added to the DOM
fetch("{% url 'bookshowroom:get_showrooms' %}")
  .then(response => response.json())
  .then(data => {
    const showroomSelect = document.getElementById('showroom');
    showroomSelect.innerHTML = ''; // Clear existing options
    showroomSelect.innerHTML += `<option value="${booking.showroom.name}">${booking.showroom.name}</option>`; // Default option
    data.forEach(showroom => {
    if (showroom.showroom_name !== booking.showroom.name) {
        showroomSelect.innerHTML += `<option value="${showroom.showroom_name}">${showroom.showroom_name}</option>`;
    }
      
    });
  })
  .catch(error => console.error('Error fetching showrooms:', error));


}

function editBookingEntry() {
fetch("{% url 'bookshowroom:edit_booking' %}", {
    method: "POST",
    body: new FormData(document.querySelector('#editForm')),
  })
  .then(response => {
    if (response.ok) {
      document.getElementById('book_button').style.display = 'block';
      showBookingsCancelButton(); // Assuming refreshBookings updates the bookings list
    } else {
      throw new Error('Error creating booking');
    }
  })
  .catch(error => {

  });

// Prevent default form submission
return false;
}

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Check if this cookie string begins with the name we want
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}