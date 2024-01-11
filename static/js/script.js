
let signInBtn = document.getElementById("signInBtn")


signInBtn.addEventListener("click", (e) => {
    let email = document.getElementById("email")
    let emailValue = email.value
    let emailCheck = emailValue.indexOf('@');
    let afterAtSymbol = emailCheck !== -1 ? emailValue.substring(emailCheck + 1, emailCheck + 4) : '';
    let studentId = document.getElementById("studentId")
    let pw = document.getElementById("pw")
    let pwLen = pw.value
    if(!afterAtSymbol.includes('sdh')) {
        alert("서울디지텍고등학교 전용 이메일이여야 합니다.")
        e.preventDefault();
    }else if(pwLen.length < 8){
        alert("비밀번호는 8글자 이상이여야 합니다.")
        e.preventDefault();
    }else if(studentId.value < 10101 || studentId.value > 30420){
        alert("학번을 확인해주세요.")
        e.preventDefault();
    }
})

