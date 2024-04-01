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
    let shrink = [];
    let shrinkElemToDate = {};
    element.addEventListener("click", () => {
      const itemShrinkName = element.getAttribute("data-created-btn");
      const itemShrink = document.querySelectorAll(
        `[data-created='${itemShrinkName}']`
      );
      const dataShrinkType = element.getAttribute("data-btn-type-shrink");

      const dateShrinkElem = {};

      itemShrink.forEach((elem) => {
        const dataCreatedShrink = elem.getAttribute("data-created");
        const dataShrink = elem.getAttribute("data-shrink");
        const dataShrinkItemType = elem.getAttribute("data-type-shrink");

        if (
          dataShrinkType == dataShrinkItemType &&
          dataCreatedShrink == itemShrinkName
        ) {
          if (dataShrink === "none") {
            elem.setAttribute("data-shrink", "block");
            element.setAttribute("data-btn-deg", "0");
            element.setAttribute(`data-btn-deg-${dataShrinkItemType}`, "0");
            let btndeg = "data-btn-deg-" + dataShrinkItemType;

            shrinkElemToDate = {
              date: dataCreatedShrink,
              type: dataShrinkItemType,
              "data-shrink": "block",
              btndeg: 0,
            };
          } else {
            elem.setAttribute("data-shrink", "none");
            element.setAttribute(`data-btn-deg-${dataShrinkItemType}`, "180");

            let btndeg = "data-btn-deg-" + dataShrinkItemType;

            shrinkElemToDate = {
              date: dataCreatedShrink,
              type: dataShrinkItemType,
              datashrink: "none",
              btndeg: 180,
            };
          }
        }
      });

      var oldSheink = localStorage.getItem("shrinks");
      const oldSheinkPars = JSON.parse(oldSheink);

      if (oldSheink) {
        const lenghtold = Object.keys(oldSheinkPars).length;
        e = 0;
        oldSheinkPars.forEach((elem, i) => {
          e++;
          if (
            elem.date == shrinkElemToDate.date &&
            elem.type == shrinkElemToDate.type
          ) {
            oldSheinkPars[i] = shrinkElemToDate;
          } else {
            if (e === lenghtold) {
              oldSheinkPars.push(shrinkElemToDate);
            }
          }
        });

        localStorage.setItem("shrinks", JSON.stringify(oldSheinkPars));
      } else {
        shrink.push(shrinkElemToDate);
        localStorage.setItem("shrinks", JSON.stringify(shrink));
      }
    });
  });
}

// установка значений скрытия раскрытия из локалсторадж
getStateLocalStorage();
function getStateLocalStorage() {
  var dataShrink = localStorage.getItem("shrinks");

  if (dataShrink) {

    const typeItemShrink = document.querySelectorAll("[data-type-shrink]");
    const oldSheinkPars = JSON.parse(dataShrink);
    oldSheinkPars.forEach((elem, i) => {
      const itemShrink = document.querySelectorAll(
        `[data-created='${elem.date}']`
      );
      itemShrink.forEach((el) => {
        const elemAttrTupe = el.getAttribute("data-type-shrink");
        if (elemAttrTupe == elem.type) {
          el.setAttribute("data-shrink", elem.datashrink);
        }
      });

      const btnShrink = document.querySelectorAll(
        `[data-created-btn='${elem.date}']`
      );
      btnShrink.forEach((el) => {
        const elemAttrTupe = el.getAttribute("data-btn-type-shrink");
        if (elemAttrTupe == elem.type) {
          el.setAttribute("data-btn-deg-suborder", elem.btndeg);
        }
      });

     
    });
  }
 
}

//новый месяц кнопка
const newBillMonth = document.querySelector(".new_month");
if (newBillMonth) {
  newBillMonth.addEventListener("click", () => {
   

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
      const setItem = item.getAttribute("data-sort-operation");
      const oldSortClient = sessionStorage.getItem("sortOper");
      if(oldSortClient == setItem){
        sessionStorage.setItem("sortOper" , "0");
       document.cookie = "sortOper= 0";
     }else{
       const operDate = item.getAttribute("data-sort-operation");
      sortOper.setAttribute("data-sort-operation", operDate);

      sessionStorage.setItem("sortOper", operDate);
      document.cookie = "sortOper=" + operDate;
     }
     
     
      location.reload();
    });

    const indexBtnOper = sortOper.getAttribute("bill-sorting-oper");
    const operDate = item.getAttribute("data-sort-operation");
    if (indexBtnOper == operDate) {
      item.classList.add("active_sorting_oper");
    }
  });
}
