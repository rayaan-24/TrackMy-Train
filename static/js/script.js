// Wait for the page to load before running scripts
document.addEventListener("DOMContentLoaded", function () {
    console.log("TrackMyTrain JavaScript Loaded!");

    // Smooth scrolling for navigation links
    document.querySelectorAll('.navbar a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (this.hash !== "") {
                e.preventDefault();
                let target = document.querySelector(this.hash);
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }
        });
    });

    // Booking Form Submission
    const bookingForm = document.getElementById("bookingForm");
    if (bookingForm) {
        bookingForm.addEventListener("submit", function (event) {
            event.preventDefault();
            alert("Your booking has been submitted successfully!");
            bookingForm.reset();
        });
    }

    // Feedback Form Submission
    const feedbackForm = document.getElementById("feedbackForm");
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function (event) {
            event.preventDefault();
            alert("Thank you for your feedback!");
            feedbackForm.reset();
        });
    }

    // Real-time train tracking (Mock Data)
    const trainStatusButton = document.getElementById("checkTrainStatus");
    if (trainStatusButton) {
        trainStatusButton.addEventListener("click", function () {
            let trainNumber = document.getElementById("trainNumber").value;
            if (trainNumber === "") {
                alert("Please enter a train number!");
                return;
            }
            let mockLat = (Math.random() * (12.90 - 12.80) + 12.80).toFixed(5);
            let mockLon = (Math.random() * (80.30 - 80.20) + 80.20).toFixed(5);
            let speed = (Math.random() * (120 - 60) + 60).toFixed(2);

            document.getElementById("trainLocation").innerHTML = `
                <strong>Train ${trainNumber} Location:</strong> <br>
                Latitude: ${mockLat}, Longitude: ${mockLon} <br>
                Speed: ${speed} km/h
            `;
        });
    }

    // Notification Popups
    function showNotification(message) {
        let notificationBox = document.createElement("div");
        notificationBox.classList.add("notification-popup");
        notificationBox.innerText = message;
        document.body.appendChild(notificationBox);

        setTimeout(() => {
            notificationBox.style.opacity = "0";
            setTimeout(() => {
                notificationBox.remove();
            }, 500);
        }, 3000);
    }
    document.getElementById("trainStatusForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const trainNumber = document.getElementById("trainNumber").value.trim();
    
        fetch(`/api/train_status/${trainNumber}`)
            .then(response => {
                if (!response.ok) throw new Error("Train not found");
                return response.json();
            })
            .then(data => {
                document.getElementById("trainInfo").classList.remove("hidden");
                document.getElementById("trainName").innerText = data.train_name;
                document.getElementById("currentLocation").innerText = data.location;
                document.getElementById("arrivalTime").innerText = data.arrival_time;
                document.getElementById("departureTime").innerText = data.departure_time;
                document.getElementById("status").innerText = data.status;
    
                const map = new google.maps.Map(document.getElementById("map"), {
                    center: { lat: parseFloat(data.latitude), lng: parseFloat(data.longitude) },
                    zoom: 12
                });
    
                new google.maps.Marker({
                    position: { lat: parseFloat(data.latitude), lng: parseFloat(data.longitude) },
                    map: map
                });
            })
            .catch(error => {
                alert("❌ " + error.message);
            });
    });
    

    // Show a notification on page load (Mock notification)
    setTimeout(() => {
        showNotification("🚆 Welcome to TrackMyTrain! Check your train status now.");
    }, 2000);
});
