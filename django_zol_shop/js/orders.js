/**
 * Created by Administrator on 2016/9/16.
 */
$(function(){
    var users = $.cookie("users") ? JSON.parse( $.cookie("users") ) : [];
    var usersgood = $.cookie("usersgood") ? JSON.parse( $.cookie("usersgood") ) : [];
    function shopinfto(data) {
        // $.post()
        console.log(data)
    }
    var user = "";
    var orders_id=0
    for(var r=0 ; r<users.length ; r++){
        if(users[r].status == 1){
            user = users[r].user;
        }
    }
    users = user;
    //读取cookie中买家购买的物品(最后一个登录的买家) status为1的顾客

    for(var i=0 ; i<1 ; i++){
        (function(index) {
            //拿到data中的数据，并显示
            if(users == usersgood[index].user){
                var data = usersgood[index].data;
                for(var x=0 ;x<1 ; x++){
                    (function(z) {
                        var id = data[z].id;
                        //转换num类型
                        var num = data[z].num *1;
                        var color = data[z].color;
                        var suit = data[z].suit;
                        //JSON
                        $.get("http://127.0.0.1:8080/shop_pay/order?user_id="+$.cookie('user_id'),function(respond) {
                                orders_id=respond['order_code']
                                // ids = id
                                console.log(orders_id)
                                // if(id == respond[j].id){

                                    //a,span,div字符串
                                    // var total = parseInt(respond[j].price)*num;
                                    // var a ="<a href='goodsdetail.html?"+  respond[j].id +"'><img src="+ respond[j].goodimg.small[0].img +"></a>"
                                    // var span = "<span>【顺丰包邮s】" + respond[j].a+"</span>"
                                    // var div ="<div class='color-suit'><dl class='color'><dt>颜色</dt><dd>"+  color   + "</dd></dl><dl class='suit'><dt>套装:</dt><dd>" + suit + "</dd></dl> </div>"
                                    // var chose =$("<td><input class='shop' id="+ respond[j].id+" type='checkbox'></td>");
                                    var td1 = $("<td class='cell1'><div class='goods-info'>"+ respond['order_code']+"</div></td>");
                                    var td2 = $("<td class='cell2'></td>");
                                    // var div = "<ul class='buy-number'><li class='reduce'>-</li><li class='num'>" + num + "</li><li class='add'>+</li></ul>";
                                    var td3 = $("<td class='cell3'>" + respond['address'] +"</td>");
                                    var td4 = $("<td class='cell4'>" + respond['price'] +"</td>");
                                    var td5 = $("<td class='cell5'><a href='#'>删除</a> </td>");
                                    var tr = $("<tr></tr>");
                                    tr.append(td1,td2,td3,td4,td5);
                                    $(".goodtotal table").append(tr);
                                // }

                            //删除按键 cookie对应的id删除
                            $(function(){
                                $(".cell5 a").click(function() {
                                    var id = $(this).parent().parent().find(".goods-info").find("a").attr("href").split("?")[1];
                                    var users = $.cookie("users") ? JSON.parse( $.cookie("users") ) : [];
                                    users = users[users.length-1].user;

                                    var usersgood = $.cookie("usersgood") ? JSON.parse( $.cookie("usersgood") ) : [];
                                    if(usersgood.length > 0){
                                        for(var i=0 ; i<usersgood.length ; i++){
                                            (function(index) {
                                                if(users ==usersgood[index].user ){
                                                    var data = usersgood[index].data;
                                                    for(var p =0 ;p<data.length;p++){
                                                        (function(t) {
                                                            if(id == data[t].id){
                                                                data.splice(t,1);
                                                                $.cookie("usersgood",JSON.stringify(usersgood),{expires: 7, path: "/"});
                                                            }
                                                        })(p)
                                                    }
                                                }
                                            })(i)
                                        }
                                    }
                                    $(this).parent().parent().remove();
                                })
                            });




                        })
                    })(x)
                }
            }
        })(i)

    }

    $(".submit").click(function() {
                                location.href="http://127.0.0.1:8080/shop_pay/pay/"+orders_id+"/"
                                // $.get('http://127.0.0.1:8080/shop_pay/pay/'+orders_id+'/',function (res) {
                                //     alert(res)
                                // })
                                })
});


