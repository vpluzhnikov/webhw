/**
 * Created with PyCharm.
 * User: vs
 * Date: 09.12.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */
var eos_items = [];
var modified_record = -1;
var ru_vals = { 'new' : "Новый",
    'upgrade' : "Апгрейд",
    'app' : "Сервер приложения",
    'db' : "Сервер СУБД",
    'dbarch' : "Сервер СУБД (архивная)",
    'term' : "Терминальный сервер",
    'dp' : "IBM DataPower",
    'lb' : "Балансировщик",
    'mqdmz' : "Сервер MQ (DMZ)",
    'other' : "Другое",
    'power' : "IBM Power",
    't_series' : "Oracle T-series",
    'm_series' : "Oracle M-series",
    'itanium' : "HP Itanium",
    'x86' : "Intel x86",
    '---' : "---"
};

function editReq(id){
    window.alert("edit " + id);
//    prepareReqForm(id);
//    $('#add_req_dialog').arcticmodal();

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
    var prom_cost_hw = 0.0;
    var prom_cost_sw = 0.0;
    var prom_cost_sup = 0.0;


    var test_nt_count = 0;
    var test_nt_cost = 0.0;
    var test_nt_cost_hw = 0.0;
    var test_nt_cost_sw = 0.0;
    var test_nt_cost_sup = 0.0;

    var test_other_count = 0;
    var test_other_cost = 0.0;
    var test_other_cost_hw = 0.0;
    var test_other_cost_sw = 0.0;
    var test_other_cost_sup = 0.0;


    $("#prom_body").empty();
    $("#test_nt_body").empty();
    $("#test_other_body").empty();
    for (var i =0; i < eos_items.length; ++i) {
        e_item = eos_items[i];
//        console.log(e_item);
        if (e_item["itemstatus"] == 'prom'){
            $("#prom_body").append("<table class=\"appended_table\"> <tr>"+
                "<td width=\"62px\"> <label class=\"main_window_data\">"+ru_vals[e_item["itemtype2"]]+"</label></td>" +
                "<td width=\"172px\"> <label class=\"main_window_data\">"+ru_vals[e_item["itemtype1"]]+"</label></td>" +
                "<td width=\"112px\"> <label class=\"main_window_data\"> Кол-во: "+e_item["item_count"]+"</label></td>"+
                "<td width=\"112px\"> <label class=\"main_window_data\"> Тип: "+ru_vals[e_item["platform_type"]]+"</label></td>"+
                "<td width=\"172px\"> <label class=\"main_window_data\"> Стоимость "+e_item["price"]+"$</label></td>"+
                "<td width=\"40px\"> <a onclick=\"prepareReqForm("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-pencil-square-o\"></i></a> </td>" +
                "<td width=\"40px\"> <a onclick=\"deleteReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-trash-o\"></i></a> </td>" +
                "</tr> </table>");
            prom_count += 1;
            prom_cost += parseFloat(e_item["price"]);
            prom_cost_hw += parseFloat(e_item["price_hw"]);
            prom_cost_sw += parseFloat(e_item["price_lic"]);
            prom_cost_sup += parseFloat(e_item["price_support"]);

        }
        else if (e_item["itemstatus"] == 'test-nt'){
            $("#test_nt_body").append("<table class=\"appended_table\"> <tr>"+
                "<td width=\"62px\"> <label class=\"main_window_data\">"+ru_vals[e_item["itemtype2"]]+"</label></td>" +
                "<td width=\"172px\"> <label class=\"main_window_data\">"+ru_vals[e_item["itemtype1"]]+"</label></td>" +
                "<td width=\"112px\"> <label class=\"main_window_data\"> Кол-во: "+e_item["item_count"]+"</label></td>"+
                "<td width=\"112px\"> <label class=\"main_window_data\"> Тип: "+ru_vals[e_item["platform_type"]]+"</label></td>"+
                "<td width=\"172px\"> <label class=\"main_window_data\"> Стоимость "+e_item["price"]+"$</label></td>"+
                "<td width=\"40px\"> <a onclick=\"prepareReqForm("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-pencil-square-o\"></i></a> </td>" +
                "<td width=\"40px\"> <a onclick=\"deleteReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-trash-o\"></i></a> </td>" +
                "</tr> </table>");
            test_nt_count += 1;
            test_nt_cost += parseFloat(e_item["price"]);
            test_nt_cost_hw += parseFloat(e_item["price_hw"]);
            test_nt_cost_sw += parseFloat(e_item["price_lic"]);
            test_nt_cost_sup += parseFloat(e_item["price_support"]);

        }
        else {
            $("#test_other_body").append("<table class=\"appended_table\"> <tr>"+
                "<td width=\"62px\"> <label class=\"main_window_data\">"+ru_vals[e_item["itemtype2"]]+"</label></td>" +
                "<td width=\"172px\"> <label class=\"main_window_data\">"+ru_vals[e_item["itemtype1"]]+"</label></td>" +
                "<td width=\"112px\"> <label class=\"main_window_data\"> Кол-во: "+e_item["item_count"]+"</label></td>"+
                "<td width=\"112px\"> <label class=\"main_window_data\"> Тип: "+ru_vals[e_item["platform_type"]]+"</label></td>"+
                "<td width=\"172px\"> <label class=\"main_window_data\"> Стоимость "+e_item["price"]+"$</label></td>"+
                "<td width=\"40px\"> <a onclick=\"prepareReqForm("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-pencil-square-o\"></i></a> </td>" +
                "<td width=\"40px\"> <a onclick=\"deleteReq("+ i +")\" class=\"button is-inverse has-fixed-icon\"><i class=\"fa fa-trash-o\"></i></a> </td>" +
                "</tr> </table>");
            test_other_count += 1;
            test_other_cost += parseFloat(e_item["price"]);
            test_other_cost_hw += parseFloat(e_item["price_hw"]);
            test_other_cost_sw += parseFloat(e_item["price_lic"]);
            test_other_cost_sup += parseFloat(e_item["price_support"]);

        }

    }
    var total_cost = prom_cost + test_nt_cost + test_other_cost;
    var total_cost_hw = prom_cost_hw + test_nt_cost_hw + test_other_cost_hw;
    var total_cost_sw = prom_cost_sw + test_nt_cost_sw + test_other_cost_sw;
    var total_cost_sup = prom_cost_sup + test_nt_cost_sup + test_other_cost_sup;

    $("#prom_count").html('Кол-во ' + prom_count);
    $("#prom_cost").html('Стоимость ' + prom_cost +'$');
    $("#prom_hw_cost").html('Оборудование ' + prom_cost_hw +'$');
    $("#prom_sw_cost").html('Лицензии ' + prom_cost_sw +'$');
    $("#prom_sup_cost").html('Поддержка ' + prom_cost_sup +'$');

    $("#test_nt_count").html('Кол-во ' + test_nt_count);
    $("#test_nt_cost").html('Стоимость ' + test_nt_cost +'$');
    $("#test_nt_hw_cost").html('Оборудование ' + test_nt_cost_hw +'$');
    $("#test_nt_sw_cost").html('Лицензии ' + test_nt_cost_sw +'$');
    $("#test_nt_sup_cost").html('Поддержка ' + test_nt_cost_sup +'$');


    $("#test_other_count").html('Кол-во ' + test_other_count);
    $("#test_other_cost").html('Стоимость ' + test_other_cost +'$');
    $("#test_other_hw_cost").html('Оборудование ' + test_other_cost_hw +'$');
    $("#test_other_sw_cost").html('Лицензии ' + test_other_cost_sw +'$');
    $("#test_other_sup_cost").html('Поддержка ' + test_other_cost_sup +'$');


    $("#total_cost").html('Общая стоимость ' + total_cost +'$');
    $("#total_cost_hw").html('Оборудование ' + total_cost_hw +'$');
    $("#total_cost_sw").html('Лицензии ' + total_cost_sw +'$');
    $("#total_cost_sup").html('Поддержка за год ' + total_cost_sup +'$');

}


function prepareReqForm(num_req) {
    if (num_req == -1 ) {
        $("#itemtype2").val('new');
        $("#itemtype1").val('other');
        $("#itemstatus").val('---');
        $("#servername").val('-');
        $("#upgrade_params").hide();
        $("#new_params").show();
        $("#cpu_count").val('0');
        $("#ram_count").val('0');
        $("#hdd_count").val('0');
        $("#san_count").val('0');
        $("#nas_count").val('0');
        $("#item_count").val('0');
        $("#ostype").val('---');
        $("#ostype").show();
        $("#platform_type").val('---');
        $("#platform_type").show();
        $("#lan_segment").val('alpha');
        $("#db_type").val('---');
        $("#db_type").hide();
        $("#db_type_label").hide();
        $("#app_type").val('---');
        $("#app_type").hide();
        $("#app_type_label").hide();
        $("#cluster_type").val('none');
        $("#cluster_type").show();
        $("#backup_type").val('no');
        $("#backup_type").show();
        $("#utilization").val('100');
        $("#utilization").hide();
        $("#utilization_label").hide();
        $("#itemtype1").css({'color':'black'});
        $("#itemstatus").css({'color':'black'});
        $("#servername").css({'color':'black'});
        $("#item_count").css({'color':'black'});
        $("#ostype").css({'color':'black'});
        $("#platform_type").css({'color':'black'});
        $("#utilization").css({'color':'black'});
        $("#add_req_modal").show();
        $("#edit_req_modal").hide();
    }
    if (num_req >= 0) {
        var req_line = {}
        req_line = eos_items[num_req];
        $("#itemtype2").val(req_line["itemtype2"]);
        $("#itemtype1").val(req_line["itemtype1"]);
        $("#itemstatus").val(req_line["itemstatus"]);
        $("#servername").val(req_line["servername"]);
        $("#cpu_count").val(req_line["cpu_count"]);
        $("#ram_count").val(req_line["ram_count"]);
        $("#hdd_count").val(req_line["hdd_count"]);
        $("#san_count").val(req_line["san_count"]);
        $("#nas_count").val(req_line["nas_count"]);
        $("#item_count").val(req_line["item_count"]);
        $("#ostype").val(req_line["ostype"]);
        $("#platform_type").val(req_line["platform_type"]);
        $("#lan_segment").val(req_line["lan_segment"]);
        $("#db_type").val(req_line["db_type"]);
        $("#app_type").val(req_line["app_type"]);
        $("#cluster_type").val(req_line["cluster_type"]);
        $("#backup_type").val(req_line["backup_type"]);
        $("#edit_req_modal").show();
        $("#add_req_modal").hide();


        if ((req_line["itemtype1"] == 'lb') || (req_line["itemtype1"] == 'dp') || (req_line["itemtype1"] == 'mqdmz')) {
            $("#db_type_label").hide();
            $("#db_type").hide();
            $("#app_type_label").hide();
            $("#app_type").hide();
            $("#new_params").hide();
            $("#ostype").hide();
            $("#platform_type").hide();
            $("#cluster_type").hide();
            $("#backup_type").hide();
            $("#cluster_type_label").hide();
            $("#backup_type_label").hide();
            $("#utilization").val(req_line["utilization"]);
            $("#utilization").show();
            $("#utilization_label").show();
        } else
        {
            if ((req_line["itemtype1"] == 'db') || (req_line["itemtype1"] == 'dbarch')) {
                $("#db_type_label").show();
                $("#db_type").show();
            } else {
                $("#db_type_label").hide();
                $("#db_type").hide();

            }
            if (req_line["itemtype1"] == 'app') {
                $("#app_type_label").show();
                $("#app_type").show();
            } else {
                $("#app_type_label").hide();
                $("#app_type").hide();
            }
            $("#new_params").show();
            $("#ostype").show();
            $("#platform_type").show();
            $("#cluster_type").show();
            $("#backup_type").show();
            $("#cluster_type_label").show();
            $("#backup_type_label").show();
            $("#utilization").hide();
            $("#utilization_label").hide();
            if (req_line["itemtype2"] == 'upgrade') {
                $("#upgrade_params").show();
            }
            else {
                $("#upgrade_params").hide();
            }
        }

        modified_record = num_req;
    }
    $('#add_req_dialog').arcticmodal();
}

function formCheck() {
    var formValid = 1;
//    if ($("#itemtype1").val() == '---') {
//        $("#itemtype1").css({'color' : 'red'});
//        formValid = 0;
//    } else
//    {
//        $("#itemtype1").css({'color' : 'black'});
//    }
    if ($("#itemstatus").val() == '---'){
        $("#itemstatus").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#itemstatus").css({'color' : 'black'});
    }
    if (($("#itemtype2").val() == 'upgrade') && ($("#servername").val() == '-' )){
        $("#servername").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#servername").css({'color' : 'black'});
    }
    if (parseInt($("#item_count").val()) <= 0) {
        $("#item_count").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#item_count").css({'color' : 'black'});
    }
    if (parseInt($("#cpu_count").val()) < 0) {
        $("#cpu_count").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#cpu_count").css({'color' : 'black'});
    }
    if (parseInt($("#ram_count").val()) < 0) {
        $("#ram_count").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#ram_count").css({'color' : 'black'});
    }
    if (parseInt($("#hdd_count").val()) < 0) {
        $("#hdd_count").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#hdd_count").css({'color' : 'black'});
    }
    if (parseInt($("#san_count").val()) < 0) {
        $("#san_count").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#san_count").css({'color' : 'black'});
    }
    if (parseInt($("#nas_count").val()) < 0) {
        $("#nas_count").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#nas_count").css({'color' : 'black'});
    }

    if ((parseInt($("#utilization").val()) < 0)||(parseInt($("#utilization").val()) > 100)) {
        $("#utilization").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#utilization").css({'color' : 'black'});
    }


    if (($("#ostype").val() == '---') && !(($("#itemtype1").val() == 'dp')||($("#itemtype1").val() == 'lb')||($("#itemtype1").val() == 'mqdmz')||($("#itemtype1").val() == 'other'))) {
        $("#ostype").css({'color' : 'red'});
        formValid = 0;
    } else
    {
        $("#ostype").css({'color' : 'black'});
    }
    if (($("#platform_type").val() == '---')  && !(($("#itemtype1").val() == 'dp')||($("#itemtype1").val() == 'lb')||($("#itemtype1").val() == 'mqdmz')||($("#itemtype1").val() == 'other'))) {
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
        $("#id_xls_file").click();
    }
);

$("#id_xls_file").change(function ()
{
    console.log($("#id_xls_file").val());
    $("#load_img").show();
    $("#boc_form").submit();
}
);


$("#save").add("#rp_save").click(function (event)
    {
        $("#prj_function").val(event.target.id);
        console.log(event.target.id)

        var url_get_prj_list = "/eos/get_prj_list"
        $.ajax({
            url:url_get_prj_list ,
            async:false,
            dataType:'json',
            success:function (data, status) {
//                console.log(data);
                curr_project = $('#prjnum').val()
                curr_project_name = $('#prjname').val()

                for (var i=0;i<data.prjcount;i++) {
                    $('#prjselect').append('<option value='+data[i]+'>'+data[i]+'</option>');
                }
                if (curr_project != '') {
                    $('#prjselect').val(curr_project);
                    $('#prjname').val(curr_project_name);
                }

            }
        });

        $('#prjselect_dialog').arcticmodal();

    }
);

$("#prj_confirm").click(function ()
{
    $("#close_prjselect_dialog").click();

    if ($("#prj_function").val() == 'save') {
        var url_eos_pdfsave = "/eos/export_to_pdf";
        eosdata = {};
        i = 1;
        for (line in eos_items) {
            eosdata[i] = eos_items[line];
            i++;
        }
        eosdata['project_id'] = $("#prjnum").val();
        eosdata['project_name'] = $("#prjname").val();
        console.log(eosdata);
        $.ajax({
            type : 'POST',
            url: url_eos_pdfsave ,
            async: false,
            dataType: 'json',
            data: {"json" : JSON.stringify(eosdata) },
            success: function(data, status){
                error = data.error;
//                console.log(data);
                document.location.href="eos/get_eos_pdf/"+data['filename'];
            }
        });
    } else
    {
        var url_plan_build = "/eos/build_resource_plan";
        eosdata = {};
        i = 1;
        for (line in eos_items) {
            eosdata[i] = eos_items[line];
            i++;
        }
        eosdata['project_id'] = $("#prjnum").val();
        eosdata['project_name'] = $("#prjname").val();
        console.log(eosdata);
        $.ajax({
            type : 'POST',
            url: url_plan_build ,
            async: false,
            dataType: 'json',
            data: {"json" : JSON.stringify(eosdata) },
            success: function(data, status){
                error = data.error;
                console.log(data);
                document.location.href="eos/get_resource_plan/"+data['filename'];
            }
        });
    }
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
    prepareReqForm(-1);
//    $('#add_req_dialog').arcticmodal();
});

$("#itemtype2").change(function() {
    if ($(this).val() == 'new'){
        $("#upgrade_params").fadeOut(300);
    } else {
        $("#upgrade_params").fadeIn(300);
    }

});

$("#itemtype1").change(function() {
    if ($("#itemtype2").val() == 'new') {
        if (($(this).val() == 'db') ||($(this).val() == 'dbarch'))  {
            $("#db_type_label").fadeIn(300);
            $("#db_type").fadeIn(300);
            $("#app_type_label").fadeOut(300);
            $("#app_type").fadeOut(300);
            $("#new_params").fadeIn(300);
            $("#cpu_count").val('4');
            $("#ram_count").val('32');
            $("#hdd_count").val('300');
            $("#ostype").val('aix');
            $("#platform_type").val('power');

            $("#ostype").show();
            $("#platform_type").show();
            $("#cluster_type").show();
            $("#backup_type").show();
            $("#cluster_type_label").show();
            $("#backup_type_label").show();
            $("#utilization").hide();
            $("#utilization_label").hide();
        }
        if ($(this).val() == 'app') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#app_type_label").fadeIn(300);
            $("#app_type").fadeIn(300);
            $("#new_params").fadeIn(300);
            $("#cpu_count").val('6');
            $("#ram_count").val('48');
            $("#hdd_count").val('100');
            $("#san_count").val('0');
            $("#nas_count").val('0');
            $("#ostype").val('linux');
            $("#platform_type").val('x86');

            $("#ostype").show();
            $("#platform_type").show();
            $("#cluster_type").show();
            $("#backup_type").show();
            $("#cluster_type_label").show();
            $("#backup_type_label").show();
            $("#utilization").hide();
            $("#utilization_label").hide();

        }
        if ($(this).val() == 'term') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#app_type_label").fadeOut(300);
            $("#app_type").fadeOut(300);
            $("#new_params").fadeIn(300);
            $("#cpu_count").val('4');
            $("#ram_count").val('24');
            $("#hdd_count").val('100');
            $("#san_count").val('0');
            $("#nas_count").val('0');
            $("#ostype").val('windows');
            $("#platform_type").val('x86');

            $("#ostype").show();
            $("#platform_type").show();
            $("#cluster_type").show();
            $("#backup_type").show();
            $("#cluster_type_label").show();
            $("#backup_type_label").show();
            $("#utilization").hide();
            $("#utilization_label").hide();

        }
        if ($(this).val() == 'lb') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#app_type_label").fadeOut(300);
            $("#app_type").fadeOut(300);
            $("#new_params").fadeOut(300);
            $("#cpu_count").val('0');
            $("#ram_count").val('0');
            $("#hdd_count").val('0');
            $("#san_count").val('0');
            $("#nas_count").val('0');
            $("#ostype").val('---');
            $("#platform_type").val('---');
            $("#cluster_type").val('none');
            $("#backup_type").val('no');

            $("#ostype").hide();
            $("#platform_type").hide();
            $("#cluster_type").hide();
            $("#backup_type").hide();
            $("#cluster_type_label").hide();
            $("#backup_type_label").hide();
            $("#utilization").show();
            $("#utilization_label").show();


        }
        if ($(this).val() == 'dp') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#app_type_label").fadeOut(300);
            $("#app_type").fadeOut(300);
            $("#new_params").fadeOut(300);
            $("#cpu_count").val('0');
            $("#ram_count").val('0');
            $("#hdd_count").val('0');
            $("#san_count").val('0');
            $("#nas_count").val('0');
            $("#ostype").val('---');
            $("#platform_type").val('---');
            $("#cluster_type").val('none');
            $("#backup_type").val('no');

            $("#ostype").hide();
            $("#platform_type").hide();
            $("#cluster_type").hide();
            $("#backup_type").hide();
            $("#cluster_type_label").hide();
            $("#backup_type_label").hide();
            $("#utilization").show();
            $("#utilization_label").show();

        }
        if ($(this).val() == 'mqdmz') {
            $("#db_type_label").fadeOut(300);
            $("#db_type").fadeOut(300);
            $("#app_type_label").fadeOut(300);
            $("#app_type").fadeOut(300);
            $("#new_params").fadeOut(300);
            $("#cpu_count").val('32');
            $("#ram_count").val('96');
            $("#hdd_count").val('300');
            $("#san_count").val('50');
            $("#nas_count").val('0');
            $("#ostype").val('windows');
            $("#platform_type").val('x86');
            $("#cluster_type").val('vcs');
            $("#backup_type").val('yes');

            $("#ostype").hide();
            $("#platform_type").hide();
            $("#cluster_type").hide();
            $("#backup_type").hide();
            $("#cluster_type_label").hide();
            $("#backup_type_label").hide();
            $("#utilization").show();
            $("#utilization_label").show();

        }

    }
});

$("#itemstatus").change(function() {
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
            if ($("#itemtype1").val() == 'mqdmz') {
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
        else  {
            $("#cluster_type").val('none');
            $("#backup_type").val('no');
        }
    }
});

$("#ostype").change(function() {
    if ($(this).val() == 'aix') {
        $("#platform_type").val('power');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 'solaris') {
        $("#platform_type").val('t_series');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 'hpux') {
        $("#platform_type").val('itanium');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 'linux') {
        $("#platform_type").val('x86');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 'windows') {
        $("#platform_type").val('x86');
    }
});

$("#platform_type").change(function() {
    if ($(this).val() == 'power') {
        $("#ostype").val('aix');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 't_series') {
        $("#ostype").val('solaris');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 'm_series') {
        $("#ostype").val('solaris');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 'itanium') {
        $("#ostype").val('hpux');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
    if ($(this).val() == 'x86') {
        $("#ostype").val('linux');
        if ($("#db_type").val() == 'mssql') {
            $("#db_type").val('---');
        }
    }
});

$("#db_type").change(function() {
    if ($(this).val() == 'mssql') {
        $("#ostype").val('windows');
        $("#platform_type").val('x86');
    }
});

$("#add_req_modal").click(function() {
    var url_eos_addreq = "/eos/calc_req";
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
        req_line["app_type"] = $("#app_type").val();
        req_line["cluster_type"] = $("#cluster_type").val();
        req_line["backup_type"] = $("#backup_type").val();
        req_line["utilization"] = $("#utilization").val();
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

$("#edit_req_modal").click(function() {
    var url_eos_addreq = "/eos/calc_req";
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
        req_line["app_type"] = $("#app_type").val();
        req_line["cluster_type"] = $("#cluster_type").val();
        req_line["backup_type"] = $("#backup_type").val();
        req_line["utilization"] = $("#utilization").val();
        $.ajax({
            type:'POST',
            url:url_eos_addreq,
            async:false,
            dataType:'json',
            data:{"json":JSON.stringify(req_line) },
            success:function (data, status) {
                error = data.error;
//                console.log(data);
                eos_items[modified_record] = data;
                console.log(eos_items);
            }
        });
        renderEos();
        $("#close").click();
    }



});

$("#prjselect").change(function ()
{
    var url_get_prj_name = "/eos/get_prj_name"
    $.ajax({
        url: url_get_prj_name,
        async: false,
        dataType: 'json',
        data: { "project_id" : $("#prjselect").val() },
        success: function(data, status){
            $("#prjname").val(data.project_name);
            $("#prjnum").val(data.project_id);
            if ($("#prjnum").val() == "") {
                $("#prjnum").prop("readonly",false);
                $("#prjname").prop("readonly",false);
            } else
            {
                $("#prjnum").prop("readonly",true);
                $("#prjname").prop("readonly",true);
            }

        }
    });
}
);

$("#boc_form").ready(function ()
    {
        $("#load_img").hide();
        $("#id_xls_file").hide();
        var url_get_loaded_eos = "/eos/get_loaded_eos"
        var url_eos_addreq = "/eos/calc_req";


        $.ajax({
            url:url_get_loaded_eos,
            async:false,
            dataType:'json',
            success:function (data, status) {
//                console.log(data);
                if (data.prjnum != null || data.prjnum != undefined) {
                    $("#prjselect").val(data.prjnum);
                    $("#prjnum").val(data.prjnum);
                    var url_get_prj_name = "/eos/get_prj_name"
                    $.ajax({
                        url: url_get_prj_name,
                        async: false,
                        dataType: 'json',
                        data: { "project_id" : $("#prjnum").val() },
                        success: function(data, status){
                            $("#prjname").val(data.project_name);
                        }
                    });
                }

                for (var i = 1; i < data.req_count+1; ++i) {
                    req_line = {}
                    req_line["itemtype2"] = data["itemtype2_"+i];
                    req_line["itemtype1"] = data["itemtype1_"+i];
                    req_line["itemstatus"] = data["itemstatus_"+i];
                    req_line["servername"] = data["servername_"+i];
                    req_line["cpu_count"] = data["cpu_count_"+i];
                    req_line["ram_count"] = data["ram_count_"+i];
                    req_line["hdd_count"] = data["hdd_count_"+i];
                    req_line["san_count"] = data["san_count_"+i];
                    req_line["nas_count"] = data["nas_count_"+i];
                    req_line["item_count"] = data["item_count_"+i];
                    req_line["ostype"] = data["ostype_"+i];
                    req_line["platform_type"] = data["platform_type_"+i];
                    req_line["lan_segment"] = data["lan_segment_"+i];
                    req_line["db_type"] = data["db_type_" + i];
                    req_line["app_type"] = data["app_type_" + i];
                    req_line["cluster_type"] = data["cluster_type_"+i];
                    req_line["backup_type"] = data["backup_type_"+i];
                    req_line["price"] = data["price_"+i];
                    req_line["price_hw"] = data["price_hw_"+i];
                    req_line["price_lic"] = data["price_lic_"+i];
                    req_line["price_support"] = data["price_support_"+i];
                    req_line["utilization"] = data["utilization_"+i];

                    req_line["lic_symantec_count"] = data["lic_symantec_count_"+i];
                    req_line["lic_symantec_cost"] = data["lic_symantec_cost_"+i];
                    req_line["lic_ms_count"] = data["lic_ms_count_"+i];
                    req_line["lic_ms_cost"] = data["lic_ms_cost_"+i];
                    req_line["lic_vmware_count"] = data["lic_vmware_count_"+i];
                    req_line["lic_vmware_cost"] = data["lic_vmware_cost_"+i];
                    req_line["supp_symantec_count"] = data["supp_symantec_count_"+i];
                    req_line["supp_symantec_cost"] = data["supp_symantec_cost_"+i];
                    req_line["supp_rhel_count"] = data["supp_rhel_count_"+i];
                    req_line["supp_rhel_cost"] = data["supp_rhel_cost_"+i];
                    req_line["supp_vmware_count"] = data["supp_vmware_count_"+i];
                    req_line["supp_vmware_cost"] = data["supp_vmware_cost_"+i];


//                    console.log(req_line);
                    eos_items.push(req_line);
//                    console.log(eos_items);
//                    renderEos();
//                    $.ajax({
//                        type:'POST',
//                        url:url_eos_addreq,
//                        async:false,
//                        dataType:'json',
//                        data:{"json":JSON.stringify(req_line) },
//                        success:function (data, status) {
//                            error = data.error;
//                            console.log(data);
//                            eos_items.push(data);
//                            console.log(eos_items);
//                        }
//                    });

//                    eos_items.push(req_line);
                }
//                console.log(eos_items);
                renderEos();

            }
        });


    }

);