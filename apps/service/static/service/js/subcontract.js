choiceColor();

const btnSubcontarct = document.querySelectorAll(".add_sabcontactor");

if (btnSubcontarct) {
  btnSubcontarct.forEach((element) => {
    element.addEventListener("click", () => {
      let elem = element.getAttribute("data-name");
      let idBill = element.getAttribute("data-bill-month-id");

      modal(elem);
      getInfoBill(element);
      createInputSubcontract()
    });
  });
}

function getInfoBill(element) {
  const clientName = element.getAttribute("data-bill-month-client-name");
  const contractName = element.getAttribute("data-bill-month-name");
  const contractData = element.getAttribute("data-bill-month-data");
  const advMonthSum = element.getAttribute("data-bill-month-adv");

  const modalClient = document.querySelector(".add-subcontract_client-name");
  const modalContract = document.querySelector(
    ".add-subcontract_contract-name"
  );
  const modalData = document.querySelector(".add-subcontract_data");

  modalClient.innerHTML = clientName;
  modalContract.innerHTML = contractName;
  modalData.innerHTML = contractData;
}

function createInputSubcontract() {
  console.log(2)
    // const contractWrapper = document.getElementById("modal_contract_wrapper");
    // let divWrapper = document.createElement("div");
    // divWrapper.className = "modal_add_contract";
    // contractWrapper.append(divWrapper);
    choiceColor();
    const subTypeSelect = document.querySelectorAll(".modal-subcontract-type")
    subTypeSelect.forEach((el) =>{
      el.addEventListener("change",()=>{
        console.log(4)
      })
    })
  
    // let select = document.createElement("select");
    // select.className = "modal-subcontract-type choice";
    // divWrapper.append(select);
    // addService(select);

    // new Input(
    //   "text",
    //   "modal-client_contract-input input-200",
    //   "",
    //   "Номер договора"
    // ).appendTo(divWrapper);
    // new Input(
    //   "date",
    //   "modal-client_contract-input input-130",
    //   "",
    //   "Подписан"
    // ).appendTo(divWrapper);
    // new Input(
    //   "number",
    //   "modal-client_contract-input input-130",
    //   "",
    //   "Сумма"
    // ).appendTo(divWrapper);
    // new Input("hidden", " 1").appendTo(divWrapper);
  
    // let button = document.createElement("button");
    // button.className = "modal_add_contract_btn";
    // button.innerHTML = "OK";
    // divWrapper.append(button);
    // choiceColor();
  
    // button.addEventListener("click", () => {
    //   button.remove();
    //   createInputContract();
    // });
  }


// function addSubcontarctT(selectInput, selected,instanse) {
//   const select = selectInput;
//   new selectOption("modal-select", "0", "", "Услуга").appendTo(select);
//   const instance = "/service/api/service_category/";

//   fetch(instance, {
//     method: "get",
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       data.forEach(function (value, key) {
//         new selectOption(
//           "modal-select input-130",
//           value.id,
//           value.id,
//           value.name,
//           selected
//         ).appendTo(select);
//       });
//     });
// }