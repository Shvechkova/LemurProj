choiceColor();

const addOperationEntry = document.querySelectorAll(".add-operation-entry");

if (addOperationEntry) {
  addOperationEntry.forEach((element) => {
    element.addEventListener("click", () => {
      document.getElementById('date-operation').valueAsDate = new Date();
      const lastOperationWrap = document.querySelector(".previous_operation");
      lastOperationWrap.innerHTML = "";

      let elem = element.getAttribute("data-name");
      let operationIdvalue = element.getAttribute(
        "data-bill-month-operation-entry"
      );

      const add_operation = document.querySelector(".operation_add");
      modal(elem, add_operation);
      const sumChek = document.querySelector("#sum_cheked");
      console.log(sumChek);
      sumChek.setAttribute("data-step", "1");
      // const prevoperationWrap = document.querySelector('.previous_operation')
      // var ndList = prevoperationWrap.childNodes;
      // console.log(ndList)

      const chekinOtherSum = document.getElementById("other_sum_namber");
      chekinOtherSum.addEventListener("input", () => {
        const chekinOtherSum = document.getElementById("other_sum");

        chekinOtherSum.checked = true;
      });
      newOperationEntry(element, elem);
      // const modalWindows = document.getElementById(elem);
      // modalWindows.addEventListener("input", () => {
      //   validate(elem, ".operation_add");
      // });
      getInfoBillOperation(element);
      const endpointOperation = "/operations/api/operation/";
      addFetchOperationEntry(element, endpointOperation, elem);
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

function addFetchOperationEntry(element, endpoint, elem) {
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
    const sumChekedInp = document.getElementById("sum_cheked");
    const stepCheked = sum_cheked.getAttribute("data-step");

    const sumElement = document.querySelectorAll(
      '#sum_cheked input[name="sum"]'
    );

    let intMonthSum = allMonthSum.replace(/[^0-9]/g, "");
    if (stepCheked == "1") {
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
    } else if (stepCheked == "2") {
      sumElement.forEach((el) => {
        if (el.checked) {
          if (el.value > "1") {
            sumChecked = +el.value;

            return;
          } else {
            const otherSumCheck = document.querySelector("#other_sum_namber");
            sumChecked = +otherSumCheck.value;
            return;
          }
        }
      });
    }

    const commentOperation = document.getElementById("operation_comment").value;
    const data_select = document.getElementById('date-operation').value
    const form = new FormData();
    form.append("amount", sumChecked);
    form.append("comment", commentOperation);
    form.append("bank", bankChecked);
    form.append("monthly_bill", billId);
    form.append("type_operation", "entry");
    form.append("data", data_select);

    let object = {};
    form.forEach((value, key) => (object[key] = value));
    const dataJson = JSON.stringify(object);

    let csrfToken = getCookie("csrftoken");

    fetch(endpoint, {
      method: "POST",
      body: dataJson,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    }).then((response) => {
      if (response.ok) {
        const windowContent = document.getElementById(elem);
        alertSuccess(windowContent);
        const timerId = setTimeout(() => {
          location.reload();
        }, 200);
      } else {
        const windowContent = document.getElementById(elem);

        alertError(windowContent);
        const timerId = setTimeout(() => {
          location.reload();
        }, 200);
      }
    });
  });
}

function newOperationEntry(element, elem) {
  let operationIdvalue = element.getAttribute(
    "data-bill-month-operation-entry"
  );
  let operationAllSum = element.getAttribute(
    "data-bill-month-sum-dont-operation"
  );

  const idOperationrepl = operationIdvalue.replace(
    /^\D+|[^\d-]+|-(?=\D+)|\D+$/gim,
    ""
  );

  const idOperation = idOperationrepl.split("-");
  console.log(idOperationrepl);

  if (idOperationrepl !== "") {
    console.log(idOperationrepl);
    const sumcheked = document.querySelector(".sum_cheked");

    let data = new FormData();
    let object = [];
    idOperation.forEach((item) => {
      const Obj = {
        id: item,
      };
      object.push(Obj);
    });

    let st = parseInt(operationAllSum.replace(/\s+/g, ""), 10);
    let sumOperationEnded = "";
    const dataJson = JSON.stringify(object);

    let csrfToken = getCookie("csrftoken");
    fetch("/operations/api/operation/operation_entry_list/", {
      method: "POST",
      body: dataJson,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const lastOperationWrap = document.querySelector(".previous_operation");
        lastOperationWrap.innerHTML = "";

        data.forEach((item) => {
          console.log(item);
          var options = {
            day: "numeric",
            month: "long",
            year: "numeric",
          };
          var d = new Date(item[0].created_timestamp);
          const sumoperation = item[0].amount;
          let dataOperation = d.toLocaleString("ru", options);

          let prevOperationItem = document.createElement("div");
          prevOperationItem.className = "previous_operation_item";
          lastOperationWrap.append(prevOperationItem);

          let prevOperationDel = document.createElement("button");
          prevOperationDel.className = "previous_operation_del";

          prevOperationItem.append(prevOperationDel);
          prevOperationDel.setAttribute("data-id-peration", item[0].id);
          prevOperationDel.innerHTML = "-";

          let prevOperationTitle = document.createElement("div");
          prevOperationTitle.className = "previous_operation_title";
          prevOperationItem.append(prevOperationTitle);
          prevOperationTitle.innerHTML =
            dataOperation +
            " - оплата " +
            sumoperation +
            "₽ из " +
            operationAllSum +
            " ₽";

          let comment = item[0].comment;

          let prevOperationComm = document.createElement("div");
          prevOperationComm.className = "previous_operation_comment";
          prevOperationItem.append(prevOperationComm);
          if (comment != "") {
            prevOperationComm.innerHTML = "Комментарий: " + comment;
          }
          st -= +sumoperation;
        });
        DelOperation(element);
        sumOperationEnded = st;
        const sumExpected = document.querySelector(".operation_entry_sum_all");
        sumExpected.innerHTML = sumOperationEnded;
        const sumChekedWrap = document.getElementById("sum_cheked");
        sumChekedWrap.setAttribute("data-step", "2");
        sumChekedWrap.innerHTML =
          '<p>Сколько оплатили?</p><input checked type="radio" id="100" name="sum" value="' +
          sumOperationEnded +
          '" /><label for="100">Остаток</label><input type="radio" id="other_sum" name="sum" value="1" /><label for="other_sum">Другая сумма</label><input data-validate="0" type="number" id="other_sum_namber" name="" value="" />';

        const chekinOtherSum = document.getElementById("other_sum_namber");
        chekinOtherSum.addEventListener("input", () => {
          const chekinOtherSum = document.getElementById("other_sum");

          chekinOtherSum.checked = true;
          return
        });
      });
  } else {
    const sumChekedWrap = document.getElementById("sum_cheked");
    sumChekedWrap.setAttribute("data-step", "1");
    sumChekedWrap.innerHTML =
      ' <p>Сколько оплатили?</p><input  type="radio" id="100" name="sum" value="100" /><label for="100">100%</label><input type="radio" id="50" name="sum" value="50" /><label for="50">50%</label><input type="radio" id="other_sum" name="sum" value="1" /><label for="other_sum">Другая сумма</label><input data-validate="0"  type="number" id="other_sum_namber" name="" value="" />';

    const chekinOtherSum = document.getElementById("other_sum_namber");
    chekinOtherSum.addEventListener("input", () => {
      const chekinOtherSum = document.getElementById("other_sum");

      chekinOtherSum.checked = true;
     
    });
  }

  return idOperationrepl;
}

function DelOperation(element) {
  const delButton = document.querySelectorAll(".previous_operation_del");
  delButton.forEach((item) => {
    item.addEventListener("click", () => {
      idOperation = item.getAttribute("data-id-peration");
      console.log(idOperation);
      endpoint = "/operations/api/operation/" + idOperation + "/";

      item.parentElement.remove();

      fetch(endpoint, {
        method: "DELETE",
        // body: dataJson,
        headers: {
          "Content-Type": "application/json",
          // "X-CSRFToken": csrfToken,
        },
      }).then((response) => {
        if (response.ok) {
          // location.reload();
          console.log(element);
          //  element.click()
          let operationIdvalue = element.getAttribute(
            "data-bill-month-operation-entry"
          );

          const idOperationrepl = operationIdvalue.replace(
            /^\D+|[^\d-]+|-(?=\D+)|\D+$/gim,
            ""
          );

          const idOperat = idOperationrepl.split("-");
          console.log(idOperation);
          let newidoper = "";
          idOperat.forEach((item) => {
            if (item != idOperation) {
              newidoper += item + "-";
            }
          });

          element.setAttribute("data-bill-month-operation-entry", newidoper);
          console.log("pppp");
          console.log(element.getAttribute("data-bill-month-operation-entry"));
          const add_operation = document.querySelector(".operation_add");
          add_operation.replaceWith(add_operation.cloneNode(true));
          element.click();
          
          return
        }
      });
    });
  });
}
