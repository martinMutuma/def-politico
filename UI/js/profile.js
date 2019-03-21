var inputImage = document.getElementById("input-field");
function uploadImage(event) {
  event.preventDefault();
  let reader = new FileReader();

  reader.onload = function() {
    if (reader.readyState == 2) {
      let image = reader.result;
      function uploadImgur() {
        event.preventDefault();
        var strImage = image.replace(/^data:image\/[a-z]+;base64,/, "");
        data = new FormData();
        data.append("image", strImage);
        fetch("https://api.imgur.com/3/image", {
          method: "POST",
          headers: {
            Authorization: "Client-ID 6c78ded85463291"
          },
          body: data
        })
          .then(resp => resp.json())
          .then(data => {
            let image_url = data.data.link;

            fetch(
              `https://premier-voting.herokuapp.com/api/v2/user/update_image`,
              {
                method: "PATCH",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                  url: image_url
                })
              }
            )
              .then(resp => resp.json())
              .then(data => {
                if (data.status !== 200) {
                  console.log(data.error);
                } else {
                  console.log(data.message);
                }
              });
          });
      }
      uploadImgur();
    }
  };

  reader.readAsDataURL(event.target.files[0]);
}

inputImage.addEventListener("change", uploadImage);
