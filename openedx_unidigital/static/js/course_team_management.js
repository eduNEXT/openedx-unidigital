function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function addInstructorToTable(data) {
  let instructorsTableBody = $("#instructors-table-body");
  let row = $("<tr>");
  let usernameCell = $("<td>");
  let revokeAccessCell = $("<td>");
  usernameCell.text(data.user);
  revokeAccessCell.html(
    `
    <a href="#">
      <span class="icon fa fa-times fa-lg revoke-access" data-course-instructor-team-id="${data.id} aria-hidden="true"></span>
    </a>
    `
  );
  row.append(usernameCell);
  row.append(revokeAccessCell);
  row.addClass("pgn__data-table-row");
  row.attr("role", "row");
  instructorsTableBody.append(row);
}

function fetchInstructorsForTeam(teamId) {
  let instructorsTable = $("#instructors-table");
  let instructorsTableBody = $("#instructors-table-body");
  instructorsTable.css("display", "block");
  instructorsTableBody.empty(); // Clear previous data

  // Call API to fetch instructors for the selected team
  fetch("api/v1/course-team-instructor/" + "?course_team_id=" + teamId)
    .then(function (response) {
      return response.json();
    })
    .then(function (instructors) {
      instructors.results.forEach(function (instructor) {
        addInstructorToTable(instructor);
      });
    })
    .catch(function (error) {
      console.error("Error fetching instructors:", error);
    });
}
$("#add-instructor").on("click", function (select) {
  $("#error-message").text("");
  const username = $("#add-instructor-input").val();
  const courseTeamId = $("#course-teamset").val();
  const courseTeamName = $("#course-teamset option:selected").text();
  fetch("api/v1/course-team-instructor/", {
    method: "POST",
    body: JSON.stringify({
      user: username,
      course_team_id: courseTeamId,
      course_team_name: courseTeamName,
    }),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then(function (response) {
      if (!response.ok) {
        $("#add-instructor-input").val("");
        $("#error-message").text("Error adding instructor. Please try again.");
        return Promise.reject("Error adding instructor");
      }
      return response.json();
    })
    .then(function (data) {
      addInstructorToTable(data);
      $("#add-instructor-input").val("");
    });
});

$("#course-teamset").on("change", function (select) {
  const teamId = $("#course-teamset").val();
  let instructorsTable = $("#instructors-table");
  if (teamId) {
    fetchInstructorsForTeam(teamId);
  } else {
    instructorsTable.css("display", "none");
  }
});

  function revokeAccess(courseInstructorTeamId) {
    fetch("api/v1/course-team-instructor/" + courseInstructorTeamId, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then(function () {
        const teamId = $("#course-teamset").val();
        fetchInstructorsForTeam(teamId);
      })
  }

  document.addEventListener("click", function(event) {
    if (event.target && event.target.classList.contains("revoke-access")) {
      const courseInstructorTeamId = event.target.getAttribute("data-course-instructor-team-id");
      revokeAccess(courseInstructorTeamId);
    }
  });

$(function () {
  const cssUrl = "https://cdn.jsdelivr.net/npm/@openedx/paragon@22.4.0/dist/paragon.min.css";

  $("<link>")
    .attr({
      href: cssUrl,
      rel: "stylesheet",
    })
    .appendTo("head");
});
