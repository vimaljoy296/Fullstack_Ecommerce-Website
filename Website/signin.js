const submitButton = document.getElementById("submitBtn");

submitButton.addEventListener("click", async function () {
    // Get values from inputs by their IDs
    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const password = document.getElementById("password").value.trim();
    const email = document.getElementById("email").value.trim();

    // Check if all fields are filled
    if (!firstName || !lastName || !password || !email) {
        alert("Please fill in all fields.");
        return;
    }

    // Create a data object to send to the server
    const data = {
        first_name: firstName,
        last_name: lastName,
        password: password,
        email: email
    };

    try {
        // Send data to the API with a POST request
        const response = await fetch("http://127.0.0.1:5000/sign_up", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        // Check if the response is OK
        if (!response.ok) {
            throw new Error("Error signing up. Please try again.");
        } 
        const result = await response.json();
        alert("Signup Successful! You can Go Back To The HOMEPAGE");

        // Redirect to home.html after successful signup
        window.location.href = "home.html";

    } catch (error) {
        // Handle errors and log the error message
        alert("Request failed: " + error.message);
        console.error("Error:", error);
    }
});
