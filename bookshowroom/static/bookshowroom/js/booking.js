const daysContainer = document.getElementById("days-container");
    const monthName = document.getElementById("month-name");

    const today = new Date();
    let currentDate = new Date();
    currentDate.setDate(1);

    const months = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ];

    async function renderCalendar() {
        try {
            const bookings = await getBookings();
            bookedDates = bookings.map(booking => new Date(booking.visit_date));
        } catch (error) {
            console.error("Error updating bookedDates:", error);
        }

        daysContainer.innerHTML = "";
        monthName.textContent = `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

        const firstDayIndex = currentDate.getDay();
        const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();

        for (let i = 0; i < firstDayIndex; i++) {
            const emptyDiv = document.createElement("div");
            daysContainer.appendChild(emptyDiv);
        }

        for (let i = 1; i <= lastDay; i++) {
            const dayButton = document.createElement("button");
            dayButton.textContent = i;

            const buttonDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), i);

            if (buttonDate < today && buttonDate.toDateString() !== today.toDateString()) {
                dayButton.classList.add("past"); 
            }

            if (bookedDates.some(bookedDate => bookedDate.toDateString() === buttonDate.toDateString())) {
                dayButton.classList.add('booked'); 
            }

          
            dayButton.addEventListener("click", () => showBookings(buttonDate.toDateString()));

            daysContainer.appendChild(dayButton);
        }
    }

    function changeMonth(direction) {
       currentDate.setMonth(currentDate.getMonth() + direction);
    
        renderCalendar(); 
    }

    document.getElementById("prev-month").addEventListener("click", () => changeMonth(-1));
    document.getElementById("next-month").addEventListener("click", () => changeMonth(1));

    renderCalendar();

    function formatDate(dateStr) {
        const dateParts = dateStr.split(' ');
        const month = dateParts[1]; 
        const day = dateParts[2];    
        const year = dateParts[3];    

        const monthMap = {
            Jan: '01', Feb: '02', Mar: '03', Apr: '04',
            May: '05', Jun: '06', Jul: '07', Aug: '08',
            Sep: '09', Oct: '10', Nov: '11', Dec: '12'
        };

        const monthNumber = monthMap[month];

        return `${year}-${monthNumber}-${day.padStart(2, '0')}`;
    }


    function showBookings(date) {
        const element = document.getElementById("bookings");
        const bookButton = document.getElementById("book_button");

        const selectedDate = new Date(date);
        const today = new Date(); 

        today.setHours(0, 0, 0, 0);

        
        if (selectedDate < today) {
            bookButton.style.display = "none"; 
        } else {
            bookButton.style.display = "block"; 
        }

        element.style.display = "flex";
        refreshBookings(date);
}

    function showBookingsCancelButton(){
    
        const dateHeader = document.getElementById("date_header").innerHTML;
        
        refreshBookings("   " + dateHeader);
        document.getElementById('book_button').style.display = 'block';

    }

    async function getBookings() {
        return fetch("json/")
            .then((res) => res.json());
    }

    async function getBookingById(booking_id){
        const encodedShowroomId = encodeURIComponent(booking_id);

        const url = `get_booking_by_id/${encodedShowroomId}/`;

        return fetch(url)
            .then((res) => res.json());
        
    }

    async function getBookingsFiltered() {
        var dateHeader = document.getElementById("date_header").innerHTML;

        dateHeader = dateHeader.trim()

        const encodedBookingDate = encodeURIComponent(dateHeader);

        const url = `get_bookings/${encodedBookingDate}/`;

        return fetch(url)
            .then((res) => res.json());
    }


    async function refreshBookings(date) {
        document.getElementById("booking_cards").innerHTML = "";
        document.getElementById("booking_cards").className = "";

        const slicedDate = date.slice(3);
        document.getElementById("date_header").innerHTML = slicedDate;

        const bookings = await getBookingsFiltered();

        let htmlString = ''
       
        if (bookings.length === 0) {
            htmlString += `<div>No bookings have been made for this date.</div>`; 
            document.getElementById("booking_cards").style.justifyContent = 'center';
        } else {
      
            document.getElementById("booking_cards").style.justifyContent = 'top';
            bookings.forEach((booking) => {
                
                const brand = booking.car.brand
                const name = booking.car.car_type; 
                const visitDate = booking.visit_date; 
                const visitTime = booking.visit_time;
                const status = booking.status; 
                const notes = booking.notes; 
                const showroom = booking.showroom; 
                const carImgUrl = `${STATIC_URL}images/${brand}.png`;
                const locationImgUrl = `${STATIC_URL}images/Gmaps.png`;
               
                htmlString += `<div id="${booking.id}" class="booking-card">
                    <div class="booking-header">
                        <h3>${showroom.name}</h3>
                        <div class="booking-status status-${status}">
                            ${status.charAt(0).toUpperCase() + status.slice(1)}
                        </div>
                    </div>
                    <img src="${locationImgUrl}" alt="Google Maps" class="location-img" style="display:none;">
                    <div class="booking-detail" style="display:none;">
                            <strong>Location:</strong>
                            <span>${booking.showroom.location}, ${booking.showroom.regency}</span>
                        </div>
                    <div class="booking-details">
                        <img src="${carImgUrl}" alt="${brand} logo" class="car-img">
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
                        <button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50" onclick="editBooking('${booking.id}')">Edit</button>
                        <button class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"" onclick="deleteBooking('${booking.id}')">Delete</button>
                        <button  class="bg-[#674ea7] hover:bg-[#5b3c94] text-white font-semibold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-[#674ea7] focus:ring-opacity-50" onclick="showLocation('${booking.id}')">Location</button>
                    </div>
                    <div class="back-card-button-div" style="display:none;">
                    <button class="back-card-button" onclick="showCard('${booking.id}')">Back</button></div></div>`;
                } else {
                    htmlString += `<div class="booking-actions"><button class="location-button" onclick="showLocation('${booking.id}')">Location</button>
                    </div>
                    <div class="back-card-button-div" style="display:none;">
                    <button class="back-card-button" onclick="showCard('${booking.id}')">Back</button></div></div>`; 
                }

            });
        }

          
            document.getElementById("booking_cards").innerHTML = htmlString; 
            
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
    bookingNotes.style.display = 'block';
  
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
    bookingNotes.style.display = 'none';
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
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
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


    document.getElementById("booking_cards").innerHTML = htmlString;
    document.getElementById('visit_date').value = formattedDate;
    document.getElementById('book_button').style.display = 'none';

    fetch("get-showrooms/")
    .then(response => response.json())
    .then(data => {
        const showroomSelect = document.getElementById('showroom');
        showroomSelect.innerHTML = ''; 
        showroomSelect.innerHTML += '<option value="">Select a showroom</option>'; 
        data.forEach(showroom => {
        showroomSelect.innerHTML += `<option value="${showroom.showroom_name}">${showroom.showroom_name}</option>`;
        });
    })
    .catch(error => console.error('Error fetching showrooms:', error));


    }

    function fetchLocations(edit=false) {
    const showroomSelect = document.getElementById('showroom');
    const selectedShowroomName = showroomSelect.value;
    const locationContainer = document.getElementById('location-container');
    const locationSelect = document.getElementById('location');


    if (!edit) {
        locationSelect.innerHTML = '<option value="">Select a location</option>';
    }
    const existingOptions = Array.from(locationSelect.options).map(option => option.value);

    if (!selectedShowroomName) {  
       
        return; 
    } else {
  
    
   const encodedShowroomName = encodeURIComponent(selectedShowroomName);

    const url = `get_locations/${encodedShowroomName}/`;

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

            const options = data.map(location => {
                
                if (!existingOptions.includes(location.id)) {
                    return `<option value="${location.id}">${location.showroom_location}, ${location.showroom_regency}</option>`;
                }
                return ''; 
            }).join('');

            locationSelect.innerHTML += options; 
        })
        .catch(error => console.error('Error fetching locations:', error));
}
}

function fetchCars(edit=false) {
const locationSelect = document.getElementById('location');
const selectedShowroomId = locationSelect.value;
const carContainer = document.getElementById('car-container');
const carSelect = document.getElementById('car');
const existingOptions = Array.from(carSelect.options).map(option => option.value);

if (!edit){
    
    carSelect.innerHTML = '<option value="">Select a car</option>';
};

if (!selectedShowroomId) {  
    return; 
} else {
  
    const encodedShowroomId = encodeURIComponent(selectedShowroomId);

    const url = `get_cars/${encodedShowroomId}/`;

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
            
            const options = data.map(car => {
              
                if (!existingOptions.includes(car.id)) {
                    return  `<option value="${car.id}">${car.brand}, ${car.car_type}, ${car.model}</option>`;
                }
                return ''; 
            }).join('');

            carSelect.innerHTML += options; 
        })
        .catch(error => console.error('Error fetching cars:', error));
}
}

function addBookingEntry() {
    fetch("create_booking_ajax/", {
        method: "POST",
        body: new FormData(document.querySelector('#bookingForm')),
    })
    .then(response => {
        if (response.ok) {
        document.getElementById('book_button').style.display = 'block';
        showBookingsCancelButton(); 

        renderCalendar()
        } else {
        throw new Error('Error creating booking');
        }
    })
    .catch(error => {

    });


    return false;
}

async function deleteBooking(booking_id) {

    const encodedShowroomId = encodeURIComponent(booking_id);


    const url = `delete_booking/${encodedShowroomId}/`;

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), 
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();  

        if (response.ok) {
            const dateHeader = document.getElementById("date_header").innerHTML;
            
            refreshBookings("   " + dateHeader);
            renderCalendar()
        } else {
        
            alert('Error: ' + data.message);
        }
    } catch (error) {
        
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
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        
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


    document.getElementById("booking_cards").innerHTML = htmlString;
    document.getElementById('visit_date').value = formattedDate;
    document.getElementById('book_button').style.display = 'none';


    fetch("get-showrooms/")
    .then(response => response.json())
    .then(data => {
        const showroomSelect = document.getElementById('showroom');
        showroomSelect.innerHTML = ''; 
        showroomSelect.innerHTML += `<option value="${booking.showroom.name}">${booking.showroom.name}</option>`; 
        data.forEach(showroom => {
        if (showroom.showroom_name !== booking.showroom.name) {
            showroomSelect.innerHTML += `<option value="${showroom.showroom_name}">${showroom.showroom_name}</option>`;
        }
    
        });
        fetchLocations(edit=true);
        fetchCars(edit=true)
    })
    .catch(error => console.error('Error fetching showrooms:', error));

}

function editBookingEntry() {
    fetch("edit_booking/", {
        method: "POST",
        body: new FormData(document.querySelector('#editForm')),
    })
    .then(response => {
        if (response.ok) {
        document.getElementById('book_button').style.display = 'block';
        showBookingsCancelButton(); 
        } else {
        throw new Error('Error creating booking');
        }
    })
    .catch(error => {

    });

    return false;
}

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}