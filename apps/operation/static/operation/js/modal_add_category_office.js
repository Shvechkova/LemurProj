
const addCategoryOperAccount = document.querySelectorAll(
  '[data-name="modal-add_category_oper_account"]'
);

if (addCategoryOperAccount) {
 
  addCategoryOperAccount.forEach((element) => {

    element.addEventListener("click", (event) => {

      const battonAdd = document.querySelector(".add_category_oper_account");

      let elem = element.getAttribute("data-name");
      const modalWindow = document.getElementById(elem);
     
   
      const inputNameCAtegoru = modalWindow.querySelector(
        ".modal_add_category_input"
      );
      inputNameCAtegoru.value = "";
        getCoords(event,elem)
      modal(elem, battonAdd);
   
      getTitleInfoCategory(modalWindow, element);
      addCategoryOperationFetch(battonAdd,element,modalWindow)
    //   modalWindow.addEventListener("input", () => {
    //     validateOtherInput(elem, ".add-category");
    //   });
    });
  });
}

// заполнение тайтла инфой
function getTitleInfoCategory(modalWindow, element) {
  let elementCat = element.getAttribute("data-cat");
  // const titleNameData = element.getAttribute("modal_title_category_data")
  const titleInput = modalWindow.querySelector(".modal_title_category_data");

  titleInput.innerHTML = `"${elementCat}"`;
}

// расположенеи модалки относительно кнопки клика 
function getCoords(event,elem) {
    console.log('Позиция x относительно документа', event.pageX)
    console.log('Позиция y относительно документа', event.pageY)
   const windowModal = document.getElementById(elem)
   const windowModalWrap = windowModal.querySelector(".modal-wrapper-individual")
  console.log(windowModalWrap)

   windowModalWrap.style.top=(event.pageY-20) + "px"
   windowModalWrap.style.left=(event.pageX-20)+ "px"
//    windowModalWrap.style.right=0 + "px"
   windowModalWrap.style.transform="none"
    
  }

function addCategoryOperationFetch(battonAdd,element,modalWindow){
    console.log(battonAdd)
    battonAdd.addEventListener("click", () => {
        const num_metacat = element.getAttribute("data-cat-numb")
        const inputNameCat = modalWindow.querySelector(".modal_add_category_input").value

        const form = new FormData();
        form.append("amount", sumChecked);
 
    })
}
