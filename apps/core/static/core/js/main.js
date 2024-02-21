// const opetaionEntryEmpty = document.querySelectorAll(".operation_entry_bank")

// if(opetaionEntryEmpty){
//   opetaionEntryEmpty.forEach((item)=>{
//     console.log(item.firstChild)
//     console.log(item.childNodes(".operation_entry_bank_true"))

//   })
// }

function modal(elem, buttonAdd) {
  const modal_windows = document.getElementById(elem);
  modal_windows.classList.add("modal-active");

  const nameclose = "." + "modal_close" + "_" + elem + "";
  console.log(nameclose);
  // let modalClose = document.querySelector(".modal_close");
  // modalClose.addEventListener("click", (event) => {
  //   modal_windows.classList.remove("modal-active");
  //   return false;
  // });

  let modalCloseAll = document.querySelector(nameclose);
  console.log(modalCloseAll);
  modalCloseAll.addEventListener("click", (event) => {
    modal_windows.classList.remove("modal-active");

    buttonAdd.replaceWith(buttonAdd.cloneNode(true));
  });
}

// }
function alertSuccess(element) {
  element.querySelector(".modal-items-wrap").innerHTML = "Успех";
}
function alertError(element) {
  element.querySelector(".modal-items-wrap").innerHTML = "Неудача, повторите";
}

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

function validate(elem, btn) {
  const modalWindows = document.getElementById(elem);
  const allInputModal = modalWindows.querySelectorAll("input");
  const allSelectModal = modalWindows.querySelectorAll("select");
  // console.log(allInputModal)
  const add_contract = document.querySelector(btn);
  let inputYes;
  let selectYes;
  let validateClass = false;
  allInputModal.forEach((elInput) => {
    if (elInput.value == "") {
      const c = elInput.getAttribute("data-validate");
      if (c == 0) {
        add_contract.disabled = false;
        inputYes = true;
      } else {
        add_contract.disabled = true;

        throw false;
      }
    } else {
      add_contract.disabled = false;
      inputYes = true;
    }
  });

  allSelectModal.forEach((elSelect) => {
    const elSelectChecked = elSelect.options[elSelect.selectedIndex].value;
    if (elSelectChecked == 0 || elSelectChecked == "") {
      add_contract.disabled = true;
      throw false;
    } else {
      add_contract.disabled = false;
      selectYes = true;
    }
  });

  if (selectYes || selectYes) {
    validateClass = true;
  }

  return validateClass;
}

// function openLoginModal() {
//   // открытие модалки
//   const modalLogin = document.getElementById("modal-login");
//   const modalBack = document.querySelector(".modal-section");
//   modalBack.classList.add("modal-section--active");
//   document.body.style.overflow = "hidden";
//   const timerId = setTimeout(() => {
//     modalLogin.classList.add("modal--active");
//   }, 200);
//   // закрытие модалки
//   let modalCloseLogin = document.querySelector(".modal-content__close__login");
//   modalCloseLogin.addEventListener("click", (event) => {
//     modalLogin.classList.remove("modal--active");
//     modalBack.classList.remove("modal-section--active");
//     document.body.style.overflow = "";
//   });
//   //закрытие по общему контейнеру
//   let modalWrapperLogin = document.querySelector(".modal-wrapper-login");
//   let modalContentWrapperLogin = document.querySelector(
//     ".modal-content-wrap-login"
//   );
//   let modalContentLogin = document.querySelector(".modal-content-login");
//   modalWrapperLogin.addEventListener("click", (event) => {
//     if (event.target == modalContentLogin || !modalContentWrapperLogin) {
//       modalLogin.classList.remove("modal--active");
//       modalBack.classList.remove("modal-section--active");
//       document.body.style.overflow = "";
//     }
//   });
// }

// класс конструктор инпутов
class Input {
  constructor(type, className, value, placeholder,readonly,dataname) {
    this.elem = document.createElement("input");
    if (type) this.elem.type = type;
    if (className) this.elem.className = className;
    if (value) this.elem.value = value;
    if (placeholder) this.elem.placeholder = placeholder;
    if(readonly == true) this.elem.readOnly = true;
    if(dataname ) this.elem.setAttribute("data-id", dataname)  
  }

  appendTo(parent) {
    parent.append(this.elem);
  }

  afterTo(parent) {
    parent.after(this.elem);
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

// чекин окна другой сумы НЕ РАБОТАЕТ

function ChekinOtherSum(inputOtherSum,radioOtherSum) {
  const chekinOtherSum = document.getElementById(inputOtherSum);
  chekinOtherSum.addEventListener("input", () => {
    const chekinOtherSum = document.getElementById(radioOtherSum);
    chekinOtherSum.checked = true;
  });
}
