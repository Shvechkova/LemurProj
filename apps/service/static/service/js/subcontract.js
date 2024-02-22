choiceColor();

const btnSubcontarct = document.querySelectorAll(".add_sabcontactor");

if (btnSubcontarct) {
  btnSubcontarct.forEach((element) => {
    element.addEventListener("click", () => {
      let elem = element.getAttribute("data-name");
      let idBill = element.getAttribute("data-bill-month-id");
      let sumAdv = element.getAttribute("data-bill-month-adv");

      let budgetInnerAll = document.querySelector(".modal_adv_budget_all");
      budgetInnerAll.innerHTML = sumAdv;

      const add_subc = document.querySelector(".subcontarct_add");
      modal(elem, add_subc);
      const c = document.querySelector(".modal_add_subcontract_wrapper");
      // c.innerHTML = ""
      c.innerHTML =
        '<div class="modal_add_contract modal_add-subcontract"><select class="modal-subcontract-type choice"><option disabled selected class="modal-select empty" value="0">Тип</option><option class="modal-select" value="adv">площадка</option><option class="modal-select" value="other">премия</option></select></div>';

      getOldSumcintract(idBill, element);
      getInfoBill(element);
      createInputSubcontract(element);
      observerChangeCreateInput(element);
      addSubcontractFetch(idBill, elem);
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

function createInputSubcontract(element) {
  const subTypeSelect = document.querySelectorAll(".modal-subcontract-type");
  subTypeSelect.forEach((el) => {
    el.addEventListener("change", (event) => {
      if (el.nextSibling) {
        while (el.parentNode.children.length > 1) {
          el.parentNode.removeChild(el.parentNode.lastChild);
        }
      }
      let subcontractCategory = el.value;
      let endpoint =
        "/service/api/subcontract-category-" + subcontractCategory + "/";
      fetch(endpoint, {
        method: "get",
      })
        .then((response) => response.json())
        .then((data) => {
          let select = document.createElement("select");
          select.className = "modal-subcontract-type_choises choice";
          el.after(select);
          data.forEach(function (value, key) {
            new selectOption(
              "modal-select input-130",
              value.id,
              value.id,
              value.name
            ).appendTo(select);
          });
          new Input(
            "number",
            "modal-subcontract-input_sum input-200",
            "",
            "сумма"
          ).afterTo(select);

          let button = document.createElement("button");
          button.className = "modal_add_subcontract";
          button.innerHTML = "OK";
          select.nextElementSibling.after(button);

          new Input("hidden", "subcontract_id", "").afterTo(select);

          createNextSubcontractInput(button);
          return;
        });
    });
  });
}

function createNextSubcontractInput(button) {
  button.addEventListener("click", () => {
    let wrapperSubcontractInp = button.parentNode;

    var throwawayNode = wrapperSubcontractInp.removeChild(button);

    let dupNode = wrapperSubcontractInp.cloneNode();
    let dupSelect = wrapperSubcontractInp.firstElementChild.cloneNode(true);

    wrapperSubcontractInp.after(dupNode);
    dupNode.append(dupSelect);
    createInputSubcontract();
  });
}

function changeSum(element, mutationRecords) {
  let sumAdv = element.getAttribute("data-bill-month-adv");

  let sumAdvReplace = sumAdv.replace(/\s+/g, "");

  const wrapSubcontractors = document.querySelectorAll(
    ".modal-subcontract-input_sum"
  );
  let useBudget = document.querySelector(".modal_adv_budget_not_use");
  var sum = sumAdvReplace;
  // useBudget.innerHTML = sum;
  wrapSubcontractors.forEach((el, value) => {
    // sum += cashUse;
    // useBudget.innerHTML = sum

    el.addEventListener("keyup", () => {
      sum = sumAdvReplace - sum;

      sum = sumAdvReplace - el.value;
      useBudget.innerHTML = sum;
      // sum += cashUse;
      // let cashUseActuall = el.value
      // sum += cashUseActuall;
      // useBudget.innerHTML = sum
    });
    // let cashUse = +el.value;
    // sum += cashUse;
    // useBudget.innerHTML = sum;
  });
}

function observerChangeCreateInput(element) {
  const wrapSubcontractors = document.querySelector(
    ".modal_add_subcontract_wrapper"
  );

  let observer = new MutationObserver((mutationRecords) => {
    changeSum(element, mutationRecords);
  });
  observer.observe(wrapSubcontractors, {
    childList: true, // наблюдать за непосредственными детьми
    subtree: true, // и более глубокими потомками
    // characterDataOldValue: true // передавать старое значение в колбэк
  });
}

function addSubcontractFetch(idBill, elem) {
  const buttonAddSubcontract = document.querySelector(".subcontarct_add ");
  buttonAddSubcontract.addEventListener("click", () => {
    const subcontractArr = document.querySelectorAll(".modal_add-subcontract ");

    let arrSubcontarctAll = [];
    let contractId;

    subcontractArr.forEach((element, i) => {
      contractChild = element.children;
      const nameSubcontract = contractChild[1];
      let subcontractAdv;
      let subcontractOther;

      let idelemOld = contractChild[3];
      if (idelemOld === undefined) {
      } else {
        if (idelemOld.classList.contains("subcontract_id")) {
          let namesubs = contractChild[0].getAttribute("placeholder");
          choseNameSubcontract = nameSubcontract.getAttribute("data-id");
          if (namesubs == "adv") {
            subcontractAdv = choseNameSubcontract;
            subcontractOther = null;
          } else {
            subcontractOther = choseNameSubcontract;
            subcontractAdv = null;
          }
          let amount = contractChild[2].value;
          const contractObj = {
            id: idelemOld.value,
            month_bill: idBill,
            amount: amount,
            adv: subcontractAdv,
            other: subcontractOther,
          };

          arrSubcontarctAll.push(contractObj);
        } else {
          var choseNameSubcontract =
            nameSubcontract.options[nameSubcontract.selectedIndex].getAttribute(
              "data-id"
            );

          if (contractChild[0].value == "adv") {
            subcontractAdv = choseNameSubcontract;
            subcontractOther = null;
          } else {
            subcontractOther = choseNameSubcontract;
            subcontractAdv = null;
          }
          let amount = contractChild[3].value;
          const contractObj = {
            id: "",
            month_bill: idBill,
            amount: amount,
            adv: subcontractAdv,
            other: subcontractOther,
          };

          arrSubcontarctAll.push(contractObj);
        }
      }
    });

    const endpoint = "/service/api/subcontract/upd_subs/";
    let csrfToken = getCookie("csrftoken");
    let data = JSON.stringify(arrSubcontarctAll);
    console.log(data);
    fetch(endpoint, {
      method: "POST",
      body: data,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const updBill = {
          id: idBill,
          chekin_add_subcontr: true,
        };
        const endpoint = "/service/api/month_bill/" + idBill + "/";
        let csrfToken = getCookie("csrftoken");
        let data2 = JSON.stringify(updBill);
        fetch(endpoint, {
          method: "PUT",
          body: data2,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
        }).then((response) => {
          if (response.ok) {
            const windowContent = document.getElementById(elem);
            alertSuccess(windowContent);
            const timerId = setTimeout(() => {
              // location.reload();
            }, 200);
          } else {
            const windowContent = document.getElementById(elem);

            alertError(windowContent);
            const timerId = setTimeout(() => {
              // location.reload();
            }, 200);
          }
        });
      });
  });
}

function getOldSumcintract(idBill,element) {
  const endpoint = "/service/api/subcontract/" + idBill + "/subcontract_li/";
  let csrfToken = getCookie("csrftoken");
  fetch(endpoint, {
    method: "GET",
    // body: data,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.length == 0) {
        return;
      } else {
        let endpoint = "/service/api/subcontract-category-adv/";
        fetch(endpoint, {
          method: "get",
        })
          .then((response) => response.json())
          .then((dataCategoryAdv) => {
            const c = document.querySelector(".modal_add_subcontract_wrapper");
            c.innerHTML = "";
            data.forEach(function (value, key) {
              let modal_add_subcontract = document.createElement("div");
              modal_add_subcontract.className =
                "modal_add_contract modal_add-subcontract";
              c.append(modal_add_subcontract);

              if (value.adv != null) {
                modal_add_subcontract.innerHTML =
                  '<input type="text" readonly class="modal-subcontracts input-130" placeholder="adv" value="площадка" data-adv="adv">';
                dataCategoryAdv.forEach((item) => {
                  if (item.id == value.adv) {
                    new Input(
                      "text",
                      "modal-subcontracts   input-130 subs-old",
                      item.name,
                      "сумма",
                      true,
                      item.id
                    ).appendTo(modal_add_subcontract);

                    new Input(
                      "text",
                      "modal-subcontracs input-200",
                      value.amount,
                      "сумма"
                    ).appendTo(modal_add_subcontract);
      
                    new Input("hidden", "subcontract_id", value.id).appendTo(
                      modal_add_subcontract
                    );
                    let prevOperationDel = document.createElement("button");
                    prevOperationDel.className = "subcontract_del";
      
                    modal_add_subcontract.append(prevOperationDel);
                    prevOperationDel.setAttribute("data-id-peration", value.id);
                    prevOperationDel.innerHTML = "-";
                  }
                });
              } else {
                let endpoint = "/service/api/subcontract-category-other/";
                fetch(endpoint, {
                  method: "get",
                })
                  .then((response) => response.json())
                  .then((dataCategoryOther) => {
                    dataCategoryOther.forEach((item) => {
                      if (item.id == value.other) {
                        modal_add_subcontract.innerHTML =
                          '<input type="text" readonly class="modal-subcontracts input-130" placeholder="other" value="премия" data-adv="other">';
                        new Input(
                          "text",
                          "modal-subcontracts   input-130 subs-old",
                          item.name,
                          "сумма",
                          true,
                          item.id
                        ).appendTo(modal_add_subcontract);
                        new Input(
                          "text",
                          "modal-subcontracs input-200",
                          value.amount,
                          "сумма"
                        ).appendTo(modal_add_subcontract);

                        new Input(
                          "hidden",
                          "subcontract_id",
                          value.id
                        ).appendTo(modal_add_subcontract);

                        let prevOperationDel = document.createElement("button");
                        prevOperationDel.className = "subcontract_del";

                        modal_add_subcontract.append(prevOperationDel);
                         prevOperationDel.setAttribute("data-id-peration",value.id);
                        prevOperationDel.innerHTML = "-";
                      }
                    });
                  });
              }

              
            });
            DelSubcontr(element)
            let modal_add_subcontract = document.createElement("div");
            modal_add_subcontract.className =
              "modal_add_contract modal_add-subcontract";
            c.append(modal_add_subcontract);

            let modal_add_subcontract_select = document.createElement("select");
            modal_add_subcontract_select.className =
              "modal-subcontract-type choice";
            modal_add_subcontract.append(modal_add_subcontract_select);

            new selectOption(
              "modal-select empty",
              0,
              "",
              "Тип",
              0,
              false
            ).appendTo(modal_add_subcontract_select);
            new selectOption(
              "modal-select",
              "adv",
              "",
              "площадка",
              "selected",
              false
            ).appendTo(modal_add_subcontract_select);

            new selectOption(
              "modal-select ",
              "other",
              "",
              "премия",
              "selected",
              false
            ).appendTo(modal_add_subcontract_select);

            createInputSubcontract();
           
          });
      }
    });
}

function FetchCatSubsOther() {
  let endpoint = "/service/api/subcontract-category-other/";
  fetch(endpoint, {
    method: "get",
  })
    .then((response) => response.json())
    .then((dataCategoryOther) => {
      return dataCategoryOther;
    });
}


function DelSubcontr(element) {
  console.log(1)
  const delButton = document.querySelectorAll(".subcontract_del");
  delButton.forEach((item) => {
    item.addEventListener("click", () => {
      console.log(1111)
      idOperation = item.getAttribute("data-id-peration");
      console.log(idOperation);
      endpoint = "/service/api/subcontract/" + idOperation + "/";

      item.parentElement.remove();

      let csrfToken = getCookie("csrftoken");

      fetch(endpoint, {
        method: "DELETE",
        
        headers: {
          "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
      }).then((response) => {
        if (response.ok) {
          const add_operation = document.querySelector(".subcontarct_add");
          add_operation.replaceWith(add_operation.cloneNode(true));
          element.click();

          return;
        }
      });
    });
  });
}

