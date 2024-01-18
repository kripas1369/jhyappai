console.log("hello world.");
const bottom_floating_navigation_bar = document.getElementById(
  "bottom_floating_navigation_bar"
);
const search_product_field = document.getElementById("search_product");
const search_small_product = document.getElementById("search_small_product");
const search_button = document.getElementById("button_search");
const display_back = document.getElementById("display_back");


const getTotalCartItems = () => {
  let cartItems = localStorage.getItem("cartItems");
  if (cartItems === null) {
    return 0;
  }
  document.getElementById("cart_itemnumber").style.display = "";
  let totalCount = 0;
  cartItems = JSON.parse(localStorage.getItem("cartItems"));

  for (let i = 0; i < cartItems.length; i++) {
    totalCount += parseInt(cartItems[i].quantity);
  }
  return totalCount;
};
document.getElementById("cart_itemnumber").innerHTML = getTotalCartItems();

const listenWindowWidth = () => {
  if (window.innerWidth <= 600) {
    bottom_floating_navigation_bar.style.display = "flex";
  }
};

listenWindowWidth();

window.addEventListener("resize", (event) => {
  if (event.delegateTarget.innerWidth <= 600) {
    bottom_floating_navigation_bar.style.display = "flex";
  } else {
    bottom_floating_navigation_bar.style.display = "none";
  }
});
search_button.addEventListener("click",()=>{
  console.log("hello world");
  const location = `${window.location.origin}/search?product=${search_small_product.value}`;
  window.location.replace(location);
})


// const displayBack = () =>{
//   console.log("helloworld");
//   search_box.style.display = "none";
// }
display_back.onclick =()=>{
  console.log("helloworld")
}



