const wishdocumenticon = document.getElementById("wishlisticon_div");
let box = document.getElementById("notification_box");
let wishlist = document.getElementById("wishlist");
const fav_icon = document.getElementById("fav_icon");

const increaseQuantityNumber = (id) => {
  let num = parseInt(
    document.getElementById(`quantity_number_${id}`).innerHTML
  );
  if (num == 10) {
    return;
  }
  document.getElementById(`quantity_number_${id}`).innerHTML = num + 1;
};
const decreaseQuantityNumber = (id) => {
  let num = parseInt(
    document.getElementById(`quantity_number_${id}`).innerHTML
  );
  if (num == 1) {
    return;
  }
  document.getElementById(`quantity_number_${id}`).innerHTML = num - 1;
};

wishdocumenticon.addEventListener("click", () => {
  let wishlist_num = parseInt(
    document.getElementById("wishlist_itemnumber").innerHTML
  );

  if (wishdocumenticon.children[0].style.color == "red") {
    wishdocumenticon.children[0].style.color = "grey";
    document.getElementById("wishlist_itemnumber").innerHTML = wishlist_num - 1;
  } else {
    wishdocumenticon.children[0].style.color = "red";
    document.getElementById("wishlist_itemnumber").innerHTML = wishlist_num + 1;
  }
  const productId = document.getElementById("hide_product_id").value;

  axios
    .get(`${window.location.origin}/add_to_wishlist/${productId}`)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
});

const change_image = (index) => {
  const abc = document.getElementsByClassName("Single_Box_Image_Box_Image");
  for (let i = 0; i < abc.length; i++) {
    abc[i].style.border = "none";
  }
  const d = document.getElementById("large_big_image");
  const a = document.getElementById(`${index}_image`);
  a.style.border = "2px solid #f57224";
  d.src = a.src;
};

//javascript for Review and description

// const showDescription = () => {
//   description_heading.style.color = "#f57224";
//   review_heading.style.color = "#1f1f1f";
//   review_body.style.display = "none";
//   description_body.style.display = "flex";
//   description_body.style.justifyContent = "center";
//   description_body.style.alignItems = "center";
// };

// const showReview = () => {
//   description_heading.style.color = "#1f1f1f";
//   review_heading.style.color = "#f57224";
//   review_body.style.display = "block";
//   description_body.style.display = "none";
// };

const takeReview = (id) => {
  var star_elements = document.querySelectorAll(
    ".Single_Description_Review_Rating_Stars_Star"
  );
  let rating_input = document.getElementById("hidden_star_value");
  rating_input.value = id;
  for (let i = 0; i <= id; i++) {
    star_elements[i].style.color = "#f57224";
  }
  for (let i = id; i < 5; i++) {
    star_elements[i].style.color = "#777777";
  }
};

const buyNow = (productId, productPrice) => {
  const quantiy = document.getElementById(
    `quantity_number_${productId}`
  ).innerHTML;
  window.location.replace(
    `${
      window.location.origin
    }/billing/?product_id=${productId}&quantity=${quantiy.trim()}&price=${
      parseFloat(productPrice) * parseInt(quantiy.trim())
    }`
  );
};

// const buyNow = (
//   productName,
//   productSlug,
//   productId,
//   productImage,
//   productPrice
// ) => {
//   const cartItems = localStorage.getItem("cartItems");
//   const quantity = parseInt(
//     document.getElementById(`quantity_number_${productId}`).innerHTML
//   );
//   if (cartItems === null) {
//     localStorage.setItem(
//       "cartItems",
//       JSON.stringify([
//         {
//           productName,
//           productSlug,
//           productId,
//           productImage,
//           productPrice,
//           quantity,
//         },
//       ])
//     );
//   } else {
//     let cart = JSON.parse(localStorage.getItem("cartItems"));
//     let index = cart.findIndex((e) => e.productId === productId);
//     if (index === -1) {
//       cart.push({
//         productName,
//         productSlug,
//         productId,
//         productImage,
//         productPrice,
//         quantity,
//       });
//     } else {
//       cart[index].quantity = quantity + cart[index].quantity;
//     }
//     localStorage.setItem("cartItems", JSON.stringify(cart));
//   }

//   document.getElementById("cart_itemnumber").style.display = "";
//   document.getElementById("cart_itemnumber").innerHTML =
//     parseInt(document.getElementById("cart_itemnumber").innerHTML) +
//     parseInt(quantity);
// };

const addtocart = (
  productName,
  productSlug,
  productId,
  productImage,
  productPrice
) => {
  const cartItems = localStorage.getItem("cartItems");

  const quantity = parseInt(
    document.getElementById(`quantity_number_${productId}`).innerHTML
  );

  const success = `
    <div class="Header_Box_Message added_item_cart" id="homesuccess" >
      <p>${productName} added to cart.</p>
      <p>Quantity: ${quantity}</p>
    </div>`;
  box.innerHTML += success;

  setTimeout(() => {
    document.getElementById("homesuccess").remove();
  }, 5000);

  if (cartItems === null) {
    localStorage.setItem(
      "cartItems",
      JSON.stringify([
        {
          productName,
          productSlug,
          productId,
          productImage,
          productPrice,
          quantity: parseInt(quantity),
        },
      ])
    );
  } else {
    let cart = JSON.parse(localStorage.getItem("cartItems"));
    let index = cart.findIndex((e) => e.productId === productId);
    if (index === -1) {
      cart.push({
        productName,
        productSlug,
        productId,
        productImage,
        productPrice,
        quantity: parseInt(quantity),
      });
    } else {
      cart[index].quantity = parseInt(quantity + cart[index].quantity);
    }
    localStorage.setItem("cartItems", JSON.stringify(cart));
  }

  document.getElementById("cart_itemnumber").style.display = "";
  document.getElementById("cart_itemnumber").innerHTML =
    parseInt(document.getElementById("cart_itemnumber").innerHTML) +
    parseInt(quantity);
};

//Add To wishlist
const addToWishlist = () => {
  fav_icon.innerHTML = `
  <div class="Single_Box_Right_Wishlist_Button" onclick="removeFromWishlist()">
  <i style="font-size: 30px; color: red" class="fa-solid fa-heart"></i>
</div>`;
  // document.getElementById("success").style.display = "block"
  const success = `
    <div id="notification_item" class="Header_Box_Message notification" >
      <p>Added to wishlist.</p>
    </div>`;
  box.innerHTML += success;

  setTimeout(() => {
    document.getElementById("notification_item").remove();
  }, 5000);

  // wishlist.style.color = "red";
  // wishlist.style.zIndex = 10;
};

//Remove From Wishlist

const removeFromWishlist = () => {
  fav_icon.innerHTML = `
  <div class="Single_Box_Right_Wishlist_Button" onclick="addToWishlist()">
<i style="font-size: 30px; color: grey" class="fa-solid fa-heart"></i>
</div>

`;
  // document.getElementById("success").style.display="none";
  const success = `
    <div  id="notification_item" class="Header_Box_Message notification" >
      <p>Removed from wishlist.</p>
    </div>`;
  box.innerHTML += success;

  setTimeout(() => {
    document.getElementById("notification_item").remove();
  }, 5000);

  // wishlist.style.color = "grey";
  // wishlist.style.zIndex = 10;
};
