
// // установка скрытия раскрытия блока в зависмости от даты клика кнопки
// const shrinkItem = document.querySelectorAll(".btn_month_bill-shrink");
// if (shrinkItem) {
//   shrinkItem.forEach((element, i) => {
//     element.addEventListener("click", () => {
//       const itemShrinkName = element.getAttribute("data-created-btn");
//       const itemShrink = document.querySelectorAll(
//         `[data-created='${itemShrinkName}']`
//       );
//       const dataShrinkType = element.getAttribute("data-btn-type-shrink");

//       itemShrink.forEach((elem) => {
//         const dataShrink = elem.getAttribute("data-shrink");
//         const dataShrinkItemType = elem.getAttribute("data-type-shrink");

//         if (dataShrinkType == dataShrinkItemType) {
//           if (dataShrink === "none") {
//             elem.setAttribute("data-shrink", "block");
//             element.setAttribute("data-btn-deg", "0");
//             element.setAttribute(`data-btn-deg-${dataShrinkItemType}`, "0");

//             sessionStorage.setItem(dataShrinkItemType, "block");
//             sessionStorage.setItem("stateShrink", "block");
//             sessionStorage.setItem("elemShrink", itemShrinkName);
//             sessionStorage.setItem(`data-btn-deg-${dataShrinkItemType}`, "0");
//           } else {
//             elem.setAttribute("data-shrink", "none");
//             element.setAttribute(`data-btn-deg-${dataShrinkItemType}`, "180");

//             sessionStorage.setItem(dataShrinkItemType, "none");
//             sessionStorage.setItem("stateShrink", "none");
//             sessionStorage.setItem("elemShrink", itemShrinkName);
//             sessionStorage.setItem(`data-btn-deg-${dataShrinkItemType}`, "180");
//           }
//         }
//       });
//     });
//   });
// }

// // установка значений скрытия раскрытия из локалсторадж
// getStateLocalStorage();
// function getStateLocalStorage() {
//   var datastateShrink = sessionStorage.getItem("stateShrink");
//   var dataelemShrink = sessionStorage.getItem("elemShrink");
//   var dataBtnsuborder = sessionStorage.getItem("data-btn-deg-suborder");
//   var databtndegentry = sessionStorage.getItem("data-btn-deg-entry");
//   var databtndegout = sessionStorage.getItem("data-btn-deg-out");
//   var entry = sessionStorage.getItem("entry");
//   var suborder = sessionStorage.getItem("suborder");
//   var out = sessionStorage.getItem("out");

//   const itemShrink = document.querySelectorAll(
//     `[data-created='${dataelemShrink}']`
//   );

//   const btnType = document.querySelectorAll(".btn_month_bill-shrink");
//   btnType.forEach((element) => {
//     const btnTypeEntry = element.getAttribute("data-btn-type-shrink");

//     if (btnTypeEntry === "entry" && databtndegentry != null) {
//       element.setAttribute("data-btn-deg-entry", databtndegentry);
//     }
//     if (btnTypeEntry === "suborder" && dataBtnsuborder != null) {
//       element.setAttribute("data-btn-deg-suborder", dataBtnsuborder);
//     }
//     if (btnTypeEntry === "out" && databtndegout != null) {
//       element.setAttribute("data-btn-deg-out", databtndegout);
//     }
//   });

//   itemShrink.forEach((elem) => {
//     const dataI = elem.getAttribute("data-type-shrink");

//     if (dataI === "entry" && entry != null) {
//       elem.setAttribute("data-shrink", entry);
//     }
//     if (dataI === "suborder" && suborder != null) {
//       elem.setAttribute("data-shrink", suborder);
//     }
//     if (dataI === "out" && out != null) {
//       elem.setAttribute("data-shrink", out);
//     }
//   });
// }


// установка скрытия раскрытия блока в зависмости от даты клика кнопки
const shrinkItem = document.querySelectorAll(".btn_month_bill-shrink");
if (shrinkItem) {
  shrinkItem.forEach((element, i) => {
    element.addEventListener("click", () => {
      const itemShrinkName = element.getAttribute("data-created-btn");
      const itemShrink = document.querySelectorAll(
        `[data-created='${itemShrinkName}']`
      );
      const dataShrinkType = element.getAttribute("data-btn-type-shrink");

      itemShrink.forEach((elem) => {
        const dataShrink = elem.getAttribute("data-shrink");
        const dataShrinkItemType = elem.getAttribute("data-type-shrink");

        if (dataShrinkType == dataShrinkItemType) {
          if (dataShrink === "none") {
            elem.setAttribute("data-shrink", "block");
            element.setAttribute("data-btn-deg", "0");
            element.setAttribute(`data-btn-deg-${dataShrinkItemType}`, "0");

            sessionStorage.setItem(dataShrinkItemType, "block");
            sessionStorage.setItem("stateShrink", "block");
            sessionStorage.setItem("elemShrink", itemShrinkName);
            sessionStorage.setItem(`data-btn-deg-${dataShrinkItemType}`, "0");
          } else {
            elem.setAttribute("data-shrink", "none");
            element.setAttribute(`data-btn-deg-${dataShrinkItemType}`, "180");

            sessionStorage.setItem(dataShrinkItemType, "none");
            sessionStorage.setItem("stateShrink", "none");
            sessionStorage.setItem("elemShrink", itemShrinkName);
            sessionStorage.setItem(`data-btn-deg-${dataShrinkItemType}`, "180");
          }
        }
      });
    });
  });
}

// установка значений скрытия раскрытия из локалсторадж
getStateLocalStorage();
function getStateLocalStorage() {
  var datastateShrink = sessionStorage.getItem("stateShrink");
  var dataelemShrink = sessionStorage.getItem("elemShrink");
  var dataBtnsuborder = sessionStorage.getItem("data-btn-deg-suborder");
  var databtndegentry = sessionStorage.getItem("data-btn-deg-entry");
  var databtndegout = sessionStorage.getItem("data-btn-deg-out");
  var entry = sessionStorage.getItem("entry");
  var suborder = sessionStorage.getItem("suborder");
  var out = sessionStorage.getItem("out");

  const itemShrink = document.querySelectorAll(
    `[data-created='${dataelemShrink}']`
  );

  const btnType = document.querySelectorAll(".btn_month_bill-shrink");
  btnType.forEach((element) => {
    const btnTypeEntry = element.getAttribute("data-btn-type-shrink");

    if (btnTypeEntry === "entry" && databtndegentry != null) {
      element.setAttribute("data-btn-deg-entry", databtndegentry);
    }
    if (btnTypeEntry === "suborder" && dataBtnsuborder != null) {
      element.setAttribute("data-btn-deg-suborder", dataBtnsuborder);
    }
    if (btnTypeEntry === "out" && databtndegout != null) {
      element.setAttribute("data-btn-deg-out", databtndegout);
    }
  });

  itemShrink.forEach((elem) => {
    const dataI = elem.getAttribute("data-type-shrink");

    if (dataI === "entry" && entry != null) {
      elem.setAttribute("data-shrink", entry);
    }
    if (dataI === "suborder" && suborder != null) {
      elem.setAttribute("data-shrink", suborder);
    }
    if (dataI === "out" && out != null) {
      elem.setAttribute("data-shrink", out);
    }
  });
}


//новый месяц кнопка
const newBillMonth = document.querySelector(".new_month");
if (newBillMonth) {
  newBillMonth.addEventListener("click", () => {
    console.log(window.location.origin);

    location.href = window.location.origin + "/service/new_month";
    window.history.back();
  });
}

// установка сортировки месяца
const sortDate = document.querySelector(".bill-sorting-date");
if (sortDate) {
  const sortMonthReload = sessionStorage.getItem("sortMonth");
  if (sortMonthReload) {
    sortDate.setAttribute("bill-sorting-date", sortMonthReload);
  }

  const btnSort = document.querySelectorAll(".btn_sorting_month");

  btnSort.forEach((item) => {
    console.log(item);
    item.addEventListener("click", () => {
      const monthDate = item.getAttribute("data-sort-month");
      sortDate.setAttribute("data-sort-month", monthDate);
      sessionStorage.setItem("sortMonth", monthDate);
      document.cookie = "sortMonth=" + monthDate;
      location.reload();
    });

    const indexBtn = sortDate.getAttribute("bill-sorting-date");
    const monthDate = item.getAttribute("data-sort-month");
    if (indexBtn == monthDate) {
      console.log(item);
      item.classList.add("active_sorting");
    }
  });
}

// // установка сортировки operation
const sortOper = document.querySelector(".bill-sorting-operation");
if (sortOper) {
  const sortOperReload = sessionStorage.getItem("sortOper");
  const btnSortOper = document.querySelectorAll(".btn_sorting_operation");

  if (sortOperReload) {
    sortOper.setAttribute("bill-sorting-oper", sortOperReload);
  } else {
    document.cookie = "sortOper=" + "0";
    sortOper.setAttribute("bill-sorting-oper", "0");
    btnSortOper.forEach((item) => {
      item.classList.remove("active_sorting_oper");
    });
  }

  btnSortOper.forEach((item) => {
    item.addEventListener("click", () => {
      const operDate = item.getAttribute("data-sort-operation");
      sortOper.setAttribute("data-sort-operation", operDate);

      sessionStorage.setItem("sortOper", operDate);
      document.cookie = "sortOper=" + operDate;
      location.reload();
    });

    const indexBtnOper = sortOper.getAttribute("bill-sorting-oper");
    const operDate = item.getAttribute("data-sort-operation");
    if (indexBtnOper == operDate) {
      item.classList.add("active_sorting_oper");
    }
  });
}
