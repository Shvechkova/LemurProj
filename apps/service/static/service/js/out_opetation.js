choiceColor();

const addOperationOut = document.querySelectorAll(".suborder_out_operation");

if (addOperationOut) {
  addOperationOut.forEach((element) => {
    element.addEventListener("click", () => {
      document.getElementById("date-operation_out").valueAsDate = new Date();
      const lastOperationWrap = document.querySelector(
        ".previous_operation_out"
      );
      lastOperationWrap.innerHTML = "";

      let elem = element.getAttribute("data-name");
      // let operationIdvalue = element.getAttribute(
      //   "data-bill-month-operation-entry"
      // );

      const add_operation = document.querySelector(".operation_add_out");
      modal(elem, add_operation);
      const nameElemOtherSum = "other_sum_namber_out";
      const nameRadioOtherSum = "other_sum_out";
      ChekinOtherSum(nameElemOtherSum, nameRadioOtherSum);

      getInfoBillOperationOperOut(element);

      const chekinOtherSum = document.getElementById("other_sum_namber");
      chekinOtherSum.addEventListener("input", () => {
        const chekinOtherSum = document.getElementById("other_sum");

        chekinOtherSum.checked = true;
      });
      newOperationOut(element, elem);
      const modalWindows = document.getElementById(elem);

      const endpointOperation = "/operations/api/operation/";
      addFetchOperationOut(element, endpointOperation, elem);
    });
  });
}

function getInfoBillOperationOperOut(element) {
  const clientName = element.getAttribute("data-bill-month-client-name");
  const contractName = element.getAttribute("data-bill-month-name");
  const contractData = element.getAttribute("data-bill-month-data");
  const allMonthSum = element.getAttribute("data-id-sub-amount");
  const nameSumorder = element.getAttribute("data-name-sub");

  const modalClient = document.querySelector(
    ".operation_entry_client-name_out"
  );
  const modalContract = document.querySelector(
    ".operation_entry_contract-name_out"
  );
  const modalData = document.querySelector(".operation_entry_data_out");

  const modalNameSuborder = document.querySelector(".name_suborder_modal_out");
  const modalSumCtr = document.querySelector(".sum_operation_suborders_outs");
  const modalsunordrt_operation_all = document.querySelector(
    ".sum_operation_suborders_all"
  );

  modalClient.innerHTML = clientName;
  modalContract.innerHTML = contractName;
  modalData.innerHTML = contractData;

  modalNameSuborder.innerHTML = nameSumorder;
  modalSumCtr.innerHTML = allMonthSum;
  modalsunordrt_operation_all.innerHTML = 0;
}

function addFetchOperationOut(element, endpoint, elem) {
  const btnAddOperationEntry = document.querySelector(".operation_add_out");
  // const allMonthSum = element.getAttribute(
  //   "name_suborder_modal"
  // );
  const billId = element.getAttribute("data-id-sub");
  const billMonthId = element.getAttribute("data-bill-month-id");

  btnAddOperationEntry.addEventListener("click", () => {
    const allMonthSum = element.getAttribute("data-id-sub-amount");
    let bankChecked;
    const bankElement = document.querySelectorAll(
      '#bank_cheked_out input[name="bank"]'
    );
    bankElement.forEach((el) => {
      if (el.checked) {
        bankChecked = el.value;
      }
    });
    let sumChecked;
    const sumChekedInp = document.getElementById("sum_cheked_out");
    const stepCheked = sumChekedInp.getAttribute("data-step");

    const sumElement = document.querySelectorAll(
      '#sum_cheked_out input[name="sum"]'
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
            const otherSumCheck = document.querySelector(
              "#other_sum_namber_out"
            );
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
            const otherSumCheck = document.querySelector(
              "#other_sum_namber_out"
            );
            sumChecked = +otherSumCheck.value;
            return;
          }
        }
      });
    }

    const commentOperation = document.getElementById(
      "operation_comment_out"
    ).value;
    const data_select = document.getElementById("date-operation_out").value;
    const form = new FormData();
    form.append("amount", sumChecked);
    form.append("comment", commentOperation);
    form.append("bank", bankChecked);
    form.append("suborder", billId);
    form.append("monthly_bill", billMonthId);
    form.append("type_operation", "out");
    form.append("data", data_select);

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
      // .then((response) => response.json())
      // .then((data) => {
      //   console.log(data);
      // });
      .then((response) => {
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

function newOperationOut(element, elem) {
  let operationIdvalue = element.getAttribute("data-id-sub");
  let operationAllSum = element.getAttribute("data-id-sub-amount");

  const idOperationrepl = operationIdvalue.replace(
    /^\D+|[^\d-]+|-(?=\D+)|\D+$/gim,
    ""
  );
  let st = parseInt(operationAllSum.replace(/\s+/g, ""), 10);
  let sum_all = parseInt(operationAllSum.replace(/\s+/g, ""), 10);
  console.log(idOperationrepl);
  if (idOperationrepl !== "") {
    let data = new FormData();
    let object = {
      id: idOperationrepl,
    };

    const dataJson = JSON.stringify(object);

    let csrfToken = getCookie("csrftoken");
    fetch("/operations/api/operation/operation_out_filter/", {
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
        if (data.length > 0) {
          const lastOperationWrap = document.querySelector(
            ".previous_operation_out"
          );
          lastOperationWrap.innerHTML = "";

          data.forEach((item) => {
            var options = {
              day: "numeric",
              month: "long",
              year: "numeric",
            };
            var d = new Date(item.created_timestamp);
            const sumoperation = item.amount;

            let dataOperation = d.toLocaleString("ru", options);
            let prevOperationItem = document.createElement("div");
            prevOperationItem.className = "previous_operation_item";
            lastOperationWrap.append(prevOperationItem);

            let prevOperationDel = document.createElement("button");
            prevOperationDel.className = "previous_operation_del";

            prevOperationItem.append(prevOperationDel);
            prevOperationDel.setAttribute("data-id-peration", item.id);
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

            let comment = item.comment;

            let prevOperationComm = document.createElement("div");
            prevOperationComm.className = "previous_operation_comment";
            prevOperationItem.append(prevOperationComm);
            if (comment != "") {
              prevOperationComm.innerHTML = "Комментарий: " + comment;
            }
            st -= +sumoperation;
          });

          DelOperationOut(element);
          sumOperationEnded = st;

          const sumExpected = document.querySelector(
            ".sum_operation_suborders_all"
          );
          sumExpected.innerHTML = sum_all - sumOperationEnded;
          const sumChekedWrap = document.getElementById("sum_cheked_out");
          sumChekedWrap.setAttribute("data-step", "2");
          sumChekedWrap.innerHTML =
            '<p>Сколько оплатили?</p><input checked type="radio" id="100_out" name="sum" value="' +
            sumOperationEnded +
            '" /><label for="100_out">Остаток</label><input type="radio" id="other_sum_out" name="sum" value="1" /><label for="other_sum_out"></label><input placeholder="Другая сумма" data-validate="0" type="number" id="other_sum_namber_out" name="" value="" />';

          const nameElemOtherSum = "other_sum_namber_out";
          const nameRadioOtherSum = "other_sum_out";
          ChekinOtherSum(nameElemOtherSum, nameRadioOtherSum);
        } else {
          const sumChekedWrap = document.getElementById("sum_cheked_out");
          sumChekedWrap.setAttribute("data-step", "1");
          sumChekedWrap.innerHTML =
            '<h3>Сколько оплатили?</h3><input  type="radio" id="100_out" name="sum" value="100" /><label for="100_out">100%</label><input type="radio" id="50_out" name="sum" value="50" /><label for="50_out">50%</label><input type="radio" id="other_sum_out" name="sum" value="1" /><label for="other_sum_out"></label><input placeholder="Другая сумма" data-validate="0"  type="number" id="other_sum_namber_out" name="" value="" />';

          const nameElemOtherSum = "other_sum_namber_out";
          const nameRadioOtherSum = "other_sum_out";
          ChekinOtherSum(nameElemOtherSum, nameRadioOtherSum);
        }

        // });
      });
  }

  return idOperationrepl;
}

function DelOperationOut(element) {
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
          const add_operation = document.querySelector(".operation_add_out");
          add_operation.replaceWith(add_operation.cloneNode(true));
          element.click();

          return;
        }
      });
    });
  });
}
