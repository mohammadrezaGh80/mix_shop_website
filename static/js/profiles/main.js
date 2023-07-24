const awaitingCommentRegisterButton = document.getElementById("nav-awaiting-comment-register-tab");
const myCommentsButton = document.getElementById("nav-my-comments-tab");
const buttons = Array(awaitingCommentRegisterButton, myCommentsButton);

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function (event) {
        buttons[i].className = "nav-link active text-danger";
        for (let btn of buttons){
            if(btn !== buttons[i]){
                btn.className = "nav-link text-secondary";
            }
        }
    })
}