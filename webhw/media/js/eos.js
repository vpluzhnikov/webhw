/**
 * Created with PyCharm.
 * User: vs
 * Date: 09.12.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */

var eos_items = []
var ru_vals = { 'new' : "Новый",
    'upgrade' : "Апгрейд",
    'app' : "Сервер приложения",
    'db' : "Сервер СУБД",
    'term' : "Терминальный сервер",
    'dp' : "IBM DataPower",
    'lb' : "Балансировщик",
    'power' : "IBM Power",
    't_series' : "Oracle T-series",
    'm_series' : "Oracle M-series",
    'itanium' : "HP Itanium",
    'x86' : "Intel x86",
    '---' : "---"
}

function editReq(id){
    window.alert("edit " + id);
}

function deleteReq(id){
    eos_items.splice(id, 1);
    renderEos();
}

function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

function renderEos() {
    var prom_count = 0;
    var prom_cost = 0.0;
    var test_nt_count = 0;
    var test_nt_cost = 0.0;
    var test_other_count = 0;
    var test_other_cost = 0.0;

    $("#prom_body").empty();
    $("#test_nt_body").empty();
    $("#test_other_body").empty();
    for (var i =0; i < eos_items.length; ++i) {
        item = eos_items[i];
        console.log(item);
        if (item["itemstatus"] == 'prom'){
            $("#prom_body").append("<table> <tr>"+
                "<td> <label class=\"main_window_data\">"+ru_vals[item["itemtype2"]]+"</label></td>" +
                "<td> <label class=\"main_window_data\">"+ru_vals[item["itemtype1"]]+"</label></td>" +
                "<td> <label class=\"main_window_data\"> Кол-во: "+item["item_count"]+"</label></td>"+
                "<td> <label class=\"main_window_data\"> Тип: "+ru_vals[item["platform_type"]]+"</label></td>"+
                "<td> <label class=\"main_window_data\"> Стоимость "+item["price"]+"$</label></td>"+
                "<td> <a onclick=\"editReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-pencil-square-o\"></i></a> </td>" +
                "<td> <a onclick=\"deleteReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-trash-o\"></i></a> </td>" +
                "</tr> </table>");
            prom_count += 1;
            prom_cost += parseFloat(item["price"]);
        }
        if (item["itemstatus"] == 'test-nt'){
            $("#test_nt_body").append("<table> <tr>"+
                "<td> <label class=\"main_window_data\">"+ru_vals[item["itemtype2"]]+"</label></td>" +
                "<td> <label class=\"main_window_data\">"+ru_vals[item["itemtype1"]]+"</label></td>" +
                "<td> <label class=\"main_window_data\"> Кол-во: "+item["item_count"]+"</label></td>"+
                "<td> <label class=\"main_window_data\"> Тип: "+ru_vals[item["platform_type"]]+"</label></td>"+
                "<td> <label class=\"main_window_data\"> Стоимость "+item["price"]+"$</label></td>"+
                "<td> <a onclick=\"editReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-pencil-square-o\"></i></a> </td>" +
                "<td> <a onclick=\"deleteReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-trash-o\"></i></a> </td>" +
                "</tr> </table>");
            test_nt_count += 1;
            test_nt_cost += parseFloat(item["price"]);
        }
        if (item["itemstatus"] == 'test-other'){
            $("#test_other_body").append("<table> <tr>"+
                "<td> <label class=\"main_window_data\">"+ru_vals[item["itemtype2"]]+"</label></td>" +
                "<td> <label class=\"main_window_data\">"+ru_vals[item["itemtype1"]]+"</label></td>" +
                "<td> <label class=\"main_window_data\"> Кол-во: "+item["item_count"]+"</label></td>"+
                "<td> <label class=\"main_window_data\"> Тип: "+ru_vals[item["platform_type"]]+"</label></td>"+
                "<td> <label class=\"main_window_data\"> Стоимость "+item["price"]+"$</label></td>"+
                "<td> <a onclick=\"editReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-pencil-square-o\"></i></a> </td>" +
                "<td> <a onclick=\"deleteReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-trash-o\"></i></a> </td>" +
                "</tr> </table>");
            test_other_count += 1;
            test_other_cost += parseFloat(item["price"]);
        }

    }
    $("#prom_count").html('Кол-во ' + prom_count);
    $("#prom_cost").html('Стоимость ' + prom_cost +'$');
    $("#test_nt_count").html('Кол-во ' + prom_count);
    $("#test_nt_cost").html('Стоимость ' + prom_cost +'$');
    $("#test_other_count").html('Кол-во ' + prom_count);
    $("#test_other_cost").html('Стоимость ' + prom_cost +'$');

//    $("#prom_count").prop('value', 'Кол-во ' + prom_count);
//    $("#prom_cost").val("Стоимость " + prom_cost +"$");
}


function clearAddForm() {
    $("#itemtype2").val('new');
    $("#itemtype1").val('---');
    $("#itemstatus").val('---');
    $("#servername").val('-');
    $("#upgrade_params").hide();
    $("#cpu_count").val('0');
    $("#ram_count").val('0');
    $("#hdd_count").val('0');
    $("#san_count").val('0');
    $("#nas_count").val('0');
    $("#item_count").val('0');
    $("#ostype").val('---');
    $("#platform_type").val('---');
    $("#lan_segment").val('alpha');
    $("#db_type").val('---');
    $("#cluster_type").val('none');
    $("#backup_type").val('no');
    $("#itemtype1").css({'color' : 'black'});
    $("#itemstatus").css({'color' : 'black'});
    $("#servername").css({'color' : 'black'});
    $("#item_count").css({'color' : 'black'});
    $("#ostype").css({'color' : 'black'});
    $("#platform_type").css({'color' : 'black'});
}

function formCheck() {
    var formValid = 1;
    if ($("#itemtype1").val() == '---') {
        $("#itemtype1").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#itemtype1").css({'color' : 'black'});
    }
    if ($("#itemstatus").val() == '---'){
        $("#itemstatus").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#itemstatus").css({'color' : 'black'});
    }
    if (($("#itemtype1").val() == 'upgrade') && ($("#servername").val() == '-' )){
        $("#servername").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#servername").css({'color' : 'black'});
    }
    if ($("#item_count").val() == '0'){
        $("#item_count").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#item_count").css({'color' : 'black'});
    }
    if (($("#ostype").val() == '---') && !(($("#itemtype1").val() == 'dp')||($("#itemtype1").val() == 'lb'))) {
        $("#ostype").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#ostype").css({'color' : 'black'});
    }
    if (($("#platform_type").val() == '---')  && !(($("#itemtype1").val() == 'dp')||($("#itemtype1").val() == 'lb'))) {
        $("#platform_type").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#platform_type").css({'color' : 'black'});
    }
    return formValid;
}


$("#load").click(function ()
    {
//        var url_boc_xlssave = "/boc_xlssave"
//        gdata = {}
//        i = 1
//        for (line in griddata) {
//            gdata[i] = griddata[line];
//            i++;
//        }
//        $.ajax({
//            type : 'POST',
//            url: url_boc_xlssave,
//            async: false,
//            dataType: 'json',
//            data: {"json" : JSON.stringify(griddata) },
//            success: function(data, status){
//                error = data.error;
//                console.log(data);
//                element = '<input id="xlsfilename" name="xlsfilename" value="'+ data['filename'] +'" type="hidden">'
//                var input = $('#boc_form').appendTo(document.body).append(element);
//            }
//        });
        $("#xls_file").click();
    }
);

$("#xls_file").change(function ()
{
    console.log($("#xls_file").val());
    $("#boc_form").submit();
}
);

$("#save").click(function ()
    {
//        var url_boc_xlssave = "/boc_xlssave"
//        gdata = {}
//        i = 1
//        for (line in griddata) {
//            gdata[i] = griddata[line];
//            i++;
//        }
//        $.ajax({
//            type : 'POST',
//            url: url_boc_xlssave,
//            async: false,
//            dataType: 'json',
//            data: {"json" : JSON.stringify(griddata) },
//            success: function(data, status){
//                error = data.error;
//                console.log(data);
//                element = '<input id="xlsfilename" name="xlsfilename" value="'+ data['filename'] +'" type="hidden">'
//                var input = $('#boc_form').appendTo(document.body).append(element);
//            }
//        });
        window.alert("save");
    }
);

//$("#add_req").click(function ()
//    {
//        var url_boc_xlssave = "/boc_xlssave"
//        gdata = {}
//        i = 1
//        for (line in griddata) {
//            gdata[i] = griddata[line];
//            i++;
//        }
//        $.ajax({
//            type : 'POST',
//            url: url_boc_xlssave,
//            async: false,
//            dataType: 'json',
//            data: {"json" : JSON.stringify(griddata) },
//            success: function(data, status){
//                error = data.error;
//                console.log(data);
//                element = '<input id="xlsfilename" name="xlsfilename" value="'+ data['filename'] +'" type="hidden">'
//                var input = $('#boc_form').appendTo(document.body).append(element);
//            }
//        });
//        window.alert("add");
//    }
//);

$('#add_req').click(function() {
    clearAddForm();
    $('#add_req_dialog').arcticmodal();
});

$("#itemtype2").click(function() {
    if ($(this).val() == 'new'){
        $("#upgrade_params").fadeOut(300);
    } else {
        $("#upgrade_params").fadeIn(300);
    }

});

$("#itemtype1").click(function() {
    if ($("#itemtype2").val() == 'new') {
        if ($(this).val() == 'db') {
            $("#db_type_label").fadeIn(300);
            $("#db_type").fadeIn(300);
            $("#cpu_count").val('4');
            $("#ram_count").val('32');
            $("#hdd_count").val('300');
            $("#ostype").val('aix');
            $("#platform_type").val('power');
        }
        if ($(this).val() == 'app') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#cpu_count").val('6');
            $("#ram_count").val('48');
            $("#hdd_count").val('100');
            $("#san_count").val('0');
            $("#nas_count").val('0');
            $("#ostype").val('linux');
            $("#platform_type").val('x86');
        }
        if ($(this).val() == 'term') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#cpu_count").val('4');
            $("#ram_count").val('24');
            $("#hdd_count").val('100');
            $("#san_count").val('0');
            $("#nas_count").val('0');
            $("#ostype").val('widows');
            $("#platform_type").val('x86');
        }
        if ($(this).val() == 'lb') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#cpu_count").val('-');
            $("#ram_count").val('-');
            $("#hdd_count").val('-');
            $("#san_count").val('-');
            $("#nas_count").val('-');
            $("#ostype").val('---');
            $("#platform_type").val('---');
            $("#cluster_type").val('none');
            $("#backup_type").val('no');
        }
        if ($(this).val() == 'dp') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#cpu_count").val('-');
            $("#ram_count").val('-');
            $("#hdd_count").val('-');
            $("#san_count").val('-');
            $("#nas_count").val('-');
            $("#ostype").val('---');
            $("#platform_type").val('---');
            $("#cluster_type").val('none');
            $("#backup_type").val('no');
        }
    }
});

$("#itemstatus").click(function() {
    if ($("#itemtype2").val() == 'new') {
        if ($(this).val() == 'prom') {
            if ($("#itemtype1").val() == 'db') {
                $("#cluster_type").val('vcs');
                $("#backup_type").val('yes');
            }
            if ($("#itemtype1").val() == 'app') {
                $("#cluster_type").val('app');
                $("#backup_type").val('yes');
            }
            if ($("#itemtype1").val() == 'term') {
                $("#cluster_type").val('app');
                $("#backup_type").val('yes');
            }
            if ($("#itemtype1").val() == 'lb') {
                $("#cluster_type").val('none');
                $("#backup_type").val('no');
            }
            if ($("#itemtype1").val() == 'dp') {
                $("#cluster_type").val('none');
                $("#backup_type").val('no');
            }
        }
        if ($(this).val() == 'test-nt') {
            $("#cluster_type").val('none');
            $("#backup_type").val('no');
        }
        if ($(this).val() == 'test-other') {
            $("#cluster_type").val('none');
            $("#backup_type").val('no');
        }
    }
});

$("#ostype").click(function() {
    if ($(this).val() == 'aix') {
        $("#platform_type").val('power');
    }
    if ($(this).val() == 'solaris') {
        $("#platform_type").val('t_series');
    }
    if ($(this).val() == 'hpux') {
        $("#platform_type").val('itanium');
    }
    if ($(this).val() == 'linux') {
        $("#platform_type").val('x86');
    }
    if ($(this).val() == 'windows') {
        $("#platform_type").val('x86');
    }
});

$("#platform_type").click(function() {
    if ($(this).val() == 'power') {
        $("#ostype").val('aix');
    }
    if ($(this).val() == 't_series') {
        $("#ostype").val('solaris');
    }
    if ($(this).val() == 'm_series') {
        $("#ostype").val('solaris');
    }
    if ($(this).val() == 'itanium') {
        $("#ostype").val('hpux');
    }
    if ($(this).val() == 'x86') {
        $("#ostype").val('linux');
    }
});

$("#db_type").click(function() {
    if ($(this).val() == 'mssql') {
        $("#ostype").val('windows');
        $("#platform_type").val('x86');
    }
});

$("#add_req_modal").click(function() {
    var url_eos_addreq = "/add_req";
    var req_line = {};
    if (formCheck()) {
        req_line["itemtype2"] = $("#itemtype2").val();
        req_line["itemtype1"] = $("#itemtype1").val();
        req_line["itemstatus"] = $("#itemstatus").val();
        req_line["servername"] = $("#servername").val();
        req_line["cpu_count"] = $("#cpu_count").val();
        req_line["ram_count"] = $("#ram_count").val();
        req_line["hdd_count"] = $("#hdd_count").val();
        req_line["san_count"] = $("#san_count").val();
        req_line["nas_count"] = $("#nas_count").val();
        req_line["item_count"] = $("#item_count").val();
        req_line["ostype"] = $("#ostype").val();
        req_line["platform_type"] = $("#platform_type").val();
        req_line["lan_segment"] = $("#lan_segment").val();
        req_line["db_type"] = $("#db_type").val();
        req_line["cluster_type"] = $("#cluster_type").val();
        req_line["backup_type"] = $("#backup_type").val();
    console.log(req_line);
    $.ajax({
        type:'POST',
        url:url_eos_addreq,
        async:false,
        dataType:'json',
        data:{"json":JSON.stringify(req_line) },
        success:function (data, status) {
            error = data.error;
//            console.log(data);
            eos_items.push(data);
            console.log(eos_items);
        }
    });
    renderEos();
    $("#close").click();
    }
});