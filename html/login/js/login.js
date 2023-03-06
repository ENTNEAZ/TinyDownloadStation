function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var data = "username=" + username + "&hashPassword=" + generateHash(password);
    window.location.href = "https://download.dragon.hotdoge.cn/api/login?" + data;
}

function generateHash(password) {
    password =  password + "saltysalt";
    var hash = 0;
    if (password.length == 0) return hash;
    for (i = 0; i < password.length; i++) {
        char = password.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
        ret = md5(hash + "NaCl");
    }

    return ret;
}