let cart = document.getElementById("profile_logo");
let box = document.getElementById("profile_box");
let cart1 = document.getElementById("profile_logo_1");
let show_search =document.getElementById("Header_Show_Search");
let search_box = document.getElementById("search_box_small");
let find_search = document.getElementById("Header_Show_Find");
let show_input = document.getElementById("Header_Show_Input");
let navigation = document.getElementById("Navigation");
let navbar = document.getElementById('navbar'); // Get The NavBar
box.style.display = "none";
let click_logo = false;
var lastScrollTop; 

// window.addEventListener('scroll',function(){
//  //on every scroll this funtion will be called
//   var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
//   //This line will get the location on scroll
//   console.log()
//   if(scrollTop > lastScrollTop){ //if it will be greater than the previous
//     navbar.style.top=`-${navbar.offsetHeight}px`;
//     //set the value to the negetive of height of navbar 
//   }
//   else{
//     navbar.style.top='0';
//   }
//   lastScrollTop = scrollTop; //New Position Stored
// });
cart.addEventListener("click", (e) => {
  click_logo = true;
  if (box.style.display === "block") {
    box.style.display = "none";
  } else {
    box.style.display = "block";
  }
});
cart1.addEventListener("click", (e) => {
  if (box.style.display === "block") {
    box.style.display = "none";
  } else {
    box.style.display = "block";
  }
});

document.addEventListener("click", (event) => {
  const is_click_inside = box.contains(event.target);
  if (!is_click_inside && !click_logo) {
    if (box.style.display === "block") {
      box.style.display = "none";
    }
  }
});
box.addEventListener("mouseover", () => {
  click_logo = false;
});

show_search.addEventListener("click",()=>{
  console.log("helloworld");
  show_search.style.display = "none";
  find_search.style.display="block";
  show_input.style.display="block";
  navigation.style.flexDirection="column";
  // search_box.style.display = "block";
});

const searchProduct = () => {
  const location = `${window.location.origin}/search?product=${search_product_field.value}`;
  window.location.replace(location);
};




