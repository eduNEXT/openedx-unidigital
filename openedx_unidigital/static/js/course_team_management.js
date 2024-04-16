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
  var instructorsTableBody = $("#instructors-table-body");
  var row = $("<tr>");
  var usernameCell = $("<td>");
  var revokeAccessCell = $("<td>");
  usernameCell.text(data.username);
  revokeAccessCell.html(
    '<input type="button" value="Revoke Access" data-course-instructor-team-id="' + data.id + '" class="revoke-access-button">'
  );
  row.append(usernameCell);
  row.append(revokeAccessCell);
  row.addClass("pgn__data-table-row");
  row.attr("role", "row");
  instructorsTableBody.append(row);
}

function fetchInstructorsForTeam(teamId) {
  var instructorsTable = $("#instructors-table");
  var instructorsTableBody = $("#instructors-table-body");
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
$("#add-instructor-button").on("click", function (select) {
  const username = $("#add-instructor-input").val();
  const courseTeamId = $("#course-teamset").val();
  const courseTeamName = $("#course-teamset option:selected").text();
  fetch("api/v1/course-team-instructor/", {
    method: "POST",
    body: JSON.stringify({
      username: username,
      course_team_id: courseTeamId,
      course_team_name: courseTeamName,
    }),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data);
      addInstructorToTable(data);
      $("#add-instructor-input").val("");
    });
});

$("#course-teamset").on("change", function (select) {
  const teamId = $("#course-teamset").val();
  var instructorsTable = $("#instructors-table");
  var instructorsTableBody = $("#instructors-table-body");
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
    console.log(event.target);
    if (event.target && event.target.classList.contains("revoke-access-button")) {
      const courseInstructorTeamId = event.target.getAttribute("data-course-instructor-team-id");
      revokeAccess(courseInstructorTeamId);
    }
  });

$(function () {
  const cssUrl = "https://cdn.jsdelivr.net/npm/@edx/paragon@20.45.5/dist/paragon.min.css";

  $("<link>")
    .attr({
      href: cssUrl,
      rel: "stylesheet",
    })
    .appendTo("head");
});
