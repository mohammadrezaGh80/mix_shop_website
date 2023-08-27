const passwordInput = document.getElementById("id_password");
const toggleEyeLabel = document.getElementById("toggle_eye_label_password");
const checkboxInput = document.getElementById("id_checkbox_password");

toggleEyeLabel.addEventListener("click", function (event){
    if(!checkboxInput.checked){
        toggleEyeLabel.querySelector("i").className = "bi bi-eye-fill";
        passwordInput.type = "text";
    }else{
        toggleEyeLabel.querySelector("i").className  = "bi bi-eye-slash-fill";
        passwordInput.type = "password";
    }
})