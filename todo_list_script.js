function add_line(interact_mode){
    console.log('点击'+interact_mode);
    let table = document.getElementById('secret_table');
    let new_row = table.insertRow(-1); // 在表格末尾插入新行
    let cell1 = new_row.insertCell(0);
    let cell2 = new_row.insertCell(1);
    let cell3 = new_row.insertCell(2);
    let cell4 = new_row.insertCell(3);
    let cell5 = new_row.insertCell(4);
    cell1.innerHTML = table.rows.length - 1; // 序号
    cell2.innerHTML = "新任务";
    cell3.innerHTML = "新目标";
    cell4.innerHTML = new Date().toISOString().split('T')[0]; // 当前日期
    cell5.innerHTML = `<button onclick="modify_button('修改')">修改</button>
                        <button onclick="delete_button('删除')">删除</button>`;


}

function modify_button(){
    console.log('触发修改');

}

function delete_button(){
    console.log('触发删除');

}