const modal_button = document.querySelectorAll(".open-modal");
const modal_windows = document.querySelector(".modal");

// модалка первичного добавления клиента и контракта
modal_button.forEach((element) => {
  element.addEventListener("click", () => {
    let elem = element.getAttribute("data-name");
    modal(elem);

    addManager();
    createInputContract();
    choiceColor();
    const endpointClient = "/clients/api/client/";
    const endpointContact = "/clients/api/contract/";
    const endpointContractAll = "/clients/api/contract/create_contracts/";
    const optionsMethod = "POST";

    addNewClient(
      endpointClient,
      endpointContact,
      endpointContractAll,
      optionsMethod
    );
  });
});
// менеджеры из базы
function addManager(selected) {
  const endpoint = "/clients/api/client/manager_list/";
  const select = document.querySelector(".modal-manager_client");
  new selectOption("modal-select empty", "0", "", "Менеджер", true).appendTo(
    select
  );

  fetch(endpoint, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      data.forEach(function (value, key) {
        new selectOption(
          "modal-select",
          value.last_name,
          value.id,
          value.last_name,
          selected
        ).appendTo(select);
      });
    });
}
// сервисы из базы
function addService(selectInput, selected) {
  const select = selectInput;
  new selectOption("modal-select", "0", "", "Услуга").appendTo(select);
  const instance = "/service/service_category/";

  fetch(instance, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      data.forEach(function (value, key) {
        new selectOption(
          "modal-select input-130",
          value.id,
          value.id,
          value.name,
          selected
        ).appendTo(select);
      });
    });
}

// создание пустых строчек договоров
function createInputContract() {
  const contractWrapper = document.getElementById("modal_contract_wrapper");
  let divWrapper = document.createElement("div");
  divWrapper.className = "modal_add_contract";
  contractWrapper.append(divWrapper);

  let select = document.createElement("select");
  select.className = "modal-service_type choice";
  divWrapper.append(select);
  addService(select);
  new Input(
    "text",
    "modal-client_contract-input input-200",
    "",
    "Номер договора"
  ).appendTo(divWrapper);
  new Input(
    "date",
    "modal-client_contract-input input-130",
    "",
    "Подписан"
  ).appendTo(divWrapper);
  new Input(
    "number",
    "modal-client_contract-input input-130",
    "",
    "Сумма"
  ).appendTo(divWrapper);
  new Input("hidden", " 1").appendTo(divWrapper);

  let button = document.createElement("button");
  button.className = "modal_add_contract_btn";
  button.innerHTML = "OK";
  divWrapper.append(button);
  choiceColor();

  button.addEventListener("click", () => {
    button.remove();
    createInputContract();
  });
}

function addNewClient(
  endpointClient,
  endpointContact,
  endpointContractAll,
  optionsMethod,
  clientId
) {
  const add_contract = document.querySelector(".client_contract_add");

  add_contract.addEventListener("click", () => {
    const clientName = document.querySelector(".modal-client_name").value;
    const manegeSelect = document.querySelector(".modal-manager_client");
    let managerProject =
      manegeSelect.options[manegeSelect.selectedIndex].getAttribute("data-id");
    let clientObj = {
      client_name: clientName,
    };
    if (clientId != undefined) {
      clientObj["id"] = clientId;
    }

    let data = JSON.stringify(clientObj);
    function getCookie(name) {
      let matches = document.cookie.match(
        new RegExp(
          "(?:^|; )" +
            name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
            "=([^;]*)"
        )
      );
      return matches ? decodeURIComponent(matches[1]) : undefined;
    }
    let csrfToken = getCookie("csrftoken");

    fetch(endpointClient, {
      method: optionsMethod,
      body: data,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())

      .then((response) => {
        clientId = response.id;
        const contractArr = document.querySelectorAll(".modal_add_contract");

        let arrContractAll = [];
        let contractId;
        contractArr.forEach((element) => {
          let contractChild = element.childNodes;
          console.log(contractChild[1].value);
          if (contractChild[1].value == "") {
            return;
          } else {
            let contractName = contractChild[1].value;
            const type_servise = contractChild[0];
            var servise =
              type_servise.options[type_servise.selectedIndex].getAttribute(
                "data-id"
              );
            const data = contractChild[2].value;
            const contractSum = contractChild[3].value;

            const contractObj = {
              client: clientId,
              contract_number: contractName,
              date_start: data,
              service: servise,
              manager: managerProject,
              contract_sum: contractSum,
            };

            if (contractChild[4]) {
              contractId = contractChild[4].value;
              contractObj["id"] = contractId;
            }

            arrContractAll.push(contractObj);
          }
         
        });
        let endpointTwo;

        let data;
        if (arrContractAll.length > 1) {
          endpointTwo = endpointContractAll;
          data = JSON.stringify(arrContractAll);
        } else {
          if (contractId != "") {
            endpointTwo = endpointContact  + contractId + "/";
          } else {
            endpointTwo = endpointContact;
            optionsMethod = "POST";
          }

          objContractAll = arrContractAll[0];
          data = JSON.stringify(objContractAll);
        }
        fetch(endpointTwo, {
          method: optionsMethod,
          body: data,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
        });
      });
  });
}
// модалка обновления клиента контракта
const updInfo = document.querySelectorAll(".upd_info");
updInfo.forEach((element) => {
  element.addEventListener("click", () => {
    // const modalWindows = document.querySelector(".modal");
    let elem = element.getAttribute("data-name");
    let clientName = element.getAttribute("data-client-name");

    modal(elem);
    updClientContract(element, clientName);

    const idClient = element.getAttribute("data-client-id");
    const endpointClient = "/clients/api/client/" + idClient + "/";
    const endpointContact = "/clients/api/contract/";
    //  + contractId + "/"
    const endpointContractAll = "/clients/api/contract/upd_contracts/";
    const optionsMethod = "PUT";

    addNewClient(
      endpointClient,
      endpointContact,
      endpointContractAll,
      optionsMethod,
      idClient
    );
  });
});
//забрать имя клиента
function updClientContract(element, clientName) {
  const titleModal = document.querySelector(".modal-client_title");
  titleModal.innerHTML = "изменить клиента";
  const idClient = element.getAttribute("data-client-id");
  getContracts(idClient);
  const clientNameInput = document.querySelector(".modal-client_name");
  clientNameInput.value = clientName;
}

//получить контракты по имени клиента
function getContracts(idClient) {
  const endpoint = "/clients/api/contract/" + idClient + "/contract_li/";
  fetch(endpoint, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      const contractWrapper = document.getElementById("modal_contract_wrapper");

      data.forEach((el) => {
        // запись менеджера
        manager = el.manager;
        addManager(manager);

        let divWrapper = document.createElement("div");
        divWrapper.className = "modal_add_contract";
        contractWrapper.append(divWrapper);

        //запись услуг
        let select = document.createElement("select");
        select.className = "modal-service_type";
        divWrapper.append(select);
        addService(select, el.service);

        new Input(
          "text",
          "modal-client_contract-input",
          el.contract_number,
          "Номер договора"
        ).appendTo(divWrapper);
        new Input(
          "date",
          "modal-client_contract-input",
          el.date_start,
          "Подписан"
        ).appendTo(divWrapper);
        new Input(
          "number",
          "modal-client_contract-input",
          el.contract_sum,
          "Сумма"
        ).appendTo(divWrapper);
        new Input("hidden", " ", el.id, "").appendTo(divWrapper);
      });

      createInputContract();
    });
}

// класс конструктор инпутов
class Input {
  constructor(type, className, value, placeholder) {
    this.elem = document.createElement("input");
    if (type) this.elem.type = type;
    if (className) this.elem.className = className;
    if (value) this.elem.value = value;
    if (placeholder) this.elem.placeholder = placeholder;
  }

  appendTo(parent) {
    parent.append(this.elem);
  }
}
// класс конструктор оптион в селектах
class selectOption {
  constructor(className, value, id, text, selected, disabled) {
    this.elem = document.createElement("option");
    if (className) this.elem.className = className;
    if (value) this.elem.value = value;
    if (id) this.elem.setAttribute("data-id", id);
    if (text) this.elem.innerHTML = text;
    if (selected == id) this.elem.selected = true;
    if (disabled == true) this.elem.disabled = true;
  }

  appendTo(parent) {
    parent.append(this.elem);
  }
}
// смена цвета оптион на серый
function choiceColor() {
  let choice = document.querySelectorAll(".choice");
  choice.forEach((element) => {
    const selectedValue = element.value;
    if (element.value == 0) {
      element.classList.add("empty");
    } else element.classList.remove("empty");
    element.addEventListener("change", (event) => {
      if (element.value == 0) {
        element.classList.add("empty");
      } else element.classList.remove("empty");
    });
  });
}
