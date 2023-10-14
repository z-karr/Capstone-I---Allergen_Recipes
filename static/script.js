// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Get all save buttons with class "save-button"
    const saveButtons = document.querySelectorAll(".save-button");

    // Function to update button text based on the save status of the recipe
    function updateButtonText(button, recipeId) {
        // Send a GET request to the server to check if the recipe is saved
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

        axios.get(`/recipes/${recipeId}/save_status`, {
            headers: {
                'X-CSRFToken': csrfToken,
            }
        })
            .then(response => {
                const saved = response.data.saved;
                button.querySelector(".button-text").innerText = saved ? "Unsave" : "Save";
                if (saved) {
                    button.querySelector(".fa-star").classList.add("text-warning");
                } else {
                    button.querySelector(".fa-star").classList.remove("text-warning");
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    // Attach click event listener to each save button
    saveButtons.forEach(button => {
        const recipeId = button.getAttribute("data-recipe-id");

        // Update button text when the page loads
        updateButtonText(button, recipeId);

        // Add click event listener to toggle save/unsave on button click
        button.addEventListener("click", function(event) {
            event.preventDefault();

            // Send a POST request to the server to save/unsave the recipe
            const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

            axios.post(`/recipes/${recipeId}/save`, {}, {
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            })
                .then(response => {
                    // Update button text after saving/unsaving the recipe
                    updateButtonText(button, recipeId);
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        });
    });
});






// document.addEventListener("DOMContentLoaded", function () {
//     console.log('DOM Content Loaded'); // Check if this line is logged
//     const forms = document.querySelectorAll(".save-form");

//     forms.forEach(form => {
//         form.addEventListener("submit", function (event) {
//             console.log('Button Clicked'); // check if button click is logged
//             event.preventDefault(); // Prevent the form from submitting traditionally
//             const recipeId = this.querySelector(".save-button").getAttribute("data-recipe-id");
//             saveRecipe(recipeId, this.querySelector(".save-button"));
//         });
//     });


//     function saveRecipe(recipeId, buttonElement) {
//         axios.post(`/recipes/${recipeId}/save`, {}, {
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCSRFToken()
//             }
//         })
//         .then(response => {
//             console.log('Response:', response);
//             const buttonTextElement = buttonElement.querySelector(".button-text");
    
//             if (response.data.message === "Recipe removed successfully.") {
//                 buttonTextElement.textContent = "Save";
//             } else if (response.data.message === "Recipe saved successfully.") {
//                 buttonTextElement.textContent = "Unsave";
//             } else {
//                 console.error('Failed to save recipe.');
//             }
//         })
//         .catch(error => {
//             console.error('Error saving recipe:', error);
//         });
//     }
    
    

// function getCSRFToken() {
//     const tokenElement = document.querySelector('meta[name=csrf-token]');
//     if (tokenElement) {
//         return tokenElement.getAttribute('content');
//     }
//     return null;
// }

// });
