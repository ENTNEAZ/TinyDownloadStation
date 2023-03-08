function upload(){
    $('.progress > div').css('width', "0%");
    var file = document.getElementById('file').files[0];
    var formdata = new FormData();
    formdata.append("file", file);
    //提交文件名
    formdata.append("filename", file.name);
    var lastTime = 0;
    var lastSize = 0;
    $.ajax({
        url: "/upload",
        type: "POST",
        data: formdata,
        processData: false,
        contentType: false,
        xhr: function() {
            var xhr = new XMLHttpRequest();
            //使用XMLHttpRequest.upload监听上传过程，注册progress事件，打印回调函数中的event事件
            xhr.upload.addEventListener('progress', function (e) {
                var progressRate = (e.loaded / e.total) * 100 + '%';
                $('.progress > div').css('width', progressRate);

                var nowTime = new Date().getTime();
                var nowSize = e.loaded;
                var speed = (nowSize - lastSize) / (nowTime - lastTime) * 1000 / 1024;
                lastTime = nowTime;
                lastSize = nowSize;
                var speedStr = speed > 1024 ? (speed / 1024).toFixed(2) + 'MB/s' : speed.toFixed(2) + 'KB/s';
                $('.speed').text(speedStr);
                $(".rate").text((e.loaded / e.total).toFixed(2) * 100 + '%');
            })

            return xhr;
        },
        success: function (data) {
            alert("Upload success!");
        },
        error: function (data) {
            alert("Upload failed!");
        }
    });
}