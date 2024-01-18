document.getElementById("LoginHeading").style.borderBottom =
  "3px solid #f57224";
document.getElementById("LoginBox").style.display = "block";
document.getElementById("RegisterBox").style.display = "none";

document.getElementById("LoginHeading").addEventListener("click", () => {
  console.log("hello login");
  document.getElementById("RegisterHeading").style.borderBottom =
    "3px solid #777";
  document.getElementById("LoginHeading").style.borderBottom =
    "3px solid #f57224";
  document.getElementById("LoginBox").style.display = "block";
  document.getElementById("RegisterBox").style.display = "none";
});

document.getElementById("RegisterHeading").addEventListener("click", () => {
  console.log("hello register");
  document.getElementById("LoginHeading").style.borderBottom = "3px solid #777";
  document.getElementById("RegisterHeading").style.borderBottom =
    "3px solid #f57224";
  document.getElementById("LoginBox").style.display = "none";
  document.getElementById("RegisterBox").style.display = "block";
});
