PREFIX_NEWS1 = "news1_";

const emailChange = (event, email) => {
  localStorage.setItem(PREFIX_NEWS1 + "email", email.value);
};

const collectEmail = () => {
  let email = document.querySelector('input[type="email"]');
  if (email !== null) {
    // console.dir(email);
    localStorage.setItem(PREFIX_NEWS1 + "email", "");
    email.addEventListener("change", (event) => emailChange(event, email));
  }
};

const checkbox_change = (event, checkboxElement, type_label) => {
  //   console.dir(checkboxElement);
  let news_type = localStorage.getItem(PREFIX_NEWS1 + "news_type");
  if (news_type === null) {
    news_type = "";
  }
  news_type = news_type.replace(type_label, "");

  if (checkboxElement.checked) {
    news_type += type_label;
  }
  localStorage.setItem(PREFIX_NEWS1 + "news_type", news_type);
};

const radio_change = (event) => {
  localStorage.setItem(PREFIX_NEWS1 + "days_in_week", event.target.value);
};

const phone_change = (event) => {
  localStorage.setItem(PREFIX_NEWS1 + "phone", event.target.value);
};
const show_error = (error) => {
  console.warn(error);
};
const get_my_headlines = (event) => {
  let headers = {
    "Content-Type": "application/json",
  };
  //   headers["Authorization"] =
  //     "Bearer " + localStorage.getItem(TOKEN_ACCESS_ITEM_NAME);
  let request = {
    method: "post",

    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: headers,
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  let currentDate = new Date();
  let utc_now_int = Math.floor(currentDate.getTime() / 1000);
  request["body"] = JSON.stringify({
    email: localStorage.getItem(PREFIX_NEWS1 + "email"),
    news_type: localStorage.getItem(PREFIX_NEWS1 + "news_type"),
    days_in_week: localStorage.getItem(PREFIX_NEWS1 + "days_in_week"),
    phone: localStorage.getItem(PREFIX_NEWS1 + "phone"),
  });
  fetch("https://myheadlines.pro/news/api/client/add/", request)
    .then((response) => {
      if (response.status == 201) {
        response
          .json()
          .then((response_json) => {
            console.log(response_json[0]);
            // ok
            localStorage.setItem(
              PREFIX_NEWS1 + "clients_id",
              response_json[0]["clients_id"]
            );
          })
          .catch((error) => show_error(error));
      } else if (response.status == 400) {
        // get error text
        response
          .json()
          .then((response_json) => {
            console.log(response_json);
            //   throw new Error(response_json[0]);
          })
          .catch((error) => show_error(error));
      } else {
        throw new Error(`Status code ${response.status} received`);
      }
    })
    .catch((error) => show_error(error));
};

const collectInterests = () => {
  let itemw = document.getElementById("World-News");
  if (itemw !== null) {
    localStorage.setItem(PREFIX_NEWS1 + "news_type", "");
    localStorage.setItem(PREFIX_NEWS1 + "days_in_week", "");
    localStorage.setItem(PREFIX_NEWS1 + "phone", "");
    itemw.addEventListener("change", (event) =>
      checkbox_change(event, itemw, "w")
    );
    let itemt = document.getElementById("Tech-Innovation");
    itemt.addEventListener("change", (event) =>
      checkbox_change(event, itemt, "t")
    );
    let itemb = document.getElementById("Business-Finance");
    itemb.addEventListener("change", (event) =>
      checkbox_change(event, itemb, "b")
    );
    let items = document.getElementById("Science-Discovery");
    items.addEventListener("change", (event) =>
      checkbox_change(event, items, "s")
    );
    let itemh = document.getElementById("Health-Wellness");
    itemh.addEventListener("change", (event) =>
      checkbox_change(event, itemh, "h")
    );
    itemp = document.getElementById("Sports");
    itemp.addEventListener("change", (event) =>
      checkbox_change(event, itemp, "p")
    );
    let itemo = document.getElementById("Politics-Government");
    itemo.addEventListener("change", (event) =>
      checkbox_change(event, itemo, "o")
    );
    let iteme = document.getElementById("Environment-Sustainability");
    iteme.addEventListener("change", (event) =>
      checkbox_change(event, iteme, "e")
    );
    let itemn = document.getElementById("Entertainment-Culture");
    itemn.addEventListener("change", (event) =>
      checkbox_change(event, itemn, "n")
    );
    itemf = document.getElementById("Food-Lifestyle");
    itemf.addEventListener("change", (event) =>
      checkbox_change(event, itemf, "f")
    );
    let itema = document.getElementById("Art-Fashion");
    itema.addEventListener("change", (event) =>
      checkbox_change(event, itema, "a")
    );
    let radio_list = document.querySelectorAll('input[type="radio"]');
    radio_list.forEach((radio_item) => {
      radio_item.addEventListener("change", (event) => radio_change(event));
    });
    let phone = document.getElementById("phone-number");
    phone.addEventListener("change", (event) => phone_change(event));
    let btn_get_my_headlines = document.getElementById("btn-get-my-headlines");
    btn_get_my_headlines.addEventListener("click", (event) =>
      get_my_headlines(event)
    );
  }
};

document.addEventListener("DOMContentLoaded", () => {
  pageURL = window.location.href.toLowerCase();
  collectEmail();
  collectInterests();
});
