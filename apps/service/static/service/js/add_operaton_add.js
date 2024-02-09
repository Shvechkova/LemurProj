choiceColor();

const addOperationEntry = document.querySelectorAll(".add-operation-entry");

if (addOperationEntry) {
  addOperationEntry.forEach((element) => {
    element.addEventListener("click", () => {
      let elem = element.getAttribute("data-name");

      modal(elem);
      getInfoBillOperation(element);

      addFetchOperationEntry(element);
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

function addFetchOperationEntry(element) {
  const btnAddOperationEntry = document.querySelector(".operation_entry_add");
  const allMonthSum = element.getAttribute(
    "data-bill-month-sum-dont-operation"
  );

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
        }
        if (el.value == "50") {
          sumChecked = +intMonthSum / 2;
        } else {
          const otherSumCheck = document.querySelector("#other_sum_namber");
          sumChecked = +otherSumCheck.value;
        }
      }
    });

    const commentOperation =  document.querySelector("#operation_comment_entry")


    const data = new FormData();
    form.append("monthly_bill", client);
    form.append("bank", bankChecked);
    form.append("amount", sumChecked);
    form.append("comment", commentOperation.value);

  });
}

//
