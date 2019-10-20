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
    for(var r=0 ; r<users.length ; r++){
        if(users[r].status == 1){
            user = users[r].user;
        }
    }
    users = user;
    //读取cookie中买家购买的物品(最后一个登录的买家) status为1的顾客
    for(var i=0 ; i<usersgood.length ; i++){
        (function(index) {
            //拿到data中的数据，并显示
            if(users == usersgood[index].user){
                var data = usersgood[index].data;
                for(var x=0 ;x<data.length  ; x++){
                    (function(z) {
                        var id = data[z].id;
                        //转换num类型
                        var num = data[z].num *1;
                        var color = data[z].color;
                        var suit = data[z].suit;
                        //JSON
                        $.get("http://10.20.159.194:8080/json/number/"+id+"/",function(respond) {

                            for(var j=0 ;j<respond.length  ;j++){
                                ids = id
                                console.log(respond[j].id)
                                if(id == respond[j].id){

                                    //a,span,div字符串
                                    var total = parseInt(respond[j].price)*num;
                                    var a ="<a href='goodsdetail.html?"+  respond[j].id +"'><img src="+ respond[j].goodimg.small[0].img +"></a>"
                                    var span = "<span>【顺丰包邮s】" + respond[j].a+"</span>"
                                    var div ="<div class='color-suit'><dl class='color'><dt>颜色</dt><dd>"+  color   + "</dd></dl><dl class='suit'><dt>套装:</dt><dd>" + suit + "</dd></dl> </div>"
                                    var chose =$("<td><input class='shop' id="+ respond[j].id+" type='checkbox'></td>");
                                    var td1 = $("<td class='cell1'><div class='goods-info'>"+ a + span + div  +"</div></td>");
                                    var td2 = $("<td class='cell2'>"+ respond[j].price +"</td>");
                                    var div = "<ul class='buy-number'><li class='reduce'>-</li><li class='num'>" + num + "</li><li class='add'>+</li></ul>";
                                    var td3 = $("<td class='cell3'>" + div +"</td>");
                                    var td4 = $("<td class='cell4'>" + total +"</td>");
                                    var td5 = $("<td class='cell5'><a href='#'>删除</a> </td>");
                                    var tr = $("<tr></tr>");
                                    tr.append(chose,td1,td2,td3,td4,td5);
                                    $(".goodtotal table").append(tr);
                                }
                            }
                            //给多选框加事件
                            $(function(){
                                var checkbox = $(":checkbox").not(".chose");
                                $(".chose").click(function() {
                                    checkbox.prop( "checked", this.checked );
                                    shopinfto(this.checked)
                                });
                                checkbox.click(function() {
                                    var num = checkbox.filter(":checked").length;
                                    $(".chose").prop("checked", num ==  checkbox.length  );

                                })

                            });
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
                            //商品数量
                            $(function(){
                                $(".add").unbind("click").click(function() {
                                    var num = $(this).prev("li").html() *1;
                                    num++;
                                    $(this).prev("li").html(num);

                                });

                                $(".reduce").unbind("click").click(function() {
                                    var num = $(this).next("li").html() *1;
                                    if(num==0){
                                        num = 0;
                                        $(this).next("li").html(num);
                                        return
                                    }
                                    num--;
                                    $(this).next("li").html(num)
                                });

                            });



                        })
                    })(x)
                }
            }
        })(i)

    }

    $(".submit").click(function() {
                                    // var id = $(this).parent().parent().find(".goods-info").find("a").attr("href").split("?")[1];
                                    var users = $.cookie("users") ? JSON.parse( $.cookie("users") ) : [];
                                    var id = $.cookie("user_id") ? JSON.parse( $.cookie("user_id") ) : [];
                                    console.log(id)
                                    console.log(users)
                                    users = user;
                                    var active = 0;
                                    var num =0
                                    var usersgood = $.cookie("usersgood") ? JSON.parse( $.cookie("usersgood") ) : [];
                                    var data = []
                                // console.log(num)
                                for (var i=0;i<usersgood[0].data.length;i++){
                                    num =$('.num').eq(i).text()
                                    goods_id = usersgood[0].data[i].id
                                    console.log("ss"+i+num)
                                    active =$('.shop ').eq(i).prop('checked')
                                    console.log(active)
                                    // {'shop_id': 2516, 'shop_number': 4, 'is_active': 1}
                                    data.push({'shop_id': goods_id,'shop_number':num,'is_active':active});

                                    };
                                dict ={'user_id':id,'data':data}
                                console.log(dict)
                                $.post('http://10.20.159.194:8080/shop_pay/order_shop/',dict,function (res) {
                                    alert(res)
                                    window.location.href='orders.html'

                                })
                                })
});


