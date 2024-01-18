const first_name = document.getElementById("first_name");
const last_name = document.getElementById("last_name");
const email = document.getElementById("email");
const location_input = document.getElementById("location_input");
const phonenumber = document.getElementById("phonenumber");
const zipcode = document.getElementById("zipcode");
const coupon = document.getElementById("coupon");
const total_cart_items = document.getElementById("total_cart_items");
const location_price = document.getElementById("location_price");
let box = document.getElementById("notification_box");
const final_order_submit_button = document.getElementById(
  "final_order_submit_button"
);
const coupon_field = document.getElementById("coupon_field");
const fill_form_correctly = document.getElementById("fill_form_correctly");
const coupon_code_percent = document.getElementById("coupon_code_percent");
const coupon_price_div = document.getElementById("coupon_price_div");
const wrong_coupon_div = document.getElementById("wrong_coupon_div");
const coupon_percent = document.getElementById("coupon_percent");
const apply_coupon_code = document.getElementById("apply_coupon_code");

let cart_t = [];
let cart_items = [];

if (JSON.parse(localStorage.getItem("cartItems") !== null)) {
  cart_items = JSON.parse(localStorage.getItem("cartItems"));
  document.getElementById("total_cart_items").value = cart_items.length;
} else {
  document.getElementById("total_cart_items").value = 1;
}

const sub_total_price = document.getElementById("sub_total_price");
const total_price = document.getElementById("total_price");
let grandTotalOfAllItems = 0;

const params = new URLSearchParams(window.location.search);
const url_quan = params.get("quantity");
const url_prod_id = params.get("product_id");
const url_price = params.get("price");
console.log(url_price);

if (url_quan == null || url_prod_id == null || url_price == null) {
  for (let i = 0; i < cart_items.length; i++) {
    cart_t.push({
      product_id: cart_items[i].productId,
      quantity: cart_items[i].quantity,
    });

    //     const data = `<div><input name="product_id_${i + 1}" value=${
    //       cart_items[i].productId
    //     } />
    //   <input name="quantity_id_${i + 1}" value=${cart_items[i].quantity} />

    //     </div>`;
    //     document.getElementById("add_items_from_localstorage").innerHTML += data;
  }

  if (cart_items.length === 0) {
  } else {
    for (let i = 0; i < cart_items.length; i++) {
      grandTotalOfAllItems +=
        cart_items[i].productPrice * cart_items[i].quantity;
    }
    sub_total_price.innerHTML = grandTotalOfAllItems;
    total_price.innerHTML = grandTotalOfAllItems;
  }
} else {
  cart_t.push({
    product_id: url_prod_id,
    quantity: parseInt(url_quan),
  });

  //   const data = `<div><input name="product_id_${1}" value=${params.get(
  //     "product_id"
  //   )} />
  // <input name="quantity_id_${1}" value=${params.get("quantity")} />

  //   </div>`;

  //   document.getElementById("add_items_from_localstorage").innerHTML += data;

  sub_total_price.innerHTML = params.get("price");
  total_price.innerHTML = params.get("price");
}

document.getElementById("select_location").addEventListener("change", (sel) => {
  const el = document.getElementById("select_location");
  const id = el.options[el.selectedIndex].value;
  let abc = el.options[el.selectedIndex].text.split("-");
  if (abc.length == 2) {
    document.getElementById("delivery_price").innerHTML = abc[1];
    document.getElementById("total_price").innerHTML =
      parseFloat(document.getElementById("sub_total_price").innerText) -
      parseFloat(
        (parseFloat(
          coupon_code_percent.value == "" ? 0 : coupon_code_percent.value
        ) /
          100) *
          parseFloat(document.getElementById("sub_total_price").innerText)
      ) +
      parseFloat(abc[1]);

    document.getElementById("location_input").value = id;
    document.getElementById("location_price").value = abc[1];
  } else {
    document.getElementById("delivery_price").innerHTML = 0.0;
    document.getElementById("total_price").innerHTML =
      parseFloat(document.getElementById("sub_total_price").innerText) -
      parseFloat(
        (parseFloat(
          coupon_code_percent.value == "" ? 0 : coupon_code_percent.value
        ) /
          100) *
          parseFloat(document.getElementById("sub_total_price").innerText)
      ) +
      0.0;
    document.getElementById("location_price").value = 0;
    // document.getElementById("total_price").innerHTML =
    //   parseFloat(document.getElementById("total_price").innerText) + 0.0;
  }
});

const app = () => {
  console.log("apps ");
};

const applyCouponCode = () => {
  apply_coupon_code.innerHTML = "Wait...";
  apply_coupon_code.disabled = true;

  axios
    .post(
      `${window.location.origin}/apply-coupon-code/`,
      {
        coupon: coupon_field.value,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
    .then((res) => {
      console.log(res.data[0].fields);
      coupon_price_div.style.display = "block";
      wrong_coupon_div.style.display = "none";

      coupon_percent.innerHTML = res.data[0].fields.discount;

      const sub_price = parseFloat(
        document.getElementById("sub_total_price").innerText
      );

      const dis_sub_price =
        (parseFloat(res.data[0].fields.discount) / 100) * sub_price;

      const total_price = document.getElementById("total_price");
      //   console.log(location_price.value);

      total_price.innerText =
        parseFloat(sub_price) -
        dis_sub_price +
        parseFloat(location_price.value);

      apply_coupon_code.disabled = false;
      apply_coupon_code.innerText = "Apply";

      coupon.value = res.data[0].fields.coupon_code;
      coupon_code_percent.value = res.data[0].fields.discount;
    })
    .catch((err) => {
      coupon_price_div.style.display = "none";
      wrong_coupon_div.style.display = "block";
      apply_coupon_code.innerHTML = "Apply";
      apply_coupon_code.disabled = false;
    });
};

const submitAjaxForm = () => {
  if (
    first_name.value.trim() == "" ||
    last_name.value.trim == "" ||
    email.value.trim == "" ||
    location_input.value.trim == "" ||
    zipcode.value.trim == "" ||
    total_cart_items == 0 ||
    cart_items.length == 0
  ) {
    validateForm();
    return;
  }

  final_order_submit_button.innerHTML = "Load...";
  final_order_submit_button.disabled = true;

  axios
    .post(
      `${window.location.origin}/billing_api/`,
      {
        first_name: first_name.value,
        last_name: last_name.value,
        email: email.value,
        location_input: location_input.value,
        phonenumber: phonenumber.value,
        zipcode: zipcode.value,
        total_cart_items: total_cart_items.value,
        coupon: coupon.value,
        cart_items: cart_t,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
    .then((res) => {
      if (url_price === null || url_prod_id === null || url_quan === null) {
        localStorage.removeItem("cartItems");
      }

      const success = `
        <div class="Header_Box_Message success" id="shopping_success" >
          <p>
          Order successfully placed.
          </p>
        </div>`;

      box.innerHTML += success;

      setTimeout(() => {
        document.getElementById("shopping_success").remove();
      }, 3000);

      //   window.location.reload();
      window.location.replace(`${window.location.origin}/success-page`);
    })
    .catch((err) => {
      console.log(err);
    });
};

const validateForm = () => {
  fill_form_correctly.style.display = "flex";
  final_order_submit_button.disabled = true;
  setTimeout(() => {
    fill_form_correctly.style.display = "none";
    final_order_submit_button.disabled = false;
  }, 4000);
};
