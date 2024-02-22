const addOperationOutPeople = document.querySelectorAll(
  ".suborder_out_operation_people"
);

if (addOperationOutPeople) {
  addOperationOutPeople.forEach((element) => {
    element.addEventListener("click", () => {
      let elem = element.getAttribute("data-name");

      const add_operation = document.querySelector(".operation_add_out_other");
      modal(elem, add_operation);
      const historySuborder = document.querySelector(".history_suborder");
      historySuborder.innerHTML = "";
      const operPrev = document.querySelector(".previous_operation_out_other");
      operPrev.innerHTML = "";
      const wrapOperOther = document.querySelector(".wrapper_oper_out_other");

      wrapOperOther.style.display = "none";

      FetchInfosubsPeople(element, elem);
      getInfoBillOperationOperOut(element);
      AddOperationOtherOut(element, elem);

      const chekinOtherSum = document.getElementById("other_sum_namber");
      chekinOtherSum.addEventListener("input", () => {
        const chekinOtherSum = document.getElementById("other_sum");

        chekinOtherSum.checked = true;
      });
      const nameElemOtherSum = "other_sum_namber_out_other";
      const nameRadioOtherSum = "other_sum_out_other";
      ChekinOtherSum(nameElemOtherSum, nameRadioOtherSum);
    });
  });
}

function FetchInfosubsPeople(element, elem) {
  let idBill = element.getAttribute("data-bill-month-id");
  const endpoint = "/service/api/subcontract/" + idBill + "/subcontract_li/";
  //   let operationIdvalue = element.getAttribute("data-id-sub");
  //   const idOperationrepl = operationIdvalue.replace(
  //     /^\D+|[^\d-]+|-(?=\D+)|\D+$/gim,
  //     ""
  //   );
  //   let data = new FormData();
  //   let object = {
  //     id: idOperationrepl,
  //   };
  //   const dataJson = JSON.stringify(object);

  fetch(endpoint, {
    method: "GET",

    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      let endpoint = "/service/api/subcontract-category-other/";

      fetch(endpoint, {
        method: "get",
      })
        .then((response) => response.json())
        .then((dataCategoryPeople) => {
          i = 0;
          data.forEach((item) => {
            if (item.other != null) {
              i++;
            }
          });

          if (i > 1) {
            data.forEach((item) => {
              if (item.other != null) {
                idCat = item.other;
                let nameCat = "";
                dataCategoryPeople.forEach((item) => {
                  if (item.id == idCat) {
                    nameCat = item.name;
                  }
                });

                const historySuborderWrap =
                  document.querySelector(".history_suborder");

                let historySuborderItem = document.createElement("div");
                historySuborderItem.className = "historySuborder_item";
                historySuborderWrap.append(historySuborderItem);

                let historySuborderName = document.createElement("p");
                historySuborderName.className = "history_suborder_name";
                historySuborderItem.append(historySuborderName);
                historySuborderName.innerHTML = nameCat;

                let historySuborderAmount = document.createElement("p");
                historySuborderAmount.className = "history_suborder_amount";
                historySuborderItem.append(historySuborderAmount);
                historySuborderAmount.innerHTML = item.amount;

                let historySuborderBtn = document.createElement("button");
                historySuborderBtn.className = "previous_operation_del";
                historySuborderItem.append(historySuborderBtn);
                // idCat = item.other;
                // idSubcontr = item.id;
                // otherAmount = item.amount;
                // monthBill = item.month_bill;
                historySuborderBtn.setAttribute("data-id-cat", item.other);
                historySuborderBtn.setAttribute("data-id-subcontr", item.id);
                historySuborderBtn.setAttribute("data-id-amount", item.amount);
                historySuborderBtn.setAttribute(
                  "data-id-month-bill",
                  item.month_bill
                );
                historySuborderBtn.setAttribute("data-name-cat", nameCat);
                historySuborderBtn.innerHTML = "оплатить";
              }
            });
            const btnPaySubs = document.querySelectorAll(
              ".previous_operation_del"
            );

            btnPaySubs.forEach((item) => {
              item.addEventListener("click", () => {
                dataEmpty = [];
                CreateSubcontractOtherOne(
                  dataEmpty,
                  dataCategoryPeople,
                  element,
                  item
                );
              });
            });
          } else {
            CreateSubcontractOtherOne(data, dataCategoryPeople, element);
          }
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
    ".operation_entry_client-name_out_other"
  );
  const modalContract = document.querySelector(
    ".operation_entry_contract-name_out_other"
  );
  const modalData = document.querySelector(".operation_entry_data_out_other");

  const modalNameSuborder = document.querySelector(
    ".name_suborder_modal_out_other"
  );
  const modalSumCtr = document.querySelector(
    ".sum_operation_suborders_outs_other"
  );
  const modalsunordrt_operation_all = document.querySelector(
    ".sum_operation_suborders_all_other"
  );

  modalClient.innerHTML = clientName;
  modalContract.innerHTML = contractName;
  modalData.innerHTML = contractData;

  modalNameSuborder.innerHTML = nameSumorder;
  modalSumCtr.innerHTML = allMonthSum;
  modalsunordrt_operation_all.innerHTML = 0;
}

function CreateSubcontractOtherOne(data, dataCategoryPeople, element, item) {
  const historySuborderWrap = document.querySelector(".history_suborder");
  historySuborderWrap.innerHTML = ""
  let idCat;
  let idSubcontr;
  let otherAmount;
  let monthBill;
  let nameCat = "";
  if (data.length == 0) {
    idCat = item.getAttribute("data-id-cat");
    idSubcontr = item.getAttribute("data-id-subcontr");
    otherAmount = item.getAttribute("data-id-amount");
    monthBill = item.getAttribute("data-id-month-bill");
    nameCat = item.getAttribute("data-name-cat");
  } else {
    console.log(2);
    data.forEach((item) => {
      if (item.other != null) {
        idCat = item.other;
        idSubcontr = item.id;
        otherAmount = item.amount;
        monthBill = item.month_bill;
      }
    });

    dataCategoryPeople.forEach((item) => {
      if (item.id == idCat) {
        nameCat = item.name;
      }
    });
  }

  const wrapOperOther = document.querySelector(".wrapper_oper_out_other");

  wrapOperOther.style.display = "block";
  const modalNameSuborder = document.querySelector(
    ".name_suborder_modal_out_other"
  );
  modalNameSuborder.innerHTML = "Премия " + nameCat;
  wrapOperOther.setAttribute("data-id-sub-other", idSubcontr);
  wrapOperOther.setAttribute("data-id-sub-amount-id", otherAmount);
  wrapOperOther.setAttribute("data-bill-month-id", monthBill);
  NewOperationOutOther(element);
}

function AddOperationOtherOut(element, elem) {
  const btnAddOperationOut = document.querySelector(".operation_add_out_other");
  const wrapOperOther = document.querySelector(".wrapper_oper_out_other");

  btnAddOperationOut.addEventListener("click", () => {
    const allMonthSum = wrapOperOther.getAttribute("data-id-sub-amount-id");
    const billId = wrapOperOther.getAttribute("data-id-sub-other");
    const billMonthId = wrapOperOther.getAttribute("data-bill-month-id");

    let bankChecked;
    const bankElement = document.querySelectorAll(
      '#bank_cheked_out_other input[name="bank"]'
    );
    bankElement.forEach((el) => {
      if (el.checked) {
        bankChecked = el.value;
      }
    });
    let sumChecked;
    const sumChekedInp = document.getElementById("sum_cheked_out_other");
    const stepCheked = sumChekedInp.getAttribute("data-step");

    const sumElement = document.querySelectorAll(
      '#sum_cheked_out_other input[name="sum"]'
    );

    let intMonthSum = parseInt(allMonthSum);

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
              "#other_sum_namber_out_other"
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
      "operation_comment_out_other"
    ).value;

    const form = new FormData();
    form.append("amount", sumChecked);
    form.append("comment", commentOperation);
    form.append("bank", bankChecked);
    form.append("suborder", billId);
    form.append("monthly_bill", billMonthId);
    form.append("type_operation", "out");
    let object = {};
    form.forEach((value, key) => (object[key] = value));
    const dataJson = JSON.stringify(object);
    console.log(dataJson);
    let csrfToken = getCookie("csrftoken");
    const endpoint = "/operations/api/operation/";
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

function NewOperationOutOther(element) {
  const wrapOperOther = document.querySelector(".wrapper_oper_out_other");
  let operationAllSum = wrapOperOther.getAttribute("data-id-sub-amount-id");

  let operationIdvalue = wrapOperOther.getAttribute("data-id-sub-other");
  let st = parseInt(operationAllSum);
  let sum_all = parseInt(operationAllSum);

  if (operationIdvalue !== "") {
    let data = new FormData();
    let object = {
      id: operationIdvalue,
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
            ".previous_operation_out_other"
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

          DelOperationOutOther(element);
          sumOperationEnded = st;

          const sumExpected = document.querySelector(
            ".sum_operation_suborders_all"
          );
          sumExpected.innerHTML = sum_all - sumOperationEnded;
          const sumChekedWrap = document.getElementById("sum_cheked_out_other");
          sumChekedWrap.setAttribute("data-step", "2");
          sumChekedWrap.innerHTML =
            '<p>Сколько оплатили?</p><input checked type="radio" id="100_out_other" name="sum" value="' +
            sumOperationEnded +
            '" /><label for="100_out_other">Остаток</label><input type="radio" id="other_sum_out_other" name="sum" value="1" /><label for="other_sum_out_other">Другая сумма</label><input data-validate="0" type="number" id="other_sum_namber_out_other" name="" value="" />';

          const nameElemOtherSum = "other_sum_namber_out_other";
          const nameRadioOtherSum = "other_sum_out_other";
          ChekinOtherSum(nameElemOtherSum, nameRadioOtherSum);
        } else {
          const lastOperationWrap = document.querySelector(
            ".previous_operation_out_other"
          );
          lastOperationWrap.innerHTML = "";
          const sumChekedWrap = document.getElementById("sum_cheked_out_other");
          sumChekedWrap.setAttribute("data-step", "1");
          sumChekedWrap.innerHTML =
            '<p>Сколько оплатили?</p><input  type="radio" id="100_out_other" name="sum" value="100" /><label for="100_out_other">100%</label><input type="radio" id="50_out_other" name="sum" value="50" /><label for="50_out_other">50%</label><input type="radio" id="other_sum_out_other" name="sum" value="1" /><label for="other_sum_out_other">Другая сумма</label><input data-validate="0"  type="number" id="other_sum_namber_out_other" name="" value="" />';

          const nameElemOtherSum = "other_sum_namber_out_other";
          const nameRadioOtherSum = "other_sum_out_other";
          ChekinOtherSum(nameElemOtherSum, nameRadioOtherSum);
        }

        // });
      });
  }
}

function DelOperationOutOther(element) {
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
          const add_operation = document.querySelector(
            ".operation_add_out_other "
          );
          add_operation.replaceWith(add_operation.cloneNode(true));
          element.click();

          return;
        }
      });
    });
  });
}
