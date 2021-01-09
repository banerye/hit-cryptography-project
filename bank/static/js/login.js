$(function () {
    $("#submit_btn").click(function(e){
        e.preventDefault();
        var md = forge.md.sha256.create();
        // the password should have strange word.
        md.update($("#password").val());
        var passwd_md = md.digest().toHex();
        console.log('pass_md: ', passwd_md);
        var toCipher = $("#username").val() + "&" + passwd_md;

        console.log("toCipher: ", toCipher);

        var cipherForm = document.createElement("form");
        cipherForm.method = "post";
        cipherForm.action = $("form").attr("action");
        // cipherForm.action = ""
        
        var cipherElem = document.createElement("input");
        cipherElem.type = "hidden";
        cipherElem.name = "ciphertext";
        cipherElem.value = encryptToBase64(toCipher);

        console.log("cipherElem.value: " + cipherElem.value);

        cipherForm.appendChild(cipherElem);

        document.body.appendChild(cipherForm);
        cipherForm.submit();
    })
})