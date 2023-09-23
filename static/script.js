// document.addEventListener("DOMContentLoaded", function () {
//     const searchForm = document.querySelector("#search-form");
//     const searchResults = document.querySelector("#search-results");

//     searchForm.addEventListener("submit", function (event) {
//         event.preventDefault();
//         const selectedAllergens = Array.from(document.querySelectorAll("input[name='allergens']:checked")).map(input => input.value);

//         axios.post('/search', { allergens: selectedAllergens })
//             .then(response => {
//                 const recipes = response.data.recipes;

//                 searchResults.innerHTML = ""; // Clear previous results

//                 recipes.forEach(recipe => {
//                     const recipeItem = document.createElement("li");
//                     recipeItem.innerHTML = `
//                         <img src="${recipe.image}" alt="${recipe.title}" width="200" height="200">
//                         <h2>${recipe.title}</h2>
//                         <a href="${recipe.sourceUrl}" target="_blank">View Recipe</a>
//                     `;
//                     searchResults.appendChild(recipeItem);
//                 });
//             })
//             .catch(error => {
//                 console.error("Error searching for recipes:", error);
//                 // Handle the error, e.g., display an error message to the user
//             });
//     });
// });



/////////////////////////////////////////////////////////////////////////////
// document.addEventListener("DOMContentLoaded", function () {
//     console.log("DOMContentLoaded event fired"); // Debugging statement

//     // Define a function to perform recipe search based on selected allergens
//     function searchRecipes(allergens) {
//         console.log("searchRecipes called"); // Debugging statement
//         // const searchResults = document.getElementById("search-results");
//         const searchResults = document.querySelector("#search-results");
//         console.log(document); // Log the entire document
//         console.log("searchResults:", searchResults); // Log the searchResults variable
//         console.log("searchResults:", searchResults); // Debugging statement

//         // Clear previous search results
//         searchResults.innerHTML = "";

//         // Make Axios POST request to send data as form data
//         axios.post('/search', new URLSearchParams({ 'allergens': selectedAllergens }) )
//             .then(response => {
//                 console.log("Response data:", response.data); // Debugging statement
//                 const recipes = response.data.recipes;

//                 // Loop through the retrieved recipes and add them to the results list
//                 recipes.forEach(recipe => {
//                     const recipeItem = document.createElement("li");
//                     recipeItem.innerHTML = `
//                         <img src="${recipe.image}" alt="${recipe.title}" width="200" height="150">
//                         <h3>${recipe.title}</h3>
//                         <p>${recipe.summary}</p>
//                     `;
//                     searchResults.appendChild(recipeItem);
//                 });
//             })
//             .catch(error => {
//                 console.error("Error searching for recipes:", error);
//             // Handle the error, e.g., display an error message to the user
//             });
//     }

//     // Add a submit event listener to the search form
//     const searchForm = document.getElementById("search-form");
//     console.log("searchForm:", searchForm);
//     searchForm.addEventListener("submit", function (event) {
//         event.preventDefault(); // Prevent the default form submission

//         // Get the selected allergens from the form
//         const selectedAllergens = Array.from(document.querySelectorAll("input[name='allergens']:checked")).map(input => input.value);

//         // Call the searchRecipes function with the selected allergens
//         searchRecipes(selectedAllergens);
//         });

// });


// ////////////////////////////////////////////////////////////////////////////////
// document.addEventListener('DOMContentLoaded', function() {
//     console.log('DOMContentLoaded event fired.'); // check to be sure DOM fired correctly

//     function renderRecipes(recipes, append = false) {
//         console.log('Rendering recipes:', recipes);
//         const searchResults = document.getElementById('search-results'); // Get the existing <ul> element
    
//         if (searchResults) {
//             if (Array.isArray(recipes) && recipes.length > 0) {
//                 // Clear the existing content if not appending
//                 if (!append) {
//                     searchResults.innerHTML = '';
//                 }
    
//                 recipes.forEach(function(recipe) {
//                     const listItem = document.createElement('li');
//                     const image = document.createElement('img');
//                     const heading = document.createElement('h2');
//                     const viewLink = document.createElement('a');
    
//                     image.src = recipe.image;
//                     image.alt = recipe.title;
//                     image.width = 200;
//                     image.height = 200;
    
//                     heading.textContent = recipe.title; // Set the recipe title
    
//                     viewLink.href = `/recipe/${recipe.id}`;
//                     viewLink.textContent = 'View Recipe';
    
//                     listItem.appendChild(image);
//                     listItem.appendChild(heading); // Append the recipe title
//                     listItem.appendChild(viewLink);
    
//                     searchResults.appendChild(listItem); // Append to the existing <ul>
//                 });
//             } else {
//                 // If no recipes are found, you can add a message or handle it as needed
//                 searchResults.innerHTML = '<p>No recipes found.</p>';
//             }
//         } else {
//             console.error('searchResults not found in the DOM.');
//         }
//     }

    // // Function to fetch and render recipes using JavaScript
    // function fetchAndRenderRecipes() {
    //     const searchForm = document.getElementById('search-form');
    //     const savedRecipes = document.getElementById('saved-recipes');
    //     const loadMoreButton = document.getElementById('load-more');

    //     if (searchForm) {
    //         searchForm.addEventListener('submit', function(event) {
    //             event.preventDefault();
    //             const allergens = Array.from(document.querySelectorAll('input[name="allergens"]:checked')).map(input => input.value);

    //             axios.post('/search', { allergens })
    //                 .then(function(response) {
    //                     console.log('API Response:', response.data); // print to console checking if response data to client is correct
    //                     const recipes = response.data.results;
    //                     console.log('Recipes:', recipes); // Check the recipes variable
    //                     renderRecipes(recipes);
    //                 })
    //                 .catch(function(error) {
    //                     console.error(error);
    //                 });
    //         });
    //     }

    //     if (loadMoreButton) {
    //         let page = 2; // Initialize page counter for "load more" button

    //         loadMoreButton.addEventListener('click', function(event) {
    //             event.preventDefault();

    //             // Get the selected allergens
    //             const allergens = Array.from(document.querySelectorAll('input[name="allergens"]:checked')).map(input => input.value);

    //             // Make an additional request for the next page of recipes
    //             axios.post(`/search?page=${page}`, { allergens })
    //                 .then(function(response) {
    //                     const recipes = response.data.results;
    //                     renderRecipes(recipes, true);
    //                     page++; // Increment page counter
    //                 })
    //                 .catch(function(error) {
    //                     console.error(error);
    //                 });
    //         });
    //     }
    // }

    //     function renderRecipes(recipes, append = false) {
    //         console.log('Rendering recipes:', recipes);
    //         const searchResults = document.getElementById('search-results'); // Get the existing <ul> element

    //         if (searchResults) {
    //             if (Array.isArray(recipes) && recipes.length > 0) {
    //                 // Clear the existing content if not appending
    //                 if (!append) {
    //                     searchResults.innerHTML = '';
    //                 }

    //                 recipes.forEach(function(recipe) {
    //                     const listItem = document.createElement('li');
    //                     const image = document.createElement('img');
    //                     const heading = document.createElement('h2');
    //                     const viewLink = document.createElement('a');

    //                     image.src = recipe.image;
    //                     image.alt = recipe.title;
    //                     image.width = 200;
    //                     image.height = 200;

    //                     heading.textContent = recipe.title; // Set the recipe title

    //                     viewLink.href = `/recipe/${recipe.id}`;
    //                     viewLink.textContent = 'View Recipe';

    //                     listItem.appendChild(image);
    //                     listItem.appendChild(heading); // Append the recipe title
    //                     listItem.appendChild(viewLink);

    //                     searchResults.appendChild(listItem); // Append to the existing <ul>
    //                 });
    //             } else {
    //                 // If no recipes are found, you can add a message or handle it as needed
    //                 searchResults.innerHTML = '<p>No recipes found.</p>';
    //             }
    //         } else {
    //             console.error('searchResults not found in the DOM.');
    //         }
    //     }
    // }

    // Call the function to fetch and render recipes when needed
    // fetchAndRenderRecipes();


    
    
    




    

    // if (savedRecipes) {
    //     savedRecipes.addEventListener('submit', function(event) {
    //         event.preventDefault();
    //         if (event.target.classList.contains('unsave-form')) {
    //             const recipeId = event.target.dataset.recipeId;

    //             axios.post(`/unsave/${recipeId}`)
    //                 .then(function(response) {
    //                     event.target.parentElement.remove();
    //                     showMessage(response.data.message, 'success');
    //                 })
    //                 .catch(function(error) {
    //                     console.error(error);
    //                 });
    //         }
    //     });
    // }

   

//     function showMessage(message, type) {
//         const flashMessages = document.querySelector('.flash-messages');
//         const messageElement = document.createElement('li');
//         messageElement.classList.add(type);
//         messageElement.textContent = message;
//         flashMessages.appendChild(messageElement);
//     }
// });
