$(function() {
    var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9+/=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/rn/g,"n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}

//     var storePublicKeyPem = "-----BEGIN PUBLIC KEY-----\
// MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA30Mdr5GbwnuQqjbOL5mm\
// Qy3F7Q6sQDPuIl8JXJagJMyx99ICEk++kKmsflnxWDe1JUBAIux9CGp6jnk33G7N\
// C6S7/6VoQJI3hhuWwTtWXcTnasTer++qIjAARjEHFXPL/Y27RMD485Hdy9AMb9UK\
// SQWuZ1SR5IihvibdwkM7nMHvRIOi+NSw56EYdSc3fH3smHrhDcAjJSZAzffe11gQ\
// u+RbDkVAV3g7eMQARGKDWZ9lmRqCWxY7NMVtbXWyBfLBY96VFGUB/U181KiM8OLi\
// LCzcdYLRG1KRmwMIpoPbtlyqs5M+NxCarzPBZnW8BwBzkz6HYaYa1ZD981Tm6LNv\
// TwIDAQAB\
// -----END PUBLIC KEY-----"
    var storePublicKeyPem = "-----BEGIN PUBLIC KEY-----\
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAydENcOQXysHXbhu+fNhN\
F9lio5j8xR4Um02S1rm5aiFG+cIxvlChNSbhMk3ZlyVNDjw3rIsWiNRtifs+7NXP\
SpZwtc3HUPMw9rjg0ocycAk3FcSulotk9/7g8Xr9jxSq8+ppqpfPFFQ/3DyCtau0\
M0Smg59X8mzn+Gr/x+YHE6ZJ7XEptbbarluAQsVfxP3AVmzttkZ+lsry9T0p+BB8\
L6sXs2koCVf/6jqjOqTDjBq0E/cAyqizDjHsmpxvpC87cGMIIMAhh6V2nOOpVmtc\
pEesXlohkPMxECQZluvTsebQYzk4LSNxQDAMRQUvW1fyrOR+fMwev6XFV2IKiyxd\
0wIDAQAB\
-----END PUBLIC KEY-----";
    var storePublicKey = forge.pki.publicKeyFromPem(storePublicKeyPem);

    var bankPublicKeyPem = "-----BEGIN PUBLIC KEY-----\
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkXLAYu+vT/vcuXn5Mucq4Fl/rTvFV1VL6Eo15crLQ5CGvJBWkk5LxGyHnyrgxykdnhnqaJuKPezYP4SLfgpxlagQA8FavQJX5apWTQaLgEcIiDn8lLqUtrebwPM1IOQkIIWvP7vn32mZYTTT/7GK+KL+sHU/u8ZiqDK+zacOYrbmYlsx7PoXYOycWfPzhOmzXnp8YzNbYciPO7TcYDtHdytQR+tCwwGB07YuZZ4tFmBd0Vr+aqzW22CDg6GQJlt0Gu4Cj2kJFK0KCnzYzJjnwALQLRjCYs6Bxc6yufjoNfk6tUWl1z0EQ1MLvO8XyySzv0dr6XJurFZ+JztaFcTexwIDAQAB\
-----END PUBLIC KEY-----";
    var bankPublicKey = forge.pki.publicKeyFromPem(bankPublicKeyPem);

    $("#privatekey").change(() => {
        console.log('emm?');
        
        $("#privatekey")[0].innerHTML = JSON.stringify($("#privatekey").val());
        console.log($("#privatekey")[0].innerHTML);
    })

    $("#loadPrivateKeyBtn").click((event) => {
        event.preventDefault();

        console.log("hello");

        console.log("privatekey load..");
        var privatekeyFile = $("#privatekey")[0].files[0];
        var reader = new FileReader(); 
        reader.readAsText(privatekeyFile);
        reader.onload = function() {
            var privatekey = this.result;
            console.log(this.result);
            // $("#submitBtn").click();
            upload(privatekey);
        }
    })

    function upload(privatekey){
        // analyse aes private key
        console.log("submit Btn!", privatekey);
        var aes_passwd = $("#aesPasswd").val();
        console.log("aes_passwd: ", aes_passwd);

        var key = CryptoJS.enc.Utf8.parse(aes_passwd);
        var encryptedHexStr = CryptoJS.enc.Hex.parse(privatekey);
        var encryptedBase64Str = CryptoJS.enc.Base64.stringify(encryptedHexStr);

        var decryptedData = CryptoJS.AES.decrypt(encryptedBase64Str, key, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });

        var decryptedStr = decryptedData.toString(CryptoJS.enc.Utf8);

        // var ciphertext = CryptoJS.enc.Base64.parse(privatekey);
        // var iv = ciphertext.clone();
        // iv.sigBytes = 16;
        // iv.clamp();
        // ciphertext.words.splice(0, 4);
        // ciphertext.sigBytes -= 16;

        // var decrypted = CryptoJS.AES.decrypt({ciphertext: ciphertext}, key, {
        //     iv: iv
        // });
        // var decryptedStr = decrypted.toString(CryptoJS.enc.Utf8);

        //

        // ...
        var privateKey = forge.pki.privateKeyFromPem(decryptedStr);

        var pathName = window.location.pathname;
        let tmp_str = pathName.replace("/payment/detail/", "");
        var b64_ciphertext = tmp_str.substr(0, tmp_str.length - 1);

        var b_ciphertext = atob(decodeURIComponent(b64_ciphertext));

        var plaintext = privateKey.decrypt(b_ciphertext);
        var plainlst = plaintext.split('&&');

        var uri_oi = decodeURIComponent(plainlst[plainlst.length - 1]);
        var oi_lst = uri_oi.split("AAAAA");

        // return; 
        // create dual-sign
        var username = $("#username").val();
        var password = $("#password").val();

        var md = forge.md.sha256.create();
        md.update(password);
        var passwd_hash = md.digest().toHex();

        var PI = username + "AAA" + passwd_hash + "AAA" + plainlst[0] + "AAA" + plainlst[2] + "AAA" + oi_lst[0];
        var OI = uri_oi;
        
        var md = forge.md.sha256.create();
        md.update(Base64.encode(OI));
        OI_hash = md.digest().toHex();

        var md = forge.md.sha256.create();
        md.update(Base64.encode(PI));
        PI_hash = md.digest().toHex();

        var md = forge.md.sha256.create();
        md.update(OI_hash + PI_hash);
        OI_PI_hash = md.digest().toHex();

        var md = forge.md.sha256.create();
        md.update(OI_PI_hash)
        
        var signature = privateKey.sign(md);
        var DUAL_SIG = window.btoa(privateKey.sign(md));
        var b_dual_sig = atob(DUAL_SIG);
       
        var toStorePlaintext = encodeURIComponent(OI) + "&&" + PI_hash + "&&" + DUAL_SIG;
        var toBankPlaintext = encodeURIComponent(PI) + "&&" + OI_hash + "&&" + DUAL_SIG;

        
        // use aes them rsa
        var keyToBank = forge.random.getBytesSync(16);
        var ivToBank = forge.random.getBytesSync(16);

        var keyToStore = forge.random.getBytesSync(16);
        var ivToStore = forge.random.getBytesSync(16);

        var cipher = forge.cipher.createCipher('AES-CBC', keyToBank);
        cipher.start({iv: ivToBank});
        cipher.update(forge.util.createBuffer(toBankPlaintext));
        cipher.finish();
        var toBankCiphertext = cipher.output;


        var cipher = forge.cipher.createCipher('AES-CBC', keyToStore);
        cipher.start({iv: ivToStore});
        cipher.update(forge.util.createBuffer(toStorePlaintext));
        cipher.finish();
        var toStoreCiphertext = cipher.output;

        var encryptedKeyToBank = bankPublicKey.encrypt(keyToBank)
        var encryptedKeyToStore = storePublicKey.encrypt(keyToStore)


        var toSubmit = btoa(encryptedKeyToBank) + "&&" + btoa(ivToBank) + "&&" + toBankCiphertext.toHex()
        + "&&&" + btoa(encryptedKeyToStore) + "&&" + btoa(ivToStore) + "&&" + toStoreCiphertext.toHex();

        $.ajax({
            type: "post",
            url: '/payment/check/',  // function you want to use in python
            data: {
                data: toSubmit,
            },
            dataType: "json",
            success:function(data){
                window.close();
            },
            error:function(data){
                $("#loadFailAlert").removeAttr("hidden");
            }
        });
    }
})