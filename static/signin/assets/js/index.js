const signUpDiv = document.getElementById('signUp');
const signInDiv = document.getElementById('signIn');
const signInContent = document.getElementById('signInContent')
const signUpContent = document.getElementById('signUpContent')
const fieldUsername = document.getElementById('id_username')
const fieldPassword = document.getElementById('id_password')
const signInBtn = document.getElementById('signInBtn');
const remeberMeCheck = document.getElementById('remeberMeCheck')
let isSignInActive = true;
const defaultPageIsSignIn = true


remeberMeCheck.addEventListener('click', function() {
    if (remeberMeCheck.checked == true) {
        signInBtn.disabled = false;
    } else {
        signInBtn.disabled = true;

    }
})



function activateSignIn() {
    signInDiv.classList.add("bgColorBlue")
    signInDiv.classList.add("textColorWhite")
    signUpContent.style.display = "none";
    signInContent.style.display = "display";
}

function deactivateSignIn() {
    signInDiv.classList.remove("bgColorBlue")
    signInDiv.classList.remove("textColorWhite")
    signUpContent.style.display = "display";
    signInContent.style.display = "none";
}

function activateSignUp() {
    signUpDiv.classList.add("bgColorBlue")
    signUpDiv.classList.add("textColorWhite")
    signInContent.style.display = "none";
    signUpContent.style.display = "block";

}

function deactivateSignUp() {
    signUpDiv.classList.remove("bgColorBlue")
    signUpDiv.classList.remove("textColorWhite")
    signInContent.style.display = "block";
    signUpContent.style.display = "none";

}



document.addEventListener("DOMContentLoaded", function(event) {
    signInBtn.disabled = true;

    if (defaultPageIsSignIn === false) {
        deactivateSignIn();
        activateSignUp();
        isSignInActive = false;
    } else {
        activateSignIn();
        deactivateSignUp();
        isSignInActive = true;
    }


})

signInDiv.addEventListener('click', function() {
    window.location.href = "/sign-in"

    // if (isSignInActive) {} else {
    //     deactivateSignUp();
    //     activateSignIn();
    //     isSignInActive = true;
    // }

})

signUpDiv.addEventListener('click', function() {
    window.location.href = "/sign-up"
        // if (isSignInActive) {
        //     deactivateSignIn();
        //     activateSignUp();
        //     isSignInActive = false;
        // } else {
        //     activateSignUp();
        //     isSignInActive = true;

    // }
})