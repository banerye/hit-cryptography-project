$(function(){
    console.log("hello?");
    $.ajax({
        type: "post",
        url: "/user/get_records/",
        data: {
            username: $("#username")[0].innerHTML
        },
        dataType: 'json',
        success: function(data){
            var context = "";
            for (var i = 0; i < data.outrecords.length; i++) {
                context += "<tr><td>" + data.outrecords[i].payee 
                + "</td><td>" + data.outrecords[i].account + " ￥" 
                + "</td><td>" + data.outrecords[i].time + "</td></tr>";
            }
            $("#outputRecord")[0].innerHTML = context;
            context = "";
            for (var i = 0; i < data.inrecords.length; i++) {
                context += "<tr><td>" + data.inrecords[i].payer 
                + "</td><td>" + data.inrecords[i].account + " ￥"
                + "</td><td>" + data.inrecords[i].time + "</td></tr>";
            }
            $("#inputRecord")[0].innerHTML = context;
        },
        error: function(data){
            console.log("connect error");
        }
    });

    $("#newPublickey").change(() => {
        $("#publickeyLabel")[0].innerHTML = JSON.stringify($("#newPublickey").val());
    })

    $("#uploadPublicKeyBtn").click((event) => {
        event.preventDefault();

        var publickeyFile = $("#newPublickey")[0].files[0];
        var reader = new FileReader(); 
        reader.readAsText(publickeyFile);
        reader.onload = function() {
            var publickey = this.result;
            console.log(publickey);
            $.ajax({
                type: "post",
                url: "/user/upload_publickey/",
                data: {
                    publickey: publickey
                },
                dataType: 'json',
                success: function(data){
                    console.log("upload sec");
                    $("#uploadAlert").removeAttr("hidden");
                },
                error: function(data){
                    console.log("connect error");
                }
            });
        }
        
    });
})