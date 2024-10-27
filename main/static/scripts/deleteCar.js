document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-car-btn').forEach(button => {
        button.addEventListener('click', function() {
            const carId = this.getAttribute('data-car-id');

            if (confirm('Are you sure you want to delete this car?')) {
                fetch(`/delete_car/${carId}/`, {
                    method: 'POST', // Change to POST for testing
                    headers: {
                        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Server response:", data); // Log server response

                    if (data.success) {
                        alert("Car deleted successfully");
                        this.closest('.car-card').remove();
                    } else {
                        alert(data.error || 'Error deleting the car.');
                    }
                })
                .catch(error => console.error('Fetch error:', error));
            }
        });
    });
});
