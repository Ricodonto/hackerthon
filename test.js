// Get form in JS
var myForm = document.getElementById("myForm");
console.log(myForm);

// function onSubmit() {

// }

// Tell JS what to do when form submits
myForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    // console.log("Hello Wierdo!")
    const response = await fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc
        headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: "hello" // body data type must match "Content-Type" header
      });
});