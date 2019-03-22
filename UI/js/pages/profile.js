var inputImage = document.getElementById("input-field");

function uploadImgur(image) {
  event.preventDefault();
  var strImage = image.replace(/^data:image\/[a-z]+;base64,/, "");
  let data = new FormData();
  data.append("image", strImage);
  fetch("https://api.imgur.com/3/image", {
    method: "POST",
    headers: {
      Authorization: "Client-ID 6c78ded85463291"
    },
    body: data
  })
    .then((resp) => resp.json())
    .then((data) => {
      let imageUrl = data.data.link;
      let token = localStorage.getItem("token");
      localStorage.setItem("passport_url", imageUrl);
      
      fetch(
        "https://premier-voting.herokuapp.com/api/v2/user/update_image",
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({
            url: imageUrl
          })
        }
        
      )
        .then((resp) => resp.json())
        .then((data) => {
          if (data.status == 200) {
         location.reload();
          }
        });
    });
}

function uploadImage(event) {
  event.preventDefault();
  let reader = new FileReader();

  reader.onload = function() {
    if (reader.readyState === 2) {
      let image = reader.result;
      uploadImgur(image);
    }
  };

  reader.readAsDataURL(event.target.files[0]);
  
}

inputImage.addEventListener("change", uploadImage);
