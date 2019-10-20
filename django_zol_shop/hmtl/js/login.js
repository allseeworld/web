/**
 * Created by Administrator on 2016/9/14.
 */
$(function(){
    $(".linkparter ul li").eq(0).siblings().css("cursor","pointer")
});

$(function(){
    $("#enter").click(function() {
        var user = $("#user").val();
        var pwd = $("#pwd").val();
        $.post("http://10.20.159.194:8080/users/authorizations/",
            {
                username: user,
                password: pwd,
            },function (data) {
                        var users=[]
                        var user = {"user":data['user'], "pwd": $("#pwd").val(), "status": 1};
                        users.push(user);
                        $.cookie("users", JSON.stringify(users), {expires: 7, path: "/"});
                        document.cookie = 'token=' + data['token'] + "; expires=" + new Date(2020, 1, 1,)
                        document.cookie = 'user=' + data['user'] + "; expires=" + new Date(2020, 1, 1,)
                        document.cookie = 'user_id=' + data['user_id'] + "; expires=" + new Date(2020, 1, 1,)

                        window.location.href =  "index.html";
                return;
            });


        // var users = $.cookie("users") ? JSON.parse( $.cookie("users") ) : []
        //
        // for(var i = 0 ; i < users.length; i ++){
        //     if(users[i].user == user && users[i].pwd == pwd ){
        //         users[i].status = 1;
        //         $.cookie("users", JSON.stringify(users), {expires: 7, path: "/"});
        //         window.location.href =  "index.html";
        //         return;
        //     }
        // }
        alert("账号未注册 即将跳转注册界面");
        window.location.href = "register.html";


    })
});