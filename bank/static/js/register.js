$(function(){
	console.log("hello regis	");
	$("#registerBtn").click((event) => {
		event.preventDefault();
		console.log("what??");
		var md = forge.md.sha256.create();
        // the password should have strange word.
        md.update($("#password").val());
		var passwd_md = md.digest().toHex();
		console.log(passwd_md);
		$("#password").val(passwd_md);
		$('form').submit();
	})
})