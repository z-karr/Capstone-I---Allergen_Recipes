// // Define a function to fetch data from the API
// function fetchSpoonacularData() {
//     $.ajax({
//       url: 'https://api.spoonacular.com/recipes/complexSearch', // API endpoint from Docs
//       method: 'GET',
//       data: {
//         apiKey: '5e3f80e8f6f64272a5a29fc9e6c99b74', // Spoonacular API key as a query parameter
//       },
//       success: function (data) {
//         // Handle the API response data here
//         console.log(data);
//         // Send the data to your Flask route
//         $.ajax({
//           url: '/fetch-spoonacular-data', // Replace with the actual route URL
//           method: 'GET',
//           data: { data: data },
//           success: function (response) {
//             console.log(response);
//             // Handle the response from your Flask route
//           },
//           error: function (error) {
//             console.error(error);
//           },
//         });
//       },
//     });
//   }
  
//   // Call the function to fetch data when needed, e.g., when a button is clicked
//   $('#fetch-data-button').click(function () {
//     fetchSpoonacularData();
//   });
  