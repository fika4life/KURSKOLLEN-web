// const registerForm = document.getElementById("registerForm");

// const email = document.getElementById("email");
// const password = document.getElementById("password");

// // show error message

// // show success outline

// // check all fields filled in

// //check email is correct format

// //check password is at least 8 characters

// registerForm.addEventListener("submit", function (e) {
//   e.preventDefault();
// });

// ------------------  range slider---------
//get the value of the range
const rangeSlider = document.getElementById("rating-slider");

const ratingInput = document.getElementById("rating-input");

//get the input text element and set the value to the rangeSlider value
rangeSlider.addEventListener("input", (e) => {
  ratingInput.value = e.target.value;
});

ratingInput.addEventListener("change", (e) => {
  rangeSlider.value = e.target.value;
});
