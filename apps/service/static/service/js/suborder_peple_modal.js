const addOperationOutPeople = document.querySelectorAll(
  ".suborder_out_operation_people"
);

if (addOperationOutPeople) {
  addOperationOutPeople.forEach((element) => {
    element.addEventListener("click", () => {
      let elem = element.getAttribute("data-name");

      console.log(elem);
      modal(elem);
      FetchInfosubsPeople(element);
    });
  });
}

function FetchInfosubsPeople(element) {
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
          data.forEach((item) => {
            if(item.other != null){
                console.log(item)
            }

          });
        });
    });
}
