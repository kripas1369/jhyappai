import { SITE_NAME } from "./constants/site_name_constant.js";
document.title = `${SITE_NAME}-AboutUs`;

const nav_items = document.getElementsByClassName("nav-item");
for (let i = 0; i < nav_items.length; i++) {
  nav_items[i].setAttribute("class", "nav-item");
}
document
  .getElementById("aboutus_nav_item")
  .setAttribute("class", "nav-item active");
// Get all .faq-question
var questions = document.getElementsByClassName("faq-question");

// Assign openQuestion on click
for (var i = 0; i < questions.length; i++) {
  questions[i].onclick = openQuestion;
}

// Apply .hidden to sibling .faq-answer
// Apply .open to .faq-question
function openQuestion(event) {
  var answer = event.target.parentNode.getElementsByClassName("faq-answer")[0];

  if (-1 !== answer.className.indexOf("hidden")) {
    answer.className = answer.className.replace(" hidden", "");
  } else {
    answer.className += " hidden";
  }
  if (-1 !== event.target.className.indexOf("open")) {
    event.target.className = event.target.className.replace(" open", "");
  } else {
    event.target.className += " open";
  }
}

let boxes = document.getElementsByClassName("boxes");
let paragraph = document.getElementsByClassName("faqparagraph");
for(let i =0; i< paragraph.length; i++){
    paragraph[i].style.display = "none";
}
for(let i=0; i< boxes.length; i++){
    boxes[i].addEventListener("click",()=>{
        if(paragraph[i].style.display ==="none"){
            paragraph[i].style.display ="block";
        }else{
            paragraph[i].style.display ="none";
        }
    })
}
