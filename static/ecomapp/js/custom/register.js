import {SITE_NAME} from "./constants/site_name_constant.js"
document.title=`${SITE_NAME}-Register`

document.getElementById("aggreingterms_checkbox")
addEventListener("change",(e)=>{
    console.log(e.target.checked)
    if(e.target.checked===true)
    {
    document.getElementById("register_button").disabled=false;
    document.getElementById("register_button").style.backgroundColor="#f57224";
    }
    else {
    document.getElementById("register_button").disabled=true;
    document.getElementById("register_button").style.backgroundColor="#efefef";
    }

})

document.querySelector("form")[0].addEventListener("submit",(e)=>{
    e.preventDefault();
})

