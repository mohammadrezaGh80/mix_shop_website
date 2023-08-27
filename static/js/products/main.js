const listCommentLikeButton = document.getElementsByClassName("comment-like-button")
const listCommentDislikeButton = document.getElementsByClassName("comment-dislike-button")
const listAnswerLikeButton = document.getElementsByClassName("answer-like-button")
const listAnswerDislikeButton = document.getElementsByClassName("answer-dislike-button")
const likeButton = Array.from(listCommentLikeButton).concat(Array.from(listAnswerLikeButton))
const dislikeButton = Array.from(listCommentDislikeButton).concat(Array.from(listAnswerDislikeButton))
const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value

for(let btn of likeButton){
    btn.addEventListener("click", function (event){
        event.preventDefault();
        let url = btn.parentElement.action;
        let formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrfToken)
        axios.post(url, formData).then(res => {
            let countLikesElement = this.parentElement.previousElementSibling;
            let iconLike = this.querySelector(".bi");
            if(res.data["status"] ===  "liked"){
                countLikesElement.innerHTML = `${+countLikesElement.innerHTML + 1}`;
                iconLike.className = "bi bi-hand-thumbs-up-fill";
            }else if(res.data["status"] ===  "retake_liked"){
                countLikesElement.innerHTML = `${+countLikesElement.innerHTML - 1}`;
                iconLike.className = "bi bi-hand-thumbs-up";
            }
        }).catch(err => {
            console.log(err)
        })
    })
}

for(let btn of dislikeButton){
    btn.addEventListener("click", function (event){
        event.preventDefault();
        let url = btn.parentElement.action;
        let formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrfToken)
        axios.post(url, formData).then(res => {
            let countDislikesElement = this.parentElement.previousElementSibling;
            let iconDislike = this.querySelector(".bi");
            if(res.data["status"] ===  "disliked"){
                countDislikesElement.innerHTML = `${+countDislikesElement.innerHTML + 1}`;
                iconDislike.className = "bi bi-hand-thumbs-down-fill";
            }else if(res.data["status"] ===  "retake_disliked"){
                countDislikesElement.innerHTML = `${+countDislikesElement.innerHTML - 1}`;
                iconDislike.className = "bi bi-hand-thumbs-down";
            }
        }).catch(err => {
            console.log(err)
        })
    })
}

const textQuestion = document.getElementById("id_text_question")
const textAnswer = document.getElementById("id_text_answer")
const questionButton = document.getElementById("question_button")
const answerButton = document.getElementById("answer_button")
const lengthTextQuestion = document.getElementById("length_text_question")
const lengthTextAnswer = document.getElementById("length_text_answer")

textQuestion.addEventListener("input", function (event){
    const lengthText = textQuestion.value.length;
    questionButton.disabled = lengthText < 7 || lengthText > 100;
    lengthTextQuestion.textContent = `100/${lengthText}`
})

if(textAnswer){
    textAnswer.addEventListener("input", function (event){
        const lengthText = textAnswer.value.length;
        answerButton.disabled = lengthText < 7 || lengthText > 500;
        lengthTextAnswer.textContent = `500/${lengthText}`
    })
}
