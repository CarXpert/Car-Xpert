document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById("add-car-modal");
    const addCarButton = document.getElementById("add-car-button");
    const closeModal = document.getElementById("close-modal");
    const addCarForm = document.getElementById("add-car-form");

    // Show modal when "Add Car" button is clicked
    addCarButton.onclick = function () {
        modal.style.display = "flex";  // Use "flex" or "block" to make modal visible
    };

    // Hide modal when "Close" button is clicked
    closeModal.onclick = function () {
        modal.style.display = "none";
    };

    // Hide modal when clicking outside the modal content
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };

    // AJAX form submission
    addCarForm.onsubmit = function (e) {
        e.preventDefault();
        
        // Get the URL from the data-url attribute
        const url = addCarButton.getAttribute("data-url");
        const formData = new FormData(addCarForm);

        fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Car added successfully!");
                modal.style.display = "none";
                window.location.reload();
            } else {
                alert("Failed to add car.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred.");
        });
    };
});
