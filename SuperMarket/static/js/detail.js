let miniImage = document.querySelectorAll(".miniImages");
let bigImage = document.querySelector("#BigImage");

function changeBigImage(event){
    bigImage.src = event.target.src;
    miniImage.forEach((image)=>{
        image.classList.remove("ActiveImage");
    });
    event.target.classList.add("ActiveImage");
}

miniImage.forEach((image, i)=>{
   image.addEventListener("click", changeBigImage);
});



let addressCards = document.querySelectorAll(".AddressCard");
let addressField = document.querySelector("#addressField");


function toggleOtherAddressCards(){
    addressCards.forEach( (element, num) =>{
        element.classList.remove("SelectedAddressCard");
    } );
}

addressCards.forEach((card, num) => {

    card.addEventListener("click", (event) => {
        toggleOtherAddressCards();
        card.classList.toggle("SelectedAddressCard");
        addressField.value = card.id;
    });

});