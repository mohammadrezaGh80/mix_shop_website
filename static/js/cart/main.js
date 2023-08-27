// increase and decrease number of product in cart
const plusIcon = document.getElementById("plus-icon")
const dashIcon = document.getElementById("dash-icon")
const inputNumber = document.getElementById("input-number")

plusIcon.addEventListener("click", function (event){
    inputNumber.value ++;
})

dashIcon.addEventListener("click", function (event){
    if(inputNumber.value - 1 !== 0){
        inputNumber.value --;
    }
})