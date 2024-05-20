const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

hamBurger.addEventListener("click", function () {
  document.querySelector(".notification_box").classList.toggle("expand");
});


document.getElementById("notification").addEventListener("click", function() {
          var notificationBox = document.getElementById("notification_box");
            if (notificationBox.style.display === "block") {
                notificationBox.style.display = "none";
            } else {
                notificationBox.style.display = "block";
            }
        });