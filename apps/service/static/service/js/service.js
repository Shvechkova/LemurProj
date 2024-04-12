choiceColor();
// добавление счета первичное
const addBill = document.querySelectorAll('[data-name="modal-add-bill"]');
if (addBill) {
  addBill.forEach((el) => {
    el.addEventListener("click", () => {
      choiceColor();
      let elem = el.getAttribute("data-name");
      let dataBill = el.getAttribute("data-month");
      let dataCatServise = el.getAttribute("data-cat-service");
      // убрать сумму ведения для не адв
      if (dataCatServise != 1) {
        const advWrap = document.querySelector(".adv_all_sum_wrapper");
        advWrap.style.display = "none";
        const advSum = document.querySelector("#adv_all_sum");
        advSum.value = 0;
       
      }
      // имя страницы для фильтрации доступных клиентов
      const pageName = document.getElementById("page_name").value;
      // очистить селекты повторыне открытия
      const selectContract = document.querySelector(
        ".modal-client_main-contract"
      );

      selectContract.innerHTML = "";
      new selectOption("modal-select empty", 0, 0, "Договор", 0, true).appendTo(
        selectContract
      );

      const contractSum = document.querySelector(".modal-contract_sum");
      contractSum.value = "";
      const battonAdd = document.querySelector(
        ".client_additional-contract_add"
      );

      modal(elem, battonAdd);
     
      getClientFilterCategory(pageName, dataBill, elem);
      addMonthBill(dataBill, elem);

      // валидация
      const modalWindows = document.getElementById(elem);
      modalWindows.addEventListener("input", () => {
        validate(elem, ".client_additional-contract_add");
      });
    });
  });
}

// получение доступных клиентов для категории сервиса
function getClientFilterCategory(pageName, dataBill, elem) {
  const endpoint =
    "/clients/api/client/client_filter_list/?service=" + pageName;
  const select = document.querySelector(".modal-client");

  fetch(endpoint, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      select.innerHTML = "";
      // заполнение селекта клиентов списком
      new selectOption("modal-select empty", 0, 0, "Клиент", 0, true).appendTo(
        select
      );

      data.forEach(function (value, key) {
        new selectOption(
          "modal-select",
          value.id,
          value.id,
          value.client_name
        ).appendTo(select);
      });
      
      // при выборе клиента заполнение остальнох инпутов доступно инфой из контракта
      select.addEventListener("change", (event) => {
        let clientId = select.value;
        const endpoint =
          "/clients/api/contract/contract_filter_list/?service=" + pageName;
        fetch(endpoint + "&client=" + clientId, {
          method: "get",
        })
          .then((response) => response.json())
          .then((data) => {
            const selectContract = document.querySelector(
              ".modal-client_main-contract"
            );
            selectContract.innerHTML = "";

            new selectOption(
              "modal-select empty",
              0,
              0,
              "Контракт",
              0,
              true
            ).appendTo(selectContract);

            data.forEach(function (value, key) {
              new selectOption(
                "modal-select",
                value.id,
                value.id,
                value.contract_number,
                value.id
              ).appendTo(selectContract);
              choiceColor();
              const contractSum = document.querySelector(".modal-contract_sum");
              contractSum.value = value.contract_sum;
              replaceNam ()
            });
          modalWindows.click();
            // иммитация лика для валидации не адв
          });
      });
      // валидация
      const modalWindows = document.getElementById(elem);
      modalWindows.addEventListener("click", () => {
        validate(elem, ".client_additional-contract_add");
      });
    });
}
// добавление месячного счета
function addMonthBill(dataBill, elem) {
  const addMontContract = document.querySelector(
    ".client_additional-contract_add"
  );

  addMontContract.addEventListener("click", (event) => {
    const form = document.getElementById("month_bill");
    const service_name = document.getElementById("page_name").value;
    const contractId = document.getElementById("contract_main").value;

    const contract_sum = document.getElementById("contract_sum").value.replace(/[^+\d]/g, '').replace(/(\d)\++/g, '$1');
    const adv_sum = document.getElementById("adv_all_sum").value.replace(/[^+\d]/g, '').replace(/(\d)\++/g, '$1');
    const diff_sum = contract_sum - adv_sum;

    const clientId = document.querySelector(".modal-client");
    const nameServise = document.querySelector("#page_name_abc").value;

    let date = new Date();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();
    const contractName = nameServise + "/" + year + "-" + month;

    const data = new FormData();
    data.append("client", clientId.value);
    data.append("service", service_name);
    data.append("contract_number", contractName);
    data.append("contract", contractId);
    data.append("contract_sum", contract_sum);
    data.append("diff_sum", diff_sum);
    // суммы адв для категорий
    if (service_name == "1") {

      data.append("adv_all_sum", adv_sum);
    } else {
     
      data.append("adv_all_sum", 0);
    }

    let object = {};
    data.forEach((value, key) => (object[key] = value));
    const dataJson = JSON.stringify(object);

    let csrfToken = getCookie("csrftoken");
    fetch("/service/api/month_bill/", {
      method: "POST",
      body: dataJson,
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
        "X-CSRFToken": csrfToken,
      },
    }).then((response) => {
      if (response.ok === true) {
        const windowContent = document.getElementById(elem);
        alertSuccess(windowContent);
        const timerId = setTimeout(() => {
           location.reload();
        }, 200);
      } else {
        const windowContent = document.getElementById(elem);
        console.log(windowContent);
        alertError(windowContent);
        const timerId = setTimeout(() => {
           location.reload();
        }, 200);
      }
    });
  });
}

// изменение счета данные
const changeBill = document.querySelectorAll('[data-name="modal-change-bill"]');
if (changeBill) {
  changeBill.forEach((el) => {
    let dataCatServise = el.getAttribute("data-cat-service");
    if (dataCatServise != 1) {
      const advWrap = document.querySelector(".adv_all_sum_wrapper_change");
      advWrap.style.display = "none";
    }
    el.addEventListener("click", () => {
  
      let elem = el.getAttribute("data-name");
      let idBill = el.getAttribute("data-id-bill");
      let idBillName = el.getAttribute("data-bill-month-client-name");
      let nameClientBill = el.getAttribute("data-bill-month-name");
      let sumBill = el.getAttribute("data-bill-month-sum");
      let sumAdvBill = el.getAttribute("data-bill-month-sum-adv");
      let service_name = el.getAttribute("data-cat-service");

      const battonAddchange = document.querySelector(".client-contract_change");
      let sumBillStr = sumBill.replace(/\s+/g, "");
      let sumAdvBillStr = sumAdvBill.replace(/\s+/g, "");

      modal(elem, battonAddchange);

      let idBillModal = document.querySelector("#client_change");
      let nameClientBillModal = document.querySelector("#contract_main_change");
      let sumBillModal = document.querySelector("#contract_sum_change");
      let sumAdvBillModal = document.querySelector("#adv_all_sum_change");
      idBillModal.value = idBillName;
      nameClientBillModal.value = nameClientBill;
      sumBillModal.value = +sumBillStr;
      sumAdvBillModal.value = +sumAdvBillStr;
     
      updBillChange(idBill, service_name, elem);
    });
  });
}
// изменение счета функции
function updBillChange(idBill, service_name, elem) {
  replaceNam ()
  const battonAddchange = document.querySelector(".client-contract_change");
  battonAddchange.addEventListener("click", () => {
    const endpoint = "/service/api/month_bill/" + idBill + "/";
    const data = new FormData();

    let nameClientBillModal = document.querySelector(
      "#contract_main_change"
    ).value;
    let sumBillModal = document.querySelector("#contract_sum_change").value.replace(/[^+\d]/g, '').replace(/(\d)\++/g, '$1');
    let sumAdvBillModal = document.querySelector("#adv_all_sum_change").value.replace(/[^+\d]/g, '').replace(/(\d)\++/g, '$1');

    const diff_sum = sumBillModal - sumAdvBillModal;

    data.append("contract_number", nameClientBillModal);
    data.append("contract_sum", sumBillModal);
    data.append("diff_sum", diff_sum);

    if (service_name == "1") {
      data.append("adv_all_sum", sumAdvBillModal);
    } else {
      data.append("adv_all_sum", 0);
    }
    let object = {};
    data.forEach((value, key) => (object[key] = value));
    const dataJson = JSON.stringify(object);
    console.log(dataJson);
    let csrfToken = getCookie("csrftoken");
    fetch(endpoint, {
      method: "PUT",
      body: dataJson,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    }).then((response) => {
      if (response.ok === true) {
        const windowContent = document.getElementById(elem);
        alertSuccess(windowContent);
        const timerId = setTimeout(() => {
          location.reload();
        }, 200);
      } else {
        const windowContent = document.getElementById(elem);
        console.log(windowContent);
        alertError(windowContent);
        const timerId = setTimeout(() => {
          location.reload();
        }, 200);
      }
    });
  });
}

// удаление месячного счета
const btnDelBill = document.querySelectorAll(".btn_month_bill-del");
if (btnDelBill) {
  btnDelBill.forEach((element) => {
    element.addEventListener("click", () => {
 
      // preloaderModal(isLoading=false,isLoaded=true)
      const idBill = element.getAttribute("data-id-bill");
      endpoint = "/service/api/month_bill/" + idBill + "/";
      fetch(endpoint, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => {
        if (response.ok === true) {
          const itemWrap = element.parentElement;
          itemWrap.parentElement.parentElement.remove();
          location.reload();
        }else {
       
          let allarm = document.createElement("div");
          allarm.className = "allarm";
          allarm.innerHTML = "нельзя удалить";
          element.parentElement.after(allarm);
          const timerId = setTimeout(() => {
            allarm.remove()
          }, 700);
      
          
        }
      });
    });
  });
}
