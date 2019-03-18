
function switchTab(tab,group){
    var i;
    var x = document.getElementsByClassName(group);
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none"; 
        x[i].style.opacity = 0; 
    }
    document.getElementById(tab).style.opacity = 1;
    document.getElementById(tab).style.display = "block";
}

function showNav() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }

  function showParty(){
      window.location = 'party-detail.html'
  }


////
function onVote(){
    console.log('voted');
}

////MODALS

function closeModal(_id){
    document.getElementById(_id).style.display='none';
}


function showModal(modal_id){
    document.getElementById(modal_id).style.display='block';
}