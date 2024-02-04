
function modal(elem) {
  const modal_windows = document.getElementById(elem);
  modal_windows.classList.add("modal-active");
  // const modal_button = document.querySelectorAll(".open-modal");
  // const modal_windows = document.querySelector(".modal");
  // modal_button.forEach((element) => {
  //   element.addEventListener("click", () => {
  //     modal_windows.classList.add("modal-active");
     
  //   });
  // });
  let modalClose = document.querySelector(".modal_close");
  modalClose.addEventListener("click", (event) => {
    modal_windows.classList.remove("modal-active");
   console.log(123)
  });
}
// modal();

function addMonthBill() {
  function getClientName() {
    fetch("/service/bill/client_list/", {
      method: "get",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        let selectHTML = "";
        data.forEach(function (value, key) {
          selectHTML += `<option class="modal-bill_client-select" data-id-client="${value.id}"  value="${value.client_name}">${value.client_name}</option>`;
        });
        document.querySelector(".modal-bill_client").innerHTML = selectHTML;
      });
  }
  function fillValues() {
    let select = document.querySelector(".modal-bill_client");
    const service = document.querySelector(".modal-bill_service").value;
    select.addEventListener("change", () => {
      let date = new Date();
      year = date.getFullYear();
      let last_number_year = year.toString().slice(-2);
      let month_all = date.getMonth();
      var month = new Array();
      month[0] = "Январь";
      month[1] = "Февраль";
      month[2] = "Март";
      month[3] = "Апрель";
      month[4] = "Май";
      month[5] = "Июнь";
      month[6] = "Июль";
      month[7] = "Август";
      month[8] = "Сентябрь";
      month[9] = "Октябрь";
      month[10] = "Ноябрь";
      month[11] = "Декабрь";
      var result = month[date.getMonth()];
      let name_bill = document.querySelector(".modal-bill_contract");
      let month_bill = document.querySelector(".modal-bill_data");
      month_bill.value = result;

      name_bill.value = service + "/" + last_number_year + "-" + select.value;
    });
  }
  function addFormMonth() {
    const add_bill = document.querySelector(".bill_add");
    add_bill.addEventListener("click", () => {
      const client_elem = document.querySelector(".modal-bill_client");

      var client =
        client_elem.options[client_elem.selectedIndex].getAttribute(
          "data-id-client"
        );

      const service_elem = document.querySelector("[data-id-service]");
      const service = service_elem.dataset.idService;

      const contract_number = document.querySelector(
        ".modal-bill_contract"
      ).value;
      const contract_sum = document.querySelector(".modal-bill_sum-all").value;
      const adv_all_sum = document.querySelector(
        ".modal-bill_sum-mentor"
      ).value;

      let form = new FormData();

      form.append("client", +client);
      form.append("service", +service);
      form.append("contract_number", contract_number);
      form.append("contract_sum", contract_sum);
      form.append("adv_all_sum", adv_all_sum);

      fetch("/service/create-contract/", {
        // fetch("/service/bill/add_contract/", {
        method: "POST",
        body: form,
      })
        .then((response) => response.json())
        .then((response) => {});
    });
  }
  getClientName();
  fillValues();
  addFormMonth();
}

function addContentSelect(instance,select,select_inner){
  fetch(instance, {
          method: "get",
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            let selectHTML = "";
            data.forEach(function (value, key) {
              selectHTML += `<option class="modal-select" data-id="${value.id}"  value="${value.last_name}">${value.last_name}</option>`;
            });
            select.innerHTML = selectHTML;
          });
}


function getCookie(name) {
  let matches = document.cookie.match(
    new RegExp(
      "(?:^|; )" +
      name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
      "=([^;]*)"
    )
  );
  return matches ? decodeURIComponent(matches[1]) : undefined;
}


function openLoginModal() {
  // открытие модалки
  const modalLogin = document.getElementById("modal-login");
  const modalBack = document.querySelector(".modal-section");
  modalBack.classList.add("modal-section--active");
  document.body.style.overflow = "hidden";
  const timerId = setTimeout(() => {
    modalLogin.classList.add("modal--active");
  }, 200);
  // закрытие модалки
  let modalCloseLogin = document.querySelector(".modal-content__close__login");
  modalCloseLogin.addEventListener("click", (event) => {
    modalLogin.classList.remove("modal--active");
    modalBack.classList.remove("modal-section--active");
    document.body.style.overflow = "";
  });
  //закрытие по общему контейнеру
  let modalWrapperLogin = document.querySelector(".modal-wrapper-login");
  let modalContentWrapperLogin = document.querySelector(
    ".modal-content-wrap-login"
  );
  let modalContentLogin = document.querySelector(".modal-content-login");
  modalWrapperLogin.addEventListener("click", (event) => {
    if (event.target == modalContentLogin || !modalContentWrapperLogin) {
      modalLogin.classList.remove("modal--active");
      modalBack.classList.remove("modal-section--active");
      document.body.style.overflow = "";
    }
  });
}