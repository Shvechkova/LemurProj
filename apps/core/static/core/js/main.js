const baseEndpoint = "http://127.0.0.1:8000";

function modal() {
  const modal_button = document.querySelectorAll(".open-modal");
  const modal_windows = document.querySelector(".modal");
  modal_button.forEach((element) => {
    element.addEventListener("click", () => {
      modal_windows.classList.add("modal-active");
      getClientName();
      //   postClientName();
    });
  });
}
modal();

function getClientName() {
  fetch("/service/bill/client_list/", {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      let selectHTML = "";
      data.forEach(function (value, key) {
        selectHTML += `<option value="${value.client_name}">${value.client_name}</option>`;
      });
    
    });

    document.querySelector(".modal-bill_client").innerHTML = selectHTML;

    let select = document.querySelector(".modal-bill_client");
    select.addEventListener("change", () => {
      console.log(select.value);
    });
    fetch("/service/bill/client_list_contract/", {
        method: "get",
      })
        .then((response) => response.json())
        .then((data) => {
          let selectHTML = "";
          data.forEach(function (value, key) {
            selectHTML += `<option value="${value.client_name}">${value.client_name}</option>`;
          });
        
        });
    
    
}

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
