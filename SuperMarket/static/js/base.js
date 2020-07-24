//############################# Buttons ############################# \\
let openShopCart = document.querySelector("#OpenShop");
let openUser = document.querySelector("#OpenUser");
let closeCart = document.querySelector("#closeShopCart");
let closeUserMenu = document.querySelector("#closeAccountMenu");


//############################# Shop Cart ############################# \\
// Open shop cart
openShopCart.addEventListener("click", (event) => {
    let shopCartMenu = document.querySelector(".ShopCartMenu");
    shopCartMenu.classList.toggle("ShopCartMenuActive");
});

//close ShopCart
closeCart.addEventListener("click", (event) =>{
    let shopCartMenu = document.querySelector(".ShopCartMenu");
    shopCartMenu.classList.toggle("ShopCartMenuActive");
});


//############################# Account Menu ############################# \\
// Open Account Menu
openUser.addEventListener('click', (event) => {
    let userMenu = document.querySelector(".AccountMenu");
    userMenu.classList.toggle("AccountMenuActive");
});

// close Account menu
closeUserMenu.addEventListener("click", (event) =>{
    let userMenu =  document.querySelector(".AccountMenu");
    userMenu.classList.toggle("AccountMenuActive");
});


// Set Navbar on scroll
window.addEventListener("scroll", (event) => {
    let navbar = document.querySelector(".Navbar");
    (window.pageYOffset>50) ? navbar.classList.add("NavbarActive") : navbar.classList.remove("NavbarActive");
});
