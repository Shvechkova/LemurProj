ShrinkEmployee()
function ShrinkEmployee(){
    const employee = document.querySelectorAll('.salary_employee_name')
    if (employee){
        employee.forEach((element)=>{
            let shrink = [];
    let shrinkElemToDate = {};
  
            element.addEventListener("click", () => {
                console.log(element)
                const itemShrinkName = element.getAttribute("data-created-btn");
                console.log(itemShrinkName)
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
                      elem.setAttribute("data-shrink", "flex");
                      element.setAttribute("data-btn-deg", "0");
                      element.setAttribute(`data-btn-deg-${dataShrinkItemType}`, "0");
                      let btndeg = "data-btn-deg-" + dataShrinkItemType;
          
                      shrinkElemToDate = {
                        date: dataCreatedShrink,
                        type: dataShrinkItemType,
                        "data-shrink": "flex",
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
        })
    }
}