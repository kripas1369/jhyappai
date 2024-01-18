const form = document.getElementById("wishlist_form");
const delete_or_add_to_cart = document.getElementById("delete_or_add_to_cart");
const wishlist_id = document.getElementById("wishlist_id");
let box = document.getElementById("notification_box");

const removeFromWishlist = (wishlistId) => {
  delete_or_add_to_cart.value = "delete";
  wishlist_id.value = wishlistId;
  form.submit();
};

const addToCart = (
  productName,
  productSlug,
  productId,
  productImage,
  productPrice,
  quantity
) => {
  const cartItems = localStorage.getItem("cartItems");

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
      cart[index].quantity =
        parseInt(quantity) + parseInt(cart[index].quantity);
    }
    localStorage.setItem("cartItems", JSON.stringify(cart));
  }

  document.getElementById("cart_itemnumber").style.display = "";
  document.getElementById("cart_itemnumber").innerHTML =
    parseInt(document.getElementById("cart_itemnumber").innerHTML) +
    parseInt(quantity);

  const success = `
    <div class="Header_Box_Message added_item_cart" id="homesuccess" >
      <p>Product added to cart.</p>
      <p>Quantity: 1</p>
    </div>`;
  box.innerHTML += success;

  setTimeout(() => {
    document.getElementById("homesuccess").remove();
  }, 5000);
};
