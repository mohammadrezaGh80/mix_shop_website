const listPlusIcon = document.getElementsByClassName("plus-icon")
const listDashIcon = document.getElementsByClassName("dash-icon")

const closest = (to, selector) => {
    let currentElement = document.querySelector(to)
    let returnElement

    while (currentElement.parentNode && !returnElement) {
        currentElement = currentElement.parentNode
        returnElement = currentElement.querySelector(selector)
    }

    return returnElement
}


for (let plusIcon of listPlusIcon) {
    plusIcon.addEventListener("click", function (event) {
        closest(`#${plusIcon.id}`, '.input-number').value++;
    })
}

for (let minusIcon of listDashIcon) {
    minusIcon.addEventListener("click", function (event) {
        const numberInput = closest(`#${minusIcon.id}`, '.input-number');
        if (numberInput.value - 1 !== 0) {
            numberInput.value--;
        }
    })
}