choiceColor();

const addOperationEntry = document.querySelectorAll(".add-operation-entry");

if (addOperationEntry) {
  addOperationEntry.forEach((element) => {
    element.addEventListener("click", () => {
   
      let elem = element.getAttribute("data-name");
   
      // const add_operation = document.querySelector(".operation_add");
      modal(elem);

      newOperationEntry(element);
      // const modalWindows = document.getElementById(elem);
      // modalWindows.addEventListener("input", () => {
      //   validate(elem);
      // });
      getInfoBillOperation(element);
      const endpointOperation = "/operations/api/entry/";
      addFetchOperationEntry(element, endpointOperation);
    });
  });
}

function getInfoBillOperation(element) {
  const clientName = element.getAttribute("data-bill-month-client-name");
  const contractName = element.getAttribute("data-bill-month-name");
  const contractData = element.getAttribute("data-bill-month-data");
  const allMonthSum = element.getAttribute(
    "data-bill-month-sum-dont-operation"
  );

  const modalClient = document.querySelector(".operation_entry_client-name");
  const modalContract = document.querySelector(
    ".operation_entry_contract-name"
  );
  const modalData = document.querySelector(".operation_entry_data");
  const modalSumcontract = document.querySelector(".operation_entry_sum_all");

  modalClient.innerHTML = clientName;
  modalContract.innerHTML = contractName;
  modalData.innerHTML = contractData;
  modalSumcontract.innerHTML = allMonthSum;
}

function addFetchOperationEntry(element, endpoint) {
  const btnAddOperationEntry = document.querySelector(".operation_add");
  const allMonthSum = element.getAttribute(
    "data-bill-month-sum-dont-operation"
  );
  const billId = element.getAttribute("data-bill-month-id");

  btnAddOperationEntry.addEventListener("click", () => {
    const allMonthSum = element.getAttribute(
      "data-bill-month-sum-dont-operation"
    );
    let bankChecked;
    const bankElement = document.querySelectorAll(
      '#bank_cheked input[name="bank"]'
    );
    bankElement.forEach((el) => {
      if (el.checked) {
        bankChecked = el.value;
      }
    });
    let sumChecked;
    const sumElement = document.querySelectorAll(
      '#sum_cheked input[name="sum"]'
    );

    let intMonthSum = allMonthSum.replace(/[^0-9]/g, "");

    sumElement.forEach((el) => {
      if (el.checked) {
        if (el.value == "100") {
          sumChecked = +intMonthSum;

          return;
        } else if (el.value == "50") {
          sumChecked = +intMonthSum / 2;
          return;
        } else {
          const otherSumCheck = document.querySelector("#other_sum_namber");
          sumChecked = +otherSumCheck.value;
          return;
        }
      }
    });

    const commentOperation = document.getElementById("operation_comment").value;

    const form = new FormData();
    form.append("amount", sumChecked);
    form.append("comment", commentOperation);
    form.append("bank", bankChecked);
    form.append("monthly_bill", billId);

    let object = {};
    form.forEach((value, key) => (object[key] = value));
    const dataJson = JSON.stringify(object);
    console.log(dataJson);
    let csrfToken = getCookie("csrftoken");

    fetch(endpoint, {
      method: "POST",
      body: dataJson,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      });
    // .then((response) => {
    //   if (response.ok) {
    //     const windowContent = document.getElementById(element);
    //     alertSuccess(windowContent);
    //     const timerId = setTimeout(() => {
    //       location.reload();
    //     }, 200);
    //   } else {
    //     const windowContent = document.getElementById(element);
    //     alertError(windowContent);
    //     const timerId = setTimeout(() => {
    //       location.reload();
    //     }, 200);
    //   }
    // });
  });
}

function newOperationEntry(element) {
  let operationIdvalue = element.getAttribute("data-bill-month-operation-entry")
  const idOperationrepl = operationIdvalue.replace(/^\D+|[^\d-]+|-(?=\D+)|\D+$/gim, '')
  const idOperation = idOperationrepl.split("-");
  let data = new FormData();
  let object = [];
  idOperation.forEach((item)=>{
    const Obj = {
      id: item
    }
    object.push(Obj);
  })
 console.log(object)


  const dataJson = JSON.stringify(object);

console.log(dataJson)
let csrfToken = getCookie("csrftoken");
  fetch('/operations/api/entry/contract_filter_list/', {
    method: "POST",
    body: dataJson,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}
