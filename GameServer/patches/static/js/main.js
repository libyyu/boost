 function $$(Id) {
    return window.document.getElementById(Id);
 }

 //创建XMLHttpRequest对象       
 function createXMLHttpRequest() {
    var XMLHttpReq = null;
     if(window.XMLHttpRequest) { //Mozilla 浏览器
         XMLHttpReq = new XMLHttpRequest();
     }
     else if (window.ActiveXObject) { // IE浏览器
         try {
             XMLHttpReq = new ActiveXObject("Msxml2.XMLHTTP");
         } catch (e) {
             try {
                 XMLHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
             } catch (e) {}
         }
     }

     return XMLHttpReq;
 }
 //get
 function sendRequest (url) {
     r = createXMLHttpRequest();
     r.open('GET', url, false);
     r.send(null);
     return r;
 }

 function sendAyncRequest (url, processer) {
     r = createXMLHttpRequest();
     r.open('GET', url, true);
     r.onreadystatechange = function(){processer(r);};
     r.send(null);
 }

 function postRequest (url, data) {
     r = createXMLHttpRequest();
     r.open('POST', url, false);
     r.send(data);
     return r;
 }

 function postAsyncRequest (url, data, processer) {
     r = createXMLHttpRequest();
     r.open('POST', url, true);
     r.setRequestHeader("Content-type","application/x-www-form-urlencoded");
     r.onreadystatechange = function(){processer(r);};
     r.send(data);
 }

 /*

 //发送请求函数
 function sendRequest(url) {
     createXMLHttpRequest();
     XMLHttpReq.open("GET", url, true);
     XMLHttpReq.onreadystatechange = processResponse;//指定响应函数
     XMLHttpReq.send(null);  // 发送请求
 }
 // 处理返回信息函数
 function processResponse() {
     if (XMLHttpReq.readyState == 4) { // 判断对象状态
         if (XMLHttpReq.status == 200) { // 信息已经成功返回，开始处理信息
             var res=XMLHttpReq.responseXML.getElementsByTagName("res")[0].firstChild.data;
                window.alert(res);                
            } else { //页面不正常
                window.alert("您所请求的页面有异常。");
            }
        }
    }
 // 身份验证函数
 function userCheck() {
     var uname = document.myform.uname.value;
     var psw = document.myform.psw.value;
     if(uname=="") {
         window.alert("用户名不能为空。");
         document.myform.uname.focus();
         return false;
     }
     else {
         sendRequest('login?uname='+ uname + '&psw=' + psw);
     }
 }
*/
//搜索
function searchlrc() {
    var name = document.searchlrcform.key.value;
    if (!name) {
        alert('请输入');
        return false;
    };
    //return true;
    getsearchresult(name);
    return false;
}

function onSearchResult(r)
{
    if (4 == r.readyState) {
        if (200 == r.status) {
            window.document.getElementById('top').value = r.responseText;
            document.write(r.responseText);
            //alert(r.responseText);
        };
    };
}

function getsearchresult(s) {
    data = 'key=' + s;
    postAsyncRequest('/lrcsearch', 'key=abacd', onSearchResult)
}

function searchTextCheck() {
    var name = document.searchlrcform.key.value;
    if (!name) {
        alert('内容不能为空！');
        return false;
    };
    return true;
}

//
function logincheck() {
    var name = document.getElementById('name');
    var pwd = document.getElementById('pwd');
    if (!name.value) {
        alert('用户名不能为空。');
        name.focus()
    }
    else if(!pwd.value)
    {
        alert('密码不能为空');
        pwd.focus();
    }
    else
    {
        return true;
    }
    return false;
}
/*
window.onload = function(){ 
    var oTable = document.getElementById("bbsTab"); 
    for(var i=0;i<oTable.rows.length;i++){ 
        oTable.rows[i].cells[0].innerHTML = (i+1); 
        if(i%2==0)    //偶数行 
            oTable.rows[i].className = "ys01"; 
    } 
} 
*/


//lrc op
function onlrcopfinished(r) {
     if (4 == r.readyState) {
            if (200 == r.status) {
                window.location.reload();
                return;
            };

            alert(r.status);
        };   
}
function lrcop(Id, op) {
    data = 'id=' + Id + "&optype=" + op;
    postAsyncRequest('/manager/lrc', data, onlrcopfinished)
}

function modifylrc(Id, name, obj_name, id_num) {
    newlrcform = document.newlrcform;
    newlrcform.name.value = name;
    newlrcform.obj_name.value = obj_name;
    newlrcform.id_num.value = id_num;
    newlrcform.optype.value = 4;
    newlrcform.id.value = Id;
}


function isvalidnewlrc() {
    newlrcform = document.newlrcform;
    var name = newlrcform.name.value;
    var obj_name = newlrcform.obj_name.value;
    var optype = newlrcform.optype.value;
    var Id = newlrcform.id.value;
    var id_num = newlrcform.id_num.value;
    if (name && obj_name && 3 == optype) {
        return true;
    }
    else if(name && obj_name && 4 == optype && Id) {
        return true;
    }
    alert('请检查输入');
    return false;
}

//
function ontestload(r) {
    if (4 == r.readyState) {
        if (200 == r.status) {
            var obj = eval ("(" + txt + ")");
            alert(r.responseText.totalpost);
        };
    };
}

function load() {
    sendAyncRequest('/manager/postlist',ontestload);
}

//分页
function shownavpages(url, page, count, maxshowpagenum, prepagecnt) {
    var totalpage = count/prepagecnt  + (count%prepagecnt > 0 ? 1 : 0)|0;
    if (totalpage <= 1)
        return;

    var pagesnode = document.getElementById('page-navigator');
    var html = '';
    var n = (page - (page%maxshowpagenum == 0 ? maxshowpagenum : 0))/(maxshowpagenum)|0;
    
    var nbeg =  n*maxshowpagenum + 1;
    var nend = nbeg + maxshowpagenum - 1;
    if(nend > totalpage)
        nend = totalpage;

    if(nbeg > 1) {
        npre = nbeg - 1;
        if(npre <= 0)
            npre = 1;
        html += "<li><a href='" + url + npre + "'>...</a></li>";
    }

    for (var i = nbeg; i <= nend; i++) {
        if(i == page)
            html += "<li class=\"active\"><a>"+ i +"</a></li>";
        else
            html += "<li><a href='" + url + i + "'>" + i + " </a></li>";
    };

    if(nend < totalpage) {
        nnext = nend + 1;
        if(nnext > totalpage)
            nnext = totalpost;
        html += "<li><a href='" + url + nnext + "'>...</a></li>";
    }

    pagesnode.innerHTML =html;
}

//操作DB
function dbtableop(tbname, optype) {
    function onoptypefinished(data) {
         window.location.reload();
    }
    $.post('/manager/dbtable', {'tbname':tbname, 'optype':optype}, onoptypefinished, 'text');
}
//操作python
function invokepythoncode (objId, resultId) {
    function onresult(data) {
        $('#' + resultId).html(data);
    }
    code = $('#' + objId).val();
    $.post('/manager/pythonrun', {'content':code}, onresult, 'text');
    return false;
}