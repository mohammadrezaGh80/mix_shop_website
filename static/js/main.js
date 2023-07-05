const listCommentLikeButton = document.getElementsByClassName("comment-like-button")
const listCommentDislikeButton = document.getElementsByClassName("comment-dislike-button")
const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value

for(let btn of listCommentLikeButton){
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


for(let btn of listCommentDislikeButton){
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