function upload(){
    $('.progress > div').css('width', "0%");
    var file = document.getElementById('file').files[0];
    var formdata = new FormData();
    formdata.append("file", file);
    //提交文件名
    formdata.append("filename", file.name);
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
                console.log(e);
                //loaded代表上传了多少
                //total代表总数为多少
                var progressRate = (e.loaded / e.total) * 100 + '%';

                //通过设置进度条的宽度达到效果
                $('.progress > div').css('width', progressRate);
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