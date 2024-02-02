
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

// let select = document.querySelector(".modal-bill_client");
// select.addEventListener("change", () => {
//   console.log(select.value);
// });
// fetch("/service/bill/client_list_contract/", {
//     method: "get",
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       let selectHTML = "";
//       data.forEach(function (value, key) {
//         selectHTML += `<option value="${value.client_name}">${value.client_name}</option>`;
//       });

//     });

// function postClientName() {
//   let select = document.querySelector(".modal-bill_client");
//   select.addEventListener("change", () => {
//     const form = new FormData();
//     form.append("select", select);
//   });
//   console.log(form);
//   fetch("/service/bill/", {
//     method: "POST",
//   })
//     .then((response) => response.json())
//     .then((data) => {});
// }

// function addBill() {
// //   if (step == "stepOne") {
// //     // form.append("phone", telValueNum);
// //   }
// fetch("/service/bill/", {
//     method: "get",
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       let selectHTML = "";
//       data.forEach(function (value, key) {
//         console.log(value.client_name);
//         selectHTML += `<option value="${value.client_name}">${value.client_name}</option>`;
//       });
//       document.querySelector(".modal-bill_client").innerHTML = selectHTML;
//     });

// }

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
