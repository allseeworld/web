/**
 * Created by Administrator on 2016/9/14.
 */
//手机号验证
$(function () {
    $("#phone").blur(function () {
        var reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!reg.test($(this).val())) {
            $(this).next("i").html("邮箱格式不对");
        } else {

            $(this).next("i").html("");
        }

    });
})

$(function () {
    $("#pwdc").blur(function () {
        var last = $("#pwd").val();
        var now = $(this).val();
        if (last == now) {
            $(this).next("i").html("密码一致");
        } else {
            $(this).next("i").html("密码不一致");
            $(this).val("");
            $("#pwd").val("");
        }
    })
});

//验证码
$(function () {
    $(".code").html(Random());
    $("#register").click(function () {
        var email = $("#phone").val()
        console.log('em' + email)
        var users = []
        $.get('http://10.20.159.194:8080/users/verify/', {'email': email}, function (data) {
            users = data;
            console.log("dddd"+data)
        })
        console.log("sss"+users)
        if (users==[]) {

            alert("已注册，请直接登录");

            return;

        }
        var reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

        if (!reg.test($("#phone").val())) {
            alert("邮箱格式不对");
            return
        }

        if ($("#phone").val().length <= 0) {
            alert("邮箱不能为空");
            return;
        }
        if ($("#pwd").val().length <= 0) {
            alert("密码不能为空");
            return;
        }
        if (!($("#pwd").val() == $("#pwdc").val())) {
            alert("两次密码输入不一致");
            return;
        }

        // if (!($(".sure").val() == $(".code").html())) {
        //     $(".code").html(Random());
        //     alert("验证码错误")
        //     return;
        // }
        for (var p = 0; p < users.length; p++) {
            users[p].status = 0;
        }
        var user = {"user": $("#phone").val(), "pwd": $("#pwd").val(), "status": 1};
        $.post("http://10.20.159.194:8080/users/register/",user, function (data) {
                alert(data['code'])
                if (data['code'] == "200") {
                    // users.push(user);
                    // $.cookie("users", JSON.stringify(users), {expires: 7, path: "/"});
                    alert("注册成功。。。即将跳转,请从邮箱激活账户");
                    window.location.href = "login.html";
                } else {
                    alert("注册失败")
                    return;
                }
            });
    });

        function Random() {
            var str = "";
            for (var i = 0; i < 4; i++) {
                var a = parseInt(Math.random() * 10)
                str += a;
            }
            return str;
        }

});
