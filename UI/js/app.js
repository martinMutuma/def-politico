/**
 * This file will contain all app logic
 */

/**
 * Convinience methods and properties
 */
const BASE_URL = "https://premier-voting.herokuapp.com/api/v2";
var office_ids = [];

function getToken() {
  token = localStorage.getItem("token");
  if (token) return token;
  window.location.replace("signup.html");
  return null;
}

function createNode(type, id, clazz) {
  const node = document.createElement(type);
  node.classList.add(clazz);
  node.id = id;
  return node;
}

function showModal(modal_id) {
  document.getElementById(modal_id).style.display = "block";
}

function tokenError(status) {
  if (status === 401) {
    window.location.replace("signup.html");
    return true;
  }
  return false;
}

function displayError(msg) {
  document.getElementById("snackbar").innerText = msg;
  document.getElementById("snackbar").style.backgroundColor = "#d32f2f";
  showSnackbar();
}

function displaySuccess(msg) {
  document.getElementById("snackbar").innerText = msg;
  document.getElementById("snackbar").style.backgroundColor = "#1abc9c";
  showSnackbar();
}

function displayInfo(msg) {
  document.getElementById("snackbar").innerText = msg;
  document.getElementById("snackbar").style.backgroundColor = "#2980b9";
  showSnackbar();
}

function showSnackbar() {
  var x = document.getElementById("snackbar");
  x.className = "show";
  setTimeout(function() {
    x.className = x.className.replace("show", "");
  }, 3000);
}

/**
 * Login function
 */
function onLogin() {
  loader = document.getElementById("load-modal");
  loader.style.display = "block";

  fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email: document.getElementById("login_email").value,
      password: document.getElementById("login_password").value
    })
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        var user = data.data[0].user;
        var votingHistory = data.data[0].voting_history;

        // Save user profile to local storage
        localStorage.setItem("token", data.data[0].token);
        localStorage.setItem("firstname", user.firstname);
        localStorage.setItem("lastname", user.lastname);
        localStorage.setItem("email", user.email);
        localStorage.setItem("phone", user.phonenumber);
        localStorage.setItem("admin", user.admin);
        localStorage.setItem("uid", user.id);
        localStorage.setItem("passport_url", user.passport_url);
        votingHistory.forEach(function(history) {
          localStorage.setItem(`vote-${history.office}`, history.candidate);
        });
        // Redirect to homepage after successful login
        window.location.replace("index.html");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {
      console.log(error);
      loader.style.display = "none";
      displayError("Please check your connection");
    });
}

/**
 * Password reset function
 */
function onResetPassword() {
  loader = document.getElementById("load-modal");
  loader.style.display = "block";

  let email = document.getElementById("login_email").value;
  if (email.length < 3) {
    displayError("Please provide a valid email");
    return;
  }

  fetch(`${BASE_URL}/auth/reset`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email: email
    })
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        displaySuccess(data.data[0].message);
      } else {
        displayError("Please provide a valid email");
      }
    })
    .catch(error => {
      loader.style.display = "none";
      displayError("Please provide a valid email");
    });
}

/**
 * Signup function
 */
function onSignup() {
  password = document.getElementById("password").value;
  confirm_password = document.getElementById("confirm").value;

  if (password !== confirm_password) {
    displayError("Passwords do not match");
    return;
  }

  loader = document.getElementById("load-modal");
  loader.style.display = "block";

  let payload = {
    firstname: document.getElementById("firstname").value,
    lastname: document.getElementById("lastname").value,
    othername: document.getElementById("othername").value,
    phoneNumber: document.getElementById("phoneNumber").value,
    passportUrl: document.getElementById("passportUrl").value,
    isAdmin: false,
    email: document.getElementById("email").value,
    password: password
  };

  fetch(`${BASE_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      console.log(data);
      if (data.status === 201) {
        var user = data.data[0].user;

        // Save user profile to local storage
        localStorage.setItem("token", data.data[0].token);
        localStorage.setItem("firstname", user.firstname);
        localStorage.setItem("lastname", user.lastname);
        localStorage.setItem("email", user.email);
        localStorage.setItem("phone", user.phonenumber);
        localStorage.setItem("admin", user.isAdmin);
        localStorage.setItem("uid", user.id);
        localStorage.setItem("passport_url", user.passport_url);
        // Redirect to homepage after successful login
        window.location.replace("index.html");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {
      loader.style.display = "none";
      displayError("Please check your connection");
    });
}

function resetPassword() {
  let password = document.getElementById("password").value;
  let c_password = document.getElementById("c-password").value;
  if (password !== c_password) {
    displayError("Passwords do not match");
    return;
  }

  let token = location.search.replace("?token=", "");

  loader = document.getElementById("load-modal");
  loader.style.display = "block";

  let payload = {
    password: password
  };

  fetch(`${BASE_URL}/reset-password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        displaySuccess("Your password has been updated");

        setTimeout(function() {
          window.location.replace("signup.html?tab=2");
        }, 1500);
      } else {
        displayError(data.error);
      }
    })
    .catch(error => {
      loader.style.display = "none";
      displayError("Please check your connection");
    });
}

/**
 * PROFILE PAGE
 */
function loadUserProfile() {
  fname = localStorage.getItem("firstname");
  lname = localStorage.getItem("lastname");
  document.getElementById("username").innerText = `${fname} ${lname}`;
  document.getElementById("email").innerText = localStorage.getItem("email");
  document.getElementById("phone").innerText = localStorage.getItem("phone");
  document.getElementById("photo").src = localStorage.getItem("passport_url");
  initAdmin();
}

function loadVotingHistory() {
  document.getElementById("voting-history").innerHTML = "";

  loader = document.getElementById("loader");
  loader.style.display = "block";

  fetch(`${BASE_URL}/voting-history`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      console.log(data);
      if (data.status === 200) {
        results = document.getElementById("voting-history");

        let current_year = createNode("h1", "current-year", "h1");
        current_year.innerText = new Date().getFullYear();
        results.appendChild(current_year);

        data.data.forEach(function(result) {
          let result_node = createNode("div", "", "candidate");

          let percentage = (result.results / result.total_votes) * 100;

          result_node.innerHTML = `
                <img src="${result.passport_url}" class="profile"/>
                <div class="candidate-details">
                    <span class="candidate-name">${result.candidate}</span>
                    <span class="candidate-position">${result.office}</span>
                    <span class="candidate-party">${result.party}</span>
                    <span class="candidate-results">Votes: <span class="outof">${
                      result.results
                    }/${
            result.total_votes
          }</span>   <span class="vote-perc">${Math.ceil(
            percentage
          )}%</span></span>
                </div>
                <img src="images/won.png" style="display: ${
                  (percentage => 50) ? "block" : "none"
                }" class="win-icon"/>
                `;

          results.appendChild(result_node);
        });

        if (data.data.length == 0) {
          let notyet = createNode("h3", "not-yet", "center-prompt");
          notyet.innerText = "You have not voted for any candidate yet";
          results.appendChild(notyet);
        }
      } else if (tokenError(data.status)) {
        loader.style.display = "none";
        console.log("Expired token");
      } else {
        loader.style.display = "none";
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function on_logout() {
  localStorage.clear();
  window.location.replace("signup.html");
}

function loadOffices() {
  fetch(`${BASE_URL}/offices`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 200) {
        offices = document.getElementById("office-list");

        data.data.forEach(function(office) {
          let office_node = createNode("div", office.id, "office");
          office_node.innerText = office.name;
          office_node.addEventListener("click", function() {
            showModal("vote-modal");
            localStorage.setItem("office-id", this.id);
            loadCandidatesHomePage(this.id, office.name);
          });
          offices.appendChild(office_node);
        });
      } else if (tokenError(data.status)) {
        console.log("Expired token");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function loadOfficesInPartyDetail() {
  fetch(`${BASE_URL}/offices`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 200) {
        offices = document.getElementById("offices-vert");

        data.data.forEach(function(office) {
          let office_node = createNode(
            "div",
            `office-${office.id}-container`,
            "office-row"
          );
          office_node.innerHTML = `
                <div class="office-content">
                    <div class="office-name"> &nbsp; ${office.name}</div>
                    <button id="${
                      office.id
                    }" onclick="vieForOffice(this.id);">VIE</button>
                </div>
                <hr>
                `;
          offices.appendChild(office_node);
        });
      } else if (tokenError(data.status)) {
        console.log("Expired token");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function createOffice() {
  loader = document.getElementById("load-modal");
  loader.style.display = "block";

  let payload = {
    name: document.getElementById("office-name").value,
    type: document.getElementById("office-type").value
  };

  fetch(`${BASE_URL}/offices`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 201) {
        displaySuccess("Office created successfuly");

        setTimeout(function() {
          window.location.replace("index.html");
        }, 2000);
      } else {
        displayError(data.error);
      }
    })
    .catch(error => {
      loader.style.display = "none";
      displayError("Please check your connection");
    });
}

/**
 * Create party function
 */

function onCreatePartySubmit() {
  if (localStorage.getItem("editMode")) {
    editParty();
  } else {
    createParty();
  }
}

function createParty() {
  loader = document.getElementById("load-modal");
  loader.style.display = "block";

  let payload = {
    name: document.getElementById("party-name").value,
    slogan: document.getElementById("slogan").value,
    hq_address: document.getElementById("hq_address").value,
    logo_url: document.getElementById("logo_url").value,
    manifesto: document.getElementById("manifesto").value
  };

  fetch(`${BASE_URL}/parties`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 201) {
        var party_id = data.data[0].id;

        displaySuccess("Party created successfuly");

        localStorage.setItem("party-id", party_id);
        setTimeout(function() {
          showParty(party_id);
        }, 2000);
      } else {
        displayError(data.error);
      }
    })
    .catch(error => {
      loader.style.display = "none";
      displayError("Please check your connection");
    });
}

function onEditParty() {
  localStorage.setItem("editMode", "true");
  setTimeout(function() {
    location.href = "create-party.html";
  }, 1000);
}

function editParty() {
  loader = document.getElementById("load-modal");
  loader.style.display = "block";

  let payload = {
    name: document.getElementById("party-name").value,
    slogan: document.getElementById("slogan").value,
    hq_address: document.getElementById("hq_address").value,
    logo_url: document.getElementById("logo_url").value,
    manifesto: document.getElementById("manifesto").value,
    id: localStorage.getItem("party-id")
  };

  fetch(`${BASE_URL}/parties`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 201) {
        var party_id = data.data[0].id;

        setTimeout(function() {
          showParty(party_id);
        }, 1000);
      } else {
        displayError(data.error);
      }
    })
    .catch(error => {
      loader.style.display = "none";
      displayError("Please check your connection");
    });
}

function loadParties() {
  loader = document.getElementById("loader");
  loader.style.display = "block";

  fetch(`${BASE_URL}/parties`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        parties = document.getElementById("party-list");

        data.data.forEach(function(party) {
          let party_node = createNode("div", party.id, "icon-card");
          var logo_url = party.logo_url;

          party_node.innerHTML = `
                <img src="${logo_url}"/>

                <div class="icon-card-content">
                    <span class="icon-card-title">${party.name}</span>
                    <span class="icon-card-slogan">${party.manifesto}</span>
                    <button>VIEW PARTY</button>
                </div>
                `;
          party_node.addEventListener("click", function(event) {
            localStorage.setItem("party-id", this.id);
            showParty(this.id);
          });
          parties.appendChild(party_node);
        });
      } else if (tokenError(data.status)) {
        loader.style.display = "none";
        console.log("Expired token");
      } else {
        displayError(data.error);
        loader.style.display = "none";
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function loadSingleParty() {
  id = localStorage.getItem("party-id");

  if (!id) return;
  loader = document.getElementById("loader");
  loader.style.display = "block";

  fetch(`${BASE_URL}/parties/${id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        var party = data.data[0];
        document.getElementById("party-name").innerText = party.name;
        document.getElementById("party-slogan").innerText = party.slogan;
        document.getElementById("party-icon").src = party.logo_url;
      } else if (tokenError(data.status)) {
        console.log("Expired token");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {
      loader.style.display = "none";
    });
}

function loadSinglePartyEditMode() {
  loader = document.getElementById("load-modal");
  loader.style.display = "block";
  id = localStorage.getItem("party-id");

  if (!id) return;

  fetch(`${BASE_URL}/parties/${id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        var party = data.data[0];
        document.getElementById("party-name").value = party.name;
        document.getElementById("slogan").value = party.slogan;
        document.getElementById("hq_address").value = party.hq_address;
        document.getElementById("manifesto").value = party.manifesto;
        document.getElementById("logo_url").value = party.logo_url;
      } else if (tokenError(data.status)) {
        console.log("Expired token");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {
      loader.style.display = "none";
    });
}

function deleteParty() {
  id = localStorage.getItem("party-id");

  if (!id) return;
  if (!confirm("You are about to delete this party")) {
    return;
  }

  fetch(`${BASE_URL}/parties/${id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 200) {
        displaySuccess("Party Deleted");
        setTimeout(function() {
          window.location.replace("index.html");
        }, 2000);
      } else if (tokenError(data.status)) {
        console.log("Expired token");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function loadCandidates() {
  id = localStorage.getItem("party-id");
  if (!id) return;

  document.getElementById("candidate-list").innerHTML = "";

  const url = `${BASE_URL}/party/${id}/candidates`;
  console.log(url);

  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 200) {
        candidates = document.getElementById("candidate-list");

        data.data.forEach(function(candidate) {
          let candidate_node = createNode("div", candidate.id, "icon-card");

          candidate_node.innerHTML = `
                <img src="${candidate.passport_url}"/>

                <div class="icon-card-content">
                    <span class="icon-card-title">${candidate.candidate}</span>
                    <span class="icon-card-subtitle">${candidate.office}</span>
                    <span class="icon-card-slogan">Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quibusdam cupiditate maiores accusamus. Odit perferendis dolores architecto iste repellendus aut quod sunt nostrum aliquam, sed quae! Pariatur maiores numquam similique architecto.</span>
                </div>
                `;

          candidates.appendChild(candidate_node);
        });
      } else if (tokenError(data.status)) {
        console.log("Expired token");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function loadCandidatesHomePage(office_id, name) {
  document.getElementById("candidate-list").innerHTML = "";
  document.getElementById("office-name").innerText = name;

  loader = document.getElementById("vote-loader");
  loader.style.display = "block";

  fetch(`${BASE_URL}/office/${office_id}/candidates`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        let voteExists = localStorage.getItem(`vote-${office_id}`);
        let uid = localStorage.getItem("uid");

        candidates = document.getElementById("candidate-list");

        data.data.forEach(function(candidate) {
          let candidate_node = createNode("div", candidate.id, "candidate");

          let action = `<button class="vote-button" onclick="castVote(${
            candidate.id
          }, ${office_id})">VOTE</button>`;
          if (voteExists) {
            if (candidate.id == voteExists) {
              action = '<img class="check" src="images/checkmark2.png"/>';
            } else {
              action = "";
            }
          }

          candidate_node.innerHTML = `
                    <img src="${candidate.passport_url}" />
                    <div class="candidate-details">
                        <span class="candidate-name">${
                          candidate.candidate
                        }</span>
                        <span class="candidate-position">${
                          candidate.office
                        }</span>
                        <span class="candidate-party">${candidate.party}</span>
                    </div>
                    ${action}
                `;

          candidates.appendChild(candidate_node);
        });
      } else if (tokenError(data.status)) {
        console.log("Expired token");
        loader.style.display = "none";
      } else {
        displayError(data.error);
        console.log(data.status);
        loader.style.display = "none";
      }
    })
    .catch(error => {});
}

function loadAllResults() {
  document.getElementById("results-list").innerHTML = "";

  loader = document.getElementById("loader");
  loader.style.display = "block";

  fetch(`${BASE_URL}/results`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";

      if (data.status === 200) {
        results = document.getElementById("results-list");

        data.data.forEach(function(result) {
          let result_node = createNode(
            "div",
            result.candidate,
            "candidate-result"
          );

          result_node.innerHTML = `
                <img id="candidate-result-photo" src="${result.passport_url}" />
                <div class="candidate-result-details">
                        <h1 class="winner-user">${result.candidate}</h1>
                        <h2 class="winner-pos">${result.office}</h2>
                        <h2 class="winner-party">${result.party}</h2>
                </div>
                <div class="result">
                ${result.results}
                <span style="font-size:14px;">votes</span>
                </div>
                `;

          results.appendChild(result_node);
        });

        if (data.data.length == 0) {
          displayInfo("No results for this Election yet");
        }
      } else if (tokenError(data.status)) {
        loader.style.display = "none";
        console.log("Expired token");
      } else {
        loader.style.display = "none";
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function loadOfficeResults(id) {
  id = id.split("-")[1];

  document.getElementById("results-list").innerHTML = "";
  loader = document.getElementById("loader");
  loader.style.display = "block";

  fetch(`${BASE_URL}/office/${id}/result`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";
      if (data.status === 200) {
        results = document.getElementById("results-list");

        data.data.forEach(function(result) {
          let result_node = createNode(
            "div",
            result.candidate,
            "candidate-result"
          );

          result_node.innerHTML = `
                <img id="candidate-result-photo" src="${result.passport_url}" />
                <div class="candidate-result-details">
                        <h1 class="winner-user">${result.candidate}</h1>
                        <h2 class="winner-pos">${result.office}</h2>
                        <h2 class="winner-party">${result.party}</h2>
                </div>
                <div class="result">
                ${result.results}
                <span style="font-size:14px;">votes</span>
                </div>
                `;

          results.appendChild(result_node);
        });

        if (data.data.length === 0) {
          displayInfo("No results for selected office");
        }
      } else if (tokenError(data.status)) {
        loader.style.display = "none";
        console.log("Expired token");
      } else {
        displayError(data.error);
        loader.style.display = "none";
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function loadOfficesInResultsPage() {
  office_ids = [];

  fetch(`${BASE_URL}/offices`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === 200) {
        offices = document.getElementById("office-list");

        data.data.forEach(function(office) {
          let office_node = createNode("div", `office-${office.id}`, "office");
          if (office_ids.length == 0) {
            office_node.classList.add("focused");
            loadOfficeResults(`office-${office.id}`);
          }
          office_node.innerText = office.name;
          office_ids.push(office.id);
          office_node.addEventListener("click", function() {
            selectOffice(this.id);
            loadOfficeResults(this.id);
          });
          offices.appendChild(office_node);
        });
      } else if (tokenError(data.status)) {
        console.log("Expired token");
      } else {
        displayError(data.error);
        console.log(data.status);
      }
    })
    .catch(error => {});
}

function selectOffice(office_id) {
  office_ids.forEach(function(id) {
    document.getElementById(`office-${id}`).classList.remove("focused");
  });
  document.getElementById(office_id).classList.add("focused");
}

function vieForOffice(office_id) {
  party_id = localStorage.getItem("party-id");
  uid = localStorage.getItem("uid");
  console.log(office_id);

  // loader = document.getElementById('load-modal');
  // loader.style.display = 'block';

  let payload = {
    party: parseInt(party_id),
    candidate: parseInt(uid)
  };

  fetch(`${BASE_URL}/office/${office_id}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      // loader.style.display = 'none';

      console.log(data);
      if (data.status === 201) {
        loadCandidates();
        displaySuccess(data.message);
      } else {
        displayError(data.error);
      }
    })
    .catch(error => {
      // loader.style.display = 'none';
      displayError("Please check your connection");
    });
}

function castVote(candidate, office_id) {
  let payload = {
    office: parseInt(office_id),
    candidate: parseInt(candidate)
  };

  fetch(`${BASE_URL}/votes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      authorization: `Bearer ${getToken()}`
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      if (data.status === 201) {
        closeModal("vote-modal");
        displaySuccess(data.message);
        localStorage.setItem(`vote-${office_id}`, candidate);
      } else {
        displayError(data.error);
      }
    })
    .catch(error => {
      displayError("Please check your connection");
    });
}

function showParty(id) {
  window.location = "party-detail.html";
  if (localStorage.getItem("editMode")) {
    displaySuccess("Party updated successfuly");
    localStorage.removeItem("editMode");
  }
}

function initHomePage() {
  loadOffices();
  loadParties();
  initAdmin();
}

function initPartyDetail() {
  loadOfficesInPartyDetail();
  loadSingleParty();
  loadCandidates();
  if (!initAdmin()) {
    document.getElementsByClassName("actions")[0].style.display = "none";
  }
}

function initResults() {
  loadOfficesInResultsPage();
  initAdmin();
}

function initAddParty() {
  if (localStorage.getItem("editMode")) {
    loadSinglePartyEditMode();
    document.getElementById("page-title").innerText = "EDIT PARTY";
  }
}

function initAdmin() {
  isAdmin = localStorage.getItem("admin");
  if (isAdmin == "false") {
    document.getElementById("new-party-button").style.display = "none";
    document.getElementById("new-office-button").style.display = "none";
    return false;
  }
  return true;
}
