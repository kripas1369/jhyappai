const shopping_list_table = document.getElementById("shopping_list_table");
const shopping_list_price = document.getElementById("shopping_list_price");
const cart_is_empty = document.getElementById("cart_is_empty");
const subtotal_div_price = document.getElementById("subtotal_div");
const total_div_price = document.getElementById("total_div");
const product_cart_table_body = document.getElementById(
  "product_cart_table_body"
);
let cart_item_number = document.getElementById("cart_itemnumber");
let success = document.getElementById("success");
let success_paragraph = document.getElementById("success_paragraph");
let grandTotalOfAllItems = 0;
let box = document.getElementById("notification_box");

const truncateProductName = (productName) => {
  if (productName.length > 30) {
    return `${productName.substring(0, 30)}...`;
  } else {
    return productName;
  }
};

const cart_items = JSON.parse(localStorage.getItem("cartItems"));
cart_is_empty.style.display = "flex";

if (cart_items.length === 0) {
  shopping_list_table.style.display = "none";
  shopping_list_price.style.display = "none";
  cart_is_empty.style.display = "flex";
} else {
  cart_is_empty.style.display = "none";
  shopping_list_table.style.display = "block";
  shopping_list_price.style.display = "block";

  for (let i = 0; i < cart_items.length; i++) {
    grandTotalOfAllItems += cart_items[i].productPrice * cart_items[i].quantity;
    const data = `<tr id="table_row_${
      cart_items[i].productId
    }" class="ProductTable_Body_Box">
    <td class="ProductTable_Body_Box_Item">
        <img src="${cart_items[i].productImage}" alt="Product Item Rozai"
            class="ProductTable_Body_Box_Item_Image">
        <p>
        <a href="${window.location.origin}/product/${
      cart_items[i].productSlug
    }">
        ${truncateProductName(cart_items[i].productName)}
        </a>
        </p>

    </td>
    <td class="ProductTable_Body_Box_Item1">
    <button onclick="removeOneFromCart(${
      cart_items[i].productId
    })" class="ProductTable_Body_Box_Item1_ButtonPrimary">
    <i class="fa-solid fa-minus ProductTable_Body_Box_Item1_ButtonPrimary_Logo"></i>
    </button>
    <h3 id="car_items_quantity_${cart_items[i].productId}">
    ${cart_items[i].quantity}
    </h3>
    <button onclick="addToCart(${
      cart_items[i].productId
    })" class="ProductTable_Body_Box_Item1_ButtonPrimary">
    <i class="fa-solid fa-plus ProductTable_Body_Box_Item1_ButtonPrimary_Logo"></i>
    </button>
    </td>
    <td class="ProductTable_Body_Box_Item1">Rs. ${
      cart_items[i].productPrice
    }</td>
    <td id="total_price_quantity_${
      cart_items[i].productId
    }" class="ProductTable_Body_Box_Item1">${
      cart_items[i].productPrice * cart_items[i].quantity
    }</td>

    <td  class="ProductTable_Body_Box_Item">
          <button onclick="removeFromCart(${
            cart_items[i].productId
          })" class="ProductTable_Body_Box_Item_ButtonPrimary">
          <i class="fa-solid fa-xmark ProductTable_Body_Box_Item_ButtonPrimary_Logo"></i></button>
    </td>
</tr>`;
    product_cart_table_body.innerHTML += data;
  }
  subtotal_div_price.innerHTML = `${grandTotalOfAllItems}`;
  total_div_price.innerHTML = `${grandTotalOfAllItems}`;
}

//REMOVE WHOLE ROW FROM CART
const removeFromCart = (index) => {
  let cart_array = JSON.parse(localStorage.getItem("cartItems"));
  const cart_index = cart_array.findIndex((x) => x.productId == index);
  const product_name = cart_array[cart_index].productName;
  const quantity = cart_array[cart_index].quantity;
  const price = cart_array[cart_index].productPrice * quantity;
  cart_array = cart_array.filter((x) => x.productId != index);
  localStorage.setItem("cartItems", JSON.stringify(cart_array));

  const success = `
  <div class="Header_Box_Message success" id="shopping_success" >
    <p>${product_name} removed from cart </p>
  </div>`;

  box.innerHTML += success;

  setTimeout(() => {
    document.getElementById("shopping_success").remove();
  }, 3000);

  if (cart_array.length === 0) {
    shopping_list_table.style.display = "none";
    shopping_list_price.style.display = "none";
    cart_is_empty.style.display = "flex";
  }
  const tr = document.getElementById(`table_row_${index}`);
  tr.remove();
  const cart_number = document.getElementById("cart_itemnumber").innerHTML;
  document.getElementById("cart_itemnumber").innerHTML =
    parseInt(cart_number) - parseInt(quantity);

  subtotal_div_price.innerHTML =
    parseInt(subtotal_div_price.innerHTML) - parseInt(price);
  total_div_price.innerHTML =
    parseInt(total_div_price.innerHTML) - parseInt(price);
};

//ADDING INDIVIDUAL ITEMS TO THE CART
const addToCart = (index) => {
  let cart_array = JSON.parse(localStorage.getItem("cartItems"));
  const cart_index = cart_array.findIndex((x) => x.productId == index);

  const price = cart_array[cart_index].productPrice;
  cart_array[cart_index].quantity += 1;

  //CHANING CART ITEMS IN LOCAL STORAGE
  localStorage.setItem("cartItems", JSON.stringify(cart_array));

  //CHANGING THE QUANTITY NUMBER
  const tr = document.getElementById(`car_items_quantity_${index}`);
  tr.innerHTML = parseInt(tr.innerHTML) + 1;

  //UPDATING NAVBAR CART NUMBER
  const cart_number = document.getElementById("cart_itemnumber").innerHTML;
  document.getElementById("cart_itemnumber").innerHTML =
    parseInt(cart_number) + 1;

  //UPDATING TOTAL PRICE FOR ITEM IN ROW
  const total_item_price_row = document.getElementById(
    `total_price_quantity_${index}`
  );
  total_item_price_row.innerHTML =
    parseInt(total_item_price_row.innerHTML) + parseInt(price);

  //UPDATING  CART TOTAL PRICE
  subtotal_div_price.innerHTML =
    parseInt(subtotal_div_price.innerHTML) + parseInt(price);
  total_div_price.innerHTML =
    parseInt(total_div_price.innerHTML) + parseInt(price);
};

//REMOVING INDIVIDUAL ITESM FROM CART
const removeOneFromCart = (index) => {
  let cart_array = JSON.parse(localStorage.getItem("cartItems"));
  const cart_index = cart_array.findIndex((x) => x.productId == index);
  const price = cart_array[cart_index].productPrice;

  if (cart_array[cart_index].quantity == 1) {
    cart_array.splice(cart_index, 1);
    localStorage.setItem("cartItems", JSON.stringify(cart_array));
    console.log("yes its zero");
    const tr = document.getElementById(`table_row_${index}`);
    tr.remove();
    const cart_number = document.getElementById("cart_itemnumber").innerHTML;
    document.getElementById("cart_itemnumber").innerHTML =
      parseInt(cart_number) - 1;
  } else {
    cart_array[cart_index].quantity -= 1;

    //CHANING CART ITEMS IN LOCAL STORAGE
    localStorage.setItem("cartItems", JSON.stringify(cart_array));

    //CHANGING THE QUANTITY NUMBER
    const tr = document.getElementById(`car_items_quantity_${index}`);
    tr.innerHTML = parseInt(tr.innerHTML) - 1;

    //UPDATING NAVBAR CART NUMBER
    const cart_number = document.getElementById("cart_itemnumber").innerHTML;
    document.getElementById("cart_itemnumber").innerHTML =
      parseInt(cart_number) - 1;

    //UPDATING TOTAL PRICE FOR ITEM IN ROW
    const total_item_price_row = document.getElementById(
      `total_price_quantity_${index}`
    );
    total_item_price_row.innerHTML =
      parseInt(total_item_price_row.innerHTML) - parseInt(price);
  }

  //UPDATING  CART TOTAL PRICE
  subtotal_div_price.innerHTML =
    parseInt(subtotal_div_price.innerHTML) - parseInt(price);
  total_div_price.innerHTML =
    parseInt(total_div_price.innerHTML) - parseInt(price);
};

const showPopUpModal = () => {
  console.log("this is the popup model.");
  document.getElementById("login_popup_item").style.display = "flex";
};

const emptyCart = () => {
  shopping_list_price.style.display = "none";
  shopping_list_table.style.display = "none";
  const notification = `
  <div class="Header_Box_Message notification" id="shopping_success_empty" >
    <p>Cart is Empty</p>
  </div>`;
  box.innerHTML += notification;
  setTimeout(() => {
    document.getElementById("shopping_success_empty").remove();
  }, 3000);
  cart_item_number.innerText = "0";

  localStorage.removeItem("cartItems");
  cart_is_empty.style.display = "flex";

  // window.location.reload();
};
