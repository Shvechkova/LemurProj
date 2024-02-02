const modal_button = document.querySelectorAll(".open-modal");
const modal_windows = document.querySelector(".modal");
const selectOne = document.querySelector(".modal-service_type");

modal_button.forEach((element) => {
  element.addEventListener("click", () => {
    let elem = element.getAttribute("data-name");
    modal(elem);
    addManager();
    addService(selectOne);
    createInputContract();
    
    const endpointClient = "/clients/api/client/";
    const endpointContact = "/clients/api/contract/";
    const endpointContractAll = "/clients/api/contract/create_contracts/";
    const optionsMethod = "POST"
   
    addNewClient(endpointClient,endpointContact,endpointContractAll,optionsMethod);
  });
});


function addManager(selectedOption) {
  const endpoint = "/clients/api/client/manager_list/";
  const select = document.querySelector(".modal-manager_client");

  fetch(endpoint, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      let selectHTML = "";

      data.forEach(function (value, key) {
        if (value.id == selectedOption) {
          selectHTML += `<option selected  class="modal-select" data-id="${value.id}"  value="${value.last_name}">${value.last_name}</option>`;
        } else {
          selectHTML += `<option class="modal-select" data-id="${value.id}"  value="${value.last_name}">${value.last_name}</option>`;
        }
      });
      select.innerHTML = selectHTML;
    });
}
//  const selectOne = document.querySelector(".modal-service_type");
function addService(selectInput, selectedOption) {
  const instance = "/service/service_category/";

  const select = selectInput;
  fetch(instance, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      let selectHTML = "";
      let selectedTag = "";

      data.forEach(function (value, key) {
        let name = value.name;
        if (value.id == selectedOption) {
          selectHTML += `<option selected  class="modal-select" data-id="${value.id}"  value="${value.id}">${name}</option>`;
        } else {
          selectHTML += `<option class="modal-select" data-id="${value.id}"  value="${value.id}">${name}</option>`;
        }
      });
      select.innerHTML = selectHTML;
    });
}

function createInputContract() {
  document
    .querySelector(".contract_add")
    .addEventListener("click", function () {
      const contract_add = document.querySelectorAll(".contract_add");

      var contractInput = document
        .querySelector(".modal_add_contract")
        .cloneNode();
      contractInput.innerHTML = document.querySelector(
        ".modal_add_contract"
      ).innerHTML;

      document.querySelector(".modal-client").appendChild(contractInput);
      contractInput = document.querySelector(".modal_add_contract").cloneNode();
      contractInput.innerHTML = document.querySelector(
        ".modal_add_contract"
      ).innerHTML;
    });
}

function addNewClient(endpointClient,endpointContact,endpointContractAll,optionsMethod,clientId) {
  const add_contract = document.querySelector(".client_contract_add");

  add_contract.addEventListener("click", () => {
    const clientName = document.querySelector(".modal-client_name").value;
    const manegeSelect = document.querySelector(".modal-manager_client");
    let managerProject =
      manegeSelect.options[manegeSelect.selectedIndex].getAttribute("data-id");
    let clientObj = {
      client_name: clientName,
      
    };
    if(clientId != undefined){
      clientObj['id'] = clientId
    }
    console.log()
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
    console.log(optionsMethod)
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
        let contractId
        contractArr.forEach((element) => {
          let contract_child = element.childNodes;
       
          const contract_name = contract_child[3].value;
          
          const type_servise = contract_child[1];
          var servise =
            type_servise.options[type_servise.selectedIndex].getAttribute(
              "data-id"
            );
          const data = contract_child[5].value;
          const contractSum = contract_child[7].value;

          const contractObj = {
            client: clientId,
            contract_number: contract_name,
            date_start: data,
            service: servise,
            manager: managerProject,
            contract_sum: contractSum,
          };

          
          
          if (contract_child[9]){
            contractId = contract_child[9].value;
             contractObj['contract_id'] = contractId
          }
          
          arrContractAll.push(contractObj);
        });
        let endpointTwo;
        let data;
        if (arrContractAll.length > 1) {
          endpointTwo = endpointContractAll;
          data = JSON.stringify(arrContractAll);
        } else {
          endpointTwo = endpointContact + contractId +"/";
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

const updInfo = document.querySelectorAll(".upd_info");
updInfo.forEach((element) => {
  element.addEventListener("click", () => {
    // const modalWindows = document.querySelector(".modal");
    let elem = element.getAttribute("data-name");
    let clientName = element.getAttribute("data-client-name");
    
    modal(elem);
    updClientContract(element, clientName);
    createInputContract();
   
    const idClient = element.getAttribute("data-client-id");
    const endpointClient = "/clients/api/client/" +idClient+"/";
    const endpointContact = "/clients/api/contract/"
    const endpointContractAll = "/clients/api/contract/create_contracts/";
    const optionsMethod = "PUT"
   
    addNewClient(endpointClient,endpointContact,endpointContractAll,optionsMethod,idClient)
  });
});

function updClientContract(element, clientName) {
  const titleModal = document.querySelector(".modal-client_title");
  titleModal.innerHTML = "изменить клиента";
  const idClient = element.getAttribute("data-client-id");
  getContracts(idClient);
  const clientNameInput = document.querySelector(".modal-client_name");
  clientNameInput.value = clientName;

}

function getContracts(idClient) {
  const endpoint = "/clients/api/contract/" + idClient + "/contract_li/";
  fetch(endpoint, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      let contaractHTML = "";
      const contractWrapper = document.querySelector(
        ".modal_add_contract_wrapper"
      );

      let manager;
      data.forEach((el) => {
        manager = el.manager;

        contaractHTML += `
        <div class="modal_add_contract">
        <select data-selected="${el.service}" class="modal-service_type"></select>
        <input
          class="modal-client_contract-name"
          type="text"
          placeholder="Номер договора"
          value="${el.contract_number}"
        />
        <input
          class="modal-client_contract-date"
          type="date"
          placeholder="Подписан"
          value="${el.date_start}"
        />
        <input
          class="modal-client_contract-sum"
          type="number"
          placeholder="Сумма"
          value="${el.contract_sum}"
        />
        <input
          type="hidden"
          value="${el.id}"
        />
      </div>`;
      });
      contractWrapper.innerHTML = contaractHTML;
      const serviceName = document.querySelectorAll(".modal_add_contract");

      serviceName.forEach((elem) => {
        let elemSelect = elem.querySelector(".modal-service_type");
        const selected = elemSelect.getAttribute("data-selected");
        addService(elemSelect, selected);
      });

      addManager(manager);
    });
}
