$(document).ready(function () {
  console.log("loaded");
  $.material.init();
  console.log("loaded");
  $(document).on("submit", "#signup-form", function (e) {
    e.preventDefault();

    var form = $("#signup-form").serialize();

    $.ajax({
      url: "/api/signup",
      type: "POST",
      data: form,
      success: function (response) {
        if (response) {
          res = JSON.parse(response);
          if (res.error) {
            alert(res.msg);
          } else {
            window.location.href = "/";
          }
        }
      },
    });
  });

  $(document).on("submit", "#login-form", function (e) {
    e.preventDefault();

    var form = $(this).serialize();
    $.ajax({
      url: "/api/login",
      type: "POST",
      data: form,
      success: function (res) {
        if (res == "error") {
          alert("could not login");
        } else {
          console.log("Logged in as: ", res);
          window.location.href = "/";
        }
      },
    });
  });

  $(document).on("click", "#logout-link", function (e) {
    e.preventDefault();
    $.ajax({
      url: "/api/logout",
      type: "GET",
      success: function (res) {
        if (res == "success") {
          window.location.href = "/login";
        } else {
          alert("Something went wrong!");
        }
      },
    });
  });

  $(document).on("submit", "#post-activity", function (e) {
    e.preventDefault();
    form = $(this).serialize();
    $.ajax({
      url: "/api/post-activity",
      type: "POST",
      data: form,
      success: function (res) {
        console.log(res);
      },
    });
  });
});
