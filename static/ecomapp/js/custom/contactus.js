import {SITE_NAME} from "./constants/site_name_constant.js"
document.title=`${SITE_NAME}-ContactUs`

const nav_items=document.getElementsByClassName("nav-item")
for(let i=0;i<nav_items.length;i++)
{
    nav_items[i].setAttribute("class","nav-item")
}
document.getElementById("contactus_nav_item").setAttribute("class","nav-item active")
