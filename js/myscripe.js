console.log('hellow,外联样式');
let mode;
let botton_mode = 0;
let interact_mode;
function click_alert(mode){
    alert('触发弹窗'+mode);
}

function inside_element(input_name){
    console.log('点击了'+input_name+'内部');

}

function outside_element(input_name){
    console.log('点击了'+input_name+'外部');
}

 
function change_button2(){
    botton_mode = 1 - botton_mode;
    if (botton_mode === 1){
        doc_id.style.backgroundColor = "green";
        doc_id.style.width = "300px";
        doc_id.style.height = "70px";
        doc_id.style.fontSize = "30px";
        doc_id.innerHTML = "变化回复";
    }
    else{
        // width: 100px;
        //     height: 30px;
        // background-color: aqua;
        doc_id.style.backgroundColor = "aqua";
        doc_id.style.width = "100px";
        doc_id.style.height = "30px";
        doc_id.style.fontSize = "16px";
        doc_id.innerHTML = "变化案例";
        
        doc_id.onclick = change_button;
    }
}
function change_button(){
    // doc_id.innerHTML = "变化成功";
    doc_id.style.backgroundColor = "red";
    doc_id.style.width = "200px";
    doc_id.style.height = "50px";
    doc_id.style.fontSize = "20px";

    console.log(doc_id);
    // alert('按钮变化成功');
    // 用n = 1 - n 的方法，实现按钮的切换
    botton_mode = 1 - botton_mode;
    if (botton_mode === 1){
        doc_id.innerHTML = "变化/成功";
    }
    else{
        doc_id.innerHTML = "变化成功2";
        doc_id.onclick = change_button2;
    }
    
}

function change_on(){
    alert('发生变化');
}
