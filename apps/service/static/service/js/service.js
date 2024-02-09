choiceColor();

const addBill = document.querySelectorAll('[data-name="modal-add-bill"]');

if (addBill) {
  addBill.forEach((el) => {
    el.addEventListener("click", () => {
      let elem = el.getAttribute("data-name");
      let dataBill = el.getAttribute("data-month");
      // 2024-02-08 11:01:04.011583
      const date = new Date();
      let currentYear = new Date().getFullYear();
      const monthName = date.toLocaleString("default", { month: "long" });
      let currentMonthYear = monthName.substr(0, 3) + " " + currentYear;
      console.log(date)

      const pageName = document.getElementById("page_name").value;
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

      const contractSum = document.querySelector(".modal-contract_sum");
      contractSum.value = "";
      modal(elem);
      getClientFilterCategory(pageName, dataBill, currentMonthYear);
    });
  });
}

function getClientFilterCategory(pageName, dataBill, currentMonthYear) {
  const endpoint =
    "/clients/api/client/client_filter_list/?service=" + pageName;
  const select = document.querySelector(".modal-client");

  fetch(endpoint, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      select.innerHTML = "";

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
            });
            addMonthBill(dataBill, currentMonthYear);
          });
      });
    });
}

function addMonthBill(dataBill, currentMonthYear) {
  const addMontContract = document.querySelector(
    ".client_additional-contract_add"
  );

  addMontContract.addEventListener("click", (event) => {
    const form = document.getElementById("month_bill");
    const service_name = document.getElementById("page_name").value;
    const contractId = document.getElementById("contract_main").value;

    let date = new Date();

    let month = date.getMonth() + 1;
    let year = date.getFullYear();

    const contractName = contractId + "/" + year + "-" + month;

    const data = new FormData(form);
    data.append("service", service_name);
    data.append("contract_number", contractName);

    if (dataBill.toLowerCase() === currentMonthYear) {
      console.log(1);
    } else {
      console.log(0);
    }

    let object = {};
    data.forEach((value, key) => (object[key] = value));
    const dataJson = JSON.stringify(object);
    let csrfToken = getCookie("csrftoken");
    // const endpoint = "/clients/api/additional_contract/";
    fetch(endpoint, {
      method: "POST",
      body: dataJson,
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const client = data.client;
        const service = data.service;
        const contract = data.main_contract;
        const additional_contract = data.id;

        const form = new FormData();
        form.append("client", client);
        form.append("service", service);
        form.append("contract", contract);
        form.append("additional_contract", additional_contract);

        let object = {};
        form.forEach((value, key) => (object[key] = value));
        const dataJson = JSON.stringify(object);

        let csrfToken = getCookie("csrftoken");

        fetch("/service/api/month_bill/", {
          method: "POST",
          body: dataJson,
          headers: {
            "Content-Type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrfToken,
          },
        });
      });
  });
}
