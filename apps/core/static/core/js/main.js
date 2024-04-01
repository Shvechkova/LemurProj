window.onload = function () {
  document.body.classList.add("loaded_hiding");
  window.setTimeout(function () {
    document.body.classList.add("loaded");
    document.body.classList.remove("loaded_hiding");
  }, 100);
};

// прелоадер для модалки
isLoading = false;
isLoaded = true;
function preloaderModal(isLoading, isLoaded) {
  if (isLoading == true) {
    // window.setTimeout(function () {
    //   document.body.classList.add("loaded_hiding");
    // document.body.classList.remove("loaded");
    // const preloader = document.querySelector(".preloader");
    // preloader.style.opacity = "1";
    // }, 500);

    document.body.classList.add("loaded_hiding");
    document.body.classList.remove("loaded");
    const preloader = document.querySelector(".preloader");
    preloader.style.opacity = "1";
  }
  if (isLoaded == true) {
    document.body.classList.remove("loaded_hiding");
    document.body.classList.add("loaded");
    const preloader = document.querySelector(".preloader");
    preloader.style.opacity = "0";
  }
}
preloaderModal(isLoading, isLoaded);

function modal(elem, buttonAdd) {
  const modal_windows = document.getElementById(elem);
  modal_windows.classList.add("modal-active");

  const nameclose = "." + "modal_close" + "_" + elem + "";
 
  //  закрытие по общему контейнеру
  let modalWrapper = document.querySelector(".modal-wrapper");
  let modalWrapperWind = document.querySelector(".modal-items");
 

  modal_windows.addEventListener("click", (event) => {
   

     let modalWrapperWind = document.querySelector(".modal-items");
 
    let modalSelect = modal_windows.querySelectorAll(".modal-select");
    let modalSelectWrap = modal_windows.querySelector("#modal-select");
  
 

      if (event.target == modal_windows && event.target != modalWrapper && event.isTrusted == true  ) {

        modal_windows.classList.remove("modal-active");
        modal_windows.replaceWith(modal_windows.cloneNode(true));
      }
  });
  let modalCloseAll = document.querySelector(nameclose);

  modalCloseAll.addEventListener("click", (event) => {
    modal_windows.classList.remove("modal-active");

    buttonAdd.replaceWith(buttonAdd.cloneNode(true));
  });
}

// функции завершения модального окна
function alertSuccess(element) {
  const wrap = element.querySelector(".modal-items")
  wrap.style.padding = "100px"
  element.querySelector(".modal-items-wrap").innerHTML = "Успех";
}
function alertError(element) {
  element.querySelector(".modal-items-wrap").innerHTML = "Неудача, повторите";
}

// получение куки с срфс токен
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

// валидация без радио кнопок
function validate(elem, btn) {
  const modalWindows = document.getElementById(elem);
  const allInputModal = modalWindows.querySelectorAll("input");
  const allSelectModal = modalWindows.querySelectorAll("select");
  
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

// валидация без радио кнопок для кнопки ок дающаяя сохранить форму
function validateBtn(elem, btn) {
  const modalWindows = document.getElementById(elem);
 
  const add_contract = document.querySelector(btn);
  const elemParent = add_contract.parentElement

  const allInputModal = elemParent.querySelectorAll("input");
  const allSelectModal = elemParent.querySelectorAll("select");

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

// валидация если есть радио кнопок
function validateRadio(elem, btn, wrapOne, wrapTwo) {
  const modalWindows = document.getElementById(elem);
  const wrapOneElem = document.querySelector(wrapOne);
  const wrapTwoElem = document.querySelector(wrapTwo);
  const allInputModalOne = wrapOneElem.querySelectorAll("input[type='radio']");
  const allInputModalTwo = wrapTwoElem.querySelectorAll("input[type='radio']");

  const add_contract = document.querySelector(btn);
  let inputYes;
  let inputYesTwo;
  let validateClass = false;
  allInputModalOne.forEach((elInput) => {
    if (elInput.checked == false) {
      add_contract.disabled = true;
    } else {
      add_contract.disabled = false;
      inputYes = true;
    }
  });

  allInputModalTwo.forEach((elInput) => {
    if (elInput.checked == false) {
      add_contract.disabled = true;
    } else {
      add_contract.disabled = false;
      inputYesTwo = true;
    }
  });
  if (inputYes && inputYesTwo) {
    validateClass = true;
    add_contract.disabled = false;
  }
  return validateClass;
}



// класс конструктор инпутов
class Input {
  constructor(type, className, value, placeholder, readonly, dataname) {
    this.elem = document.createElement("input");
    if (type) this.elem.type = type;
    if (className) this.elem.className = className;
    if (value) this.elem.value = value;
    if (placeholder) this.elem.placeholder = placeholder;
    if (readonly == true) this.elem.readOnly = true;
    if (dataname) this.elem.setAttribute("data-id", dataname);
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

function ChekinOtherSum(inputOtherSum, radioOtherSum) {
  const chekinOtherSum = document.getElementById(inputOtherSum);
  chekinOtherSum.addEventListener("input", () => {
    const chekinOtherSum = document.getElementById(radioOtherSum);
    chekinOtherSum.checked = true;
  });
}
