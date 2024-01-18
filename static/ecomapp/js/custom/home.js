let box = document.getElementById("notification_box");
const paragraph = document.getElementById("notification_paragraph");
const nav_items = document.getElementsByClassName("nav-item");
let slides = document.getElementsByClassName("slides");
let category_box = document.getElementById("CategoryBox");
let home_section = document.getElementById("home_section");
let navbar = document.getElementById("navbar");
let counter = 0;

home_section.style.marginTop = `${navbar.offsetHeight + 2}px !important`;
console.log(navbar);
console.log("helloworld");
window.addEventListener("resize", function() {
  if(window.innerWidth > 1300 && category_box.style.display !== "block"){
    category_box.style.display = "block";
  }
  if(window.innerWidth <=1300&& category_box.style.display ==="block"){
    category_box.style.display="none";
  }
})
for (let i = 0; i < nav_items.length; i++) {
  nav_items[i].setAttribute("class", "nav-item");
}
for (let i = 0; i < slides.length; i++) {
  slides[i].style.left = `${i * 100}%`;
  if (i === 0) {
    document.getElementById("1").style.background = "#ffffff";
  }
}
console.log("helloworld");
var interval = setInterval(sliderRight, 3000);

const sliderLeft = () => {
  console.log("Helloworld");
  if (counter - 1 < 0) {
    counter = slides.length - 1;
  } else {
    counter--;
  }
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.left = `${Math.abs(counter - i) * 100}%`;
    if (counter - i === 0) {
      document.getElementById(`${counter + 1}`).style.background = "#ffffff";
    } else {
      document.getElementById(`${i + 1}`).style.background = "#C4C4C4";
    }
  }
};

const sliderRight = () => {
  if (counter === slides.length - 1) {
    counter = 0;
  } else {
    counter++;
  }
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.left = `${Math.abs(counter - i) * 100}%`;
    if (counter - i === 0) {
      document.getElementById(`${counter + 1}`).style.background = "#ffffff";
    } else {
      let dots = document.getElementById(`${i + 1}`);
      document.getElementById(`${i + 1}`).style.background = "#C4C4C4";
    }
  }
};

const buttonLeftClick = (box_name) => {
  let mainBox = document.getElementById(`main_box_${box_name}`);
  mainBox.scrollLeft -= 300;
};

const buttonRightClick = (box_name) => {
  let mainBox = document.getElementById(`main_box_${box_name}`);
  mainBox.scrollLeft += 300;
};

const showCategoryDiv = (category_id) => {
  const category_div = document.getElementById(
    `sub_category_div_${category_id}`
  );

  const sub_categ_div = document.getElementsByClassName(
    "Home_Top_SubCategories"
  );
  for (let i = 0; i < sub_categ_div.length; i++) {
    if (sub_categ_div[i] == category_div) {
      continue;
    }
    sub_categ_div[i].style.display = "none";
  }
  if (category_div.style.display === "block") {
    category_div.style.display = "none";
  } else {
    category_div.style.display = "block";
  }
};

const hoverCategory = () => {
  let windowWidth = window.innerWidth;
  if (windowWidth < 1300) {
    category_box.style.display = "block";
  }
};
const outFromCategory = () => {
  let windowWidth = window.innerWidth;
  if (windowWidth < 1300) {
    category_box.style.display = "none";
  }
};

const hoverBox = (box_name) => {
  let left_button = document.getElementById(`scroll_left_${box_name}`);
  let right_button = document.getElementById(`scroll_right_${box_name}`);
  left_button.style.display = "block";
  right_button.style.display = "block";
};
const outFromBox = (box_name) => {
  // let left_button = document.getElementById(`scroll_left_${box_name}`);
  // let right_button = document.getElementById(`scroll_right_${box_name}`);
  // const timeout = setTimeout(()=>{
  //   left_button.style.display="none";
  //   right_button.style.display ="none";
  // },5000);
  // clearTimeout(timeout);
};
const hoverItem = (product_name) => {
  let logo_box = document.getElementById(`logo_box_${product_name}`);
  logo_box.style.display = "none";
};

const to_the_product_item = (product_name) =>{
  // console.log(product_name);
  let add_to_cart = document.getElementById(`add_to_cart_${product_name}`);
  // console.log(add_to_cart);
  add_to_cart.style.display = "flex";
}
const out_from_product_item = (product_name) =>{
  let add_to_cart = document.getElementById(`add_to_cart_${product_name}`);
  // console.log(add_to_cart);
  add_to_cart.style.display = "none";
}

