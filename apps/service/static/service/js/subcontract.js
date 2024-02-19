choiceColor();

const btnSubcontarct = document.querySelectorAll(".add_sabcontactor");

if (btnSubcontarct) {
  btnSubcontarct.forEach((element) => {
    element.addEventListener("click", () => {
      let elem = element.getAttribute("data-name");
      let idBill = element.getAttribute("data-bill-month-id");
      let sumAdv = element.getAttribute("data-bill-month-adv");
      console.log(sumAdv)
      let budgetInnerAll = document.querySelector(".modal_adv_budget_all");
      budgetInnerAll.innerHTML = sumAdv;

      const add_subc = document.querySelector(".subcontarct_add");
      modal(elem,add_subc);
      const c = document.querySelector(".modal_add_subcontract_wrapper")
      // c.innerHTML = ""
      c.innerHTML = '<div class="modal_add_contract modal_add-subcontract"><select class="modal-subcontract-type choice"><option disabled selected class="modal-select empty" value="0">Тип</option><option class="modal-select" value="adv">площадка</option><option class="modal-select" value="other">премия</option></select></div>'


      getOldSumcintract(idBill);

      getInfoBill(element);
      createInputSubcontract(element);
      observerChangeCreateInput(element);
      addSubcontractFetch(idBill);
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

  const wrapSubcontractors = document.querySelectorAll(
    ".modal-subcontract-input_sum"
  );
  let useBudget = document.querySelector(".modal_adv_budget_not_use");
  var sum = 0;
  useBudget.innerHTML = sum;
  wrapSubcontractors.forEach((el, value) => {
    // sum += cashUse;
    // useBudget.innerHTML = sum

    el.addEventListener("keyup", () => {
      // sum += cashUse;
      // let cashUseActuall = el.value
      // sum += cashUseActuall;
      // useBudget.innerHTML = sum
    });
    let cashUse = +el.value;
    sum += cashUse;
    useBudget.innerHTML = sum;
  });
}

function observerChangeCreateInput(element) {
  const wrapSubcontractors = document.querySelector(
    ".modal_add_subcontract_wrapper"
  );

  let observer = new MutationObserver((mutationRecords) => {
    // console.log(mutationRecords)
    changeSum(element, mutationRecords);
  });
  observer.observe(wrapSubcontractors, {
    childList: true, // наблюдать за непосредственными детьми
    subtree: true, // и более глубокими потомками
    // characterDataOldValue: true // передавать старое значение в колбэк
  });
}

function addSubcontractFetch(idBill) {
  const buttonAddSubcontract = document.querySelector(".subcontarct_add ");
  buttonAddSubcontract.addEventListener("click", () => {
    const subcontractArr = document.querySelectorAll(".modal_add-subcontract ");

    let arrSubcontarctAll = [];
    let contractId;

    subcontractArr.forEach((element, i) => {
      contractChild = element.children;

      const nameSubcontract = contractChild[1];
      var choseNameSubcontract =
        nameSubcontract.options[nameSubcontract.selectedIndex].getAttribute(
          "data-id"
        );

      let subcontractAdv;
      let subcontractOther;
      if (contractChild[0].value == "adv") {
        subcontractAdv = choseNameSubcontract;
        subcontractOther = null;
      } else {
        subcontractOther = choseNameSubcontract;
        subcontractAdv = null;
      }

      let amount = contractChild[3].value;

      const contractObj = {
        month_bill: idBill,
        amount: amount,
        adv: subcontractAdv,
        other: subcontractOther,
      };

      arrSubcontarctAll.push(contractObj);
    });

    const endpoint = "/service/api/subcontract/add/";
    let csrfToken = getCookie("csrftoken");
    let data = JSON.stringify(arrSubcontarctAll);
    fetch(endpoint, {
      method: "POST",
      body: data,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      // .then((response) => response.json(

      // ))
      .then((response) => {
        if (response.ok) {
          location.reload();
        }
      });
  });
}

function getOldSumcintract(idBill) {
//  const endpoint = "/service/api/subcontract/" +idBill +"/subcontract_li/";
//   let csrfToken = getCookie("csrftoken");
 

//   fetch(endpoint, {
//     method: "GET",
//     // body: data,
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": csrfToken,
//     },
//   })
//    .then((response) => response.json())
//       .then((data) => {
//         console.log(data.length);
//       if(data.length == 0){
//         return
//       } 
//       else{
//         const c = document.querySelector(".modal_add_subcontract_wrapper")
//         c.innerHTML = ""

        

    
//         data.forEach(function (value, key) {
//           let modal_add_subcontract = document.createElement("div");
//           modal_add_subcontract.className = "modal_add_contract modal_add-subcontract";
//            c.append(modal_add_subcontract)
//           console.log(value.adv)
//           if(value.adv == 1){
//             modal_add_subcontract.innerHTML = '<input type="text" class="modal-subcontract-type input-200" placeholder="1" value="площадка">'
//           } else if(value.adv == 2){
//             modal_add_subcontract.innerHTML = '<input type="text" class="modal-subcontract-type input-200" placeholder="1" value="премия">'
//           }

//           new Input(
//           "text",
//           "modal-subcontract-type input-200",
//           "",
//           "сумма"
//         ).afterTo(modal_add_subcontract);
          
//         });
       

//         // let button = document.createElement("button");
//         // button.className = "modal_add_subcontract";
//         // button.innerHTML = "OK";
//         // select.nextElementSibling.after(button);

//         // new Input("hidden", "subcontract_id", "").afterTo(select);

//         // createNextSubcontractInput(button);
//         return
      
     

         

//       }
//       }); 
}
